import web
import urlparse
import boto3
import hashlib
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
users = dynamodb.Table('User')

def authenticate(user, username, password):
    return user['email'] == username and user['password'] == create_password(password)

def create_password(password):
    return hashlib.sha512(password).hexdigest()

class Login(object):
    def POST(self):
        web.header('Access-Control-Allow-Origin', 'http://localhost:4201')
        web.header('Access-Control-Allow-Credentials', 'true')
        params = web.input()

        try:
            response = users.get_item(
                Key={ 'email': params.username }
            )
        except ClientError as e:
            return web.internalerror(message=str(e))
        else:
            user = response['Item']

            if authenticate(user, params.username, params.password):
                return json.dumps(dict(aws_access_key_id=user['aws_access_key_id'], aws_secret_access_key=user['aws_secret_access_key']))

        return web.unauthorized()

def create_user(email, password, aws_access_key_id, aws_secret_access_key):
    users.put_item(
        Item=dict(
            email=email,
            password=create_password(password),
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        ),
        ConditionExpression="attribute_not_exists(email)"
    )

def main():
    urls = (
        '/login', 'Login'
    )
    app = web.application(urls, globals())
    app.run()

if __name__ == '__main__':
    main()
