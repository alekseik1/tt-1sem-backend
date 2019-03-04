import unittest
from tests.utils import equals_json


class UtilsTest(unittest.TestCase):

    def test_compare_json(self):
        equalJSONS = [
            {'a': 1, 'b': 2, 'c': [1, 2]},
            {'a': 1, 'b': 2, 'c': [2, 1]}
        ]
        unequal_pairs = [
            ({'a': 1, 'b': 2, 'c': [1, 2]}, {'a': 1, 'b': 2, 'c': [3, 1]}),
            ({'a': 1, 'b': 2, 'c': [1, 2]}, {'a': 1, 'b': 2, 'c': [2, 2]})
        ]

        with self.subTest('Equal JSONS'):
            for i, json1 in enumerate(equalJSONS):
                for j, json2 in enumerate(equalJSONS[i:]):
                    self.assertTrue(equals_json(json1, json2))
        with self.subTest('Unequal JSONS'):
            for (json1, json2) in unequal_pairs:
                    self.assertFalse(equals_json(json1, json2))


if __name__ == '__main__':
    unittest.main()
