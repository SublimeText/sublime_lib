import sublime

from uuid import uuid4
from threading import Lock

from ._compat.typing import Optional, Union
from types import TracebackType
from abc import ABCMeta, abstractmethod


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


class SchedulerState:
    running = False
    stopping = False


class ActivityIndicator:
    """
    An animated text-based indicator to show that some activity is in progress.

    The `target` argument should be a :class:`sublime.View` or :class:`sublime.Window`.
    The indicator will be shown in the status bar of that view or window.
    If `label` is provided, then it will be shown next to the animation.

    :class:`ActivityIndicator` can be used as a context manager.

    .. versionadded:: 1.4
    """
    width = 10  # type: int
    interval = 100  # type: int

    _target = None  # type: StatusTarget
    _ticks = 0
    _running = False
    _stopping = False

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

        self._lock = Lock()

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
        """
        Start displaying the indicator and animate it.

        :raise ValueError: if the indicator is already running.
        """
        with self._lock:
            if self._running and not self._stopping:
                raise ValueError('Timer is already running')
            elif self._stopping:
                self._stopping = False
            else:
                self._running = True
                self.update()
                sublime.set_timeout(self._run, self.interval)

    def stop(self) -> None:
        """
        Stop displaying the indicator.

        If the indicator is not running, do nothing.
        """
        with self._lock:
            if self._running:
                self._stopping = True

    def _run(self) -> None:
        with self._lock:
            if self._stopping:
                self._running = self._stopping = False
                self._target.clear()
            else:
                self.tick()
                sublime.set_timeout(self._run, self.interval)

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
