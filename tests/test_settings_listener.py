import sublime
from sublime_lib import ResourcePath, new_view, close_view
from .temporary_package import TemporaryPackage

from unittest import TestCase
from unittesting import DeferrableTestCase

from sublime_lib import GlobalSettingsListener


class TestViewSettingsListener(DeferrableTestCase):
    def setUp(self):
        self.view = new_view(sublime.active_window())
        self.temporary_package = TemporaryPackage(
            'sublime_lib_settings_listener_test',
            ResourcePath("Packages/sublime_lib/tests/settings_listener_package")
        )
        self.temporary_package.create()
        yield self.temporary_package.exists

    def tearDown(self):
        self.temporary_package.destroy()
        if getattr(self, 'view', None):
            try:
                close_view(self.view, force=True)
            except ValueError:
                pass

    def test_view_listener(self):
        self.view.settings().set('foo', 'A')
        self.view.settings().set('foo', 'B')

        self.temporary_package.destroy()
        yield lambda: not self.temporary_package.exists()

        self.view.settings().set('foo', 'C')

        self.assertEqual(self.view.settings().get('changes'), [
            ['A', None],
            ['B', 'A'],
        ])


class TestGlobalSettingsListener(DeferrableTestCase):
    def setUp(self):
        name = 'TestGlobalSettingsListener:{}'.format(str(id(self)))
        self.settings = sublime.load_settings(name + '.sublime-settings')
        self.settings.set('changes', [])
        self.settings.set('foo', None)
        self.temporary_package = TemporaryPackage(
            name,
            ResourcePath("Packages/sublime_lib/tests/settings_listener_package")
        )
        self.temporary_package.create()
        yield self.temporary_package.exists

    def tearDown(self):
        self.temporary_package.destroy()

    def test_global_listener(self):
        self.settings.set('foo', 'A')
        self.settings.set('foo', 'B')

        self.temporary_package.destroy()
        yield lambda: not self.temporary_package.exists()
        yield 100
        import gc
        gc.collect()
        yield 100

        self.settings.set('foo', 'C')

        self.assertEqual(self.settings.get('changes'), [
            ['A', None],
            ['B', 'A'],
        ])


class TestGlobalSettingsListenerErrors(TestCase):
    def test_instantiate_base(self):
        GlobalSettingsListener()

    def test_instantiate_without_name(self):
        class TestListener(GlobalSettingsListener):
            pass

        with self.assertRaises(RuntimeError):
            TestListener()
