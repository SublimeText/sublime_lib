from threading import Condition

from types import TracebackType
from .._compat.typing import Optional, TypeVar, Generic, Callable

T = TypeVar('T')
R = TypeVar('R')

__all__ = ['LockedState']


class LockedState(Generic[T]):
    def __init__(self, initial_state: T) -> None:
        self._state = initial_state
        self._condition = Condition()  # RLock

    @property
    def state(self) -> T:
        return self._state

    def __enter__(self) -> T:
        self._condition.acquire()
        return self.state

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: TracebackType
    ) -> None:
        self._condition.release()

    def set(self, state: T) -> None:
        with self._condition:
            self._state = state
            self._condition.notify_all()

    def wait_for(
        self,
        predicate: Callable[[T], R],
        timeout: Optional[float] = None
    ) -> R:
        with self._condition:
            return self._condition.wait_for(
                lambda: predicate(self.state),
                timeout
            )
