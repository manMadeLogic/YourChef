# from flask import session
import unittest
from unittest.mock import patch
import YourChef.application as application


class TestAddDishCase(unittest.TestCase):
    #
    # def setUp(self):
    #     application.application.testing = True
    #     self.app = application.application.test_client()
    #     session['dishes'] = [('a', 1)]

    # test add to session
    # todo
    def testSession(self):
        # session['dishes'] = [('a', 1)]
        with patch("YourChef.application.session", dict()) as session:
            session['dishes'] = [['a', 1]]
            session['total_dishes'] = 1
            session['restaurant'] = 'a'
            assert application.add_a_dish("a", "c", 1)
            # print(len(session['dishes']))
            # print(session['dishes'])
            assert len(session['dishes']) == 2 and session['total_dishes'] == 2
            assert application.add_a_dish("a", "a", 1)
            assert application.add_a_dish("a", "c", 1)
            # print(len(session['dishes']))
            # print(session['dishes'])
            assert len(session['dishes']) == 2 and session['total_dishes'] == 4
            assert application.add_a_dish("a", "a", 1)
            assert application.add_a_dish("a", "c", 1)
            assert application.add_a_dish("a", "a", 1)
            assert application.add_a_dish("a", "c", 1)
            assert application.add_a_dish("a", "a", 1)
            assert application.add_a_dish("a", "c", 1)
            assert session['total_dishes'] == 10
            assert not application.add_a_dish("a", "a", 1)
            assert not application.add_a_dish("a", "c", 1)
            assert session['total_dishes'] == 10


if __name__ == '__main__':
    unittest.main()
