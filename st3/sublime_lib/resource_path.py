import sublime
import os.path
from collections import OrderedDict

from .pure_resource_path import PureResourcePath
from ._path_compat import Path
from .glob_util import get_glob_expr


__all__ = ['glob_resources', 'ResourcePath']


def glob_resources(pattern):
    expr = get_glob_expr(pattern)
    return sorted(
        ResourcePath(path) for path in sublime.find_resources('')
        if expr.match(path)
    )


class ResourcePath(PureResourcePath):
    def file_path(self):
        """Return a Path object representing a filesystem path inside the
        Packages or Cache directory. Even if there is a resource at this
        `ResourcePath`, there may not be a file at that filesystem path.

        If `pathlib` is available, return a :class:`pathlib.Path`. Otherwise,
        return a stub object that is compatible with :func:`str` and
        :func:`os.fspath`.

        :raise ValueError: if ``ResourcePath.root`` is not `Packages` or
        `Cache`.
        """
        if self.root == 'Packages':
            return Path(os.path.join(sublime.packages_path(), *self.parts[1:]))
        elif self.root == 'Cache':
            return Path(os.path.join(sublime.cache_path(), *self.parts[1:]))
        else:
            raise ValueError("%r is not a packages or cache path" % (self,))

    def exists(self):
        """Return ``True`` if there is a resource at this path, or ``False``
        otherwise."""
        return str(self) in sublime.find_resources(self.name)

    def read_text(self):
        """Load the resource at this path and return it as text.

        :raise FileNotFoundError: if there is no resource at this path.

        :raise UnicodeDecodeError: if the resource cannot be decoded as UTF-8.
        """
        try:
            return sublime.load_resource(str(self))
        except IOError as err:
            raise FileNotFoundError from err

    def read_bytes(self):
        """Load the resource at this path and return it as bytes.

        :raise FileNotFoundError: if there is no resource at this path.
        """
        try:
            return sublime.load_binary_resource(str(self))
        except IOError as err:
            raise FileNotFoundError from err

    def glob(self, pattern):
        base = str(self) + '/' if self._parts else ''
        return glob_resources(base + pattern)

    def rglob(self, pattern):
        return self.glob('**/' + pattern)

    def children(self):
        depth = len(self._parts)
        return [
            self / next_part
            for next_part in OrderedDict.fromkeys(
                resource.parts[depth]
                for resource in self.glob('**')
            )
        ]
