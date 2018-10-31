import boto3
from YourChef.credentials import region, aws_id, aws_key
from Test.SampleUser import users
from passlib.hash import sha256_crypt


dynamodb = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)

table = dynamodb.create_table(
    TableName='test_user',
    KeySchema=[
         {'AttributeName': 'userid', 'KeyType': 'HASH'},
    ],
    AttributeDefinitions=[
        {'AttributeName': 'userid', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)
# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='test_user')
print('created table {}.'.format('test_user'))


for user in users:
    response = table.put_item(
        Item={
            'email': user["email"],
            'userid': user["userid"],
            'password': sha256_crypt.encrypt(str(user["password"])),
            'username': user["username"]
        }
    )
    if response:
        print(user['userid']+" saved")
    else:
        print(user['userid'] + " save fail")
