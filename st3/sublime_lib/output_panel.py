from .view_stream import ViewStream
from .view_utils import set_view_options, validate_view_options


class OutputPanel(ViewStream):
    @classmethod
    def create(
        cls,
        window, name, *,
        force_writes=False,
        unlisted=False,
        **kwargs
    ):
        validate_view_options(kwargs)

        window.destroy_output_panel(name)
        view = window.create_output_panel(name, unlisted)
        set_view_options(view, **kwargs)

        return cls(window, name, force_writes=force_writes)

    def __init__(
        self, window, name, *,
        force_writes=False
    ):
        view = window.find_output_panel(name)
        if view is None:
            raise ValueError('Output panel "%s" does not exist.' % name)

        super().__init__(view, force_writes=force_writes)

        self.window = window
        self.name = name

    @property
    def full_name(self):
        return "output.%s" % self.name

    @ViewStream.guard_validity
    def is_visible(self):
        return self.window.active_panel() == self.full_name

    @ViewStream.guard_validity
    def show(self):
        self.window.run_command("show_panel", {"panel": self.full_name})

    @ViewStream.guard_validity
    def hide(self):
        self.window.run_command("hide_panel", {"panel": self.full_name})

    @ViewStream.guard_validity
    def toggle_visibility(self):
        if self.is_visible():
            self.hide()
        else:
            self.show()

    def destroy(self):
        self.window.destroy_output_panel(self.name)
