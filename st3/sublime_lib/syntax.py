import sublime

import re

__all__ = ['list_syntaxes', 'get_syntax_for_scope']


class SyntaxInfo():
    __slots__ = ['path', 'name', 'scope', 'hidden']

    def __init__(self, path, name=None, scope=None, hidden=False):
        self.path = path
        self.name = name
        self.scope = scope
        self.hidden = hidden

    def __eq__(self, other):
        return ((self.path, self.name, self.scope, self.hidden)
                == (other.path, other.name, other.scope, other.hidden))


def get_syntax_metadata(path, text):
    ret = {}

    keys = {'name', 'scope', 'hidden'}

    for line in text.splitlines():
        m = re.match(r'^(\w+):\s*(.*?)\s*$', line)
        if not m:
            continue
        key, value = m.groups()
        if key in keys:
            ret[key] = value

    return SyntaxInfo(path=path, **ret)


def list_syntaxes():
    return [
        get_syntax_metadata(path, sublime.load_resource(path))
        for path in sublime.find_resources('*.sublime-syntax')
    ]


def get_syntax_for_scope(scope):
    return next((
        syntax.path
        for syntax in list_syntaxes()
        if syntax.scope == scope
    ), None)
