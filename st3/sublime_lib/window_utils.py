import sublime


__all__ = ['new_window', 'close_window']


def new_window(
    *,
    menu_visible=None,
    sidebar_visible=None,
    tabs_visible=None,
    minimap_visible=None,
    status_bar_visible=None,
    project_data=None
):
    """Open a new window, returning the :class:`~sublime.Window` object.

    :raises RuntimeError: if the window is not created for any reason.
    """
    original_ids = set(window.id() for window in sublime.windows())

    sublime.run_command('new_window')

    try:
        window = next(window for window in sublime.windows() if window.id() not in original_ids)
    except StopIteration:
        raise RuntimeError("Window not created.")

    if menu_visible is not None:
        window.set_menu_visible(menu_visible)

    if sidebar_visible is not None:
        window.set_sidebar_visible(sidebar_visible)

    if tabs_visible is not None:
        window.set_tabs_visible(tabs_visible)

    if minimap_visible is not None:
        window.set_minimap_visible(minimap_visible)

    if status_bar_visible is not None:
        window.set_status_bar_visible(status_bar_visible)

    if project_data is not None:
        window.set_project_data(project_data)

    return window


def close_window(window, *, force=False):
    """
    Close the given window, discarding unsaved changes if `force` is ``True``.

    :raise ValueError: if any view in the window has unsaved changes and `force`
    is not ``True``.
    """
    for view in window.views():
        if view.is_dirty() and not view.is_scratch():
            if force:
                view.set_scratch(True)
            else:
                raise ValueError('A view has unsaved changes.')

    window.run_command('close_window')
