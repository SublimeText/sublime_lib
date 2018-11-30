from sublime_lib.encodings import from_sublime, to_sublime

from unittest import TestCase


class TestPureResourcePath(TestCase):

    def test_from(self):
        self.assertEqual(
            from_sublime("Western (Windows 1252)"),
            "cp1252"
        )

    def test_to(self):
        self.assertEqual(
            to_sublime("cp1252"),
            "Western (Windows 1252)"
        )
