import boto3
import os

def create_table(table_name):

    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=os.getenv('AWS_DYNAMODB_ENDPOINT'),
        region_name=os.getenv('AWS_DEFAULT_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    return table

if __name__ == '__main__':
    rsvptable = create_table('rsvp')
    print("rsvp table status:", rsvptable.table_status)