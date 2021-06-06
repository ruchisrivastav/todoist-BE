import flask
from flask import request
from flask import jsonify, make_response
import constants
import databaseService as service
import base64
from flask_cors import CORS, cross_origin
app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=["GET"])
def home():
    return "<h3>Welcome to Todoist</h3>"


@app.route('/login', methods=['GET'])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    # providing base64 encoding to the password for security
    user = service.login(username, base64.b64encode(
        password.encode("ascii")).decode("utf-8"))
    if(user != None):
        resp = jsonify({"message": "logged in", "status": 200,
                       "username": user["username"]})
        return resp, 200
    else:
        resp = jsonify({"message": "user does not exist", "status": 400})
        return resp, 400


@app.route("/register", methods=["POST"])
def register():
    requestData = request.get_json()
    return service.register(requestData.get("username"), requestData.get("password"))


@app.route("/getData", methods=["GET"])
def getData():
    return service.getData(request.args.get("username"))


@app.route("/deleteTask", methods=["PUT"])
def deleteTask():
    requestData = request.get_json()
    return service.deleteTask(requestData.get("username"), requestData.get("date"), requestData.get("task"))


@app.route("/editTask", methods=["PUT"])
def editTask():
    requestData = request.get_json()
    return service.editTask(requestData.get("username"), requestData.get("currentDate"), requestData.get("currentTask"), requestData.get("newDate"), requestData.get("newTask"))


if __name__ == "__main__":
    app.run(debug=True)
