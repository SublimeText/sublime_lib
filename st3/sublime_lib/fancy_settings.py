from uuid import uuid4

def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

class FancySettings():
    def __init__(self, settings, defaults={}):
        self.settings = settings
        self.defaults = defaults

    def get(self, name, default=None):
        return self.settings.get(name, self.defaults.get(default))

    def set(self, name, value):
        self.settings.set(name, value)

    def erase(self, name):
        self.settings.erase(name)

    def has(self, name):
        return self.settings.has(name)

    def __getitem__(self, key):
        if self.settings.has(key) or key in self.defaults:
            return self.get(key)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        if self.has(name):
            self.erase(name)
        else:
            raise KeyError(name)

    def __contains__(self, item):
        return self.has(item)

    def subscribe(self, selector, callback, default_value=None):
        if callable(selector):
            selector_fn = selector
        elif isinstance(selector, str):
            selector_fn = lambda this: this.get(selector, default_value)
        elif isiterable(selector):
            selector_fn = lambda this: { key : this[key] for key in selector }
        else:
            raise TypeError('The "callback" argument should be a function, string, or iterable of strings.')

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
