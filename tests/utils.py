# TODO: перенести сюда эталонные тесты и константы. Из тестового класса.

from instance.config import DevelopmentConfig as config

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


if __name__ == '__main__':
    fill_users()
    fill_chats()
    fill_members()
    fill_messages()
