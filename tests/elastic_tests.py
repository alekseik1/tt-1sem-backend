from unittest import TestCase, main
from app import db, app
from tests.utils_orm import fill_all
from app.model import User, Chat
import time


class ElasticsearchTests(TestCase):

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.users, self.chats, self.messages = fill_all()

    def test_search_user(self):
        users = [self.users[0]]
        with self.subTest('Search for the first user'):
            found, total = User.search(users[0].nick, 1, 100)
            self.assertEqual(total, 1)
            self.assertEqual(found[0], users[0])
        with self.subTest('User not found'):
            found, total = User.search('I dont exist at all!', 1, 100)
            self.assertEqual(total, 0)
            self.assertEqual(found, [])

        users = [
            User(name='Tom Sayer', nick='free_lancer_228', avatar=''),
            User(name='Tom Balmer', nick='fire_lancer_300', avatar='')
        ]
        db.session.add_all(users)
        db.session.commit()
        time.sleep(1)
        with self.subTest('Sayer by name'):
            for u in users:
                found, total = User.search(u.name, 1, 100)
                # Находит двух, но с разным score
                self.assertEqual(total, 2)
        with self.subTest('Say* by name'):
            found, total = User.search('Tom', 1, 100)
            self.assertEqual(total, 2, 'Expected to find 2 users')
        with self.subTest('by nickname'):
            for u in users:
                found, total = User.search(u.nick, 1, 100)
                self.assertEqual(total, 1)
                self.assertEqual(found[0], u)

    def test_search_chat(self):
        chats = [self.chats[0]]
        with self.subTest('Chat by name'):
            found, total = Chat.search(chats[0].topic, 1, 100)
            self.assertEqual(total, 1)
        with self.subTest('No chat found'):
            found, total = Chat.search('I dont exist', 1, 100)
            self.assertEqual(total, 0)


if __name__ == '__main__':
    main()
