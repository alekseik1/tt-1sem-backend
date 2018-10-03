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

    def test_shift(self):
        for i in range(self.N):
            self.list.unshift(i**2)
        with self.subTest("Посередине"):
            self.assertEqual(self.list.shift(self.N // 2), (self.N // 2)**2)
        with self.subTest("Последний"):
            self.assertEqual(self.list.shift(), (self.N - 1)**2)

    def test_unshift(self):
        for i in range(self.N):
            try:
                self.list.unshift(i)
            except Exception as e:
                self.fail(e)
        self.assertEqual(len(self.list), self.N)
        for i in range(self.N):
            self.assertEqual(self.list[i], self.N - i - 1)

    def test_contains(self):
        for i in range(self.N):
            self.list.append((1-i)**2)
            self.list.unshift(i**2)

        with self.subTest("Python `in` operator"):
            self.assertFalse(2 in self.list)
            self.assertFalse(100500 in self.list)
            self.assertTrue(4 in self.list)
        with self.subTest("Our `contains()` method"):
            self.assertTrue(self.list.contains(4))
            self.assertFalse(self.list.contains(100500))
            self.assertFalse(self.list.contains(2))

