import unittest

from YourChef.dbHelper import UserHelper


class UserFunctionTestCase(unittest.TestCase):

    def testDBConn(self):
        db = UserHelper("test_user")
        assert db is not None

    def testGetUser(self):
        assert True

    def testAddUser(self):
        assert True

    def testCheckPassword(self):
        assert True


if __name__ == '__main__':
    unittest.main()
