# TODO: перенести сюда эталонные тесты и константы. Из тестового класса.

from instance.config import TestingConfig as config
from instance.config import DevelopmentConfig as dev_config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

USER_IDS = range(2, 10)
CHAT_IDS = range(2, 10)
MATRIX = [[2, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 8], [7, 9], [9, 8]]


def fill_users():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for user_id in USER_IDS:
        cursor.execute("""INSERT INTO users (user_id, nick, name, avatar)
                      VALUES (%(user_id)s, %(nick)s, %(name)s, %(avatar)s)
                      ON CONFLICT DO NOTHING;""",
                       {'user_id': user_id, 'nick': 'test%s' % user_id, 'name': 'test-user', 'avatar': ''})
    cursor.close()
    conn.commit()
    conn.close()


def fill_chats():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for chat_id in CHAT_IDS:
        cursor.execute("""
        INSERT INTO chats (chat_id, is_group_chat, topic)
        VALUES (%(chat_id)s, 0, 'Test chat')
        ON CONFLICT DO NOTHING;
        """, {'chat_id': chat_id})
    cursor.close()
    conn.commit()
    conn.close()


def fill_members():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for ind, value in enumerate(MATRIX):
        chat_id = ind + min(CHAT_IDS)
        for user_id in value:
            cursor.execute("""
            INSERT INTO members (user_id, chat_id, new_messages)
            VALUES (%(user_id)s, %(chat_id)s, 0)
            ON CONFLICT DO NOTHING;
            """, {'user_id': user_id, 'chat_id': chat_id})
    cursor.close()
    conn.commit()
    conn.close()


def fill_messages():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for ind, value in enumerate(MATRIX):
        chat_id = ind + min(CHAT_IDS)
        user1, user2 = value
        for i in range(10):
            sender = user1 if (i % 2 == 0) else user2
            cursor.execute("""
            INSERT INTO messages(chat_id, user_id, content)
            VALUES (%(chat_id)s, %(user_id)s, %(content)s)
            """, {'chat_id': chat_id, 'user_id': sender, 'content': 'test {} from {}'.format(i, sender)})
    cursor.close()
    conn.commit()
    conn.close()


def init_all():
    create_db()
    fill_tables()
    fill_users()
    fill_chats()
    fill_members()
    fill_messages()


def deinit_all():
    delete_db()


def fill_tables():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER,
                            password=config.DB_PASS, host=config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
    CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    nick TEXT NOT NULL UNIQUE
        CHECK (length(nick) < 32),
    name TEXT NOT NULL
        CHECK (length(name) < 32),
    avatar TEXT NOT NULL
);

CREATE TABLE chats (
  chat_id SERIAL PRIMARY KEY,
  is_group_chat INTEGER,
  topic TEXT NOT NULL
    CHECK (length(topic) < 1000),
  added_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL
      REFERENCES chats(chat_id),
    user_id INTEGER NOT NULL
        REFERENCES users(user_id),
    content TEXT NOT NULL
        CHECK (length(content) < 65536),
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE members (
  user_id INTEGER NOT NULL
    REFERENCES users(user_id),
  chat_id INTEGER NOT NULL
    REFERENCES chats(chat_id),
  new_messages INTEGER NOT NULL,
  last_read_message_id INTEGER
    REFERENCES messages(message_id)
);

CREATE TABLE attachments (
  attach_id SERIAL PRIMARY KEY,
  chat_id INTEGER NOT NULL
    REFERENCES chats(chat_id),
  user_id INTEGER NOT NULL
    REFERENCES users(user_id),
  message_id INTEGER NOT NULL
    REFERENCES messages(message_id),
  type TEXT NOT NULL
    CHECK (length(type) < 1000),
  url TEXT NOT NULL
);
    """)
    cursor.close()
    conn.commit()
    conn.close()


def create_db():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=dev_config.DB_NAME, user=dev_config.DB_USER,
                            password=dev_config.DB_PASS, host=dev_config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor.execute("""
    CREATE DATABASE {}
    """.format(config.DB_NAME))
    cursor.close()
    conn.commit()
    conn.close()


def delete_db():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=dev_config.DB_NAME, user=dev_config.DB_USER,
                            password=dev_config.DB_PASS, host=dev_config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor.execute("""
    DROP DATABASE {}
    """.format(config.DB_NAME))
    cursor.close()
    conn.commit()
    conn.close()


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def equals_json(json1, json2):
    return ordered(json1) == ordered(json2)


if __name__ == '__main__':
    init_all()
    #delete_db()
