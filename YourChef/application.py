from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from wtforms import Form, StringField, PasswordField, validators

from YourChef.menu import MenuHelper
from YourChef.registration import RegistrationHelper
from YourChef.restaurant import RestaurantHelper


application = Flask(__name__)
application.config['SECRET_KEY'] = 'yourchef'
application.config['SESSION_TYPE'] = 'filesystem'

server_register = RegistrationHelper()
server_menu = MenuHelper()
server_restaurant = RestaurantHelper()


class RegisterForm(Form):
    userid = StringField('userid', [validators.Length(min=1, max=50)])
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


def logged_in():
    return 'logged_in' in session


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if logged_in():
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


@application.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('You are already logged in', 'success')
        return redirect("/")
    if request.method == 'POST':
        user, err_message = server_register.login(request.form)
        if user:  # result > 0
            # Passed
            flash('You are now logged in', 'success')
            session['logged_in'] = True
            session['is_restaurant'] = False
            session['user_name'] = user["username"]
            session['user_id'] = user["userid"]

            session['dishes'] = []
            session['total_dishes'] = 0
            session['total'] = 0.0
            return redirect("/")
        else:
            error = err_message
            return render_template('login.html', error=error)
    return render_template('login.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        result, message = server_register.register(form)
        if result:
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')

    return render_template('register.html', form=form)


@application.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@application.route('/get_dish_in_cart', methods=['POST'])
def get_dish_in_cart():
    if logged_in():
        # print(session['dishes'])
        return jsonify({"dishes":session['dishes'], "total":session["total"]})
    else:
        return jsonify(None)


@application.route('/clear_cart', methods=['POST'])
@is_logged_in
def clear_cart():
    session['dishes'] = []
    session['total_dishes'] = 0
    session['total'] = 0.0
    # session['restaurant']
    return jsonify(True)


@application.route('/check_out')
@is_logged_in
def check_out():
    # todo save order
    session['dishes'] = []
    session['total_dishes'] = 0
    session['total'] = 0.0
    # session['restaurant']
    flash('Successfully placed order', 'success')
    return redirect("/")


@application.route('/add_dish', methods=['POST'])
def add_dish():
    # todo guest cart
    amount = 1
    restaurant = request.values.get('restaurant')
    dish_id = request.values.get('dish_id')
    return jsonify(server_menu.add_to_cart(session, restaurant, dish_id, amount))


@application.route('/manageDish/<string:restaurant>', methods=['GET', 'POST'])
def manageDish(restaurant):
    if session['is_restaurant']:
        restaurant = session['restaurant']
    # else:
    # todo
    # redirect("/")
    dishes = server_menu.getDish(restaurant)
    if request.method == 'POST':
        valid, message = server_menu.addDish(restaurant, request.form)
        if valid is False:
            flash(message, 'danger')
        else:
            flash('Successfully added', 'success')
        dishes = server_menu.getDish(restaurant)

    return render_template("manageDish.html", dishes=dishes)


@application.route('/restaurantRegister', methods=['GET', 'POST'])
def resgister_restaurant():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        result, message = server_restaurant.register(form)
        if result:
            session['restaurant'] = form['userid']
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login_restaurant'))
        else:
            flash(message, 'danger')

    return render_template('restaurant_register.html', form=form)




@application.route('/restaurantLogin', methods=['GET', 'POST'])
def login_restaurant():
    # if 'logged_in' in session:
    #     flash('You are already logged in', 'success')
    #     return redirect("/")
    if request.method == 'POST':
        user, err_message = server_restaurant.login(request.form)
        if user:  # result > 0
            # Passed
            flash('You are now logged in', 'success')
            session['logged_in'] = True
            session['is_restaurant'] = True
            session['restaurant'] = user['userid']
            # session['user_name'] = user["username"]
            # session['user_id'] = user["userid"]
            # session['dishes'] = []
            # session['total_dishes'] = 0
            # session['total'] = 0.0
            restaurant = user['userid']
            if server_restaurant.find_location(restaurant):
                return redirect("/manageDish/"+restaurant)
                # redirect("/manageDish/"+restaurant)
            # return redirect("/")
            else:
                return redirect(url_for('location'))

        else:
            error = err_message
            return render_template('restaurant_login.html', error=error)
    return render_template('restaurant_login.html')

@application.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        restuarant_name = request.form['restuarant_name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']


        address = server_restaurant.get_restuarant_info(restuarant_name,latitude,longitude)
        restaurant = session['restaurant']
        server_restaurant.save_restaurant_info(restaurant, restuarant_name, address)

        if address!="Zero Result":
            flash(address, 'success')
            return redirect("/manageDish/"+restaurant)
        else:
            flash('Get address fail! Please try again', 'danger')

    return render_template('location.html')


@application.route('/delete_dish/<string:restaurant>')
def delete_dish(restaurant):
    if session['is_restaurant']:
        restaurant = session['restaurant']
    # else:
    # todo
    #     redirect("/")

    dishname = request.values.get('dishname')
    result = server_menu.deleteDish(restaurant, dishname)
    if result:
        flash('deleted dish ' + dishname, "success")
    else:
        flash('delete dish ' + dishname + " fail", "danger")
    return redirect("/manageDish/"+restaurant)


@application.route('/menu/<string:restaurant>')
def menu(restaurant):
    if not server_restaurant.find_restaurant(restaurant):
        return render_template("menu.html", error="invalid restaurant")
    session['restaurant'] = restaurant
    dishes = server_menu.getDish(restaurant)
    # print (dishes)
    return render_template("menu.html", restaurant=session['restaurant'], dishes=dishes)


@application.route('/')
# @application.route("/home")
def index():
    return render_template("home.html")
    # return render_template('radio.group.html')


@application.route('/quick_fix')
def quick_fix():
    result = server_restaurant.get_restaurant_list()
    flash('Urgent Quick Fix\n' + str(result), "success")
    return render_template("home.html")


if __name__ == '__main__':
    application.run(debug=True)
