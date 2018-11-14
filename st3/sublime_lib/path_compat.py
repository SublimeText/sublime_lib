__all__ = ['Path']

try:
    from pathlib import Path
except ImportError:
    import os.path

    class Path():
        def __init__(self, path):
            self.text = os.path.normpath(path)

        def __repr__(self):
            return "%s(%s)" % (type(self).__name__, repr(self.text))

        def __str__(self):
            return self.text

        def __fspath__(self):
            return self.text

        def __eq__(self, other):
            return self.text == other.text
