from flask_restful import Resource, reqparse

from models.store_model import StoreModel

class StoreList(Resource):
    def get(self):
        stores = [store.json() for store in StoreModel.query.all()]
        return {"stores":stores}

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "store with name {} does not exist".format(name)}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "store with name {} exists".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error ocuured while creating the store"}
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "store with name {} is deleted".format(name)}

