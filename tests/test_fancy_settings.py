import sublime
from sublime_lib import FancySettings

from unittest import TestCase

class TestFancySettings(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.settings = self.view.settings()
        self.settings.set("example_setting", "Hello, World!")

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_get(self):
        fancy = FancySettings(self.settings)

        self.assertEqual(fancy['example_setting'], "Hello, World!")
