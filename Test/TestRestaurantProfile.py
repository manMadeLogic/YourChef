import unittest

from restaurant_profile import RestaurantProfileDBHelper
from SampleResProfile import insert_users, update_profiles, profiles


class TestRestaurantProfileCase(unittest.TestCase):

    def testGetUser(self):
        server = RestaurantProfileDBHelper('rProfile_test')
        for user in profiles:
            user_data = server.get_user(user["userid"])
            assert user_data['userid'] == user['userid'] and user_data['username'] == user['username'] and \
                   user_data['spicy'] == user['spicy'] and user_data['sour'] == user['sour'] and \
                   user_data['sweet'] == user['sweet'] and user_data['salt'] == user['salt']

    def testInsertUser(self):
        server = RestaurantProfileDBHelper('rProfile_test')
        for user in insert_users:
            result, message = server.insert(user)
            assert result
            assert server.delete_user(user["userid"])


    def testUpdateUser(self):
        server = RestaurantProfileDBHelper('rProfile_test')
        for user in update_profiles:
            assert server.update_flavor(user['userid'], user['salt'], user['sour'], user['sweet'], user['spicy'])
            user_data = server.get_user(user["userid"])
            assert user_data['userid'] == user['userid'] and user_data['username'] == user['username'] and \
                   user_data['spicy'] == user['spicy'] and user_data['sour'] == user['sour'] and \
                   user_data['sweet'] == user['sweet'] and user_data['salt'] == user['salt']


if __name__ == '__main__':
    unittest.main()
