from YourChef.dishHelper import DishHelper
import re

class ManageDishHelper:
    def __init__(self, db_name="DishInfo"):
        self.db = DishHelper(db_name)

    def addDish(self, restaurant, form):
        dishname = form['dishname']
        price = form['price']
        if re.findall(r'[^a-zA-Z-\s]', dishname) or re.findall('[^A-Za-z0-9_]', restaurant):
            return False, "Can't contain special character."
        if not price or price == "":
            return False, "Price not specified!"
        valid, message = self.db.add_dish(restaurant, dishname, price)
        return valid, message

    def getDish(self, restaurant):
        return self.db.get_dish(restaurant)

    def deleteDish(self, restaurant, dishname):
        return self.db.delete_dish(restaurant, dishname)
