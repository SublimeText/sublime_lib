import sublime
from sublime_lib import ViewStream

from unittest import TestCase
from io import UnsupportedOperation


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
        self.assertEqual(self.stream.tell(), 14)

        self.stream.seek_start()
        self.assertEqual(self.stream.tell(), 0)
        self.stream.print("Top")

        self.stream.seek_end()
        self.assertEqual(self.stream.tell(), 18)
        self.stream.print("Bottom")

        self.stream.seek(4)
        self.stream.print("After Top")

        self.assertContents("Top\nAfter Top\nHello, World!\nBottom\n")

    def test_clear(self):
        self.stream.write("Some text")
        self.stream.clear()
        self.assertContents("")

    def test_read(self):
        self.stream.write("Hello, World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.read(5)
        self.assertEqual(text, "World")
        self.assertEqual(self.stream.tell(), 12)

        text = self.stream.read(3)
        self.assertEqual(text, "!\nG")
        self.assertEqual(self.stream.tell(), 15)

        text = self.stream.read(1000)
        self.assertEqual(text, "oodbye, World!")
        self.assertEqual(self.stream.tell(), self.stream.view.size())

        self.stream.seek(7)
        text = self.stream.read(None)
        self.assertEqual(text, "World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.read(-1)
        self.assertEqual(text, "World!\nGoodbye, World!")

    def test_readline(self):
        self.stream.write("Hello, World!\nGoodbye, World!")

        self.stream.seek(7)
        text = self.stream.readline()
        self.assertEqual(text, "World!\n")
        self.assertEqual(self.stream.tell(), 14)

        text = self.stream.readline()
        self.assertEqual(text, "Goodbye, World!")

        self.stream.seek(7)
        text = self.stream.readline(1000)
        self.assertEqual(text, "World!\n")
        self.assertEqual(self.stream.tell(), 14)

        self.stream.seek(7)
        text = self.stream.readline(-1)
        self.assertEqual(text, "World!\n")
        self.assertEqual(self.stream.tell(), 14)

        self.stream.seek(7)
        text = self.stream.readline(5)
        self.assertEqual(text, "World")
        self.assertEqual(self.stream.tell(), 12)

    def test_write_only(self):
        self.stream.view.set_read_only(True)

        self.assertRaises(ValueError, self.stream.write, 'foo')

        self.stream.force_writes = True
        self.assertEqual(self.stream.write('foo'), 3)

    def test_unsupported(self):
        self.assertRaises(UnsupportedOperation, self.stream.detach)
