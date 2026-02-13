from __future__ import annotations
from types import MethodType
from typing import TYPE_CHECKING

import weakref

if TYPE_CHECKING:
    from typing import Callable
    from typing_extensions import ParamSpec, TypeVar

    P = ParamSpec("P")
    T = TypeVar("T")

__all__ = ['weak_method']


def weak_method(method: Callable[P, T]) -> Callable[P, T | None]:
    assert isinstance(method, MethodType)
    self_ref = weakref.ref(method.__self__)
    function_ref = weakref.ref(method.__func__)

    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T | None:
        self = self_ref()
        function = function_ref()
        if self is not None and function is not None:
            return function(self, *args, **kwargs)
        return None

    return wrapped
