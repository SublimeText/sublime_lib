from sublime_lib._util.weak_method import weak_method

from unittest import TestCase


class TestWeakMethod(TestCase):

    def test_weak(self):
        count = 0

        class TestObject:
            def foo(self):
                nonlocal count
                count += 1

        obj = TestObject()

        obj.foo()
        self.assertEqual(count, 1)

        weak = weak_method(obj.foo)

        weak()
        self.assertEqual(count, 2)

        del obj

        weak()
        self.assertEqual(count, 2)
