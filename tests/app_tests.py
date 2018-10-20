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

    def test_form(self):
        rv = self.app.post('/form/', data={'first_name': 'Jesse',
                                           'last_name': 'Pinkman'})

    def tearDown(self):
        pass

    def stub_check(self, method_name, user, http_method):
        rv = self.app.open('/%s/%s' % (method_name, user), method=http_method)
        # Ожидаемый ответ + закодируем его в кодировку, продиктованную сервером
        expected_answer = json.dumps({
            'status_code': 200,
            'mimetype': 'text/json',
            'method': '/%s/%s' % (method_name, user)
        }).encode(rv.charset)

        self.assertEqual(rv.status_code, 200)
        self.assertEqual('text/json', rv.mimetype)
        self.assertEqual(expected_answer, rv.data)

    def test_get_user_chats(self):
        users = ['aleksei', 'mailru', 'bigboss']
        for user in users:
            self.stub_check('get_user_chats', user, 'GET')

    def test_get_user_chats_with_POST(self):
        users = ['aleksei', 'bigboss']
        for user in users:
            rv = self.app.open('/get_user_chats/%s' % user,
                              method='POST')
            self.assertEqual(rv.status_code, 405)   # Method not allowed

    def test_get_user_contacts(self):
        users = ['aleksei', 'bigboss']
        for user in users:
            self.stub_check('get_user_contacts', user, 'GET')

    def test_get_user_contacts_with_POST(self):
        users = ['aleksei', 'bigboss']
        for user in users:
            rv = self.app.open('/get_user_contacts/%s' % user,
                          method='POST')
            self.assertEqual(rv.status_code, 405)

    def test_create_chat(self):
        names = ['tt-team', 'ZOG']
        for name in names:
            self.stub_check('create_chat', name, 'POST')

    def test_create_chat_with_GET(self):
        names = ['tt-team', 'ZOG']
        for name in names:
            rv = self.app.open('/create_chat/%s' % name, method='GET')
            self.assertEqual(rv.status_code, 405)


if __name__ == '__main__':
    unittest.main()

