from .view_stream import ViewStream
from .view_utils import set_view_options, validate_view_options


class OutputPanel(ViewStream):
    def __init__(
        self, window, name, *,
        force_writes=False,
        unlisted=False,
        **kwargs
    ):
        validate_view_options(kwargs)

        super().__init__(
            window.create_output_panel(name, unlisted),
            force_writes=force_writes
        )

        self.window = window
        self.name = name

        set_view_options(self.view, **kwargs)

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
