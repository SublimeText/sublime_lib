import sublime

from uuid import uuid4
from collections.abc import Mapping


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
    def __init__(self, settings, defaults={}):
        self.settings = settings
        self.defaults = defaults

    def __getitem__(self, key):
        if key in self or key in self.defaults:
            return self.get(key)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.settings.set(key, value)

    def __delitem__(self, key):
        if key in self:
            self.settings.erase(key)
        else:
            raise KeyError(key)

    def __contains__(self, item):
        return self.settings.has(item)

    def get(self, key, default=None):
        return self.settings.get(key, self.defaults.get(key, default))

    def pop(self, key, default=NOT_GIVEN):
        if key in self:
            ret = self[key]
            del self[key]
            return ret
        elif default is NOT_GIVEN:
            raise KeyError(key)
        else:
            return default

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(self, other=[], **kwargs):
        if ismapping(other):
            other = other.items()

        for key, value in other:
            self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def subscribe(self, selector, callback, default_value=None):
        if callable(selector):
            selector_fn = selector
        elif isinstance(selector, str):
            selector_fn = lambda this: this.get(selector, default_value)
        elif isiterable(selector):
            selector_fn = lambda this: {key: this[key] for key in selector}
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
    def __init__(self, name, defaults={}):
        super().__init__(sublime.load_settings(name), defaults)
        self.name = name

    def save(self):
        sublime.save_settings(self.name)
