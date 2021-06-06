import flask
from flask import request
from flask import jsonify, make_response
import constants
import databaseService as service

app = flask.Flask(__name__)


@app.route('/login', methods=['GET'])
def home():
    username = request.args.get("username")
    password = request.args.get("password")
    user = service.login(username, password)
    if(user != None):
        resp = jsonify({"message": "logged in", "username": user["username"]})
        return make_response(resp, 200)
