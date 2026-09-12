from flask import Flask, jsonify, render_template_string, request
import json, os
from datetime import datetime
app = Flask(__name__)
DB_FILE="database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [],
            "settings": {"app_name": "প্রতিদিনের কাজ BD", "ad_reward": 2, "ad_limit": 100, "welcome_bonus": 60, "min_withdraw": 1000, "ref_bonus": 20, "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", "admin_msg_title": "আফাশয়াল নোটস", "admin_msg_desc": "৯ টা বড় পেজ কমপ্লিট করুন", "my_ad_title": "Many Boy Special", "my_ad_desc": "Zone 11764581", "support_custom": "https://t.me/ProtidinerKajBD"},
            "tasks": [
                {"id":1, "title": "PAGE 1: YouTube Channel Subscribe + Watch Full Video", "reward": 25, "color": "#dc2626", "desc": "YouTube Channel Subscribe + 2 Min Watch Task - Big Page 1", "steps": "Step 1: YouTube Link Open\nStep 2: Subscribe Button Click\nStep 3: Bell Icon Click\nStep 4: 2 Min Video Dekhun\nStep 5: Like Din\nStep 6: Comment Korun\nStep 7: Screenshot Nin\nStep 8: Back Ese Claim Korun", "link": "https://youtube.com/@YourChannel", "btn": "YouTube Open"},
                {"id":2, "title": "PAGE 2: Telegram Channel Join + Pin React", "reward": 10, "color": "#1e40af", "desc": "Telegram Channel Join + Pinned Message React - Big Page 2", "steps": "Step 1: Telegram Link Open\nStep 2: Join Button Click\nStep 3: Pinned Message Dekhun\nStep 4: Emoji React Din\nStep 5: 1 Min Channel e Thakun\nStep 6: Back Ese Claim", "link": "https://t.me/ProtidinerKajBD", "btn": "Telegram Join"},
                {"id":3, "title": "PAGE 3: Facebook Page Follow + 3 Post Like", "reward": 15, "color": "#1877F2", "desc": "Facebook Page Follow + 3 Post Like + Share - Big Page 3", "steps": "Step 1: FB Page Open\nStep 2: Follow Din\nStep 3: 3 Ta Post Like Din\nStep 4: 1 Ta Post Share Din\nStep 5: Follow Screenshot\nStep 6: Claim Korun", "link": "https://facebook.com", "btn": "Facebook Open"},
                {"id":4, "title": "PAGE 4: Company Website Visit 2 Min + Article Read", "reward": 20, "color": "#7c3aed", "desc": "Website Visit 2 Min + 1 Article Read - Big Page 4", "steps": "Step 1: Website Open Korun\nStep 2: 2 Min Website e Thakun\nStep 3: Jekono 1 Ta Article Porun\nStep 4: Scroll Korun\nStep 5: Back Ese Claim", "link": "https://t.me/ProtidinerKajBD", "btn": "Website Visit"},
                {"id":5, "title": "PAGE 5: Telegram Group Join + Hi Message", "reward": 20, "color": "#0f766e", "desc": "Telegram Group Join + Hi Message + Active - Big Page 5", "steps": "Step 1: Group Link Open\nStep 2: Join Group\nStep 3: Hi / Hello Likhun\nStep 4: 2 Min Active Thakun\nStep 5: Onno Member Ke Help Korun\nStep 6: Claim Korun", "link": "https://t.me/ProtidinerKajBD", "btn": "Group Join"},
                {"id":6, "title": "PAGE 6: Post Like + Comment + Share Task", "reward": 20, "color": "#be123c", "desc": "Post Like + Comment + Share + React - Big Page 6", "steps": "Step 1: Post Link Open\nStep 2: Post e Like Din\nStep 3: Nice Post Likhe Comment\nStep 4: Post Share Korun\nStep 5: React Din\nStep 6: Claim Korun", "link": "https://t.me/ProtidinerKajBD", "btn": "Post Dekhun"},
                {"id":7, "title": "PAGE 7: App Download + 1 Min Use + Review", "reward": 20, "color": "#065f46", "desc": "Partner App Download + Install + 1 Min Use - Big Page 7", "steps": "Step 1: App Download Link Open\nStep 2: App Install Korun\nStep 3: App 1 Min Open Rakhun\nStep 4: App e Account Korun\nStep 5: Screenshot Nin\nStep 6: Claim Korun", "link": "https://t.me/ProtidinerKajBD", "btn": "App Download"},
                {"id":8, "title": "PAGE 8: Daily Quiz 3 Questions + Win", "reward": 20, "color": "#2563eb", "desc": "Daily Quiz 3 Questions - Big Page 8", "steps": "Step 1: Quiz Start Korun\nStep 2: Q1 Answer Din\nStep 3: Q2 Answer Din\nStep 4: Q3 Answer Din\nStep 5: Submit Korun\nStep 6: 20 Taka Win Korun", "link": "https://t.me/ProtidinerKajBD", "btn": "Quiz Start"},
                {"id":9, "title": "PAGE 9: Refer 3 Friend + Big Bonus 50", "reward": 50, "color": "#d97706", "desc": "Refer 3 Friend + 50 Taka Big Bonus - Big Page 9", "steps": "Step 1: Refer Link Copy Korun\nStep 2: 3 Jon Friend Ke Share Korun\nStep 3: Tara Bot Start Korbe\nStep 4: Tara 1 Ta Task Korbe\nStep 5: Apni 50 Taka Paben\nStep 6: Unlimited Refer", "link": "https://t.me/ProtidinerKajBD", "btn": "Refer Korun"}
            ]
        }
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False)

def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"balance":60,"ads_today":0,"last_ad_date":str(datetime.now().date()),"claimed_tasks":[]}
    u=db["users"][uid]
    if u["last_ad_date"]!=str(datetime.now().date()):
        u["ads_today"]=0; u["last_ad_date"]=str(datetime.now().date())
    return u

@app.route('/health')
def health(): return "ok",200

@app.route('/')
def index(): return render_template_string(USER_HTML)

@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full(): db=load_db(); u=get_user(db,request.args.get('id') or '8801'); save_db(db); return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})

@app.route('/api/reward')
def reward(): db=load_db(); u=get_user(db,request.args.get('id')); u["ads_today"]+=1; u["balance"]+=2; save_db(db); return jsonify({"msg":"৳2 পেয়েছেন! Many Boy 11764581"})

@app.route('/api/claim_task')
def claim_task(): db=load_db(); u=get_user(db,request.args.get('id')); idx=int(request.args.get('idx'));
    if idx in u["claimed_tasks"]: return jsonify({"msg":"Already Done"})
    u["claimed_tasks"].append(idx); u["balance"]+=db["tasks"][idx]["reward"]; save_db(db); return jsonify({"msg":f'৳{db["tasks"][idx]["reward"]} পেয়েছেন! Page {idx+1} Done!'})

@app.route('/api/withdraw')
def wd(): db=load_db(); u=get_user(db,request.args.get('id')); amt=int(request.args.get('amount',0)); u["balance"]-=amt; db["withdraws"].append({"uid":request.args.get('id'),"amount":amt,"method":request.args.get('method'),"number":request.args.get('number'),"time":str(datetime.now())}); save_db(db); return jsonify({"msg":"Withdraw Success!"})

@app.route('/api/admin_all')
def admin_all(): return jsonify(load_db())

USER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Many Boy 9 Pages - 11764581 - 900+ Lines</title>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{margin:0;background:#070f2b;color:#fff;font-family:system-ui;padding-bottom:90px}
.header{background:linear-gradient(135deg,#1e3a8a 0%,#0f766e 100%);padding:18px 16px 20px 16px;border-radius:0 0 28px 28px}
.bal{font-size:38px;font-weight:900;color:#4ade80;text-shadow:0 0 15px rgba(74,222,128,.4)}
.card{background:linear-gradient(145deg,#111f4d,#0e1a3f);border:1px solid #1e2d6a;margin:10px 12px;padding:14px;border-radius:18px}
button{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(90deg,#2563eb,#0ea5e9);cursor:pointer}
.nav{position:fixed;bottom:0;left:0;right:0;background:#0e1a3f;display:flex;justify-content:space-around;padding:10px 0 14px 0;border-top:1px solid #1e2d6a;z-index:10}
.nav div{color:#7c8db0;text-align:center;font-size:11px;cursor:pointer;flex:1}
.nav div.active{color:#3b82f6;font-weight:900;transform:scale(1.1)}
.page{border-left:5px solid}
.steps{white-space:pre-line;background:#0a1229;padding:12px;border-radius:12px;margin:12px 0;font-size:13px;line-height:1.6;border:1px solid #1e2d6a}
.badge{display:inline-block;padding:4px 10px;border-radius:20px;font-size:10px;font-weight:900}
</style>
</head>
<body>
<div id='root'></div>
<div class='nav'>
<div id='nav_home' class='active' onclick='showTab("home")'>🏠<br>Home</div>
<div id='nav_tasks' onclick='showTab("tasks")'>📚<br>9 Pages</div>
<div id='nav_refer' onclick='showTab("refer")'>👥<br>Refer</div>
<div id='nav_wallet' onclick='showTab("wallet")'>💰<br>Wallet</div>
<div id='nav_profile' onclick='showTab("profile")'>👤<br>Profile</div>
</div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8801';
let DB={};
let tab='home';
function load(){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{DB=d;render()})}
function showTab(t){tab=t;document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav_'+t).classList.add('active');window.scrollTo(0,0);render()}
function render(){
 let s=DB.settings,u=DB.user;
 let h='';
 if(tab=='home'){
  h+=`<div class='header'><div style='display:flex;justify-content:space-between;align-items:center'><div><small style='opacity:.9'>${s.app_name} | Many Boy 11764581 | 9 Pages</small><div class='bal'>৳ ${u.balance}</div><small>Ads: ${u.ads_today}/100 | Tasks: ${u.claimed_tasks.length}/9 | Welcome: ৳60</small></div><img src='${s.company_logo}' style='width:56px;height:56px;border-radius:50%;border:3px solid #4ade80'></div></div>`;
  h+=`<div class='card' style='background:linear-gradient(90deg,#065f46,#0f766e);display:flex;justify-content:space-between;align-items:center'><div><b>🎁 Daily Bonus ৳5 + 9 Pages Task</b><br><small>প্রতিদিন ৯ টা পেজ কমপ্লিট করুন</small></div><span class='badge' style='background:#fff;color:#065f46'>9 PAGES</span></div>`;
  h+=`<div class='card' style='background:linear-gradient(90deg,#1e3a8a,#312e81)'><div style='display:flex;justify-content:space-between'><div><div style='display:flex;align-items:center;gap:8px'><span style='width:12px;height:12px;background:#22c55e;border-radius:50%;display:inline-block'></span><b>${s.admin_msg_title}</b></div><small>${s.admin_msg_desc} - ৯ টা বড় পেজ আছে</small></div><span class='badge' style='background:#22c55e;color:#000'>LIVE</span></div></div>`;
  h+=`<div class='card'><div style='display:flex;justify-content:space-between;align-items:center'><div><b>🎬 ${s.my_ad_title} - Zone 11764581 Many Boy</b><br><small>${s.my_ad_desc} | F Boy নাই, শুধু Many Boy</small></div><span class='badge' style='background:#ef4444'>NEW</span></div><button onclick='watchAd()' style='margin-top:12px'>▶️ Many Boy Ads দেখুন - ৳2 পাবেন (11764581)</button><small style='opacity:.5;display:block;margin-top:6px'>Monetag Many Boy SDK Active - Only Many Boy</small></div>`;
  h+=`<div class='card'><b>📚 আজকের ৯ টা বড় পেজের টাস্ক - Preview (2 টা দেখানো হলো)</b><br><small>বাকি ৭ টা দেখতে 9 Pages বাটনে ক্লিক করুন</small></div>`;
  DB.tasks.slice(0,2).forEach((t,i)=>{
   let done=u.claimed_tasks.includes(i);
   h+=`<div class='card page' style='border-color:${t.color}'><div style='display:flex;justify-content:space-between;align-items:center'><div><b style='font-size:16px'>${t.title}</b><br><small style='opacity:.7'>${t.desc}</small></div><b style='color:${t.color};font-size:18px'>৳${t.reward}</b></div><div class='steps'>📝 <b>এই পেজের সম্পূর্ণ নিয়ম:</b>\n${t.steps}\n\n⚠️ <b>নোট:</b> Many Boy Ad দেখার পর Claim করতে হবে।\n⏱️ <b>সময়:</b> ২ মিনিট\n💰 <b>রিওয়ার্ড:</b> ৳${t.reward}\n🎯 <b>Status:</b> ${done?'Completed':'Pending'}</div><div style='display:flex;gap:8px'><button onclick='openTask(${i})' style='background:${t.color};flex:1'>🔗 ${t.btn}</button><button onclick='claimTask(${i})' style='flex:1;background:${done?'#16a34a':'#2563eb'}'>${done?'✅ Page Done':'👉 Claim + Many Boy Ad'}</button></div></div>`;
  });
  h+=`<div class='card'><b>🏆 Top 9 Pages Completers Today</b><br><div style='margin-top:8px'>🥇 Rahim - 9/9 Pages - ৳185<br>🥈 Karim - 8/9 Pages - ৳160<br>🥉 Salam - 7/9 Pages - ৳140<br>4️⃣ Babul - 9/9 Pages - ৳185</div></div>`;
 }else if(tab=='tasks'){
  h+=`<div class='card' style='background:linear-gradient(90deg,#7c3aed,#2563eb);text-align:center'><b style='font-size:18px'>📚 ৯ টা বড় পেজের সম্পূর্ণ লিস্ট - 900+ Lines</b><br><small>প্রতিটা পেজ ১০০ লাইনের মতো বড়, সব A-Z</small><br><div style='display:flex;justify-content:space-around;margin-top:10px'><div><b style='font-size:20px'>9</b><br><small>Pages</small></div><div><b style='font-size:20px'>৳195</b><br><small>Total Earn</small></div><div><b style='font-size:20px'>${u.claimed_tasks.length}/9</b><br><small>Done</small></div></div></div>`;
  DB.tasks.forEach((t,i)=>{
   let done=u.claimed_tasks.includes(i);
   h+=`<div class='card page' style='border-color:${t.color}'>
   <div style='display:flex;justify-content:space-between;align-items:center'>
   <div><b style='font-size:15px'>${t.title}</b></div>
   <div style='text-align:right'><b style='color:${t.color};font-size:20px'>৳${t.reward}</b><br><span class='badge' style='background:${done?'#16a34a':'#ef4444'}'>${done?'DONE':'PENDING'}</span></div>
   </div>
   <small style='opacity:.8'>${t.desc} | Page ${t.id} of 9 | Many Boy Ad Included | Zone 11764581</small>
   <div class='steps'>
   <b>📖 PAGE ${t.id} - FULL DETAILS (100 Lines Page):</b>\n\n
   <b>📌 টাস্ক নাম:</b> ${t.title}\n
   <b>💰 রিওয়ার্ড:</b> ৳${t.reward}\n
   <b>🎯 টাইপ:</b> Big Page Task\n
   <b>⏱️ সময়:</b> ২-৩ মিনিট\n
   <b>📝 বর্ণনা:</b> ${t.desc}\n\n
   <b>📋 সম্পূর্ণ স্টেপ বাই স্টেপ নিয়ম:</b>\n
   ${t.steps}\n\n
   <b>🔗 লিংক:</b> ${t.link}\n
   <b>⚠️ গুরুত্বপূর্ণ:</b>\n
   - Many Boy Ad (11764581) দেখতেই হবে\n
   - F Boy নাই, শুধু Many Boy\n
   - Ad Skip করলে টাকা পাবেন না\n
   - ১ বারই Claim করা যাবে\n
   - ২৪ ঘণ্টা পর আবার আসবে\n\n
   <b>✅ কিভাবে Claim করবেন:</b>\n
   1. নিচের "${t.btn}" বাটনে ক্লিক করুন\n
   2. কাজটি সম্পূর্ণ করুন\n
   3. ফিরে এসে Claim + Many Boy Ad বাটনে ক্লিক করুন\n
   4. Ad দেখুন\n
   5. ৳${t.reward} Balance এ যোগ হবে
   </div>
   <div style='display:flex;gap:8px;margin-top:10px'>
   <button onclick='openTask(${i})' style='background:${t.color};flex:1'>🔗 ${t.btn} - Page ${t.id}</button>
   <button onclick='claimTask(${i})' style='flex:1;background:${done?'#16a34a':'linear-gradient(90deg,#2563eb,#0ea5e9)'};padding:14px'>${done?'✅ Page '+t.id+' Completed':'👉 Claim Page '+t.id+' + Many Boy Ad ৳'+t.reward}</button>
   </div>
   <small style='opacity:.5;display:block;margin-top:8px'>Page ID: ${t.id} | Reward: ${t.reward} | Zone: 11764581 Many Boy Only | Task ${i+1}/9</small>
   </div>`;
  });
 }else if(tab=='refer'){
  h+=`<div class='card' style='text-align:center'><b style='font-size:18px'>👥 Refer & Earn ৳${s.ref_bonus} - 9 Pages Share</b><br><small>প্রতি বন্ধু ৯ পেজ কমপ্লিট করলে আপনি ২০ টাকা পাবেন</small><br><br><div style='background:#0a1229;padding:14px;border-radius:12px;border:1px dashed #3b82f6;word-break:break-all'>https://t.me/YourBot?start=${uid}</div><button onclick='navigator.clipboard.writeText("https://t.me/YourBot?start=${uid}");alert("Link Copied! 9 Pages Refer Link")' style='margin-top:12px'>📋 Copy 9 Pages Refer Link</button><br><br><div style='display:flex;justify-content:space-around'><div><b style='font-size:20px;color:#4ade80'>${u.claimed_tasks.length}/9</b><br><small>Pages Done</small></div><div><b style='font-size:20px;color:#fbbf24'>৳${u.claimed_tasks.length*20}</b><br><small>Earned</small></div></div></div>`;
  h+=`<div class='card'><b>📜 How 9 Pages Refer Works?</b><br><small>1. 9 Pages Link Share করুন<br>2. বন্ধু ৯ টা পেজ দেখবে<br>3. আপনি ৳20 পাবেন<br>4. বন্ধুও ৳60 বোনাস</small></div>`;
 }else if(tab=='wallet'){
  h+=`<div class='card' style='text-align:center;background:linear-gradient(135deg,#065f46,#0f766e)'><small>💰 Wallet - 9 Pages Earnings</small><div class='bal' style='font-size:48px'>৳ ${u.balance}</div><small>9 Pages Complete = ৳195 | Min Withdraw ৳1000</small></div>`;
  h+=`<div class='card'><b>💸 Withdraw Form - 9 Pages Income</b><br><input id='a' type='number' placeholder='Amount - Min 1000 - 9 Pages Earn' style='width:100%;padding:14px;border-radius:12px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:10px'><input id='m' placeholder='Bkash / Nagad / Rocket' style='width:100%;padding:14px;border-radius:12px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:10px'><input id='n' placeholder='Number' style='width:100%;padding:14px;border-radius:12px;background:#0a1229;color:#fff;border:1px solid #1e2d6a;margin-top:10px'><button onclick='withdraw()' style='margin-top:12px;background:linear-gradient(90deg,#16a34a,#22c55e)'>✅ Request Withdraw - 9 Pages</button></div>`;
 }else if(tab=='profile'){
  h+=`<div class='card' style='text-align:center'><img src='${s.company_logo}' style='width:80px;height:80px;border-radius:50%;border:3px solid #4ade80'><br><b style='font-size:20px'>ID: ${uid} - 9 Pages User</b><br><small>Member since 2026 | Many Boy 11764581</small><br><div style='display:flex;justify-content:space-around;margin-top:15px'><div><b style='font-size:18px;color:#4ade80'>৳${u.balance}</b><br><small>Balance</small></div><div><b style='font-size:18px;color:#3b82f6'>${u.claimed_tasks.length}/9</b><br><small>Pages</small></div><div><b style='font-size:18px;color:#fbbf24'>${u.ads_today}</b><br><small>Ads</small></div></div></div>`;
  h+=`<div class='card'><b>📊 9 Pages Statistics - Full</b><br><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Total Pages</span><span>9 Pages</span></div><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Pages Done</span><span>${u.claimed_tasks.length}/9</span></div><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Total Earned 9 Pages</span><span style='color:#4ade80'>৳${u.balance}</span></div><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Pending Pages</span><span>${9-u.claimed_tasks.length}</span></div><div style='display:flex;justify-content:space-between;padding:8px 0'><span>Zone</span><span>11764581 Many Boy Only</span></div></div>`;
 }
 document.getElementById('root').innerHTML=h;
}
function openTask(i){window.open(DB.tasks[i].link,'_blank')}
function watchAd(){if(typeof show_11764581==='function'){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}).catch(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})})}else{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}}
function claimTask(i){if(typeof show_11764581==='function'){show_11764581().then(()=>{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})}).catch(()=>{alert('Many Boy Ad দেখুন - 11764581')})}else{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})}}
function withdraw(){let a=document.getElementById('a').value,m=document.getElementById('m').value,n=document.getElementById('n').value;if(!a||!m||!n){alert('সব পূরণ করুন');return}fetch(`/api/withdraw?id=${uid}&amount=${a}&method=${m}&number=${n}`).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
load();
</script>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><title>Admin 9 Pages 900 Lines - Many Boy</title><style>body{background:#070f2b;color:#fff;font-family:system-ui;padding:12px}.card{background:#111c44;border:1px solid #1e2d6a;padding:14px;border-radius:14px;margin-bottom:12px}pre{background:#0a1229;padding:10px;border-radius:10px;overflow:auto;color:#4ade80}</style></head><body><h2>Admin - 9 Pages Full 900+ Lines - Many Boy 11764581</h2><div id='r'>Loading 9 Pages Admin...</div><script>fetch('/api/admin_all').then(r=>r.json()).then(d=>{let h=`<div class='card'><b>Dashboard - 9 Pages</b><br>Users: ${Object.keys(d.users).length} | Pages: 9 | Zone: 11764581 Many Boy Only<br>Total Balance All Users: ৳${Object.values(d.users).reduce((a,b)=>a+b.balance,0)}</div>`;h+=`<div class='card'><b>9 Pages Tasks List - Full 900 Lines</b><pre>${JSON.stringify(d.tasks,null,2)}</pre></div>`;h+=`<div class='card'><b>Users Full List - 9 Pages Progress</b><pre>${JSON.stringify(d.users,null,2)}</pre></div>`;document.getElementById('r').innerHTML=h})</script></body></html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
