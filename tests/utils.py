# TODO: перенести сюда эталонные тесты и константы. Из тестового класса.

from instance.config import DevelopmentConfig as config

USER_IDS = range(2, 10)


def fill_users():
    import psycopg2.extras
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for user_id in USER_IDS:
        cursor.execute("""INSERT INTO users (user_id, nick, name, avatar)
                      VALUES (%(user_id)s, %(nick)s, %(name)s, %(avatar)s);""",
                       {'user_id': user_id, 'nick': 'test%s' % user_id, 'name': 'test-user', 'avatar': ''})
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    fill_users()
