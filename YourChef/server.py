from YourChef.gmHelper import MapHelper

from YourChef.dbHelper import UserHelper, DishHelper
import re


class RegistrationHelper:
    def __init__(self, db_name="RegisterInfo"):
        self.db = UserHelper(db_name)
        self.gm = MapHelper()

    def login(self, user_id, password):
        return self.db.check_password(user_id, password)

    def register(self, form):
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
            # return False

    # only for test
    def delete_user(self, user_id):
        return self.db.delete_user(user_id)
    # def check_id(self, user_id):
    #     return True

    def get_restuarant_info(self, restuarant_name,latitude,longitude):
        address = self.gm.get_restuarant_info(restuarant_name,latitude,longitude)
        if(address == ""):
            return False, "Invalid"
        return address

class ManageDishHelper:
    def __init__(self, db_name = "DishInfo"):
        self.db = DishHelper(db_name)

    def addDish(self, restaurant, dishname):
        self.db.add_dish(restaurant, dishname)

    def getDish(self, restaurant):
        return self.db.get_dish(restaurant)
