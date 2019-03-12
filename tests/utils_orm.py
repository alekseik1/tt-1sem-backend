from app.model import User, Message, Member, Chat
from app import db

USER_IDS = range(2, 10)
CHAT_IDS = range(2, 10)
MATRIX = [[2, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 8], [7, 9], [9, 8]]


def fill_users():
    users = []
    for user_id in USER_IDS:
        users.append(User(nick='test_user_{}'.format(user_id),
                          name='tester_{}'.format(user_id),
                          avatar='REKLAMA',
                          )
                     )
    db.session.add_all(users)
    db.session.commit()


def fill_all():
    fill_users()
    db.session.commit()
