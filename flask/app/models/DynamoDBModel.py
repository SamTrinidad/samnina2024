import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

class DynamoDBModel:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb',
            endpoint_url=os.getenv('AWS_DYNAMODB_ENDPOINT'),
            region_name=os.getenv('AWS_DEFAULT_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def put_item(self, item):
        self.table.put_item(Item=item)

    def update_item(self, key, update_expression, expression_attribute_values):
        self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

    def delete_item(self, key):
        self.table.delete_item(Key=key)

    def query_items(self, key_condition_expression):
        response = self.table.query(KeyConditionExpression=key_condition_expression)
        return response.get('Items')
