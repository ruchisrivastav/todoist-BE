import flask
from flask import request
from flask import jsonify, make_response
import constants
import databaseService as service

app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "<h3>Welcome to Todoist</h3>"


@app.route('/login', methods=['GET'])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    user = service.login(username, password)
    if(user != None):
        resp = jsonify({"message": "logged in", "username": user["username"]})
        return make_response(resp, 200)
    else:
        resp = jsonify({"message": "user does not exist"})
        return make_response(resp, 400)


if __name__ == "__main__":
    app.run(debug=True)
