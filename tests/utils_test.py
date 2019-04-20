import unittest
from tests.utils_orm import compare_json, damerau_levenshtein_distance


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
                    self.assertTrue(compare_json(json1, json2))
        with self.subTest('Unequal JSONS'):
            for (json1, json2) in unequal_pairs:
                    self.assertFalse(compare_json(json1, json2))

    def test_damerau_levenstein_distance(self):

        with self.subTest('Equal strings'):
            s1, s2 = 'Hello', 'Hello'
            self.assertEqual(0, damerau_levenshtein_distance(s1, s2))

        with self.subTest('One letter'):
            s1, s2 = 'Hello', 'Hell'
            self.assertEqual(1, damerau_levenshtein_distance(s1, s2))

        with self.subTest('Maximum distance'):
            s1, s2 = 'qwdd', 'back'
            self.assertEqual(4, damerau_levenshtein_distance(s1, s2))


if __name__ == '__main__':
    unittest.main()
