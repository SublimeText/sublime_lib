import sublime
from sublime_lib import ViewStream

from unittest import TestCase


class TestViewStream(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.stream = ViewStream(self.view)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def assertContents(self, text):
        self.assertEqual(
            self.view.substr(sublime.Region(0, self.view.size())),
            text
        )

    def test_stream_operations(self):
        self.stream.write("Hello, ")
        self.stream.print("World!")

        self.stream.seek_start()
        self.stream.print("Top")

        self.stream.seek_end()
        self.stream.print("Bottom")

        self.stream.seek(4)
        self.stream.print("After Top")

        self.assertContents("Top\nAfter Top\nHello, World!\nBottom\n")

    def test_clear(self):
        self.stream.write("Some text")
        self.stream.clear()
        self.assertContents("")
