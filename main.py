from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    with open(DATA_FILE, "r") as f:
        try: return json.load(f)
        except: return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {"balance":715,"total_earn":715,"today_earn":0,"yesterday_earn":315,"ads_watched":37,"refer":0,"withdraw":0,"history":[]}
        save_data(data)
    return data["users"][uid], data

@app.route("/")
def home():
    user_id = request.args.get("user_id", "108365")
    u, _ = get_user(user_id)
    return render_template("index.html", user_id=user_id, balance=u["balance"], total_earn=u["total_earn"], today_earn=u["today_earn"], yesterday_earn=u["yesterday_earn"], ads_watched=u["ads_watched"], total_refer=u["refer"], withdraw=u["withdraw"], history=u["history"])

@app.route("/api/watch_ad", methods=["POST"])
def watch_ad():
    user_id = request.args.get("user_id", "108365") or request.get_json(silent=True, cache=False).get("user_id", "108365")
    u, data = get_user(user_id)
    u["balance"] += 18; u["total_earn"] += 18; u["today_earn"] += 18; u["ads_watched"] += 1
    save_data(data)
    return jsonify({"new_balance": u["balance"], "ads": u["ads_watched"], "today": u["today_earn"]})

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    j = request.get_json()
    user_id = str(j.get("user_id", "108365")); amount = int(j.get("amount", 0)); number = j.get("number", ""); method = j.get("method", "bKash")
    u, data = get_user(user_id)
    if u["balance"] < 1000: return jsonify({"error": "ব্যালেন্স যথেষ্ট নয়, ৳1000 লাগবে"})
    if amount < 1000: return jsonify({"error": "মিনিমাম ৳1000"})
    if len(number) < 11: return jsonify({"error": "সঠিক নাম্বার দিন"})
    u["balance"] -= amount; u["withdraw"] += amount
    u["history"].append({"amount":amount,"number":number,"method":method,"time":datetime.now().strftime("%d/%m %H:%M"),"status":"Pending"})
    save_data(data)
    return jsonify({"success":True, "new_balance": u["balance"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
