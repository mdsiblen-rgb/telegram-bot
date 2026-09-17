import os, json, time, requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- DB Setup MongoDB + JSON Fallback ---
MONGO_URL = os.getenv("MONGODB_URI") or os.getenv("MONGO_URL") or os.getenv("MONGODB_URL") or os.getenv("MONGO_URI")
USE_MONGO = False
client = None
db_col = None
config_col = None

try:
    if MONGO_URL:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URL)
        db = client["telegram_bot_db"]
        db_col = db["users"]
        config_col = db["config"]
        USE_MONGO = True
        print("✅ MongoDB Connected")
except Exception as e:
    print(f"MongoDB Fail: {e}")
    USE_MONGO = False

DB_FILE = "/data/db.json" if os.path.exists("/data") else "db.json"
DEFAULT_CONFIG = {
    "min_withdraw": 20,
    "per_ad": 2,
    "daily_limit": 10,
    "direct_link_company": "https://www.profitablecpmrate.com/v2iyv02n?key=8a0f68d9fb7d1d9d05d5e6c6e8e8c6e8",
    "popup_company": "https://www.profitablecpmrate.com/v2iyv02n?key=8a0f68d9fb7d1d9d05d5e6c6e8e8c6e8"
}

def load_config():
    if USE_MONGO:
        c = config_col.find_one({"_id": "main"})
        if c: return c
        config_col.insert_one({"_id": "main", **DEFAULT_CONFIG})
        return DEFAULT_CONFIG
    if not os.path.exists(DB_FILE): return DEFAULT_CONFIG.copy()
    try:
        with open(DB_FILE, "r") as f:
            d = json.load(f)
            return d.get("config", DEFAULT_CONFIG)
    except: return DEFAULT_CONFIG.copy()

def save_config(cfg):
    if USE_MONGO:
        config_col.update_one({"_id": "main"}, {"$set": cfg}, upsert=True)
    else:
        data = {}
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r") as f: data = json.load(f)
            except: pass
        data["config"] = cfg
        with open(DB_FILE, "w") as f: json.dump(data, f)

def load_users():
    if USE_MONGO:
        users = {}
        for u in db_col.find():
            users[u["_id"]] = u
        return users
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f).get("users", {})
    except: return {}

def get_user(uid):
    uid = str(uid)
    if USE_MONGO:
        u = db_col.find_one({"_id": uid})
        if not u:
            u = {"_id": uid, "balance": 0, "ads": 0, "last_reset": time.time()}
            db_col.insert_one(u)
        return u
    users = load_users()
    if uid not in users:
        users[uid] = {"balance": 0, "ads": 0, "last_reset": time.time()}
        # save
        data = {"users": users, "config": load_config()}
        with open(DB_FILE, "w") as f: json.dump(data, f)
    return users[uid]

def update_user(uid, data):
    uid = str(uid)
    if USE_MONGO:
        db_col.update_one({"_id": uid}, {"$set": data}, upsert=True)
    else:
        users = load_users()
        if uid in users:
            users[uid].update(data)
        else:
            users[uid] = data
        with open(DB_FILE, "w") as f:
            json.dump({"users": users, "config": load_config()}, f)

# --- Bot Config ---
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("BOT_") or os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID") or os.getenv("ADMIN_ID")

def send_bot(msg):
    if not BOT_TOKEN or not ADMIN_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": ADMIN_ID, "text": msg, "parse_mode": "HTML"})
    except: pass

# --- Routes (Same as before) ---
@app.route("/")
def home():
    cfg = load_config()
    return render_template_string(open("index.html").read() if os.path.exists("index.html") else "<h1>Bot Live</h1>", config=cfg)

@app.route("/api/balance")
def balance():
    uid = request.args.get("uid", "0")
    user = get_user(uid)
    cfg = load_config()
    # 12 hour reset
    if time.time() - user.get("last_reset", 0) > 43200: # 12h
        update_user(uid, {"ads": 0, "last_reset": time.time()})
        user["ads"] = 0
    return jsonify({"balance": user.get("balance",0), "ads": user.get("ads",0), "config": cfg})

@app.route("/api/watch", methods=["POST"])
def watch():
    d = request.json
    uid = str(d.get("uid", "0"))
    user = get_user(uid)
    cfg = load_config()

    if time.time() - user.get("last_reset", 0) > 43200:
        user["ads"] = 0
        user["last_reset"] = time.time()

    if user.get("ads",0) >= cfg.get("daily_limit",10):
        return jsonify({"error": "limit"}), 400

    new_bal = user.get("balance",0) + cfg.get("per_ad",2)
    new_ads = user.get("ads",0) + 1
    update_user(uid, {"balance": new_bal, "ads": new_ads, "last_reset": user.get("last_reset", time.time())})
    return jsonify({"balance": new_bal, "ads": new_ads})

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    d = request.json
    uid = str(d.get("uid", "0"))
    amount = d.get("amount", 0)
    method = d.get("method", "")
    acc = d.get("account", "")
    user = get_user(uid)

    cfg = load_config()
    if user.get("balance",0) < cfg.get("min_withdraw",20):
        return jsonify({"error": "low balance"}), 400

    update_user(uid, {"balance": 0})
    send_bot(f"🔔 <b>New Withdraw</b>\n\nUser: <code>{uid}</code>\nAmount: {amount}\nMethod: {method}\nAccount: {acc}\n\nBalance was: {user.get('balance')}")
    return jsonify({"success": True})

@app.route("/admin")
def admin():
    # simple admin page redirect
    return jsonify(load_config())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
