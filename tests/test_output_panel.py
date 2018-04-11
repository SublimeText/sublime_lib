import sublime
from sublime_lib import OutputPanel

from unittest import TestCase


class TestOutputPanel(TestCase):

    def setUp(self):
        self.window = sublime.active_window()
        self.panel_to_restore = self.window.active_panel()

        self.panel_name = "test_panel"
        self.panel = OutputPanel(self.window, self.panel_name)

    def tearDown(self):
        self.panel.destroy()

        if self.panel_to_restore:
            self.window.run_command("show_panel", {"panel": self.panel_to_restore})

    def assertContents(self, text):
        view = self.panel.view
        self.assertEqual(
            view.substr(sublime.Region(0, view.size())),
            text
        )

    def test_stream_operations(self):
        self.panel.write("Hello, ")
        self.panel.print("World!")

        self.panel.seek_start()
        self.panel.print("Top")

        self.panel.seek_end()
        self.panel.print("Bottom")

        self.panel.seek(4)
        self.panel.print("After Top")

        self.assertContents("Top\nAfter Top\nHello, World!\nBottom\n")

    def test_clear(self):
        self.panel.write("Some text")
        self.panel.clear()
        self.assertContents("")

    def test_show_hide(self):
        self.panel.show()

        self.assertEqual(self.window.active_panel(), self.panel.full_name)

        self.panel.hide()

        self.assertNotEqual(self.window.active_panel(), self.panel.full_name)

    def test_exists(self):
        self.assertIsNotNone(self.window.find_output_panel(self.panel.name))

    def test_destroy(self):
        self.panel.destroy()
        self.assertIsNone(self.window.find_output_panel(self.panel.name))
