import weakref

from .._compat.typing import Callable, Any
from types import MethodType


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
