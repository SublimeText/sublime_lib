from threading import Condition, RLock

from types import TracebackType
from .._compat.typing import Optional, TypeVar, Generic, Callable

T = TypeVar('T')

__all__ = ['LockedState']


class LockedState(Generic[T]):
    """A value wrapped in a :class:`threading.Condition`.

    The condition uses a reentrant lock,
    so a thread may acquire it recursively.
    """
    def __init__(self, initial_state: T) -> None:
        self._state = initial_state
        self._condition = Condition(RLock())

    @property
    def state(self) -> T:
        """The current state."""
        return self._state

    def __enter__(self) -> T:
        """Acquire the condition and return the current state.
        """
        self._condition.acquire()

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: TracebackType
    ) -> None:
        self._condition.release()

    def set(self, state: T) -> None:
        """Set the state, acquiring the condition temporarily."""
        with self._condition:
            self._state = state
            self._condition.notify_all()

    def wait_for(
        self,
        predicate: Callable[[T], bool],
        timeout: Optional[float] = None
    ) -> bool:
        """Wait until the state meets the given `predicate`.

        Return ``True`` unless a given `timeout` expires,
        in which case return ``False``.
        """
        with self._condition:
            return bool(self._condition.wait_for(
                lambda: predicate(self.state),
                timeout
            ))
