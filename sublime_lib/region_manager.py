import sublime

from typing import Optional, List, TypeVar, Collection

from .flags import RegionOption


__all__ = ['RegionManager']


T = TypeVar('T')


def _coalesce(*values: Optional[T]) -> T:
    return next(value for value in values if value is not None)


class RegionManager:
    """A manager for regions in a given :class:`sublime.View` with the same `key`.

    If `key` is not given,
    a unique identifier will be used.

    If the `scope`, `icon`, and `flags` args are given,
    then they will be used as default values for :meth:`set`.

    When the region manager is garbage-collected, all managed regions will be erased.

    .. versionadded:: 1.4
    """

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
        """Replace managed regions with the given regions.

        If the `scope`, `icon`, and `flags` arguments are given,
        then they will be passed to :meth:`sublime.add_regions`.
        Otherwise, the defaults specified in the initializer will be used.
        """
        self.view.add_regions(
            self.key,
            regions,
            _coalesce(scope, self.scope, ''),
            _coalesce(icon, self.icon, ''),
            _coalesce(flags, self.flags, 0),
        )

    def get(self) -> List[sublime.Region]:
        """Return the list of managed regions."""
        return self.view.get_regions(self.key)

    def erase(self) -> None:
        """Erase all managed regions.
        """
        self.view.erase_regions(self.key)
