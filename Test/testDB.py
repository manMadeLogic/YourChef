import boto3

#from YourChef.credentials import region, aws_id, aws_key
# from Test.SampleUser import users
# from passlib.hash import sha256_crypt
# import argparse

# from YourChef.dishHelper import DishHelper
# from Test.SampleManageDish import dishes
import os
import decimal
# from YourChef.userHelper import UserHelper


# class arguments:
#     def __init__(self, name='RegisterInfo'):
#         parser = argparse.ArgumentParser(description='Process some integers.')
#         parser.add_argument('--aws_region', type=str, default = "us-east-2",
#                             help='the aws access region')
#         parser.add_argument('--aws_id', type=str, default = "",
#                             help='the aws access id')
#         parser.add_argument('--aws_key', type=str, default = "",
#                             help='the aws access key')
#         args = parser.parse_args()
#         self.region = args.aws_region
#         self.aws_id = args.aws_id
#         self.aws_key = args.aws_key
#
# if __name__ == '__main__':
#     args = arguments()
#     dynamodb = boto3.resource('dynamodb', region_name=args.region, aws_access_key_id=args.aws_id, aws_secret_access_key=args.aws_key)
#
    # table = dynamodb.create_table(
    #     TableName='test_user',
    #     KeySchema=[
    #          {'AttributeName': 'userid', 'KeyType': 'HASH'},
    #     ],
    #     AttributeDefinitions=[
    #         {'AttributeName': 'userid', 'AttributeType': 'S'}
    #     ],
    #     ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    # )
#     # Wait until the table exists.
#     table.meta.client.get_waiter('table_exists').wait(TableName='test_user')
#     print('created table {}.'.format('test_user'))
#
#
#     for user in users:
#         response = table.put_item(
#             Item={
#                 'email': user["email"],
#                 'userid': user["userid"],
#                 'password': sha256_crypt.encrypt(str(user["password"])),
#                 'username': user["username"]
#             }
#         )
#         if response:
#             print(user['userid']+" saved")
#         else:
#             print(user['userid'] + " save fail")



# from YourChef.orderHelper import OrderHelper
if __name__ == '__main__':
    # db = UserHelper("test_user")

    # response = db.table.scan()
    # if response['Items']:
    #     for i in response['Items']:
    #         print(i)

    region = os.environ.get('region')
    aws_id = os.environ.get('Access_key_ID')
    aws_key = os.environ.get('Secret_access_key')
    dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
    # # table = dynamodb.Table('test_dish')
    # table = dynamodb.create_table(
    #     TableName='Order',
    #     # TableName='order_test',
    #     KeySchema=[
    #         {'AttributeName': 'restaurant', 'KeyType': 'HASH'},
    #         # {'AttributeName': 'userid', 'KeyType': 'HASH'},
    #         {'AttributeName': 'date', 'KeyType': 'RANGE'}
    #     ],
    #     AttributeDefinitions=[
    #         {'AttributeName': 'restaurant', 'AttributeType': 'S'},
    #         # {'AttributeName': 'userid', 'AttributeType': 'S'},
    #         {'AttributeName': 'date', 'AttributeType': 'S'}
    #     ],
    #     ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    # )

    session = dict()
    session['dishes'] = [['a', 10, 1]]
    session['total_dishes'] = 1
    session['total'] = 1.0
    session['restaurant'] = 'a'
    # server = OrderHelper('test_dish2')
    finished = False
    userid = 'xc'

    table = dynamodb.Table('Order')
    response = table.put_item(
        Item={
            'restaurant': session['restaurant'],
            'date': '2018-12-13T19:42:44+00:00',
            'dishes': session['dishes'],
            'total': decimal.Decimal(session['total']),
            'userid': userid,
            'finished': finished
        }
    )
    if response:
        print("success")
    else:
        print("fail")

    # server = DishHelper('test_dish2')
    # for dish in dishes:
    #     print(dish)
    #     result, message = server.add_dish(dish['restaurant'], dish['dishname'], dish['price'])
    #     print(result, message)

    # print(server.table_name_ManageDish)
    # response = server.table.scan()
    # if response['Items']:
    #     for i in response['Items']:
    #         print(i)

    #
    # db.delete_user("lt6666")
    # db.delete_user("xc-6666")
    # db.delete_user("xc6666")