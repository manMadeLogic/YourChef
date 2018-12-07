from YourChef.dishHelper import DishHelper
import re

class MenuHelper:
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

    def getDishPrice(self, restaurant, dishname):
        dish, message = self.db.get_dish_price(restaurant, dishname)
        return dish

    def deleteDish(self, restaurant, dishname):
        return self.db.delete_dish(restaurant, dishname)

        # todo  cart class
    def add_to_cart(self, session, restaurant, dishname, amount):
        if session['total_dishes'] >= 10:
            return False

        dish = self.getDishPrice(restaurant, dishname)
        if dish:
            price = dish['price']
        else:
            return False

        if restaurant != session['restaurant']:
            session['restaurant'] = restaurant
            session['dishes'] = []
            session['total_dishes'] = 0
        # session['restaurant'] = 'b'
        # print(restaurant, dish_id, session['dishes'], session['total_dishes'])
        i = 0
        while i < len(session['dishes']):
            if dishname == session['dishes'][i][0]:
                break
            i += 1
        if i != len(session['dishes']):
            # print(i)
            session['dishes'][i][2] += amount
        else:
            session['dishes'].append([dishname, price, amount])
        # print("end ", restaurant, dish_id, session['dishes'], session['total_dishes'])
        session['total_dishes'] += 1
        return True
