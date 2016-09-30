from __future__ import absolute_import
import web

from .utils import setup_environment
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
