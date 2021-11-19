from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from restapicode.models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank.")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store_id.")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "Something went wrong with the search"}, 500
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with the name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            ItemModel.save_to_db(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500 #internal server error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"], data["store_id"])
        if item is None:
            item = ItemModel(name, data['price'], data["store_id"])
        else:
            item.price = data["price"]


        return updated_item.json(), 201

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}