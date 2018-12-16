import sublime
import sublime_lib.flags as flags

from unittest import TestCase


class TestFlags(TestCase):

    def _test_enum(self, enum, prefix=''):
        for item in enum:
            self.assertEqual(item, getattr(sublime, prefix + item.name))
            self.assertEqual(item, enum(item.name))

    def test_flags(self):
        self._test_enum(flags.DialogResult, 'DIALOG_')
        self._test_enum(flags.PointClass, 'CLASS_')
        self._test_enum(flags.PhantomLayout, 'LAYOUT_')

        self._test_enum(flags.FindOption)
        self._test_enum(flags.RegionOption)
        self._test_enum(flags.PopupOption)
        self._test_enum(flags.OpenFileOption)
        self._test_enum(flags.QuickPanelOption)

    def test_from_strings(self):
        self.assertEqual(
            flags.RegionOption('DRAW_EMPTY', 'HIDE_ON_MINIMAP'),
            flags.RegionOption.DRAW_EMPTY | flags.RegionOption.HIDE_ON_MINIMAP
        )

    def test_from_strings_empty(self):
        self.assertEqual(
            flags.RegionOption(),
            flags.RegionOption(0)
        )
