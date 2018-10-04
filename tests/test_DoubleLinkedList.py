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

    def test_first(self):
        for i in range(self.N):
            self.list.append(i**2)
        self.assertEqual(self.list.first().value, 0)

    def test_last(self):
        for i in range(self.N):
            self.list.append(i**2)
        self.assertEqual(self.list.last().value, (self.N-1)**2)

    def test_last_after_push(self):
        self.list.push(2)
        self.assertEqual(self.list[-1], 2)

    def test_first_after_unshift(self):
        self.list.unshift(100500)
        self.assertEqual(self.list[0], 100500)

    def test_iterator(self):
        for i in range(100):
            self.list.append(i)
        for value in self.list:
            self.assertEqual(value, i)


class BadTests(unittest.TestCase):
    """
    Класс с очень плохими тестами
    """

    def setUp(self):
        self.list = DoubleLinkedList()
        self.N = 30

    def test_empty_list_size(self):
        self.assertEqual(len(self.list), 0)

    def test_pop_empty_list(self):
        try:
            self.list.pop()
        except Exception as e:
            self.assertEqual(e.args[0], 'The list is empty!')

    def test_get_incorrect_index(self):
        with self.subTest("Too big index"):
            for i in range(5):
                self.list.append(i)
            with self.assertRaises(IndexError):
                self.list[1000]
        with self.subTest("Empty list"):
            self.list = DoubleLinkedList()
            with self.assertRaises(IndexError):
                self.list[0]

    def test_first_last_empty_list(self):
        self.assertIsNone(self.list.head)
        self.assertIsNone(self.list.tail)

    def test_delete_bad_element(self):
        for i in range(10):
            self.list.push(100)
        with self.assertRaises(IndexError):
            self.list.remove(105)


if __name__ == '__main__':
    # Run only the tests in the specified classes

    test_classes_to_run = [BasicTests, BadTests]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
