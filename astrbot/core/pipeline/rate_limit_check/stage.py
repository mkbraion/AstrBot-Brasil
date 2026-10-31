import asyncio
from collections import defaultdict, deque
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

from astrbot.core import logger
from astrbot.core.config.astrbot_config import RateLimitStrategy
from astrbot.core.platform.astr_message_event import AstrMessageEvent

from ..context import PipelineContext
from ..stage import Stage, register_stage


@register_stage
class RateLimitStage(Stage):
    """Verifica se é necessário limitar o envio de mensagens.

    Usa o algoritmo de janela fixa (Fixed Window).
    Quando o limite é atingido, pausa o pipeline até a próxima janela de tempo.
    """

    def __init__(self) -> None:
        # Armazena a fila de horários das requisições de cada sessão
        self.event_timestamps: defaultdict[str, deque[datetime]] = defaultdict(deque)
        # Usa um bloqueio por sessão para evitar conflitos de concorrência
        self.locks: defaultdict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        # Parâmetros de limitação de taxa
        self.rate_limit_count: int = 0
        self.rate_limit_time: timedelta = timedelta(0)

    async def initialize(self, ctx: PipelineContext) -> None:
        """Inicializa os parâmetros de limitação de taxa conforme a configuração."""
        self.rate_limit_count = ctx.astrbot_config["platform_settings"]["rate_limit"][
            "count"
        ]
        self.rate_limit_time = timedelta(
            seconds=ctx.astrbot_config["platform_settings"]["rate_limit"]["time"],
        )
        self.rl_strategy = ctx.astrbot_config["platform_settings"]["rate_limit"][
            "strategy"
        ]  # Modos: stall (aguardar) ou discard (descartar)

    async def process(
        self,
        event: AstrMessageEvent,
    ) -> None | AsyncGenerator[None, None]:
        """Verifica e aplica a limitação de taxa. Quando o limite é atingido,
        o pipeline aguarda e retoma automaticamente na próxima janela.

        Args:
            event (AstrMessageEvent): Evento da mensagem atual.

        Returns:
            None ou AsyncGenerator[None, None]: Resultado do processamento.

        """
        if self.rate_limit_count <= 0:
            return

        umo = event.unified_msg_origin

        async with self.locks[umo]:  # Impede alterações simultâneas na fila da mesma sessão
            now = datetime.now()
            # Repete a verificação do limite até que a condição seja atendida
            while True:
                timestamps = self.event_timestamps[umo]
                self._remove_expired_timestamps(timestamps, now)

                if self.rate_limit_count <= 0:
                    break
                if len(timestamps) < self.rate_limit_count:
                    timestamps.append(now)
                    break
                next_window_time = timestamps[0] + self.rate_limit_time
                stall_duration = (next_window_time - now).total_seconds() + 0.3

                match self.rl_strategy:
                    case RateLimitStrategy.STALL.value:
                        logger.info(
                            f"A sessão {umo} atingiu o limite de requisições. O processamento "
                            f"será pausado por {stall_duration:.2f} segundos, conforme "
                            "a política de limitação de taxa.",
                        )
                        await asyncio.sleep(stall_duration)
                        now = datetime.now()
                    case RateLimitStrategy.DISCARD.value:
                        logger.info(
                            f"A sessão {umo} atingiu o limite de requisições. Esta solicitação "
                            "foi descartada conforme a política de limitação de taxa; "
                            f"o limite será redefinido em {stall_duration:.2f} segundos.",
                        )
                        return event.stop_event()

    def _remove_expired_timestamps(
        self,
        timestamps: deque[datetime],
        now: datetime,
    ) -> None:
        """Remove os registros de horário fora da janela atual.

        Args:
            timestamps (deque[datetime]): Fila de horários da sessão atual.
            now (datetime): Horário atual usado para calcular a expiração.

        """
        expiry_threshold: datetime = now - self.rate_limit_time
        while timestamps and timestamps[0] < expiry_threshold:
            timestamps.popleft()
