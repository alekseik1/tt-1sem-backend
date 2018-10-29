import unittest
from app import app
import json


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Hello, world', rv.data)
        self.assertEqual('text/html', rv.mimetype)

    def test_create_chat(self):
        names = ['tt-team', 'ZOG']
        for name in names:
            rv = self.app.post(
                '/create_chat/', data=dict(
                    topic=name,
                    is_group=0
                ))
            data = json.loads(rv.json)[0]
            self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()

