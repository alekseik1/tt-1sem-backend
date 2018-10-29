from app import db


def list_messages_by_chat(chat_id, limit):
    return db.query_all("""
        SELECT user_id, nick, name,
               message_id, content, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
""", chat_id=int(chat_id), limit=int(limit))


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


def find_user(limit: int=100, **kwargs):
    user_name = kwargs.get('user_name', None)
    if user_name:
        return _get_all_user_info("user_name", user_name, limit=limit)

    nick = kwargs.get('nick', None)
    if nick:
        return _get_all_user_info("nick", nick, limit=limit)

    user_id = kwargs.get('user_id', None)
    if user_id:
        return _get_all_user_info("user_id", user_id, limit=limit)
