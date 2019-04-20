from app import db, app
from app.search import add_to_index, remove_from_index, query_index
from sqlalchemy import func
from werkzeug.contrib.cache import MemcachedCache
import sys

cache = MemcachedCache(['127.0.0.1:11211'])
MAX_MESSAGE_SIZE = 65536


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return ids, total
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)).all(), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)



class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    chat_id = db.Column('chat_id', db.Integer, db.ForeignKey('chats.id', ondelete='cascade'))


class Chat(SearchableMixin, db.Model):
    __tablename__ = 'chats'
    __searchable__ = ['topic']
    id = db.Column(db.Integer, primary_key=True)
    is_group = db.Column(db.Integer)
    topic = db.Column(db.String(1000), nullable=False)
    added_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now())
    messages = db.relationship('Message', back_populates='chat')
    users = db.relationship('User', secondary='members', backref='Chat')

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class User(SearchableMixin, db.Model):
    __tablename__ = 'users'
    __searchable__ = ['nick', 'name']
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(32), nullable=False, unique=True)
    name = db.Column(db.String(32), nullable=False)
    avatar = db.Column(db.String, nullable=False)
    messages = db.relationship('Message', back_populates='user')
    chats = db.relationship('Chat', secondary='members', backref='User')

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    chat = db.relationship("Chat", back_populates='messages')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='messages')
    content = db.Column(db.String(MAX_MESSAGE_SIZE), nullable=False)
    added_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now())

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


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
