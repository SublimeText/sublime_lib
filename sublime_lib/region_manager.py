from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar
    T = TypeVar('T')

import sublime

from .flags import RegionOption

__all__ = ['RegionManager']


def _coalesce(*values: T | None) -> T:
    return next(value for value in values if value is not None)


class RegionManager:
    """A manager for regions in a given :class:`sublime.View` with the same `key`.

    If `key` is not given,
    a unique identifier will be used.

    If the `scope`, `icon`, and `flags` args are given,
    then they will be used as default values for :meth:`set`.

    When the region manager is garbage-collected, all managed regions will be erased.

    .. versionadded:: 1.6
    """

    def __init__(
        self,
        view: sublime.View,
        key: str | None = None,
        *,
        scope: str | None = None,
        icon: str | None = None,
        flags: type[RegionOption] | None = None
    ):
        self.view: sublime.View = view

        if key is None:
            self.key = str(id(self))
        else:
            self.key = key

        self.scope: str | None = scope
        self.icon: str | None = icon
        self.flags: type[RegionOption] | None = flags

    def __del__(self) -> None:
        self.erase()

    def set(
        self,
        regions: list[sublime.Region],
        *,
        scope: str | None = None,
        icon: str | None = None,
        flags: type[RegionOption] | None = None
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
            _coalesce(flags, self.flags, RegionOption.NONE),  # type: ignore
        )

    def get(self) -> list[sublime.Region]:
        """Return the list of managed regions."""
        return self.view.get_regions(self.key)

    def erase(self) -> None:
        """Erase all managed regions.
        """
        self.view.erase_regions(self.key)
