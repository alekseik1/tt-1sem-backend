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
                '/create_chat/?topic=%s&is_group=0' % name)
            data = rv.json
            self.assertEqual(data.get('topic', None), name)

    def test_list_messages_by_chat(self):
        rv = self.app.get('/messages/?chat_id={}'
                          .format(23))  # TODO: сделать тесты через chat_topic
        data = rv.json
        self.assertIsNotNone(data)

    def test_find_user(self):
        rv = self.app.get('/find_user/?nick=%s' % 'another.user')
        data = rv.json
        self.assertNotEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()

