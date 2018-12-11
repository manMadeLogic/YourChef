from YourChef.gmHelper import MapHelper


class RestaurantHelper:
    def __init__(self):
        self.gm = MapHelper()

    def get_restuarant_info(self, restuarant_name, latitude, longitude):
        address = self.gm.get_restuarant_info(restuarant_name, latitude, longitude)
        if address == "":
            return False, "Invalid"
        return address
