import unittest

from YourChef.user_profile import UserProfileDBHelper
from Test.SampleUserProfile import insert_users, update_users, users


class TestRestaurantProfileCase(unittest.TestCase):
    def testGetUser(self):
        server = UserProfileDBHelper('uProfile_test')
        for user in users:
            # server.insert(user, user['userid'])
            user_data = server.get_user(user["userid"])
            print("user_data", user_data)
            print("user", user)
            assert user_data['userid'] == user['userid'] and user_data['spicy'] == user['spicy'] and \
                   user_data['sour'] == user['sour'] and user_data['sweet'] == user['sweet'] and \
                   user_data['salt'] == user['salt']

    def testInsertUser(self):
        server = UserProfileDBHelper('uProfile_test')
        for user in insert_users:
            result, message = server.insert(user, user["userid"])
            assert result
            assert server.delete_user(user["userid"])

    def testUpdateUser(self):
        server = UserProfileDBHelper('uProfile_test')
        for user in update_users:
            assert server.update_flavor(user['userid'], user['salt'], user['sour'], user['sweet'], user['spicy'])
            user_data = server.get_user(user["userid"])
            assert user_data['userid'] == user['userid'] and user_data['spicy'] == user['spicy'] and \
                   user_data['sour'] == user['sour'] and user_data['sweet'] == user['sweet'] and \
                   user_data['salt'] == user['salt']


# if __name__ == '__main__':
#     # unittest.main()
#     server = UserProfileDBHelper("uProfile_test")
#     for user in users:
#         result, message = server.insert(user, user["userid"])
