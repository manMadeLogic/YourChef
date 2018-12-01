from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from wtforms import Form, StringField, PasswordField, validators

from YourChef.server import ManageDishHelper
from YourChef.registration import RegistrationHelper

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yourchef'
application.config['SESSION_TYPE'] = 'filesystem'

server = RegistrationHelper()
server_dish = ManageDishHelper()


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


@application.route('/get_dish_in_cart', methods=['POST'])
def get_dish_in_cart():
    if logged_in():
        # print(session['dishes'])
        return jsonify(session['dishes'])
    else:
        return jsonify(None)


@application.route('/clear_cart', methods=['POST'])
def clear_cart():
    if logged_in():
        # print(session['dishes'])
        session['dishes'] = []
        session['total_dishes'] = 0
        return jsonify(True)


@application.route('/add_dish', methods=['POST'])
def add_dish():
    amount = 1
    restaurant = request.values.get('restaurant')
    dish_id = request.values.get('dish_id')
    return jsonify(add_a_dish(restaurant, dish_id, amount))


def add_a_dish(restaurant, dish_id, amount):
    if session['total_dishes'] >= 10:
        return False

    # print(restaurant, session['restaurant'])
    if restaurant != session['restaurant']:
        session['restaurant'] = restaurant
        # todo
        session['dishes'] = []
        session['total_dishes'] = 0
    # session['restaurant'] = 'b'
    # print(restaurant, dish_id, session['dishes'], session['total_dishes'])
    i = 0
    while i < len(session['dishes']):
        if dish_id == session['dishes'][i][0]:
            break
        i += 1
    if i != len(session['dishes']):
        # print(i)
        session['dishes'][i][1] += amount
    else:
        session['dishes'].append([dish_id, amount])
    # print("end ", restaurant, dish_id, session['dishes'], session['total_dishes'])
    session['total_dishes'] += 1
    return True


@application.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('You are already logged in', 'success')
        return redirect("/")
    if request.method == 'POST':
        # Get Form Fields
        user_id = request.form['userid']
        password = request.form['password']
        user, err_message = server.login(user_id, password)
        if user:  # result > 0
            # Passed
            flash('You are now logged in', 'success')
            session['logged_in'] = True
            session['user_name'] = user["username"]
            session['user_id'] = user["userid"]
            session['dishes'] = []
            session['total_dishes'] = 0
            return redirect("/")
        else:
            error = err_message
            return render_template('login.html', error=error)
    return render_template('login.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if server.register(form):
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Register fail! Please try again', 'fail')

    return render_template('register.html', form=form)
    # return render_template('register.html', form=form)


@application.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



@application.route('/manageDish', methods=['GET', 'POST'])
def manageDish():
    restaurant = "a"
    dishes = server_dish.getDish(restaurant)
    if request.method == 'POST':
        valid, message = server_dish.addDish(restaurant, request.form)
        if valid is False:
            flash(message, 'fail')
        else:
            flash('Successfully added', 'success')
        dishes = server_dish.getDish(restaurant)

    return render_template("manageDish.html", dishes=dishes)


def find_restaurant(restaurant):
    return restaurant == 'a'


@application.route('/menu/<string:restaurant>')
# @application.route("/home")
def menu(restaurant):
    if not find_restaurant(restaurant):
        return render_template("menu.html", error="invalid restaurant")
    session['restaurant'] = restaurant
    dishes = server_dish.getDish(restaurant)
    return render_template("menu.html", restaurant=session['restaurant'], dishes=dishes)

@application.route('/')
# @application.route("/home")
def index():
    return render_template("home.html")
    # return render_template('radio.group.html')


if __name__ == '__main__':
    application.run(debug=True)
