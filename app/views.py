from flask import request, jsonify
from app import app
from app import model, jsonrpc
from flask_jsonrpc.exceptions import InvalidRequestError
from app import db
from app.model import *
from sqlalchemy.sql.expression import any_
import json
from flask import abort
from datetime import datetime
from app.forms import *


@jsonrpc.method('get_user_chats')
def get_user_chats(user_id=0, limit=100):
    """
    Чаты пользователя
    """
    if limit < 0:
        raise ValueError('Limit should be positive, not %s' % limit)
    chats = [chat.as_dict() for chat in
             db.session.query(Chat).filter(User.id == user_id)]
    if len(chats) == 0:
        abort(404)
    return chats


def validate_user(user):
    return UserForm(None, user).validate()


@jsonrpc.method('get_messages_by_chat')
def get_chat_messages(chat_id, limit=10, offset=0):
    return [message.as_dict() for message in
            db.session.query(Message).filter(Chat.id == chat_id).limit(limit).offset(offset)]


@jsonrpc.method('create_chat')
def create_chat(topic, members_id, is_group):
    # Создадим чат
    new_chat = Chat(is_group=is_group, topic=topic)
    members = db.session.query(User).filter(User.id.in_(members_id)).all()
    new_chat.users = members
    db.session.add(new_chat)
    db.session.commit()
    return db.session.query(User).all()


@jsonrpc.method('leave_chat')
def leave_chat(chat_id, user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    chat = next((x for x in user.chats if x.id == chat_id), None)
    if chat is None:
        raise ValueError("User {} is not in chat {}".format(user_id, chat_id))
    user.chats.remove(chat)
    db.session.commit()


@jsonrpc.method('delete_chat')
def delete_chat(chat_id, remove_users=False):
    chat = db.session.query(Chat).filter(Chat.id == chat_id).first_or_404()
    members = db.session.query(Member).filter(Chat.id == chat.id).all()
    if len(chat.users) != 0 and not remove_users:
        raise ValueError('Chat is not empty! To force remove, pass `remove_users=True`')
    # Выкинем всех пользователей из чата
    elif len(chat.users) != 0:
        chat.users = []
        db.session.commit()
    db.session.delete(chat)
    db.session.commit()


@jsonrpc.method('join_chat')
def join_chat(user_id, chat_id):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    chat = db.session.query(Chat).filter(Chat.id == chat_id).first_or_404()
    if chat in user.chats:
        raise ValueError('User {} is already in chat {}'.format(user_id, chat_id))
    user.chats.append(chat)
    db.session.commit()


@jsonrpc.method('send_message')
def send_message(sender_id, chat_id, content):
    if len(content) > MAX_MESSAGE_SIZE:
        raise ValueError('Message text max length is {}'.format(MAX_MESSAGE_SIZE))
    chat = db.session.query(Chat).filter(Chat.id == chat_id).first_or_404()
    user = db.session.query(User).filter(User.id == sender_id).first_or_404()
    message = Message(chat=chat, user=user, content=content)
    chat.messages.append(message)
    db.session.commit()
    return message.id


@jsonrpc.method('find_user')
def find_user(nick=None, name=None):
    if nick is None and name is None:
        return json.dumps([])
    if nick is not None:
        users = [user.as_dict() for user in
                 db.session.query(User).filter(User.nick.like(nick + '%')).all()]
        return json.dumps(users)
    if name is not None:
        users = [user.as_dict() for user in
                 db.session.query(User).filter(User.name.like(name + '%')).all()]
        return json.dumps(users)


@jsonrpc.method('get_user_info')
def get_user_info(user_id):
    user_id = int(user_id)
    return json.dumps(
        db.session.query(User).filter(User.id == user_id).first_or_404().as_dict()
    )



# -------------------------------------------------------------------------

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

@jsonrpc.method('get_user_contacts')
def get_user_contacts(user_id=0):
    """
    Контакты пользователя
    """
    return create_stub_answer(request, 200)


@jsonrpc.method('read_messages')
def read_messages(chat_id, user_id, number_of_messages, last_read_message_id):
    model.read_messages(user_id, chat_id, last_read_message_id, number_of_messages)
