from .activity_indicator import ActivityIndicator
from .panel import OutputPanel, Panel
from .region_manager import RegionManager
from .resource_path import ResourcePath
from .settings_dict import NamedSettingsDict, SettingsDict
from .show_selection_panel import NO_SELECTION, show_selection_panel
from .syntax import get_syntax_for_scope, list_syntaxes
from .view_stream import ViewStream
from .view_utils import LineEnding, close_view, new_view
from .window_utils import close_window, new_window

try:
    from ._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0-dev"
    __version_tuple__ = (0, 0, 0, "dev")

__all__ = [
    "NO_SELECTION",
    "ActivityIndicator",
    "LineEnding",
    "NamedSettingsDict",
    "OutputPanel",
    "Panel",
    "RegionManager",
    "ResourcePath",
    "SettingsDict",
    "ViewStream",
    "__version__",
    "__version_tuple__",
    "close_view",
    "close_window",
    "get_syntax_for_scope",
    "list_syntaxes",
    "new_view",
    "new_window",
    "show_selection_panel",
]
