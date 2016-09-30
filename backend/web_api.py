import web
import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils import setup_environment
from controllers.login import LoginController
from controllers.update import UpdateLeadController

urls = (
    '/login',  'LoginController',
    '/update', 'UpdateLeadController'
)

app = web.application(urls, globals())

wsgi = app.wsgifunc()

def main():
    setup_environment()
    app.run()

if __name__ == '__main__':
    main()
