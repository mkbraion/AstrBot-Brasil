from collections.abc import AsyncGenerator

from astrbot.core import logger
from astrbot.core.platform.astr_message_event import AstrMessageEvent
from astrbot.core.platform.message_type import MessageType

from ..context import PipelineContext
from ..stage import Stage, register_stage


@register_stage
class WhitelistCheckStage(Stage):
    """Verifica a lista de permissões de grupos e conversas privadas."""

    async def initialize(self, ctx: PipelineContext) -> None:
        self.enable_whitelist_check = ctx.astrbot_config["platform_settings"][
            "enable_id_white_list"
        ]
        self.whitelist = ctx.astrbot_config["platform_settings"]["id_whitelist"]
        self.whitelist = [
            str(i).strip() for i in self.whitelist if str(i).strip() != ""
        ]
        self.wl_ignore_admin_on_group = ctx.astrbot_config["platform_settings"][
            "wl_ignore_admin_on_group"
        ]
        self.wl_ignore_admin_on_friend = ctx.astrbot_config["platform_settings"][
            "wl_ignore_admin_on_friend"
        ]
        self.wl_log = ctx.astrbot_config["platform_settings"]["id_whitelist_log"]

    async def process(
        self,
        event: AstrMessageEvent,
    ) -> None | AsyncGenerator[None, None]:
        if not self.enable_whitelist_check:
            # Verificação da lista de permissões desativada
            return

        if len(self.whitelist) == 0:
            # Lista de permissões vazia: nenhuma verificação necessária
            return

        if event.get_platform_name() == "webchat":
            # WebChat está isento da verificação
            return

        # Verifica se a sessão está na lista de permissões
        if self.wl_ignore_admin_on_group:
            if (
                event.role == "admin"
                and event.get_message_type() == MessageType.GROUP_MESSAGE
            ):
                return
        if self.wl_ignore_admin_on_friend:
            if (
                event.role == "admin"
                and event.get_message_type() == MessageType.FRIEND_MESSAGE
            ):
                return
        if (
            event.unified_msg_origin not in self.whitelist
            and str(event.get_group_id()).strip() not in self.whitelist
        ):
            if self.wl_log:
                logger.info(
                    f"O ID de sessão {event.unified_msg_origin} não está na lista de "
                    "permissões; por isso, a propagação do evento foi interrompida. "
                    "Adicione esse ID na interface web, em Configurações > Controle "
                    "de acesso > Lista de permissões > IDs permitidos, usando o "
                    "perfil atribuído a este bot.",
                )
            event.stop_event()
