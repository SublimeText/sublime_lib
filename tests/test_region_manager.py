import sublime
from sublime import Region
from sublime_lib import RegionManager, new_view, close_view

from unittest import TestCase
from unittest.mock import NonCallableMagicMock, MagicMock

from inspect import signature


class ViewMock(NonCallableMagicMock):
    def __init__(self):
        super().__init__()

        self.add_regions = MagicMock(spec=sublime.View.add_regions)


class TestRegionManager(TestCase):
    def setUp(self):
        self.window = sublime.active_window()

    def tearDown(self):
        if getattr(self, 'view', None):
            try:
                close_view(self.view, force=True)
            except ValueError:
                pass

    def test_set(self):
        self.view = new_view(self.window, scratch=True, content='Hello, World!')
        manager = RegionManager(self.view)

        manager.set([Region(0, 5)])

        self.assertEqual(
            manager.get(),
            [Region(0, 5)]
        )

        self.assertEqual(
            self.view.get_regions(manager.key),
            [Region(0, 5)]
        )

        manager.set([Region(7, 13)])

        self.assertEqual(
            manager.get(),
            [Region(7, 13)]
        )

        self.assertEqual(
            self.view.get_regions(manager.key),
            [Region(7, 13)]
        )

        manager.erase()

        self.assertEqual(
            manager.get(),
            []
        )

        self.assertEqual(
            self.view.get_regions(manager.key),
            []
        )

    def test_del(self):
        self.view = new_view(self.window, scratch=True, content='Hello, World!')
        manager = RegionManager(self.view)

        manager.set([Region(0, 5)])

        self.assertEqual(
            manager.get(),
            [Region(0, 5)]
        )

        self.assertEqual(
            self.view.get_regions(manager.key),
            [Region(0, 5)]
        )

        key = manager.key
        del manager

        self.assertEqual(
            self.view.get_regions(key),
            []
        )

    def test_key(self):
        self.view = new_view(self.window, scratch=True, content='Hello, World!')
        key = 'TestRegionManager'
        manager = RegionManager(self.view, key)

        manager.set([Region(0, 5)])

        self.assertEqual(
            manager.get(),
            [Region(0, 5)]
        )

        self.assertEqual(
            self.view.get_regions(key),
            [Region(0, 5)]
        )

    def test_no_default_args(self):
        view = ViewMock()
        manager = RegionManager(view)

        regions = [Region(0, 5)]
        manager.set(regions)

        view.add_regions.assert_called_once_with(
            manager.key,
            regions,
            '',
            '',
            0
        )

    def test_args(self):
        view = ViewMock()
        manager = RegionManager(
            view,
            scope='region.reddish',
            icon='dot',
            flags=sublime.DRAW_EMPTY,
        )

        regions = [Region(0, 5)]
        manager.set(regions)

        view.add_regions.assert_called_once_with(
            manager.key,
            regions,
            'region.reddish',
            'dot',
            sublime.DRAW_EMPTY
        )
        view.add_regions.reset_mock()

        manager.set(
            regions,
            scope='region.bluish',
            icon='circle',
            flags=sublime.HIDE_ON_MINIMAP
        )

        view.add_regions.assert_called_once_with(
            manager.key,
            regions,
            'region.bluish',
            'circle',
            sublime.HIDE_ON_MINIMAP
        )
