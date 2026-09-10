from flask import Flask, request, jsonify, render_template
import json, os, time
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "withdraws": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users": {}, "withdraws": []}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    if request.args.get("id") != "8807178385":
        return "Unauthorized", 403
    return render_template("admin.html")

@app.route("/api/admin/data")
def admin_data():
    if request.args.get("id") != "8807178385":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(load_db())

@app.route("/api/admin/edit", methods=["POST"])
def admin_edit():
    data = request.json
    db = load_db()
    uid = data.get("user_id")
    if uid in db["users"]:
        db["users"][uid]["balance"] = int(data.get("balance", 0))
        db["users"][uid]["total"] = int(data.get("total", 0))
        save_db(db)
        return jsonify({"ok": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/admin/ban", methods=["POST"])
def admin_ban():
    db = load_db()
    uid = request.json.get("user_id")
    if uid in db["users"]:
        db["users"][uid]["status"] = "BANNED" if db["users"][uid].get("status") != "BANNED" else "OK"
        save_db(db)
        return jsonify({"ok": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    uid = str(data.get("user_id"))
    db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid, "balance": 20, "ref_count": 0, "total": 20, "status": "OK",
            "joined": datetime.now().strftime("%d/%m/%Y"),
            "ref_by": data.get("ref")
        }
        ref_by = data.get("ref")
        if ref_by and ref_by in db["users"]:
            db["users"][ref_by]["balance"] += 10
            db["users"][ref_by]["total"] += 10
            db["users"][ref_by]["ref_count"] += 1
        save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid = str(request.json.get("user_id"))
    db = load_db()
    db["users"][uid]["balance"] += 5
    db["users"][uid]["total"] += 5
    save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    uid = str(request.json.get("user_id"))
    amt = int(request.json.get("amount", 0))
    db = load_db()
    if db["users"][uid]["balance"] < amt:
        return jsonify({"error": "Insufficient"}), 400
    db["users"][uid]["balance"] -= amt
    db["withdraws"].append({"id": str(int(time.time())), "user": uid, "amount": amt, "method": "Bkash", "status": "PENDING"})
    save_db(db)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
