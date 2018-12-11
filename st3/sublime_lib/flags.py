"""
Python enumerations for use with Sublime API methods.

Descendants of :class:`IntFlag` each implement the following class method:

..  py:classmethod:: from_strings(strings)

    Convert each element of strings to this type, then return their union.

    :raise KeyError: if an element of strings cannot be converted to this type.

    ..  versionadded:: 1.2
"""

import sublime

from .vendor.python.enum import IntEnum, IntFlag
from inspect import cleandoc


__all__ = [
    'DialogResult', 'PointClass', 'FindOption', 'RegionOption',
    'PopupOption', 'PhantomLayout', 'OpenFileOption', 'QuickPanelOption'
]


def autodoc(prefix=None):
    if prefix is None:
        prefix_str = ''
    else:
        prefix_str = prefix + '_'

    def decorator(enum):
        enum.__doc__ = cleandoc(enum.__doc__) + '\n\n' + '\n'.join([
            cleandoc("""
            .. py:attribute:: {name}

                = :attr:`sublime.{pre}{name}`
            """).format(name=item.name, pre=prefix_str) for item in enum
        ])

        return enum

    return decorator


class EnhancedIntFlag(IntFlag):
    @classmethod
    def from_strings(cls, strings):
        ret = cls(0)
        for string in strings:
            ret |= cls[string]

        return ret


@autodoc('DIALOG')
class DialogResult(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with :func:`sublime.yes_no_cancel_dialog`.
    """
    CANCEL = sublime.DIALOG_CANCEL
    YES = sublime.DIALOG_YES
    NO = sublime.DIALOG_NO


@autodoc('CLASS')
class PointClass(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with several methods of :class:`sublime.View`:

    - :meth:`~sublime.View.classify`
    - :meth:`~sublime.View.find_by_class`
    - :meth:`~sublime.View.expand_by_class`
    """
    WORD_START = sublime.CLASS_WORD_START
    WORD_END = sublime.CLASS_WORD_END
    PUNCTUATION_START = sublime.CLASS_PUNCTUATION_START
    PUNCTUATION_END = sublime.CLASS_PUNCTUATION_END
    SUB_WORD_START = sublime.CLASS_SUB_WORD_START
    SUB_WORD_END = sublime.CLASS_SUB_WORD_END
    LINE_START = sublime.CLASS_LINE_START
    LINE_END = sublime.CLASS_LINE_END
    EMPTY_LINE = sublime.CLASS_EMPTY_LINE


@autodoc()
class FindOption(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with several methods of :class:`sublime.View`:

    - :meth:`~sublime.View.find`
    - :meth:`~sublime.View.find_all`
    """
    LITERAL = sublime.LITERAL
    IGNORECASE = sublime.IGNORECASE


@autodoc()
class RegionOption(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.View.add_regions`.
    """
    DRAW_EMPTY = sublime.DRAW_EMPTY
    HIDE_ON_MINIMAP = sublime.HIDE_ON_MINIMAP
    DRAW_EMPTY_AS_OVERWRITE = sublime.DRAW_EMPTY_AS_OVERWRITE
    DRAW_NO_FILL = sublime.DRAW_NO_FILL
    DRAW_NO_OUTLINE = sublime.DRAW_NO_OUTLINE
    DRAW_SOLID_UNDERLINE = sublime.DRAW_SOLID_UNDERLINE
    DRAW_STIPPLED_UNDERLINE = sublime.DRAW_STIPPLED_UNDERLINE
    DRAW_SQUIGGLY_UNDERLINE = sublime.DRAW_SQUIGGLY_UNDERLINE
    PERSISTENT = sublime.PERSISTENT
    HIDDEN = sublime.HIDDEN


@autodoc()
class PopupOption(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.View.show_popup`.
    """
    COOPERATE_WITH_AUTO_COMPLETE = sublime.COOPERATE_WITH_AUTO_COMPLETE
    HIDE_ON_MOUSE_MOVE = sublime.HIDE_ON_MOUSE_MOVE
    HIDE_ON_MOUSE_MOVE_AWAY = sublime.HIDE_ON_MOUSE_MOVE_AWAY


@autodoc('LAYOUT')
class PhantomLayout(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with :class:`sublime.Phantom`.
    """
    INLINE = sublime.LAYOUT_INLINE
    BELOW = sublime.LAYOUT_BELOW
    BLOCK = sublime.LAYOUT_BLOCK


@autodoc()
class OpenFileOption(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.Window.open_file`.
    """
    ENCODED_POSITION = sublime.ENCODED_POSITION
    TRANSIENT = sublime.TRANSIENT


@autodoc()
class QuickPanelOption(EnhancedIntFlag):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.Window.show_quick_panel`.
    """
    MONOSPACE_FONT = sublime.MONOSPACE_FONT
    KEEP_OPEN_ON_FOCUS_LOST = sublime.KEEP_OPEN_ON_FOCUS_LOST
