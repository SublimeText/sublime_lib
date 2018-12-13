from .view_stream import ViewStream
from .view_utils import set_view_options, validate_view_options


__all__ = ['OutputPanel']


class OutputPanel(ViewStream):
    """A :class:`~sublime_lib.view_stream.ViewStream`
    wrapping an output panel in the given `window` with the given `name`.

    :raise ValueError: if `window` has no output panel called `name`.
    """
    @classmethod
    def create(
        cls,
        window, name, *,
        force_writes=False,
        follow_cursor=False,
        unlisted=False,
        **kwargs
    ):
        """Create a new output panel with the given `name` in the given `window`.

        If `kwargs` are given,
        they will be interpreted as for :func:`~sublime_lib.view_utils.new_view`.
        """
        validate_view_options(kwargs)

        window.destroy_output_panel(name)
        view = window.create_output_panel(name, unlisted)
        set_view_options(view, **kwargs)

        return cls(window, name, force_writes=force_writes, follow_cursor=follow_cursor)

    def __init__(
        self, window, name, *,
        force_writes=False,
        follow_cursor=False
    ):
        view = window.find_output_panel(name)
        if view is None:
            raise ValueError('Output panel "%s" does not exist.' % name)

        super().__init__(view, force_writes=force_writes, follow_cursor=follow_cursor)

        self.window = window
        self.name = name

    @property
    def full_name(self):
        """The output panel name, beginning with ``'output.'``.

        Generally, API methods specific to output panels will use :attr:`name`,
        while methods that work with any panels will use :attr:`full_name`.
        """
        return "output.%s" % self.name

    @ViewStream.guard_validity
    def is_visible(self):
        """Return ``True`` if the output panel is currently visible."""
        return self.window.active_panel() == self.full_name

    @ViewStream.guard_validity
    def show(self):
        """Show the output panel, hiding any other visible panel."""
        self.window.run_command("show_panel", {"panel": self.full_name})

    @ViewStream.guard_validity
    def hide(self):
        """Hide the output panel."""
        self.window.run_command("hide_panel", {"panel": self.full_name})

    @ViewStream.guard_validity
    def toggle_visibility(self):
        """If the output panel is visible, hide it; otherwise, show it."""
        if self.is_visible():
            self.hide()
        else:
            self.show()

    def destroy(self):
        """Destroy the output panel."""
        self.window.destroy_output_panel(self.name)
