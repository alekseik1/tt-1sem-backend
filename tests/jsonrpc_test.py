import unittest
from app import app, jsonify
from flask_jsonrpc.proxy import ServiceProxy

# Меняйте их от теста к тесту, я лучше пока не придумал
user_id = 2
chat_id = 143


class JsonrpcTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_send_message(self):
        request_json = {'method': 'send_message', 'params': {
                'chat_id': chat_id, 'user_id': user_id, 'content': 'TestMessage'
            }, 'id': 1}
        a = self.app.post('/api/', json=request_json)
        self.assertNotEqual(a, None)

    def test_get_messages_by_chat(self):
        request_json = {'method': 'get_messages_by_chat', 'params': {
            'chat_id': chat_id
        }, 'id': 2}
        a = self.app.post('/api/', json=request_json)
        self.assertNotEqual(a, None)
        self.assertIsNotNone(a.json.get('result'))
        self.assertEqual(a.json['id'], 2, 'Id не совпадают')


if __name__ == '__main__':
    unittest.main()
