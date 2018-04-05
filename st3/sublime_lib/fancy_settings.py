ARGUMENT_NOT_GIVEN = {}

def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

class FancySettings():
    def __init__(self, settings):
        self.settings = settings

    def get(self, name, default=ARGUMENT_NOT_GIVEN):
        if default is ARGUMENT_NOT_GIVEN:
            if self.settings.has(name):
                return self.settings.get(name)
            else:
                raise KeyError(name)
        else:
            return self.settings.get(name, default)

    def set(self, name, value):
        self.settings.set(name, value)

    def erase(self, name):
        if self.settings.has(name):
            self.settings.erase(name)
        else:
            raise KeyError(name)

    def has(self, name):
        return self.settings.has(name)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.erase(key)

    def __contains__(self, item):
        return self.has(item)

    def subscribe(self, key, selector, callback):
        if callable(selector):
            selector_fn = selector
        elif isinstance(selector, str):
            selector_fn = lambda this: this[selector]
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

        self.settings.add_on_change(key, onchange)

    def unsubscribe(self, key):
        self.settings.clear_on_change(key)
