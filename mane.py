# -*- coding: utf-8 -*-
# FINAL A-Z MINI APP - 5 Button - Full Admin Control - 11764581 - 8807178385
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE='database.json'

def default_db():
    return {
        "users": {},
        "withdraws": [],
        "posts": [
            {"img":"https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg","title":"Refer & Earn ৳20","link":"https://t.me/ProtidinerKajBD"},
            {"img":"https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg","title":"Daily Bonus ৳50","link":"https://google.com"}
        ],
        "settings": {
            "app_name": "Protidiner Kaj BD",
            "admin_name": "Admin - 8807178385",
            "admin_id": "8807178385",
            "admin_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "welcome_bonus": 1120,
            "ad_reward": 2,
            "ad_coins": 10,
            "ad_limit": 50,
            "min_withdraw": 1000,
            "monetag_zone": "11764581",
            "company_banner_title": "📢 Sponsored by Company - Token 11764581",
            "official_title": "অফিসিয়াল নোটিস - 11764581",
            "official_desc": "প্রতিদিন Ads দেখুন, PLW জমান, ডলার ইনকাম করুন",
            "banner1": "https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2": "https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3": "https://img.freepik.com/free-vector/gradient-sale-landing-page-template_52683-24288.jpg",
            "support_tg": "https://t.me/ProtidinerKajBD",
            "wallet_rule": "১. Min ৳1000 হলে Withdraw\n২. 24 ঘন্টায় পেমেন্ট\n৩. ভুল নাম্বারে দায় আপনার না"
        },
        "tasks": [
            {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","doller":"$1","icon":"⚡"},
            {"title":"Telegram Join","reward":10,"link":"https://t.me/ProtidinerKajBD","color":"#1e40af","doller":"$2","icon":"📺"},
            {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9","doller":"$5","icon":"👍"},
            {"title":"Daily Checkin","reward":20,"link":"https://google.com","color":"#7c3aed","doller":"$1","icon":"🎁"},
            {"title":"Invite 3 Friends","reward":50,"link":"https://t.me","color":"#0f766e","doller":"$10","icon":"👥"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d=default_db(); save_db(d); return d
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","balance":db["settings"]["welcome_bonus"],"coins":0,"ads_today":0,"total_ads":0,"last_date":today,"claimed":[],"total_earn":db["settings"]["welcome_bonus"],"banned":False}
    u=db["users"][uid]
    if u.get("last_date")!=today: u["ads_today"]=0; u["last_date"]=today
    return u

@app.route('/')
def index(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "Admin Only?id=8807178385",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get')
def api_get():
    db=load_db(); uid=request.args.get('id','8807178385'); u=get_user(db,uid); save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"posts":db["posts"]})
@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id'))
    if u["banned"]: return jsonify({"msg":"Banned!"})
    if u["ads_today"]>=db["settings"]["ad_limit"]: return jsonify({"msg":"আজকের লিমিট শেষ!"})
    u["balance"]+=db["settings"]["ad_reward"]; u["coins"]+=db["settings"]["ad_coins"]; u["ads_today"]+=1; u["total_ads"]+=1; u["total_earn"]+=db["settings"]["ad_reward"]; save_db(db)
    return jsonify({"msg":f"৳{db['settings']['ad_reward']} + {db['settings']['ad_coins']} Coins পেয়েছেন!"})
@app.route('/api/claim')
def api_claim():
    db=load_db(); idx=int(request.args.get('idx')); uid=request.args.get('id'); u=get_user(db,uid)
    if idx in u["claimed"]: return jsonify({"msg":"Already Done!"})
    u["claimed"].append(idx); u["balance"]+=db["tasks"][idx]["reward"]; u["total_earn"]+=db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg":"Task Complete!"})

@app.route('/api/admin/full')
def admin_full(): return jsonify(load_db())
@app.route('/api/admin/save',methods=['POST'])
def admin_save():
    db=load_db(); j=request.json
    for k,v in j.items():
        if k in db["settings"]: db["settings"][k]=v
        if k=="tasks": db["tasks"]=v
        if k=="posts": db["posts"]=v
        if k=="users": db["users"]=v
    save_db(db); return jsonify({"msg":"Saved A to Z!"})

USER_HTML="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mini App</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}
body{background:#060610;background:radial-gradient(circle at 50% 0%,#2a1a6b 0%,#0f0a28 45%,#060610 100%);color:#fff;max-width:430px;margin:0 auto;min-height:100vh;padding-bottom:115px}
.top{padding:16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:50;background:rgba(6,6,16,0.7);backdrop-filter:blur(20px)}
.card{background:linear-gradient(180deg,rgba(255,255,255,0.09),rgba(255,255,255,0.03));border:1px solid rgba(255,255,255,0.12);margin:12px;border-radius:22px;padding:16px;backdrop-filter:blur(20px)}
.bigbtn{width:100%;padding:18px;border:none;border-radius:16px;font-weight:900;font-size:16px;cursor:pointer;margin-top:10px;background:linear-gradient(90deg,#6d4cff,#3a1aff);color:#fff;box-shadow:0 12px 30px rgba(109,76,255,0.4)}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(12,10,30,0.95);backdrop-filter:blur(20px);display:flex;border-top:1px solid rgba(255,255,255,0.1);padding:8px 0 12px;z-index:99;border-radius:22px 22px 0 0}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;padding:6px;cursor:pointer}.btm div.on{color:#fff;background:rgba(109,76,255,0.25);border-radius:14px}
.page{display:none}.page.active{display:block}
.coin{width:130px;height:130px;background:radial-gradient(circle at 30% 30%,#8bb6ff,#3a5bff 60%,#1e1b8a);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:58px;font-weight:900;margin:0 auto;box-shadow:0 0 60px rgba(90,100,255,0.6),inset 0 0 20px rgba(255,255,255,0.3);border:3px solid rgba(255,255,255,0.2)}
.slider{margin:12px;border-radius:20px;overflow:hidden;height:160px;position:relative;border:1px solid rgba(255,255,255,0.1)}.slides{display:flex;width:300%;transition:0.6s}.slide{min-width:100%;height:160px}.slide img{width:100%;height:160px;object-fit:cover}
.task{display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.06);padding:14px;border-radius:16px;margin-top:10px;border:1px solid rgba(255,255,255,0.08)}
.g{width:62px;height:62px;background:rgba(255,255,255,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;margin:0 auto}
</style></head><body>

<div id="page-home" class="page active">
<div class="top"><div style="display:flex;gap:10px;align-items:center"><img id="logo" style="width:38px;height:38px;border-radius:50%;border:2px solid #6d4cff"><div><div id="appName" style="font-weight:900"></div><small style="opacity:0.6">Good Morning ☀️</small></div></div><div style="opacity:0.6">🔔</div></div>

<div style="text-align:center;padding:10px"><div class="coin">D</div><div style="margin-top:14px"><small style="opacity:0.6" id="uName">John_dou</small><div style="font-size:34px;font-weight:900">PLW <span id="bal">1120.00</span></div><div style="opacity:0.5;font-size:13px">🪙 <span id="coins">0</span> Coins | Ads: <span id="adsInfo"></span></div></div></div>

<div class="card" style="border-color:#22c55e;display:flex;justify-content:space-between"><div><b id="offTitle"></b><br><small id="offDesc" style="opacity:0.7"></small></div><div style="color:#22c55e;font-weight:900">● LIVE</div></div>

<div class="slider"><div class="slides" id="slides"><div class="slide"><img id="b1"></div><div class="slide"><img id="b2"></div><div class="slide"><img id="b3"></div></div></div>

<!-- কোম্পানির ব্যানার - এখান থেকে ইনকাম - 40s পর পর -->
<div class="card" style="border:2px dashed #6d4cff;text-align:center;background:rgba(109,76,255,0.1)"><small style="color:#a78bfa" id="compTitle"></small><div id="companyBox" style="margin:10px 0;background:#000;border-radius:14px;height:90px;display:flex;align-items:center;justify-content:center">Company Ads - Monetag 11764581<br>ছোট ব্যানার আসবে, বড় কোম্পানি লাগবে</div><button class="bigbtn" style="background:linear-gradient(90deg,#22c55e,#16a34a);color:#000" onclick="watchAd()">▶️ ADS দেখুন - বড় বাটন</button></div>

<div id="postsBox"></div>
<div id="homeTasks"></div>
</div>

<div id="page-tasks" class="page"><div class="card"><h3>✅ Tasks - বড় বাটন</h3></div><div id="tasksList"></div></div>

<div id="page-ads" class="page"><div style="text-align:center;padding:30px"><div style="width:90px;height:90px;background:linear-gradient(135deg,#6d4cff,#3a1aff);border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:40px">▶️</div><h2 style="margin-top:16px">Watch Ads & Earn Money</h2><p style="opacity:0.5;font-size:13px;margin-top:6px">Ads দেখে PLW জমান - Fast Earn</p></div><div class="card"><button class="bigbtn" onclick="watchAd()">⚡ Start Earning Now - বড় বাটন</button></div><div id="adsTasks"></div></div>

<div id="page-wallet" class="page"><div class="card"><h3>💰 Wallet</h3><div style="font-size:42px;font-weight:900;color:#6d4cff">$<span id="wBal">0</span> | ৳<span id="wBal2">0</span></div><div style="opacity:0.6">🪙 Coins: <span id="wCoins">0</span></div><button class="bigbtn">💸 Withdraw - বড় বাটন</button></div><div class="card"><b id="wRuleT"></b><br><small id="wRuleD" style="white-space:pre-line;opacity:0.7"></small></div></div>

<div id="page-profile" class="page">
<div class="card" style="background:transparent;border:none">
<div style="background:linear-gradient(135deg,#6d28ff,#3b82f6);border-radius:22px;padding:22px;text-align:center"><div style="display:flex;justify-content:space-between"><span>Profile</span><span>🔄</span></div><div class="g" id="pG">G</div><div style="font-weight:900;margin-top:10px" id="pName">Guest User</div><div style="font-size:11px;background:rgba(0,0,0,0.3);display:inline-block;padding:4px 10px;border-radius:20px;margin-top:6px;color:#22c55e">● Active - <span id="pId"></span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px">
<div style="background:rgba(255,255,255,0.1);padding:12px;border-radius:14px"><div id="pBal" style="font-weight:900">৳0</div><small>Balance</small></div>
<div style="background:rgba(255,255,255,0.1);padding:12px;border-radius:14px"><div id="pCoins">0</div><small>Coins</small></div>
<div style="background:rgba(255,255,255,0.1);padding:12px;border-radius:14px"><div id="pAds">0</div><small>Ads Today</small></div>
<div style="background:rgba(255,255,255,0.1);padding:12px;border-radius:14px"><div id="pTotal">0</div><small>Total Ads</small></div>
</div>
</div>
<div class="card" style="margin-top:12px"><div style="display:flex;justify-content:space-between"><div>👤 Admin: <span id="adminName"></span></div><div>🟢</div></div><div style="margin-top:8px;opacity:0.7;font-size:13px" id="refLink"></div><button class="bigbtn" style="padding:14px" onclick="copyRef()">📋 Refer Link Copy</button></div>
</div>
</div>

<div class="btm">
<div class="on" onclick="goPage('home',this)">🏠<br>Home</div>
<div onclick="goPage('tasks',this)">✅<br>Tasks</div>
<div onclick="goPage('ads',this)">⚡<br>Earn</div>
<div onclick="goPage('wallet',this)">💰<br>Wallet</div>
<div onclick="goPage('profile',this)">👤<br>Profile</div>
</div>

<script>
let DB=null, UID=localStorage.getItem('uid')||'8807178385'; localStorage.setItem('uid',UID);
let sdkLoaded=false;
function loadSDK(cb){ if(sdkLoaded){cb();return;} let s=document.createElement('script'); s.src='//libtl.com/sdk.js'; s.dataset.zone=DB?DB.settings.monetag_zone:'11764581'; s.dataset.sdk='show_'+(DB?DB.settings.monetag_zone:'11764581'); s.onload=()=>{sdkLoaded=true;cb();}; document.body.appendChild(s); }
async function loadAll(){
 let r=await fetch('/api/get?id='+UID); DB=await r.json();
 document.getElementById('appName').innerText=DB.settings.app_name;
 document.getElementById('logo').src=DB.settings.admin_logo;
 document.getElementById('bal').innerText=DB.user.balance+'.00';
 document.getElementById('wBal').innerText=DB.user.balance; document.getElementById('wBal2').innerText=DB.user.balance;
 document.getElementById('coins').innerText=DB.user.coins; document.getElementById('wCoins').innerText=DB.user.coins;
 document.getElementById('adsInfo').innerText=DB.user.ads_today+'/'+DB.settings.ad_limit;
 document.getElementById('offTitle').innerText=DB.settings.official_title;
 document.getElementById('offDesc').innerText=DB.settings.official_desc;
 document.getElementById('compTitle').innerText=DB.settings.company_banner_title;
 document.getElementById('b1').src=DB.settings.banner1; document.getElementById('b2').src=DB.settings.banner2; document.getElementById('b3').src=DB.settings.banner3;
 document.getElementById('wRuleT').innerText=DB.settings.app_name; document.getElementById('wRuleD').innerText=DB.settings.wallet_rule;
 document.getElementById('uName').innerText=DB.user.name; document.getElementById('pName').innerText=DB.user.name; document.getElementById('pG').innerText=DB.user.name[0];
 document.getElementById('pId').innerText=DB.user.id; document.getElementById('adminName').innerText=DB.settings.admin_name;
 document.getElementById('pBal').innerText='৳'+DB.user.balance; document.getElementById('pCoins').innerText=DB.user.coins; document.getElementById('pAds').innerText=DB.user.ads_today; document.getElementById('pTotal').innerText=DB.user.total_ads;
 document.getElementById('refLink').innerText=location.origin+'?ref='+UID;
 let posts=''; DB.posts.forEach(p=>{ posts+=`<div class="card"><img src="${p.img}" style="width:100%;height:140px;object-fit:cover;border-radius:12px"><div style="display:flex;justify-content:space-between;margin-top:10px"><b>${p.title}</b><button class="smallbtn" onclick="window.open('${p.link}')">Open</button></div></div>`; });
 document.getElementById('postsBox').innerHTML=posts;
 let ht=''; DB.tasks.forEach((t,i)=>{
   let done=DB.user.claimed.includes(i);
   ht+=`<div class="card"><div class="task" style="margin:0;border:none;background:transparent;padding:0"><div><div style="font-size:12px;opacity:0.6">${t.icon} ${t.title}</div><b>${t.title}</b><br><small style="opacity:0.5">Reward ৳${t.reward}</small></div><div style="text-align:right"><b style="color:#fbbf24">${t.doller}</b></div></div><button class="bigbtn" style="background:${done?'#333':t.color}" ${done?'disabled':''} onclick="claimTask(${i})">${done?'✅ Done':'👉 Claim - বড় বাটন'}</button></div>`;
 }); document.getElementById('tasksList').innerHTML=ht; document.getElementById('homeTasks').innerHTML=ht; document.getElementById('adsTasks').innerHTML=ht;
}
function goPage(p,el){ document.querySelectorAll('.page').forEach(x=>x.classList.remove('active')); document.getElementById('page-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on')); el.classList.add('on'); window.scrollTo(0,0); }
function watchAd(){ loadSDK(()=>{ show_11764581().then(()=>{ fetch('/api/reward?id='+UID).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();}) }) }); }
function claimTask(i){ let t=DB.tasks[i]; window.open(t.link,'_blank'); fetch('/api/claim?id='+UID+'&idx='+i).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();}); }
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied!');}
let cur=0; setInterval(()=>{cur=(cur+1)%3; let s=document.getElementById('slides'); if(s) s.style.transform=`translateX(-${cur*100}%)`;},3000);
setInterval(()=>{ loadSDK(()=>{ try{ show_11764581({type:'inApp', inAppSettings:{frequency:1,capping:0,interval:30,timeout:5,everyPage:false}}); }catch(e){} }); },40000);
loadAll();
</script></body></html>
"""

ADMIN_HTML="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{background:#0f172a;color:#fff;font-family:sans-serif;padding:12px}
.card{background:#1e293b;padding:14px;border-radius:14px;margin-top:12px;border:1px solid #334155}
input,textarea{width:100%;padding:12px;margin-top:6px;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff}
button{width:100%;padding:14px;border:none;border-radius:12px;font-weight:900;margin-top:10px;cursor:pointer}
.tab{display:inline-block;padding:10px 16px;background:#1e293b;border-radius:20px;margin:4px;cursor:pointer}.tab.on{background:#6d4cff}
</style></head><body>
<h2>🔧 Admin A-Z - 8807178385</h2>
<div><span class="tab on" onclick="showTab('settings',this)">⚙️ Settings</span><span class="tab" onclick="showTab('banners',this)">🖼️ Banners</span><span class="tab" onclick="showTab('tasks',this)">✅ Tasks</span><span class="tab" onclick="showTab('posts',this)">📝 Posts</span><span class="tab" onclick="showTab('users',this)">👥 Users</span></div>

<div id="tab-settings" class="card"></div>
<div id="tab-banners" class="card" style="display:none"></div>
<div id="tab-tasks" class="card" style="display:none"></div>
<div id="tab-posts" class="card" style="display:none"></div>
<div id="tab-users" class="card" style="display:none"></div>

<button style="background:#22c55e;color:#000" onclick="saveAll()">💾 SAVE ALL A-Z</button>
<div id="msg" style="margin-top:10px;color:#22c55e"></div>

<script>
let DB=null;
async function load(){
 let r=await fetch('/api/admin/full'); DB=await r.json(); let s=DB.settings;
 document.getElementById('tab-settings').innerHTML=`
 App Name<br><input id="app_name" value="${s.app_name}"><br>
 Admin Name<br><input id="admin_name" value="${s.admin_name}"><br>
 Admin Logo<br><input id="admin_logo" value="${s.admin_logo}"><br>
 Welcome Bonus PLW<br><input id="welcome_bonus" type="number" value="${s.welcome_bonus}"><br>
 Ad Reward ৳<br><input id="ad_reward" type="number" value="${s.ad_reward}"><br>
 Ad Coins<br><input id="ad_coins" type="number" value="${s.ad_coins}"><br>
 Ad Limit<br><input id="ad_limit" type="number" value="${s.ad_limit}"><br>
 Min Withdraw<br><input id="min_withdraw" type="number" value="${s.min_withdraw}"><br>
 Monetag Zone ID (Company Ads)<br><input id="monetag_zone" value="${s.monetag_zone}"><br>
 Company Banner Title<br><input id="company_banner_title" value="${s.company_banner_title}"><br>
 Official Title<br><input id="official_title" value="${s.official_title}"><br>
 Official Desc<br><textarea id="official_desc">${s.official_desc}</textarea><br>
 Telegram Link<br><input id="support_tg" value="${s.support_tg}"><br>
 Wallet Rule<br><textarea id="wallet_rule">${s.wallet_rule}</textarea>
 `;
 document.getElementById('tab-banners').innerHTML=`
 Banner1<br><input id="banner1" value="${s.banner1}"><br>
 Banner2<br><input id="banner2" value="${s.banner2}"><br>
 Banner3<br><input id="banner3" value="${s.banner3}"><br>
 <img src="${s.banner1}" style="width:100%;height:100px;object-fit:cover;border-radius:10px;margin-top:8px">
 `;
 let th=''; DB.tasks.forEach((t,i)=>{ th+=`<div style="background:#0f172a;padding:10px;border-radius:10px;margin-top:8px"><b>Task ${i+1}</b><br>Title<input id="t_title_${i}" value="${t.title}"><br>Reward<input id="t_reward_${i}" type="number" value="${t.reward}"><br>Doller<input id="t_doller_${i}" value="${t.doller}"><br>Link<input id="t_link_${i}" value="${t.link}"><br>Color<input id="t_color_${i}" value="${t.color}"></div>`; });
 th+=`<button onclick="addTask()" style="background:#3b82f6">+ Add Task</button>`;
 document.getElementById('tab-tasks').innerHTML=th;

 let ph=''; DB.posts.forEach((p,i)=>{ ph+=`<div style="background:#0f172a;padding:10px;border-radius:10px;margin-top:8px"><b>Post ${i+1}</b><br>Image<input id="p_img_${i}" value="${p.img}"><br>Title<input id="p_title_${i}" value="${p.title}"><br>Link<input id="p_link_${i}" value="${p.link}"></div>`; });
 ph+=`<button onclick="addPost()" style="background:#8b5cf6">+ Add Post</button>`;
 document.getElementById('tab-posts').innerHTML=ph;

 let uh=`Total Users: ${Object.keys(DB.users).length}<br><br>`;
 Object.values(DB.users).slice(0,20).forEach(u=>{
   uh+=`<div style="background:#0f172a;padding:10px;border-radius:10px;margin-top:6px;display:flex;justify-content:space-between"><div>${u.id} - ${u.name} - ৳${u.balance} - ${u.coins} Coins - Ads:${u.ads_today}</div><div><input id="bal_${u.id}" type="number" value="${u.balance}" style="width:80px"><button onclick="setBal('${u.id}')" style="width:auto;padding:6px 10px;background:#22c55e">Set</button></div></div>`;
 });
 document.getElementById('tab-users').innerHTML=uh;
}
function showTab(id,el){ document.querySelectorAll('[id^=tab-]').forEach(d=>d.style.display='none'); document.getElementById('tab-'+id).style.display='block'; document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on')); el.classList.add('on'); }
function addTask(){ DB.tasks.push({title:"New Task",reward:10,link:"https://t.me",color:"#1e40af",doller:"$1",icon:"⚡"}); load(); }
function addPost(){ DB.posts.push({img:"https://via.placeholder.com/400x200",title:"New Post",link:"https://t.me"}); load(); }
async function setBal(uid){ let v=parseInt(document.getElementById('bal_'+uid).value); DB.users[uid].balance=v; await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({users:DB.users})}); alert('Balance Updated'); }
async function saveAll(){
 let s={};
 ["app_name","admin_name","admin_logo","company_banner_title","official_title","official_desc","banner1","banner2","banner3","support_tg","wallet_rule","monetag_zone"].forEach(k=>{ let el=document.getElementById(k); if(el) s[k]=el.value; });
 ["welcome_bonus","ad_reward","ad_coins","ad_limit","min_withdraw"].forEach(k=>{ let el=document.getElementById(k); if(el) s[k]=parseInt(el.value); });
 let tasks=[]; DB.tasks.forEach((t,i)=>{ let el=document.getElementById('t_title_'+i); if(!el) return; tasks.push({title:document.getElementById('t_title_'+i).value,reward:parseInt(document.getElementById('t_reward_'+i).value),doller:document.getElementById('t_doller_'+i).value,link:document.getElementById('t_link_'+i).value,color:document.getElementById('t_color_'+i).value,icon:t.icon}); });
 s.tasks=tasks;
 let posts=[]; DB.posts.forEach((p,i)=>{ let el=document.getElementById('p_img_'+i); if(!el) return; posts.push({img:document.getElementById('p_img_'+i).value,title:document.getElementById('p_title_'+i).value,link:document.getElementById('p_link_'+i).value}); });
 s.posts=posts;
 let r=await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(s)}); let j=await r.json(); document.getElementById('msg').innerText=j.msg+' - Reload User App';
}
load();
</script></body></html>
"""
if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
