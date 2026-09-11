from flask import Flask, request, jsonify
import json, os
from datetime import datetime
app = Flask(__name__)
DB_FILE = "database.json"
ADMIN_ID = "8807178385"

DEFAULT_DB = {
    "users": {}, "withdraws": [],
    "settings": {
        "app_name": "Protidiner Kaj BD",
        "theme": "#6C5CE7",
        "welcome": 60,
        "ref_bonus": 10,
        "ad_reward": 1,
        "ad_limit": 30,
        "min_wd": 200,
        "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "bot_username": "ProtidinerKaj_BD_Bot",
        "channel_username": "ProtidinerKajBD",
        "admin_username": "ProtidinerKajBD",
        "monetag_zone": "11764581",
        "tasks": [
            {"id": "yt", "title": "YouTube video", "reward": 25, "icon": "youtube", "color": "#dc2626", "link": "https://youtube.com"},
            {"id": "tg", "title": "Join telegram", "reward": 10, "icon": "telegram", "color": "#0ea5e9", "link": "https://t.me/ProtidinerKajBD"}
        ]
    }
}

def load_db():
    if not os.path.exists(DB_FILE):
        return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE,"r",encoding="utf-8") as f:
            db=json.load(f)
            for k in DEFAULT_DB:
                if k not in db: db[k]=DEFAULT_DB[k]
            for kk in DEFAULT_DB["settings"]:
                if kk not in db["settings"]:
                    db["settings"][kk]=DEFAULT_DB["settings"][kk]
            return db
    except:
        return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    db=load_db(); s=db["settings"]
    return f"""
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{s['app_name']} - ✅ Monetag Connected</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='{s['monetag_zone']}' data-sdk='show_{s['monetag_zone']}'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
*{{font-family:system-ui,sans-serif;box-sizing:border-box}}
body{{margin:0;background:#f5f7fb;padding-bottom:85px;color:#111}}
.top-title{{background:#ccfbf1;padding:8px 14px;font-weight:700;display:flex;align-items:center;justify-content:space-between;font-size:14px;border-bottom:1px solid #99f6e0}}
.header-purple{{background:{s['theme']};color:white;padding:14px 16px;display:flex;align-items:center;gap:12px}}
.avatar-white{{width:54px;height:54px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;color:{s['theme']};font-weight:800;font-size:22px}}
.earn-card{{background:{s['theme']};color:white;border-radius:26px;padding:20px 18px;margin:16px 12px;text-align:center}}
.earn-stats{{display:flex;gap:12px;margin:16px 0}}
.earn-stat{{background:rgba(255,255,255,0.22);border-radius:16px;padding:12px;flex:1}}
.task-card{{background:white;border-radius:18px;padding:14px 16px;margin:10px 12px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,0.04)}}
.task-icon{{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white;font-size:24px}}
.btn-purple{{background:{s['theme']};color:white;border:none;padding:10px 20px;border-radius:12px;font-weight:700;cursor:pointer}}
.btn-white{{background:white;color:{s['theme']};border:none;padding:14px;border-radius:14px;width:100%;font-weight:800;font-size:15px;cursor:pointer}}
.w-input{{width:100%;padding:14px 16px;border:1px solid #e2e8f0;border-radius:14px;margin:8px 0;outline:none;background:#f8fafc;box-sizing:border-box}}
.balance-box{{background:white;border-radius:22px;padding:16px;margin:12px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}}
.ref-box{{background:#f1f5f9;border:1px solid #e2e8f0;border-radius:12px;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;margin:10px 0;font-size:13px}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:8px 0 6px 0;border-top:1px solid #e2e8f0;z-index:100}}
.b-item{{text-align:center;font-size:11px;color:#94a3b8;cursor:pointer;flex:1}}.b-item.active{{color:{s['theme']}}}.b-item i{{font-size:22px;display:block;margin-bottom:3px}}
.page{{display:none}}.page.active{{display:block}}
</style>
</head>
<body>

<div class="top-title">
    <span>{s['app_name']} - ✅ Monetag Connected</span>
    <span style="display:flex;gap:12px"><i class="fas fa-chevron-down"></i><i class="fas fa-ellipsis-v"></i></span>
</div>

<div class="header-purple">
    <div class="avatar-white">৳</div>
    <div><b id="hname">User</b><br><span>৳<span id="hbal">60.00</span></span></div>
    <div style="margin-left:auto"><i class="fas fa-check-circle" style="font-size:20px"></i></div>
</div>

<!-- HOME PAGE -->
<div id="home" class="page">
    <div class="balance-box">
        <div style="text-align:center"><div style="font-size:36px;font-weight:800;color:{s['theme']}">৳<span id="bal1">60.00</span></div><small style="color:#64748b">Your Balance</small></div>
        <p style="color:#64748b;font-size:13px;margin:12px 0 4px 0">আপনার রেফারাল লিংক:</p>
        <div class="ref-box"><span id="reflink" style="overflow:hidden;white-space:nowrap;max-width:75%">Loading...</span><button onclick="copyRef()" style="background:white;border:1px solid #e2e8f0;padding:6px 10px;border-radius:8px"><i class="far fa-copy"></i></button></div>
    </div>
    <div style="background:#134e4a;color:white;border-radius:20px;padding:16px;margin:12px"><b>অফিশিয়াল নোটিশ</b><br><small>প্রতি রেফারে {s['ref_bonus']} টাকা, প্রতি Ads এ {s['ad_reward']} টাকা। {s['min_wd']} টাকা হলেই উইথড্র।</small></div>
</div>

<!-- EARN PAGE - SCREENSHOT LIKE -->
<div id="earn" class="page active">
    <div class="earn-card">
        <div style="font-size:15px;opacity:0.95">প্রতি বিজ্ঞাপনে নিশ্চিত আয়</div>
        <div style="font-size:54px;font-weight:800;margin:6px 0">৳<span id="perAd">{s['ad_reward']}.00</span></div>
        <div class="earn-stats">
            <div class="earn-stat"><div style="font-size:12px;opacity:0.9">আজকের বিজ্ঞাপন দেখা</div><div style="font-size:22px;font-weight:700;margin-top:4px"><span id="todayCount">0</span> টি</div></div>
            <div class="earn-stat"><div style="font-size:12px;opacity:0.9">আজকের বিজ্ঞাপন আয়</div><div style="font-size:22px;font-weight:700;margin-top:4px">৳ <span id="todayIncome">0.00</span></div></div>
        </div>
        <button class="btn-white" onclick="watchAd()">▶ বিজ্ঞাপন শুরু করুন (<span id="leftAd">{s['ad_limit']}</span> টি বাকি | আজ <span id="todaySmall">0</span>/{s['ad_limit']})</button>
        <div style="margin-top:12px;font-size:12px;opacity:0.9">✅ Connected: Monetag Zone {s['monetag_zone']} - Your Earnings $0.02</div>
        <div id="lastTime" style="margin-top:6px;font-size:11px;opacity:0.8"></div>
    </div>
    <div id="taskList"></div>
</div>

<!-- SUPPORT -->
<div id="support" class="page">
    <div style="background:white;border-radius:18px;padding:16px;margin:12px">সাপোর্ট - @{s['admin_username']}</div>
</div>

<!-- WITHDRAW -->
<div id="withdraw" class="page">
    <div style="background:{s['theme']};border-radius:0 0 26px 26px;padding:22px 18px 30px 18px;color:white;text-align:center"><div>আপনার ব্যালেন্স</div><div style="font-size:44px;font-weight:800">৳<span id="wBal">60.00</span></div><div style="margin-top:8px;font-size:12px">মিনিমাম: ৳{s['min_wd']}.00</div></div>
    <div style="background:white;border-radius:20px 20px 0 0;margin-top:-18px;padding:16px">
        <input id="w_number" class="w-input" placeholder="Bkash/Nagad Number">
        <input id="w_amount" class="w-input" placeholder="Amount" type="number">
        <button style="background:{s['theme']};color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:700;margin-top:8px" onclick="doWithdraw()">Withdraw</button>
        <div id="wdHistory" style="margin-top:16px;color:#94a3b8;text-align:center">কোন হিস্ট্রি নেই</div>
    </div>
</div>

<!-- PROFILE -->
<div id="profile" class="page">
    <div style="background:{s['theme']};border-radius:22px;padding:18px;margin:12px;display:flex;gap:14px;color:white;align-items:center">
        <div style="width:60px;height:60px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;color:{s['theme']};font-size:24px">৳</div>
        <div><div style="font-size:18px;font-weight:700" id="pname">User</div><div style="font-size:12px">ID: <span id="pid">8807178385</span></div></div>
    </div>
    <div style="background:white;border-radius:16px;padding:14px;margin:8px 12px;display:flex;justify-content:space-between"><span>বর্তমান ব্যালেন্স</span><b>৳<span id="pBal">60.00</span></b></div>
    <div style="background:white;border-radius:16px;padding:14px;margin:8px 12px;display:flex;justify-content:space-between"><span>মোট Ads</span><b><span id="pAds">0</span> টি</b></div>
    <div style="margin:12px"><small>Last: <span id="lastTime2">-</span> | Joined: <span id="joined">-</span></small></div>
</div>

<div class="bottom">
    <div class="b-item" onclick="showPage('home',this)"><i class="fas fa-home"></i>হোম</div>
    <div class="b-item active" onclick="showPage('earn',this)"><i class="fas fa-list"></i>আয় করুন</div>
    <div class="b-item" onclick="showPage('support',this)"><i class="fas fa-question-circle"></i>সাপোর্ট</div>
    <div class="b-item" onclick="showPage('withdraw',this)"><i class="fas fa-credit-card"></i>উইথড্র</div>
    <div class="b-item" onclick="showPage('profile',this)"><i class="fas fa-user"></i>প্রোফাইল</div>
</div>

<script>
let UID = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || new URLSearchParams(location.search).get('id') || '8807178385';
let UNAME = window.Telegram?.WebApp?.initDataUnsafe?.user?.first_name || 'User';
function showPage(p,el){{document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById(p).classList.add('active');document.querySelectorAll('.b-item').forEach(x=>x.classList.remove('active'));el.classList.add('active')}}
function copyRef(){{navigator.clipboard.writeText(document.getElementById('reflink').innerText);alert('Copied!')}}
function load(){{
 fetch('/api/register',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID, name:UNAME}})}}).then(r=>r.json()).then(u=>{{
  document.getElementById('hname').innerText=u.name||UNAME;
  document.getElementById('pname').innerText=u.name||UNAME;
  document.getElementById('pid').innerText=UID;
  document.getElementById('hbal').innerText=u.balance.toFixed(2);
  document.getElementById('bal1').innerText=u.balance.toFixed(2);
  document.getElementById('wBal').innerText=u.balance.toFixed(2);
  document.getElementById('pBal').innerText=u.balance.toFixed(2);
  document.getElementById('pAds').innerText=u.total_ads||0;
  document.getElementById('todayCount').innerText=u.today_ads||0;
  document.getElementById('todaySmall').innerText=u.today_ads||0;
  document.getElementById('todayIncome').innerText=(u.today_ads||0)*{s['ad_reward']}+'.00';
  document.getElementById('leftAd').innerText={s['ad_limit']}-(u.today_ads||0);
  document.getElementById('lastTime').innerText=u.last_ads_time? 'Last: '+u.last_ads_time:'';
  document.getElementById('lastTime2').innerText=u.last_ads_time||'Never';
  document.getElementById('joined').innerText=u.joined||'';
  document.getElementById('reflink').innerText='https://t.me/{s['bot_username']}?start='+UID;
 }});
 fetch('/api/settings').then(r=>r.json()).then(s=>{{
  let h=''; (s.tasks||[]).forEach(t=>{{
   h+=`<div class="task-card"><div style="display:flex;gap:12px;align-items:center"><div class="task-icon" style="background:${{t.color}}"><i class="fab fa-${{t.icon}}"></i></div><div><b>${{t.title}}</b><br><small style="color:{s['theme']}">৳${{t.reward}}.00</small></div></div><button class="btn-purple" onclick="window.open('${{t.link}}')">শুরু করুন</button></div>`;
  }});
  document.getElementById('taskList').innerHTML=h;
 }});
}}
function watchAd(){{
 if(typeof show_{s['monetag_zone']}==='function'){{
  show_{s['monetag_zone']}().then(()=>{{
   fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}}).then(r=>r.json()).then(d=>{{if(d.error) alert(d.error); else {{load(); alert('৳{s['ad_reward']} Added!');}}}})
  }})
 }} else {{
  fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}}).then(r=>r.json()).then(d=>{{load(); alert('Test Ad Added!');}})
 }}
}}
function doWithdraw(){{
 fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID,number:document.getElementById('w_number').value,amount:document.getElementById('w_amount').value}})}}).then(r=>r.json()).then(d=>{{alert(d.msg||d.error); load()}})
}}
load();
</script>
</body></html>
"""

@app.route("/api/register", methods=["POST"])
def register():
    uid=str(request.json.get("user_id")); name=request.json.get("name","User"); db=load_db()
    if uid not in db["users"]:
        db["users"][uid]={"name":name,"balance":db["settings"]["welcome"],"total":db["settings"]["welcome"],"today_ads":0,"total_ads":0,"last_date":datetime.now().strftime("%d/%m/%Y"),"last_ads_time":"","joined":datetime.now().strftime("%d/%m/%Y %I:%M %p")}
        save_db(db)
    else:
        if name!="User": db["users"][uid]["name"]=name; save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid=str(request.json.get("user_id")); db=load_db(); s=db["settings"]
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y")
    if u.get("today_ads",0)>=s["ad_limit"]: return jsonify({"error":f"আজ {s['ad_limit']} টা শেষ!"}),400
    u["balance"]+=s["ad_reward"]; u["total"]+=s["ad_reward"]; u["today_ads"]+=1; u["total_ads"]+=1
    u["last_ads_time"]=datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_db(db); return jsonify(u)

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    d=request.json; uid=str(d.get("user_id")); db=load_db()
    u=db["users"][uid]; amt=int(float(d.get("amount",0)))
    if amt < db["settings"]["min_wd"]: return jsonify({"error":f"Min {db['settings']['min_wd']} Tk"})
    if u["balance"]<amt: return jsonify({"error":"Balance কম"})
    u["balance"]-=amt
    db["withdraws"].append({"user_id":uid,"number":d.get("number"),"amount":amt,"time":datetime.now().strftime("%d/%m/%Y %I:%M %p"),"status":"pending"})
    save_db(db); return jsonify({"msg":"Withdraw সফল!"})

@app.route("/api/settings")
def get_settings(): return jsonify(load_db()["settings"])

@app.route("/admin")
def admin_panel():
    aid=request.args.get("id",""); db=load_db(); s=db["settings"]
    if str(aid)!=ADMIN_ID: return f"<h2>Denied</h2>",403
    return f"<html><body style='font-family:system-ui;padding:15px'><h2>👑 {s['app_name']} ADMIN</h2><p>Users: {len(db['users'])} | Theme: {s['theme']} | Zone: {s['monetag_zone']}</p><p><a href='/'>App দেখো</a></p></body></html>"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
