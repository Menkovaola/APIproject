import os
from flask import Flask

from flask_restful import Api
from resources.user import UserRegister, UserLogin
from resources.items import ItemList, Item, ItemDelete, ItemAccept, ItemTransfer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///object-collection.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'wilson'
api = Api(app)

# if run locally
# create db and all table before request, unless they exist already
@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/new')
api.add_resource(ItemDelete, '/items/<string:id>')
api.add_resource(ItemTransfer, '/send')
api.add_resource(ItemAccept, '/get')

if __name__ == '__main__':
    from db import db
    db.init_app(app)  # register our database with our app
    app.run(port=5000, debug=True)
