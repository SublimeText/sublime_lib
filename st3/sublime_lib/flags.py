"""
Python enumerations for use with Sublime API methods.

In addition to the standard behavior,
these enumerations' constructors accept the name of an enumerated value as a string:

.. code-block:: python

   >>> PointClass(sublime.DIALOG_YES)
   <DialogResult.YES: 1>
   >>> PointClass("YES")
   <DialogResult.YES: 1>

Descendants of :class:`IntFlag` accept zero or more arguments:

.. code-block:: python

   >>> PointClass("WORD_START", "WORD_END")
   <PointClass.WORD_END|WORD_START: 3>
   >>> PointClass()
   <PointClass.0: 0>

.. versionchanged:: 1.2
    Constructors accept member names
    and `IntFlag` constructors accept multiple arguments.
"""

import sublime

from .vendor.python.enum import IntEnum, IntFlag
from inspect import cleandoc

from ._util.enum import ExtensibleConstructorMeta, construct_union, construct_with_alternatives


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
                :annotation: = sublime.{pre}{name}
            """).format(name=item.name, pre=prefix_str) for item in enum
        ])

        return enum

    return decorator


construct_from_name = construct_with_alternatives(
    lambda cls, value: cls.__members__.get(value, None)
)


@autodoc('DIALOG')
@construct_from_name
class DialogResult(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with :func:`sublime.yes_no_cancel_dialog`.
    """
    CANCEL = sublime.DIALOG_CANCEL
    YES = sublime.DIALOG_YES
    NO = sublime.DIALOG_NO


@autodoc('CLASS')
@construct_union
@construct_from_name
class PointClass(IntFlag, metaclass=ExtensibleConstructorMeta):
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
@construct_union
@construct_from_name
class FindOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with several methods of :class:`sublime.View`:

    - :meth:`~sublime.View.find`
    - :meth:`~sublime.View.find_all`
    """
    LITERAL = sublime.LITERAL
    IGNORECASE = sublime.IGNORECASE


@autodoc()
@construct_union
@construct_from_name
class RegionOption(IntFlag, metaclass=ExtensibleConstructorMeta):
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
@construct_union
@construct_from_name
class PopupOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.View.show_popup`.
    """
    COOPERATE_WITH_AUTO_COMPLETE = sublime.COOPERATE_WITH_AUTO_COMPLETE
    HIDE_ON_MOUSE_MOVE = sublime.HIDE_ON_MOUSE_MOVE
    HIDE_ON_MOUSE_MOVE_AWAY = sublime.HIDE_ON_MOUSE_MOVE_AWAY


@autodoc('LAYOUT')
@construct_union
@construct_from_name
class PhantomLayout(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :class:`sublime.Phantom`.
    """
    INLINE = sublime.LAYOUT_INLINE
    BELOW = sublime.LAYOUT_BELOW
    BLOCK = sublime.LAYOUT_BLOCK


@autodoc()
@construct_union
@construct_from_name
class OpenFileOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.Window.open_file`.
    """
    ENCODED_POSITION = sublime.ENCODED_POSITION
    TRANSIENT = sublime.TRANSIENT


@autodoc()
@construct_union
@construct_from_name
class QuickPanelOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.Window.show_quick_panel`.
    """
    MONOSPACE_FONT = sublime.MONOSPACE_FONT
    KEEP_OPEN_ON_FOCUS_LOST = sublime.KEEP_OPEN_ON_FOCUS_LOST


@autodoc('HOVER')
@construct_from_name
class HoverLocation(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with
    :func:`sublime_plugin.EventListener.on_hover`.
    """
    TEXT = sublime.HOVER_TEXT
    GUTTER = sublime.HOVER_GUTTER
    MARGIN = sublime.HOVER_MARGIN


@autodoc('OP')
@construct_from_name
class QueryContextOperator(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with
    :func:`sublime_plugin.EventListener.on_query_context`.
    """
    EQUAL = sublime.OP_EQUAL
    NOT_EQUAL = sublime.OP_NOT_EQUAL
    REGEX_MATCH = sublime.OP_REGEX_MATCH
    NOT_REGEX_MATCH = sublime.OP_NOT_REGEX_MATCH
    REGEX_CONTAINS = sublime.OP_REGEX_CONTAINS
    NOT_REGEX_CONTAINS = sublime.OP_NOT_REGEX_CONTAINS


@autodoc()
@construct_union
@construct_from_name
class CompletionOptions(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with
    :func:`sublime_plugin.EventListener.on_query_completions`.
    """
    INHIBIT_WORD_COMPLETIONS = sublime.INHIBIT_WORD_COMPLETIONS
    INHIBIT_EXPLICIT_COMPLETIONS = sublime.INHIBIT_EXPLICIT_COMPLETIONS
