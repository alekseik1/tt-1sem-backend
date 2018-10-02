import unittest
from app.double_linked_list import DoubleLinkedList


class BasicTests(unittest.TestCase):

    def test_create(self):
        try:
            l = DoubleLinkedList()
        except Exception as e:
            self.fail(e)
        self.assertNotEqual(l, None)

    def test_append_right(self):
        l = DoubleLinkedList()
        try:
            l.appned_right(4)
        except Exception as e:
            self.fail(e)

    def test_append_left(self):
        l = DoubleLinkedList()
        try:
            l.append_left("asd")
        except Exception as e:
            self.fail(e)

    def test_get_size(self):
        N = 5
        with self.subTest("To right border"):
            l = DoubleLinkedList()
            for i in range(N):
                l.append_right(i)
            self.assertEqual(l.size() == N)
        with self.subTest("To left border"):
            l = DoubleLinkedList()
            for i in range(N):
                l.append_left(i)
            self.assertEqual(l.size() == N)
