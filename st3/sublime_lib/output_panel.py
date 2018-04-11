from .view_stream import ViewStream


class OutputPanel(ViewStream):
    def __init__(self, window, name, *, settings=None):
        super().__init__(window.get_output_panel(name))

        self.window = window
        self.name = name

        if settings:
            view_settings = self.view.settings()
            for key, value in settings.items():
                view_settings.set(key, value)

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
