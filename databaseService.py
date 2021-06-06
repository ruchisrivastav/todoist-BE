import pymongo
import constants
from flask import json, jsonify, make_response
import base64


mongoClient = pymongo.MongoClient(constants.DEV_MONGO_CLIENT)
database = mongoClient[constants.DATABASE]


def login(username, password):
    collection = database[constants.USER_COLLECTION]
    user = collection.find_one({"username": username, "password": password})
    return user


def register(username, password):
    collection = database[constants.USER_COLLECTION]
    user = collection.find_one({"username": username})
    if(user != None):
        response = jsonify({"message": "user already exists", "status": 400})
        return make_response(response, 400)
    else:
        user = {"username": username, "password": base64.b64encode(
            password.encode("ascii")).decode("utf-8")}
        collection.insert_one(user)
        response = jsonify(
            {"message": "registration successful", "status": 201})
        return make_response(response, 201)
