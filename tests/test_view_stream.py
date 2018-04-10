import sublime
from sublime_lib import ViewStream

from sublime_lib.testing import ViewTestCase

class TestViewStream(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.stream = ViewStream(self.view)

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
