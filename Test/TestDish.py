import unittest
from YourChef.dishHelper import DishHelper
from Test.SampleManageDish import manage_fail_dish


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = DishHelper('DishInfo')
        assert server is not None

    def testFailRegister(self):
        server = DishHelper("DishInfo")
        for dish in manage_fail_dish:
            # form = Object()
            # form.restaurant = Data(dish['restaurant'])
            # form.dishname = Data(dish['dishname'])
            # form.price = Data(dish['price'])
            result, message = server.add_dish(dish['restaurant'], dish, 10)
            assert not result
