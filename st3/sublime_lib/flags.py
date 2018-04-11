import sublime

from .enum import IntEnum, IntFlag


class DialogResult(IntEnum):
    CANCEL = sublime.DIALOG_CANCEL
    YES = sublime.DIALOG_YES
    NO = sublime.DIALOG_NO


class PointClass(IntFlag):
    WORD_START = sublime.CLASS_WORD_START
    WORD_END = sublime.CLASS_WORD_END
    PUNCTUATION_START = sublime.CLASS_PUNCTUATION_START
    PUNCTUATION_END = sublime.CLASS_PUNCTUATION_END
    SUB_WORD_START = sublime.CLASS_SUB_WORD_START
    SUB_WORD_END = sublime.CLASS_SUB_WORD_END
    LINE_START = sublime.CLASS_LINE_START
    LINE_END = sublime.CLASS_LINE_END
    EMPTY_LINE = sublime.CLASS_EMPTY_LINE


class FindOption(IntFlag):
    LITERAL = sublime.LITERAL
    IGNORECASE = sublime.IGNORECASE


class RegionOption(IntFlag):
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


class PopupOption(IntFlag):
    COOPERATE_WITH_AUTO_COMPLETE = sublime.COOPERATE_WITH_AUTO_COMPLETE
    HIDE_ON_MOUSE_MOVE = sublime.HIDE_ON_MOUSE_MOVE
    HIDE_ON_MOUSE_MOVE_AWAY = sublime.HIDE_ON_MOUSE_MOVE_AWAY


class PhantomLayout(IntFlag):
    INLINE = sublime.LAYOUT_INLINE
    BELOW = sublime.LAYOUT_BELOW
    BLOCK = sublime.LAYOUT_BLOCK


class OpenFileOption(IntFlag):
    ENCODED_POSITION = sublime.ENCODED_POSITION
    TRANSIENT = sublime.TRANSIENT


class QuickPanelOption(IntFlag):
    MONOSPACE_FONT = sublime.MONOSPACE_FONT
    KEEP_OPEN_ON_FOCUS_LOST = sublime.KEEP_OPEN_ON_FOCUS_LOST
