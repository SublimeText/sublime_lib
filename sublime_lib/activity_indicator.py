from __future__ import annotations
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from threading import Lock
from types import TracebackType
from uuid import uuid4

import sublime

from ._util.weak_method import weak_method

__all__ = ['ActivityIndicator']


class StatusTarget(metaclass=ABCMeta):
    @abstractmethod
    def set(self, message: str) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...


class WindowTarget(StatusTarget):
    def __init__(self, window: sublime.Window) -> None:
        self.window: sublime.Window = window

    def set(self, message: str) -> None:
        self.window.status_message(message)

    def clear(self) -> None:
        self.window.status_message("")


class ViewTarget(StatusTarget):
    def __init__(self, view: sublime.View, key: str | None = None) -> None:
        self.view: sublime.View = view
        if key is None:
            self.key: str = f"_{uuid4()!s}"
        else:
            self.key = key

    def set(self, message: str) -> None:
        self.view.set_status(self.key, message)

    def clear(self) -> None:
        self.view.erase_status(self.key)


class ActivityIndicator:
    """
    An animated text-based indicator to show that some activity is in progress.

    The `target` argument should be a :class:`sublime.View` or :class:`sublime.Window`.
    The indicator will be shown in the status bar of that view or window.
    If `label` is provided, then it will be shown next to the animation.

    :class:`ActivityIndicator` can be used as a context manager.

    .. versionadded:: 1.4
    """

    class State(IntEnum):
        STOPPED = 0
        STOPPING = 1
        RUNNING = 2

    frames: str | list[str] = "⣷⣯⣟⡿⢿⣻⣽⣾"
    interval: int = 100

    def __init__(
        self,
        target: StatusTarget | sublime.View | sublime.Window,
        label: str | None = None,
    ) -> None:
        self.label: str | None = label

        if isinstance(target, sublime.View):
            self._target: StatusTarget = ViewTarget(target)
        elif isinstance(target, sublime.Window):
            self._target = WindowTarget(target)
        else:
            self._target = target

        self._lock: Lock = Lock()
        self._state: int = self.State.STOPPED
        self._ticks: int = 0
        self._tick_ref = weak_method(self._tick)

    def __del__(self) -> None:
        self.stop()
        self._target.clear()

    def __enter__(self) -> ActivityIndicator:
        self.start()
        return self

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
            if self._state == self.State.RUNNING:
                raise ValueError("Activity indicator is already running!")
            elif self._state == self.State.STOPPING:
                self._state = self.State.RUNNING
            else:
                self.update()
                sublime.set_timeout(self._tick_ref, self.interval)
                self._state = self.State.RUNNING

    def stop(self) -> None:
        """
        Stop displaying the indicator.

        If the indicator is not running, do nothing.
        """
        with self._lock:
            if self._state != self.State.STOPPED:
                self._state = self.State.STOPPING

    def _tick(self) -> None:
        with self._lock:
            if self._state == self.State.RUNNING:
                self.tick()
                sublime.set_timeout(self._tick_ref, self.interval)
                return
            self._state = self.State.STOPPED
        self._target.clear()

    def tick(self) -> None:
        self._ticks += 1
        self.update()

    def update(self) -> None:
        self._target.set(self.render(self._ticks))

    def render(self, ticks: int) -> str:
        text = self.frames[ticks % len(self.frames)]
        if self.label:
            text += " " + self.label
        return text
