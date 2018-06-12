import sublime

from uuid import uuid4
from collections.abc import Mapping

from .collection_utils import projection


__all__ = [ 'SettingsDict', 'NamedSettingsDict', 'DefaultSettingsDict' ]


def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def ismapping(obj):
    return isinstance(obj, Mapping)


NOT_GIVEN = {}


class SettingsDict():
    """
    Wraps a :class:`sublime.Settings` object `settings` with a :class:`dict`-like
    interface.

    There is no way to list or iterate over the keys of a
    :class:`~sublime.Settings` object. As a result, the following methods are
    not implemented:

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
        self.settings = settings

    def __getitem__(self, key):
        """
        :synopsis: foo?

        Return the setting named `key`. Raises :exc:`KeyError` if there is no such
        setting.

        If a subclass of SettingsDict defines a method `__missing__()` and
        `key` is not present, the `d[key]` operation calls that method with the
        key `key` as argument. The `d[key]` operation then returns or raises
        whatever is returned or raised by the `__missing__(key)` call. No other
        operations or methods invoke `__missing__()`. If `__missing__()` is not
        defined, `KeyError` is raised. `__missing__()` must be a method; it
        cannot be an instance variable.
        """
        if key in self:
            return self.get(key)
        else:
            return self.__missing__(key)

    def __missing__(self, key):
        raise KeyError(key)

    def __setitem__(self, key, value):
        """Set `d[key]` to `value`."""
        self.settings.set(key, value)

    def __delitem__(self, key):
        """Remove `d[key]` from *d*. Raises :exc:`KeyError` if *key* is not in the map."""
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
        raises :exc:`KeyError`.
        """
        return self.settings.get(key, default)

    def pop(self, key, default=NOT_GIVEN):
        """
        If key is in the dictionary, remove it and return its value, else
        return default. If default is not given and key is not in the
        dictionary, raise :exc:`KeyError`.
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
        If `key` is in the dictionary, return its value. If not, insert `key` with
        a value of `default` and return `default`.
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


class NamedSettingsDict(SettingsDict):
    """
    Wraps a `sublime.Settings` object corresponding to a `sublime-settings`
    file.
    """

    def __init__(self, name):
        """Return a new NamedSettingsDict corresponding to the given name."""

        super().__init__(sublime.load_settings(name))
        self.name = name

    def save(self):
        """Flushes any in-memory changes to the named settings object to disk."""
        sublime.save_settings(self.name)


class DefaultSettingsDict(SettingsDict):
    """
    A subclass of SettingsDict that accepts user-defined default values.

    This class generally should not be used with named settings files. Instead,
    package developers should provide settings files populated with defaults.
    """

    def __init__(self, settings, defaults):
        """
        Return a new DefaultSettingsDict wrapping a given Settings object
        *settings*, with a given dict-like object *defaults* of default values.
        """
        super().__init__(settings)
        self.defaults = defaults

    def __missing__(self, key):
        """
        Lookup the given `key` in this object's `defaults` attribute, insert
        that value into this object for the `key`, and return that value.

        If looking up `key` in `defaults` raises an exception (such as a
        `KeyError`), this exception is propagated unchanged.

        This method is called by the __getitem__() method of the SettingsDict
        class when the requested key is not found; whatever it returns or
        raises is then returned or raised by __getitem__().

        Note that __missing__() is not called for any operations besides
        __getitem__(). This means that get() will, like normal dictionaries,
        return None as a default rather than using defaults.
        """
        self[key] = self.defaults[key]
        return self[key]
