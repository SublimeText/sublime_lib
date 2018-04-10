import sublime
from sublime_lib import OutputPanel

from sublime_lib.testing import ViewTestCase

class TestOutputPanel(ViewTestCase):

    def setUp(self):
        self.window = sublime.active_window()
        self.panel = OutputPanel(self.window, "test_panel")
        self.view = self.panel.view
        self.panel.show()

    def tearDown(self):
        self.panel.destroy()


    def test_stream_operations(self):
        self.panel.write("Hello, ")
        self.panel.print("World!")
        
        self.panel.seek_start()
        self.panel.print("Top")

        self.panel.seek_end()
        self.panel.print("Bottom")

        self.panel.seek(4)
        self.panel.print("After Top")

        self.assertContents("Top\nAfter Top\nHello, World!\nBottom\n")

    def test_clear(self):
        self.panel.write("Some text")
        self.panel.clear()
        self.assertContents("")

    def test_show_hide(self):
        self.panel.show()

        self.assertEqual(self.window.active_panel(), self.panel.full_name)

        self.panel.hide()

        self.assertNotEqual(self.window.active_panel(), self.panel.full_name)

    def test_exists(self):
        self.assertIsNotNone(self.window.find_output_panel(self.panel.name))

    def test_destroy(self):
        self.panel.destroy()
        self.assertIsNone(self.window.find_output_panel(self.panel.name))
