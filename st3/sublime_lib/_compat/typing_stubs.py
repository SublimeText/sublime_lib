
class _TypeMeta(type):
    def __getattr__(self, *args):
        name = '{}[{}]'.format(
            self.name,
            ', '.join(arg.name for name in args)
        )
        return _TypeMeta(name, (), {})

class Type(metaclass=_TypeMeta):
    pass

class Any(Type):
    pass

class Callable(Type):
    pass

class Optional(Type):
    pass
