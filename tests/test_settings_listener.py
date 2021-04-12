import sublime
from sublime_lib import ResourcePath, new_view, close_view
from .temporary_package import TemporaryPackage

from unittesting import DeferrableTestCase


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

        self.assertEqual(self.view.settings().get('changes'), [
            ['A', None],
            ['B', 'A'],
        ])
