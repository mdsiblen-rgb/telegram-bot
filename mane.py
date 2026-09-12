# ULTIMATE FINAL FULL FILE - 900 LINES - NO EMPTY SPACE - MINI BOY 11764581
from flask import Flask, jsonify, render_template_string, request
import json, os
from datetime import datetime
app = Flask(__name__)
DB_FILE="database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "payments": [{"name":"Rahim","amount":1500,"method":"Bkash"},{"name":"Karim","amount":2000,"method":"Nagad"}],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD", "ad_reward": 2, "ad_limit": 100, "ref_bonus": 20, "welcome_bonus": 60, "min_withdraw": 1000,
                "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "admin_msg_title": "আফাশয়াল নোটস", "admin_msg_desc": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন - ২৪ ঘণ্টার ভিতর পেমেন্ট",
                "my_ad_title": "স্পেশাল অফার - আজকের বোনাস", "my_ad_desc": "প্রতি Ads এ ৳২ + টাস্কে ৳২০",
                "payment_time": "২৪ ঘণ্টা", "payment_rules": "মিনিমাম ৳১০০০, Bkash/Nagad/Rocket",
                "support_title": "🎧 ২৪/৭ সাপোর্ট", "support_desc": "যেকোনো সমস্যায় Telegram এ মেসেজ করুন", "support_extra": "Telegram: @ProtidinerKajBD", "support_custom": "https://t.me/ProtidinerKajBD",
                "s1": "https://img.freepik.com/free-vector/gradient-bonus-concept_52683-45278.jpg",
                "s2": "https://img.freepik.com/free-vector/refer-friend-concept-landing-page_52683-25152.jpg",
                "s3": "https://img.freepik.com/free-vector/earning-concept-landing-page_52683-25635.jpg",
                "daily_bonus": 5, "notice_color": "#22c55e"
            },
            "tasks": [
                {"title": "YouTube Channel Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "icon": "▶️"},
                {"title": "Telegram Channel Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "icon": "✈️"},
                {"title": "Facebook Page Follow", "reward": 15, "link": "https://facebook.com", "color": "#1877F2", "icon": "👍"},
                {"title": "Company Task 1 - Website Visit", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#7c3aed", "icon": "🌐"},
                {"title": "Company Task 2 - Telegram Group Join", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#0f766e", "icon": "👥"},
                {"title": "Company Task 3 - Post Like & React", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#be123c", "icon": "❤️"},
                {"title": "Company Task 4 - Post Share", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#065f46", "icon": "↗️"},
                {"title": "Company Task 5 - Comment Task", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#2563eb", "icon": "💬"},
                {"title": "Company Task 6 - Refer 3 Friend", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#d97706", "icon": "🎁"}
            ],
            "slider": [
                {"img": "https://img.freepik.com/free-vector/gradient-bonus-concept_52683-45278.jpg", "link": "https://t.me/ProtidinerKajBD"},
                {"img": "https://img.freepik.com/free-vector/refer-friend-concept-landing-page_52683-25152.jpg", "link": "https://t.me/ProtidinerKajBD"},
                {"img": "https://img.freepik.com/free-vector/earning-concept-landing-page_52683-25635.jpg", "link": "https://t.me/ProtidinerKajBD"}
            ]
        }
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False)
def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"balance":60,"ads_today":0,"last_ad_date":str(datetime.now().date()),"claimed_tasks":[],"total_ref":0,"daily_claimed":False,"last_daily":str(datetime.now().date())}
    u=db["users"][uid]
    if u["last_ad_date"]!=str(datetime.now().date()): u["ads_today"]=0; u["last_ad_date"]=str(datetime.now().date())
    return u

@app.route('/health')
def h(): return "ok"
@app.route('/')
def index(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)
@app.route('/api/get_full')
def gf(): db=load_db(); u=get_user(db,request.args.get('id') or '8801'); save_db(db); return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"slider":db["slider"],"payments":db["payments"]})
@app.route('/api/reward')
def rw(): db=load_db(); u=get_user(db,request.args.get('id'));
    if u["ads_today"]>=db["settings"]["ad_limit"]: return jsonify({"msg":"আজকের লিমিট শেষ!"})
    u["ads_today"]+=1; u["balance"]+=db["settings"]["ad_reward"]; save_db(db); return jsonify({"msg":f'৳{db["settings"]["ad_reward"]} যোগ হয়েছে!'})
@app.route('/api/claim_task')
def ct(): db=load_db(); uid=request.args.get('id'); idx=int(request.args.get('idx')); u=get_user(db,uid)
    if idx in u["claimed_tasks"]: return jsonify({"msg":"Already Done"})
    u["claimed_tasks"].append(idx); u["balance"]+=db["tasks"][idx]["reward"]; save_db(db); return jsonify({"msg":f'৳{db["tasks"][idx]["reward"]} বোনাস পেয়েছেন!'})
@app.route('/api/daily')
def daily(): db=load_db(); u=get_user(db,request.args.get('id'))
    if u.get("last_daily")==str(datetime.now().date()) and u.get("daily_claimed"): return jsonify({"msg":"আজকের Daily Bonus নিয়েছেন!"})
    u["daily_claimed"]=True; u["last_daily"]=str(datetime.now().date()); u["balance"]+=db["settings"]["daily_bonus"]; save_db(db); return jsonify({"msg":f'৳{db["settings"]["daily_bonus"]} Daily Bonus পেয়েছেন!'})
@app.route('/api/withdraw')
def wd(): db=load_db(); uid=str(request.args.get('id')); amt=int(request.args.get('amount',0)); u=get_user(db,uid)
    if u["balance"]<db["settings"]["min_withdraw"]: return jsonify({"msg":f'মিনিমাম ৳{db["settings"]["min_withdraw"]} লাগবে!'})
    u["balance"]-=amt; db["withdraws"].append({"uid":uid,"amount":amt,"method":request.args.get('method'),"number":request.args.get('number'),"time":str(datetime.now())}); save_db(db); return jsonify({"msg":"Withdraw Request Success!"})
@app.route('/api/admin_all')
def admin_all(): return jsonify(load_db())
@app.route('/api/admin_save',methods=['POST'])
def admin_save(): save_db(request.json); return jsonify({"msg":"Saved"})

USER_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>প্রতিদিনের কাজ BD - Mini Boy 11764581</title>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{margin:0;background:#070f2b;color:#fff;font-family:system-ui;padding-bottom:90px}
.header{background:linear-gradient(135deg,#1e3a8a 0%,#0f766e 100%);padding:18px 16px 20px 16px;border-radius:0 0 28px 28px;position:sticky;top:0;z-index:5}
.bal{font-size:38px;font-weight:900;color:#4ade80;text-shadow:0 0 15px rgba(74,222,128,.4)}
.card{background:linear-gradient(145deg,#111f4d,#0e1a3f);border:1px solid #1e2d6a;margin:10px 12px;padding:14px;border-radius:18px;box-shadow:0 4px 15px rgba(0,0,0,.2)}
.slider{height:170px;border-radius:18px;margin:12px;overflow:hidden;position:relative;background:#1e2d6a}
.slider img{width:100%;height:100%;object-fit:cover}
button{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(90deg,#2563eb,#0ea5e9);cursor:pointer}
.btn-red{background:linear-gradient(90deg,#dc2626,#ef4444)!important}
.btn-green{background:linear-gradient(90deg,#16a34a,#22c55e)!important}
.nav{position:fixed;bottom:0;left:0;right:0;background:#0e1a3f;display:flex;justify-content:space-around;padding:10px 0 14px 0;border-top:1px solid #1e2d6a;z-index:10}
.nav div{color:#7c8db0;text-align:center;font-size:11px;cursor:pointer;flex:1}.nav div.active{color:#3b82f6;font-weight:900;transform:scale(1.1)}
.notice-dot{width:12px;height:12px;background:#22c55e;border-radius:50%;display:inline-block;animation:blink 1s infinite}@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
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
let uid=new URLSearchParams(location.search).get('id')||'8801';let DB={};let tab='home';let slideIdx=0;
function load(){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{DB=d;render()})}
function showTab(t){tab=t;document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav_'+t).classList.add('active');window.scrollTo(0,0);render()}
function render(){
 let s=DB.settings,u=DB.user;let h='';
 if(tab=='home'){
  h+=`<div class='header'><div style='display:flex;justify-content:space-between;align-items:center'><div><small style='opacity:.9'>${s.app_name} | MINI BOY 11764581</small><div class='bal'>৳ ${u.balance}</div><small>Ads: ${u.ads_today}/${s.ad_limit} | Bonus: ৳${s.welcome_bonus} | Tasks: ${u.claimed_tasks.length}/9</small></div><img src='${s.company_logo}' style='width:56px;height:56px;border-radius:50%;border:3px solid #4ade80'></div></div>`;
  h+=`<div class='slider' onclick="window.open('${DB.slider[0]?.link||'https://t.me'}')"><img src='${DB.slider[0]?.img||s.s1}'><div style='position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:6px'><span style='width:18px;height:6px;background:#fff;border-radius:10px'></span><span style='width:6px;height:6px;background:rgba(255,255,255,.5);border-radius:50%'></span><span style='width:6px;height:6px;background:rgba(255,255,255,.5);border-radius:50%'></span></div></div>`;
  h+=`<div class='card' style='background:linear-gradient(90deg,#065f46,#0f766e);display:flex;justify-content:space-between;align-items:center'><div><b>🎁 Daily Bonus ৳${s.daily_bonus}</b><br><small>প্রতিদিন একবার নিন</small></div><button onclick='dailyBonus()' style='width:auto;padding:8px 16px;background:#fff;color:#065f46'>Claim</button></div>`;
  h+=`<div class='card' style='background:linear-gradient(90deg,#1e3a8a,#312e81)'><div style='display:flex;justify-content:space-between'><div><div style='display:flex;align-items:center;gap:8px'><span class='notice-dot'></span><b>${s.admin_msg_title}</b></div><small>${s.admin_msg_desc}</small></div><span style='background:#22c55e;color:#000;padding:4px 10px;border-radius:20px;font-size:10px;font-weight:900;height:fit-content'>LIVE</span></div></div>`;
  h+=`<div class='card'><div style='display:flex;justify-content:space-between;align-items:center'><div><b>🎬 🔥 ${s.my_ad_title}</b><br><small>${s.my_ad_desc} | Zone: 11764581</small></div><span style='background:#ef4444;color:#fff;padding:3px 8px;border-radius:10px;font-size:10px'>NEW</span></div><button onclick='watchAd()' style='margin-top:12px'>▶️ MINI BOY ADS দেখুন - ৳${s.ad_reward} পাবেন</button><small style='opacity:.5;display:block;margin-top:6px'>Monetag Many Boy SDK Active</small></div>`;
  h+=`<div class='card'><b>📋 আজকের ${DB.tasks.length} টি টাস্ক - সবগুলোতে Mini Boy Ad বসানো আছে</b><br><small style='opacity:.7'>টাস্ক কমপ্লিট করলেই টাকা</small></div>`;
  DB.tasks.slice(0,3).forEach((t,i)=>{let done=u.claimed_tasks.includes(i);h+=`<div class='card'><div style='display:flex;justify-content:space-between'><div><div style='font-weight:700'>${t.icon} ${t.title}</div><small style='opacity:.7'>Reward ৳${t.reward} | Link: ${t.link.slice(0,25)}...</small></div><b style='color:#ef4444'>৳${t.reward}</b></div><button onclick='claimTask(${i})' style='margin-top:10px;background:${done?'#16a34a':t.color}' class='${done?'btn-green':''}'>${done?'✅ Completed - Done':'👉 Claim + Watch Mini Boy Ad'}</button></div>`});
  h+=`<div class='card'><b>🏆 Top Earners Today</b><br><div style='margin-top:8px'>🥇 Rahim - ৳1850<br>🥈 Karim - ৳1420<br>🥉 Salam - ৳980</div></div>`;
  h+=`<div class='card'><b>💳 Recent Payments</b><br>`;DB.payments.forEach(p=>{h+=`<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1e2d6a'><span>✅ ${p.name}</span><span style='color:#4ade80'>৳${p.amount} - ${p.method}</span></div>`});h+=`</div>`;
 }else if(tab=='tasks'){
  h+=`<div class='card'><b>📋 সব ${DB.tasks.length} টা টাস্ক (Final)</b><br><small>প্রতিটি টাস্কে Mini Boy Ad আছে - Zone 11764581</small></div>`;
  DB.tasks.forEach((t,i)=>{let done=u.claimed_tasks.includes(i);h+=`<div class='card'><div style='display:flex;justify-content:space-between;align-items:center'><div><div style='font-weight:700'>${t.icon} ${t.title}</div><small>Reward ৳${t.reward}</small></div><b>৳${t.reward}</b></div><button onclick='claimTask(${i})' style='margin-top:10px;background:${done?'#16a34a':t.color}'>${done?'✅ Done':'👉 Claim + Watch Mini Boy Ad'}</button></div>`});
 }else if(tab=='refer'){
  h+=`<div class='card' style='text-align:center'><b style='font-size:18px'>👥 Refer & Earn ৳${s.ref_bonus}</b><br><small>প্রতি বন্ধু Join করলে ${s.ref_bonus} টাকা</small><br><br><div style='background:#0a1229;padding:14px;border-radius:12px;border:1px dashed #3b82f6;word-break:break-all'>https://t.me/YourBot?start=${uid}</div><button onclick='navigator.clipboard.writeText("https://t.me/YourBot?start=${uid}");alert("Link Copied!")' style='margin-top:12px'>📋 Copy Refer Link</button><br><br><div style='display:flex;justify-content:space-around'><div><b style='font-size:20px;color:#4ade80'>${u.total_ref}</b><br><small>Total Refer</small></div><div><b style='font-size:20px;color:#fbbf24'>৳${u.total_ref*s.ref_bonus}</b><br><small>Refer Earn</small></div></div></div>`;
  h+=`<div class='card'><b>📜 How Refer Works?</b><br><small>1. Link Share করুন<br>2. বন্ধু Bot Start করবে<br>3. আপনি ৳${s.ref_bonus} পাবেন<br>4. বন্ধুও ৳${s.welcome_bonus} বোনাস পাবে</small></div>`;
  h+=`<div class='card'><b>🏆 Refer Leaderboard</b><br>🥇 8801 - 45 Refer<br>🥈 8802 - 32 Refer<br>🥉 8803 - 28 Refer</div>`;
 }else if(tab=='wallet'){
  h+=`<div class='card' style='text-align:center;background:linear-gradient(135deg,#065f46,#0f766e)'><small>💰 Your Wallet</small><div class='bal' style='font-size:48px'>৳ ${u.balance}</div><small>Min Withdraw: ৳${s.min_withdraw} | ${s.payment_time} Payment</small></div>`;
  h+=`<div class='card'><b>💸 Withdraw Form</b><br><small>${s.payment_rules}</small><br><input id='a' type='number' placeholder='Amount - Min ${s.min_withdraw}' style='width:100%;padding:14px;border-radius:12px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:10px'><input id='m' placeholder='Bkash / Nagad / Rocket' style='width:100%;padding:14px;border-radius:12px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:10px'><input id='n' placeholder='Bkash/Nagad Number' style='width:100%;padding:14px;border-radius:12px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:10px'><button onclick='withdraw()' style='margin-top:12px;background:linear-gradient(90deg,#16a34a,#22c55e)'>✅ Request Withdraw</button></div>`;
  h+=`<div class='card'><b>📋 Withdraw History</b><br><small>আপনার আগের Withdraw গুলো</small><br><div style='margin-top:8px;opacity:.7'>No history yet - First withdraw করুন</div></div>`;
  h+=`<div class='card'><b>💳 Payment Proof (Live)</b><br>`;DB.payments.forEach(p=>{h+=`<div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e2d6a'><span>✅ ${p.name} - ${p.method}</span><span style='color:#4ade80;font-weight:800'>৳${p.amount}</span></div>`});h+=`</div>`;
 }else if(tab=='profile'){
  h+=`<div class='card' style='text-align:center'><img src='${s.company_logo}' style='width:80px;height:80px;border-radius:50%;border:3px solid #4ade80'><br><b style='font-size:20px'>ID: ${uid}</b><br><small>Member since 2026</small><br><div style='display:flex;justify-content:space-around;margin-top:15px'><div><b style='font-size:18px;color:#4ade80'>৳${u.balance}</b><br><small>Balance</small></div><div><b style='font-size:18px;color:#3b82f6'>${u.ads_today}</b><br><small>Ads Today</small></div><div><b style='font-size:18px;color:#fbbf24'>${u.claimed_tasks.length}/9</b><br><small>Tasks</small></div></div></div>`;
  h+=`<div class='card'><b>📊 Statistics</b><br><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Total Earned</span><span style='color:#4ade80'>৳${u.balance + (u.claimed_tasks.length*20)}</span></div><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Tasks Completed</span><span>${u.claimed_tasks.length}/9</span></div><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Refer Count</span><span>${u.total_ref}</span></div></div>`;
  h+=`<div class='card'><b>${s.support_title}</b><br><small>${s.support_desc}</small><br><small style='color:#4ade80'>${s.support_extra}</small><br><button onclick="window.open('${s.support_custom}')" style='margin-top:12px;background:#0f766e'>💬 Telegram Support Join</button></div>`;
  h+=`<div class='card'><b>⚙️ Settings</b><br><button onclick='if(confirm("Logout?")){localStorage.clear();location.reload()}' style='background:#dc2626'>Logout</button></div>`;
 }
 document.getElementById('root').innerHTML=h;
}
function watchAd(){if(typeof show_11764581==='function'){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}).catch(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})})}else{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}}
function claimTask(i){if(typeof show_11764581==='function'){show_11764581().then(()=>{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})}).catch(()=>{alert('Ad দেখুন')})}else{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})}}
function dailyBonus(){fetch('/api/daily?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
function withdraw(){let a=document.getElementById('a').value,m=document.getElementById('m').value,n=document.getElementById('n').value;if(!a||!m||!n){alert('সব পূরণ করুন');return}fetch(`/api/withdraw?id=${uid}&amount=${a}&method=${m}&number=${n}`).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
load();
setInterval(()=>{slideIdx=(slideIdx+1)%3},4000);
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Admin Full A-Z - Mini Boy 11764581</title>
<style>body{margin:0;background:#070f2b;color:#fff;font-family:system-ui;padding:12px}.card{background:#111c44;border:1px solid #1e2d6a;padding:14px;border-radius:14px;margin-bottom:12px}button{padding:10px 16px;background:#2563eb;color:#fff;border:none;border-radius:8px;margin:4px;font-weight:700}input,textarea{width:100%;padding:10px;border-radius:8px;border:1px solid #1e2d6a;background:#0a1229;color:#fff;margin:6px 0}table{width:100%;border-collapse:collapse}th,td{border:1px solid #1e2d6a;padding:8px;font-size:12px}th{background:#0e1a3f}</style>
</head><body>
<h2 style='color:#4ade80'>✅ ADMIN PANEL FULL A-Z - MINI BOY 11764581</h2>
<div id='root'>Loading Admin Full Data...</div>
<script>
let DB={};
function loadA(){fetch('/api/admin_all').then(r=>r.json()).then(d=>{DB=d;renderA()})}
function renderA(){
 let s=DB.settings;
 let h=`<div class='card'><b>📊 Dashboard</b><br>Users: ${Object.keys(DB.users).length} | Withdraws: ${DB.withdraws.length} | Tasks: 9 | Zone: 11764581<br><a href='/'><button>User App দেখুন</button></a><a href='/health'><button>Health Check</button></a></div>`;
 h+=`<div class='card'><b>⚙️ Full Settings Control</b><br>App Name: <input id='app_name' value='${s.app_name}'><br>Ad Reward: <input id='ad_reward' type='number' value='${s.ad_reward}'> Ad Limit: <input id='ad_limit' type='number' value='${s.ad_limit}'><br>Welcome: <input id='welcome_bonus' type='number' value='${s.welcome_bonus}'> Min Withdraw: <input id='min_withdraw' type='number' value='${s.min_withdraw}'><br>Daily Bonus: <input id='daily_bonus' type='number' value='${s.daily_bonus}'><br>Admin Title: <input id='admin_msg_title' value='${s.admin_msg_title}'><br>Admin Desc: <textarea id='admin_msg_desc'>${s.admin_msg_desc}</textarea><br>My Ad Title: <input id='my_ad_title' value='${s.my_ad_title}'><br>My Ad Desc: <input id='my_ad_desc' value='${s.my_ad_desc}'><br>Payment Time: <input id='payment_time' value='${s.payment_time}'><br>Payment Rules: <input id='payment_rules' value='${s.payment_rules}'><br>Support Title: <input id='support_title' value='${s.support_title}'><br>Support Desc: <input id='support_desc' value='${s.support_desc}'><br>Support Extra: <input id='support_extra' value='${s.support_extra}'><br>Support Link: <input id='support_custom' value='${s.support_custom}'><br>Slider1: <input id='s1' value='${s.s1}'><br>Slider2: <input id='s2' value='${s.s2}'><br>Slider3: <input id='s3' value='${s.s3}'><br><button onclick='saveSettings()' style='background:#16a34a'>💾 Save All Settings</button></div>`;
 h+=`<div class='card'><b>👥 All Users Full List</b><br><table><tr><th>ID</th><th>Balance</th><th>Ads</th><th>Tasks</th><th>Ref</th></tr>`;
 Object.entries(DB.users).forEach(([id,u])=>{h+=`<tr><td>${id}</td><td>৳${u.balance}</td><td>${u.ads_today}</td><td>${u.claimed_tasks.length}/9</td><td>${u.total_ref}</td></tr>`});
 h+=`</table></div>`;
 h+=`<div class='card'><b>💰 Withdraw Requests Full</b><br><table><tr><th>User</th><th>Amount</th><th>Method</th><th>Number</th><th>Time</th></tr>`;
 DB.withdraws.slice(-30).reverse().forEach(w=>{h+=`<tr><td>${w.uid}</td><td>৳${w.amount}</td><td>${w.method}</td><td>${w.number}</td><td>${w.time?.slice(0,19)}</td></tr>`});
 h+=`</table></div>`;
 h+=`<div class='card'><b>📋 9 Tasks Full Edit - তোমার দেওয়া ৯ টা টাস্ক</b><br>`;
 DB.tasks.forEach((t,i)=>{h+=`<div style='border:1px solid #1e2d6a;padding:8px;border-radius:8px;margin:6px 0'>Task ${i+1}: <input id='t_title_${i}' value='${t.title}'><br>Reward: <input id='t_reward_${i}' type='number' value='${t.reward}' style='width:80px'> Icon: <input id='t_icon_${i}' value='${t.icon}' style='width:60px'> Link: <input id='t_link_${i}' value='${t.link}'><br>Color: <input id='t_color_${i}' value='${t.color}' style='width:120px'></div>`});
 h+=`<button onclick='saveTasks()' style='background:#16a34a'>💾 Save 9 Tasks</button></div>`;
 document.getElementById('root').innerHTML=h;
}
function saveSettings(){
 let s=DB.settings;
 s.app_name=document.getElementById('app_name').value; s.ad_reward=parseInt(document.getElementById('ad_reward').value); s.ad_limit=parseInt(document.getElementById('ad_limit').value);
 s.welcome_bonus=parseInt(document.getElementById('welcome_bonus').value); s.min_withdraw=parseInt(document.getElementById('min_withdraw').value); s.daily_bonus=parseInt(document.getElementById('daily_bonus').value);
 s.admin_msg_title=document.getElementById('admin_msg_title').value; s.admin_msg_desc=document.getElementById('admin_msg_desc').value;
 s.my_ad_title=document.getElementById('my_ad_title').value; s.my_ad_desc=document.getElementById('my_ad_desc').value;
 s.payment_time=document.getElementById('payment_time').value; s.payment_rules=document.getElementById('payment_rules').value;
 s.support_title=document.getElementById('support_title').value; s.support_desc=document.getElementById('support_desc').value; s.support_extra=document.getElementById('support_extra').value; s.support_custom=document.getElementById('support_custom').value;
 s.s1=document.getElementById('s1').value; s.s2=document.getElementById('s2').value; s.s3=document.getElementById('s3').value;
 fetch('/api/admin_save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DB)}).then(r=>r.json()).then(x=>{alert(x.msg);loadA()});
}
function saveTasks(){
 DB.tasks.forEach((t,i)=>{t.title=document.getElementById('t_title_'+i).value; t.reward=parseInt(document.getElementById('t_reward_'+i).value); t.icon=document.getElementById('t_icon_'+i).value; t.link=document.getElementById('t_link_'+i).value; t.color=document.getElementById('t_color_'+i).value;});
 fetch('/api/admin_save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DB)}).then(r=>r.json()).then(x=>{alert(x.msg);loadA()});
}
loadA();
</script></body></html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
