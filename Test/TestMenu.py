import unittest
from YourChef.menu import ManageDishHelper
from Test.SampleManageDish import manage_fail_dish, insert_dishes
# from Test.SampleManageDish import manage_fail_dish, insert_dishes, dishes


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = ManageDishHelper('DishInfo')
        assert server is not None

    def testFailAddDish(self):
        server = ManageDishHelper("DishInfo")
        for dish in manage_fail_dish:
            result, message = server.addDish(dish['restaurant'], dish)
            assert not result

    def testAddAndDeleteDish(self):
        server = ManageDishHelper("DishInfo")
        for dish in insert_dishes:
            result, message = server.addDish(dish['restaurant'], dish)
            assert result

        for dish in insert_dishes:
            assert server.deleteDish(dish['restaurant'], dish["dishname"])


if __name__ == '__main__':
    unittest.main()
