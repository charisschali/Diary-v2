from functools import wraps
from flask import request, current_app
import datetime
import jwt


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token =jwt.encode(payload, str(current_app.config.get('SECRET_KEY')),algorithm='HS256')
        return token.decode()
    except Exception as e:
        return e



def token_required(func):
    '''checks if the user is authenticated'''
    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                access_token = authorization_header.split(' ')[1]
            if access_token:
                payload = jwt.decode(access_token, str(current_app.config.get("SECRET_KEY")))
                user_id = payload['sub']
                return func(user_id=user_id, *args, **kwargs)
        except jwt.ExpiredSignatureError:
                return {"message":"Token has expired. Please login again"}, 400

        except jwt.InvalidTokenError:
            return{"message":"Invalid token"}, 400

    return decorated
