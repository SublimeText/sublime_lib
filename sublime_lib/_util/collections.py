from __future__ import annotations
from collections.abc import Mapping, Sequence
from typing import Callable, Iterable, TypeVar


_V = TypeVar('_V')

__all__ = ['projection', 'get_selector', 'isiterable', 'ismapping', 'is_sequence_not_str']


def projection(
    d: dict[str, _V],
    keys: dict[str, str] | Iterable[str]
) -> dict[str, _V]:
    """
    Return a new :class:`dict` with keys of ``d`` restricted to values in ``keys``.

    .. code-block:: python

       >>> projection({'a': 1, 'b': 2}, ['b'])
       {'b': 2}

    If ``keys`` is a :class:`dict`, then it maps keys of the original dict to
    keys of the result:

    .. code-block:: python

       >>> projection({'a': 1, 'b': 2}, {'b': 'c'})
       {'c': 2}
    """
    if isinstance(keys, dict):
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


def get_selector(selector: object, default_value: object = None) -> Callable:  # noqa: F811
    if callable(selector):
        return selector
    elif isinstance(selector, str):
        return lambda this: this.get(selector, default_value)
    elif isiterable(selector):
        return lambda this: projection(this, selector)  # type: ignore
    else:
        raise TypeError(
            'The selector should be a function, string, or iterable of strings.'
        )


def isiterable(obj: object) -> bool:
    try:
        iter(obj)  # type: ignore
        return True
    except TypeError:
        return False


def ismapping(obj: object) -> bool:
    return isinstance(obj, Mapping)


def is_sequence_not_str(obj: object) -> bool:
    return isinstance(obj, Sequence) and not isinstance(obj, str)
