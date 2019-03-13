from unittest import TestCase, main, skip
from app import db
from tests.utils_orm import fill_all
from app.views import *
from app.model import User, Chat
from tests.utils_orm import USER_IDS, chats, users
import time


class ViewsMethodsTest(TestCase):

    def setUp(self):
        # Почему-то в tearDown зависает drop_all(), будет теперь здесь
        db.drop_all()
        db.create_all()
        fill_all()

    def test_create_chat(self):
        CHAT_TOPIC = 'chat_topic_1'
        chat_members = USER_IDS[:len(USER_IDS) // 2]
        create_chat(topic=CHAT_TOPIC,
                    members_id=chat_members,
                    is_group=0)
        chat = db.session.query(Chat).filter(Chat.topic == CHAT_TOPIC).first()
        # Чат существует
        self.assertIsNotNone(chat)
        # В чате нужные пользователи
        self.assertEqual([user.id for user in chat.users], list(chat_members))
        # У чата нужный топик
        self.assertEqual(chat.topic, CHAT_TOPIC)

    def test_get_chat_messages(self):
        # Проверим, что после инициализации список сообщений не пуст
        self.assertNotEqual(len(get_chat_messages(chats[0].id)), 0)
        # Добавим руками сообщение и проверим, появится ли оно
        CONTENT = 'Check!'
        new_mess = Message(chat=chats[0], user=chats[0].users[0], content=CONTENT)
        db.session.add(new_mess)
        db.session.commit()
        # Оно будет последним, проверим его
        message_json = get_chat_messages(chats[0].id)[-1]
        self.assertEqual(message_json['user_id'], str(chats[0].users[0].id))
        self.assertEqual(message_json['content'], CONTENT)

    def test_leave_chat(self):
        user, chat = users[-1], users[-1].chats[-1]
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


if __name__ == '__main__':
    main()
