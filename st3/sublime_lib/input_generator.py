from sublime_plugin import CommandInputHandler, Command, ListInputHandler, TextInputHandler

from ._compat.typing import Callable, Generator, Optional, Union
from functools import wraps

FancyInputHandler = Union['GenericListInputHandler', 'GenericTextInputHandler']
GeneratorType = Generator[FancyInputHandler, object, None]


__all__ = ['input_generator', 'GenericListInputHandler', 'GenericTextInputHandler']


def input_generator(
    input_function: Callable[[Command, dict], GeneratorType],
) -> Callable[[Command, dict], Optional[FancyInputHandler]]:
    @wraps(input_function)
    def wrapped(self: Command, args: dict) -> Optional[FancyInputHandler]:
        return _next_input(input_function(self, args), None)

    return wrapped


def _next_input(gen: GeneratorType, value: object) -> Optional[FancyInputHandler]:
    try:
        next_input_handler = gen.send(value)
        next_input_handler._gen = gen
        return next_input_handler
    except StopIteration:
        return None


class GenericListInputHandler(ListInputHandler):
    _gen = None  # type: GeneratorType

    def __init__(
        self,
        *,
        name: str,
        items: list
    ) -> None:
        super().__init__()
        self._name = name
        self._items = items

    def name(self) -> str:
        return self._name

    def list_items(self) -> list:
        return self._items

    def next_input(self, args: dict) -> Optional[CommandInputHandler]:
        return _next_input(self._gen, args.get(self._name, None))


class GenericTextInputHandler(TextInputHandler):
    _gen = None  # type: GeneratorType

    def __init__(
        self,
        *,
        name: str
    ) -> None:
        super().__init__()
        self._name = name

    def name(self) -> str:
        return self._name

    def next_input(self, args: dict) -> Optional[CommandInputHandler]:
        return _next_input(self._gen, args.get(self._name, None))
