import os, json, time, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- MONGO SETUP ---
MONGO_URL = os.getenv("MONGODB_URI") or os.getenv("MONGO_URL") or os.getenv("MONGO_URI") or os.getenv("MONG_")
USE_MONGO = False
db_col = None
config_col = None

if MONGO_URL:
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URL)
        db = client["telegram_bot_db"]
        db_col = db["users"]
        config_col = db["config"]
        USE_MONGO = True
        print("✅ MongoDB Connected")
    except Exception as e:
        print(f"Mongo Error: {e}")

DB_FILE = "/data/db.json" if os.path.exists("/data") else "db.json"
DEFAULT_CONFIG = {
    "min_withdraw": 20,
    "per_ad": 2,
    "daily_limit": 10
}

def load_config():
    if USE_MONGO:
        c = config_col.find_one({"_id": "main"})
        if c: return c
        config_col.insert_one({"_id": "main", **DEFAULT_CONFIG})
        return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def get_user(uid):
    uid = str(uid)
    if USE_MONGO:
        u = db_col.find_one({"_id": uid})
        if not u:
            u = {"_id": uid, "balance": 0, "ads": 0, "last_reset": time.time()}
            db_col.insert_one(u)
        # 12 hour reset ads only
        if time.time() - u.get("last_reset", 0) > 43200:
            db_col.update_one({"_id": uid}, {"$set": {"ads": 0, "last_reset": time.time()}})
            u["ads"] = 0
        return u
    return {"_id": uid, "balance": 0, "ads": 0, "last_reset": time.time()}

def update_user(uid, data):
    if USE_MONGO:
        db_col.update_one({"_id": str(uid)}, {"$set": data}, upsert=True)

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT_")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID") or os.getenv("ADMIN_ID") or os.getenv("ADMIN_")

def send_bot(msg):
    if not BOT_TOKEN or not ADMIN_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": ADMIN_ID, "text": msg})
    except: pass

@app.after_request
def after(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

@app.route("/")
def home():
    return "Bot is Live - MongoDB Connected" if USE_MONGO else "Bot is Live"

@app.route("/api/balance")
def balance():
    uid = request.args.get("uid", "0")
    user = get_user(uid)
    return jsonify({"balance": user.get("balance",0), "ads": user.get("ads",0), "config": load_config()})

@app.route("/api/watch", methods=["POST", "OPTIONS"])
def watch():
    if request.method == "OPTIONS": return jsonify({})
    d = request.json
    uid = str(d.get("uid", "0"))
    user = get_user(uid)
    cfg = load_config()
    if user.get("ads",0) >= cfg.get("daily_limit",10):
        return jsonify({"error": "limit"}), 400
    new_bal = user.get("balance",0) + cfg.get("per_ad",2)
    new_ads = user.get("ads",0) + 1
    update_user(uid, {"balance": new_bal, "ads": new_ads})
    return jsonify({"balance": new_bal, "ads": new_ads})

@app.route("/api/withdraw", methods=["POST", "OPTIONS"])
def withdraw():
    if request.method == "OPTIONS": return jsonify({})
    d = request.json
    uid = str(d.get("uid", "0"))
    amount = d.get("amount", 0)
    user = get_user(uid)
    update_user(uid, {"balance": 0})
    send_bot(f"New Withdraw\nUser: {uid}\nAmount: {amount}\nMethod: {d.get('method')}\nAccount: {d.get('account')}\nBalance was: {user.get('balance')}")
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
