from __future__ import annotations
from types import MethodType
from typing import Callable, Any

import weakref


__all__ = ['weak_method']


def weak_method(method: Callable) -> Callable:
    assert isinstance(method, MethodType)
    self_ref = weakref.ref(method.__self__)
    function_ref = weakref.ref(method.__func__)

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        self = self_ref()
        function = function_ref()
        if self is not None and function is not None:
            return function(self, *args, **kwargs)

    return wrapped
