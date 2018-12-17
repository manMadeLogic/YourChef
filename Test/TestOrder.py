import unittest

from Test.SampleOrder import orders, orders_failed
from YourChef.orderHelper import OrderHelper


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
