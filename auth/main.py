import web
import urlparse
import boto3
import hashlib
import json
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
users = dynamodb.Table('User')

urls = (
    '/login', 'LoginController'
)

app = web.application(urls, globals())
wsgi = app.wsgifunc()

def create_password(password):
    return hashlib.sha512(password).hexdigest()

class LoginController(object):
    def authenticate(self, user, username, password):
        return user['email'] == username and user['password'] == create_password(password)

    def serialized_user(self, user):
        blacklist_fields = ['password']
        return json.dumps(dict([(k, v) for k, v in user.items() if k not in blacklist_fields]))

    def POST(self):
        web.header('Access-Control-Allow-Origin', os.environ.get('LATITUDE_CORS_ORIGIN', 'http://localhost:4201'))
        web.header('Access-Control-Allow-Credentials', 'true')
        params = web.input()

        try:
            response = users.get_item(Key={ 'email': params.username })
        except ClientError as e:
            return web.internalerror(message=str(e))
        else:
            user = response['Item']

            if self.authenticate(user, params.username, params.password):
                return self.serialized_user(user)

        return web.unauthorized()

def create_user(**kwargs):
    kwargs['password'] = create_password(kwargs['password'])
    users.put_item(
        Item=kwargs,
        ConditionExpression="attribute_not_exists(email)"
    )

def main():
    app.run()

if __name__ == '__main__':
    main()
