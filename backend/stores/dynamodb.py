import boto3
import logging
import os

from .models import Source, Lead

dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ.get('AWS_DYNAMODB_ENDPOINT_URL', None))
logger = logging.getLogger('latitude.dynamodb')

def destroy():
    dynamodb.Table('Source').delete()
    dynamodb.Table('Lead').delete()

def initialize(seeds=None):
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

    # if seeds:
    #     for seed in seeds:
    #         if isinstance(seed, Source):
    #             create_source(seed)
    #         elif isinstance(seed, Lead):
    #             create_lead(seed)

def seed_db(seeds):
    for seed in seeds:
        if isinstance(seed, Source):
            create_source(seed)
        elif isinstance(seed, Lead):
            create_lead(seed)

def put_item(table, item, condition=None):
    logger.debug("Creating {} {}".format(table, item))
    try:
        dynamodb.Table(table).put_item(
            Item=dict(item),
            ConditionExpression=condition
        )
    except Exception, e:
        logger.error("Error creating {}: {}".format(table, str(e)))
        pass

def create_lead(lead):
    put_item('Lead', lead._asdict(), "attribute_not_exists(lead_url) and attribute_not_exists(date_created)")

def create_source(source):
    put_item('Source', source._asdict(), "attribute_not_exists(source_name)")

def all_sources():
    response = dynamodb.Table('Source').scan()
    if response.has_key('Items'):
        return map(lambda item: Source(**item), response['Items'])
    else:
        return []
