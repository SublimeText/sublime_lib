from sublime_lib import list_syntaxes
from sublime_lib import get_syntax_for_scope
from sublime_lib.syntax import get_yaml_metadata
from sublime_lib.syntax import get_xml_metadata
from sublime_lib.syntax import SyntaxInfo

from sublime_lib import ResourcePath

from unittest import TestCase
from textwrap import dedent


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

    def test_sublime_syntax(self):
        syntax = get_yaml_metadata((TEST_SYNTAXES_PATH / 'sublime_lib_test.sublime-syntax').read_text())
        self.assertEqual(syntax, {
            'hidden': True,
            'name': "sublime_lib test syntax (sublime-syntax)",
            'scope': "source.sublime_lib_test",
        })

    def test_tmlanguage(self):
        syntax = get_xml_metadata((TEST_SYNTAXES_PATH / 'sublime_lib_test_2.tmLanguage').read_bytes())
        self.assertEqual(syntax, {
            'hidden': True,
            'name': "sublime_lib test syntax 2 (tmLanguage)",
            'scope': "source.sublime_lib_test_2",
        })
