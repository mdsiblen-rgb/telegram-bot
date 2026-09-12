# -*- coding: utf-8 -*-
# Final 500 Lines - Token 11764581 - Admin 8807178385 - Banner Slider 3 Pics
import os
import json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database.json'

def default_db():
    return {
        "users": {},
        "withdraws": [],
        "settings": {
            "app_name": "প্রতিদিনের কাজ BD",
            "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "bkash_logo": "https://freepnglogo.com/images/all-images/bkash-logo-png-1024x790-1.png",
            "nagad_logo": "https://freelogopng.com/images/all-img/1657044418nagad-logo-png.png",
            "welcome_bonus": 60,
            "ad_reward": 2,
            "ad_limit": 100,
            "min_withdraw": 1000,
            "ref_bonus": 20,
            "official_title": "আফাশিয়াল নোটস",
            "official_desc": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন",
            "official_live": "LIVE",
            "home_ad_top_title": "🎬 🔥 স্পেশাল অফার - আজকের বোনাস",
            "home_ad_btn": "▶️ MINI BOY ADS দেখুন - ৳2 পাবেন",
            "home_ad_zone_text": "Zone: 11764581 - Monetag Mini Boy - Token 11764581",
            "home_ad_zone": "11764581",
            "tasks_header": "📋 আজকের 9 টি টাস্ক - সবগুলোতে Mini Boy Ad বসানো আছে",
            "support_title": "💬 সাপোর্ট সেন্টার",
            "support_desc": "যেকোনো সমস্যায় আমাদের সাথে যোগাযোগ করুন। আমরা ২৪ ঘণ্টার মধ্যে Reply দেব।\nএই লেখাটি এডমিন প্যানেল থেকে পরিবর্তন করতে পারবেন।",
            "support_tg": "https://t.me/ProtidinerKajBD",
            "support_channel": "https://t.me/ProtidinerKajBD",
            "support_rules": "📜 নিয়ম:\n১. প্রতিদিন ১০০ টা Ad দেখতে পারবেন\n২. ভুল নাম্বারে Withdraw দিলে টাকা পাবেন না\n৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন\n৪. Fake Refer করলে Ban",
            "ref_bottom_title": "📖 কিভাবে রেফার কাজ করে?",
            "ref_bottom_desc": "১. আপনার লিংক কপি করুন\n২. বন্ধুকে শেয়ার করুন\n৩. বন্ধু জয়েন করলে সাথে সাথে ৳20 পাবেন\n৪. বন্ধু Ad দেখলেও বোনাস\n\nএই লেখাটি Admin থেকে Change করতে পারবেন।",
            "banner1": "https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2": "https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3": "https://img.freepik.com/free-vector/earning-money-online-concept-landing-page_52683-25203.jpg"
        },
        "tasks": [
            {"title": "YouTube Channel Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Telegram Channel Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Facebook Page Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Company Task 1 - Website Visit", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Company Task 2 - Telegram Group Join", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Company Task 3 - Post Like", "reward": 20, "link": "https://t.me", "color": "#be123c", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Company Task 4 - Post Share", "reward": 20, "link": "https://t.me", "color": "#065f46", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Company Task 5 - Comment Task", "reward": 20, "link": "https://t.me", "color": "#2563eb", "btn": "👉 Claim + Watch Mini Boy Ad"},
            {"title": "Company Task 6 - Refer 3 Friend", "reward": 20, "link": "https://t.me", "color": "#d97706", "btn": "👉 Claim + Watch Mini Boy Ad"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d = default_db()
        save_db(d)
        return d
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            d = json.load(f)
            dd = default_db()
            for k, v in dd["settings"].items():
                if k not in d["settings"]:
                    d["settings"][k] = v
            if "tasks" not in d:
                d["tasks"] = dd["tasks"]
            return d
    except:
        d = default_db()
        save_db(d)
        return d

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def get_user(db, uid):
    uid = str(uid)
    today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "balance": db["settings"]["welcome_bonus"],
            "ads_watched": 0,
            "ads_today": 0,
            "last_date": today,
            "claimed": [],
            "ref_count": 0,
            "total_earn": db["settings"]["welcome_bonus"]
        }
    u = db["users"][uid]
    if u.get("last_date")!= today:
        u["ads_today"] = 0
        u["last_date"] = today
    return u

@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin():
    if request.args.get('id')!= '8807178385':
        return "Unauthorized - Add?id=8807178385 - Admin ID 8807178385 - Token 11764581", 403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id', '8807178385')
    db = load_db()
    u = get_user(db, uid)
    save_db(db)
    top = sorted(db["users"].values(), key=lambda x: x.get('ref_count', 0), reverse=True)[:5]
    user_withdraws = [w for w in db["withdraws"] if str(w["uid"]) == str(uid)]
    return jsonify({
        "user": u,
        "settings": db["settings"],
        "tasks": db["tasks"],
        "withdraws": user_withdraws,
        "top_users": top
    })

@app.route('/api/reward')
def reward():
    db = load_db()
    uid = request.args.get('id')
    u = get_user(db, uid)
    if u["ads_today"] >= db["settings"]["ad_limit"]:
        return jsonify({"msg": "আজকের লিমিট শেষ!"})
    u["balance"] += db["settings"]["ad_reward"]
    u["total_earn"] += db["settings"]["ad_reward"]
    u["ads_watched"] += 1
    u["ads_today"] += 1
    save_db(db)
    return jsonify({"msg": f"Mini Boy Token 11764581 - ৳{db['settings']['ad_reward']} পেয়েছেন!"})

@app.route('/api/claim_task')
def claim_task():
    db = load_db()
    idx = int(request.args.get('idx'))
    uid = request.args.get('id')
    u = get_user(db, uid)
    if idx in u["claimed"]:
        return jsonify({"msg": "এই টাস্ক করেছেন"})
    u["claimed"].append(idx)
    u["balance"] += db["tasks"][idx]["reward"]
    u["total_earn"] += db["tasks"][idx]["reward"]
    save_db(db)
    return jsonify({"msg": "Task Complete! Token 11764581"})

@app.route('/api/withdraw')
def withdraw():
    db = load_db()
    uid = request.args.get('id')
    amt = int(request.args.get('amount', 0))
    num = request.args.get('number')
    method = request.args.get('method', 'bKash')
    u = get_user(db, uid)
    if amt < db["settings"]["min_withdraw"]:
        return jsonify({"msg": f"Min {db['settings']['min_withdraw']} Taka"})
    if u["balance"] < amt:
        return jsonify({"msg": "Balance কম"})
    u["balance"] -= amt
    db["withdraws"].append({
        "uid": uid,
        "amount": amt,
        "number": num,
        "method": method,
        "time": str(datetime.now()),
        "status": "Pending"
    })
    save_db(db)
    return jsonify({"msg": "Withdraw Request Success! Token 11764581"})

@app.route('/api/admin/full')
def a_full():
    return jsonify(load_db())

@app.route('/api/admin/save_settings', methods=['POST'])
def a_save():
    db = load_db()
    j = request.json
    for k, v in j.items():
        if k in db["settings"]:
            db["settings"][k] = v
        if k == "tasks":
            db["tasks"] = v
    save_db(db)
    return jsonify({"msg": "Saved! Token 11764581 - Admin 8807178385"})

@app.route('/api/admin/approve')
def a_approve():
    db = load_db()
    idx = int(request.args.get('idx', 0))
    if 0 <= idx < len(db["withdraws"]):
        db["withdraws"].pop(idx)
        save_db(db)
        return jsonify({"msg": "Approved & Paid! Token 11764581"})
    return jsonify({"msg": "Error"})

# ==========================================================
# USER HTML - 400+ LINES EXPANDED VERSION WITH BANNER SLIDER
# Token 11764581 - Admin 8807178385
# ==========================================================
USER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - Token 11764581 - Admin 8807178385</title>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{
 box-sizing:border-box;
 margin:0;
 padding:0;
 font-family:Hind Siliguri,sans-serif;
}
body{
 background:#0a1222;
 color:#fff;
 max-width:430px;
 margin:0 auto;
 padding-bottom:140px;
}
.top{
 background:linear-gradient(135deg,#1e3a8a,#0f172a);
 padding:16px;
 border-radius:0 0 24px 24px;
 display:flex;
 justify-content:space-between;
 align-items:center;
 position:sticky;
 top:0;
 z-index:10;
}
.bal{
 color:#22c55e;
 font-size:44px;
 font-weight:900;
}
.card{
 background:#162032;
 margin:12px;
 border-radius:18px;
 padding:14px;
 border:1px solid #22314a;
}
.btn{
 width:100%;
 padding:13px;
 border:none;
 border-radius:12px;
 font-weight:800;
 cursor:pointer;
 color:#fff;
 font-size:14px;
}
.btm{
 position:fixed;
 bottom:0;
 left:50%;
 transform:translateX(-50%);
 width:100%;
 max-width:430px;
 background:#121d32;
 display:flex;
 border-top:1px solid #23344a;
 padding:12px 0 14px 0;
 z-index:99;
}
.btm div{
 flex:1;
 text-align:center;
 color:#94a3b8;
 font-size:11px;
 cursor:pointer;
 line-height:1.2;
}
.btm div.on{
 color:#38bdf8;
}
.inp{
 width:100%;
 padding:12px;
 border-radius:12px;
 border:1px solid #334155;
 background:#0f172a;
 color:#fff;
 margin-top:8px;
}
.grid2{
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:10px;
}
.stat{
 background:#0f172a;
 border:1px solid #22314a;
 border-radius:14px;
 padding:12px;
}
.stat b{
 color:#38bdf8;
}
.support{
 background:linear-gradient(135deg,#1e293b,#0f172a);
 border:1px solid #38bdf8;
}
.sbtn{
 display:flex;
 gap:10px;
 margin-top:12px;
}
.sbtn a{
 flex:1;
 text-align:center;
 padding:12px;
 border-radius:12px;
 text-decoration:none;
 font-weight:800;
 color:#fff;
}
.spacer{
 height:60px;
 width:100%;
 display:block;
}
.live{
 width:54px;
 height:54px;
 border-radius:50%;
 background:#22c55e;
 color:#000;
 display:flex;
 align-items:center;
 justify-content:center;
 font-weight:900;
 font-size:12px;
}
.mcard{
 flex:1;
 background:#0f172a;
 border:2px solid #334155;
 border-radius:14px;
 padding:10px;
 text-align:center;
 cursor:pointer;
}
.mcard.sel{
 border-color:#e2136e;
}
/* Company Banner Slider - 3 Pics Auto Change */
.slider{
 position:relative;
 margin:12px;
 border-radius:18px;
 overflow:hidden;
 height:170px;
 border:1px solid #22314a;
 background:#000;
}
.slides{
 display:flex;
 transition:transform 0.6s ease;
 width:300%;
 height:170px;
}
.slide{
 min-width:100%;
 height:170px;
}
.slide img{
 width:100%;
 height:170px;
 object-fit:cover;
}
.dots{
 position:absolute;
 bottom:10px;
 left:50%;
 transform:translateX(-50%);
 display:flex;
 gap:6px;
}
.dot{
 width:8px;
 height:8px;
 border-radius:50%;
 background:rgba(255,255,255,0.4);
}
.dot.on{
 background:#38bdf8;
 width:20px;
 border-radius:10px;
}
.badge{
 position:absolute;
 top:8px;
 left:8px;
 background:rgba(0,0,0,0.6);
 padding:4px 10px;
 border-radius:20px;
 font-size:11px;
 border:1px solid #38bdf8;
}
</style>
</head>
<body>

<div class="top">
<div>
<div style="opacity:.8;font-size:13px">প্রতিদিনের কাজ BD - Token 11764581 - Admin 8807178385</div>
<div class="bal">৳ <span id="bal">60</span></div>
<div style="font-size:12px;opacity:.8">Ads: <span id="ads">0</span>/100 | Bonus: ৳<span id="bonus">60</span></div>
</div>
<img id="cLogo" src="" style="width:50px;height:50px;border-radius:50%;background:#fff">
</div>

<div id="p-home">
<div class="card" style="background:linear-gradient(90deg,#1e40af,#0f766e);display:flex;justify-content:space-between;align-items:center">
<div>
<div style="font-weight:800" id="offTitle">আফাশিয়াল নোটস</div>
<div style="font-size:13px;opacity:.9" id="offDesc">প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন</div>
</div>
<div class="live" id="offLive">LIVE</div>
</div>

<!-- Company 3 Banner Slider - Auto Change Every 3 Sec - Admin Editable -->
<div class="slider" id="bannerSlider">
<div class="badge">📢 কোম্পানির বিজ্ঞাপন - Token 11764581</div>
<div class="slides" id="slides">
<div class="slide"><img id="b1" src=""></div>
<div class="slide"><img id="b2" src=""></div>
<div class="slide"><img id="b3" src=""></div>
</div>
<div class="dots">
<div class="dot on" id="d0"></div>
<div class="dot" id="d1"></div>
<div class="dot" id="d2"></div>
</div>
</div>

<div class="card">
<div style="font-weight:800;margin-bottom:8px" id="adTopTitle">🎬 🔥 স্পেশাল অফার - আজকের বোনাস</div>
<button class="btn" style="background:#0ea5e9" onclick="watchAd()" id="adBtn">▶️ MINI BOY ADS দেখুন - ৳2 পাবেন - Token 11764581</button>
<div style="font-size:11px;opacity:.5;margin-top:6px" id="adZone">Zone: 11764581 - Monetag Mini Boy - Token 11764581</div>
</div>

<div class="card">
<div style="font-weight:800" id="taskHead">📋 আজকের 9 টি টাস্ক - Token 11764581</div>
</div>

<div id="homeTasks"></div>
<div class="spacer"></div>
</div>

<div id="p-tasks" style="display:none">
<div class="card"><div style="font-weight:800">📋 সব টাস্ক - Token 11764581 - Admin 8807178385</div></div>
<div id="allTasks"></div>
<div class="spacer"></div>
</div>

<div id="p-refer" style="display:none">
<div class="card">
<div style="font-weight:800;font-size:18px">👥 Refer & Earn ৳<span id="refBonus">20</span> - Token 11764581</div>
<div class="inp" id="refLink" style="word-break:break-all"></div>
<button class="btn" style="background:#2563eb;margin-top:10px" onclick="copyRef()">📋 Copy Link</button>
<div style="display:flex;justify-content:space-between;margin-top:12px">
<div>Total Refer: <b id="refCount">0</b></div>
<div>Total Earn: ৳<span id="refEarn">0</span></div>
</div>
</div>
<div class="card" style="border:1px solid #22c55e">
<div style="font-weight:800;font-size:16px" id="refBottomTitle"></div>
<div style="font-size:13px;margin-top:8px;white-space:pre-line;opacity:.85;line-height:1.6" id="refBottomDesc"></div>
<div style="background:#0f172a;border-radius:12px;padding:10px;margin-top:12px">
<div style="font-weight:800">🏆 Top 5 Referrer - Admin 8807178385</div>
<div id="refLeader" style="font-size:13px;margin-top:6px;line-height:1.8"></div>
</div>
</div>
<div class="spacer"></div>
</div>

<div id="p-wallet" style="display:none">
<div class="card">
<div style="font-weight:800">💰 Wallet - Token 11764581</div>
<div class="bal" style="font-size:36px">৳ <span id="wBal">60</span></div>
<div style="font-size:13px">Min Withdraw: ৳<span id="minW">1000</span></div>
</div>
<div class="card">
<input class="inp" id="wAmt" placeholder="Amount - যেমন 1000" type="number">
<div style="display:flex;gap:10px;margin-top:10px">
<div class="mcard sel" id="m-bkash" onclick="setM('bKash')">
<img id="bkLogo" src="" style="width:45px;height:28px;object-fit:contain">
<div>bKash</div>
</div>
<div class="mcard" id="m-nagad" onclick="setM('Nagad')">
<img id="naLogo" src="" style="width:45px;height:28px;object-fit:contain">
<div>Nagad</div>
</div>
</div>
<input class="inp" id="wNum" placeholder="Number - যেমন 017xxxxxxxx">
<button class="btn" style="background:#2563eb;margin-top:12px" onclick="doWithdraw()">💸 Withdraw Request</button>
</div>
<div id="wHistory"></div>
<div class="spacer"></div>
</div>

<div id="p-profile" style="display:none">
<div class="card">
<div style="display:flex;justify-content:space-between;margin-bottom:12px">
<div style="font-weight:800;font-size:18px">👤 Profile - Admin 8807178385</div>
<div style="background:#22c55e;color:#000;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:800">ACTIVE</div>
</div>
<div class="grid2">
<div class="stat"><div style="font-size:11px;opacity:.6">🆔 ID</div><b id="pId" style="font-size:12px"></b></div>
<div class="stat"><div style="font-size:11px;opacity:.6">💰 Balance</div><b style="color:#22c55e">৳<span id="pBal"></span></b></div>
<div class="stat"><div style="font-size:11px;opacity:.6">🎬 Ads Watched</div><b id="pAds"></b></div>
<div class="stat"><div style="font-size:11px;opacity:.6">✅ Tasks Done</div><b id="pTasks"></b></div>
<div class="stat"><div style="font-size:11px;opacity:.6">👥 Refer Count</div><b id="pRef"></b></div>
<div class="stat"><div style="font-size:11px;opacity:.6">📈 Total Earn</div><b style="color:#facc15">৳<span id="pEarn"></span></b></div>
</div>
</div>
<div class="card support">
<div style="font-weight:800;font-size:17px" id="supTitle"></div>
<div style="font-size:13px;margin-top:8px;white-space:pre-line;opacity:.85;line-height:1.7" id="supDesc"></div>
<div style="background:#0a1222;border-radius:12px;padding:11px;margin-top:12px;font-size:13px;white-space:pre-line;line-height:1.7;border:1px dashed #334155" id="supRules"></div>
<div class="sbtn">
<a id="supTg" target="_blank" style="background:#229ED9">✈️ Support</a>
<a id="supCh" target="_blank" style="background:#22c55e">📢 Channel</a>
</div>
</div>
<div class="spacer"></div>
</div>

<div class="btm">
<div class="on" id="b-home" onclick="go('home')">🏠<br>Home</div>
<div id="b-tasks" onclick="go('tasks')">✅<br>Tasks</div>
<div id="b-refer" onclick="go('refer')">👥<br>Refer</div>
<div id="b-wallet" onclick="go('wallet')">💰<br>Wallet</div>
<div id="b-profile" onclick="go('profile')">👤<br>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let method='bKash';
let cur=0;
function go(p){
 ['home','tasks','refer','wallet','profile'].forEach(x=>{
  document.getElementById('p-'+x).style.display=x==p?'block':'none';
  document.getElementById('b-'+x).classList.toggle('on',x==p);
 });
 window.scrollTo(0,0);
}
function setM(m){
 method=m;
 document.getElementById('m-bkash').classList.toggle('sel',m=='bKash');
 document.getElementById('m-nagad').classList.toggle('sel',m=='Nagad');
}
function copyRef(){
 navigator.clipboard.writeText(document.getElementById('refLink').innerText);
 alert('Link Copied! Token 11764581');
}
function load(){
 fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.balance;
  document.getElementById('wBal').innerText=d.user.balance;
  document.getElementById('pBal').innerText=d.user.balance;
  document.getElementById('ads').innerText=d.user.ads_watched;
  document.getElementById('pAds').innerText=d.user.ads_watched;
  document.getElementById('bonus').innerText=d.settings.welcome_bonus;
  document.getElementById('minW').innerText=d.settings.min_withdraw;
  document.getElementById('refBonus').innerText=d.settings.ref_bonus;
  document.getElementById('cLogo').src=d.settings.company_logo;
  document.getElementById('bkLogo').src=d.settings.bkash_logo;
  document.getElementById('naLogo').src=d.settings.nagad_logo;
  document.getElementById('offTitle').innerText=d.settings.official_title;
  document.getElementById('offDesc').innerText=d.settings.official_desc;
  document.getElementById('offLive').innerText=d.settings.official_live;
  document.getElementById('adTopTitle').innerText=d.settings.home_ad_top_title;
  document.getElementById('adBtn').innerText=d.settings.home_ad_btn;
  document.getElementById('adZone').innerText=d.settings.home_ad_zone_text;
  document.getElementById('refLink').innerText='https://t.me/YourBot?start='+d.user.id;
  document.getElementById('refCount').innerText=d.user.ref_count;
  document.getElementById('pId').innerText=d.user.id;
  document.getElementById('pTasks').innerText=d.user.claimed.length+'/9';
  document.getElementById('pRef').innerText=d.user.ref_count;
  document.getElementById('pEarn').innerText=d.user.total_earn;
  document.getElementById('refEarn').innerText=d.user.ref_count*d.settings.ref_bonus;
  document.getElementById('supTitle').innerText=d.settings.support_title;
  document.getElementById('supDesc').innerText=d.settings.support_desc;
  document.getElementById('supRules').innerText=d.settings.support_rules;
  document.getElementById('supTg').href=d.settings.support_tg;
  document.getElementById('supCh').href=d.settings.support_channel;
  document.getElementById('refBottomTitle').innerText=d.settings.ref_bottom_title;
  document.getElementById('refBottomDesc').innerText=d.settings.ref_bottom_desc;
  document.getElementById('b1').src=d.settings.banner1;
  document.getElementById('b2').src=d.settings.banner2;
  document.getElementById('b3').src=d.settings.banner3;
  let ht='';
  d.tasks.forEach((t,i)=>{
   let done=d.user.claimed.includes(i);
   ht+=`<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div style="color:#f87171">৳${t.reward}</div></div><button class="btn" style="background:${t.color};margin-top:8px" ${done?'disabled':''} onclick="claim(${i})">${done?'✅ Completed':t.btn}</button></div>`;
  });
  document.getElementById('homeTasks').innerHTML=ht;
  document.getElementById('allTasks').innerHTML=ht;
  let wh='';
  d.withdraws.forEach(w=>{
   wh+=`<div class="card">${w.method} - ৳${w.amount} - ${w.status}<br><small>${w.number}</small><br><small>${w.time}</small></div>`;
  });
  document.getElementById('wHistory').innerHTML=wh;
  let lh='';
  (d.top_users||[]).forEach((u,i)=>{
   lh+=`<div>${i+1}. ID:${u.id} - ${u.ref_count} Refer - ৳${u.ref_count*d.settings.ref_bonus}</div>`;
  });
  if(!lh) lh='এখনো কেউ Refer করেনি';
  document.getElementById('refLeader').innerHTML=lh;
 });
}
function watchAd(){
 show_11764581().then(()=>{
  fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{
   alert(x.msg);
   load();
  });
 });
}
function claim(i){
 show_11764581().then(()=>{
  fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{
   alert(x.msg);
   load();
  });
 });
}
function doWithdraw(){
 let a=document.getElementById('wAmt').value;
 let n=document.getElementById('wNum').value;
 if(!a||!n) return alert('Amount & Number দিন');
 fetch(`/api/withdraw?id=${uid}&amount=${a}&number=${n}&method=${method}`).then(r=>r.json()).then(x=>{
  alert(x.msg);
  load();
 });
}
load();
// Banner Auto Slider - 3 Second Por Por Change Hobe - Token 11764581
setInterval(()=>{
 cur=(cur+1)%3;
 document.getElementById('slides').style.transform=`translateX(-${cur*100}%)`;
 document.querySelectorAll('.dot').forEach((d,i)=>{
  d.classList.toggle('on',i==cur);
 });
},3000);
</script>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Admin Full 500 Lines - Token 11764581 - ID 8807178385</title>
<style>
body{
 background:#0f172a;
 color:#fff;
 padding:12px;
 font-family:sans-serif;
 padding-bottom:60px;
}
.card{
 background:#1e293b;
 padding:14px;
 border-radius:12px;
 margin:10px 0;
}
input,textarea{
 width:100%;
 padding:11px;
 border-radius:8px;
 border:1px solid #334155;
 background:#0f172a;
 color:#fff;
 margin:6px 0;
}
button{
 padding:12px;
 border:none;
 border-radius:8px;
 background:#2563eb;
 color:#fff;
 font-weight:700;
 cursor:pointer;
}
label{
 font-size:12px;
 color:#38bdf8;
}
.grid{
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:8px;
}
</style>
</head>
<body>
<h2>🔧 Admin Panel - Full 500 Lines Final - Token 11764581 - Admin 8807178385</h2>
<div id="stats" class="card"></div>

<div class="card" style="border:2px solid #38bdf8">
<h3>📢 কোম্পানির ৩ টা বিজ্ঞাপন ব্যানার - Admin থেকে Pic Change</h3>
<label>Banner 1 Pic Link - Image URL - Token 11764581</label>
<input id="banner1" placeholder="https://example.com/banner1.jpg">
<div style="display:flex;gap:8px;align-items:center">
<img id="pre1" src="" style="width:80px;height:45px;object-fit:cover;border-radius:8px;background:#000">
<small>Preview 1 - Token 11764581</small>
</div>
<label>Banner 2 Pic Link</label>
<input id="banner2" placeholder="https://example.com/banner2.jpg">
<div style="display:flex;gap:8px;align-items:center">
<img id="pre2" src="" style="width:80px;height:45px;object-fit:cover;border-radius:8px;background:#000">
<small>Preview 2</small>
</div>
<label>Banner 3 Pic Link</label>
<input id="banner3" placeholder="https://example.com/banner3.jpg">
<div style="display:flex;gap:8px;align-items:center">
<img id="pre3" src="" style="width:80px;height:45px;object-fit:cover;border-radius:8px;background:#000">
<small>Preview 3</small>
</div>
<small style="opacity:.6">Tip: imgbb.com থেকে লিংক নিয়ে এখানে বসালেই User App এ Auto Slider 3 Sec পর পর পাল্টাবে - Token 11764581</small>
</div>

<div class="card">
<h3>🎨 Logo & Name - Admin 8807178385</h3>
<label>Company Logo URL</label>
<input id="company_logo">
<label>bKash Logo URL</label>
<input id="bkash_logo">
<label>Nagad Logo URL</label>
<input id="nagad_logo">
<label>App Name</label>
<input id="app_name">
</div>

<div class="card">
<h3>💰 Taka Control - Token 11764581</h3>
<div class="grid">
<div><label>Welcome Bonus</label><input id="welcome_bonus" type="number"></div>
<div><label>Ad Reward Mini Boy</label><input id="ad_reward" type="number"></div>
<div><label>Ad Limit</label><input id="ad_limit" type="number"></div>
<div><label>Min Withdraw</label><input id="min_withdraw" type="number"></div>
<div><label>Refer Bonus</label><input id="ref_bonus" type="number"></div>
</div>
</div>

<div class="card">
<h3>📢 Home + Notice Control - Admin 8807178385</h3>
<label>Official Title</label><input id="official_title">
<label>Official Desc</label><input id="official_desc">
<label>Official Live</label><input id="official_live">
<label>Home Ad Top Title</label><input id="home_ad_top_title">
<label>Home Ad Button - Mini Boy Token 11764581</label><input id="home_ad_btn">
<label>Home Ad Zone Text</label><input id="home_ad_zone_text">
<label>Tasks Header</label><input id="tasks_header">
</div>

<div class="card" style="border:2px solid #22c55e">
<h3>💬 Profile Support Box - Admin 8807178385 থেকে Change</h3>
<label>Support Title</label><input id="support_title">
<label>Support Description</label><textarea id="support_desc" rows="4"></textarea>
<label>Rules Box</label><textarea id="support_rules" rows="4"></textarea>
<label>Support TG Link</label><input id="support_tg">
<label>Channel Link</label><input id="support_channel">
</div>

<div class="card" style="border:2px solid #facc15">
<h3>👥 Refer Bottom Box - Refer পেজের ফাঁকা জায়গা</h3>
<label>Title</label><input id="ref_bottom_title">
<label>Description</label><textarea id="ref_bottom_desc" rows="5"></textarea>
</div>

<div class="card">
<h3>📋 9 Task Control - Token 11764581</h3>
<div id="tasksEdit"></div>
<button onclick="addTask()">+ Add Task - Token 11764581</button>
</div>

<div class="card">
<button style="background:#22c55e;width:100%;padding:18px;font-size:18px" onclick="saveAll()">💾 SAVE ALL - Token 11764581 - Admin 8807178385 - Final 500 Lines</button>
</div>

<div class="card">
<h3>💸 Withdraw - Admin 8807178385</h3>
<div id="wds"></div>
</div>

<div class="card">
<h3>👥 Users - Admin 8807178385 - Token 11764581</h3>
<div id="users"></div>
</div>

<script>
let DB={};
function load(){
fetch('/api/admin/full?id=8807178385').then(r=>r.json()).then(d=>{
DB=d;
document.getElementById('company_logo').value=d.settings.company_logo;
document.getElementById('bkash_logo').value=d.settings.bkash_logo;
document.getElementById('nagad_logo').value=d.settings.nagad_logo;
document.getElementById('app_name').value=d.settings.app_name;
document.getElementById('welcome_bonus').value=d.settings.welcome_bonus;
document.getElementById('ad_reward').value=d.settings.ad_reward;
document.getElementById('ad_limit').value=d.settings.ad_limit;
document.getElementById('min_withdraw').value=d.settings.min_withdraw;
document.getElementById('ref_bonus').value=d.settings.ref_bonus;
document.getElementById('official_title').value=d.settings.official_title;
document.getElementById('official_desc').value=d.settings.official_desc;
document.getElementById('official_live').value=d.settings.official_live;
document.getElementById('home_ad_top_title').value=d.settings.home_ad_top_title;
document.getElementById('home_ad_btn').value=d.settings.home_ad_btn;
document.getElementById('home_ad_zone_text').value=d.settings.home_ad_zone_text;
document.getElementById('tasks_header').value=d.settings.tasks_header;
document.getElementById('support_title').value=d.settings.support_title;
document.getElementById('support_desc').value=d.settings.support_desc;
document.getElementById('support_rules').value=d.settings.support_rules;
document.getElementById('support_tg').value=d.settings.support_tg;
document.getElementById('support_channel').value=d.settings.support_channel;
document.getElementById('ref_bottom_title').value=d.settings.ref_bottom_title;
document.getElementById('ref_bottom_desc').value=d.settings.ref_bottom_desc;
document.getElementById('banner1').value=d.settings.banner1;
document.getElementById('banner2').value=d.settings.banner2;
document.getElementById('banner3').value=d.settings.banner3;
try{
document.getElementById('pre1').src=d.settings.banner1;
document.getElementById('pre2').src=d.settings.banner2;
document.getElementById('pre3').src=d.settings.banner3;
}catch(e){}
renderTasks();
document.getElementById('wds').innerHTML=d.withdraws.map((w,i)=>`<div style="border:1px solid #334155;padding:8px;margin:4px;border-radius:8px">${w.uid} - ${w.method} - ৳${w.amount} - ${w.number} <button onclick="approve(${i})">Approve</button></div>`).join('')||'No Pending - Token 11764581';
document.getElementById('users').innerHTML=Object.values(d.users).map(u=>`<div style="border-bottom:1px solid #334155;padding:6px">${u.id} - ৳${u.balance} - Ads:${u.ads_watched} - Ref:${u.ref_count} - Total:৳${u.total_earn}</div>`).join('')||'No Users';
});
fetch('/api/admin/full?id=8807178385').then(r=>r.json()).then(d=>{
document.getElementById('stats').innerHTML=`<div class="card">Total Users: ${Object.keys(d.users).length} | Pending Withdraw: ${d.withdraws.length} | Token: 11764581 | Admin: 8807178385 | Mini Boy Ads Active | 3 Banner Slider Active | Final 500 Lines</div>`;
});
}
function renderTasks(){
let h='';
DB.tasks.forEach((t,i)=>{
h+=`<div class="card" style="background:#0f172a"><label>Task ${i+1} - Token 11764581 - Mini Boy</label><input value="${t.title}" onchange="DB.tasks[${i}].title=this.value"><div class="grid"><div><label>Reward</label><input type="number" value="${t.reward}" onchange="DB.tasks[${i}].reward=parseInt(this.value)"></div><div><label>Color</label><input value="${t.color}" onchange="DB.tasks[${i}].color=this.value"></div></div><label>Link</label><input value="${t.link}" onchange="DB.tasks[${i}].link=this.value"><button style="background:#ef4444;margin-top:6px" onclick="DB.tasks.splice(${i},1);renderTasks()">Delete Task ${i+1}</button></div>`;
});
document.getElementById('tasksEdit').innerHTML=h;
}
function addTask(){
DB.tasks.push({title:"New Task - Token 11764581",reward:20,link:"https://t.me",color:"#2563eb",btn:"👉 Claim + Watch Mini Boy Ad - Token 11764581"});
renderTasks();
}
function saveAll(){
let s={
company_logo:document.getElementById('company_logo').value,
bkash_logo:document.getElementById('bkash_logo').value,
nagad_logo:document.getElementById('nagad_logo').value,
app_name:document.getElementById('app_name').value,
welcome_bonus:parseInt(document.getElementById('welcome_bonus').value),
ad_reward:parseInt(document.getElementById('ad_reward').value),
ad_limit:parseInt(document.getElementById('ad_limit').value),
min_withdraw:parseInt(document.getElementById('min_withdraw').value),
ref_bonus:parseInt(document.getElementById('ref_bonus').value),
official_title:document.getElementById('official_title').value,
official_desc:document.getElementById('official_desc').value,
official_live:document.getElementById('official_live').value,
home_ad_top_title:document.getElementById('home_ad_top_title').value,
home_ad_btn:document.getElementById('home_ad_btn').value,
home_ad_zone_text:document.getElementById('home_ad_zone_text').value,
tasks_header:document.getElementById('tasks_header').value,
support_title:document.getElementById('support_title').value,
support_desc:document.getElementById('support_desc').value,
support_rules:document.getElementById('support_rules').value,
support_tg:document.getElementById('support_tg').value,
support_channel:document.getElementById('support_channel').value,
ref_bottom_title:document.getElementById('ref_bottom_title').value,
ref_bottom_desc:document.getElementById('ref_bottom_desc').value,
banner1:document.getElementById('banner1').value,
banner2:document.getElementById('banner2').value,
banner3:document.getElementById('banner3').value,
tasks:DB.tasks
};
fetch('/api/admin/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(s)}).then(r=>r.json()).then(x=>{alert(x.msg);load();});
}
function approve(i){
fetch('/api/admin/approve?idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});
}
load();
</script>
</body>
</html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
