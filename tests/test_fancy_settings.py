import sublime
from sublime_lib import FancySettings
from sublime_lib import DefaultFancySettings

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

    def test_delete(self):
        self.fancy["example_setting"] = "Hello, World!"
        del self.fancy["example_setting"]
        self.assertNotIn("example_setting", self.fancy)

    def test_delete_missing_error(self):
        self.fancy["example_setting"] = "Hello, World!"
        del self.fancy["example_setting"]
        self.assertRaises(KeyError, self.fancy.__delitem__, "example_setting")

    def test_contains(self):
        self.assertNotIn("example_setting", self.fancy)
        self.fancy["example_setting"] = "Hello, World!"
        self.assertIn("example_setting", self.fancy)

    def test_pop(self):
        self.fancy["example_setting"] = "Hello, World!"
        result = self.fancy.pop("example_setting")

        self.assertEqual(result, "Hello, World!")
        self.assertNotIn("example_setting", self.fancy)

        default = self.fancy.pop("example_setting", 42)
        self.assertEqual(default, 42)

        self.assertRaises(KeyError, self.fancy.pop, "example_setting")

    def test_setdefault(self):
        result = self.fancy.setdefault("example_setting", "Hello, World!")

        self.assertEqual(result, "Hello, World!")
        self.assertEqual(self.fancy["example_setting"], "Hello, World!")

        result = self.fancy.setdefault("example_setting", 42)

        self.assertEqual(result, "Hello, World!")
        self.assertEqual(self.fancy["example_setting"], "Hello, World!")

    def test_setdefault_none(self):
        result = self.fancy.setdefault("example_setting")

        self.assertEqual(result, None)
        self.assertEqual(self.fancy["example_setting"], None)

    def test_update(self):
        self.fancy["foo"] = "Hello, World!"

        self.fancy.update({'foo': 1, 'bar': 2}, xyzzy=3)
        self.fancy.update([('bar', 20), ('baz', 30)], yzzyx=4)

        self.assertEqual(self.fancy['foo'], 1)
        self.assertEqual(self.fancy['bar'], 20)
        self.assertEqual(self.fancy['baz'], 30)
        self.assertEqual(self.fancy['xyzzy'], 3)
        self.assertEqual(self.fancy['yzzyx'], 4)


class TestFancySettingsSubscription(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.settings = self.view.settings()
        self.fancy = FancySettings(self.settings)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

        if self.fancy and getattr(self, 'key', None):
            self.fancy.unsubscribe(self.key)

    def test_subscribe(self):
        self.fancy['example_setting'] = 1

        values = None

        def callback(new, old):
            nonlocal values
            values = (new, old)

        self.key = self.fancy.subscribe('example_setting', callback)

        self.fancy['example_setting'] = 2
        self.assertEqual(values, (2, 1))

        self.fancy.unsubscribe(self.key)
        self.fancy['example_setting'] = 3
        self.assertEqual(values, (2, 1))

    def test_subscribe_multiple(self):
        self.fancy.update(
            example_1=1,
            example_2=2
        )

        values = None

        def callback(new, old):
            nonlocal values
            values = new

        self.key = self.fancy.subscribe({'example_1', 'example_2', 'example_3'}, callback)

        self.fancy['example_1'] = 10

        self.assertEqual(values, {
            'example_1': 10,
            'example_2': 2
        })


class TestDefaultFancySettings(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.settings = self.view.settings()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_get_default(self):
        self.fancy = DefaultFancySettings(self.settings, {
            'example_1': 'Hello, World!',
        })

        self.assertEqual(self.fancy['example_1'], 'Hello, World!')

        self.fancy['example_1'] = 'Goodbye, World!'
        self.assertEqual(self.fancy['example_1'], 'Goodbye, World!')

        self.fancy.__missing__('example_1')
        self.assertEqual(self.fancy['example_1'], 'Hello, World!')

        self.assertRaises(KeyError, self.fancy.__getitem__, 'example_2')
