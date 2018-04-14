from sublime_lib.syntax import list_syntaxes
from sublime_lib.syntax import get_syntax_for_scope
from sublime_lib.syntax import get_syntax_metadata
from sublime_lib.syntax import SyntaxInfo

from unittest import TestCase
from textwrap import dedent


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
        self.assertEqual(SyntaxInfo(path="a file"),
                         SyntaxInfo("a file", None, None, False))

    def test_unquoted(self):
        contents = dedent("""\
            name: Test Syntax
            scope: source.test
            hidden: true
        """)
        syntax = get_syntax_metadata("file", contents)
        syntax_ref = SyntaxInfo(path="file", name="Test Syntax", scope="source.test", hidden=True)
        self.assertEqual(syntax, syntax_ref)

    def test_single_quoted(self):
        contents = dedent("""\
            name: 'Test''s Syntax'
        """)
        syntax = get_syntax_metadata("file", contents)
        syntax_ref = SyntaxInfo(path="file", name="Test's Syntax")
        self.assertEqual(syntax, syntax_ref)

    def test_double_quoted(self):
        contents = dedent("""\
            name: "\\" escapes "
        """)
        syntax = get_syntax_metadata("file", contents)
        syntax_ref = SyntaxInfo(path="file", name='" escapes ')
        self.assertEqual(syntax, syntax_ref)
