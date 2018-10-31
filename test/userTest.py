import unittest

from YourChef.dbHelper import UserHelper
from passlib.hash import sha256_crypt
from test.SampleUser import users


class UserFunctionTestCase(unittest.TestCase):

    def testDBConn(self):
        db = UserHelper("test_user")
        assert db is not None

    def testGetUser(self):
        db = UserHelper("test_user")
        for user in users:
            user_data = db.get_user(user["userid"])
            assert sha256_crypt.verify(user['password'], user_data['password']) and user_data['email'] == user['email'] and user_data['username'] == user['username']
    #
    # def testAddUser(self):
    #     assert True


if __name__ == '__main__':
    unittest.main()
