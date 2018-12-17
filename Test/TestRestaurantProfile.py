import unittest

from YourChef.restaurant_profile import RestaurantProfileDBHelper
from Test.SampleResProfile import insert_profiles, update_profiles, profiles


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
        for user in insert_profiles:
            result, message = server.insert(user, user['userid'], user['username'])
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

    # TODO REVIEW
    def testGetAll(self):
        server = RestaurantProfileDBHelper('rProfile_test')
        response = server.table.scan()
        assert response and len(response['Items']) == len(profiles)

        # Assuming 'userid' is the primary key, response and profiles should have the same entries
        for res in response['Items']:
            flag = False
            for user in profiles:
                if res['userid'] == user['userid']:
                    flag = res['userid'] == user['userid'] and res['username'] == user['username'] and \
                           res['spicy'] == user['spicy'] and res['sour'] == user['sour'] and \
                           res['sweet'] == user['sweet'] and res['salt'] == user['salt']
                    break

            assert flag




# if __name__ == '__main__':
#     server = RestaurantProfileDBHelper('rProfile_test')
#     for user in profiles:
#         result, message = server.insert(user, user['userid'], user['username'])


