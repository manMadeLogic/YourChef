import boto3
from boto3.dynamodb import conditions

from passlib.hash import sha256_crypt
import os


class RestaurantDBHelper:
    def __init__(self, name='RestaurantInfo'):
        self.table_name_register = name
        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')
        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_register)

    def insert(self, form):  # name, email, username, password
        email = form.email.data
        username = form.username.data
        password = form.password.data
        userid = form.userid.data
        response = self.table.put_item(
            Item={
                'email': email,
                'userid': userid,
                'password': sha256_crypt.hash(str(password)),
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
            return user
        else:
            return None

    def check_password(self, userid, password):
        user = self.get_user(userid)
        if user:
            user_pwd_saved = user['password']
            if sha256_crypt.verify(password, user_pwd_saved):
                return user, "Login success"
            else:
                return None, "Incorrect authentication"
        return None, "User Id not found"

    def delete_user(self, userid):
        response = self.table.delete_item(
            Key={'userid': userid}
        )
        if response:
            return True
        else:
            return False

    def find_location(self, restaurant):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('userid').eq(restaurant)
        )
        if response['Items']:
            user = response['Items'][0]
            return user
        else:
            return None

    def update_address(self, restaurant, address):
        response = self.table.update_item(
            Key={
                'userid' : restaurant
            },
            UpdateExpression="set address = :a",
            ExpressionAttributeValues={
                ':a' : address
            },
             ReturnValues="UPDATED_NEW"
        )

        if response:
            return True
        else:
            return False
