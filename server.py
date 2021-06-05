import flask
from flask import request
import constants
import databaseService as service

app = flask.Flask(__name__)


@app.route('/login', methods=['GET'])
def home():
    username = request.args.get("username")
    password = request.args.get("password")
    service.login(username, password)
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


app.run(debug=True)
