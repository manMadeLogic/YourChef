import base64
import boto3
from boto3.dynamodb import conditions
from credentials import *

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


class RegisterForm(Form):
    userid = StringField('userid', [validators.Length(min=1, max=50)])
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class UserHelper:
    def __init__(self, id = 1):
        self.dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
        self.table = self.dynamodb.Table(table_name_register)
        self.response = self.table.scan()
        self.user_id = len(self.response['Items']) + 1


    def register(self, form):#name, email, username, password
        email = form.email.data
        username = form.username.data
        password = form.password.data
        response = self.table.put_item(
            Item={
                'email': email,
                'userid': self.user_id,
                'password': sha256_crypt.encrypt(str(password)),
                'username': self.username
            }
        )
        if response:
            self.user_id += 1
            return True
        else:
            return False

    def login(self):
        username = request.form['username']
        password = request.form['password']
        response = self.table.query(
            KeyConditionExpression=conditions.Key('username').eq(username)
        )
        if response['Items']:
            user_pwd_saved = response['Items'][0]['password']
            # print response['Items'][0]['id']
            if sha256_crypt.verify(password, user_pwd_saved):
                session['logged_in'] = True
                session['username'] = username
                session['id'] = str(response['Items'][0]['userid'])
                session['name'] = response['Items'][0]['username']
                return True
        return False
