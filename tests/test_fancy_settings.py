import sublime
from sublime_lib import FancySettings

from unittest import TestCase

class TestFancySettings(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.settings = self.view.settings()
        self.fancy = FancySettings(self.settings)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")


    def test_item(self):
        self.settings.set("example_setting", "Hello, World!")

        self.assertEqual(self.fancy['example_setting'], "Hello, World!")

    def test_item_missing_error(self):
        self.settings.erase("example_setting")

        self.assertRaises(KeyError, lambda k: self.fancy[k], "example_setting")


    def test_get(self):
        self.settings.set("example_setting", "Hello, World!")

        self.assertEqual(self.fancy.get('example_setting'), "Hello, World!")

    def test_get_missing_none(self):
        self.settings.erase("example_setting")

        self.assertIsNone(self.fancy.get("example_setting"))

    def test_get_missing_default(self):
        self.settings.erase("example_setting")

        self.assertEqual(self.fancy.get("example_setting", "default"), "default")


    def test_set(self):
        self.fancy["example_setting"] = "Hello, World!"

        self.assertEqual(self.settings.get('example_setting'), "Hello, World!")


    def test_update(self):
        self.fancy["foo"] = "Hello, World!"

        self.fancy.update({'foo': 1, 'bar': 2}, xyzzy = 3)
        self.fancy.update([('bar', 20), ('baz', 30)], yzzyx = 4)

        self.assertEqual(self.fancy['foo'], 1)
        self.assertEqual(self.fancy['bar'], 20)
        self.assertEqual(self.fancy['baz'], 30)
        self.assertEqual(self.fancy['xyzzy'], 3)
        self.assertEqual(self.fancy['yzzyx'], 4)
