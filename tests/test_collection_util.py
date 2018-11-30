from sublime_lib._util.collection_util import projection, isiterable, ismapping, is_sequence_not_str

from unittest import TestCase


class TestSettingsDict(TestCase):

    def test_projection(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }

        self.assertEquals(
            projection(d, ()),
            {}
        )

        self.assertEquals(
            projection(d, ('a', 'c')),
            {
                'a': 1,
                'c': 3,
            }
        )

        self.assertEquals(
            projection(d, {
                'a': 'x',
                'b': 'y',
            }),
            {
                'x': 1,
                'y': 2,
            }
        )

    def test_isiterable(self):
        def generator():
            yield

        self.assertTrue(isiterable(''))
        self.assertTrue(isiterable(()))
        self.assertTrue(isiterable([]))
        self.assertTrue(isiterable(generator()))

        self.assertFalse(isiterable(None))
        self.assertFalse(isiterable(42))
        self.assertFalse(isiterable(object()))

    def test_ismapping(self):
        self.assertTrue(ismapping({}))
        self.assertFalse(ismapping([]))

    def test_is_sequence_not_str(self):
        self.assertTrue(is_sequence_not_str(()))
        self.assertTrue(is_sequence_not_str([]))

        self.assertFalse(is_sequence_not_str({}))
        self.assertFalse(is_sequence_not_str(''))
