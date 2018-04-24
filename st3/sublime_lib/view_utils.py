import inspect

from .syntax import get_syntax_for_scope
from .encodings import to_sublime


__all__ = ['new_view', 'close_view']


def new_view(window, **kwargs):
    """Open a new view in the given window, returning the View object.

    This function takes many optional keyword arguments:

    content:
        Text to be inserted into the new view. The text will be inserted even
        if the `read_only` option is True.

    encoding:
        The encoding that the view should use when saving.

    name:
        The name of the view. This will be shown as the title of the view's tab.

    overwrite:
        If True, the view will be in overwrite mode.

    read_only:
        If True, the view will be read-only.

    scope:
        A scope name. The view will be assigned a syntax definition that
        corresponds to the given scope (as determined by
        sublime_lib.syntax.get_syntax_for_scope). Exclusive with the `syntax`
        option.

    scratch:
        If True, the view will be a scratch buffer. The user will not be
        prompted to save the view before closing it.

    settings:
        A dictionary of names and values that will be applied to the new view's
        Settings object.

    syntax:
        The resource path of a syntax definition that the view will use.
        Exclusive with the `scope` option.
    """
    validate_view_options(kwargs)

    view = window.new_file()
    set_view_options(view, **kwargs)
    return view


def close_view(view, *, force=False):
    """
    Closes the given view. If the `force` argument is True, then any unsaved
    changes will be lost. Otherwise, if there are unsaved changes, ValueError
    will be raised.

    If the view is invalid (e.g. already closed), `close_view` will do nothing.
    """
    if not view.is_valid():
        return

    if view.window() is None:
        raise ValueError('The view has no associated window.')

    if view.is_dirty() and not view.is_scratch():
        if force:
            view.set_scratch(True)
        else:
            raise ValueError('The view has unsaved changes.')

    view.window().focus_view(view)
    view.window().run_command("close_file")


def validate_view_options(options):
    unknown = set(options) - VIEW_OPTIONS
    if unknown:
        raise ValueError('Unknown view options: %s.' % ', '.join(list(unknown)))

    if 'scope' in options and 'syntax' in options:
        raise ValueError('The "syntax" and "scope" arguments are exclusive.')


def set_view_options(
    view, *,
    name=None,
    settings=None,
    read_only=None,
    scratch=None,
    overwrite=None,
    syntax=None,
    scope=None,
    encoding=None,
    content=None
):
    if name is not None:
        view.set_name(name)

    if content is not None:
        view.run_command('append', {'characters': content})

    if settings is not None:
        view_settings = view.settings()
        for key, value in settings.items():
            view_settings.set(key, value)

    if read_only is not None:
        view.set_read_only(read_only)

    if scratch is not None:
        view.set_scratch(scratch)

    if overwrite is not None:
        view.set_overwrite_status(overwrite)

    if scope is not None:
        view.assign_syntax(get_syntax_for_scope(scope))

    if syntax is not None:
        view.assign_syntax(syntax)

    if encoding is not None:
        view.set_encoding(to_sublime(encoding))


VIEW_OPTIONS = {
    name
    for name, param in inspect.signature(set_view_options).parameters.items()
    if param.kind == inspect.Parameter.KEYWORD_ONLY
}
