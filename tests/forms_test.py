import unittest
from app.views import validate_user
from app.model import User


class FormsTest(unittest.TestCase):

    def test_user_form(self):
        user_good = User(name='Vasya', nick='pupkin_vasya', avatar='')
        short_nick = User(name='dw', nick='w', avatar='')
        self.assertTrue(validate_user(user_good))
        self.assertFalse(validate_user(short_nick))


if __name__ == '__main__':
    unittest.main()
