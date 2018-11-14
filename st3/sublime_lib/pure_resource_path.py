import posixpath
from functools import total_ordering


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
        return "%s(%s)" % (type(self).__name__, repr(str(self)))

    def __str__(self):
        return '/'.join(self.parts)

    def __eq__(self, other):
        return self._parts == other.parts

    def __lt__(self, other):
        return self._parts < other.parts

    def __truediv__(self, other):
        return self.joinpath(other)

    def _new(self, *args):
        return type(self)(*args)

    @property
    def parts(self):
        """A tuple giving access to the path’s various components."""
        return self._parts

    @property
    def parent(self):
        if len(self._parts) > 1:
            return self._new(*self._parts[:-1])
        else:
            return self

    @property
    def parents(self):
        parent = self.parent
        if self == parent:
            return []
        else:
            return [parent] + parent.parents

    @property
    def name(self):
        try:
            return self._parts[-1]
        except IndexError:
            return None

    @property
    def suffix(self):
        return posixpath.splitext(self.name)[1]

    @property
    def suffixes(self):
        return ['.' + suffix for suffix in self.name.split('.')[1:]]

    @property
    def stem(self):
        return self.name.split('.')[0]

    @property
    def root(self):
        try:
            return self._parts[0]
        except IndexError:
            return None

    @property
    def package(self):
        try:
            return self._parts[1]
        except IndexError:
            return None

    def joinpath(self, *other):
        return self._new(self, *other)

    def with_name(self, name):
        if not self.name:
            raise ValueError("%r has an empty name" % (self,))

        return self.parent / name

    def with_suffix(self, suffix):
        return self.parent / (posixpath.splitext(self.name)[0] + suffix)
