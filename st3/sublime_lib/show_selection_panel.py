NOT_GIVEN = object()


def show_selection_panel(
    window,
    items,
    *,
    flags=None,
    labels=str,
    selected=NOT_GIVEN,
    on_select=None,
    on_cancel=None,
    on_highlight=None
):
    """Open a quick panel in the given window to select an item from a list.

    :argument window: The :class:`sublime.Window` in which to show the panel.

    :argument items: A :class:`list` of items to choose from.

    Optional keyword arguments:

    :argument flags: A bitwise OR of :const:`sublime.MONOSPACE_FONT` and
    :const:`sublime.KEEP_OPEN_ON_FOCUS_LOST`.

    :argument labels: A function taking elements of `items` to string labels.

    :argument selected: The value in `items` that will be initially selected.
    If `selected` is not given, no value will be initially selected.

    :argument on_select: A callback accepting a value from `items` to be
    invoked when the user chooses an item.

    :argument on_cancel: A callback that will be invoked with no arguments if
    the user closes the panel without choosing an item.

    :argument on_highlight: A callback accepting a value from `items` to be
    invoked every time the user changes the highlighted item in the panel.
    """
    labels_list = list(map(labels, items))

    def on_done(index):
        if index == -1:
            if on_cancel:
                on_cancel()
        else:
            if on_select:
                on_select(items[index])

    if selected is NOT_GIVEN:
        selected_index = None
    else:
        selected_index = items.index(selected)

    if on_highlight:
        on_highlight_callback = lambda index: on_highlight(items[index])
    else:
        on_highlight_callback = None

    # The signature in the API docs is wrong.
    # See https://github.com/SublimeTextIssues/Core/issues/2290
    window.show_quick_panel(
        items=labels_list,
        on_select=on_done,
        flags=flags,
        selected_index=selected_index,
        on_highlight=on_highlight_callback
    )
