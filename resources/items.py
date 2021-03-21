from flask import request
from flask_restful import Resource, reqparse
from models.items import ItemModel
from models.tokens import TokenModel
from models.transfer import TransferModel
from models.user import UserModel


class Item(Resource):
    # it goes into the body of the request and extracts the data.
    parser = reqparse.RequestParser()  # data is in body of request

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        data = parser.parse_args()
        if "token" in request.headers:
            user_token = request.headers['token']
        else:
            return {"message": "The token cannot be left blank!"}, 400

        token = TokenModel.find_by_token(user_token)
        if not token:
            return {"message": "Token is incorrect"}, 500  # internal server error

        if data['name'] == "":
            return {'message': 'The name of item cannot be left blank!'}, 400

        if ItemModel.find_by_name(data['name'], token.user_id):
            return {'message': "An item with name '{}' already exists.".format(data['name'])}, 400

        user_id = token.user_id
        item = ItemModel(data['name'], user_id)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return item.json(), 201  # for created


class ItemDelete(Resource):
    def delete(self, id):
        if "token" in request.headers:
            user_token = request.headers['token']
        else:
            return {"message": "The token cannot be left blank!"}, 400

        token = TokenModel.find_by_token(user_token)
        if not token:
            return {"message": "Token is incorrect"}, 500  # internal server error

        item = ItemModel.delete_from_db(id, token.user_id)
        if item == "false":
              return {'message': "An item with id '{}' does not exist.".format(id)}, 400
        return {'message': 'Item deleted'}


class ItemList(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        if "token" in request.headers:
            user_token = request.headers['token']
        else:
            return {"message": "The token cannot be left blank!"}, 400
        token = TokenModel.find_by_token(user_token)
        if not token:
            return {"message": "Token is incorrect"}, 400
        items = [item.json() for item in ItemModel.find_all(token.user_id)]
        if items:
             return items, 200
        return {"message": "You don't have items"}, 400

class ItemTransfer(Resource):
    parser = reqparse.RequestParser()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',
                            type=int,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        parser.add_argument('login',
                            type=str,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        data = parser.parse_args()
        if "token" in request.headers:
            user_token = request.headers['token']
        else:
            return {"message": "The token cannot be left blank!"}, 400

        token = TokenModel.find_by_token(user_token)
        if not token:
            return {"message": "Token is incorrect"}, 400

        if not ItemModel.find_by_id(data['id'], token.user_id):
            return {'message': "An item with id '{}' does not exist.".format(data['id'])}, 400

        if not UserModel.find_by_login(data['login']):
            return {"message": "A user with that login does not exist"}, 400

        if UserModel.find_by_login(data['login']).id == token.user_id:
            return {"message": "You can not transfer item to yourself"}, 400

        transfer_user = UserModel.find_by_login(data['login']).id
        transfer_item = TransferModel.save_to_db(transfer_user, data['id'])
        if transfer_item == "true":
            return {"message": "Item has already transfered"}, 400

        response = "http://localhost:5000/get?id={0}".format(data['id'])

        return {"message": response}, 200

class ItemAccept(Resource):
    def get(self):
        if "token" in request.headers:
            user_token = request.headers['token']
        else:
            return {"message": "The token cannot be left blank!"}, 400

        token = TokenModel.find_by_token(user_token)
        if not token:
            return {"message": "Token is incorrect"}, 403  # internal server error

        item_id = request.args.get('id')
        if not TransferModel.find_transfer(token.user_id,
                         item_id):
            return {"message": "This link is not available"}, 400

        if ItemModel.transfer(item_id,token.user_id):
            return {"message": "Data transmission error"}, 400

        if TransferModel.delete_transfer(token.user_id,item_id):
            return {"message": "Data deletion error"}, 400

        return {"message":"Data transfer completed successfully!"}, 200
