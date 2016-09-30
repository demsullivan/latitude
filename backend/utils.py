from importlib import import_module
import hashlib
import os
import logging
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger('latitude')

def setup_environment():
    load_dotenv(find_dotenv())

    if os.environ.get('LATITUDE_LOGGING', None):
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
    else:
        logger.addHandler(logging.NullHandler())

def find_class(class_path):
    (module_name, class_name) = class_path.rsplit('.', 1)
    module = import_module(module_name)

    if hasattr(module, class_name):
        return getattr(module, class_name)
    else:
        raise ImportError, "Cannot find class {} in module {}".format(class_name, module_name)

def create_password(password):
    return hashlib.sha512(password).hexdigest()
