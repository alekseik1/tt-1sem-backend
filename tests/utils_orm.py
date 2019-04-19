from app.model import User, Message, Member, Chat
from app import db
import random

USER_IDS = range(1, 50)
CHAT_IDS = range(1, 50)


def fill_users():
    users = [User(nick='test_user_{}'.format(user_id),
                  name='tester_{}'.format(user_id),
                  avatar='REKLAMA') for user_id in USER_IDS]
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


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def compare_json(json1, json2):
    return ordered(json1) == ordered(json2)
