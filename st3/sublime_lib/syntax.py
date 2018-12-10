import sublime

import re
from collections import namedtuple
import plistlib

from ._util.collections import projection
from ._util.yaml import parse_simple_top_level_keys
from .resource_path import ResourcePath


__all__ = ['list_syntaxes', 'get_syntax_for_scope']


SyntaxInfo = namedtuple('SyntaxInfo', ['path', 'name', 'scope', 'hidden'])
SyntaxInfo.__new__.__defaults__ = (None, None, False)  # type: ignore


def get_yaml_metadata(text):
    return projection(
        parse_simple_top_level_keys(text),
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
    if path.suffix == '.sublime-syntax':
        meta = get_yaml_metadata(path.read_text())
    elif path.suffix == '.tmLanguage':
        meta = get_xml_metadata(path.read_bytes())
    else:
        raise TypeError("%s is not a syntax definition." % path)

    return SyntaxInfo(path=str(path), **meta)


def list_syntaxes():
    """Return a list of all loaded syntax definitions.

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
    return [
        get_syntax_metadata(path)
        for path in ResourcePath.glob_resources('')
        if path.suffix in ('.sublime-syntax', '.tmLanguage')
    ]


def get_syntax_for_scope(scope):
    """Returns the last syntax in load order that matches `scope`."""
    return next((
        syntax.path
        for syntax in reversed(list_syntaxes())
        if syntax.scope == scope
    ), None)
