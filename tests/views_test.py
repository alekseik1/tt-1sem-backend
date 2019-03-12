from unittest import TestCase, main
from app import db
from tests.utils_orm import fill_all
from app.views import create_chat
from app.model import User, Chat
from tests.utils_orm import USER_IDS


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


if __name__ == '__main__':
    main()
