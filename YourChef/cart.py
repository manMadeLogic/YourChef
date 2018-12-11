
class Cart:
    def __init__(self, session):
        if session["restaurant"]:
            self.restaurant = session["restaurant"]
            self.dishes = session['dishes']
            self.total_dishes = session['total_dishes']
            self.total = session['total']
        else:
            self.restaurant = ""
            self.dishes = []
            self.total_dishes = 0
            self.total = 0.0

    def put_in_session(self, session):
        session["restaurant"] = self.restaurant
        session['dishes'] = self.dishes
        session['total_dishes'] = self.total_dishes
        session['total'] = self.total

    def full(self):
        return self.total_dishes >= 10

    def clear(self):
        self.dishes = []
        self.total_dishes = 0
        self.total = 0.0

    def add(self, restaurant, dishname, amount, price):
        if self.total_dishes >= 10:
            return False

        if restaurant != self.restaurant:
            self.restaurant = restaurant
            self.clear()

        i = 0
        while i < len(self.dishes):
            if dishname == self.dishes[i][0]:
                break
            i += 1
        if i != len(self.dishes):
            # print(i)
            self.dishes[i][2] += amount
        else:
            self.dishes.append([dishname, price, amount])
        # print("end ", restaurant, dish_id, session['dishes'], self.total_dishes)
        self.total_dishes += 1
        return True
