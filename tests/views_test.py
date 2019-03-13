from unittest import TestCase, main, skip
from app import db
from tests.utils_orm import fill_all
from app.views import *
from app.model import User, Chat
from tests.utils_orm import USER_IDS
from werkzeug.exceptions import NotFound
import time


class ViewsMethodsTest(TestCase):

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.users, self.chats, self.messages = fill_all()

    def test_create_chat(self):
        with self.subTest('Simple create'):
            CHAT_TOPIC = 'chat_topic_1'
            chat_members = USER_IDS[:len(USER_IDS) // 2]
            create_chat(topic=CHAT_TOPIC,
                        members_id=chat_members,
                        is_group=0)
        chat = db.session.query(Chat).filter(Chat.topic == CHAT_TOPIC).first()
        with self.subTest('Chat exists'):
            self.assertIsNotNone(chat)
        with self.subTest('Check member'):
            self.assertEqual([user.id for user in chat.users], list(chat_members))
        with self.subTest('Check topic'):
            self.assertEqual(chat.topic, CHAT_TOPIC)

    def test_get_chat_messages(self):
        with self.subTest('Not empty after initialization'):
            # Проверим, что после инициализации список сообщений не пуст
            self.assertNotEqual(len(get_chat_messages(self.chats[0].id)), 0)
        with self.subTest('Is added after manual insert'):
            # Добавим руками сообщение и проверим, появится ли оно
            CONTENT = 'Check!'
            new_mess = Message(chat=self.chats[0], user=self.chats[0].users[0], content=CONTENT)
            db.session.add(new_mess)
            db.session.commit()
            # Оно будет последним, проверим его
            message_json = get_chat_messages(self.chats[0].id)[-1]
            self.assertEqual(message_json['user_id'], str(self.chats[0].users[0].id))
            self.assertEqual(message_json['content'], CONTENT)

    def test_get_user_chats(self):
        user = self.users[0]
        with self.subTest('Simple get'):
            self.assertNotEqual(len(get_user_chats(user_id=user.id)), 0)
        with self.subTest('Negative limit'):
            with self.assertRaises(ValueError):
                get_user_chats(user_id=user.id, limit=-2)
        with self.subTest('Bad user_id'):
            with self.assertRaises(NotFound):
                get_user_chats(user_id=10**8)

    def test_leave_chat(self):
        user, chat = self.users[-1], self.users[-1].chats[-1]
        user_id, chat_id = user.id, chat.id
        with self.subTest("Chat is really deleted"):
            # Выйдем
            leave_chat(chat_id=chat_id, user_id=user_id)
            # Проверим, что чата у пользователя не осталось
            self.assertIsNone(next((x for x in user.chats if x.id == chat_id), None))
        with self.subTest("ValueError if user not in chat"):
            chat_id = 10**5
            with self.assertRaises(ValueError):
                leave_chat(chat_id=chat_id, user_id=user_id)

    def test_join_chat(self):
        user = self.users[0]
        # Берем первый попавшийся чат, в котором НЕ состоит пользователь
        chat = next(chat for chat in self.chats if user not in chat.users)
        with self.subTest('Simple join'):
            join_chat(user_id=user.id, chat_id=chat.id)
        with self.subTest('User is now in chat'):
            self.assertTrue(chat in user.chats)
        with self.subTest('Chat has the user'):
            self.assertTrue(user in chat.users)
        with self.subTest('Incorrect user'):
            with self.assertRaises(NotFound):
                join_chat(user_id=10**8, chat_id=chat.id)
        with self.subTest('Incorrect chat'):
            with self.assertRaises(NotFound):
                join_chat(user_id=user.id, chat_id=10**8)
        with self.subTest('Already joined'):
            with self.assertRaises(ValueError):
                join_chat(user_id=user.id, chat_id=user.chats[0].id)

    def test_leave_all_chats(self):
        chat = self.chats[0]
        for user in chat.users:
            leave_chat(chat_id=chat.id, user_id=user.id)
        # TODO: а стоит ли удалять чат, если в нем нет участников?
        pass


if __name__ == '__main__':
    main()
