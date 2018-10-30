
from flask import session
from YourChef.dbHelper import UserHelper

class BackServer:
    def __init__(self):
        self.db = UserHelper()

    def login(self, user_id, password):
        user, message = self.db.check_password(user_id, password)
        if not user:
            return False, message
        session['logged_in'] = True
        session['user_name'] = user["username"]
        session['user_id'] = user["userid"]
        # session['admin'] = data["admin"]
        return True, message

    def register(self, form):
        userid = form.userid.data
        user = self.db.get_user(userid)
        if user:
            return False, "Repeated user ID"
        else:
            return self.db.insert(form)
            # return False

    # def check_id(self, user_id):
    #     return True
