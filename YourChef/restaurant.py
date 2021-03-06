from YourChef.restaurant_register import RestaurantDBHelper
from YourChef.gmHelper import MapHelper
import re


class RestaurantHelper:
    def __init__(self, db_name="RestaurantInfo"):
        self.db = RestaurantDBHelper(db_name)
        self.gm = MapHelper()

    def find_restaurant(self, restaurant):
        # user = self.db.get_user(restaurant)
        return self.db.get_user(restaurant)

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

    def find_location(self, restaurant):
        address = self.db.find_location(restaurant)
        # print (address)
        if address and 'address' in address:
            return True
        else:
            return False

    def get_restuarant_info(self, restuarant_name, latitude, longitude):
        address = self.gm.get_restuarant_info(restuarant_name, latitude, longitude)
        if address == "":
            return False, "Invalid"
        return address['formatted_address']

    def get_restaurant_list(self):
        return self.db.get_all()

    def save_restaurant_info(self, restaurant_id, restuarant_name, address):
        return self.db.update_address(restaurant_id, restuarant_name, address)
