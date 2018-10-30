import unittest
from YourChef.dbHelper import UserHelper


class UserFunctionTestCase(unittest.TestCase):

    def testDBConn(self):
        db = UserHelper("")

    def testGetUser(self):
        pass

    def testAddUser(self):
        pass

    def testCheckPassword(self):
        pass


if __name__ == '__main__':
    unittest.main()