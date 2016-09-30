import web
import os
from importlib import import_module

class ApplicationController(object):
    def __init__(self):
        self.store = import_module(os.environ.get('LATITUDE_STORE_PATH', 'stores.dynamodb'))

    def POST(self):
        web.header('Access-Control-Allow-Origin', os.environ.get('LATITUDE_CORS_ORIGIN', 'http://localhost:4201'))
        web.header('Access-Control-Allow-Credentials', 'true')
