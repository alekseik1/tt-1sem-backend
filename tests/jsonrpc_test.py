import unittest
from app import app, jsonify
from flask_jsonrpc.proxy import ServiceProxy
from tests.OLD_SQL_utils import equals_json

# Меняйте их от теста к тесту, я лучше пока не придумал
user_id = 2
user1_id = 3
chat_id = 4


class JsonrpcTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_create_chat(self):
        CHAT_NAME = 'BigChat'
        MEMBERS = [0, 1]
        request_json = {'method': 'create_chat', 'params': {
            'topic': CHAT_NAME,
            'members': MEMBERS,
            'is_group': 0
        }, 'id': 1}
        a = self.app.post('/api/', json=request_json)
        self.assertIsNotNone(a)
        self.assertTrue(equals_json(a,
                                    {'topic': CHAT_NAME,
                                     'chat_id': 123,
                                     'is_group_chat': 0}))

    def test_send_message(self):
        request_json = {'method': 'send_message', 'params': {
                'chat_id': chat_id, 'sender_id': user_id, 'message_text': 'TestMessage',
                'token': '123123', 'files': None, 'geo': None,
            }, 'id': 1}
        a = self.app.post('/api/', json=request_json)
        self.assertNotEqual(a, None)
        self.assertIsNotNone(a.json.get('result').get('message_id'))

    def test_get_messages_by_chat(self):
        request_json = {'method': 'get_messages_by_chat', 'params': {
            'chat_id': chat_id
        }, 'id': 2}
        a = self.app.post('/api/', json=request_json)
        self.assertNotEqual(a, None)
        self.assertIsNotNone(a.json.get('result'))
        print(a.json.get('result'))
        self.assertEqual(a.json['id'], 2, 'Id не совпадают')

    def test_read_messages(self):

        request_json = {'method': 'read_messages', 'params': {
            'user_id': user1_id,
            'chat_id': chat_id,
            'last_read_message_id': 10,
            'number_of_messages': 2
        }, 'id': 3}
        a = self.app.post('/api/', json=request_json)
        self.assertIsNotNone(a)
        print(a.json.get('result'))

    def test_get_user_chats(self):
        request_json = {'method': 'get_user_chats', 'params': {
            'user_id': user1_id,
            'limit': 100
        }, 'id': 5}
        a = self.app.post('/api/', json=request_json)
        print(a.json.get('result'))


if __name__ == '__main__':
    unittest.main()
