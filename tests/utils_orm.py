from app.model import User, Message, Member, Chat
from app import db
import random

USER_IDS = range(2, 10)
CHAT_IDS = range(2, 10)
MATRIX = [[2, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 8], [7, 9], [9, 8]]

users = [User(nick='test_user_{}'.format(user_id),
              name='tester_{}'.format(user_id),
              avatar='REKLAMA') for user_id in USER_IDS]
chats = [Chat(is_group=0, topic='Gen chat_{}'.format(chat_id)) for chat_id in CHAT_IDS]
messages = []


def fill_users():
    db.session.add_all(users)
    db.session.commit()


def fill_chats():
    db.session.add_all(chats)
    db.session.commit()


def fill_members():
    i = 0
    for user in users:
        user.chats = chats[i:i+3]
        i = (i+3) if (i+3) < len(chats) else 0
    db.session.commit()


def fill_messages():
    global messages
    messages = [Message(chat=chat, user=chat.users[0], content='Test message') for chat in chats]
    db.session.add_all(messages)
    db.session.commit()


def fill_all():
    fill_users()
    fill_chats()
    fill_members()
    fill_messages()
    db.session.commit()
