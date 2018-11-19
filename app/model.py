from app import db


def list_messages_by_chat(chat_id, limit, offset, from_id=0):
    tmp_res = db.query_all("""
        SELECT user_id, nick, name,
               message_id, content, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        AND message_id > %(from_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
""", chat_id=int(chat_id), limit=int(limit), from_id=from_id)
    if offset >= len(tmp_res):
        return []
    else:
        return tmp_res[offset:]


def _get_all_user_info(param: str="user_id",
                       param_value: str="0",
                       limit: int=100):
    # TODO: Переделай через одну передачу и проверку всех условий
    # TODO: вот таким образом
    # TODO: WHERE nick= %(nick)s OR name = %(name)s
    return db.query_all("""
    SELECT user_id, nick, name, avatar
    FROM users
    WHERE {} = %(param_value)s
    LIMIT %(limit)s;
    """.format(param), param_value=param_value, limit=int(limit))


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


def create_chat(topic: str="", is_group: int=0):
    return db.insert_one("""
    INSERT INTO chats (is_group_chat, topic)
    VALUES ( %(is_group)s , %(topic)s )
    RETURNING chat_id;
    """, is_group=str(is_group), topic=str(topic))


def read_messages(user_id: int, chat_id: int, last_read_message_id: int, number_of_messages: int):
    return db.query_one("""
    UPDATE members
    SET new_messages = new_messages - %(number_of_messages)s,
        last_read_message_id = %(last_read_message_id)s
    WHERE chat_id = %(chat_id)s
    AND user_id = %(user_id)s
    """, chat_id=chat_id, user_id=user_id, number_of_messages=number_of_messages,
                        last_read_message_id=last_read_message_id)


def send_message(chat_id: int=0, user_id: int=0, content: str='hello', added_at: str="1999-10-10 20:09:07"):
    # TODO: В методе чтения сообщений надо будет, напротив, уменьшать число непрочитанных сообщений
    return db.insert_one("""
    /* Добавил запись в таблцу Members, чтобы другие пользователи имели одно непрочитанное сообщение */
    UPDATE members
    SET new_messages = new_messages + 1
    WHERE chat_id = %(chat_id)s;
    /* Добавим сообщение в таблицу Messages */
    INSERT INTO messages (chat_id, user_id, content, added_at)
    VALUES ( %(chat_id)s, %(user_id)s, %(content)s, %(added_at)s )
    RETURNING message_id;
    """, chat_id=chat_id, user_id=user_id, content=content, added_at=added_at)
