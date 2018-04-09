import sublime

from .view_stream import ViewStream

class OutputPanel(ViewStream):
    def __init__(self, window, name):
        super().__init__(window.get_output_panel(name))

        self.window = window
        self.name = name

    @property
    def full_name(self):
        return "output.%s" % self.name

    def show(self):
        self.window.run_command("show_panel", { "panel": self.full_name })

    def hide(self):
        self.window.run_command("hide_panel", { "panel": self.full_name })

    def destroy(self):
        self.window.destroy_output_panel(self.name)
