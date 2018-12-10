from collections import namedtuple
import plistlib

from ._util.yaml import parse_simple_top_level_keys
from .resource_path import ResourcePath


__all__ = ['list_syntaxes', 'get_syntax_for_scope']


SyntaxInfo = namedtuple('SyntaxInfo', ['path', 'name', 'scope', 'hidden'])
SyntaxInfo.__new__.__defaults__ = (None, None, False)  # type: ignore


def get_sublime_syntax_metadata(path):
    yaml = parse_simple_top_level_keys(path.read_text())
    return {
        'name': yaml.get('name') or path.stem,
        'hidden': yaml.get('hidden', False),
        'scope': yaml.get('scope'),
    }


def get_tmlanguage_metadata(path):
    tree = plistlib.readPlistFromBytes(path.read_bytes())

    return {
        'name': tree.get('name') or path.stem,
        'hidden': tree.get('hidden', False),
        'scope': tree.get('scopeName'),
    }


def get_hidden_tmlanguage_metadata(path):
    tree = plistlib.readPlistFromBytes(path.read_bytes())

    return {
        'name': path.stem, # `name` key is ignored
        'hidden': True, # `hidden` key is ignored
        'scope': tree.get('scopeName'),
    }


SYNTAX_TYPES = {
    '.sublime-syntax': get_sublime_syntax_metadata,
    '.tmLanguage': get_tmlanguage_metadata,
    '.hidden-tmLanguage': get_hidden_tmlanguage_metadata,
}


def get_syntax_metadata(path):
    return SyntaxInfo(
        path=str(path),
        **SYNTAX_TYPES[path.suffix](path)
    )


def shadowed(path):
    return (
        path.suffix in {'.tmLanguage', '.hidden-tmLanguage'}
        and path.with_suffix('.sublime-syntax').exists()
    )


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
        if path.suffix in SYNTAX_TYPES and not shadowed(path)
    ]


def get_syntax_for_scope(scope):
    """Returns the last syntax in load order that matches `scope`."""
    return next((
        syntax.path
        for syntax in reversed(list_syntaxes())
        if syntax.scope == scope
    ), None)
