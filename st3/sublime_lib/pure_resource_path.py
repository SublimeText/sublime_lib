import posixpath
from functools import total_ordering

from .glob_util import get_glob_expr


__all__ = ['PureResourcePath']


@total_ordering
class PureResourcePath():
    """A representation of a Sublime Text resource path. Inspired by pathlib."""

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
        return isinstance(other, PureResourcePath) and self._parts == other.parts

    def __lt__(self, other):
        if isinstance(other, PureResourcePath):
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
        """The logical parent of the path."""
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
        """A string representing the final path component."""
        try:
            return self._parts[-1]
        except IndexError:
            return None

    @property
    def suffix(self):
        """The file extension of the final component, if any."""
        return posixpath.splitext(self.name)[1]

    @property
    def suffixes(self):
        """A list of the path’s file extensions."""
        return ['.' + suffix for suffix in self.name.split('.')[1:]]

    @property
    def stem(self):
        """The final path component, without its suffix."""
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
        ``False`` otherwise."""
        if pattern.startswith('/'):
            matcher = get_glob_expr(pattern.lstrip('/'))
        else:
            matcher = get_glob_expr('**' + pattern)

        return matcher.match(str(self))

    def joinpath(self, *other):
        """Combine this path with all of the given strings."""
        return self.__class__(self, *other)

    def with_name(self, name):
        """Return a new path with the name changed.

        :raise ValueError: if the original path doesn’t have a name."""
        if not self.name:
            raise ValueError("{!r} has an empty name".format(self))

        return self.parent / name

    def with_suffix(self, suffix):
        """Return a new path with the suffix changed.

        If the original path doesn’t have a suffix, the new suffix is appended
        instead. If the suffix is an empty string, the original suffix is
        removed."""
        return self.parent / (posixpath.splitext(self.name)[0] + suffix)
