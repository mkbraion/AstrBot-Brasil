import asyncio
import threading
import weakref
from collections import defaultdict
from contextlib import asynccontextmanager


class _PerLoopSessionLockManager:
    """Gerenciador de bloqueios de sessão por loop de eventos; mantém a semântica simples original."""

    def __init__(self) -> None:
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        self._lock_count: dict[str, int] = defaultdict(int)
        self._access_lock = asyncio.Lock()

    @asynccontextmanager
    async def acquire_lock(self, session_id: str):
        async with self._access_lock:
            lock = self._locks[session_id]
            self._lock_count[session_id] += 1

        try:
            async with lock:
                yield
        finally:
            async with self._access_lock:
                self._lock_count[session_id] -= 1
                if self._lock_count[session_id] == 0:
                    self._locks.pop(session_id, None)
                    self._lock_count.pop(session_id, None)


class SessionLockManager:
    """Gerenciador de bloqueios de sessão seguro entre threads, com isolamento por loop de eventos."""

    def __init__(self) -> None:
        self._state_guard = threading.Lock()
        self._loop_managers: weakref.WeakKeyDictionary[
            asyncio.AbstractEventLoop, _PerLoopSessionLockManager
        ] = weakref.WeakKeyDictionary()

    def _get_loop_manager(self) -> _PerLoopSessionLockManager:
        """Obtém o gerenciador de bloqueios do loop de eventos atual."""
        loop = asyncio.get_running_loop()
        with self._state_guard:
            return self._loop_managers.setdefault(loop, _PerLoopSessionLockManager())

    @asynccontextmanager
    async def acquire_lock(self, session_id: str):
        manager = self._get_loop_manager()
        async with manager.acquire_lock(session_id):
            yield


session_lock_manager = SessionLockManager()
