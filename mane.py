# -*- coding: utf-8 -*-
# FINAL PROTODINER KAJ BD - A to Z - Zone 11764581 LOCKED - No Auto Ad
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'

def default_db():
    return {
        "users": {},
        "withdraws": [],
        "supports": [],
        "settings": {
            "app_name": "Protidiner Kaj BD",
            "admin_name": "MD Emon - Owner",
            "admin_id": "8807178385",
            "admin_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "welcome_bonus": 1120,
            "ad_reward": 2,
            "ad_limit": 50,
            "min_withdraw": 500,
            "zone": "11764581",
            "company_name": "Google Ads Partner - Sponsored",
            "company_logo": "https://cdn-icons-png.flaticon.com/512/300/300221.png",
            "notice_title": "অফিসিয়াল নোটিস",
            "notice_desc": "প্রতিদিন 50 টা Ads দেখুন - বড় কোম্পানির স্পন্সর থেকে ডলার আসবে"
        },
        "tasks": [
            {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "icon": "▶️"},
            {"title": "Telegram Join", "reward": 20, "link": "https://t.me", "color": "#1e40af", "icon": "✈️"},
            {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "icon": "👍"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d = default_db()
        with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=2)
        return d
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=2)

def get_user(db, uid):
    uid = str(uid); today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "name": f"User-{uid[-4:]}", "balance": db["settings"]["welcome_bonus"], "ads_today": 0, "total_ads": 0, "last_date": today, "claimed": [], "banned": False}
    u = db["users"][uid]
    if u.get("last_date")!= today: u["ads_today"] = 0; u["last_date"] = today
    return u

@app.route('/')
def index(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!= '8807178385': return "Admin Only - Add?id=8807178385", 403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get')
def api_get():
    db = load_db(); u = get_user(db, request.args.get('id', '0')); save_db(db)
    return jsonify({"user": u, "settings": db["settings"], "tasks": db["tasks"]})
@app.route('/api/reward')
def api_reward():
    db = load_db(); u = get_user(db, request.args.get('id'))
    if u["ads_today"] >= db["settings"]["ad_limit"]: return jsonify({"msg": "আজকের লিমিট শেষ"})
    u["balance"] += db["settings"]["ad_reward"]; u["ads_today"] += 1; u["total_ads"] += 1; save_db(db)
    return jsonify({"msg": f"৳{db['settings']['ad_reward']} যোগ হয়েছে!"})
@app.route('/api/claim')
def api_claim():
    db = load_db(); idx = int(request.args.get('idx')); u = get_user(db, request.args.get('id'))
    if idx in u["claimed"]: return jsonify({"msg": "Already Done"})
    u["claimed"].append(idx); u["balance"] += db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg": "Task Complete - Bonus যোগ হয়েছে"})
@app.route('/api/withdraw', methods=['POST'])
def api_withdraw():
    db = load_db(); j = request.json; u = get_user(db, j['id'])
    if u["balance"] < db["settings"]["min_withdraw"]: return jsonify({"msg": f"সর্বনিম্ন ৳{db['settings']['min_withdraw']} লাগবে"})
    db["withdraws"].append({"uid": j['id'], "amount": u["balance"], "number": j['number'], "method": j['method'], "time": str(datetime.now()), "status": "pending"})
    u["balance"] = 0; save_db(db); return jsonify({"msg": "Withdraw Request গেছে - 24h এ পেমেন্ট"})
@app.route('/api/support', methods=['POST'])
def api_support():
    db = load_db(); j = request.json; db["supports"].append({"uid": j['id'], "msg": j['msg'], "time": str(datetime.now())}); save_db(db); return jsonify({"msg": "Support পাঠানো হয়েছে"})

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<!-- FINAL SDK - Zone 11764581 - No InApp Auto Ad -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#060610;background:radial-gradient(circle at 50% -10%,#2a1a6b 0%,#060610 80%);color:#fff;max-width:430px;margin:0 auto;padding-bottom:120px}
.top{position:sticky;top:0;z-index:99;background:rgba(6,6,16,0.85);backdrop-filter:blur(20px);padding:14px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{background:linear-gradient(180deg,rgba(255,255,255,0.09),rgba(255,255,255,0.03));border:1px solid rgba(255,255,255,0.1);margin:12px;border-radius:20px;padding:16px}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:900;font-size:15px;color:#fff;cursor:pointer;margin-top:10px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(12,10,30,0.97);display:flex;padding:10px 0 14px;border-radius:22px 22px 0 0;border-top:1px solid rgba(255,255,255,0.1);z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.btm div.on{color:#fff}
.page{display:none}.page.active{display:block}
input,select,textarea{width:100%;padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.15);background:#0f0f1f;color:#fff;margin-top:8px}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:38px;height:38px;border-radius:50%;border:2px solid #6d4cff"><div><div style="font-weight:900">Protidiner Kaj BD</div><small style="color:#00ff88">Zone 11764581 Active ✅ Auto Ad OFF</small></div></div><div>🔔</div></div>

<div id="p-home" class="page active">
<div class="card" style="text-align:center"><div style="opacity:0.6">আপনার ব্যালেন্স</div><div style="font-size:40px;font-weight:900">৳<span id="bal">0</span></div><small>আজ <span id="ads">0</span>/50 Ads</small><div style="background:rgba(0,0,0,0.3);height:6px;border-radius:10px;margin-top:10px"><div id="prog" style="height:6px;background:#6d4cff;width:10%;border-radius:10px"></div></div></div>
<div class="card" style="border:2px dashed #6d4cff;background:linear-gradient(135deg,rgba(109,76,255,0.15),rgba(0,0,0,0.5))">
<div style="text-align:center;font-weight:900;margin-bottom:8px">📢 Official Sponsored - Company থেকে ডলার আসবে</div>
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">1️⃣ COMPANY ADS দেখুন (৳2) - Zone 11764581</button>
<button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">2️⃣ POPUP ADS - বেশি টাকা আসবে</button>
<button class="btn" style="background:#1e293b" onclick="nav('task')">3️⃣ TASK BONUS - YouTube/Telegram</button>
<button class="btn" style="background:#ea580c" onclick="nav('wallet')">4️⃣ WALLET & Bkash/Nagad Withdraw</button>
<button class="btn" style="background:#0f172a" onclick="nav('support')">5️⃣ SUPPORT BOX - এডমিনকে মেসেজ</button>
</div>
<div class="card"><b>💡 কিভাবে কোম্পানি থেকে ডলার আসে?</b><br><small style="opacity:0.7">তুমি যে Zone 11764581 বানাইছো ওটা Monetag কোম্পানির। ইউজার যখন 1️⃣ বা 2️⃣ বাটনে চাপ দিয়ে Ad দেখে, তখন Monetag তোমাকে $0.02-$0.05 দেয়। In-App অটো Ad আমি বন্ধ করে দিয়েছি, তাই Warning আসবে না।</small></div>
</div>

<div id="p-task" class="page"><div class="card"><h3>Task Bonus</h3><div id="taskList"></div></div></div>
<div id="p-wallet" class="page"><div class="card"><h3>Wallet</h3><div style="font-size:32px;font-weight:900">৳<span id="bal2">0</span></div><select id="method"><option>Bkash</option><option>Nagad</option></select><input id="num" placeholder="Bkash/Nagad Number দিন"><button class="btn" style="background:#00c853" onclick="doWith()">Withdraw করুন</button><small style="opacity:0.6">Min ৳500</small></div></div>
<div id="p-support" class="page"><div class="card"><h3>Support Box</h3><textarea id="supMsg" placeholder="আপনার সমস্যা লিখুন..."></textarea><button class="btn" style="background:#6d4cff" onclick="doSup()">পাঠান</button></div></div>

<div class="btm"><div class="on" onclick="nav('home')" id="b-home">🏠<br>Home</div><div onclick="nav('task')" id="b-task">📋<br>Task</div><div onclick="nav('wallet')" id="b-wallet">💰<br>Wallet</div><div onclick="nav('support')" id="b-support">💬<br>Support</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());
 document.getElementById('bal').innerText=r.user.balance;document.getElementById('bal2').innerText=r.user.balance;
 document.getElementById('ads').innerText=r.user.ads;document.getElementById('prog').style.width=(r.user.ads/50*100)+'%';
 let tl=document.getElementById('taskList');tl.innerHTML='';r.tasks.forEach((t,i)=>{
  let done=r.user.claimed.includes(i);
  tl.innerHTML+=`<div class="card" style="display:flex;justify-content:space-between;align-items:center"><div>${t.icon} ${t.title} - ৳${t.reward}</div><button class="btn" style="width:auto;padding:10px 16px;background:${done?'#334155':'#6d4cff'}" onclick="claim(${i})">${done?'Done':'Claim'}</button></div>`;
 });
}
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');load();}
// তোমার দেওয়া 1st কোড - Rewarded Interstitial
function watchAd(){
 if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে... 2 সেকেন্ড পর চাপুন');return;}
 show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(x=>x.json()).then(d=>{alert(d.msg);load();});});
}
// তোমার দেওয়া 2nd কোড - Rewarded Popup
function watchPop(){
 if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}
 show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid).then(x=>x.json()).then(d=>{alert('Popup থেকে '+d.msg);load();});}).catch(e=>{});
}
function claim(i){fetch('/api/claim?idx='+i+'&id='+uid).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
function doWith(){let m=document.getElementById('method').value;let n=document.getElementById('num').value;if(!n){alert('Number দিন');return;}fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,method:m})}).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
function doSup(){let msg=document.getElementById('supMsg').value;if(!msg){alert('লিখুন');return;}fetch('/api/support',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,msg:msg})}).then(x=>x.json()).then(d=>{alert(d.msg);document.getElementById('supMsg').value='';});}
load();
</script></body></html>
"""

ADMIN_HTML = """<html><head><meta charset="utf-8"><title>Admin</title></head><body style="font-family:sans-serif;padding:20px"><h2>Admin Panel - Owner 8807178385</h2><div id="data">Loading...</div><script>fetch('/api/get?id=8807178385').then(x=>x.json()).then(r=>{document.getElementById('data').innerHTML='<pre>'+JSON.stringify(r,null,2)+'</pre>'});</script></body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
