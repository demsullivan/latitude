import boto3

from .models import Source, Lead

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

def destroy():
    dynamodb.Table('Source').delete()
    dynamodb.Table('Lead').delete()

def initialize():
    leads_table = dynamodb.create_table(
        TableName='Lead',
        KeySchema=[
            {
                'AttributeName': 'lead_url',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'date_created',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'lead_url',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'date_created',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    sources_table = dynamodb.create_table(
        TableName='Source',
        KeySchema=[{
            'AttributeName': 'source_name',
            'KeyType': 'HASH'
        }],
        AttributeDefinitions=[{
            'AttributeName': 'source_name',
            'AttributeType': 'S'
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

def put_item(table, item, condition=None):
    dynamodb.Table(table).put_item(
        Item=dict(item),
        ConditionExpression=condition
    )

def create_lead(lead):
    put_item('Lead', lead._asdict(), "attribute_not_exists(url) and attribute_not_exists(date_created)")

def create_source(source):
    put_item('Source', source._asdict(), "attribute_not_exists(source_name)")

def all_sources():
    response = dynamodb.Table('Source').scan()
    if response.has_key('Items'):
        return map(lambda item: Source(**item), response['Items'])
    else:
        return []
