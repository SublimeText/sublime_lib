from sphinx.ext.autodoc.importer import _MockObject

import sys


class SublimeMock:
    Region = _MockObject()

    def __getattr__(self, key):
        if key.isupper():
            return hash(key)
        else:
            raise AttributeError(key)


sys.modules[__name__] = SublimeMock()
