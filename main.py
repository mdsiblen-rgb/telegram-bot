from flask import Flask, request, jsonify
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
def home():
    return """
    <!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protidiner Kaj BD</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src='//libtl.com/sdk.js' data-zone='11760259' data-sdk='show_11760259'></script>
    <style>body{font-family:system-ui;background:#f5f7fb;margin:0;padding:15px}.card{background:white;border-radius:16px;padding:16px;margin-bottom:12px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}.btn{background:#00b894;color:white;border:none;padding:12px 20px;border-radius:12px;width:100%;font-size:16px;font-weight:bold}.balance{font-size:32px;font-weight:bold;color:#00b894}</style>
    </head><body>
    <div class="card"><div>আপনার ব্যালেন্স</div><div class="balance" id="bal">৳ 0</div><div id="uid" style="font-size:12px;color:#888"></div></div>
    <div class="card"><h3>📢 বিজ্ঞাপন দেখে আয় করুন</h3><p style="font-size:14px;color:#666">১ টি Ad = ৳৫</p><button class="btn" onclick="watchAd()">📺 Ad দেখুন (৳৫)</button></div>
    <div class="card"><h3>💸 টাকা উত্তোলন</h3><button class="btn" style="background:#6c5ce7" onclick="withdraw()">Withdraw Request</button></div>
    <script>
    let userId = "user_"+Math.floor(Math.random()*90000+10000);
    let tg = window.Telegram.WebApp;
    if(tg.initDataUnsafe && tg.initDataUnsafe.user){ userId = tg.initDataUnsafe.user.id.toString(); }
    document.getElementById("uid").innerText = "ID: " + userId;
    async function init(){
      const urlParams = new URLSearchParams(window.location.search);
      const ref = urlParams.get("start") || urlParams.get("ref");
      let res = await fetch("/api/register", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({user_id: userId, name: tg.initDataUnsafe?.user?.first_name || userId, ref: ref})});
      let data = await res.json(); document.getElementById("bal").innerText = "৳ " + data.balance;
    } init();
    async function watchAd(){
      if(typeof show_11760259!== 'function'){ alert("Ad লোড হচ্ছে... ২ সেকেন্ড পর আবার চেষ্টা করুন"); return; }
      await show_11760259().then(async ()=>{
        let res = await fetch("/api/task_complete", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({user_id: userId, amount: 5})});
        let data = await res.json(); document.getElementById("bal").innerText = "৳ " + data.balance;
        alert("✅ ৳৫ যোগ হয়েছে! Monetag এ ডলারও যোগ হয়েছে");
      });
    }
    async function withdraw(){
      let amt = prompt("কত টাকা তুলতে চান? (Min 100)"); if(!amt) return;
      let res = await fetch("/api/withdraw", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({user_id: userId, amount: parseInt(amt), method:"Bkash"})});
      let d = await res.json(); if(d.ok) alert("Withdraw Request পাঠানো হয়েছে!"); else alert(d.error);
    }
    </script></body></html>
    """

@app.route("/admin")
def admin():
    if request.args.get("id")!= "8807178385":
        return "Unauthorized -?id=8807178385 add koro", 403
    return """
    <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Admin V11 Real</title>
    <style>body{font-family:system-ui;background:#f1f5f9;padding:10px;margin:0}table{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden}th{background:#2d3436;color:white;padding:10px;font-size:12px}td{padding:8px;border-bottom:1px solid #eee;font-size:13px;text-align:center}.btn{border:none;padding:6px 10px;border-radius:8px;color:white;margin:2px;cursor:pointer;font-size:12px}.edit{background:#00b894}.ban{background:#d63031}.card{background:white;padding:15px;border-radius:12px;margin-bottom:10px}</style>
    </head><body>
    <h2>Admin Panel - Real Users V11</h2><div class="card"><div>মোট ইউজার: <b id="totalU">0</b> | মোট Withdraw: <b id="totalW">0</b> | <a href="https://publishers.monetag.com/statistics" target="_blank">Monetag $ দেখতে ক্লিক</a></div><button onclick="load()" style="margin-top:10px;padding:8px 15px">🔄 Refresh</button></div>
    <h3>Users (Real)</h3><table><thead><tr><th>ID</th><th>Bal</th><th>Ref</th><th>Total</th><th>St</th><th>Act</th></tr></thead><tbody id="users"></tbody></table>
    <h3 style="margin-top:20px">Withdraw Requests</h3><table><thead><tr><th>ID</th><th>User</th><th>Amt</th><th>Method</th><th>Status</th></tr></thead><tbody id="withdraws"></tbody></table>
    <script>
    async function load(){
      let adminId = new URLSearchParams(window.location.search).get("id");
      let res = await fetch("/api/admin/data?id="+adminId); let db = await res.json();
      document.getElementById("totalU").innerText = Object.keys(db.users).length; document.getElementById("totalW").innerText = db.withdraws.length;
      let uHtml = ""; for(let uid in db.users){ let u = db.users[uid]; uHtml += `<tr><td>${u.id}</td><td>${u.balance}</td><td>${u.ref_count}</td><td>${u.total}</td><td>${u.status}</td><td><button class="btn edit" onclick="editUser('${u.id}')">Edit</button><button class="btn ban" onclick="banUser('${u.id}')">${u.status=='BANNED'?'Unban':'Ban'}</button></td></tr>`; }
      document.getElementById("users").innerHTML = uHtml || "<tr><td colspan=6>কোনো ইউজার এখনো জয়েন করেনি</td></tr>";
      let wHtml = ""; db.withdraws.slice().reverse().forEach(w=>{ wHtml += `<tr><td>${w.id}</td><td>${w.user}</td><td>${w.amount}</td><td>${w.method}</td><td>${w.status}</td></tr>`; });
      document.getElementById("withdraws").innerHTML = wHtml || "<tr><td colspan=5>No withdraw</td></tr>";
    }
    async function editUser(uid){ let bal = prompt("নতুন Balance কত দিবেন?"); if(bal===null) return; await fetch("/api/admin/edit", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({user_id: uid, balance: bal, total: bal})}); load(); }
    async function banUser(uid){ await fetch("/api/admin/ban", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({user_id: uid})}); load(); } load();
    </script></body></html>
    """

@app.route("/api/admin/data")
def admin_data():
    if request.args.get("id")!= "8807178385": return jsonify({"error": "Unauthorized"}), 403
    return jsonify(load_db())

@app.route("/api/admin/edit", methods=["POST"])
def admin_edit():
    db = load_db(); uid = request.json.get("user_id")
    if uid in db["users"]:
        db["users"][uid]["balance"] = int(request.json.get("balance", 0)); db["users"][uid]["total"] = int(request.json.get("balance", 0)); save_db(db); return jsonify({"ok": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/admin/ban", methods=["POST"])
def admin_ban():
    db = load_db(); uid = request.json.get("user_id")
    if uid in db["users"]:
        db["users"][uid]["status"] = "BANNED" if db["users"][uid].get("status")!= "BANNED" else "OK"; save_db(db); return jsonify({"ok": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json; uid = str(data.get("user_id")); db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "balance": 20, "ref_count": 0, "total": 20, "status": "OK", "joined": datetime.now().strftime("%d/%m/%Y"), "ref_by": data.get("ref")}
        ref_by = data.get("ref")
        if ref_by and ref_by in db["users"]:
            db["users"][ref_by]["balance"] += 10; db["users"][ref_by]["total"] += 10; db["users"][ref_by]["ref_count"] += 1
        save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid = str(request.json.get("user_id")); db = load_db()
    if uid in db["users"]:
        db["users"][uid]["balance"] += 5; db["users"][uid]["total"] += 5; save_db(db); return jsonify(db["users"][uid])
    return jsonify({"error": "not found"}), 404

@app.route("/api/withdraw", methods=["POST"])
def withdraw_req():
    uid = str(request.json.get("user_id")); amt = int(request.json.get("amount", 0)); db = load_db()
    if db["users"][uid]["balance"] < amt: return jsonify({"error": "Insufficient"}), 400
    db["users"][uid]["balance"] -= amt
    db["withdraws"].append({"id": str(int(time.time())), "user": uid, "amount": amt, "method": "Bkash", "status": "PENDING"})
    save_db(db); return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
