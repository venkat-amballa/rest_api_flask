import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity

from resources.user import UserRegister
from resources.items import Item, ItemList
from resources.store import StoreList, Store

from db import db
'''
    activate virtual env(windows): .\venv\Scripts\activate
'''

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # 'sqlite:///data.db' # the database can be anytype like: postgresql, mysql etc instead of sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
api = Api(app)

@app.before_first_request
def create_tablels():
    db.create_all()

jwt = JWT(app, authenticate, identity)
# Every thing that our api deals is called a REsource

# And every Resource will be a class

# Use filter function to iterate instead of for loop

# JWT- Json Web Token

'''
    status codes:
        400 - Bad Request response status code indicates that the server cannot or will not process the request due to something that is perceived to be a client error
        401 - UnAuthorised
        404 - Not Found
        500 - Internal server error
        
        200 - Successfull responce from server
        201 - Successfully created
        202 - Accepted to create, but it may take some time. If it fails after sending `202` its another case.
'''

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/<string:name>
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__=='__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)