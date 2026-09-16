import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "")
client = MongoClient(MONGO_URI) if MONGO_URI else None
db = client['earning_app'] if client else None
users = db['users'] if db else None

@app.route('/')
def home():
    return jsonify({"status":"ok","message":"API Live with MongoDB"})

@app.route('/api/user/<user_id>')
def get_user(user_id):
    if users is None:
        return jsonify({"user_id": user_id, "balance": 0, "note": "DB not connected yet"})
    u = users.find_one({"user_id": user_id})
    if not u:
        new = {"user_id": user_id, "balance": 0, "coins": 0, "created_at": datetime.now()}
        users.insert_one(new)
        new.pop('_id', None)
        return jsonify(new)
    u['_id'] = str(u['_id'])
    return jsonify(u)

@app.route('/api/update', methods=['POST'])
def update():
    if users is None:
        return jsonify({"error":"DB not connected"}), 500
    data = request.json
    users.update_one({"user_id": data.get('user_id')}, {"$inc": {"balance": data.get('amount',0), "coins": data.get('amount',0)}}, upsert=True)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
