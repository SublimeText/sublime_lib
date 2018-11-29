import sublime

import posixpath
from functools import total_ordering
from collections import OrderedDict

from .vendor.pathlib.pathlib import Path
from .glob_util import get_glob_matcher


__all__ = ['ResourcePath']


@total_ordering
class ResourcePath():
    """A pathlib-inspired representation of a Sublime Text resource path.

    Resource paths are similar to filesystem paths in many ways, yet different
    in other ways. Many features of :class:`pathlib.Path` objects are not
    implemented by :class:`ResourcePath`, and other features may have
    differerent interpretations.

    A resource path consists of one or more parts separated by forward slashes
    (regardless of platform). The first part, generally ``'Packages'`` or
    ``'Cache'``, is the root. (A resource path must have a root.) Resource paths
    are always absolute; dots in resource paths have no special meaning.

    Like :class:`pathlib.Path` objects, :class:`ResourcePath` objects are
    immutable, hashable, and orderable with each other. The forward slash
    operator is a shorthand for :meth:`joinpath`. The string representation
    of a :class:`ResourcePath` is the raw resource path in the form that Sublime
    Text uses."""

    @classmethod
    def glob_resources(cls, pattern):
        """Find all resources that match the given pattern and return them as
        :class:`ResourcePath` objects."""
        match = get_glob_matcher(pattern)
        return sorted(
            cls(path) for path in sublime.find_resources('')
            if match(path)
        )

    def __init__(self, *pathsegments):
        self._parts = tuple(
            part
            for segment in pathsegments if segment
            for part in posixpath.normpath(str(segment)).split('/')
        )
        if self._parts == ():
            raise ValueError("Empty path.")

    def __hash__(self):
        return hash(self.parts)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, str(self))

    def __str__(self):
        return '/'.join(self.parts)

    def __eq__(self, other):
        return isinstance(other, ResourcePath) and self._parts == other.parts

    def __lt__(self, other):
        if isinstance(other, ResourcePath):
            return self._parts < other.parts
        else:
            return NotImplemented

    def __truediv__(self, other):
        return self.joinpath(other)

    @property
    def parts(self):
        """A tuple giving access to the path’s various components."""
        return self._parts

    @property
    def parent(self):
        """The logical parent of the path. A root path is its own parent."""
        if len(self._parts) == 1:
            return self
        else:
            return self.__class__(*self._parts[:-1])

    @property
    def parents(self):
        """An immutable sequence providing access to the logical ancestors of
        the path."""
        parent = self.parent
        if self == parent:
            return ()
        else:
            return (parent,) + parent.parents

    @property
    def name(self):
        """A string representing the final path component."""
        try:
            return self._parts[-1]
        except IndexError:
            return ''

    @property
    def suffix(self):
        """The file extension of the final component, or the empty string if the
        final component does not have a file extension.
        """
        return posixpath.splitext(self.name)[1]

    @property
    def suffixes(self):
        """A list of the path’s file extensions."""
        return ['.' + suffix for suffix in self.name.split('.')[1:]]

    @property
    def stem(self):
        """The final path component without its suffix."""
        return posixpath.splitext(self.name)[0]

    @property
    def root(self):
        """The first path component (usually ``'Packages'`` or ``'Cache'``)."""
        return self._parts[0]

    @property
    def package(self):
        """The second path component (usually the name of a package)."""
        try:
            return self._parts[1]
        except IndexError:
            return ''

    def match(self, pattern):
        """Return ``True`` if this path matches the given glob pattern, or
        ``False`` otherwise.

        :raise ValueError: if `pattern` is invalid."""
        match = get_glob_matcher(pattern)
        return match(str(self))

    def joinpath(self, *other):
        """Combine this path with all of the given strings."""
        return self.__class__(self, *other)

    def with_name(self, name):
        """Return a new path with the name changed."""
        if len(self._parts) == 1:
            return self.__class__(name)
        else:
            return self.parent / name

    def with_suffix(self, suffix):
        """Return a new path with the suffix changed.

        If the original path doesn’t have a suffix, the new suffix is appended
        instead. If the new suffix is an empty string, the original suffix is
        removed."""
        # return self.parent / (self.stem + suffix)
        return self.with_name(self.stem + suffix)

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
            base = sublime.packages_path()
        elif self.root == 'Cache':
            base = sublime.cache_path()
        else:
            raise ValueError("%r is not a packages or cache path" % (self,))

        return Path(base).joinpath(*self.parts[1:])

    def exists(self):
        """Return ``True`` if there is a resource at this path, or ``False``
        otherwise.

        The resource system does not keep track of directories. Even if a path
        does not point to a resource, there may be resources beneath that path.
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
        return ResourcePath.glob_resources(base + pattern)

    def rglob(self, pattern):
        """Shorthand for ``path.glob('**/' + pattern)``.

        :raise ValueError: if `pattern` is invalid.

        :raise NotImplementedError: if `pattern` begins with a slash."""
        if pattern.startswith('/'):
            raise NotImplementedError("Non-relative patterns are unsupported")

        return self.glob('**/' + pattern)

    def children(self):
        """Return a list of paths that are direct children of this path and
        point to a resource at or beneath that path."""
        depth = len(self._parts)
        return [
            self / next_part
            for next_part in OrderedDict.fromkeys(
                resource.parts[depth]
                for resource in self.glob('**')
            )
        ]
