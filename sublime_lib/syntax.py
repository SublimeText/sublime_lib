from __future__ import annotations

import sublime

__all__ = ['list_syntaxes', 'get_syntax_for_scope']


def list_syntaxes() -> list[sublime.Syntax]:
    print("sublime_lib.list_syntaxes() is deprecated,"
          " use sublime.list_syntaxes() instead!")
    return sublime.list_syntaxes()


def get_syntax_for_scope(scope: str) -> str:
    print("sublime_lib.get_syntax_for_scope() is deprecated,"
          " use sublime.find_syntax_by_scope() instead!")
    syntax = sublime.find_syntax_by_scope(scope)
    return syntax[0].path if syntax else ""
