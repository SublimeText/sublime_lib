import sublime

import re
from collections import namedtuple
import plistlib

from ._util.collections import projection


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


def get_yaml_metadata(text):
    return projection(
        dict(
            # map(_parse_yaml_value, match.groups())
            (
                _parse_yaml_value(match[1]),
                _parse_yaml_value(match[2]),
            )
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
    """
    Return a list of all loaded syntax definitions.

    Each item is a :class:`namedtuple` with the following properties:

    path
        The resource path to the syntax definition file.

    name
        The display name of the syntax definition.

    scope
        The top-level scope of the syntax.

    hidden
        Whether the syntax will appear in the syntax menus and the command palette.
    """
    syntaxes = [
        get_syntax_metadata(path)
        for path in (
            sublime.find_resources('*.sublime-syntax') + sublime.find_resources('*.tmLanguage')
        )
    ]

    def sort_key(syntax):
        path = syntax.path
        if path.startswith('Packages/Default'):
            return (0, path)
        elif path.startswith('Packages/User'):
            return (2, path)
        else:
            return (1, path)

    syntaxes.sort(key=sort_key)
    return syntaxes


def get_syntax_for_scope(scope):
    """
    Returns the last syntax in load order that matches `scope`.
    """
    return next((
        syntax.path
        for syntax in reversed(list_syntaxes())
        if syntax.scope == scope
    ), None)
