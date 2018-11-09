NOT_GIVEN = {}


def show_selection_panel(
    window,
    items,
    *,
    flags=None,
    labels=str,
    selected=NOT_GIVEN,
    on_selected=None,
    on_cancel=None,
    on_highlighted=None
):
    """Open a quick panel in the given window to select an item from a list.

    :argument window: The :class:`sublime.Window` in which to show the panel.

    :argument items: A :class:`list` of items to choose from.

    Optional keyword arguments:

    :argument flags: TODO

    :argument labels: A function taking elements of `items` to string labels.

    :argument selected: The value in `items` that will be initially selected.
    If `selected` is not given, no value will be initially selected.

    :argument on_selected: A callback accepting a value from `items` to be
    invoked when the user chooses an item.

    :argument on_cancel: A callback that will be invoked with no arguments if
    the user closes the panel without choosing an item.

    :argument on_highlighted: A callback accepting a value from `items` to be
    invoked every time the user changes the highlighted item in the panel.
    """
    labels_list = list(map(labels, items))

    def on_done(index):
        if index == -1:
            if on_cancel:
                on_cancel()
        else:
            if on_selected:
                on_selected(items[index])

    if selected == NOT_GIVEN:
        selected_index = None
    else:
        selected_index = items.index(selected)

    if on_highlighted:
        on_highlighted_callback = lambda index: on_highlighted(items[index])
    else:
        on_highlighted_callback = None

    # The signature in the API docs is wrong.
    # See https://github.com/SublimeTextIssues/Core/issues/2290
    window.show_quick_panel(
        items=labels_list,
        on_select=on_done,
        flags=flags,
        selected_index=selected_index,
        on_highlight=on_highlighted_callback
    )
