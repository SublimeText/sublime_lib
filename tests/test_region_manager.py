import sublime
from sublime import Region
from sublime_lib import RegionManager, new_view, close_view

from unittest import TestCase


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
