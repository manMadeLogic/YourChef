import unittest
from YourChef.dishHelper import DishHelper
from Test.SampleManageDish import manage_fail_dish, insert_dishes, dishes


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = DishHelper('test_dish2')
        assert server is not None

    def testFailRegister(self):
        server = DishHelper("test_dish2")
        for dish in manage_fail_dish:
            result, message = server.add_dish(dish['restaurant'], dish['dishname'], dish['price'])
            assert not result

    def testInsertUser(self):
        server = DishHelper("test_dish2")
        for user in insert_dishes:
            result, message = server.add_dish(user['restaurant'], user['dishname'], user['price'])
            assert result
            assert server.delete_dish(user['restaurant'], user['dishname'])

    def testGetDishPrice(self):
        server = DishHelper("test_dish2")
        # print (profiles)
        for user in dishes:
            # server.insert(user, user['userid'], user['username'])
            user_data, message = server.get_dish_price(user['restaurant'], user['dishname'])
            # print("user_data", user_data)
            # print("user", user)
            assert user_data
            # print(user_data, user)
            assert int(user_data['price']) == user['price']


    def testUpdateUser(self):
        server = DishHelper("test_dish2")
        for user in dishes:
            assert server.change_price(user['restaurant'], user['dishname'], 35)
            user_data = server.get_dish_price(user['restaurant'], user['dishname'])
            assert user_data['userid'] == user['userid'] and user_data['username'] == user['username'] and \
                   user_data['spicy'] == user['spicy'] and user_data['sour'] == user['sour'] and \
                   user_data['sweet'] == user['sweet'] and user_data['salt'] == user['salt']

            assert server.change_price(user['restaurant'], user['dishname'], user['price'])

if __name__ == '__main__':
    unittest.main()
