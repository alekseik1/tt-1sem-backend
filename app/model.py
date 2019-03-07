from app import db
from sqlalchemy import func
from werkzeug.contrib.cache import MemcachedCache
import sys

cache = MemcachedCache(['127.0.0.1:11211'])


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_group_chat = db.Column(db.Integer)
    topic = db.Column(db.String(1000), nullable=False)
    added_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now())


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(32), nullable=False, unique=True)
    name = db.Column(db.String(32), nullable=False)
    avatar = db.Column(db.String, nullable=False)


def list_messages_by_chat(chat_id, limit, offset=0, from_id=0):
    tmp_res = db.query_all("""
        SELECT user_id, nick, name,
               message_id, content, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        AND message_id > %(from_id)s
        ORDER BY added_at DESC
        OFFSET %(offset)s ROWS
        LIMIT %(limit)s
""", chat_id=int(chat_id), limit=int(limit), from_id=from_id, offset=int(offset))
    return tmp_res


def find_user(limit: int=100, offset: int=0, **kwargs):
    user_name, user_nick, user_id = kwargs.get('user_name'), kwargs.get('user_nick'), kwargs.get('user_id')
    # TODO: возможно, преобразование к TEXT будет замедлять БД в будущем
    db_result = db.query_all("""
    SELECT user_id, nick, name, avatar
    FROM users
    WHERE name LIKE %(user_name)s
    AND nick LIKE %(nick)s
    AND CAST(user_id AS TEXT) LIKE %(user_id)s
    LIMIT %(limit)s
    """, user_name=str(user_name), nick=str(user_nick), limit=limit, user_id=str(user_id))
    print(db_result)
    if offset >= len(db_result):
        return []
    return db_result[offset:]


def create_chat(topic: str,
                members: list,
                is_group: int=0):
    # Создадим чат
    chat_id = db.insert_one("""
        INSERT INTO chats (is_group_chat, topic)
        VALUES ( %(is_group)s , %(topic)s )
        RETURNING chat_id;
        """, is_group=str(is_group), topic=str(topic))
    # Каждого из участников добавим в этот чат
    for member in members:
        db.query_one("""
        INSERT INTO members (user_id, chat_id, new_messages)
        VALUES ( %(member)s, %(chat_id)s, 0)
        RETURNING user_id
        """, member=member, chat_id=chat_id)
        # Обнулим кэш
        cache.delete('user_chats_{}'.format(member))
    return chat_id


def get_user_chats(user_id, limit):
    chats = cache.get('user_chats_{}'.format(user_id))
    if chats is None:
        chats = db.query_all("""
        SELECT chats.chat_id, chats.topic
        FROM chats
        JOIN members m on chats.chat_id = m.chat_id
        WHERE m.user_id = %(user_id)s
        LIMIT %(limit)s
        """, user_id=user_id, limit=limit)
        cache.set('user_chats_{}'.format(user_id), chats, timeout=10*60)
        print('NO CACHE!', file=sys.stdout)
    # Возвращаем [] из ID чатов
    print('chats are:', chats, file=sys.stdout)
    return chats


def read_messages(user_id: int,
                  chat_id: int,
                  last_read_message_id: int,
                  number_of_messages: int):
    db.query_all("""
    UPDATE members
    SET new_messages = new_messages - %(number_of_messages)s,
        last_read_message_id = %(last_read_message_id)s
    WHERE chat_id = %(chat_id)s
    AND user_id = %(user_id)s
    RETURNING last_read_message_id
    """, chat_id=chat_id, user_id=user_id, number_of_messages=number_of_messages,
                        last_read_message_id=last_read_message_id)

def get_chat_for_message(message_id):
    return db.query_all("""
    SELECT messages.chat_id, messages.message_id
    FROM messages
    WHERE messages.message_id = %(message_id)s
    RETURNING messages.chat_id
    """, message_id=message_id)

def mark_as_unread(message_id, chat_id):
    db.query_all("""
    UPDATE members
    SET new_messages = new_messages + 1
    WHERE chat_id = 
    """)


def send_message(chat_id: int=0, user_id: int=0, content: str='hello', added_at: str="1999-10-10 20:09:07"):
    # TODO: В методе чтения сообщений надо будет, напротив, уменьшать число непрочитанных сообщений
    # Создадим сообщение в таблице messages
    message_id = db.query_all("""
    INSERT INTO messages (chat_id, user_id, content, added_at)
    VALUES ( %(chat_id)s, %(user_id)s, %(content)s, %(added_at)s )
    RETURNING message_id;
    """, chat_id=chat_id, user_id=user_id, content=content, added_at=added_at)
    if message_id:
        message_id = message_id[0].get('message_id')
    # А теперь всем пользователям добавим запись о созданном сообщении
    # и увеличим счетчик непрочитанных
    db.query_all("""
    UPDATE members
    SET new_messages = new_messages + 1
    WHERE chat_id = %(chat_id)s
    /* самому себе счетчик увеличивать не надо :) */
    AND user_id != %(user_id)s
    RETURNING chat_id
    """, chat_id=chat_id, user_id=user_id)
    return message_id
