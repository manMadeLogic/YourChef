from YourChef.userHelper import UserHelper
import re


class RegistrationHelper:
    def __init__(self, db_name="RegisterInfo"):
        self.db = UserHelper(db_name)

    def login(self, form):
        user_id = form['userid']
        password = form['password']
        return self.db.check_password(user_id, password)

    def register(self, form):
        # todo general helper
        userid = form.userid.data
        if not userid or userid == "":
            return False, "empty user id"
        if re.findall('[^A-Za-z0-9_]', userid):
            return False, "Can't contain special character"
        user = self.db.get_user(userid)
        if user:
            return False, "Repeated user ID"
        else:
            return self.db.insert(form)

    # only for test and quick fix
    def delete_user(self, user_id):
        return self.db.delete_user(user_id)
