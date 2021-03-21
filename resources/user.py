import uuid
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.tokens import TokenModel
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('login',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_login(data['login']):
            return {"message": "A user with that login already exists"}, 400

        if data['login'] == "":
            return {"message": "The login cannot be left blank!"}, 400

        if data['password'] == "":
            return {"message": "The password cannot be left blank!"}, 400

        user = UserModel(**data)  # data is dict
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in db
        user = UserModel.find_by_login(data['login'])

        # check password
        if user and safe_str_cmp(user.password, data['password']):
            temporary_token = str(uuid.uuid4())
            try:
                token = TokenModel.save_to_db(temporary_token, user.id)
            except:
                return {"message": "An error occurred inserting the token."}, 400

            return {'token': str(token)}, 200

        return {'message': 'Invalid credentials'}, 401
