from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from astrbot.core.platform import AstrMessageEvent


class ActiveEventRegistry:
    """Mantém o mapeamento de unified_msg_origin para os eventos ativos.

    Permite encerrar eventos em processamento na sessão, como durante um reset.
    """

    def __init__(self) -> None:
        self._events: dict[str, set[AstrMessageEvent]] = defaultdict(set)
        self._agent_stop_callbacks: dict[AstrMessageEvent, Callable[[], None]] = {}
        self._background_tasks: dict[
            str, dict[asyncio.Task[None], AstrMessageEvent]
        ] = defaultdict(dict)
        self._background_cancel_requested: set[asyncio.Task[None]] = set()

    def register(self, event: AstrMessageEvent) -> None:
        self._events[event.unified_msg_origin].add(event)

    def unregister(self, event: AstrMessageEvent) -> None:
        umo = event.unified_msg_origin
        self._agent_stop_callbacks.pop(event, None)
        self._events[umo].discard(event)
        if not self._events[umo]:
            del self._events[umo]

    def register_agent_stop_callback(
        self,
        event: AstrMessageEvent,
        callback: Callable[[], None],
    ) -> None:
        """Registra uma função para interromper imediatamente o agente de um evento ativo.

        Argumentos:
            event: Evento responsável pela execução ativa do agente.
            callback: Função de retorno que solicita a interrupção da execução ativa.
        """
        self._agent_stop_callbacks[event] = callback

    def unregister_agent_stop_callback(self, event: AstrMessageEvent) -> None:
        """Remove a função de interrupção do agente associada a um evento.

        Argumentos:
            event: Evento cuja execução ativa do agente foi concluída.
        """
        self._agent_stop_callbacks.pop(event, None)

    def get_background_stop_signal(self, event: AstrMessageEvent) -> asyncio.Event:
        """Retorna o sinal de parada compartilhado da execução em segundo plano de um evento.

        Chamadas repetidas para o mesmo evento reutilizam o sinal, inclusive quando
        ele é propagado por referência para um evento de reativação em segundo
        plano. Novos eventos do usuário possuem sinais independentes.

        Argumentos:
            event: Evento responsável pela execução em segundo plano.

        Retorno:
            Sinal de parada em memória compartilhado pelo evento e suas reativações.
        """
        signal = event.get_extra("_background_stop_signal")
        if signal is None:
            signal = asyncio.Event()
            event.set_extra("_background_stop_signal", signal)
        if event.get_extra("agent_stop_requested"):
            signal.set()
        return signal

    def register_background_task(
        self,
        event: AstrMessageEvent,
        task: asyncio.Task[None],
    ) -> None:
        """Acompanha uma tarefa em segundo plano independentemente da execução principal.

        O registro mantém a tarefa e seu evento responsável pela origem unificada
        da mensagem até a conclusão. Se o evento já tiver parado, a tarefa
        será cancelada imediatamente.

        Argumentos:
            event: Evento responsável pela tarefa e pelo sinal de parada compartilhado.
            task: Tarefa em segundo plano a manter e remover após a conclusão.

        Retorno:
            None.
        """
        if task.done():
            return
        umo = event.unified_msg_origin
        self._background_tasks[umo][task] = event

        def remove_task(done_task: asyncio.Task[None]) -> None:
            tasks = self._background_tasks.get(umo)
            if tasks is not None:
                tasks.pop(done_task, None)
                if not tasks:
                    del self._background_tasks[umo]
            self._background_cancel_requested.discard(done_task)

        task.add_done_callback(remove_task)
        if self.get_background_stop_signal(event).is_set():
            self._background_cancel_requested.add(task)
            task.cancel()

    def stop_all(
        self,
        umo: str,
        exclude: AstrMessageEvent | None = None,
    ) -> int:
        """Encerra todos os eventos ativos e as tarefas em segundo plano do UMO informado.

        Argumentos:
            umo: Identificador da origem unificada da mensagem.
            exclude: Evento a excluir (normalmente o que iniciou o reset).

        Retorno:
            Quantidade de eventos encerrados.
        """
        events = set(self._events.get(umo, []))
        events.update(
            event
            for task, event in self._background_tasks.get(umo, {}).items()
            if not task.done()
        )
        for event in events:
            if event is not exclude:
                event.stop_event()
        return self.request_agent_stop_all(umo, exclude)

    def request_agent_stop_all(
        self,
        umo: str,
        exclude: AstrMessageEvent | None = None,
    ) -> int:
        """Solicita a interrupção dos agentes de todos os eventos ativos do UMO informado.

        Ao contrário de stop_all, não chama event.stop_event(), evitando
        interromper a propagação do evento e permitindo que etapas posteriores,
        como o salvamento do histórico, continuem.

        Argumentos:
            umo: Identificador da origem unificada da mensagem.
            exclude: Evento a excluir.

        Retorno:
            Quantidade de eventos que receberam a solicitação de parada, sem duplicações.
        """
        tasks = self._background_tasks.get(umo, {})
        events = set(self._events.get(umo, []))
        events.update(event for task, event in tasks.items() if not task.done())
        count = 0
        for event in events:
            if event is not exclude:
                event.set_extra("agent_stop_requested", True)
                self.get_background_stop_signal(event).set()
                callback = self._agent_stop_callbacks.get(event)
                if callback:
                    callback()
                count += 1
        for task, event in list(tasks.items()):
            if (
                event is not exclude
                and not task.done()
                and task not in self._background_cancel_requested
            ):
                # Solicitações repetidas de parada não devem interromper a limpeza do cancelamento em andamento.
                self._background_cancel_requested.add(task)
                task.cancel()
        return count


active_event_registry = ActiveEventRegistry()
