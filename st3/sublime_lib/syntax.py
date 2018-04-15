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
        # JSON and YAML quotation rules are very similar, if not identical
        return sublime.decode_value(value)
    elif value == "true":
        return True
    elif value == "false":
        return False
    elif value == "null":
        return None
    else:
        # Does not handle numbers because we don't expect any
        return value


def get_syntax_metadata(path, text):
    ret = {}

    keys = {'name', 'scope', 'hidden'}

    for line in text.splitlines():
        m = re.match(r'^(\S.*?):\s*(.*)\s*$', line)
        if not m:
            continue
        key, value = map(_parse_yaml_value, m.groups())
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
