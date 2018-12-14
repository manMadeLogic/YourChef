import boto3
from boto3.dynamodb import conditions

import os


class RestaurantProfileDBHelper:
    def __init__(self, name='RProfile'):
        self.table_name_register = name

        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')

        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_register)

    # get all todo get all
    def get_all(self):
        response = self.table.scan()
        results = []
        if response['Items']:
            for i in response['Items']:
                print(i)
                results.append(i)
        return results

    def insert(self, form, userid, username):
        response = self.table.put_item(
            Item={
                'userid': userid,
                'username': username,
                'salt': int(form['salt']),
                'sour': int(form['sour']),
                'sweet': int(form['sweet']),
                'spicy': int(form['spicy'])
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
