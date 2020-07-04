from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item_model import ItemModel

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                    required=True, 
                    type=float, 
                    help="Every item should have a price"
                    )
    parser.add_argument('store_id',
                    required=True, 
                    type=int, 
                    help="Every item shoould have a store id"
                    )
    
    #################
    # CRUD OPERATIONS
    #################
    # Get the details of particular item.
    def get(self, name): 
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"msg":"not found"}, 404

    # Add an item using its unique name
    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"msg": "item with name {} already exists".format(name)}, 400
        request_body = Item.parser.parse_args()
        
        item = ItemModel(name, **request_body)
        try:
            item.save_to_db()
        except:
            return  {"msg":"Error occured while inserting the item"}, 500
        
        return item.json(), 201

    # Update an item based on its unique name, if present. else, make a new item and add it.
    def put(self, name):
        request_body = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_body)
        else:
            item.price = request_body["price"]
        item.save_to_db()
        return  item.json(), 200
        
    # Delete an item based on its name.
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
        except:
            return {"msg":"Error while deleting"}, 500
        return {"msg": "Deleted "}, 200
