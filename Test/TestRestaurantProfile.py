import unittest

from YourChef.restaurant_profile import RestaurantProfileDBHelper
from Test.SampleResProfile import insert_users, users


class Data:
    def __init__(self, input):
        self.data = input


class Object(object):
    pass


class TestRestaurantProfileCase(unittest.TestCase):

    def testGetUser(self):
        server = RestaurantProfileDBHelper()
        for user in users:
            user_data = server.get_user(user["userid"])
            assert user_data['userid'] == user['userid'] and user_data['username'] == user['username'] and \
                   user_data['spicy'] == user['spicy'] and user_data['sour'] == user['sour'] and \
                   user_data['sweet'] == user['sweet'] and user_data['salt'] == user['salt']

    def testInsertUser(self):
        server = RestaurantProfileDBHelper()
        for user in insert_users:
            form = Object()
            form.userid = Data(user["userid"])
            form.username = Data(user["username"])
            form.salt = Data(user["salt"])
            form.sour = Data(user["sour"])
            form.sweet = Data(user["sweet"])
            form.spicy = Data(user["spice"])

            result, message = server.insert(form)
            assert result
            assert server.delete_user(user["userid"])


if __name__ == '__main__':
    unittest.main()
