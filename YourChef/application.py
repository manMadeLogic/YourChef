from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from wtforms import Form, StringField, PasswordField, validators

from YourChef.server import RegistrationHelper

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yourchef'
application.config['SESSION_TYPE'] = 'filesystem'

server = RegistrationHelper()


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


@application.route('/')
# @application.route("/home")
def index():
    return render_template("home.html")
    # return render_template('radio.group.html')


if __name__ == '__main__':
    application.run(debug=True)
