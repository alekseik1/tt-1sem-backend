from flask import request, jsonify
from app import app
from app import model, jsonrpc
from flask_jsonrpc.exceptions import InvalidRequestError
import json
from datetime import datetime


@app.route('/')
@app.route('/<string:name>/')
def index(name="world"):
    return "Hello, {}".format(name)


def create_stub_answer(request, status_code):
    response_dict = {
        'status_code': status_code,
        'mimetype': 'text/json',
        'method': request.path
    }
    response = app.response_class(
        response=json.dumps(response_dict),
        status=response_dict.get('status_code', 404),
        mimetype=response_dict.get('mimetype', 'text/json')
    )
    return response


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return """
        <html><head></head><body>
        <form method="POST" action="/form/">
            <input name="first_name" >
            <input name="last_name" >
            <input type="submit" >
        </form>
        </body></html>
        """
    else:
        rv = jsonify(request.form)
        return rv


@jsonrpc.method('get_user_chats')
def get_user_chats(user_id=0, limit=100):
    """
    Чаты пользователя
    """
    return model.get_user_chats(user_id, limit)


@jsonrpc.method('get_user_contacts')
def get_user_contacts(user_id=0):
    """
    Контакты пользователя
    """
    return create_stub_answer(request, 200)


@jsonrpc.method('get_messages_by_chat')
def messages_by_chat(chat_id=0, limit=10, offset=0, from_id=0):
    if not chat_id:
        return {}
    chat_messages = model.list_messages_by_chat(chat_id, limit, offset, from_id=from_id)
    return chat_messages


@jsonrpc.method('find_user')
def find_user(name='%', nick='%', user_id='%'):

    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)

    users = model.find_user(limit, offset, user_name=name, user_nick=nick, user_id=user_id)
    return users


@jsonrpc.method('create_chat')
def create_chat(topic='Bad chat', members=[0], is_group=0):
    chat_id = model.create_chat(topic=str(topic), members=members, is_group=is_group)
    return {
        'topic': topic,
        'is_group_chat': is_group,
        'chat_id': chat_id
    }


@jsonrpc.method('print_name')
def foo():
    return {"name": "Ivan"}


@jsonrpc.method('send_message')
def send_message(chat_id, sender_id, token, message_text, files, geo):
    added_at = str(datetime.now())
    return {'message_id': model.send_message(chat_id, sender_id, message_text, added_at)}


@jsonrpc.method('read_messages')
def read_messages(chat_id, user_id, number_of_messages, last_read_message_id):
    model.read_messages(user_id, chat_id, last_read_message_id, number_of_messages)
