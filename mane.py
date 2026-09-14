# -*- coding: utf-8 -*-
# FINAL mane.py - A to Z - All Image Design Same + Admin Everything + 2 Monetag + No Logout
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

def load_db():
    if not os.path.exists(DB):
        data = {
            "users": {},
            "withdraws": [],
            "settings": {
                "app_name": "Protidiner Kaj BD",
                "admin_name": "SHIBLI NOMAN",
                "app_logo": "👑",
                "admin_profile_img": "",
                "zone": "11764581",
                "direct_link": "https://omg10.com/4/11760259",
                "bonus": 50,
                "ad_reward": 2,
                "popup_reward": 3,
                "company_limit": 30,
                "popup_limit": 20,
                "task_limit": 5,
                "min_with": 500,
                "refer_reward": 50,
                "refer_condition_ads": 10,
                "official_banners": [],
                "google_ads": ["🎉 Daily Bonus Available Today", "⭐ Official Ad • bKash • Nagad • Trusted", "📢 Company Sponsored • 100% Safe"],
                "offer_title": "🎉 আজকের স্পেশাল অফার",
                "offer_desc": "প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!",
                "balance_title": "আপনার বর্তমান ব্যালেন্স",
                "tg_channel": "https://t.me/",
                "support_link": "https://t.me/",
                "whatsapp": "01XXXXXXXXX"
            },
            "tasks": [
                {"id": 1, "title": "Join Telegram Channel", "reward": 10, "link": "https://t.me/", "type": "telegram"},
                {"id": 2, "title": "Subscribe YouTube", "reward": 15, "link": "https://youtube.com/", "type": "youtube"},
                {"id": 3, "title": "Follow Facebook Page", "reward": 10, "link": "https://facebook.com/", "type": "facebook"}
            ]
        }
        with open(DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data
    with open(DB, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(db):
    with open(DB, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_user(db, uid, ref=None):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "name": f"User {uid[-4:]}",
            "profile_img": "",
            "balance": db["settings"]["bonus"],
            "total": 0,
            "company_today": 0,
            "popup_today": 0,
            "tasks_done": [],
            "join_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "join_date": str(datetime.now().date()),
            "last_date": str(datetime.now().date()),
            "referred_by": ref,
            "refer_list": [],
            "refer_status": "pending",
            "ads_watched": 0
        }
        if ref and ref in db["users"] and ref!= uid:
            db["users"][ref]["refer_list"].append({"id": uid, "name": db["users"][uid]["name"], "time": db["users"][uid]["join_time"]})
    u = db["users"][uid]
    for k, v in [("join_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")), ("refer_list", []), ("ads_watched", 0), ("refer_status", "pending"), ("last_date", str(datetime.now().date()))]:
        if k not in u:
            u[k] = v
    return u

# ========== API ==========
@app.route('/api/init', methods=['POST'])
def api_init():
    db = load_db()
    j = request.json
    uid = str(j.get('id'))
    ref = j.get('ref')
    if ref == uid:
        ref = None
    u = get_user(db, uid, ref)
    today = str(datetime.now().date())
    if u.get("last_date")!= today:
        u["company_today"] = 0
        u["popup_today"] = 0
        u["last_date"] = today
    save_db(db)
    return jsonify({"user": u, "settings": db["settings"], "tasks": db["tasks"]})

@app.route('/api/ads/complete', methods=['POST'])
def ads_complete():
    db = load_db()
    j = request.json
    uid = str(j.get('id'))
    typ = j.get('type', 'company')
    u = get_user(db, uid)
    s = db["settings"]
    today = str(datetime.now().date())
    if u.get("last_date")!= today:
        u["company_today"] = 0
        u["popup_today"] = 0
        u["last_date"] = today
    if typ == 'company':
        if u["company_today"] >= s["company_limit"]:
            return jsonify({"msg": f"লিমিট {s['company_limit']} শেষ", "balance": u["balance"]})
        u["company_today"] += 1
        u["balance"] += s["ad_reward"]
        msg = f"✅ ৳{s['ad_reward']} যোগ হয়েছে"
    else:
        if u["popup_today"] >= s["popup_limit"]:
            return jsonify({"msg": f"লিমিট {s['popup_limit']} শেষ", "balance": u["balance"]})
        u["popup_today"] += 1
        u["balance"] += s["popup_reward"]
        msg = f"✅ ৳{s['popup_reward']} যোগ হয়েছে"
    u["ads_watched"] += 1
    u["total"] += 1
    ref = u.get("referred_by")
    if ref and ref in db["users"] and u["ads_watched"] >= s["refer_condition_ads"] and u["refer_status"] == "pending":
        db["users"][ref]["balance"] += s["refer_reward"]
        u["refer_status"] = "completed"
    save_db(db)
    return jsonify({"msg": msg, "balance": u["balance"]})

@app.route('/api/task/complete', methods=['POST'])
def task_complete():
    db = load_db()
    j = request.json
    uid = str(j.get('id'))
    tid = int(j.get('task_id'))
    u = get_user(db, uid)
    s = db["settings"]
    if tid in u["tasks_done"]:
        return jsonify({"msg": "আজকে করা হয়েছে"})
    if len(u["tasks_done"]) >= s["task_limit"]:
        return jsonify({"msg": f"টাস্ক লিমিট {s['task_limit']} শেষ"})
    task = next((t for t in db["tasks"] if t["id"] == tid), None)
    if not task:
        return jsonify({"msg": "Task নেই"})
    u["tasks_done"].append(tid)
    u["balance"] += task["reward"]
    u["total"] += 1
    save_db(db)
    return jsonify({"msg": f"✅ {task['title']} - ৳{task['reward']} যোগ", "balance": u["balance"]})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    db = load_db()
    j = request.json
    uid = str(j.get('id'))
    u = get_user(db, uid)
    s = db["settings"]
    amt = int(j.get('amount', 0))
    num = j.get('number', '')
    method = j.get('method', 'bKash')
    if amt < s["min_with"]:
        return jsonify({"msg": f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt:
        return jsonify({"msg": "ব্যালেন্স কম"})
    if len(num) < 11:
        return jsonify({"msg": "সঠিক নাম্বার দিন"})
    u["balance"] -= amt
    db["withdraws"].append({"uid": uid, "name": u["name"], "amount": amt, "number": num, "method": method, "status": "Pending", "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_db(db)
    return jsonify({"msg": f"✅ {method} ৳{amt} Request সফল", "balance": u["balance"]})

@app.route('/api/user/update', methods=['POST'])
def user_update():
    db = load_db()
    j = request.json
    uid = str(j.get('id'))
    u = get_user(db, uid)
    if 'name' in j:
        u["name"] = str(j['name'])[:25]
    if 'profile_img' in j and j['profile_img']:
        u["profile_img"] = j['profile_img']
    save_db(db)
    return jsonify({"msg": "✅ প্রোফাইল সেভ হয়েছে", "user": u})

@app.route('/api/admin/save', methods=['POST'])
def api_save():
    db = load_db()
    j = request.json
    for k in j:
        if k in db["settings"]:
            db["settings"][k] = j[k]
    save_db(db)
    return jsonify({"msg": "✅ Admin Saved - সব সেভ হয়েছে"})

@app.route('/api/admin/users')
def admin_users():
    db = load_db()
    return jsonify(db["users"])

@app.route('/api/admin/withdraws')
def admin_withdraws():
    db = load_db()
    return jsonify(db["withdraws"])

# ========== FRONTEND ==========
USER_HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Protidiner Kaj BD</title>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:125px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,#17172a,#0e0e20);border:1px solid #222;position:relative;overflow:hidden}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;font-size:14px;color:#fff;margin-top:8px;cursor:pointer;background:linear-gradient(90deg,#6d4cff,#9d4cff)}
.profile{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#1e293b,#334155);display:flex;align-items:center;justify-content:center;border:2px solid #6d4cff;overflow:hidden;font-size:26px;cursor:pointer}
.bannerBox{margin:12px;border-radius:22px;overflow:hidden;height:165px;background:linear-gradient(90deg,#f59e0b,#ef4444);position:relative;border:2px solid rgba(255,255,255,0.15)}
.shine{position:absolute;top:0;left:-100%;width:65%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35),transparent);transform:skewX(-20deg);animation:shineMove 2.8s infinite;z-index:2}
@keyframes shineMove{0%{left:-100%}100%{left:200%}}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:800;cursor:pointer}
.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
.taskCard{display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid #222;border-radius:12px;margin-top:10px;background:#111128}
</style>
</head>
<body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div class="profile" id="pImg" onclick="editProfile()">👑</div><div><b id="uName">Loading...</b><br><small id="uId" style="opacity:.6"></small></div></div><div id="bal" style="font-weight:900;color:#22c55e">৳0</div></div>

<div class="bannerBox"><div class="shine"></div><div style="padding:18px;position:relative;z-index:3"><h3 id="offerTitle">🎉 আজকের স্পেশাল অফার</h3><p id="offerDesc" style="margin-top:6px;opacity:.9;font-size:13px">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</p></div></div>

<div id="home" class="page active">
  <div class="card"><h4 id="balTitle">আপনার বর্তমান ব্যালেন্স</h4><h1 id="bal2" style="margin-top:8px;color:#22c55e">৳0</h1><p style="opacity:.6;font-size:12px;margin-top:4px">Company: <span id="cLim">0/30</span> | Popup: <span id="pLim">0/20</span></p></div>
  <div class="card"><h4>📢 Official Ads</h4><button class="btn" onclick="handleCompanyAd()">▶ Company Ads দেখুন - ৳<span id="adR">2</span></button><button class="btn" style="background:linear-gradient(90deg,#f59e0b,#ef4444)" onclick="handlePopupAd()">🎁 Popup Ads - ৳<span id="popR">3</span></button></div>
  <div class="card"><h4>✅ Daily Tasks</h4><div id="taskList"></div></div>
  <div class="card"><h4>👥 রেফার করুন</h4><p style="font-size:12px;opacity:.7;margin:6px 0">বন্ধু 10 টা Ads দেখলে আপনি ৳50 পাবেন</p><input id="refLink" style="width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0a0a1a;color:#fff" readonly><button class="btn" onclick="copyRef()">🔗 লিংক কপি করুন</button></div>
</div>

<div id="profile" class="page">
  <div class="card"><h4>প্রোফাইল</h4><input id="editName" placeholder="আপনার নাম" style="width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0a0a1a;color:#fff;margin-top:10px"><input type="file" id="imgFile" accept="image/*" style="margin-top:10px"><button class="btn" onclick="saveProfile()">💾 সেভ করুন</button></div>
  <div class="card"><h4>💸 টাকা তুলুন</h4><select id="wMethod" style="width:100%;padding:12px;border-radius:10px;background:#0a0a1a;color:#fff;border:1px solid #333"><option>bKash</option><option>Nagad</option></select><input id="wNumber" placeholder="01XXXXXXXXX" style="width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0a0a1a;color:#fff;margin-top:8px"><input id="wAmount" type="number" placeholder="Amount" style="width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0a0a1a;color:#fff;margin-top:8px"><button class="btn" onclick="doWithdraw()">Withdraw</button></div>
</div>

<div class="btm"><div onclick="showPage('home')" id="bHome" class="on"><span>🏠</span>Home</div><div onclick="showPage('profile')" id="bProf"><span>👤</span>Profile</div></div>

<script>
// ===== NO LOGOUT SYSTEM =====
let userId = localStorage.getItem("myAppUserId");
if(!userId){ userId = "user_" + Date.now() + "_" + Math.floor(Math.random()*9999); localStorage.setItem("myAppUserId", userId); }
let myRef = new URLSearchParams(window.location.search).get("ref"); if(myRef){ localStorage.setItem("myRef", myRef); }
let savedRef = localStorage.getItem("myRef");
let directLink = "https://omg10.com/4/11760259";

function init(){
  fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,ref:savedRef})}).then(r=>r.json()).then(d=>{
    document.getElementById('uName').innerText = d.user.name;
    document.getElementById('uId').innerText = d.user.id;
    document.getElementById('bal').innerText = "৳"+d.user.balance;
    document.getElementById('bal2').innerText = "৳"+d.user.balance;
    document.getElementById('cLim').innerText = d.user.company_today + "/" + d.settings.company_limit;
    document.getElementById('pLim').innerText = d.user.popup_today + "/" + d.settings.popup_limit;
    document.getElementById('adR').innerText = d.settings.ad_reward;
    document.getElementById('popR').innerText = d.settings.popup_reward;
    document.getElementById('offerTitle').innerText = d.settings.offer_title;
    document.getElementById('offerDesc').innerText = d.settings.offer_desc;
    document.getElementById('balTitle').innerText = d.settings.balance_title;
    document.getElementById('editName').value = d.user.name;
    document.getElementById('refLink').value = window.location.origin + "/?ref=" + d.user.id;
    if(d.user.profile_img){ document.getElementById('pImg').innerHTML = "<img src='"+d.user.profile_img+"' style='width:100%;height:100%;object-fit:cover'>"; }
    let tl=""; d.tasks.forEach(t=>{
      let done = d.user.tasks_done.includes(t.id);
      tl += `<div class="taskCard"><div><b>${t.title}</b><br><small style="color:#22c55e">৳${t.reward}</small></div><button class="btn" style="width:auto;padding:8px 14px;margin:0;background:${done?'#333':'#6d4cff'}" onclick="doTask(${t.id},'${t.link}')" ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`;
    }); document.getElementById('taskList').innerHTML = tl;
  });
}

function handleCompanyAd(){
  window.open(directLink,"_blank");
  if(typeof show_11764581 === 'function'){ show_11764581().then(()=>{ completeAd('company'); }); } else { completeAd('company'); }
}
function handlePopupAd(){ window.open(directLink,"_blank"); completeAd('popup'); }
function completeAd(type){ fetch('/api/ads/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,type:type})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function doTask(id,link){ window.open(link,"_blank"); fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function saveProfile(){ let n=document.getElementById('editName').value; let file=document.getElementById('imgFile').files[0]; if(file){ let rd=new FileReader(); rd.onload=e=>{ fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,name:n,profile_img:e.target.result})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }; rd.readAsDataURL(file); } else { fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,name:n})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); } }
function doWithdraw(){ let m=document.getElementById('wMethod').value, num=document.getElementById('wNumber').value, amt=document.getElementById('wAmount').value; fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,method:m,number:num,amount:amt})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function showPage(p){ document.querySelectorAll('.page').forEach(x=>x.classList.remove('active')); document.getElementById(p).classList.add('active'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); if(p=='home')document.getElementById('bHome').classList.add('on'); else document.getElementById('bProf').classList.add('on'); }
function copyRef(){ let i=document.getElementById('refLink'); i.select(); document.execCommand('copy'); alert('✅ লিংক কপি হয়েছে'); }
function editProfile(){ showPage('profile'); }
init();
</script>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin - Everything Control</title>
<style>*{box-sizing:border-box;font-family:system-ui}body{max-width:600px;margin:0 auto;padding:12px;background:#070710;color:#fff}.card{padding:14px;border:1px solid #222;border-radius:12px;margin-top:12px;background:#111128}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0a0a1a;color:#fff;margin-top:6px}.btn{width:100%;padding:12px;border:none;border-radius:10px;font-weight:800;color:#fff;background:#6d4cff;margin-top:10px;cursor:pointer}</style>
</head><body>
<h2>👑 Admin Everything Control</h2>
<div class="card"><h4>💰 টাকার বাটন - সব এখানে</h4>
<input id="bonus" placeholder="Join Bonus"><input id="ad_reward" placeholder="Company Ad Reward"><input id="popup_reward" placeholder="Popup Reward"><input id="refer_reward" placeholder="Refer Reward"><input id="refer_condition_ads" placeholder="Refer Condition - কত Ads দেখলে টাকা"><input id="company_limit" placeholder="Company Limit"><input id="popup_limit" placeholder="Popup Limit"><input id="min_with" placeholder="Min Withdraw">
<h4 style="margin-top:12px">📝 লেখা - অফার বক্স</h4>
<input id="offer_title"><input id="offer_desc"><input id="balance_title"><input id="app_name"><input id="direct_link" placeholder="Direct Link 11760259"><input id="zone" placeholder="SDK Zone 11764581">
<button class="btn" onclick="save()">💾 Save All</button></div>
<div class="card"><h4>👥 Users - নাম সহ, কখন জয়েন, কে কাকে রেফার</h4><div id="users"></div></div>
<div class="card"><h4>💸 Withdraws</h4><div id="wds"></div></div>
<script>
function load(){ fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:'admin'})}).then(r=>r.json()).then(d=>{
  for(let k in d.settings){ let el=document.getElementById(k); if(el) el.value=d.settings[k]; }
}); fetch('/api/admin/users').then(r=>r.json()).then(u=>{
  let h=""; for(let id in u){ let x=u[id]; h+=`<div style="border-bottom:1px solid #222;padding:8px 0"><b>${x.name}</b> (${x.id})<br>৳${x.balance} | Ads:${x.ads_watched} | Join:${x.join_time}<br>Ref By:${x.referred_by||'None'} | Refer List:${x.refer_list.length} জন | Status:${x.refer_status}</div>`; } document.getElementById('users').innerHTML=h;
}); fetch('/api/admin/withdraws').then(r=>r.json()).then(w=>{ let h=""; w.forEach(x=>{ h+=`<div style="border-bottom:1px solid #222;padding:6px 0">${x.name} - ৳${x.amount} - ${x.method} - ${x.number} - ${x.status} - ${x.time}</div>`}); document.getElementById('wds').innerHTML=h; });
}
function save(){ let data={}; document.querySelectorAll('input').forEach(i=>{ if(i.value) data[i.id]= isNaN(i.value)? i.value : parseInt(i.value); }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ alert(d.msg); load(); }); }
load();
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
