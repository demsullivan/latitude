import boto3
import json
import logging
import os
import threading
from dotenv import load_dotenv, find_dotenv

from utils import find_class
import stores.dynamodb as store
from stores import seed

logger = logging.getLogger('latitude')
store_lock = threading.Lock()

class SourceAggregatorThread(threading.Thread):
    def __init__(self, source):
        self.parser = find_class(source.parser)()
        self.params = json.loads(source.params)
        self.source = source
        super(SourceAggregatorThread, self).__init__()

    def run(self):
        leads = self.parser.get_lead_list(self.source, self.params)
        logger.debug('Received {} leads from {}'.format(len(leads), self.source.source_name))

        for lead in leads:
            store_lock.acquire()
            store.create_lead(lead)
            store_lock.release()

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

def seed_db():
    setup_environment()
    store.seed_db(seed.seeds())

def aggregate_leads():
    threads = []
    for source in store.all_sources():
        thread = SourceAggregatorThread(source)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    setup_environment()
    aggregate_leads()

# Main Lambda entry-point
def lambda_entrypoint(event, context):
    main()

if __name__ == '__main__':
    main()
