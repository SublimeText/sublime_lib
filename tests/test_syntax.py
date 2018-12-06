from sublime_lib import list_syntaxes
from sublime_lib import get_syntax_for_scope
from sublime_lib.syntax import get_yaml_metadata
from sublime_lib.syntax import get_xml_metadata
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
        self.assertEqual(
            SyntaxInfo(path="a file"),
            SyntaxInfo("a file", None, None, False)
        )

    def test_unquoted(self):
        contents = dedent("""\
            name: Test Syntax
            scope: source.test
            hidden: true
        """)
        syntax = get_yaml_metadata(contents)
        self.assertEqual(syntax, {
            'name': "Test Syntax",
            'scope': "source.test",
            'hidden': True,
        })

    def test_single_quoted(self):
        contents = dedent("""\
            name: 'Test''s Syntax'
        """)
        syntax = get_yaml_metadata(contents)
        self.assertEqual(syntax, {
            'name': "Test's Syntax",
        })

    def test_double_quoted(self):
        contents = dedent("""\
            name: "\\" escapes "
        """)
        syntax = get_yaml_metadata(contents)
        self.assertEqual(syntax, {
            'name': '" escapes ',
        })

    def test_quoted_key(self):
        contents = dedent("""\
            'name': Normal Syntax
        """)
        syntax = get_yaml_metadata(contents)
        self.assertEqual(syntax, {
            'name': 'Normal Syntax',
        })

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
            </plist>
        """)
        syntax = get_xml_metadata(contents.encode('utf-8'))
        self.assertEqual(syntax, {
            'name': "Test Syntax",
            'scope': "source.test",
            'hidden': True,
        })
