import logging
from flask import Flask, request
import requests
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/mybackend"
mongo = PyMongo(app)

@app.route("/backend")
def default():
    online_users = mongo.db.users.find({"online": True})
    return 'Backend OK!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8083, debug=True, threaded=True)
