from ._util.collections import is_sequence_not_str, isiterable
from ._util.named_value import NamedValue
from .flags import QuickPanelOption


__all__ = ['show_selection_panel', 'NO_SELECTION']


NO_SELECTION = NamedValue('NO_SELECTION')


def show_selection_panel(
    window,
    items,
    *,
    flags=0,
    labels=None,
    selected=NO_SELECTION,
    on_select=None,
    on_cancel=None,
    on_highlight=None
):
    """Open a quick panel in the given window to select an item from a list.

    :argument window: The :class:`sublime.Window` in which to show the panel.

    :argument items: A nonempty :class:`~collections.abc.Sequence`
        (such as a :class:`list`) of items to choose from.

    Optional keyword arguments:

    :argument flags: A :class:`sublime_lib.flags.QuickPanelOption`,
        a value convertible to :class:`~sublime_lib.flags.QuickPanelOption`,
        or an iterable of such values.

    :argument labels: A value determining what to show as the label for each item:

        - If `labels` is ``None`` (the default), then use `items`.
        - If `labels` is callable, then use ``map(labels, items)``.
        - Otherwise, use `labels`.

        The result should be a :class:`~collections.abc.Sequence` of labels.
        Every label must be a single item
        (a string or convertible with :func:`str`)
        or a :class:`~collections.abc.Sequence` of items.
        In the latter case,
        each entry in the quick panel will show multiple rows.

    :argument selected: The value in `items` that will be initially selected.

        If `selected` is :const:`sublime_lib.NO_SELECTION` (the default),
        then Sublime will determine the initial selection.

    :argument on_select: A callback accepting a value from `items`
        to be invoked when the user chooses an item.

    :argument on_cancel: A callback that will be invoked with no arguments
        if the user closes the panel without choosing an item.

    :argument on_highlight: A callback accepting a value from `items` to be
        invoked every time the user changes the highlighted item in the panel.

    :raise ValueError: if `items` is empty.

    :raise ValueError: if `selected` is given and the value is not in `items`.

    :raise ValueError: if some labels are sequences but not others
        or if labels are sequences of inconsistent length.

    :raise ValueError: if `flags` cannot be converted
        to :class:`sublime_lib.flags.QuickPanelOption`.

    ..  versionadded:: 1.2
    """
    if len(items) == 0:
        raise ValueError("The items parameter must contain at least one item.")

    if labels is None:
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

    if selected is NO_SELECTION:
        selected_index = -1
    else:
        selected_index = items.index(selected)

    on_highlight_callback = None
    if on_highlight:
        on_highlight_callback = lambda index: on_highlight(items[index])

    if isiterable(flags) and not isinstance(flags, str):
        flags = QuickPanelOption(*flags)
    else:
        flags = QuickPanelOption(flags)

    # The signature in the API docs is wrong.
    # See https://github.com/SublimeTextIssues/Core/issues/2290
    window.show_quick_panel(
        items=labels,
        on_select=on_done,
        flags=flags,
        selected_index=selected_index,
        on_highlight=on_highlight_callback
    )
