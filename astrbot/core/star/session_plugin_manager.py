"""Gerenciador de plugins de sessão - controla a ativação dos plugins em cada sessão"""

from astrbot.core import logger, sp
from astrbot.core.platform.astr_message_event import AstrMessageEvent


class SessionPluginManager:
    """Gerencia o estado de ativação dos plugins por sessão"""

    @staticmethod
    async def is_plugin_enabled_for_session(
        session_id: str,
        plugin_name: str,
    ) -> bool:
        """Verifica se o plugin está ativado na sessão informada

        Args:
            session_id: ID da sessão (unified_msg_origin)
            plugin_name: Nome do plugin

        Returns:
            bool: True indica ativado; False indica desativado

        """
        # Obtém a configuração de plugins da sessão
        session_plugin_config = await sp.get_async(
            scope="umo",
            scope_id=session_id,
            key="session_plugin_config",
            default={},
        )
        session_config = session_plugin_config.get(session_id, {})

        enabled_plugins = session_config.get("enabled_plugins", [])
        disabled_plugins = session_config.get("disabled_plugins", [])

        # Se o plugin estiver na lista de desativados, retorna False
        if plugin_name in disabled_plugins:
            return False

        # Se o plugin estiver na lista de ativados, retorna True
        if plugin_name in enabled_plugins:
            return True

        # Se não houver configuração, mantém ativado por padrão (compatibilidade)
        return True

    @staticmethod
    async def filter_handlers_by_session(
        event: AstrMessageEvent,
        handlers: list,
    ) -> list:
        """Filtra os manipuladores de acordo com a configuração da sessão

        Args:
            event: Evento de mensagem
            handlers: Lista original de manipuladores

        Returns:
            List: Lista de manipuladores filtrada

        """
        from astrbot.core.star.star import star_map

        session_id = event.unified_msg_origin
        filtered_handlers = []

        session_plugin_config = await sp.get_async(
            scope="umo",
            scope_id=session_id,
            key="session_plugin_config",
            default={},
        )
        session_config = session_plugin_config.get(session_id, {})
        disabled_plugins = session_config.get("disabled_plugins", [])

        for handler in handlers:
            # Obtém o plugin associado ao manipulador
            plugin = star_map.get(handler.handler_module_path)
            if not plugin:
                # Se os metadados do plugin não forem encontrados, permite a execução (pode ser um plugin do sistema)
                filtered_handlers.append(handler)
                continue

            # Ignora plugins reservados (plugins do sistema)
            if plugin.reserved:
                filtered_handlers.append(handler)
                continue

            if plugin.name is None:
                continue

            # Verifica se o plugin está ativado na sessão atual
            if plugin.name in disabled_plugins:
                logger.debug(
                    f"O plugin {plugin.name} está desativado na sessão {session_id}; "
                    f"ignorando o manipulador {handler.handler_name}.",
                )
            else:
                filtered_handlers.append(handler)

        return filtered_handlers
