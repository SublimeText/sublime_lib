import sublime

import os.path
import posixpath
from functools import total_ordering
from collections import OrderedDict

# from .pure_resource_path import PureResourcePath
from .vendor.pathlib.pathlib import Path
from .glob_util import get_glob_matcher


__all__ = ['glob_resources', 'ResourcePath']


def glob_resources(pattern):
    match = get_glob_matcher(pattern)
    return sorted(
        ResourcePath(path) for path in sublime.find_resources('')
        if match(path)
    )


@total_ordering
class ResourcePath():
    """A pathlib-inspired representation of a Sublime Text resource path.

    Resource paths are similar to filesystem paths in many ways, yet different
    in other ways. Many features of :class:`pathlib.Path` objects are not
    implemented by :class:`ResourcePath`, and other features may have
    differerent interpretations.

    Resource paths generally behave similarly to POSIX-flavored paths, except
    that the global root is the empty string, not `/`. All resource paths are
    absolute; dots in paths have no special meaning.

    Like :class:`pathlib.Path` objects, :class:`ResourcePath` objects are
    immutable, hashable, and orderable with each other. The forward slash
    operator is a shorthand for :meth:`joinpath`. The string representation
    of a :class:`ResourcePath` is the raw resource path in the form that Sublime
    Text uses."""

    def __init__(self, *pathsegments):
        self._parts = tuple(
            part
            for segment in pathsegments if segment
            for part in posixpath.normpath(str(segment)).split('/')
        )

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
        """The logical parent of the path. The empty path is its own parent."""
        if len(self._parts) > 1:
            return self.__class__(*self._parts[:-1])
        else:
            return self

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
        """A string representing the final path component, or the empty string
        if the path is empty."""
        try:
            return self._parts[-1]
        except IndexError:
            return ''

    @property
    def suffix(self):
        """The file extension of the final component, or the empty string if the
        path is empty or if the final component does not have a file extension.
        """
        return posixpath.splitext(self.name)[1]

    @property
    def suffixes(self):
        """A list of the path’s file extensions."""
        return ['.' + suffix for suffix in self.name.split('.')[1:]]

    @property
    def stem(self):
        """The final path component without its suffix, or the empty string if
        the path is empty."""
        return posixpath.splitext(self.name)[0]

    @property
    def root(self):
        """The first path component (usually `Packages` or `Cache`)."""
        try:
            return self._parts[0]
        except IndexError:
            return ''

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
        """Return a new path with the name changed.

        :raise ValueError: if the path is empty."""
        if not self.name:
            raise ValueError("{!r} has an empty name".format(self))

        return self.parent / name

    def with_suffix(self, suffix):
        """Return a new path with the suffix changed.

        If the original path doesn’t have a suffix, the new suffix is appended
        instead. If the suffix is an empty string, the original suffix is
        removed."""
        return self.parent / (self.stem + suffix)

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
