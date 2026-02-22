from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, ContextManager, TypeVar
    from typing_extensions import ParamSpec, Concatenate
    _Self = TypeVar('_Self')
    _T = TypeVar('_T')
    _P = ParamSpec('_P')


def define_guard(
    guard_fn: Callable[[_Self], ContextManager[Any] | None]
) -> Callable[[Callable[Concatenate[_Self, _P], _T]], Callable[Concatenate[_Self, _P], _T]]:
    def decorator(wrapped: Callable[Concatenate[_Self, _P], _T]) -> Callable[Concatenate[_Self, _P], _T]:
        @wraps(wrapped)
        def wrapper(self: _Self, /, *args: _P.args, **kwargs: _P.kwargs) -> _T:
            ret_val = guard_fn(self)
            if ret_val is not None:
                with ret_val:
                    return wrapped(self, *args, **kwargs)
            else:
                return wrapped(self, *args, **kwargs)

        return wrapper

    return decorator
