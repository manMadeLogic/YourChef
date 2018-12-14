import unittest

from YourChef.user_profile import UserProfileDBHelper
from Test.SampleUserProfile import insert_users, users


class Data:
    def __init__(self, input):
        self.data = input


class Object(object):
    pass


class TestRestaurantProfileCase(unittest.TestCase):
    def testGetUser(self):
        server = UserProfileDBHelper()
        # todo !!!!!!!!!!!!!!!!!!
        for user in users:
            user_data = server.get_user(user["userid"])
            assert user_data['userid'] == user['userid'] and user_data['spicy'] == user['spicy'] and \
                   user_data['sour'] == user['sour'] and user_data['sweet'] == user['sweet'] and \
                   user_data['salt'] == user['salt']

    def testInsertUser(self):
        server = UserProfileDBHelper()
        for user in insert_users:
            # form = Object()
            # form.userid = Data(user["userid"])
            # form.salt = Data(user["salt"])
            # form.sour = Data(user["sour"])
            # form.sweet = Data(user["sweet"])
            # form.spicy = Data(user["spice"])

            result, message = server.insert(user, user["userid"])
            assert result
            assert server.delete_user(user["userid"])


if __name__ == '__main__':
    unittest.main()
