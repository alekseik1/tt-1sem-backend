import unittest
from app.double_linked_list import DoubleLinkedList


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.list = DoubleLinkedList()
        self.N = 10

    def test_append(self):
        try:
            self.list.append(4)
        except Exception as e:
            self.fail(e)

    def test_size(self):
        for i in range(self.N):
            self.list.append(i)
        self.assertEqual(len(self.list), self.N)

    def test_get(self):
        for i in range(self.N):
            self.list.append(i)
        for i in range(self.N):
            self.assertEqual(self.list[i], i)

    def test_pop(self):
        for i in range(self.N):
            self.list.append(i**2)
        with self.subTest("Посередине"):
            self.assertEqual(self.list.pop(self.N // 2), (self.N // 2)**2)
        with self.subTest("Последний"):
            self.assertEqual(self.list.pop(), (self.N-1)**2)
