import sublime
import os.path
from collections import OrderedDict

from .pure_resource_path import PureResourcePath
from .vendor.pathlib.pathlib import Path
from .glob_util import get_glob_matcher


__all__ = ['glob_resources', 'ResourcePath']


def glob_resources(pattern):
    match = get_glob_matcher(pattern)
    return sorted(
        ResourcePath(path) for path in sublime.find_resources('')
        if match(path)
    )


class ResourcePath(PureResourcePath):
    def file_path(self):
        """Return a :class:`Path` object representing a filesystem path inside
        the `Packages` or `Cache` directory.

        Even if there is a resource at this path, there may not be a file at
        that filesystem path. The resource could be in a default package or an
        installed package.

        :raise ValueError: if the path does not begin with `Packages` or
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
        otherwise.

        The resource system does not keep track of directories. Even if a path
        does not contain a resource, there may be resources beneath that path.
        """
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
        """Glob the given pattern at this path, returning all matching resources.

        :raise ValueError: if `pattern` is invalid."""
        base = '/' + str(self) + '/' if self._parts else ''
        return glob_resources(base + pattern)

    def rglob(self, pattern):
        """Shorthand for ``path.glob('**/' + pattern)``.

        :raise ValueError: if `pattern` is invalid.

        :raise NotImplementedError: if `pattern` begins with a slash."""
        if pattern.startswith('/'):
            raise NotImplementedError("Non-relative patterns are unsupported")

        return self.glob('**/' + pattern)

    def children(self):
        """Return a list of paths that are direct children of this path and
        contain a resource at or beneath that path."""
        depth = len(self._parts)
        return [
            self / next_part
            for next_part in OrderedDict.fromkeys(
                resource.parts[depth]
                for resource in self.glob('**')
            )
        ]
