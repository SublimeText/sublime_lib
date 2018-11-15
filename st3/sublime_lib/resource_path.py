import sublime
import os.path
from collections import OrderedDict

from .pure_resource_path import PureResourcePath
from .path_compat import Path
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
        if self.root == 'Packages':
            return Path(os.path.join(sublime.packages_path(), *self.parts[1:]))
        elif self.root == 'Cache':
            return Path(os.path.join(sublime.cache_path(), *self.parts[1:]))
        else:
            raise ValueError("%r is not a packages or cache path" % (self,))

    def exists(self):
        return str(self) in sublime.find_resources(self.name)

    def read_text(self):
        try:
            return sublime.load_resource(str(self))
        except IOError as err:
            raise FileNotFoundError from err

    def read_bytes(self):
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
