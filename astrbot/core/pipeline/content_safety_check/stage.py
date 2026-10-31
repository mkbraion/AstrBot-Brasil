from collections.abc import AsyncGenerator

from astrbot.core import logger
from astrbot.core.message.components import Reply
from astrbot.core.message.message_event_result import MessageEventResult
from astrbot.core.platform.astr_message_event import AstrMessageEvent
from astrbot.core.utils.quoted_message.chain_parser import ReplyChainParser

from ..context import PipelineContext
from ..stage import Stage, register_stage
from .strategies.strategy import StrategySelector


@register_stage
class ContentSafetyCheckStage(Stage):
    """Verifica a segurança do conteúdo.

    Atualmente, apenas o conteúdo textual é analisado.
    """

    async def initialize(self, ctx: PipelineContext) -> None:
        config = ctx.astrbot_config["content_safety"]
        self.strategy_selector = StrategySelector(config)

    async def process(
        self,
        event: AstrMessageEvent,
        check_text: str | None = None,
    ) -> AsyncGenerator[None, None]:
        """Verifica a segurança do conteúdo."""
        if check_text is None:
            texts = [event.get_message_str()]
            reply_parser = ReplyChainParser()
            for component in event.get_messages():
                if isinstance(component, Reply) and (
                    quoted_text := reply_parser.extract_text_from_reply_component(
                        component
                    )
                ):
                    texts.append(quoted_text)
        else:
            texts = [check_text]

        ok, info = self.strategy_selector.check("\n".join(texts))
        if not ok:
            if event.is_at_or_wake_command:
                event.set_result(
                    MessageEventResult().message(
                        "Sua mensagem ou a resposta do modelo contém conteúdo "
                        "impróprio e foi bloqueada.",
                    ),
                )
                yield
            event.stop_event()
            logger.info(f"Falha na verificação de segurança do conteúdo: {info}")
            return
