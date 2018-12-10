from sublime_lib import list_syntaxes
from sublime_lib import get_syntax_for_scope
from sublime_lib.syntax import get_syntax_metadata
from sublime_lib.syntax import SyntaxInfo

from sublime_lib import ResourcePath

from unittest import TestCase


TEST_SYNTAXES_PATH = ResourcePath('Packages/sublime_lib/tests/syntax_test_package')


class TestSyntax(TestCase):

    def test_list_syntaxes(self):
        syntaxes = list_syntaxes()
        self.assertTrue(syntaxes)

    def test_get_syntax(self):
        self.assertEqual(
            get_syntax_for_scope('source.python'),
            'Packages/Python/Python.sublime-syntax'
        )


class TestGetMetadata(TestCase):

    def test_defaults(self):
        self.assertEqual(
            SyntaxInfo(path="a file"),
            SyntaxInfo("a file", None, None, False)
        )

    def test_sublime_syntax(self):
        path = TEST_SYNTAXES_PATH / 'sublime_lib_test.sublime-syntax'
        self.assertEqual(
            get_syntax_metadata(path),
            SyntaxInfo(
                path=str(path),
                name="sublime_lib test syntax (sublime-syntax)",
                hidden=True,
                scope="source.sublime_lib_test",
            )
        )

    def test_tmlanguage(self):
        path = TEST_SYNTAXES_PATH / 'sublime_lib_test_2.tmLanguage'
        self.assertEqual(
            get_syntax_metadata(path),
            SyntaxInfo(
                path=str(path),
                name="sublime_lib test syntax 2 (tmLanguage)",
                hidden=True,
                scope="source.sublime_lib_test_2",
            )
        )
