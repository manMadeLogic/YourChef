import unittest

from YourChef.userHelper import UserHelper
from passlib.hash import sha256_crypt
from Test.SampleUser import users, insert_users

class Data:
    def __init__(self, input):
        self.data = input


class Object(object):
    pass


class TestUserFunctionCase(unittest.TestCase):

    def testDBConn(self):
        db = UserHelper("test_user")
        assert db is not None

    def testGetUser(self):
        db = UserHelper("test_user")
        for user in users:
            user_data = db.get_user(user["userid"])
            assert sha256_crypt.verify(user['password'], user_data['password']) and user_data['email'] == user['email'] and user_data['username'] == user['username']

    def testInsertUser(self):
        db = UserHelper("test_user")
        for user in insert_users:
            form = Object()
            form.email = Data(user["email"])
            form.username = Data(user["username"])
            form.password = Data(user["password"])
            form.userid = Data(user["userid"])
            result, message = db.insert(form)
            assert result

        for user in insert_users:
            assert db.delete_user(user["userid"])

    def testCheckPassword(self):
        db = UserHelper("test_user")
        for user in users:
            result, message = db.check_password(user["userid"], user["password"])
            assert result

        # non-exist
        result, message = db.check_password(insert_users[0]["userid"], insert_users[0]["password"])
        assert not result

        # wrong password
        for user in users:
            fake_password = "xxxx00"
            result, message = db.check_password(user["userid"], fake_password)
            assert not result


if __name__ == '__main__':
    unittest.main()
