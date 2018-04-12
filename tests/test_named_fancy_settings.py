import sublime
from sublime_lib import FancySettings

import os
from os import path

from unittesting import DeferrableTestCase

class TestNamedFancySettings(DeferrableTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.name = "_sublime_lib_FancySettingsTest.sublime-settings"
        self.settings_path = path.join(sublime.packages_path(), 'User', self.name)
        self.fancy = FancySettings(self.name)

    def tearDown(self):
        if path.exists(self.settings_path):
            os.remove(self.settings_path)

    def test_named(self):
        other = FancySettings(self.name)

        self.fancy["example_setting"] = "Hello, World!"

        self.assertIn("example_setting", self.fancy)
        self.assertIn("example_setting", other)

        self.fancy.save()

        yield

        self.assertTrue(path.exists(self.settings_path))
