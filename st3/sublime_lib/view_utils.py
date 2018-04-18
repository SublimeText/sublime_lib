from .syntax import get_syntax_for_scope


def new_view(window, **kwargs):
    view = window.new_file()
    set_view_options(view, **kwargs)
    return view


def set_view_options(
    view, *,
    name=None,
    settings=None,
    read_only=None,
    scratch=None,
    syntax=None,
    scope=None
):
    if name is not None:
        view.set_name(name)

    if settings is not None:
        view_settings = view.settings()
        for key, value in settings.items():
            view_settings.set(key, value)

    if read_only is not None:
        view.set_read_only(read_only)

    if scratch is not None:
        view.set_scratch(scratch)

    if scope is not None:
        view.assign_syntax(get_syntax_for_scope(scope))

    if syntax is not None:
        view.assign_syntax(syntax)
