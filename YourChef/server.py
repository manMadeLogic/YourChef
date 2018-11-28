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
    def __init__(self, db_name = "DishInfo"):
        self.db = DishHelper(db_name)

    def addDish(self, restaurant, dishname):
        self.db.add_dish(restaurant, dishname)

    def getDish(self, restaurant):
        return self.db.get_dish(restaurant)
