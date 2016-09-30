from __future__ import absolute_import
import web
import json
import os
from botocore.exceptions import ClientError

from stores.models import User
from controllers.application import ApplicationController
from ..utils import create_password

class LoginController(ApplicationController):
    def authenticate(self, user, username, password):
        return user.email == username and user.password == create_password(password)

    def serialized_user(self, user):
        blacklist_fields = ['password']
        return json.dumps(dict([(k, v) for k, v in user._asdict().items() if k not in blacklist_fields]))

    def POST(self):
        super(LoginController, self).POST()
        params = web.input()

        try:
            user = self.store.get_item(User, dict(email=params.username))
        except ClientError as e:
            raise
            return web.internalerror(message=str(e))

        if self.authenticate(user, params.username, params.password):
            return self.serialized_user(user)

        return web.unauthorized()
