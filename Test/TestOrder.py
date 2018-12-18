import unittest

from SampleOrder import orders, orders_failed, orders_update, users
from orderHelper import OrderHelper


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = OrderHelper('order_test')
        assert server is not None

    def testRegister(self):
        server = OrderHelper("order_test")
        for order in orders:
            result, message = server.add_order(order['restaurant'], order['dishes'], order['total'], order['userid'])
            assert result

    def testFailRegister(self):
        server = OrderHelper("order_test")
        for order in orders_failed:
            result, message = server.add_order(order['restaurant'], order['dishes'], order['total'], order['userid'])
            assert not result

    def testUpdateOrder(self):
        server = OrderHelper("order_test")
        for order in orders_update:
            result = server.update(order['restaurant'], order['date'])
            assert result
        for order in orders:
            result, message = server.add_order(order['restaurant'], order['dishes'], order['total'], order['userid'])
            assert result

    def testGetOrder(self):
        server = OrderHelper("order_test")
        for usr in users:
            result = server.get_user_order(usr)
            assert result is not None

if __name__ == '__main__':
    unittest.main()