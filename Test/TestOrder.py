import unittest
from YourChef.orderHelper import OrderHelper
from Test.SampleOrder import orders, orders_failed


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = OrderHelper('Order')
        assert server is not None

    def testRegister(self):
        server = OrderHelper("Order")
        for order in orders:
            result, message = server.add_order(order['restaurant'], order['dishes'], order['total'], order['userid'])
            assert result

    def testFailRegister(self):
        server = OrderHelper("Order")
        for order in orders_failed:
            result, message = server.add_order(order['restaurant'], order['dishes'], order['total'], order['userid'])
            assert not result
