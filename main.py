from flask import Flask, request, jsonify
import json, os, time
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"
ADMIN_ID = "8807178385"

DEFAULT_DB = {
    "users": {},
    "withdraws": [],
    "settings": {
        "welcome": 10, "ref": 10, "task": 2, "ad_reward": 1, "ad_limit": 30, "min_wd": 200,
        "app_name": "Protidiner Kaj BD", "theme_color": "#00b894",
        "support_link": "https://t.me/support", "notice": "প্রতিদিন ৩০ টি Ad দেখে আয় করুন!"
    }
}

def load_db():
    if not os.path.exists(DB_FILE): return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            for k,v in DEFAULT_DB.items():
                if k not in db: db[k]=v
            for k,v in DEFAULT_DB["settings"].items():
                if k not in db["settings"]: db["settings"][k]=v
            return db
    except: return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    db = load_db(); s = db["settings"]
    return f"""
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['app_name']}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='11760259' data-sdk='show_11760259'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
:root{{--main:{s['theme_color']}}}; body{{margin:0;font-family:system-ui;background:#f0f4f8;padding-bottom:85px}}
.top{{background:linear-gradient(135deg,var(--main),#6c5ce7);color:white;padding:20px;border-radius:0 0 28px 28px}}
.card{{background:white;margin:12px;border-radius:18px;padding:15px;box-shadow:0 4px 15px rgba(0,0,0,0.05)}}
.balance{{font-size:32px;font-weight:800;color:var(--main)}}
.btn{{background:var(--main);color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;font-size:16px;cursor:pointer}}
.btn2{{background:#f1f2f6;color:#2f3542;border:1px solid #ddd;padding:12px;border-radius:12px;width:100%;font-weight:bold;cursor:pointer}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #eee;z-index:100}}
.b-item{{text-align:center;font-size:11px;color:#a4b0be;cursor:pointer}}.b-item.active{{color:var(--main)}}.b-item i{{font-size:20px;display:block;margin-bottom:3px}}
.page{{display:none}}.page.active{{display:block}}
.task{{display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid #f1f2f6;border-radius:12px;margin:8px 0}}
.mActive{{border:2px solid var(--main)!important;background:#eafff5!important}}
input,select{{width:94%;padding:13px;margin:6px 0;border:1px solid #ddd;border-radius:12px}}
</style></head><body>
<div class="top">
<div style="display:flex;justify-content:space-between"><div><div style="opacity:0.8;font-size:13px">{s['app_name']}</div><div id="uname" style="font-weight:bold">User</div></div><div style="background:rgba(255,255,255,0.25);padding:6px 12px;border-radius:20px;font-size:12px" id="uid">ID:...</div></div>
<div style="margin-top:15px;background:white;color:#2f3542;border-radius:16px;padding:14px;display:flex;justify-content:space-between">
<div><div style="font-size:12px;color:#888">আপনার ব্যালেন্স</div><div class="balance" id="bal">৳ 0</div></div>
<div style="text-align:right"><div style="font-size:12px;color:#888">আজ আয়</div><div style="font-weight:bold" id="todayE">৳0</div><div style="font-size:12px" id="todayC">0/{s['ad_limit']}</div></div>
</div></div>

<div id="p1" class="page active">
<div class="card" style="background:#fffbe6;border-left:4px solid #fdcb6e"><i class="fa-solid fa-bullhorn"></i> {s['notice']}</div>
<div class="card"><h3 style="margin:0">🔥 দ্রুত আয়</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px">
<div style="background:#f8f9ff;padding:12px;border-radius:12px;text-align:center"><div style="font-size:26px">📺</div><div style="font-weight:bold">Ad দেখুন</div><div style="font-size:12px;color:#888">৳{s['ad_reward']} / Ad</div><button class="btn" style="margin-top:8px;padding:10px" onclick="nav(3)">শুরু করুন</button></div>
<div style="background:#f0fff4;padding:12px;border-radius:12px;text-align:center"><div style="font-size:26px">👥</div><div style="font-weight:bold">রেফার</div><div style="font-size:12px;color:#888">৳{s['ref']} / Refer</div><button class="btn2" style="margin-top:8px" onclick="nav(4)">শেয়ার</button></div>
</div></div></div>

<div id="p2" class="page"><div class="card"><h3>📋 Tasks</h3>
<div class="task"><div><b>Telegram Join</b><div style="font-size:12px;color:#888">+৳{s['task']}</div></div><button class="btn" style="width:auto;padding:8px 15px" onclick="doTask('tg')">Join</button></div>
<div class="task"><div><b>Daily Check-in</b><div style="font-size:12px;color:#888">+৳2</div></div><button class="btn" style="width:auto;padding:8px 15px" onclick="doTask('check')">Claim</button></div>
</div></div>

<div id="p3" class="page"><div class="card" style="text-align:center;padding:25px"><div style="font-size:55px">📺</div><h2>Ad দেখে আয়</h2><p style="color:#888">১ Ad = ৳{s['ad_reward']} | বাকি: <span id="left">{s['ad_limit']}</span> টি</p>
<button class="btn" style="padding:18px;font-size:18px" onclick="watchAd()"><i class="fa-solid fa-play"></i> Ad দেখুন</button>
<div style="margin-top:15px"><div style="background:#eee;border-radius:10px;height:12px"><div id="prog" style="background:var(--main);height:12px;width:0%;border-radius:10px"></div></div><div style="font-size:12px;margin-top:6px;color:#888"><span id="watched">0</span> / {s['ad_limit']} Completed</div></div>
</div></div>

<div id="p4" class="page"><div class="card" style="text-align:center"><div style="font-size:42px">🎁</div><h3>রেফার করে আয়</h3><p style="color:#888">প্রতি রেফারে ৳{s['ref']}</p>
<div style="background:#f1f2f6;padding:12px;border-radius:12px;word-break:break-all;font-size:13px" id="refLink">Loading...</div>
<button class="btn" style="margin-top:10px" onclick="copyRef()"><i class="fa-solid fa-copy"></i> কপি করুন</button>
<div style="display:flex;gap:10px;margin-top:15px"><div style="flex:1;background:#f8f9ff;padding:12px;border-radius:12px"><div style="font-size:20px;font-weight:bold" id="refCount">0</div><div style="font-size:12px">Total Refer</div></div><div style="flex:1;background:#f0fff4;padding:12px;border-radius:12px"><div style="font-size:20px;font-weight:bold" id="refEarn">৳0</div><div style="font-size:12px">Refer Earn</div></div></div>
</div></div>

<div id="p5" class="page">
<div class="card"><h3>💸 Wallet & Withdraw</h3>
<div style="background:#f8f9ff;padding:15px;border-radius:12px;display:flex;justify-content:space-between"><div>Balance<div class="balance" id="wBal">৳0</div><div style="font-size:12px;color:#888">Min ৳{s['min_wd']}</div></div><i class="fa-solid fa-wallet" style="font-size:32px;color:var(--main)"></i></div>
<div style="margin-top:12px">
<div style="display:flex;gap:8px;margin-bottom:8px">
<button class="btn2 mActive" id="bkBtn" onclick="setMethod('Bkash')">Bkash</button>
<button class="btn2" id="ngBtn" onclick="setMethod('Nagad')">Nagad</button>
</div>
<input id="wNumber" placeholder="Number - 01XXXXXXXXX">
<input id="wAmount" type="number" placeholder="Amount">
<button class="btn" style="background:#6c5ce7;margin-top:6px" onclick="withdraw()"><i class="fa-solid fa-paper-plane"></i> Withdraw করুন</button>
</div>
<a href="{s['support_link']}" target="_blank"><button class="btn2" style="margin-top:10px"><i class="fa-brands fa-telegram"></i> Support</button></a>
</div>
<div class="card"><h4>History</h4><div id="wHistory" style="font-size:13px;color:#888">No history</div></div>
</div>

<div class="bottom">
<div class="b-item active" onclick="nav(1)" id="b1"><i class="fa-solid fa-house"></i>Home</div>
<div class="b-item" onclick="nav(2)" id="b2"><i class="fa-solid fa-list-check"></i>Task</div>
<div class="b-item" onclick="nav(3)" id="b3"><i class="fa-solid fa-tv"></i>Ads</div>
<div class="b-item" onclick="nav(4)" id="b4"><i class="fa-solid fa-users"></i>Refer</div>
<div class="b-item" onclick="nav(5)" id="b5"><i class="fa-solid fa-wallet"></i>Wallet</div>
</div>

<script>
let userId="user_"+Math.floor(Math.random()*90000+10000); let userName="User"; let tg=window.Telegram.WebApp;
if(tg.initDataUnsafe?.user){{userId=tg.initDataUnsafe.user.id.toString(); userName=tg.initDataUnsafe.user.first_name;}}
document.getElementById("uid").innerText="ID: "+userId; document.getElementById("uname").innerText=userName;
let adReward={s['ad_reward']}; let adLimit={s['ad_limit']}; let wMethod="Bkash";
function nav(n){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active')); document.getElementById('p'+n).classList.add('active'); document.querySelectorAll('.b-item').forEach(b=>b.classList.remove('active')); document.getElementById('b'+n).classList.add('active');}}
function setMethod(m){{wMethod=m; document.getElementById("bkBtn").classList.toggle("mActive", m=="Bkash"); document.getElementById("ngBtn").classList.toggle("mActive", m=="Nagad");}}
async function init(){{
 let ref=new URLSearchParams(window.location.search).get("start")||new URLSearchParams(window.location.search).get("ref");
 let res=await fetch("/api/register",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:userId,name:userName,ref:ref}})}});
 let d=await res.json();
 document.getElementById("bal").innerText="৳ "+d.balance; document.getElementById("wBal").innerText="৳ "+d.balance;
 document.getElementById("todayC").innerText=(d.today_ads||0)+"/"+adLimit; document.getElementById("watched").innerText=d.today_ads||0;
 document.getElementById("left").innerText=adLimit-(d.today_ads||0); document.getElementById("prog").style.width=((d.today_ads||0)/adLimit*100)+"%";
 document.getElementById("refCount").innerText=d.ref_count||0; document.getElementById("refEarn").innerText="৳"+(d.ref_count||0)*{s['ref']};
 document.getElementById("refLink").innerText="https://t.me/ProtidinerKajBDBot?start="+userId;
 if(d.history){{let h=""; d.history.slice().reverse().forEach(x=>{{h+=`<div style='border-bottom:1px solid #eee;padding:6px 0'>${{x.method}} ${{x.number}} - ৳${{x.amount}} - <span style='color:${{x.status=='PENDING'?'orange':'green'}}'>${{x.status}}</span></div>`}}); document.getElementById("wHistory").innerHTML=h||"No history";}}
}}
init();
async function watchAd(){{ if(typeof show_11760259!=='function'){{alert("Ad Loading...");return;}} await show_11760259().then(async ()=>{{ let res=await fetch("/api/task_complete",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:userId}})}}); let d=await res.json(); if(d.error){{alert(d.error);return;}} init(); alert("✅ ৳"+adReward+" যোগ হয়েছে!");}});}}
function copyRef(){{navigator.clipboard.writeText(document.getElementById("refLink").innerText); alert("Copied!");}}
async function withdraw(){{ let num=document.getElementById("wNumber").value; let amt=document.getElementById("wAmount").value; if(!num||num.length<11){{alert("সঠিক নাম্বার দিন");return;}} if(!amt){{alert("Amount দিন");return;}} let res=await fetch("/api/withdraw",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:userId,amount:parseInt(amt),method:wMethod,number:num}})}}); let d=await res.json(); if(d.ok){{alert("✅ Request গেছে! "+wMethod+" "+num+" এ পাবেন"); init();}} else alert(d.error);}}
function doTask(t){{fetch("/api/do_task",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:userId,type:t}})}}).then(()=>{{init(); alert("✅ ৳{s['task']} Added");}});}}
</script></body></html>
    """

@app.route("/admin")
def admin():
    if request.args.get("id")!=ADMIN_ID: return "Unauthorized",403
    db=load_db(); s=db["settings"]
    return f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Admin FINAL</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>body{{font-family:system-ui;background:#eef2f7;margin:0;padding:10px}}.card{{background:white;padding:15px;border-radius:16px;margin-bottom:12px}} input{{width:95%;padding:11px;margin:6px 0;border:1px solid #ddd;border-radius:10px}}.btn{{border:none;padding:9px 13px;border-radius:10px;color:white;cursor:pointer;font-weight:bold}}.save{{background:#2d3436;width:100%;padding:14px}}.edit{{background:#00b894}}.ban{{background:#d63031}}.ap{{background:#0984e3}} table{{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden}} th{{background:#2d3436;color:white;padding:9px;font-size:12px}} td{{padding:8px;border-bottom:1px solid #eee;font-size:12px;text-align:center}}.tab{{display:inline-block;padding:8px 14px;background:#dfe6e9;border-radius:20px;margin:3px;cursor:pointer;font-size:13px}}.tab.active{{background:#2d3436;color:white}}</style>
</head><body>
<h2>👑 ADMIN FINAL - {s['app_name']}</h2>
<div style="display:flex;gap:8px"><div class="card" style="flex:1;text-align:center"><h2 id="totalU">0</h2>Users</div><div class="card" style="flex:1;text-align:center"><h2 id="totalW">0</h2>Pending</div><div class="card" style="flex:1;text-align:center"><h2>$~</h2>Monetag</div></div>
<div class="card"><div class="tab active" onclick="showTab('set')" id="t1">⚙️ Settings</div><div class="tab" onclick="showTab('app')" id="t2">🎨 Appearance</div><div class="tab" onclick="showTab('users')" id="t3">👥 Users</div><div class="tab" onclick="showTab('wd')" id="t4">💸 Withdraw</div></div>
<div id="tab-set" class="card"><h3>⚙️ Earning Control (A to Z)</h3>
Welcome Bonus:<input id="welcome" value="{s['welcome']}"> Refer Bonus:<input id="ref" value="{s['ref']}"> Task Reward:<input id="task" value="{s['task']}">
Ad Reward (প্রতি Ad এ কত টাকা):<input id="ad_reward" value="{s['ad_reward']}"> Ad Limit (দিনে কয়টা):<input id="ad_limit" value="{s['ad_limit']}">
Min Withdraw (কমপক্ষে কত টাকা):<input id="min_wd" value="{s['min_wd']}">
<button class="btn save" onclick="saveSettings()">💾 Save All Settings</button></div>
<div id="tab-app" class="card" style="display:none"><h3>🎨 Appearance & Profile Control</h3>
App Name:<input id="app_name" value="{s['app_name']}"> Theme Color:<input id="theme_color" value="{s['theme_color']}">
Support Link:<input id="support_link" value="{s['support_link']}"> Notice:<input id="notice" value="{s['notice']}">
<button class="btn save" style="background:{s['theme_color']}" onclick="saveSettings()">🎨 Update Design</button>
<div style="font-size:11px;color:#888;margin-top:8px">Color Codes: #00b894 সবুজ, #6c5ce7 বেগুনি, #0984e3 নীল, #e17055 কমলা</div></div>
<div id="tab-users" class="card" style="display:none"><h3>Users</h3><div style="overflow:auto"><table><tr><th>ID</th><th>Name</th><th>Bal</th><th>Ref</th><th>Total</th><th>Today</th><th>St</th><th>Action</th></tr><tbody id="users"></tbody></table></div></div>
<div id="tab-wd" class="card" style="display:none"><h3>Withdraw Requests - Bkash/Nagad</h3><div style="overflow:auto"><table><tr><th>Time</th><th>User</th><th>Method</th><th>Number</th><th>Amt</th><th>Status</th><th>Action</th></tr><tbody id="withdraws"></tbody></table></div></div>
<script>
function showTab(t){{document.getElementById('tab-set').style.display=t=='set'?'block':'none';document.getElementById('tab-app').style.display=t=='app'?'block':'none';document.getElementById('tab-users').style.display=t=='users'?'block':'none';document.getElementById('tab-wd').style.display=t=='wd'?'block':'none';document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById('t'+(t=='set'?1:t=='app'?2:t=='users'?3:4)).classList.add('active'); load();}}
async function load(){{
 let res=await fetch("/api/admin/data?id={ADMIN_ID}"); let db=await res.json();
 document.getElementById("totalU").innerText=Object.keys(db.users).length; document.getElementById("totalW").innerText=db.withdraws.filter(w=>w.status=='PENDING').length;
 let uh=""; for(let uid in db.users){{let u=db.users[uid]; uh+=`<tr><td>${{u.id}}</td><td>${{u.name||''}}</td><td>${{u.balance}}</td><td>${{u.ref_count}}</td><td>${{u.total}}</td><td>${{u.today_ads||0}}</td><td>${{u.status}}</td><td><button class="btn edit" onclick="editUser('${{u.id}}')">Edit</button> <button class="btn ban" onclick="banUser('${{u.id}}')">Ban</button></td></tr>`;}}
 document.getElementById("users").innerHTML=uh||"<tr><td colspan=8>No user</td></tr>";
 let wh=""; db.withdraws.slice().reverse().forEach(w=>{{wh+=`<tr><td>${{w.date||''}}</td><td>${{w.user}}<br><small>${{w.name||''}}</small></td><td>${{w.method||'Bkash'}}</td><td style='font-weight:bold'>${{w.number||''}}</td><td>৳${{w.amount}}</td><td>${{w.status}}</td><td>${{w.status=='PENDING'?`<button class="btn ap" onclick="approveWd('${{w.id}}')">Approve</button>`: 'Done'}}</td></tr>`;}});
 document.getElementById("withdraws").innerHTML=wh||"<tr><td colspan=7>No withdraw</td></tr>";
}}
async function saveSettings(){{
 let data={{welcome:parseInt(document.getElementById("welcome").value),ref:parseInt(document.getElementById("ref").value),task:parseInt(document.getElementById("task").value),ad_reward:parseInt(document.getElementById("ad_reward").value),ad_limit:parseInt(document.getElementById("ad_limit").value),min_wd:parseInt(document.getElementById("min_wd").value),app_name:document.getElementById("app_name").value,theme_color:document.getElementById("theme_color").value,support_link:document.getElementById("support_link").value,notice:document.getElementById("notice").value}};
 await fetch("/api/admin/settings",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify(data)}}); alert("✅ Saved! App Refresh করলে নতুন ডিজাইন আসবে"); location.reload();
}}
async function editUser(uid){{let b=prompt("নতুন Balance?"); if(b===null) return; await fetch("/api/admin/edit",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:uid,balance:b}})}}); load();}}
async function banUser(uid){{await fetch("/api/admin/ban",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:uid}})}}); load();}}
async function approveWd(id){{await fetch("/api/admin/approve_wd",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{id:id}})}}); load();}}
load();
</script></body></html>
    """

@app.route("/api/admin/data")
def admin_data():
    if request.args.get("id")!=ADMIN_ID: return jsonify({"error":"Unauth"}),403
    return jsonify(load_db())

@app.route("/api/admin/settings", methods=["POST"])
def admin_settings():
    db=load_db()
    for k,v in request.json.items(): db["settings"][k]=v
    save_db(db); return jsonify({"ok":True})

@app.route("/api/admin/edit", methods=["POST"])
def admin_edit():
    db=load_db(); uid=request.json.get("user_id")
    if uid in db["users"]: db["users"][uid]["balance"]=int(request.json.get("balance")); save_db(db)
    return jsonify({"ok":True})

@app.route("/api/admin/ban", methods=["POST"])
def admin_ban():
    db=load_db(); uid=request.json.get("user_id")
    if uid in db["users"]: db["users"][uid]["status"]="BANNED" if db["users"][uid].get("status")!="BANNED" else "OK"; save_db(db)
    return jsonify({"ok":True})

@app.route("/api/admin/approve_wd", methods=["POST"])
def approve_wd():
    db=load_db(); wid=request.json.get("id")
    for w in db["withdraws"]:
        if w["id"]==wid: w["status"]="APPROVED"
    save_db(db); return jsonify({"ok":True})

@app.route("/api/register", methods=["POST"])
def register():
    data=request.json; uid=str(data.get("user_id")); db=load_db(); s=db["settings"]
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":data.get("name","User"),"balance":s["welcome"],"ref_count":0,"total":s["welcome"],"status":"OK","today_ads":0,"last_date":datetime.now().strftime("%d/%m/%Y"),"ref_by":data.get("ref")}
        ref=data.get("ref")
        if ref and ref in db["users"]: db["users"][ref]["balance"]+=s["ref"]; db["users"][ref]["total"]+=s["ref"]; db["users"][ref]["ref_count"]+=1
        save_db(db)
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y"); save_db(db)
    # attach history
    u["history"]=[w for w in db["withdraws"] if w["user"]==uid][-5:]
    return jsonify(u)

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid=str(request.json.get("user_id")); db=load_db(); s=db["settings"]
    if uid not in db["users"]: return jsonify({"error":"not found"}),404
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y")
    if u.get("today_ads",0)>=s["ad_limit"]: return jsonify({"error":f"আজ {s['ad_limit']} টা শেষ!"}),400
    u["balance"]+=s["ad_reward"]; u["total"]+=s["ad_reward"]; u["today_ads"]=u.get("today_ads",0)+1; save_db(db); return jsonify(u)

@app.route("/api/do_task", methods=["POST"])
def do_task():
    uid=str(request.json.get("user_id")); db=load_db(); s=db["settings"]
    if uid in db["users"]: db["users"][uid]["balance"]+=s["task"]; db["users"][uid]["total"]+=s["task"]; save_db(db)
    return jsonify({"ok":True})

@app.route("/api/withdraw", methods=["POST"])
def withdraw_req():
    uid=str(request.json.get("user_id")); amt=int(request.json.get("amount",0)); method=request.json.get("method","Bkash"); number=request.json.get("number","")
    db=load_db(); s=db["settings"]
    if uid not in db["users"]: return jsonify({"error":"User not found"}),404
    if amt < s["min_wd"]: return jsonify({"error":f"Min {s['min_wd']} টাকা"}),400
    if db["users"][uid]["balance"] < amt: return jsonify({"error":"Balance কম"}),400
    if len(number) < 11: return jsonify({"error":"নাম্বার ভুল"}),400
    db["users"][uid]["balance"]-=amt
    db["withdraws"].append({"id":str(int(time.time()*1000)),"user":uid,"name":db["users"][uid].get("name",""),"amount":amt,"method":method,"number":number,"status":"PENDING","date":datetime.now().strftime("%d/%m/%Y %H:%M")})
    save_db(db); return jsonify({"ok":True})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
