from .view_stream import ViewStream
from .view_utils import set_view_options


class OutputPanel(ViewStream):
    def __init__(
        self, window, name, *,
        force_writes=False,
        **kwargs
    ):
        super().__init__(
            window.get_output_panel(name),
            force_writes=force_writes
        )

        self.window = window
        self.name = name

        set_view_options(self.view, **kwargs)

    @property
    def full_name(self):
        return "output.%s" % self.name

    def show(self):
        self._check_is_valid()
        self.window.run_command("show_panel", {"panel": self.full_name})

    def hide(self):
        self._check_is_valid()
        self.window.run_command("hide_panel", {"panel": self.full_name})

    def destroy(self):
        self.window.destroy_output_panel(self.name)
