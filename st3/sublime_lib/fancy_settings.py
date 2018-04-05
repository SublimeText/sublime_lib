class FancySettings():
    def __init__(self, settings):
        self.settings = settings

    def get(self, name, default=None):
        return self.settings.get(name, default)

    def set(self, name, value):
        self.settings.set(name, value)

    def erase(self, name):
        self.settings.erase(name)

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
        if isinstance(selector, str):
            key = selector
            selector = lambda this: this[key]

        previous_value = selector(self)

        def onchange():
            nonlocal previous_value
            new_value = selector(self)

            if new_value != previous_value:
                callback(new_value, previous_value)
                previous_value = new_value

        self.settings.add_on_change(key, onchange)

    def unsubscribe(self, key):
        self.settings.clear_on_change(key)
