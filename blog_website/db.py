from pymongo import MongoClient
import os

class MongoDB:

    def __init__(self, mongo_uri="mongodb://localhost:27017/", database_name="test_database", collection_name="blogger_db") -> None:
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[database_name]
        self.collection = self.db[collection_name]

    def put(self, doc):
        self.collection.insert_one(doc)

    def get(self, query):
        return self.collection.find_one(query)

    def update(self, query, update_query):
        self.collection.update_one(query, update_query)

    def delete(self, query):

        result = self.collection.delete_one(query)

        # Check if deletion was successful
        if result.deleted_count == 1:
            print("Document deleted successfully.")
        else:
            print("No document matched the filter criteria.")

    def create_index(self, query):
        self.collection.create_index([query])

    def get_all(self, query=None):
        return self.collection.find(query)

    def print_db(self):
        for doc in self.collection.find():
            print(doc)

    def get_top_searches(self, search_query):
        return self.collection.find({ "$text": { "$search": search_query } },
                                    { "score": { "$meta": "textScore" } }).sort({ "score": { "$meta": "textScore" } })


    # docker run -p 27017:27017 mongo
mongo_uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017/")

mongodb = MongoDB(mongo_uri=mongo_uri)
mongodb_blog = MongoDB(mongo_uri=mongo_uri, collection_name="blogs")
mongodb_blog.create_index(("title", "text"))
mongodb_chat = MongoDB(mongo_uri=mongo_uri, collection_name="user_chat")