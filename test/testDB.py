import boto3
from YourChef.credentials import region, aws_id, aws_key

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

# table = dynamodb.Table('testUser')
# table.put_item(
#     Item={
#         'id': 2,
#         'password': 'xxxxxx',
#         'username': 'cindy',
#         'email': 'xc@cu.edu',
#     }
# )
# dynamodb.drop_table('testUser')
