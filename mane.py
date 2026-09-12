# app.py - FINAL FULL FILE - MINI BOY 11764581 - 9 TASK - BLUE THEME
from flask import Flask, jsonify, render_template_string, request
import json, os, time, threading, requests
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"
SELF_URL = "https://telegram-bot-1-v77g.onrender.com"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},
            "settings": {
                "ad_reward": 2, "ad_limit": 100, "ref_bonus": 20,
                "app_name": "প্রতিদিনের কাজ BD", "welcome_bonus": 60,
                "min_withdraw": 1000,
                "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "s1": "https://via.placeholder.com/430x185/1e40af/ffffff?text=Bonus",
                "s2": "https://via.placeholder.com/430x185/0f766e/ffffff?text=Offer",
                "s3": "https://via.placeholder.com/430x185/be123c/ffffff?text=Reward"
            },
            "tasks": [
                {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#065f46"},
                {"title": "Telegram Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af"},
                {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#1877F2"},
                {"title": "Company Task 1", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#7c3aed"},
                {"title": "Company Task 2", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#0f766e"},
                {"title": "Company Task 3", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#be123c"},
                {"title": "Company Task 4", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#065f46"},
                {"title": "Company Task 5", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af"},
                {"title": "Company Task 6", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#1877F2"}
            ],
            "slider": [
                {"img": "https://via.placeholder.com/430x185/1e40af/ffffff?text=Slide+1", "link": "https://t.me"},
                {"img": "https://via.placeholder.com/430x185/0f766e/ffffff?text=Slide+2", "link": "https://t.me"},
                {"img": "https://via.placeholder.com/430x185/be123c/ffffff?text=Slide+3", "link": "https://t.me"}
            ],
            "withdraws": []
        }
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"balance": db["settings"]["welcome_bonus"], "ads_today": 0, "last_ad_date": str(datetime.now().date()), "claimed_tasks": []}
    u = db["users"][uid]
    if u["last_ad_date"]!= str(datetime.now().date()):
        u["ads_today"] = 0
        u["last_ad_date"] = str(datetime.now().date())
    return u

@app.route('/health')
def health(): return "ok", 200

@app.route('/')
def index(): return render_template_string(USER_HTML)

@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    db = load_db(); uid = request.args.get('id')
    if not uid: return jsonify({"error": "no id"})
    u = get_user(db, uid); save_db(db)
    return jsonify({"user": u, "settings": db["settings"], "tasks": db["tasks"], "slider": db["slider"]})

@app.route('/api/reward')
def reward():
    db = load_db(); uid = str(request.args.get('id')); u = get_user(db, uid)
    if u["ads_today"] >= db["settings"]["ad_limit"]: return jsonify({"msg": "আজকের লিমিট শেষ!"})
    u["ads_today"] += 1; u["balance"] += db["settings"]["ad_reward"]; save_db(db)
    return jsonify({"msg": f'৳{db["settings"]["ad_reward"]} পেয়েছেন!', "balance": u["balance"]})

@app.route('/api/claim_task')
def claim_task():
    db = load_db(); uid = str(request.args.get('id')); idx = int(request.args.get('idx')); u = get_user(db, uid)
    if idx in u["claimed_tasks"]: return jsonify({"msg": "আগেই নিয়েছেন!"})
    u["claimed_tasks"].append(idx); u["balance"] += db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg": f'৳{db["tasks"][idx]["reward"]} বোনাস!'})

USER_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<!-- MINI BOY 11764581 - MANY BY -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{font-family:system-ui;background:#0f172a;color:white;margin:0;padding:12px}
.card{background:#1e293b;padding:14px;border-radius:14px;margin-bottom:10px;border:1px solid #334155}
.bal{font-size:26px;font-weight:bold;color:#22c55e}
button{background:#2563eb;color:white;border:none;padding:13px;border-radius:10px;width:100%;font-weight:bold;font-size:15px}
button:active{transform:scale(0.98)}
</style>
</head><body>
<div id='app'>Loading Mini Boy...</div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8801'; let DATA={};
function load(){ fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{ DATA=d; render(); }); }
function render(){
 let h=`<div class='card'><small>${DATA.settings.app_name}</small><div class='bal'>৳${DATA.user.balance}</div><small>Ads: ${DATA.user.ads_today}/${DATA.settings.ad_limit}</small></div>`;
 h+=`<div class='card'><button onclick='watchAd()'>🎬 MINI BOY ADS দেখুন - ৳${DATA.settings.ad_reward}</button></div>`;
 DATA.tasks.forEach((t,i)=>{
   let done=DATA.user.claimed_tasks.includes(i);
   h+=`<div class='card'><div style='display:flex;justify-content:space-between'><span>${t.title}</span><b style='color:${t.color}'>৳${t.reward}</b></div>
   <button onclick='claimTask(${i})' style='margin-top:8px;background:${done?'#16a34a':t.color}'>${done?'✅ Done':'👉 Claim + Watch Ad'}</button></div>`;
 });
 document.getElementById('app').innerHTML=h;
}
function watchAd(){
  show_11764581().then(()=>{ fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{ alert(x.msg); load(); }); }).catch(()=>{ fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{ alert(x.msg); load(); }); });
}
function claimTask(i){
  show_11764581().then(()=>{ fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{ alert(x.msg); load(); }); });
}
load();
</script></body></html>
"""

ADMIN_HTML = """<html><body style='background:#0f172a;color:white;font-family:system-ui;padding:20px'><h2>✅ ADMIN PANEL - MINI BOY 11764581 - 9 TASK LIVE</h2><p>All Fixed. Use /api/get_full to see data.</p><a href='/' style='color:#22c55e'>Go to User App</a></body></html>"""

if __name__=='__main__':
    port=int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0',port=port)
