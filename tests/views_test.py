from unittest import TestCase, main, skip
from app import db
from tests.utils_orm import fill_all
from app.views import *
from app.model import User, Chat, MAX_MESSAGE_SIZE
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
            chat_members = USER_IDS[:len(USER_IDS)]
            create_chat(topic=CHAT_TOPIC,
                        users_id=list(chat_members),
                        is_group=0)
        chat = db.session.query(Chat).filter(Chat.topic == CHAT_TOPIC).first()
        with self.subTest('Chat exists'):
            self.assertIsNotNone(chat)
        with self.subTest('Check member'):
            self.assertEqual([user.id for user in chat.users], list(chat_members))
        with self.subTest('Check topic'):
            self.assertEqual(chat.topic, CHAT_TOPIC)

    def test_create_chat_bad_users(self):
        CHAT_TOPIC = 'bad_chat'
        with self.subTest('Create chat: no such user'):
            chat_members = [max(USER_IDS) + 1]
            with self.assertRaises(ValueError):
                create_chat(topic=CHAT_TOPIC, users_id=list(chat_members), is_group=0)
        with self.subTest('Create chat: one user does not exist'):
            chat_members = list(USER_IDS)
            chat_members.append(max(USER_IDS) + 1)     # Добавим 1 лишнего)
            with self.assertRaises(ValueError):
                create_chat(topic=CHAT_TOPIC, users_id=list(chat_members), is_group=0)

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

    def test_send_message(self):
        user = self.users[-1]
        chat = user.chats[-1]
        CONTENT = 'TestSuite message'
        with self.subTest('Simple send'):
            send_message(sender_id=user.id, chat_id=chat.id, text='123', token='-1')
        message_id = send_message(sender_id=user.id, chat_id=chat.id, text=CONTENT, token='-1')
        with self.subTest('Chat has messages'):
            message = next(message for message in chat.messages if message.id == message_id)
            self.assertIsNotNone(message)
            self.assertEqual(message.content, CONTENT)
        with self.subTest('User has messages'):
            message = next(message for message in user.messages if message.id == message_id)
            self.assertIsNotNone(message)
            self.assertEqual(message.content, CONTENT)
        with self.subTest('ValueError on too long content'):
            LONG_CONTENT = 'a'*(MAX_MESSAGE_SIZE+1)
            with self.assertRaises(ValueError):
                send_message(sender_id=user.id, chat_id=chat.id, text=LONG_CONTENT, token='-1')
        with self.subTest('404 on user not found'):
            with self.assertRaises(NotFound):
                send_message(sender_id=10 * 8, chat_id=chat.id, text=CONTENT, token='-1')
        with self.subTest('404 on chat not found'):
            with self.assertRaises(NotFound):
                send_message(sender_id=user.id, chat_id=10 ** 8, text=CONTENT, token='-1')

    def test_find_user_single(self):
        # Добавим пользователя, которого будем искать
        NICK, NAME = 'sneaky_228', 'Riki Maru'
        sneaky_user = User(nick=NICK, name=NAME, avatar='')
        db.session.add(sneaky_user)
        db.session.commit()

        def _check_user(user_to_check, another_user=sneaky_user):
            self.assertEqual(user_to_check['id'], str(another_user.id))
            self.assertEqual(user_to_check['name'], str(another_user.name))
            self.assertEqual(user_to_check['nick'], str(another_user.nick))

        with self.subTest('None arguments passed'):
            self.assertEqual(json.loads(find_user()), [])

        with self.subTest('Find by full nick'):
            user = json.loads(find_user(nick=NICK))[0]
            _check_user(user)
        with self.subTest('Find by full name'):
            user = json.loads(find_user(name=NAME))[0]
            _check_user(user)
        with self.subTest('Name 3 first symbols'):
            users = json.loads(find_user(name=NAME[:3]))
            # Пока такой пользователь только один
            _check_user(users[0])
        with self.subTest('Nick 3 first symbols'):
            users = json.loads(find_user(nick=NICK[:3]))
            _check_user(users[0])
        with self.subTest('No match nick'):
            users = json.loads(find_user(nick='123' + NICK))
            self.assertEqual(len(users), 0)
        with self.subTest('No match name'):
            users = json.loads(find_user(name='123' + NAME))
            self.assertEqual(len(users), 0)
        # -------------------------------------------------------------------

    def test_find_user_multiple(self):
        NICK, NAME = 'multiple_228', 'Marin Komitsky'
        sneaky_user = User(nick=NICK, name=NAME, avatar='')
        sneaky_user2 = User(nick=NICK + '_1', name=NAME + '_1', avatar='')
        db.session.add_all([sneaky_user, sneaky_user2])
        db.session.commit()

        def _check_multiple(user):
            self.assertTrue(int(user['id']) in [sneaky_user.id, sneaky_user2.id])
            self.assertTrue(user['nick'] in [sneaky_user.nick, sneaky_user2.nick])
            self.assertTrue(user['name'] in [sneaky_user.name, sneaky_user2.name])

        with self.subTest('Length on many matches'):
            users = json.loads(find_user(nick=NICK))
            self.assertEqual(len(users), 2)
        with self.subTest('Every user is correct'):
            users = json.loads(find_user(nick=NICK))
            for user in users:
                _check_multiple(user)
        with self.subTest('Many by first 3 letters nick'):
            users = json.loads(find_user(nick=NICK[:3]))
            self.assertEqual(len(users), 2)
            for user in users:
                _check_multiple(user)
        with self.subTest('Many by first 3 letters name'):
            users = json.loads(find_user(name=NAME[:3]))
            self.assertEqual(len(users), 2)
            for user in users:
                _check_multiple(user)

    def test_get_user_info(self):

        def _check_user(user1, user):
            return user1['id'] == str(user.id) \
                   and user1['name'] == user.name \
                   and user1['nick'] == user.nick

        with self.subTest('Correct values'):
            for user in self.users:
                testing_user = json.loads(get_user_info(user.id))
                self.assertTrue(_check_user(testing_user, user))
        with self.subTest('404 on not found'):
            with self.assertRaises(NotFound):
                get_user_info(user_id=10**8)
        with self.subTest('ValueError on non-integer id'):
            with self.assertRaises(ValueError):
                get_user_info('hello')

    def test_delete_chat_empty(self):
        user, chat = self.users[0], self.users[0].chats[0]
        user_id, chat_id = user.id, chat.id
        # Сначала все покинут чат
        chat.users = []
        db.session.commit()
        # Затем удалим уже пустой чат
        with self.subTest('No crash'):
            delete_chat(chat_id)
        with self.subTest('No chat after deletion'):
            chat_query = db.session.query(Chat).filter(Chat.id == chat_id).all()
            self.assertEqual(len(chat_query), 0)

    def test_delete_chat_with_users(self):
        user, chat = self.users[0], self.users[0].chats[0]
        user_id, chat_id = user.id, chat.id
        with self.subTest('Raises without flag `remove_users`'):
            with self.assertRaises(ValueError):
                delete_chat(chat_id)
        with self.subTest('Chat is deleted with flag'):
            delete_chat(chat_id, remove_users=True)
            chat_query = db.session.query(Chat).filter(Chat.id == chat_id).all()
            self.assertEqual(len(chat_query), 0)

    def test_delete_chat_nonexist(self):
        chat_id = 10**8
        with self.assertRaises(NotFound):
            delete_chat(chat_id)


if __name__ == '__main__':
    main()
