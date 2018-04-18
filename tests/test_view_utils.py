import sublime
from sublime_lib.view_utils import new_view

from unittest import TestCase


class TestViewUtils(TestCase):

    def setUp(self):
        self.window = sublime.active_window()

    def tearDown(self):
        if getattr(self, 'view', None):
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_new_view(self):
        self.view = new_view(self.window)

        self.assertTrue(self.view.is_valid())

        self.assertEquals(self.view.name(), '')
        self.assertFalse(self.view.is_read_only())
        self.assertFalse(self.view.is_scratch())

        self.assertEquals(self.view.scope_name(0).strip(), 'text.plain')

    def test_name(self):
        self.view = new_view(self.window, name='My Name')

        self.assertEquals(self.view.name(), 'My Name')

    def test_read_only(self):
        self.view = new_view(self.window, read_only=True)

        self.assertTrue(self.view.is_read_only())

    def test_scratch(self):
        self.view = new_view(self.window, scratch=True)

        self.assertTrue(self.view.is_scratch())

    def test_settings(self):
        self.view = new_view(self.window, settings={
            'example_setting': 'Hello, World!',
        })

        self.assertEquals(
            self.view.settings().get('example_setting'),
            'Hello, World!'
        )

    def test_scope(self):
        self.view = new_view(self.window, scope='source.js')

        self.assertTrue(self.view.scope_name(0).startswith('source.js'))
