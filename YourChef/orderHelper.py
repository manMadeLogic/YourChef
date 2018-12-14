import boto3
from boto3.dynamodb import conditions
import os
import datetime
import decimal


class OrderHelper:
    def __init__(self, name="Order"):
        self.table_name_ManageDish = name
        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')
        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_ManageDish)

    def add_order(self, restaurant, dishes, total, userid):
        if not restaurant or dishes is None or not total or not userid:
            return False, "Insert Fail"

        response = self.table.put_item(
            Item={
                'restaurant': restaurant,
                'date': datetime.datetime.now().isoformat(),
                'dishes': str(dishes),
                'total': decimal.Decimal(str(total)),
                'userid': userid,
                'finished': False
            }
        )
        if response:
            return True, "Success"
        else:
            return False, "Insert Fail"

    def update(self, restaurant, date):
        response = self.table.update_item(
            Key={
                'userid': restaurant,
                'date': date
            },
            UpdateExpression="set finished = :f",
            ExpressionAttributeValues={
                ':f': True
            },
            ReturnValues="UPDATED_NEW"
        )

        if response:
            return True
        else:
            return False

    def get_order(self, restaurant, date):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant) & conditions.Key('title').eq(date)
        )
        if response['Items']:
            order = response['Items'][0]
            return order, "Success"
        else:
            return None, "No order."
