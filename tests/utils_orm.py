from app.model import User, Message, Member, Chat
from app import db
import random

USER_IDS = range(1, 50)
CHAT_IDS = range(1, 50)


def fill_users():
    users = [User(nick='test_user_{}'.format(user_id),
                  name='tester_{}'.format(user_id),
                  avatar='REKLAMA') for user_id in USER_IDS]
    # Первому и последнему пользователю дадим мой email
    MY_EMAIL = '1alekseik1@gmail.com'
    # Где-то в тестах используется users[0], где-то users[-1], поэтому дадим email обоим
    users[0].email, users[-1].email = MY_EMAIL, MY_EMAIL
    db.session.add_all(users)
    db.session.commit()
    return users


def fill_chats():
    chats = [Chat(is_group=0, topic='Gen chat_{}'.format(chat_id)) for chat_id in CHAT_IDS]
    db.session.add_all(chats)
    db.session.commit()
    return chats


def fill_members(users, chats):
    i = 0
    for user in users:
        user.chats = chats[i:i+3]
        i = (i+3) if (i+3) < len(chats) else 0
    db.session.commit()


def fill_messages(chats):
    messages = [Message(chat=chat, user=chat.users[0], content='Test message') for chat in chats]
    db.session.add_all(messages)
    db.session.commit()
    return messages


def fill_all():
    users = fill_users()
    chats = fill_chats()
    fill_members(users, chats)
    messages = fill_messages(chats)
    return users, chats, messages
