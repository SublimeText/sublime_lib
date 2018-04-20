from .view_stream import ViewStream


class OutputPanel(ViewStream):
    def __init__(
        self, window, name, *,
        force_writes=False,
        settings=None,
        read_only=None
    ):
        super().__init__(
            window.get_output_panel(name),
            force_writes=force_writes
        )

        self.window = window
        self.name = name

        if settings is not None:
            view_settings = self.view.settings()
            for key, value in settings.items():
                view_settings.set(key, value)

        if read_only is not None:
            self.view.set_read_only(read_only)

    @property
    def full_name(self):
        return "output.%s" % self.name

    @ViewStream.guard_validity
    def show(self):
        self.window.run_command("show_panel", {"panel": self.full_name})

    @ViewStream.guard_validity
    def hide(self):
        self.window.run_command("hide_panel", {"panel": self.full_name})

    def destroy(self):
        self.window.destroy_output_panel(self.name)
