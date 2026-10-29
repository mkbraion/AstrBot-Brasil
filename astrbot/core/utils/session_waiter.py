"""Controle de sessões"""

import abc
import asyncio
import copy
import functools
import time
from collections.abc import Awaitable, Callable
from typing import Any

import astrbot.core.message.components as Comp
from astrbot.core.platform import AstrMessageEvent

USER_SESSIONS: dict[str, "SessionWaiter"] = {}  # Armazena instâncias de SessionWaiter
FILTERS: list["SessionFilter"] = []  # Armazena instâncias de SessionFilter


class SessionController:
    """Controla se uma sessão foi encerrada"""

    def __init__(self) -> None:
        self.future = asyncio.Future()
        self.current_event: asyncio.Event | None = None
        """Evento assíncrono atualmente aguardado"""
        self.ts: float | None = None
        """Horário de início da última chamada de keep"""
        self.timeout: float | int | None = None
        """Tempo limite definido na última chamada de keep"""

        self.history_chains: list[list[Comp.BaseMessageComponent]] = []

    def stop(self, error: Exception | None = None) -> None:
        """Encerra imediatamente esta sessão"""
        if not self.future.done():
            if error:
                self.future.set_exception(error)
            else:
                self.future.set_result(None)

    def keep(self, timeout: float = 0, reset_timeout=False) -> None:
        """Mantém esta sessão ativa

        Args:
            timeout (float): Obrigatório. Tempo limite da sessão.
            Quando reset_timeout for True, reinicia o tempo limite. timeout deve ser > 0; se for <= 0, encerra a sessão imediatamente.
            Quando reset_timeout for False, mantém o prazo anterior: novo timeout = tempo restante + timeout (que pode ser < 0).

        """
        new_ts = time.time()

        if reset_timeout:
            if timeout <= 0:
                self.stop()
                return
        else:
            assert self.timeout is not None
            assert self.ts is not None
            left_timeout = self.timeout - (new_ts - self.ts)
            timeout = left_timeout + timeout
            if timeout <= 0:
                self.stop()
                return

        if self.current_event and not self.current_event.is_set():
            self.current_event.set()  # Sinaliza o encerramento do keep anterior

        new_event = asyncio.Event()
        self.ts = new_ts
        self.current_event = new_event
        self.timeout = timeout

        asyncio.create_task(self._holding(new_event, timeout))  # Inicia um novo keep

    async def _holding(self, event: asyncio.Event, timeout: float) -> None:
        """Aguarda a conclusão do evento ou o esgotamento do prazo"""
        try:
            await asyncio.wait_for(event.wait(), timeout)
        except asyncio.TimeoutError:
            if not self.future.done():
                self.future.set_exception(TimeoutError("Tempo limite esgotado"))
        except asyncio.CancelledError:
            pass  # Evita propagar o erro
        # finally:

    def get_history_chains(self) -> list[list[Comp.BaseMessageComponent]]:
        """Obtém o histórico das cadeias de mensagens"""
        return self.history_chains


class SessionFilter:
    """Define como identificar uma sessão"""

    @abc.abstractmethod
    def filter(self, event: AstrMessageEvent) -> str:
        """Retorna o identificador da sessão com base no evento"""


class DefaultSessionFilter(SessionFilter):
    def filter(self, event: AstrMessageEvent) -> str:
        """Implementação padrão: usa a origem unificada da mensagem como identificador da sessão"""
        return event.unified_msg_origin


class SessionWaiter:
    def __init__(
        self,
        session_filter: SessionFilter,
        session_id: str,
        record_history_chains: bool,
    ) -> None:
        self.session_id = session_id
        self.session_filter = session_filter
        self.handler: (
            Callable[[SessionController, AstrMessageEvent], Awaitable[Any]] | None
        ) = None  # Função de tratamento

        self.session_controller = SessionController()
        self.record_history_chains = record_history_chains
        """Indica se o histórico das cadeias de mensagens será registrado"""

        self._lock = asyncio.Lock()
        """Garante que cada sessão tenha apenas um acionamento por vez"""

    async def register_wait(
        self,
        handler: Callable[[SessionController, AstrMessageEvent], Awaitable[Any]],
        timeout: int = 30,
    ) -> Any:
        """Aguarda e processa uma entrada externa"""
        self.handler = handler
        USER_SESSIONS[self.session_id] = self

        # Inicia o período de manutenção da sessão
        self.session_controller.keep(timeout, reset_timeout=True)

        try:
            return await self.session_controller.future
        finally:
            # Limpa uma única vez após sucesso, falha ou cancelamento. Um filtro
            # compartilhado pode ter outro registro que não deve ser removido duas vezes.
            self._cleanup()

    def _cleanup(self, error: Exception | None = None) -> None:
        """Limpa os recursos da sessão"""
        USER_SESSIONS.pop(self.session_id, None)
        try:
            FILTERS.remove(self.session_filter)
        except ValueError:
            pass
        self.session_controller.stop(error)

    @classmethod
    async def trigger(cls, session_id: str, event: AstrMessageEvent) -> None:
        """Uma entrada externa aciona o processamento da sessão"""
        session = USER_SESSIONS.get(session_id)
        if not session or session.session_controller.future.done():
            return

        async with session._lock:
            if not session.session_controller.future.done():
                if session.record_history_chains:
                    session.session_controller.history_chains.append(
                        [copy.deepcopy(comp) for comp in event.get_messages()],
                    )
                try:
                    # TODO: Usar create_task e acompanhar a tarefa para impedir que o handler continue após o tempo limite
                    assert session.handler is not None
                    await session.handler(session.session_controller, event)
                except Exception as e:
                    session.session_controller.stop(e)


def session_waiter(timeout: int = 30, record_history_chains: bool = False):
    """Decorador: registra automaticamente a função como manipulador de SessionWaiter e aguarda uma entrada externa para executá-la.

    :param timeout: Tempo limite (em segundos)
    :param record_history_chain: Se deve registrar automaticamente o histórico das cadeias de mensagens. Pode ser obtido com controller.get_history_chains() (cópia profunda).
    """

    def decorator(
        func: Callable[[SessionController, AstrMessageEvent], Awaitable[Any]],
    ):
        @functools.wraps(func)
        async def wrapper(
            event: AstrMessageEvent,
            session_filter: SessionFilter | None = None,
            *args,
            **kwargs,
        ):
            if not session_filter:
                session_filter = DefaultSessionFilter()
            if not isinstance(session_filter, SessionFilter):
                raise ValueError("session_filter deve ser um SessionFilter")

            session_id = session_filter.filter(event)
            FILTERS.append(session_filter)

            waiter = SessionWaiter(session_filter, session_id, record_history_chains)
            return await waiter.register_wait(func, timeout)

        return wrapper

    return decorator
