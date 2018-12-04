from YourChef.gmHelper import MapHelper

from YourChef.dbHelper import DishHelper

class RestaurantHelper:
    def __init__(self, db_name="RegisterInfo"):
        self.gm = MapHelper()

    def get_restuarant_info(self, restuarant_name,latitude,longitude):
        address = self.gm.get_restuarant_info(restuarant_name,latitude,longitude)
        if(address == ""):
            return False, "Invalid"
        return address

class ManageDishHelper:
    def __init__(self, db_name="DishInfo"):
        self.db = DishHelper(db_name)

    def addDish(self, restaurant, form):
        valid, message = self.db.add_dish(restaurant, form)
        return valid, message

    def getDish(self, restaurant):
        return self.db.get_dish(restaurant)

    def deleteDish(self, restaurant, dishname):
        return self.db.delete_dish(restaurant, dishname)
