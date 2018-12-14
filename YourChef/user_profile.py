import boto3
from boto3.dynamodb import conditions

import os


class UserProfileDBHelper:
    def __init__(self, name='UProfile'):  # RProfile UProfile
        self.table_name_register = name

        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')

        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_register)

    def insert(self, form):
        userid = form.userid.data
        salt = form.salt.data
        sour = form.sour.data
        sweet = form.sweet.data
        spicy = form.spicy.data

        response = self.table.put_item(
            Item={
                'userid': userid,
                'spicy': spicy,
                'salt': salt,
                'sour': sour,
                'sweet': sweet
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

    def delete_user(self, userid):
        response = self.table.delete_item(
            Key={'userid': userid}
        )
        if response:
            return True
        else:
            return False

    def update_flavor(self, userid, salt, sour, sweet, spicy):
        response = self.table.update_item(
            Key={
                'userid': userid,
            },
            UpdateExpression="set salt = :salt, sour = :sour, sweet = :sweet, spicy = :spicy",
            ExpressionAttributeValues={
                ':salt': salt,
                ':sour': sour,
                ':sweet': sweet,
                ':spicy': spicy
            },
            ReturnValues="UPDATED_NEW"
        )

        if response:
            return True
        else:
            return False
