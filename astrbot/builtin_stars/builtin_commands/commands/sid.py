"""会话ID命令"""

from astrbot.api import star
from astrbot.api.event import AstrMessageEvent, MessageEventResult


class SIDCommand:
    """会话ID命令类"""

    def __init__(self, context: star.Context) -> None:
        self.context = context

    async def sid(self, event: AstrMessageEvent) -> None:
        """获取消息来源信息"""
        sid = event.unified_msg_origin
        user_id = str(event.get_sender_id())
        umo_platform = event.session.platform_id
        umo_msg_type = event.session.message_type.value
        umo_session_id = event.session.session_id
        ret = (
            f"UMO: {sid}\n"
            f"UID: {user_id}\n"
            "Use UMO para configurar a lista de permissões e as rotas; "
            "use UID para definir a lista de administradores.\n\n"
            "Informações da sessão:\n"
            f"ID do bot: {umo_platform}\n"
            f"Tipo de mensagem: {umo_msg_type}\n"
            f"ID da sessão: {umo_session_id}\n"
        )

        if (
            self.context.get_config()["platform_settings"]["unique_session"]
            and event.get_group_id()
        ):
            ret += f"\n\nID do grupo: {event.get_group_id()}. Adicione este ID à lista de permissões para permitir todo o grupo."

        event.set_result(MessageEventResult().message(ret).use_t2i(False))
