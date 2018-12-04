import unittest
from YourChef.server import ManageDishHelper
from Test.SampleManageDish import manage_fail_dish


class Data:
    def __init__(self, input):
        self.data = input


class Object(object):
    pass


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = ManageDishHelper('DishInfo')
        assert server is not None


    def testFailRegister(self):
        server = ManageDishHelper("test_user")
        for dish in manage_fail_dish:
            form = Object()
            form.restaurant = Data(dish['restaurant'])
            form.dishname = Data(dish['dishname'])
            result, message = server.addDish(form.restaurant, form.dishname)
            assert not result
            
