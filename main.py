from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DB = "db.json"

def load_db():
    if not os.path.exists(DB): return {}
    with open(DB,"r",encoding="utf-8") as f: return json.load(f)
def save_db(d):
    with open(DB,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    uid = request.args.get("user_id","108365")
    db = load_db()
    if uid not in db:
        db[uid] = {"balance":0,"diamond":0,"ads":0,"refs":0,"withdraws":[]}
        save_db(db)
    u = db[uid]
    return render_template("index.html", user_id=uid, balance=u["balance"], diamond=u["diamond"], ads_watched=u["ads"])

@app.route("/reset_all")
def reset_all():
    save_db({}); return "✅ সব ID জিরো করে দেওয়া হয়েছে। এখন নতুন লিংকে ঢুকো"

@app.route("/api/watch_ad", methods=["POST"])
def watch_ad():
    uid = request.args.get("user_id")
    db = load_db(); u = db.get(uid)
    if not u: return jsonify({"error":True})
    u["balance"] += 18; u["diamond"] += 1; u["ads"] += 1
    save_db(db)
    return jsonify({"balance":u["balance"],"diamond":u["diamond"]})

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data = request.json; uid = data.get("user_id")
    db = load_db(); u = db.get(uid)
    if u["balance"] < data["amount"]: return jsonify({"error":"ব্যালেন্স কম"})
    if u["balance"] < 1000: return jsonify({"error":"মিনিমাম ৳1000 লাগবে"})
    # Transaction Number সহ save
    wd = {"number":data["number"],"amount":data["amount"],"method":data["method"],"time":datetime.now().strftime("%d/%m %H:%M"),"status":"Pending","user":uid}
    u["withdraws"].append(wd); u["balance"] -= data["amount"]
    save_db(db); return jsonify({"ok":True})

@app.route("/admin")
def admin():
    db = load_db()
    all_wd = []
    for uid, u in db.items():
        for w in u.get("withdraws",[]): all_wd.append({**w,"user":uid})
    return render_template("admin.html", withdraws=all_wd[::-1], total_users=len(db))

if __name__ == "__main__": app.run(host="0.0.0.0", port=10000)
