import sublime
from sublime_lib.settings_dict import NamedSettingsDict

import os
from os import path

from unittesting import DeferrableTestCase


class TestNamedSettingsDict(DeferrableTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.name = "_sublime_lib_NamedSettingsDictTest.sublime-settings"
        self.settings_path = path.join(sublime.packages_path(), 'User', self.name)
        self.fancy = NamedSettingsDict(self.name)

    def tearDown(self):
        if path.exists(self.settings_path):
            os.remove(self.settings_path)

    def test_named(self):
        other = NamedSettingsDict(self.name)

        self.fancy["example_setting"] = "Hello, World!"

        self.assertIn("example_setting", self.fancy)
        self.assertIn("example_setting", other)

        self.fancy.save()

        yield

        self.assertTrue(path.exists(self.settings_path))
