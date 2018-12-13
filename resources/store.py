from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            return store.json()
        return {"message": "No store by that name"}, 404

    def post(self, name):
        if StoreModel.get_by_name(name):
            return {"message": "Store already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while updating the database"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            store.delete_from_db
        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
