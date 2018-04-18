from .syntax import get_syntax_for_scope
from .encodings import to_sublime


def new_view(window, **kwargs):
    if 'scope' in kwargs and 'syntax' in kwargs:
        raise TypeError('The "syntax" and "scope" arguments are exclusive.')

    view = window.new_file()
    set_view_options(view, **kwargs)
    return view


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
        view.run_command('insert', {'characters': content})

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
