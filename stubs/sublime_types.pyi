from typing_extensions import TypeAlias
from sublime import KindId, CompletionItem

DIP: TypeAlias = float
Vector: TypeAlias = tuple[DIP, DIP]
Point: TypeAlias = int
Value: TypeAlias = bool | str | int | float | list[Value] | dict[str, Value] | None
CommandArgs: TypeAlias = dict[str, Value] | None
Kind: TypeAlias = tuple[KindId, str, str]
Event: TypeAlias = dict[str, Value]
CompletionValue: TypeAlias = str | tuple[str, str] | CompletionItem
