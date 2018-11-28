from flask import session
import unittest
import YourChef.application as application


class TestAddDishCase(unittest.TestCase):

    def setUp(self):
        application.application.testing = True
        self.app = application.application.test_client()
        session['dishes'] = [('a', 1)]

    # test add to session
    # todo
    def testSession(self):
        assert session['dishes']


if __name__ == '__main__':
    unittest.main()
