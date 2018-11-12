import unittest
from app import app, jsonify
from flask_jsonrpc.proxy import ServiceProxy


class JsonrpcTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_send_message(self):
        request_json = {'method': 'send_message', 'params': {
                'chat_id': 113, 'user_id': 2, 'content': 'TestMessage'
            }, 'id': 1}
        a = self.app.post('/api/', json=request_json)
        self.assertNotEqual(a, None)


if __name__ == '__main__':
    unittest.main()
