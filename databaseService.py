import pymongo
import constants

mongoClient = pymongo.MongoClient(constants.DEV_MONGO_CLIENT)
database = mongoClient[constants.DATABASE]


def login(username, password):
    collection = database[constants.USER_COLLECTION]
    user = collection.find_one({"username": username, "password": password})
    return user
