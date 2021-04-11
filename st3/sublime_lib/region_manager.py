import sublime

from ._compat.typing import Optional, List, TypeVar, Collection
from .flags import RegionOption


__all__ = ['RegionManager']


T = TypeVar('T')


def _coalesce(*values: Optional[T]) -> T:
    return next(value for value in values if value is not None)


class RegionManager:
    def __init__(
        self,
        view: sublime.View,
        key: Optional[str] = None,
        *,
        scope: Optional[str] = None,
        icon: Optional[str] = None,
        flags: Optional[RegionOption] = None
    ):
        self.view = view

        if key is None:
            self.key = str(id(self))
        else:
            self.key = key

        self.scope = scope
        self.icon = icon
        self.flags = flags

    def __del__(self) -> None:
        self.erase()

    def set(
        self,
        regions: Collection[sublime.Region],
        *,
        scope: Optional[str] = None,
        icon: Optional[str] = None,
        flags: Optional[RegionOption] = None
    ) -> None:
        self.view.add_regions(
            self.key,
            regions,
            _coalesce(scope, self.scope, ''),
            _coalesce(icon, self.icon, ''),
            _coalesce(flags, self.flags, 0),
        )

    def get(self) -> List[sublime.Region]:
        return self.view.get_regions(self.key)

    def erase(self) -> None:
        self.view.erase_regions(self.key)
