import unittest
from app.double_linked_list import DoubleLinkedList


class BasicTests(unittest.TestCase):

    def test_create(self):
        try:
            l = DoubleLinkedList()
        except Exception as e:
            self.fail(e)
        self.assertNotEqual(l, None)

    def test_append(self):
        l = DoubleLinkedList()
        try:
            l.append(4)
        except Exception as e:
            self.fail(e)

    def test_size(self):
        N = 5
        l = DoubleLinkedList()
        for i in range(N):
            l.append(i)
        self.assertEqual(len(l), N)

    def test_get(self):
        N = 5
        l = DoubleLinkedList()
        for i in range(N):
            l.append(i)
        for i in range(N):
            self.assertEqual(l[i], i)
