import unittest

from YourChef.server import RegistrationHelper
from Test.SampleUser import insert_users, insert_fail_users, users
# from Test.SampleUser import insert_users, insert_fail_users


class Data:
    def __init__(self, input):
        self.data = input


class Object(object):
    pass


class TestRegistrationCase(unittest.TestCase):

    def testServer(self):
        server = RegistrationHelper("test_user")
        assert server is not None

    def testFailRegister(self):
        server = RegistrationHelper("test_user")
        for user in insert_fail_users:
            form = Object()
            form.email = Data(user["email"])
            form.username = Data(user["username"])
            form.password = Data(user["password"])
            form.userid = Data(user["userid"])
            result, message = server.register(form)
            assert not result

    def testGetUser(self):
        server = RegistrationHelper("test_user")
        for user in users:
            login, message = server.login(user["userid"], user['password'])
            assert login
        #
        fake_password = "xxxx00"
        for user in users:
            login, message = server.login(user["userid"], fake_password)
            assert not login


    def testRegister(self):
        server = RegistrationHelper("test_user")
        for user in insert_users:
            form = Object()
            form.email = Data(user["email"])
            form.username = Data(user["username"])
            form.password = Data(user["password"])
            form.userid = Data(user["userid"])
            result, message = server.register(form)
            assert result
            assert server.delete_user(user["userid"])


if __name__ == '__main__':
    unittest.main()
