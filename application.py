from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
application = Flask(__name__)

from Articles import posts

@application.route('/')
@application.route("/home")
def index():
    return render_template("home.html", posts=posts)
    # return render_template('radio.group.html')

if __name__ == '__main__':
    application.run(debug=True)
