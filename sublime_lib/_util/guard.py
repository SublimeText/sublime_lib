from __future__ import annotations
from functools import wraps
from typing import Any, Callable, ContextManager, TypeVar


_Self = TypeVar('_Self')
_WrappedType = Callable[..., Any]


def define_guard(
    guard_fn: Callable[[_Self], ContextManager | None]
) -> Callable[[_WrappedType], _WrappedType]:
    def decorator(wrapped: _WrappedType) -> _WrappedType:
        @wraps(wrapped)
        def wrapper_guards(self: _Self, *args: Any, **kwargs: Any) -> Any:
            ret_val = guard_fn(self)
            if ret_val is not None:
                with ret_val:
                    return wrapped(self, *args, **kwargs)
            else:
                return wrapped(self, *args, **kwargs)

        return wrapper_guards

    return decorator
