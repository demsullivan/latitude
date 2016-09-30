import boto3
import json
import logging
import os
from dotenv import load_dotenv, find_dotenv

from utils import find_class
import stores.dynamodb as store
from stores import seed

logger = logging.getLogger('latitude')

def setup_environment():
    load_dotenv(find_dotenv())

    if os.environ.get('LATITUDE_LOGGING', None):
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
    else:
        logger.addHandler(logging.NullHandler())

def initialize():
    setup_environment()
    store.initialize(seeds=seed.seeds())

def aggregate_leads():
    parsers = {}

    for source in store.all_sources():
        logger.info('Processing source {}'.format(source.source_name))

        if not parsers.has_key(source.parser):
            parsers[source.parser] = find_class(source.parser)()

        parser = parsers[source.parser]
        params = json.loads(source.params)

        leads = parser.get_leads(source, **params)
        logger.debug('Received {} leads from {}'.format(len(leads), source.source_name))

        for lead in leads:
            store.create_lead(lead)

def main():
    setup_environment()
    aggregate_leads()

# Main Lambda entry-point
def lambda_entrypoint(event, context):
    main()

if __name__ == '__main__':
    main()
