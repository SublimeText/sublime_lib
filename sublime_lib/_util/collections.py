from __future__ import annotations
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable
    from typing_extensions import TypeAlias

    Value: TypeAlias = bool | str | int | float | list[Any] | dict[str, Any] | None

__all__ = ['projection', 'get_selector']


def projection(d: Mapping[str, Value], keys: Mapping[str, str] | Iterable[str]) -> Value:
    """
    Return a new :class:`Mapping` with keys of ``d`` restricted to values in ``keys``.

    .. code-block:: python

       >>> projection({'a': 1, 'b': 2}, ['b'])
       {'b': 2}

    If ``keys`` is a :class:`Mapping`, then it maps keys of the original Mapping to
    keys of the result:

    .. code-block:: python

       >>> projection({'a': 1, 'b': 2}, {'b': 'c'})
       {'c': 2}
    """
    if isinstance(keys, Mapping):
        return {
            new_key: d[original_key]
            for original_key, new_key in keys.items()
            if original_key in d
        }
    else:
        return {
            key: d[key]
            for key in keys
            if key in d
        }


def get_selector(
    selector: Callable[[Mapping[str, Value]], Value] | Iterable[str] | str,
    default_value: Value = None
) -> Callable[[Mapping[str, Value]], Value]:
    if callable(selector):
        return selector
    elif isinstance(selector, str):
        return lambda this: this.get(selector, default_value)
    elif isinstance(selector, Iterable):
        return lambda this: projection(this, selector)
    else:
        raise TypeError(
            'The selector should be a function, string, or iterable of strings.'
        )
