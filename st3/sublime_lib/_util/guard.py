from functools import wraps


def define_guard(guard_fn):
    def decorator(wrapped):
        @wraps(wrapped)
        def wrapper_guards(self, *args, **kwargs):
            ret_val = guard_fn(self)
            if hasattr(ret_val, '__enter__'):
                with ret_val:
                    return wrapped(self, *args, **kwargs)
            else:
                return wrapped(self, *args, **kwargs)

        return wrapper_guards

    return decorator
