import boto3
from boto3.dynamodb import conditions
import os
import datetime
import decimal


class OrderHelper:
    def __init__(self, name="Order", user='User_order'):
        self.table_name_ManageDish = name
        self.table_name_user = user
        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')
        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id,
                                  aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_ManageDish)
        self.user_table = dynamodb.Table(self.table_name_user)

    def add_order(self, restaurant, dishes, total, userid):
        if not restaurant or dishes is None or not total or not userid:
            return None, "Insert Fail"

        date_str = datetime.datetime.now().isoformat()

        for dish in dishes:
            dish[1] = decimal.Decimal(str(dish[1]))

        response = self.table.put_item(
            Item={
                'restaurant': restaurant,
                'date': date_str,
                'dishes': dishes,
                'total': decimal.Decimal(str(total)),
                'userid': userid,
                'finished': False
            }
        )

        if response:
            order_return, message = self.get_order(restaurant, date_str)
            if order_return:
                # print(order)
                response = self.user_table.put_item(
                    Item={
                        'user': userid,
                        'date': date_str,
                        'restaurant': restaurant
                    }
                )
                if response:
                    return order_return, "Success"
                else:
                    return None, "Insert User Order Fail"
            else:
                return None, message
        else:
            return None, "Insert Restaurant Order Fail"

    def update(self, restaurant, date):
        response = self.table.update_item(
            Key={
                'restaurant': restaurant,
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
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant) & conditions.Key('date').eq(date)
        )
        if response['Items']:
            order = response['Items'][0]
            return order, "Success"
        else:
            return None, "No order."

    def get_restaurant_order(self, restaurant):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant)
        )
        return response['Items']

    def get_user_order(self, userid):
        response = self.user_table.query(
            KeyConditionExpression=conditions.Key('user').eq(userid)
        )
        result = []
        for user_order in response['Items']:
            order, message = self.get_order(user_order['restaurant'], user_order['date'])
            if order:
                result.append(order)
        return result

