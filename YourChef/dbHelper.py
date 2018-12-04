import boto3
from boto3.dynamodb import conditions
import os
import re


class DishHelper:
    def __init__(self, name = "DishInfo"):
        self.table_name_ManageDish = name
        region = os.environ.get('region')
        aws_id = os.environ.get('Access_key_ID')
        aws_key = os.environ.get('Secret_access_key')
        dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
        self.table = dynamodb.Table(self.table_name_ManageDish)

    def add_dish(self, restaurant, form):

        # dishname = form.dishname.data
        dishname = form['dishname']
        price = form['price']
        if re.findall(r'[^a-zA-Z-\s]', dishname) or re.findall('[^A-Za-z0-9_]', restaurant):
            return False, "Can't contain special character."

        # todo price

        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant)
        )
        if response['Items'] is None:
            return False, "Restaurant does not exist."

        for i in response['Items']:
            if i['dishname'] == dishname:
                return False, "DishName already added."

        # print("[" + price + "]")
        response = self.table.put_item(
            Item={
                'restaurant': restaurant,
                'dishname': dishname,
                'price': price
            }
        )
        if response:
            return True, "Success"
        else:
            return False, "Insert fail"

    def delete_dish(self, restaurant, dishname):
        response = self.table.delete_item(
            Key={'restaurant': restaurant, 'dishname': dishname}
        )
        if response:
            return True
        else:
            return False


    def get_dish(self, restaurant):
        response = self.table.query(
            KeyConditionExpression=conditions.Key('restaurant').eq(restaurant)
        )
        dishes = []
        if response['Items']:
            for i in response['Items']:
                dishes.append(i['dishname'] + '$' + str(i['price']))
            return dishes
        else:
            return None