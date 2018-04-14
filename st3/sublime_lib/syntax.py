import sublime

import re
from collections import namedtuple

__all__ = ['list_syntaxes', 'get_syntax_for_scope']


SyntaxInfo = namedtuple('SyntaxInfo', ['path', 'name', 'scope', 'hidden'])
SyntaxInfo.__new__.__defaults__ = (None, None, False)  # type: ignore


def _parse_yaml_value(value):
    if value.startswith("'"):
        return value[1:-1].replace("''", "'")
    elif value.startswith('"'):
        # This is a simplifcation but one that should do for now
        return re.sub(r"\\(.)", r"\1", value[1:-1])
    elif value == "true":
        return True
    elif value == "false":
        return False
    else:
        return value


def get_syntax_metadata(path, text):
    ret = {}

    keys = {'name', 'scope', 'hidden'}

    for line in text.splitlines():
        m = re.match(r'^(\w+):\s*(.*)\s*$', line)
        if not m:
            continue
        key, value = m.groups()
        if key in keys:
            ret[key] = _parse_yaml_value(value)

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
