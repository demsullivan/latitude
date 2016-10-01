import boto3
import logging
import os
from decimal import Decimal

from .models import Source, Lead, User
from utils import create_password

print "ENDPOINT URL: {}".format(os.environ.get('AWS_DYNAMODB_ENDPOINT_URL'))
dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ.get('AWS_DYNAMODB_ENDPOINT_URL', None))
logger = logging.getLogger('latitude.dynamodb')

model_keys = {
    'Source': 'source_name',
    'Lead':   'lead_url',
    'User':   'email'
}

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

    kwargs = { 'Item': dict(item) }
    if condition is not None:
        kwargs['ConditionExpression'] = condition

    try:
        dynamodb.Table(table).put_item(**kwargs)
    except Exception, e:
        logger.error("Error creating {}: {}".format(table, str(e)))
        pass

########## CREATE METHODS ##########
def create_lead(lead):
    put_item('Lead', lead._asdict(), "attribute_not_exists(lead_url) and attribute_not_exists(date_created)")

def create_source(source):
    put_item('Source', source._asdict(), "attribute_not_exists(source_name)")

def create_user(**kwargs):
    kwargs['password'] = create_password(kwargs['password'])
    put_item('User', kwargs, "attribute_not_exists(email)")

########## READ METHODS ##########
def get_item(model, key):
    logger.debug("Retrieving key {} of model {} from db".format(key, model.__name__))
    response = dynamodb.Table(model.__name__).get_item(Key=key)

    item = {}

    for k, v in response['Item'].items():
        if isinstance(v, Decimal):
            v = int(v)
        item[k] = v

    return model(**item)

def all(model):
    response = dynamodb.Table(model.__name__).scan()
    if response.has_key('Items'):
        return map(lambda item: model(**item), response['Items'])
    else:
        return []

########## UPDATE METHODS ##########
def update(obj):
    put_item(obj.__class__.__name__, obj._asdict())

def delete_by_key(model, **key):
    dynamodb.Table(model.__name__).update_item(
        Key=key,
        UpdateExpression="set deleted = :d",
        ExpressionAttributeValues={ ':d': True }
    )
