from bson import ObjectId
from django.conf import settings
from pymongo import MongoClient

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
items_collection = db["items"]


class ItemModel:
    collection = items_collection

    @staticmethod
    def get_all_items():
        result = list(ItemModel.collection.find({}))
        return result

    @staticmethod
    def create_item(data):
        result = ItemModel.collection.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def get_item(item_id):
        return ItemModel.collection.find_one({"_id": ObjectId(item_id)})

    @staticmethod
    def update_item(item_id, data):
        return ItemModel.collection.update_one({"_id": ObjectId(item_id)}, {"$set": data})

    @staticmethod
    def delete_item(item_id):
        return ItemModel.collection.delete_one({"_id": ObjectId(item_id)})

    @staticmethod
    def search_items(query):
        return list(ItemModel.collection.find(query))

    @staticmethod
    def filter_by_category(category):
        return list(ItemModel.collection.find({"category": category}))
