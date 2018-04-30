import sublime

from uuid import uuid4
from collections.abc import Mapping

from .collection_utils import projection


def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def ismapping(obj):
    return isinstance(obj, Mapping)


NOT_GIVEN = {}


class FancySettings():
    """
    Wraps a sublime.Settings object with a dict-like interface.

    There is no way to list or iterate over the keys of a `sublime.Settings`
    object. As a result, the following methods are not implemented:

    - len(d)
    - iter(d)
    - clear()
    - copy()
    - items()
    - keys()
    - popitem()
    - values()
    """

    def __init__(self, settings):
        """
        Return a new FancySettings wrapping a given Settings object *settings*.
        """
        self.settings = settings

    def __getitem__(self, key):
        """Return the setting named *key*. Raises a KeyError if there is no such setting."""
        if key in self:
            return self.get(key)
        else:
            return self.__missing__(key)

    def __missing__(self, key):
        raise KeyError(key)

    def __setitem__(self, key, value):
        """Set `d[key]` to *value*."""
        self.settings.set(key, value)

    def __delitem__(self, key):
        """Remove `d[key]` from *d*. Raises a KeyError if *key* is not in the map."""
        if key in self:
            self.settings.erase(key)
        else:
            raise KeyError(key)

    def __contains__(self, item):
        """Return `True` if *d* has a key *key*, else `False`."""
        return self.settings.has(item)

    def get(self, key, default=None):
        """
        Return the value for key if key is in the dictionary, else default. If
        default is not given, it defaults to None, so that this method never
        raises a KeyError.
        """
        return self.settings.get(key, default)

    def pop(self, key, default=NOT_GIVEN):
        """
        If key is in the dictionary, remove it and return its value, else
        return default. If default is not given and key is not in the
        dictionary, a KeyError is raised.
        """
        if key in self:
            ret = self[key]
            del self[key]
            return ret
        elif default is NOT_GIVEN:
            raise KeyError(key)
        else:
            return default

    def setdefault(self, key, default=None):
        """
        If key is in the dictionary, return its value. If not, insert key with
        a value of default and return default. default defaults to None.
        """
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(self, other=[], **kwargs):
        """
        Update the dictionary with the key/value pairs from other, overwriting
        existing keys. Return None.

        update() accepts either another dictionary object or an iterable of
        key/value pairs (as tuples or other iterables of length two). If keyword
        arguments are specified, the dictionary is then updated with those
        key/value pairs: d.update(red=1, blue=2).
        """
        if ismapping(other):
            other = other.items()

        for key, value in other:
            self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def subscribe(self, selector, callback, default_value=None):
        """
        Register a calback to be invoked when the settings object changes.
        """
        if callable(selector):
            selector_fn = selector
        elif isinstance(selector, str):
            selector_fn = lambda this: this.get(selector, default_value)
        elif isiterable(selector):
            selector_fn = lambda this: projection(this, selector)
        else:
            raise TypeError('The "callback" argument should be a function, '
                            'string, or iterable of strings.')

        previous_value = selector_fn(self)

        def onchange():
            nonlocal previous_value
            new_value = selector_fn(self)

            if new_value != previous_value:
                callback(new_value, previous_value)
                previous_value = new_value

        key = str(uuid4())
        self.settings.add_on_change(key, onchange)
        return key

    def unsubscribe(self, key):
        self.settings.clear_on_change(key)


class NamedFancySettings(FancySettings):
    """
    Wraps a `sublime.Settings` object corresponding to a `sublime-settings`
    file.
    """

    def __init__(self, name):
        """Return a new NamedFancySettings corresponding to the given name."""

        super().__init__(sublime.load_settings(name))
        self.name = name

    def save(self):
        """Flushes any in-memory changes to the named settings object to disk."""
        sublime.save_settings(self.name)


class DefaultFancySettings(FancySettings):
    def __init__(self, settings, defaults={}):
        """
        Return a new FancySettings wrapping a given Settings object *settings*.
        """
        super().__init__(settings)
        self.defaults = defaults

    def __missing__(self, key):
        return self.defaults[key]
