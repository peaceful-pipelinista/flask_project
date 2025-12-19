import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pymongo
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

db = client.test
collection = db['flask-tutorial']

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add():
    data = dict(request.json)
    data['created_at'] = datetime.now()
    collection.insert_one(data)
    return jsonify({"message": "Data saved successfully"}), 201

@app.route('/view', methods=['GET'])
def view():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

