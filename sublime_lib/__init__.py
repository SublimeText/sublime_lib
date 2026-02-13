from .activity_indicator import ActivityIndicator
from .panel import Panel, OutputPanel
from .region_manager import RegionManager
from .resource_path import ResourcePath
from .settings_dict import NamedSettingsDict, SettingsDict
from .show_selection_panel import NO_SELECTION, show_selection_panel
from .syntax import list_syntaxes, get_syntax_for_scope
from .view_stream import ViewStream
from .view_utils import LineEnding, close_view, new_view
from .window_utils import close_window, new_window

try:
    from ._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0-dev"
    __version_tuple__ = (0, 0, 0, "dev")

__all__ = [
    "__version__",
    "__version_tuple__",
    "ActivityIndicator",
    "Panel",
    "OutputPanel",
    "RegionManager",
    "ResourcePath",
    "NamedSettingsDict",
    "SettingsDict",
    "NO_SELECTION",
    "show_selection_panel",
    "list_syntaxes",
    "get_syntax_for_scope",
    "ViewStream",
    "LineEnding",
    "close_view",
    "new_view",
    "close_window",
    "new_window",
]
