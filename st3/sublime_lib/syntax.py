import sublime

import re
from collections import namedtuple

import plistlib

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


def projection(d, keys):
    if isinstance(keys, dict):
        return {
            keys[key]: value
            for key, value in d.items()
            if key in keys
        }
    else:
        return {
            key: value
            for key, value in d.items()
            if key in keys
        }


def get_yaml_metadata(text):
    return projection(
        dict(
            map(_parse_yaml_value, match.groups())
            for match in re.finditer(r'(?m)^(\S.*?):\s*(.*)\s*$', text)
        ),
        {'name', 'hidden', 'scope'}
    )


def get_xml_metadata(text):
    tree = plistlib.readPlistFromBytes(text)

    return projection(tree, {
        'name': 'name',
        'hidden': 'hidden',
        'scopeName': 'scope',
    })


def get_syntax_metadata(path):
    if path.endswith('.sublime-syntax'):
        meta = get_yaml_metadata(sublime.load_resource(path))
    elif path.endswith('.tmLanguage'):
        meta = get_xml_metadata(sublime.load_binary_resource(path))
    else:
        raise TypeError("%s is not a syntax definition." % path)

    return SyntaxInfo(path=path, **meta)


def list_syntaxes():
    return [
        get_syntax_metadata(path)
        for path in (
            sublime.find_resources('*.sublime-syntax') +
            sublime.find_resources('*.tmLanguage')
        )
    ]


def get_syntax_for_scope(scope):
    return next((
        syntax.path
        for syntax in list_syntaxes()
        if syntax.scope == scope
    ), None)
