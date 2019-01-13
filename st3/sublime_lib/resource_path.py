import sublime

import posixpath
from collections import OrderedDict

from .vendor.pathlib.pathlib import Path
from ._util.glob import get_glob_matcher


__all__ = ['ResourcePath']


def get_resource_roots():
    return {
        'Packages': sublime.packages_path(),
        'Cache': sublime.cache_path(),
    }


def get_installed_resource_roots():
    return (
        sublime.installed_packages_path(),
        Path(sublime.executable_path()).parent / 'Packages',
    )


class ResourcePath():
    """
    A pathlib-inspired representation of a Sublime Text resource path.

    Resource paths are similar to filesystem paths in many ways,
    yet different in other ways.
    Many features of :class:`pathlib.Path` objects
    are not implemented by :class:`ResourcePath`,
    and other features may have differerent interpretations.

    A resource path consists of one or more parts
    separated by forward slashes (regardless of platform).
    The first part is the root.
    At the present time, the only roots that Sublime uses are
    ``'Packages'`` and ``'Caches'``.
    Resource paths are always absolute;
    dots in resource paths have no special meaning.

    :class:`ResourcePath` objects are immutable and hashable.
    The forward slash operator is a shorthand for :meth:`joinpath`.
    The string representation of a :class:`ResourcePath`
    is the raw resource path in the form that Sublime Text uses.

    Some methods accept glob patterns as arguments.
    Glob patterns are interpreted as in pathlib.
    Recursive globs (**) are always allowed, even in :meth:`match`.
    Leading slashes are not matched literally.
    A pattern with a leading slash must match the entire path
    and not merely a suffix of the path.
    """

    @classmethod
    def glob_resources(cls, pattern):
        """
        Find all resources that match the given pattern
        and return them as :class:`ResourcePath` objects.
        """
        match = get_glob_matcher(pattern)
        return [
            cls(path) for path in sublime.find_resources('')
            if match(path)
        ]

    @classmethod
    def from_file_path(cls, file_path):
        """
        Return a :class:`ResourcePath` corresponding to the given file path.

        If the file path corresponds to a resource inside an installed package,
        then return the path to that resource.

        :raise ValueError: if the given file path does not correspond to any resource path.
        :raise ValueError: if the given file path is relative.

        .. code-block:: python

           >>> ResourcePath.from_file_path(
              os.path.join(sublime.packages_path(), 'My Package', 'foo.py')
           )
           ResourcePath("Packages/My Package/foo.py")

           >>> ResourcePath.from_file_path(
              os.path.join(
                sublime.installed_packages_path(),
                'My Package.sublime-package',
                'foo.py'
              )
           )
           ResourcePath("Packages/My Package/foo.py")
        """
        file_path = Path(file_path)
        if not file_path.is_absolute():
            raise ValueError("Cannot convert a relative file path to a resource path.")

        for root, base in get_resource_roots().items():
            try:
                rel = file_path.relative_to(base)
            except ValueError:
                pass
            else:
                return cls(root, *rel.parts)

        for base in get_installed_resource_roots():
            try:
                rel = file_path.relative_to(base).parts
            except ValueError:
                pass
            else:
                if rel == ():
                    return cls('Packages')
                package, *rest = rel
                package_path = cls('Packages', package)
                if package_path.suffix == '.sublime-package':
                    return package_path.with_suffix('').joinpath(*rest)

        raise ValueError("Path {!r} does not correspond to any resource path.".format(file_path))

    def __init__(self, *pathsegments):
        """
        Construct a :class:`ResourcePath` object with the given parts.

        :raise ValueError: if the resulting path would be empty.
        """
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

    def __truediv__(self, other):
        return self.joinpath(other)

    @property
    def parts(self):
        """
        A tuple giving access to the path’s various components.
        """
        return self._parts

    @property
    def parent(self):
        """
        The logical parent of the path. A root path is its own parent.
        """
        if len(self._parts) == 1:
            return self
        else:
            return self.__class__(*self._parts[:-1])

    @property
    def parents(self):
        """
        An immutable sequence providing access to the path's logical ancestors.
        """
        parent = self.parent
        if self == parent:
            return ()
        else:
            return (parent,) + parent.parents

    @property
    def name(self):
        """
        A string representing the final path component.
        """
        return self._parts[-1]

    @property
    def suffix(self):
        """
        The final component's last suffix, if any.
        """
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[i:]
        else:
            return ''

    @property
    def suffixes(self):
        """
        A list of the final component's suffixes, if any.
        """
        name = self.name
        if name.endswith('.'):
            return []
        name = name.lstrip('.')
        return ['.' + suffix for suffix in name.split('.')[1:]]

    @property
    def stem(self):
        """
        The final path component, minus its last suffix.
        """
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[:i]
        else:
            return name

    @property
    def root(self):
        """
        The first path component (usually ``'Packages'`` or ``'Cache'``).
        """
        return self._parts[0]

    @property
    def package(self):
        """
        The name of the package the path is within,
        or ``None`` if the path is a root path.
        """
        if len(self._parts) >= 2:
            return self._parts[1]
        else:
            return None

    def match(self, pattern):
        """
        Return ``True`` if this path matches the given glob pattern,
        or ``False`` otherwise.

        :raise ValueError: if `pattern` is invalid.
        """
        match = get_glob_matcher(pattern)
        return match(str(self))

    def joinpath(self, *other):
        """
        Combine this path with all of the given strings.
        """
        return self.__class__(self, *other)

    def relative_to(self, *other):
        """
        Compute a tuple `parts` of path components such that ``self == other.joinpath(*parts)``.

        `other` will be converted to a :class:`ResourcePath`.

        :raise ValueError: if this path is not a descendant of `other`.
        """
        other = ResourcePath(*other)
        other_len = len(other.parts)

        if other.parts == self._parts[:other_len]:
            return self._parts[other_len:]
        else:
            raise ValueError("{!s} does not start with {!s}".format(self, other))

    def with_name(self, name):
        """
        Return a new path with the name changed.
        """
        if len(self._parts) == 1:
            return self.__class__(name)
        else:
            return self.parent / name

    def with_suffix(self, suffix):
        """
        Return a new path with the suffix changed.

        If the original path doesn’t have a suffix, the new suffix is appended
        instead. If the new suffix is an empty string, the original suffix is
        removed.
        """
        return self.with_name(self.stem + suffix)

    def file_path(self):
        """
        Return a :class:`Path` object representing a filesystem path
        inside one of Sublime's data directories.

        Even if there is a resource at this path,
        there may not be a file at that filesystem path.
        The resource could be in a default package or an installed package.

        :raise ValueError: if the path's root is not used by Sublime.
        """
        try:
            return Path(get_resource_roots()[self.root]).joinpath(*self.parts[1:])
        except KeyError:
            raise ValueError("Can't find a filesystem path for {!r}.".format(self.root)) from None

    def exists(self):
        """
        Return ``True`` if there is a resource at this path,
        or ``False`` otherwise.

        The resource system does not keep track of directories.
        Even if a path does not point to a resource,
        there may be resources beneath that path.
        """
        return str(self) in sublime.find_resources(self.name)

    def read_text(self):
        """
        Load the resource at this path and return it as text.

        :raise FileNotFoundError: if there is no resource at this path.

        :raise UnicodeDecodeError: if the resource cannot be decoded as UTF-8.
        """
        try:
            return sublime.load_resource(str(self))
        except IOError as err:
            raise FileNotFoundError(str(self)) from err

    def read_bytes(self):
        """
        Load the resource at this path and return it as bytes.

        :raise FileNotFoundError: if there is no resource at this path.
        """
        try:
            return sublime.load_binary_resource(str(self))
        except IOError as err:
            raise FileNotFoundError(str(self)) from err

    def glob(self, pattern):
        """
        Glob the given pattern at this path, returning all matching resources.

        :raise ValueError: if `pattern` is invalid.
        """
        base = '/' + str(self) + '/' if self._parts else ''
        return ResourcePath.glob_resources(base + pattern)

    def rglob(self, pattern):
        """
        Shorthand for ``path.glob('**/' + pattern)``.

        :raise ValueError: if `pattern` is invalid.

        :raise NotImplementedError: if `pattern` begins with a slash.
        """
        if pattern.startswith('/'):
            raise NotImplementedError("Non-relative patterns are unsupported")

        return self.glob('**/' + pattern)

    def children(self):
        """
        Return a list of paths that are direct children of this path
        and point to a resource at or beneath that path.
        """
        depth = len(self._parts)
        return [
            self / next_part
            for next_part in OrderedDict.fromkeys(
                resource.parts[depth]
                for resource in self.glob('**')
            )
        ]
