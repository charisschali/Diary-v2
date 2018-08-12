from datetime import timedelta
from flask_restful import Resource, reqparse
from app.models import User
from app.security import token_required, encode_auth_token

class SingUp(Resource):
    """
        This is resource used to register new users
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username',
                                 type=str, required=True,
                                 help='username is required!'
                                )
        self.parser.add_argument('email',
                                 type=str, required=True,
                                 help="Email is required"
                                )
        self.parser.add_argument('password',
                                 type=str, required=True,
                                 help="password is required"
                                )
        self.parser.add_argument('confirm_password',
                                 type=str, required=True,
                                 help="confirm Password is required"
                                )
    def post(self):
        """ Register a new user """
        data = self.parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        if not len(password) >= 8:
            return{"message":"Password length should altest 8 characters"}, 401
        if not password == confirm_password:
            return {"message":"Double check your password"}, 400
        user = User().get_user_by_email(email)
        if email in str(user):
            return{"message":'User with email: {} exists'.format(email)}, 400
        else:
            new_user = (username, email, password)
            User().save(new_user)
            return{"message":"Your Account was created"}, 201

class Login(Resource):
    """
        This is resource used to login existing users
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email',
                                 type=str, required=True,
                                 help='email is required!'
                                )
        self.parser.add_argument('password',
                                 type=str, required=True,
                                 help="Password is required"
                                )
    def post(self):
        """ This method logins the user and creates an access token """
        data = self.parser.parse_args()
        email = data['email']
        password = data['password']
        db_email = User().match_email(email)
        if not db_email:
            return {"message":"User with email:'{}' does not exist".format(email)}, 400
        if User().verify_password(email, password):
            user_id = User().get_id_by_email(email)
            access_token = encode_auth_token(user_id)
            print(access_token)
            return {"message":"you logged in successfully","token":access_token}, 200
        return {"message":"Your password was Incorrect, please double check it."}, 400
