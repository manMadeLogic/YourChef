
from YourChef.dbHelper import UserHelper
import re


class RegistrationHelper:
    def __init__(self, db_name="RegisterInfo"):
        self.db = UserHelper(db_name)

    def login(self, user_id, password):
        return self.db.check_password(user_id, password)

    def register(self, form):
        userid = form.userid.data
        if re.findall('[^A-Za-z0-9_]', userid):
            return False, "Can't contain special character"
        user = self.db.get_user(userid)
        if user:
            return False, "Repeated user ID"
        else:
            return self.db.insert(form)
            # return False

    # only for test
    def delete_user(self, user_id):
        return self.db.delete_user(user_id)
    # def check_id(self, user_id):
    #     return True
