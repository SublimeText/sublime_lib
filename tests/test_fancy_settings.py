import sublime
from sublime_lib import FancySettings

from sublime_lib.testing import ViewTestCase

class TestFancySettings(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.settings = self.view.settings()
        self.fancy = FancySettings(self.settings)


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

        self.fancy.update({'foo': 1, 'bar': 2}, xyzzy = 3)
        self.fancy.update([('bar', 20), ('baz', 30)], yzzyx = 4)

        self.assertEqual(self.fancy['foo'], 1)
        self.assertEqual(self.fancy['bar'], 20)
        self.assertEqual(self.fancy['baz'], 30)
        self.assertEqual(self.fancy['xyzzy'], 3)
        self.assertEqual(self.fancy['yzzyx'], 4)
