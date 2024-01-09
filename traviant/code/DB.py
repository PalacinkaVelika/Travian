from pymongo import MongoClient

class DB:
    #Simplifies using Database
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017", connect=True)
        self.db = self.client['traviant']

    def insert_record(self, collection, new_record):
        if isinstance(collection, str):
            collection = self.db[collection]
        else:
            print("insert_record() requires string name of collection")
        return collection.insert_one(new_record)

    def get_collection(self, collection):
        if isinstance(collection, str):
            collection = self.db[collection]
        else:
            print("get_collection() requires string name of collection")
        return collection