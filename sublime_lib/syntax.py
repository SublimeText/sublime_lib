from __future__ import annotations
from warnings import deprecated
from typing import TypeAlias

import sublime

__all__ = ['list_syntaxes', 'get_syntax_for_scope']


@deprecated(
    "sublime_lib.list_syntaxes() is deprecated, use sublime.list_syntaxes() instead!"
)
def list_syntaxes() -> list[sublime.Syntax]:
    return sublime.list_syntaxes()


@deprecated(
    "sublime_lib.get_syntax_for_scope() is deprecated, use sublime.find_syntax_by_scope() instead!"
)
def get_syntax_for_scope(scope: str) -> str:
    syntax = sublime.find_syntax_by_scope(scope)
    return syntax[0].path if syntax else ""
