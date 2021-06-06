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
        return response, 400
    else:
        user = {"username": username, "password": base64.b64encode(
            password.encode("ascii")).decode("utf-8")}
        collection.insert_one(user)
        response = jsonify(
            {"message": "registration successful", "status": 201})
        return response, 201


def getData(username):
    collection = database[constants.TASK_DATA_COLLECTION]
    user = collection.find_one({"username": username}, {"_id": 0})
    if(user != None):
        response = jsonify({"status": 200, "data": user})
        return response, 200
    else:
        response = jsonify({"message": "no data", "status": 204})
        return response, 204


def deleteTask(username, date, task):
    collection = database[constants.TASK_DATA_COLLECTION]
    user = collection.find_one({"username": username}, {"_id": 0})
    if(user != None):
        print(user, user["taskData"])
        # find the date
        for object in user["taskData"]:
            if(object["date"] == date):
                object["tasks"].remove(task)
        collection.update_one({"username": username}, {"$set": user})
        response = jsonify({"message": "task Deleted", "status": 200})
        return response, 200

    else:
        response = jsonify({"message": "no data", "status": 400})
        return response, 400


def editTask(username, currentDate, currentTask, newDate, newTask):
    collection = database[constants.TASK_DATA_COLLECTION]
    user = collection.find_one({"username": username}, {"_id": 0})
    if(user != None):
        print(user, user["taskData"])
        # find the date
        dateExists = False
        for object in user["taskData"]:
            # remove previous task
            if(object["date"] == currentDate and currentTask != ""):
                object["tasks"].remove(currentTask)
            # add task to new date
            if(object["date"] == newDate):
                dateExists = True
                object["tasks"].append(newTask)

        if(not dateExists):
            user["taskData"].append({
                "date": newDate,
                "tasks": [newTask]
            })

        collection.update_one({"username": username}, {"$set": user})
        response = jsonify({"message": "task updated", "status": 200})
        return response, 200

    else:
        response = jsonify({"message": "no data", "status": 400})
        return response, 400
