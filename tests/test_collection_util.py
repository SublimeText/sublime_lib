from sublime_lib._util.collections import projection, get_selector
from unittest import TestCase


class TestSettingsDict(TestCase):

    def test_projection(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }

        self.assertEqual(
            projection(d, ()),
            {}
        )

        self.assertEqual(
            projection(d, ('a', 'c')),
            {
                'a': 1,
                'c': 3,
            }
        )

        self.assertEqual(
            projection(d, {
                'a': 'x',
                'b': 'y',
            }),
            {
                'x': 1,
                'y': 2,
            }
        )

    def test_get_selector(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }

        self.assertEqual(
            get_selector('a')(d),
            1
        )

        self.assertEqual(
            get_selector('x')(d),
            None
        )

        self.assertEqual(
            get_selector('x', 42)(d),
            42
        )

        self.assertEqual(
            get_selector(lambda d: d['a'])(d),
            1
        )

        self.assertEqual(
            get_selector(('a',))(d),
            {
                'a': 1,
            }
        )

        self.assertEqual(
            get_selector(('a', 'b'))(d),
            {
                'a': 1,
                'b': 2,
            }
        )

        self.assertEqual(
            get_selector({'a': 'x', 'b': 'y'})(d),
            {
                'x': 1,
                'y': 2,
            }
        )

    def test_get_selector_error(self):
        with self.assertRaises(TypeError):
            get_selector(42)
