from sublime_lib.resource_path import ResourcePath

from unittesting import DeferrableTestCase

import shutil


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
        self.assertRaises(
            FileNotFoundError,
            ResourcePath("Packages/test_package/nonexistentfile.txt").read_text
        )

    def test_read_bytes(self):
        self.assertEqual(
            ResourcePath("Packages/test_package/helloworld.txt").read_bytes(),
            b"Hello, World!\n"
        )

    def test_read_bytes_missing(self):
        self.assertRaises(
            FileNotFoundError,
            ResourcePath("Packages/test_package/nonexistentfile.txt").read_bytes
        )

    def test_glob(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").glob('*.txt'),
            [
                ResourcePath("Packages/test_package/helloworld.txt"),
            ]
        )

    def test_rglob(self):
        self.assertEqual(
            set(ResourcePath("Packages/test_package").rglob('*.txt')),
            {
                ResourcePath("Packages/test_package/directory/goodbyeworld.txt"),
                ResourcePath("Packages/test_package/helloworld.txt"),
            }
        )

    def test_children(self):
        self.assertEqual(
            set(ResourcePath("Packages/test_package").children()),
            {
                ResourcePath("Packages/test_package/directory"),
                ResourcePath("Packages/test_package/helloworld.txt"),
                ResourcePath("Packages/test_package/.test_package_exists"),
            }
        )
