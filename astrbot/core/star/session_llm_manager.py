"""Gerenciador de serviços de sessão - controla a ativação de LLM, TTS e outros serviços por sessão"""

from astrbot.core import logger, sp
from astrbot.core.platform.astr_message_event import AstrMessageEvent


class SessionServiceManager:
    """Gerencia a ativação de serviços por sessão, incluindo LLM e TTS"""

    # =============================================================================
    # Métodos relacionados ao LLM
    # =============================================================================

    @staticmethod
    async def is_llm_enabled_for_session(session_id: str) -> bool:
        """Verifica se o LLM está ativado na sessão informada

        Args:
            session_id: ID da sessão (unified_msg_origin)

        Returns:
            bool: True indica ativado; False indica desativado

        """
        # Obtém a configuração de serviços da sessão
        session_services = await sp.get_async(
            scope="umo",
            scope_id=session_id,
            key="session_service_config",
            default={},
        )

        # Se houver um estado configurado para o LLM nesta sessão, retorna esse estado
        llm_enabled = session_services.get("llm_enabled")
        if llm_enabled is not None:
            return llm_enabled

        # Se não houver configuração, mantém ativado por padrão (compatibilidade)
        return True

    @staticmethod
    async def set_llm_status_for_session(session_id: str, enabled: bool) -> None:
        """Define o estado de ativação do LLM na sessão informada

        Args:
            session_id: ID da sessão (unified_msg_origin)
            enabled: True indica ativado; False indica desativado

        """
        session_config = (
            await sp.get_async(
                scope="umo",
                scope_id=session_id,
                key="session_service_config",
                default={},
            )
            or {}
        )
        session_config["llm_enabled"] = enabled
        await sp.put_async(
            scope="umo",
            scope_id=session_id,
            key="session_service_config",
            value=session_config,
        )

    @staticmethod
    async def should_process_llm_request(event: AstrMessageEvent) -> bool:
        """Verifica se a solicitação ao LLM deve ser processada

        Args:
            event: Evento de mensagem

        Returns:
            bool: True indica processar; False indica ignorar

        """
        session_id = event.unified_msg_origin
        return await SessionServiceManager.is_llm_enabled_for_session(session_id)

    # =============================================================================
    # Métodos relacionados ao TTS
    # =============================================================================

    @staticmethod
    async def is_tts_enabled_for_session(session_id: str) -> bool:
        """Verifica se o TTS está ativado na sessão informada

        Args:
            session_id: ID da sessão (unified_msg_origin)

        Returns:
            bool: True indica ativado; False indica desativado

        """
        # Obtém a configuração de serviços da sessão
        session_services = await sp.get_async(
            scope="umo",
            scope_id=session_id,
            key="session_service_config",
            default={},
        )

        # Se houver um estado configurado para o TTS nesta sessão, retorna esse estado
        tts_enabled = session_services.get("tts_enabled")
        if tts_enabled is not None:
            return tts_enabled

        # Se não houver configuração, mantém ativado por padrão (compatibilidade)
        return True

    @staticmethod
    async def set_tts_status_for_session(session_id: str, enabled: bool) -> None:
        """Define o estado de ativação do TTS na sessão informada

        Args:
            session_id: ID da sessão (unified_msg_origin)
            enabled: True indica ativado; False indica desativado

        """
        session_config = (
            await sp.get_async(
                scope="umo",
                scope_id=session_id,
                key="session_service_config",
                default={},
            )
            or {}
        )
        session_config["tts_enabled"] = enabled
        await sp.put_async(
            scope="umo",
            scope_id=session_id,
            key="session_service_config",
            value=session_config,
        )

        logger.info(
            f"O estado do TTS na sessão {session_id} foi atualizado para "
            f"{'ativado' if enabled else 'desativado'}.",
        )

    @staticmethod
    async def should_process_tts_request(event: AstrMessageEvent) -> bool:
        """Verifica se a solicitação ao TTS deve ser processada

        Args:
            event: Evento de mensagem

        Returns:
            bool: True indica processar; False indica ignorar

        """
        session_id = event.unified_msg_origin
        return await SessionServiceManager.is_tts_enabled_for_session(session_id)

    # =============================================================================
    # Métodos relacionados à ativação geral da sessão
    # =============================================================================

    @staticmethod
    async def is_session_enabled(session_id: str) -> bool:
        """Verifica se a sessão está ativada

        Args:
            session_id: ID da sessão (unified_msg_origin)

        Returns:
            bool: True indica ativado; False indica desativado

        """
        # Obtém a configuração de serviços da sessão
        session_services = await sp.get_async(
            scope="umo",
            scope_id=session_id,
            key="session_service_config",
            default={},
        )

        # Se houver um estado geral configurado para a sessão, retorna esse estado
        session_enabled = session_services.get("session_enabled")
        if session_enabled is not None:
            return session_enabled

        # Se não houver configuração, mantém ativado por padrão (compatibilidade)
        return True
