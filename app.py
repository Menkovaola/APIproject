import os
import uuid


class ItemExchange:
    from flask_sqlalchemy import SQLAlchemy

    def __init__(self, database: SQLAlchemy, db_name='sqlite:///object-collection.db') -> None:
        from flask import Flask
        from flask_restful import Api

        super().__init__()
        self.server = Flask(__name__)
        self.server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', db_name)
        self.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.server.config['PROPAGATE_EXCEPTIONS'] = True

        database.init_app(self.server)

        @self.server.before_first_request
        def migrate_db():
            database.create_all()

        self.api = Api(self.server)
        self.__init_resources()

    def __init_resources(self):
        from resources.user import UserRegister, UserLogin
        from resources.items import ItemList, Item, ItemDelete, ItemAccept, ItemTransfer

        self.api.add_resource(UserRegister, '/register')
        self.api.add_resource(UserLogin, '/login')
        self.api.add_resource(ItemList, '/items')
        self.api.add_resource(Item, '/items/new')
        self.api.add_resource(ItemDelete, '/items/<string:id>')
        self.api.add_resource(ItemTransfer, '/send')
        self.api.add_resource(ItemAccept, '/get')

    def start(self, port: int):
        self.server.run(port=port, debug=True)

    def client(self):
        return self.server.test_client()


if __name__ == '__main__':
    from db import db

    app = ItemExchange(db)
    app.start(5000)
