# FINAL COMPLETE A-Z - 9 TASK - 5 BUTTON WORKING - MINI BOY 11764581 - 2026
from flask import Flask, jsonify, render_template_string, request
import json, os
from datetime import datetime
app = Flask(__name__)
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},
            "withdraws": [],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD",
                "ad_reward": 2,
                "ad_limit": 100,
                "ref_bonus": 20,
                "welcome_bonus": 60,
                "min_withdraw": 1000,
                "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "admin_msg_title": "আফাশয়াল নোটস",
                "admin_msg_desc": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন",
                "my_ad_title": "স্পেশাল অফার - আজকের বোনাস",
                "my_ad_desc": "বোনাস নিন",
                "payment_time": "২৪ ঘণ্টা",
                "payment_rules": "মিনিমাম ১০০০ টাকা",
                "support_title": "🎧 সাপোর্ট",
                "support_desc": "যেকোনো সমস্যায় মেসেজ করুন",
                "support_extra": "২৪/৭ Active",
                "support_custom": "https://t.me/ProtidinerKajBD",
                "s1": "https://via.placeholder.com/600x250/1e40af/ffffff?text=Bonus",
                "s2": "https://via.placeholder.com/600x250/0f766e/ffffff?text=Offer",
                "s3": "https://via.placeholder.com/600x250/be123c/ffffff?text=Reward"
            },
            # তোমার দেওয়া সম্পূর্ণ ৯ টা টাস্ক - একটাও বাদ দিই নাই
            "tasks": [
                {"title": "YouTube Channel Subscribe", "reward": 25, "link": "https://youtube.com/@YourChannel", "color": "#dc2626"},
                {"title": "Telegram Channel Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af"},
                {"title": "Facebook Page Follow", "reward": 15, "link": "https://facebook.com", "color": "#1877F2"},
                {"title": "Company Task 1 - Website Visit", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#7c3aed"},
                {"title": "Company Task 2 - Telegram Group Join", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#0f766e"},
                {"title": "Company Task 3 - Post Like", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#be123c"},
                {"title": "Company Task 4 - Post Share", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#065f46"},
                {"title": "Company Task 5 - Comment Task", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#2563eb"},
                {"title": "Company Task 6 - Refer 3 Friend", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#d97706"}
            ],
            "slider": []
        }
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=2, ensure_ascii=False)

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"balance": 60, "ads_today": 0, "last_ad_date": str(datetime.now().date()), "claimed_tasks": [], "total_ref": 0}
    u = db["users"][uid]
    if u["last_ad_date"]!= str(datetime.now().date()):
        u["ads_today"] = 0; u["last_ad_date"] = str(datetime.now().date())
    return u

@app.route('/health')
def health(): return "ok", 200
@app.route('/')
def index(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)
@app.route('/api/get_full')
def get_full():
    db = load_db(); uid = request.args.get('id') or '8801'
    u = get_user(db, uid); save_db(db)
    return jsonify({"user": u, "settings": db["settings"], "tasks": db["tasks"]})
@app.route('/api/reward')
def reward():
    db = load_db(); u = get_user(db, request.args.get('id'))
    if u["ads_today"] >= 100: return jsonify({"msg": "আজকের লিমিট শেষ!"})
    u["ads_today"] += 1; u["balance"] += 2; save_db(db)
    return jsonify({"msg": "৳2 যোগ হয়েছে!"})
@app.route('/api/claim_task')
def claim_task():
    db = load_db(); uid = request.args.get('id'); idx = int(request.args.get('idx')); u = get_user(db, uid)
    if idx in u["claimed_tasks"]: return jsonify({"msg": "Already Done!"})
    u["claimed_tasks"].append(idx); u["balance"] += db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg": f'৳{db["tasks"][idx]["reward"]} পেয়েছেন!'})
@app.route('/api/withdraw')
def withdraw():
    db = load_db(); uid = str(request.args.get('id')); amt = int(request.args.get('amount', 0))
    u = get_user(db, uid)
    if u["balance"] < 1000: return jsonify({"msg": "মিনিমাম ৳1000 লাগবে!"})
    u["balance"] -= amt; db["withdraws"].append({"uid": uid, "amount": amt, "method": request.args.get('method'), "number": request.args.get('number'), "time": str(datetime.now())}); save_db(db)
    return jsonify({"msg": "Withdraw Success!"})

@app.route('/api/admin_all')
def admin_all(): return jsonify(load_db())
@app.route('/api/admin_save', methods=['POST'])
def admin_save(): save_db(request.json); return jsonify({"msg": "Saved"})

USER_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{margin:0;background:#0a1435;color:#fff;font-family:system-ui;padding-bottom:90px}
.header{background:linear-gradient(135deg,#1a2a6c,#0f4c75);padding:18px;border-radius:0 0 24px 24px}
.bal{font-size:36px;font-weight:900;color:#4ade80}
.card{background:#111f4d;border:1px solid #1e2d6a;margin:10px 12px;padding:14px;border-radius:16px}
button{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;background:#2563eb}
.nav{position:fixed;bottom:0;left:0;right:0;background:#0e1a3f;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1e2d6a}
.nav div{color:#7c8db0;text-align:center;font-size:11px;cursor:pointer}.nav div.active{color:#3b82f6;font-weight:900}
</style>
</head><body>
<div id='root'></div>
<div class='nav'>
<div id='nav_home' class='active' onclick='showTab("home")'>🏠<br>Home</div>
<div id='nav_tasks' onclick='showTab("tasks")'>✅<br>Tasks</div>
<div id='nav_refer' onclick='showTab("refer")'>👥<br>Refer</div>
<div id='nav_wallet' onclick='showTab("wallet")'>💰<br>Wallet</div>
<div id='nav_profile' onclick='showTab("profile")'>👤<br>Profile</div>
</div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8801';let DB={};let tab='home';
function load(){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{DB=d;render()})}
function showTab(t){tab=t;document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav_'+t).classList.add('active');render()}
function render(){
 let s=DB.settings,u=DB.user;let h='';
 if(tab=='home'){
  h+=`<div class='header'><div style='display:flex;justify-content:space-between'><div><small>প্রতিদিনের কাজ BD</small><div class='bal'>৳ ${u.balance}</div><small>Ads: ${u.ads_today}/100 | Bonus: ৳60</small></div><img src='${s.company_logo}' style='width:50px;height:50px;border-radius:50%'></div></div>`;
  h+=`<div class='card' style='background:linear-gradient(90deg,#1e3a8a,#0f766e)'><div style='display:flex;justify-content:space-between'><div><b>${s.admin_msg_title}</b><br><small>${s.admin_msg_desc}</small></div><span style='background:#22c55e;color:#000;padding:4px 10px;border-radius:20px;font-size:10px;font-weight:900'>LIVE</span></div></div>`;
  h+=`<div class='card'><b>🎬 🔥 ${s.my_ad_title}</b><br><button onclick='watchAd()' style='margin-top:10px;background:linear-gradient(90deg,#2563eb,#0ea5e9)'>▶️ MINI BOY ADS দেখুন - ৳${s.ad_reward} পাবেন</button><small style='opacity:.5'>Zone: 11764581 - Monetag Many Boy</small></div>`;
  h+=`<div class='card'><b>📋 আজকের ${DB.tasks.length} টি টাস্ক - সবগুলোতে Mini Boy Ad বসানো আছে</b></div>`;
  DB.tasks.slice(0,3).forEach((t,i)=>{let done=u.claimed_tasks.includes(i);h+=`<div class='card'><div style='display:flex;justify-content:space-between'><span>⭐ ${t.title}</span><b style='color:#ef4444'>৳${t.reward}</b></div><small>Reward ৳${t.reward}</small><button onclick='claimTask(${i})' style='margin-top:8px;background:${done?'#16a34a':'#dc2626'}'>${done?'✅ Completed':'👉 Claim + Watch Mini Boy Ad'}</button></div>`});
 }else if(tab=='tasks'){
  h+=`<div class='card'><b>📋 সব ৯ টা টাস্ক (Final)</b></div>`;
  DB.tasks.forEach((t,i)=>{let done=u.claimed_tasks.includes(i);h+=`<div class='card'><div style='display:flex;justify-content:space-between'><span>⭐ ${t.title}</span><b>৳${t.reward}</b></div><button onclick='claimTask(${i})' style='margin-top:8px;background:${done?'#16a34a':t.color}'>${done?'✅ Done':'👉 Claim + Watch Mini Boy Ad'}</button></div>`});
 }else if(tab=='refer'){
  h+=`<div class='card'><b>👥 Refer & Earn ৳${s.ref_bonus}</b><br><div style='background:#0a1229;padding:12px;border-radius:10px;word-break:break-all'>https://t.me/YourBot?start=${uid}</div><button onclick='navigator.clipboard.writeText("https://t.me/YourBot?start=${uid}");alert("Copied")' style='margin-top:8px'>Copy Link</button></div>`;
 }else if(tab=='wallet'){
  h+=`<div class='card'><b>💰 Wallet</b><div class='bal'>৳ ${u.balance}</div><small>Min: ৳${s.min_withdraw}</small></div><div class='card'><input id='a' type='number' placeholder='Amount' style='width:100%;padding:12px;border-radius:10px;background:#0a1229;color:#fff;border:1px solid #1e2d6a'><input id='m' placeholder='Bkash/Nagad' style='width:100%;padding:12px;border-radius:10px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:8px'><input id='n' placeholder='Number' style='width:100%;padding:12px;border-radius:10px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:8px'><button onclick='withdraw()' style='margin-top:8px'>Withdraw</button></div>`;
 }else if(tab=='profile'){
  h+=`<div class='card'><b>👤 Profile</b><br>ID: ${uid}<br>Balance: ৳${u.balance}<br>Ads: ${u.ads_today}<br>Tasks: ${u.claimed_tasks.length}/${DB.tasks.length}</div>`;
 }
 document.getElementById('root').innerHTML=h;
}
function watchAd(){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})})}
function claimTask(i){show_11764581().then(()=>{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})})}
function withdraw(){let a=document.getElementById('a').value,m=document.getElementById('m').value,n=document.getElementById('n').value;fetch(`/api/withdraw?id=${uid}&amount=${a}&method=${m}&number=${n}`).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
load();
</script></body></html>
"""

ADMIN_HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{background:#070f2b;color:#fff;font-family:system-ui;padding:12px}.card{background:#111c44;padding:12px;border-radius:12px;margin-bottom:10px}button{padding:8px 12px;background:#2563eb;color:#fff;border:none;border-radius:8px}</style></head>
<body><h2>Admin Full - 9 Task - Mini Boy 11764581</h2><div id='r'>Loading...</div><script>fetch('/api/admin_all').then(r=>r.json()).then(d=>{let h=`<div class='card'>Users: ${Object.keys(d.users).length} | Withdraw: ${d.withdraws.length}</div><div class='card'><b>Tasks:</b><br>`;d.tasks.forEach((t,i)=>{h+=`${i+1}. ${t.title} - ৳${t.reward}<br>`});h+=`</div><a href='/'><button>User App</button></a>`;document.getElementById('r').innerHTML=h})</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
