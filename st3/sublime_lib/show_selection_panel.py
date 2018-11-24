from collections.abc import Sequence


__all__ = ['show_selection_panel']


NOT_GIVEN = object()


def is_sequence_not_str(obj):
    return isinstance(obj, Sequence) and not isinstance(obj, str)


def show_selection_panel(
    window,
    items,
    *,
    flags=0,
    labels=NOT_GIVEN,
    selected=NOT_GIVEN,
    on_select=None,
    on_cancel=None,
    on_highlight=None
):
    """Open a quick panel in the given window to select an item from a list.

    :argument window: The :class:`sublime.Window` in which to show the panel.

    :argument items: A nonempty :class:`list` of items to choose from.

    Optional keyword arguments:

    :argument flags: A bitwise OR of :const:`sublime.MONOSPACE_FONT` and
    :const:`sublime.KEEP_OPEN_ON_FOCUS_LOST`.

    :argument labels: Either a list of labels or a function taking elements of
    `items` to labels. If `labels` is not given, it will default to `items`.

    Every label must be a single item (a string or convertible with :func:`str`)
    or a :class:`collections.abc.Sequence` of items (such as a :class:`list` or
    :class:`tuple`). In the latter case, each entry in the quick panel will show
    multiple rows.

    :argument selected: The value in `items` that will be initially selected.
    If `selected` is not given, no value will be initially selected.

    :argument on_select: A callback accepting a value from `items` to be
    invoked when the user chooses an item.

    :argument on_cancel: A callback that will be invoked with no arguments if
    the user closes the panel without choosing an item.

    :argument on_highlight: A callback accepting a value from `items` to be
    invoked every time the user changes the highlighted item in the panel.

    :raises ValueError: if `items` is empty`.

    :raises ValueError: if `selected` is given and the value is not in `items`.

    :raises ValueError: if some labels are sequences but not others or if labels
    are sequences of inconsistent length.
    """
    if len(items) == 0:
        raise ValueError("The items parameter must contain at least one item.")

    if labels is NOT_GIVEN:
        labels = items
    elif callable(labels):
        labels = list(map(labels, items))
    elif len(items) != len(labels):
        raise ValueError("The lengths of `items` and `labels` must match.")

    if any(map(is_sequence_not_str, labels)):
        if not all(map(is_sequence_not_str, labels)):
            raise ValueError("Labels must be all strings or all lists.")

        if len(set(map(len, labels))) != 1:
            raise ValueError(
                "If labels are lists, they must all have the same number of elements.")

        labels = list(map(lambda label: list(map(str, label)), labels))
    else:
        labels = list(map(str, labels))

    def on_done(index):
        if index == -1:
            if on_cancel:
                on_cancel()
        elif on_select:
            on_select(items[index])

    if selected is NOT_GIVEN:
        selected_index = -1
    else:
        selected_index = items.index(selected)

    if on_highlight:
        on_highlight_callback = lambda index: on_highlight(items[index])
    else:
        on_highlight_callback = None

    # The signature in the API docs is wrong.
    # See https://github.com/SublimeTextIssues/Core/issues/2290
    window.show_quick_panel(
        items=labels,
        on_select=on_done,
        flags=flags,
        selected_index=selected_index,
        on_highlight=on_highlight_callback
    )
