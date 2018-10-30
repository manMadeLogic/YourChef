import boto3
from boto3.dynamodb import conditions
from YourChef.credentials import region, aws_id, aws_key

from wtforms import Form, StringField, PasswordField, validators
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
    def __init__(self, name='RegisterInfo'):
        self.table_name_register = name
        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_register)
        # self.response = self.table.scan()
        # self.user_id = len(self.response['Items']) + 1

    def insert(self, form):# name, email, username, password
        email = form.email.data
        username = form.username.data
        password = form.password.data
        userid = form.userid.data
        response = self.table.put_item(
            Item={
                'email': email,
                'userid': userid,
                'password': sha256_crypt.encrypt(str(password)),
                'username': username
            }
        )
        if response:
            return True, "Success"
        else:
            return False, "Insert fail"

    def get_user(self, userid):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('userid').eq(userid)
        )
        if response['Items']:
            user = response['Items'][0]
            print(user)
            return user
        else:
            return None


    def check_password(self, userid, password):
        user = self.get_user(userid)
        if user:
            user_pwd_saved = user['password']
            # print response['Items'][0]['id']
            if sha256_crypt.verify(password, user_pwd_saved):
                return user, "Login success"
            else:
                return None, "Incorrect authentication"
        return None, "User Id not found"
