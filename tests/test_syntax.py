import sublime

from sublime_lib.syntax import list_syntaxes
from sublime_lib.syntax import get_syntax_for_scope

from unittest import TestCase
from io import UnsupportedOperation


class TestSyntax(TestCase):

    def test_list_syntaxes(self):
        syntaxes = list_syntaxes()
        self.assertTrue(syntaxes)

    def test_get_syntax(self):
        self.assertEqual(
            get_syntax_for_scope('source.python'),
            'Packages/Python/Python.sublime-syntax'
        )
