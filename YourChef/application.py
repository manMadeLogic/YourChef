from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from wtforms import Form, StringField, PasswordField, validators

from YourChef.menu import MenuHelper
from YourChef.registration import RegistrationHelper
from YourChef.restaurant import RestaurantHelper
# from YourChef.sortByDistance import sort_restaurant
from YourChef.user_profile import UserProfileDBHelper

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yourchef'
application.config['SESSION_TYPE'] = 'filesystem'

server_register = RegistrationHelper()
server_menu = MenuHelper()
server_restaurant = RestaurantHelper()
server_user_profile = UserProfileDBHelper()


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
@application.route('/restaurantLogin', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('You are already logged in', 'success')
        return redirect("/")
    route = request.path
    if route == '/login':
        user_type = 'User'
        method = server_register.login
    else:
        user_type = 'Restaurant'
        method = server_restaurant.login

    if request.method == 'POST':
        user, err_message = method(request.form)
        if user:  # result > 0
            # Passed
            flash('You are now logged in', 'success')
            session['logged_in'] = True
            session['username'] = user["username"]
            session['userid'] = user["userid"]

            if route == '/login':
                session['dishes'] = []
                session['total_dishes'] = 0
                session['total'] = 0.0
                session['is_restaurant'] = False
                return redirect("/")
            else:
                session['is_restaurant'] = True
                restaurant = user['userid']
                if server_restaurant.find_location(restaurant):
                    return redirect("/manageDish")
                else:
                    return redirect(url_for('location'))
        else:
            flash(err_message, 'danger')
            return render_template('login.html', type=user_type)
    return render_template('login.html', type=user_type)


@application.route('/register', methods=['GET', 'POST'])
@application.route('/restaurantRegister', methods=['GET', 'POST'])
def register():
    if logged_in():
        return redirect("/")
    form = RegisterForm(request.form)
    route = request.path
    if route == '/register':
        user_type = 'User'
        method = server_register.register
        redirect_url = '/login'
    else:
        user_type = 'Restaurant'
        method = server_restaurant.register
        redirect_url = '/restaurantLogin'
    if request.method == 'POST' and form.validate():
        result, message = method(form)
        if result:
            flash('You are now registered and can log in', 'success')
            return redirect(redirect_url)
        else:
            flash(message, 'danger')
    return render_template('register.html', form=form, type=user_type)


@application.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    print(url_for('login'))
    return redirect('/')


@application.route('/get_dish_in_cart', methods=['POST'])
def get_dish_in_cart():
    if logged_in() and not session['is_restaurant']:
        # print(session['dishes'])
        return jsonify({"dishes": session['dishes'], "total": session["total"]})
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


@application.route('/manageDish', methods=['GET', 'POST'])
@is_logged_in
def manageDish():
    if session['is_restaurant']:
        restaurant = session['userid']
    else:
        return redirect("/")
    dishes = server_menu.getDish(restaurant)
    if request.method == 'POST':
        valid, message = server_menu.addDish(restaurant, request.form)
        if valid is False:
            flash(message, 'danger')
        else:
            flash('Successfully added', 'success')
        dishes = server_menu.getDish(restaurant)

    return render_template("manageDish.html", dishes=dishes)


@application.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        restuarant_name = request.form['restuarant_name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        address = server_restaurant.get_restuarant_info(restuarant_name, latitude, longitude)
        restaurant = session['userid']
        server_restaurant.save_restaurant_info(restaurant, restuarant_name, address)

        if address != "Zero Result":
            flash(address, 'success')
            return redirect("/manageDish")
        else:
            flash('Get address fail! Please try again', 'danger')

    return render_template('location.html')


@application.route('/profile', methods=['GET', 'POST'])
@is_logged_in
def profile():
    # todo pass form
    if request.method == 'POST':
        # print("Here")
        # print(request.form)
        # salt = request.form['salt']
        # sour = request.form['sour']
        # sweet = request.form['sweet']
        # spicy = request.form['spicy']

        userid = session['userid']
        # print(salt, sour, sweet, spicy, userid)
        result, message = server_user_profile.insert(request.form, userid)
        if result:
            flash("Profile Updated", 'success')
        else:
            flash(message, 'danger')

        # address = server_restaurant.get_restuarant_info(restuarant_name, latitude, longitude)
        # restaurant = session['userid']
        # server_restaurant.save_restaurant_info(restaurant, restuarant_name, address)
        #
        # if address != "Zero Result":
        #     flash(address, 'success')
        #     return redirect("/manageDish")
        # else:
        #     flash('Get address fail! Please try again', 'danger')

    return render_template('profile.html', type='User')


@application.route('/delete_dish')
@is_logged_in
def delete_dish():
    if session['is_restaurant']:
        restaurant = session['restaurant']
    else:
        return redirect("/")

    dishname = request.values.get('dishname')
    result = server_menu.deleteDish(restaurant, dishname)
    if result:
        flash('deleted dish ' + dishname, "success")
    else:
        flash('delete dish ' + dishname + " fail", "danger")
    return redirect("/manageDish")


@application.route('/menu/<string:restaurant>')
def menu(restaurant):
    if not server_restaurant.find_restaurant(restaurant):
        return render_template("menu.html", error="invalid restaurant")
    session['restaurant'] = restaurant
    dishes = server_menu.getDish(restaurant)
    # print (dishes)
    return render_template("menu.html", restaurant=session['restaurant'], dishes=dishes)


def get_restaurant_list():
    restaurants = server_restaurant.get_restaurant_list()
# todo still a lot of discussion
    if logged_in():
        # server = UserProfileDBHelper
        user_profile = server_user_profile.get_user(session['userid'])
        print(user_profile)
        # if user_profile:
        #     # todo sort
        #     restaurants = sort_restaurant(restaurants, user_profile)
    return restaurants


@application.route('/')
# @application.route("/home")
def index():
    result = get_restaurant_list()
    return render_template("home.html", restaurant=result)
    # return render_template('radio.group.html')


@application.route('/quick_fix')
def quick_fix():
    result = server_restaurant.get_restaurant_list()
    flash('Urgent Quick Fix\n' + str(result), "success")
    return render_template("home.html")


if __name__ == '__main__':
    application.run(debug=True)
