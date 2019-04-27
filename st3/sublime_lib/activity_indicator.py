import sublime

from threading import Thread
from uuid import uuid4

from ._compat.typing import Optional, Union
from types import TracebackType
from abc import ABCMeta, abstractmethod

from ._util.locked_state import LockedState


__all__ = ['ActivityIndicator']


class StatusTarget(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def set(self, message: str) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...


class WindowTarget(StatusTarget):
    def __init__(self, window: sublime.Window) -> None:
        self.window = window

    def set(self, message: str) -> None:
        self.window.status_message(message)

    def clear(self) -> None:
        self.window.status_message("")


class ViewTarget(StatusTarget):
    def __init__(self, view: sublime.View, key: Optional[str] = None) -> None:
        self.view = view
        if key is None:
            self.key = '_{!s}'.format(uuid4())
        else:
            self.key = key

    def set(self, message: str) -> None:
        self.view.set_status(self.key, message)

    def clear(self) -> None:
        self.view.erase_status(self.key)


class ActivityIndicator:
    width = 10  # type: int
    interval = 100  # type: float

    _target = None  # type: StatusTarget
    _running = None  # type: LockedState[bool]

    def __init__(
        self,
        target: Union[StatusTarget, sublime.View, sublime.Window],
        label: Optional[str] = None,
    ) -> None:
        self.label = label

        if isinstance(target, sublime.View):
            self._target = ViewTarget(target)
        elif isinstance(target, sublime.Window):
            self._target = WindowTarget(target)
        else:
            self._target = target

        self._ticks = 0

        self._running = LockedState(False)

    def __enter__(self) -> None:
        self.start()

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: TracebackType
    ) -> None:
        self.stop()

    def start(self) -> None:
        with self._running as is_running:
            if is_running:
                raise ValueError('Timer is already running.')
            else:
                self._running.set(True)
                self.update()
                Thread(
                    name=self.label,
                    target=self._run,
                ).start()

    def stop(self) -> None:
        self._running.set(False)
        self._target.clear()

    def _run(self) -> None:
        while not self._running.wait_for(lambda state: not state, self.interval / 1000):
            self.tick()

    def tick(self) -> None:
        self._ticks += 1
        self.update()

    def update(self) -> None:
        self._target.set(self.render(self._ticks))

    def render(self, ticks: int) -> str:
        status = ticks % (2 * self.width)
        before = min(status, (2 * self.width) - status)
        after = self.width - before

        return "{}[{}={}]".format(
            self.label + ' ' if self.label else '',
            " " * before,
            " " * after,
        )
