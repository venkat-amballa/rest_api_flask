import sqlite3
from flask_restful import Resource, reqparse

from models.user_model import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username cant be left")
    parser.add_argument('password', type=str, required=True, help="password cant be left")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_name(data['username']):
            return {'msg':"this user already exists"}, 400
        
        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {'msg':'Created the user succesfully'}, 201