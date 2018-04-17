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
        syntax = get_syntax_metadata("file.sublime-syntax", contents)
        syntax_ref = SyntaxInfo(
            path="file.sublime-syntax",
            name="Test Syntax",
            scope="source.test",
            hidden=True
        )
        self.assertEqual(syntax, syntax_ref)

    def test_single_quoted(self):
        contents = dedent("""\
            name: 'Test''s Syntax'
        """)
        syntax = get_syntax_metadata("file.sublime-syntax", contents)
        syntax_ref = SyntaxInfo(path="file.sublime-syntax", name="Test's Syntax")
        self.assertEqual(syntax, syntax_ref)

    def test_double_quoted(self):
        contents = dedent("""\
            name: "\\" escapes "
        """)
        syntax = get_syntax_metadata("file.sublime-syntax", contents)
        syntax_ref = SyntaxInfo(path="file.sublime-syntax", name='" escapes ')
        self.assertEqual(syntax, syntax_ref)

    def test_quoted_key(self):
        contents = dedent("""\
            'name': Normal Syntax
        """)
        syntax = get_syntax_metadata("file.sublime-syntax", contents)
        syntax_ref = SyntaxInfo(path="file.sublime-syntax", name='Normal Syntax')
        self.assertEqual(syntax, syntax_ref)

    def test_tmlanguage(self):
        contents = dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
                "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>name</key>
                <string>Test Syntax</string>
                <key>scopeName</key>
                <string>source.test</string>
                <key>hidden</key>
                <true/>
            </dict>
        """)
        syntax = get_syntax_metadata("file.tmLanguage", contents)
        syntax_ref = SyntaxInfo(
            path="file.tmLanguage",
            name="Test Syntax",
            scope="source.test",
            hidden=True
        )
        self.assertEqual(syntax, syntax_ref)
