from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="Item must have a price!"
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Item must belong to a store!"
    )

    def get(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.get_by_name(name):
            return {"message": "An item named {} already exists".format(name)}, 400

        data = self.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting the item."}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item {} has been deleted".format(name)}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.get_by_name(name)
        if not item:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return {"items": [x.json() for x in ItemModel.query.all()]}
