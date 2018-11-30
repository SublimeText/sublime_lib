import sublime
import shutil

from sublime_lib import ResourcePath
from sublime_lib.vendor.pathlib.pathlib import Path

from unittesting import DeferrableTestCase


class TestResourcePath(DeferrableTestCase):

    def setUp(self):
        shutil.copytree(
            src=str(ResourcePath("Packages/sublime_lib/tests/test_package").file_path()),
            dst=str(ResourcePath("Packages/test_package").file_path()),
        )

        yield ResourcePath("Packages/test_package/.test_package_exists").exists

    def tearDown(self):
        shutil.rmtree(
            str(ResourcePath("Packages/test_package").file_path()),
            ignore_errors=True
        )

    def test_glob_resources(self):
        self.assertEqual(
            ResourcePath.glob_resources("Packages/test_package/*.txt"),
            [
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
                ResourcePath("Packages/test_package/helloworld.txt"),
            ]
        )

    def test_from_file_path_packages(self):
        self.assertEqual(
            ResourcePath.from_file_path(Path(sublime.packages_path(), 'test_package')),
            ResourcePath("Packages/test_package")
        )

    def test_from_file_path_cache(self):
        self.assertEqual(
            ResourcePath.from_file_path(Path(sublime.cache_path(), 'test_package')),
            ResourcePath("Cache/test_package")
        )

    def test_from_file_path_error(self):
        with self.assertRaises(ValueError):
            ResourcePath.from_file_path(Path('/test_package')),

    def test_from_file_path_relative(self):
        with self.assertRaises(ValueError):
            ResourcePath.from_file_path(Path('test_package')),

    def test_file_path_packages(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").file_path(),
            Path(sublime.packages_path(), 'Foo/bar.py')
        )

    def test_file_path_cache(self):
        self.assertEqual(
            ResourcePath("Cache/Foo/bar.py").file_path(),
            Path(sublime.cache_path(), 'Foo/bar.py')
        )

    def test_file_path_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("Elsewhere/Foo/bar.py").file_path(),

    def test_exists(self):
        self.assertTrue(
            ResourcePath("Packages/test_package/helloworld.txt").exists()
        )

    def test_not_exists(self):
        self.assertFalse(
            ResourcePath("Packages/test_package/nonexistentfile.txt").exists()
        )

    def test_read_text(self):
        self.assertEqual(
            ResourcePath("Packages/test_package/helloworld.txt").read_text(),
            "Hello, World!\n"
        )

    def test_read_text_missing(self):
        with self.assertRaises(FileNotFoundError):
            ResourcePath("Packages/test_package/nonexistentfile.txt").read_text()

    def test_read_text_invalid_unicode(self):
        with self.assertRaises(UnicodeDecodeError):
            ResourcePath("Packages/test_package/UTF-8-test.txt").read_text()

    def test_read_bytes(self):
        self.assertEqual(
            ResourcePath("Packages/test_package/helloworld.txt").read_bytes(),
            b"Hello, World!\n"
        )

    def test_read_bytes_missing(self):
        with self.assertRaises(FileNotFoundError):
            ResourcePath("Packages/test_package/nonexistentfile.txt").read_bytes()

    def test_read_bytes_invalid_unicode(self):
        # Should not raise UnicodeDecodeError
        ResourcePath("Packages/test_package/UTF-8-test.txt").read_bytes()

    def test_glob(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").glob('*.txt'),
            [
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
                ResourcePath("Packages/test_package/helloworld.txt"),
            ]
        )

    def test_rglob(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").rglob('*.txt'),
            [
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
                ResourcePath("Packages/test_package/directory/goodbyeworld.txt"),
                ResourcePath("Packages/test_package/helloworld.txt"),
            ]
        )

    def test_rglob_error(self):
        with self.assertRaises(NotImplementedError):
            ResourcePath("Packages/test_package").rglob('/*.txt')

    def test_children(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").children(),
            [
                ResourcePath("Packages/test_package/.test_package_exists"),
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
                ResourcePath("Packages/test_package/directory"),
                ResourcePath("Packages/test_package/helloworld.txt"),
            ]
        )
