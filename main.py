import os, json, threading, time, datetime, requests
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db.json"
SELF_URL = "https://telegram-bot-1-v77g.onrender.com"
app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [],
            "slider": [
                {"img":"https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800","link":"https://t.me/ProtidinerKajBD"},
                {"img":"https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800","link":"https://t.me/ProtidinerKajBD"},
                {"img":"https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800","link":"https://youtube.com/@ProtidinerKajBD"}
            ],
            "settings":{
                "app_name":"প্রতিদিনের কাজ BD",
                "ad_zone":"11764581",
                "ad_reward":1,
                "ad_limit":100,
                "min_withdraw":1000,
                "welcome_bonus":60,
                "daily_bonus":10,
                "payment_time":"প্রতিদিন রাত 8PM - 10PM",
                "payment_rules":"1. ভুল Number দিবেন না 2. Min ৳1000",
                "admin_msg_title":"অফিশিয়াল চ্যানেল - ProtidinerKajBD",
                "admin_msg_desc":"Ads দেখুন, Task করুন, Refer করুন, Withdraw করুন",
                "my_ad_title":"🔥 আজকের স্পেশাল অফার",
                "my_ad_desc":"এখানে তোমার নিজের বিজ্ঞাপন লিখবে, এডমিন থেকে চেঞ্জ হবে"
            },
            "tasks":[
                {"title":"YouTube ভিডিও দেখুন","reward":25,"link":"https://youtube.com/@ProtidinerKajBD","btn":"শুরু করুন","type":"youtube","color":"#065f46"},
                {"title":"Telegram Channel Join","reward":10,"link":"https://t.me/ProtidinerKajBD","btn":"Join","type":"telegram","color":"#1e40af"},
                {"title":"Facebook Follow","reward":15,"link":"https://www.facebook.com/share/1AXw16vWRj/","btn":"Follow","type":"facebook","color":"#1877F2"},
                {"title":"Company Task 1","reward":20,"link":"https://t.me/ProtidinerKajBD","btn":"Visit","type":"company","color":"#7c3aed"},
                {"title":"Company Task 2","reward":20,"link":"https://t.me/ProtidinerKajBD","btn":"Visit","type":"company","color":"#0f766e"},
                {"title":"Company Task 3","reward":20,"link":"https://t.me/ProtidinerKajBD","btn":"Visit","type":"company","color":"#be123c"}
            ]
        }
    with open(DB_FILE,'r') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE,'w') as f: json.dump(d,f,indent=2)

def keep_alive():
    while True:
        try: time.sleep(240); requests.get(f"{SELF_URL}/health",timeout=5)
        except: pass
threading.Thread(target=keep_alive,daemon=True).start()

def is_admin(id):
    try: return int(id)==ADMIN_ID
    except: return False

# ================= USER APP =================
USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@500;700&display=swap" rel="stylesheet">
<style>
*{font-family:'Hind Siliguri',sans-serif;box-sizing:border-box;margin:0;padding:0}
body{max-width:430px;margin:0 auto;background:#eef2ff;padding-bottom:90px}
.top{background:#1e40af;color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
.top img{width:36px;height:36px;border-radius:50%;background:#fff}
.card{background:#fff;margin:12px;border-radius:20px;padding:16px;box-shadow:0 4px 18px rgba(0,0,0,.06)}
.bal-big{font-size:52px;font-weight:900;text-align:center;color:#1e40af}
.btn-blue{width:100%;background:#1e40af;color:#fff;padding:14px;border:none;border-radius:14px;font-weight:700;font-size:16px}
.btn-yellow{background:#f59e0b;color:#fff;padding:12px 22px;border:none;border-radius:12px;font-weight:700}
.slider{margin:12px;border-radius:22px;height:185px;overflow:hidden;position:relative;background:#000}
.slide{position:absolute;inset:0;opacity:0;transition:.8s}.slide.active{opacity:1}.slide img{width:100%;height:100%;object-fit:cover}
.dots{text-align:center}.dot{width:8px;height:8px;background:#cbd5e1;border-radius:50%;display:inline-block;margin:0 3px}.dot.active{background:#1e40af;width:20px}
/* WITHDRAW NEW DESIGN */
.wd-method{display:flex;gap:10px}
.wd-card{flex:1;border:2px solid #e2e8f0;border-radius:16px;padding:14px;text-align:center;cursor:pointer;background:#fff}
.wd-card.selected{border-color:#e2136e;box-shadow:0 0 0 3px rgba(226,19,110,.15)}
.wd-card img{width:60px;height:60px;object-fit:contain}
.wd-input{width:100%;padding:14px;border-radius:14px;border:1px solid #e2e8f0;margin-top:12px;background:#f8fafc;font-size:15px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#fff;display:flex;border-top:1px solid #e2e8f0;padding:8px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#94a3b8;font-size:11px}.btm div.on{color:#1e40af;font-weight:700}
</style></head><body>

<div class="top"><div style="display:flex;gap:10px;align-items:center;font-weight:700"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"><span id="appNameTop">প্রতিদিনের কাজ BD</span></div><div style="font-weight:900">৳<span id="topBal">60</span></div></div>

<div id="t-home">
<div class="slider" id="slider"></div><div class="dots" id="dots"></div>
<div class="card"><div class="bal-big">৳<span id="bal">60</span></div><button class="btn-blue" onclick="go('earn')">💰 আয় করুন</button></div>
<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><div><div style="font-size:18px">🎁 Daily Check-in</div><div style="color:#64748b;font-size:13px">প্রতিদিন বোনাস ৳10</div></div><button class="btn-yellow" onclick="dailyCheck()">আজকের বোনাস নিন</button></div></div>

<!-- MY OWN AD FROM ADMIN -->
<div class="card" style="border:2px dashed #1e40af;background:#f0f7ff">
<div style="font-weight:700;color:#1e40af" id="myAdTitle">🔥 আজকের স্পেশাল অফার</div>
<div style="font-size:14px;margin-top:6px" id="myAdDesc">এখানে তোমার নিজের বিজ্ঞাপন লিখবে</div>
</div>

<div class="card"><div style="font-weight:700" id="adminTop">Admin Message - ProtidinerKajBD</div><div style="font-weight:900;font-size:17px;margin:6px 0" id="adminTitle">অফিশিয়াল চ্যানেল</div><div style="font-size:13px;color:#334155" id="adminDesc">Ads দেখুন, Task করুন</div></div>
</div>

<div id="t-earn" style="display:none"><div class="card"><div style="font-size:14px">প্রতি Ads ৳<span id="adRate">1</span> | Timer 30s</div><div class="bal-big" style="margin:10px 0">৳<span id="adRate2">1</span></div><button class="btn-blue" id="adBtn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button><div style="font-size:12px;margin-top:8px;color:#64748b">Limit: 100 | Watched: <span id="watched">0</span></div></div><div id="tasksBox"></div></div>

<div id="t-support" style="display:none">
<div class="card"><h3 style="text-align:center">🎧 সাপোর্ট সেন্টার</h3><button class="btn-blue" style="margin-top:12px" onclick="window.open(document.getElementById('chLink').value)">📢 Telegram Channel</button><button class="btn-blue" style="margin-top:10px;background:#FF0000" onclick="window.open(document.getElementById('ytLink').value)">▶️ YouTube</button><button class="btn-blue" style="margin-top:10px;background:#1877F2" onclick="window.open(document.getElementById('fbLink').value)">📘 Facebook Page</button></div>
</div>

<div id="t-withdraw" style="display:none">
<div class="card">
<div style="font-weight:700;text-align:center">💳 পেমেন্ট মেথড</div>
<div class="wd-method" style="margin-top:14px">
<div class="wd-card selected" id="cardBkash" onclick="sel('bKash')"><img src="https://i.ibb.co/0j7GzB0/bkash.png"><div style="margin-top:8px;color:#e2136e;font-weight:700;font-size:13px">✓ Selected</div></div>
<div class="wd-card" id="cardNagad" onclick="sel('Nagad')"><img src="https://i.ibb.co/1p0pX1y/nagad.png"><div style="margin-top:8px;color:#f59e0b;font-size:13px">Tap to select</div></div>
</div>
<div style="margin-top:16px"><label style="font-size:13px">📞 একাউন্ট নম্বর</label><input class="wd-input" id="wNum" placeholder="01XXXXXXXXXX"></div>
<div style="margin-top:12px"><label style="font-size:13px">💵 টাকার পরিমাণ</label><input class="wd-input" id="wAmt" type="number" placeholder="৳ 0.00"><div style="font-size:12px;color:#64748b;margin-top:4px">মিনিমাম: ৳<span id="minW">1,000.00</span></div></div>
<button class="btn-blue" style="margin-top:16px;background:#94a3b8" id="wdBtn" onclick="doWd()">🔒 ব্যালেন্স যথেষ্ট নয়</button>
<div style="font-size:12px;margin-top:12px">⏰ <span id="payTime">প্রতিদিন রাত 8PM - 10PM</span><br>📋 নিয়ম: <span id="payRule">ভুল Number দিবেন না</span></div>
</div>
<div class="card"><div style="font-weight:700">🕒 উইথড্র হিস্ট্রি</div><div style="text-align:center;padding:20px;color:#94a3b8"><div style="font-size:40px">🕒</div>কোনো উইথড্র হিস্ট্রি নেই</div></div>
</div>

<div id="t-profile" style="display:none"><div class="card"><div class="bal-big">৳<span id="pBal">60</span></div><div style="text-align:center">ID: <span id="pId"></span></div></div></div>

<div class="btm"><div id="b-home" class="on" onclick="go('home')">🏠<br>হোম</div><div id="b-earn" onclick="go('earn')">📦<br>আয়</div><div id="b-support" onclick="go('support')">🎧<br>সাপোর্ট</div><div id="b-withdraw" onclick="go('withdraw')">💳<br>উইথড্র</div><div id="b-profile" onclick="go('profile')">👤<br>প্রোফাইল</div></div>

<div style="display:none"><span id="ytLink"></span><span id="chLink"></span><span id="fbLink"></span></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let curM='bKash';let curSlide=0;
function sel(m){curM=m;document.getElementById('cardBkash').classList.toggle('selected',m=='bKash');document.getElementById('cardNagad').classList.toggle('selected',m=='Nagad');checkBal()}
function go(t){['home','earn','support','withdraw','profile'].forEach(x=>{document.getElementById('t-'+x).style.display=x==t?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==t);});}
function checkBal(){let b=parseInt(document.getElementById('topBal').innerText)||0;let btn=document.getElementById('wdBtn');if(b>=1000){btn.style.background='#1e40af';btn.innerText='✅ উইথড্র রিকোয়েস্ট করুন';}else{btn.style.background='#94a3b8';btn.innerText='🔒 ব্যালেন্স যথেষ্ট নয়';}}
function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{
document.getElementById('topBal').innerText=d.user.balance;document.getElementById('bal').innerText=d.user.balance;document.getElementById('pBal').innerText=d.user.balance;document.getElementById('pId').innerText=uid;
document.getElementById('watched').innerText=d.user.ads_watched||0;
document.getElementById('adRate').innerText=d.settings.ad_reward;document.getElementById('adRate2').innerText=d.settings.ad_reward;
document.getElementById('appNameTop').innerText=d.settings.app_name;
document.getElementById('adminTitle').innerText=d.settings.admin_msg_title;
document.getElementById('adminDesc').innerText=d.settings.admin_msg_desc;
document.getElementById('myAdTitle').innerText=d.settings.my_ad_title;
document.getElementById('myAdDesc').innerText=d.settings.my_ad_desc;
document.getElementById('payTime').innerText=d.settings.payment_time;
document.getElementById('payRule').innerText=d.settings.payment_rules;
document.getElementById('minW').innerText=d.settings.min_withdraw+'.00';
document.getElementById('ytLink').innerText=d.tasks[0].link;
document.getElementById('chLink').innerText=d.tasks[1].link;
document.getElementById('fbLink').innerText=d.tasks[2].link;
let sBox=document.getElementById('slider');sBox.innerHTML='';d.slider.forEach((s,i)=>{sBox.innerHTML+=`<div class="slide ${i==0?'active':''}" onclick="window.open('${s.link}')"><img src="${s.img}"></div>`});
let dBox=document.getElementById('dots');dBox.innerHTML='';d.slider.forEach((_,i)=>{dBox.innerHTML+=`<span class="dot ${i==0?'active':''}"></span>`});
let tBox=document.getElementById('tasksBox');tBox.innerHTML='';d.tasks.forEach(t=>{tBox.innerHTML+=`<div class="card"><div style="display:flex;justify-content:space-between"><span>${t.title}</span><b>৳${t.reward}</b></div><button class="btn-blue" style="background:${t.color};margin-top:10px" onclick="window.open('${t.link}','_blank')">${t.btn}</button></div>`});
checkBal();
setInterval(()=>{let sl=document.querySelectorAll('.slide');let dt=document.querySelectorAll('.dot');if(!sl.length)return;sl[curSlide].classList.remove('active');dt[curSlide].classList.remove('active');curSlide=(curSlide+1)%sl.length;sl[curSlide].classList.add('active');dt[curSlide].classList.add('active');},3000);
});}
function watchAd(){let b=document.getElementById('adBtn');if(typeof show_11764581!=='undefined'){b.innerText='Loading...';show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(x=>{alert(x.msg);b.innerText='▶ বিজ্ঞাপন দেখুন';load();})});}else{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(x=>{alert(x.msg);load();})}}
function doWd(){let n=document.getElementById('wNum').value;let a=document.getElementById('wAmt').value;fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}&method=${curM}`).then(r=>r.json()).then(x=>alert(x.msg))}
function dailyCheck(){fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
load();
</script></body></html>
"""

# ================= ADMIN - FULL FIXED =================
ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Admin</title><script src="https://cdn.tailwindcss.com"></script>
<style>body{background:#eef6f3}.card{background:#fff;border-radius:18px;padding:16px;margin:10px;box-shadow:0 4px 12px rgba(0,0,0,.05)}.inp{width:100%;padding:12px;border:1px solid #ddd;border-radius:12px;margin-top:6px;background:#f9fafb}.lab{font-weight:700;margin-top:12px;display:block}</style>
</head><body style="max-width:500px;margin:0 auto;padding:10px">
<div style="background:linear-gradient(135deg,#0f766e,#115e59);color:#fff;padding:18px;border-radius:18px"><h1 style="font-weight:900;font-size:20px">🔗 Admin Panel - Full Control</h1><p style="opacity:.8;font-size:12px">ID: {{ADMIN_ID}}</p></div>

<div class="card"><h2 style="font-weight:900">📢 1 নাম্বার পেজ - নিজের বিজ্ঞাপন (My Ad)</h2>
<label class="lab">My Ad Title:</label><input id="myAdTitle" class="inp">
<label class="lab">My Ad Description:</label><input id="myAdDesc" class="inp">
<label class="lab">Admin Message Title:</label><input id="adTitle" class="inp">
<label class="lab">Admin Message Description:</label><input id="adDesc" class="inp">
</div>

<div class="card"><h2 style="font-weight:900">🔗 সব লিংক - 6 টা</h2>
<label class="lab">YouTube Link:</label><input id="ytLink" class="inp">
<label class="lab">Telegram Channel Link:</label><input id="chLink" class="inp">
<label class="lab">Facebook Page Link:</label><input id="fbLink" class="inp">
<label class="lab">Company Link 1:</label><input id="c1" class="inp">
<label class="lab">Company Link 2:</label><input id="c2" class="inp">
<label class="lab">Company Link 3:</label><input id="c3" class="inp">
</div>

<div class="card"><h2 style="font-weight:900">💸 4 নাম্বার পেজ - Withdraw Setting</h2>
<label class="lab">Payment Time (তুমি লিখবে):</label><input id="payTime" class="inp" placeholder="প্রতিদিন রাত 8PM - 10PM">
<label class="lab">Payment Rules:</label><input id="payRule" class="inp" placeholder="1. ভুল Number দিবেন না 2. Min ৳1000">
<label class="lab">Min Withdraw:</label><input id="minW" class="inp" type="number">
</div>

<div class="card"><h2 style="font-weight:900">⚙️ সাধারণ সেটিং</h2>
<label class="lab">App Name:</label><input id="appName" class="inp">
<label class="lab">Per Ad Reward:</label><input id="perAd" class="inp" type="number">
<label class="lab">Welcome Bonus:</label><input id="wel" class="inp" type="number">
</div>

<div class="card"><h2 style="font-weight:900">🖼️ Slider Images (3 টা)</h2>
<label class="lab">Slider 1 Image URL:</label><input id="s1" class="inp">
<label class="lab">Slider 2 Image URL:</label><input id="s2" class="inp">
<label class="lab">Slider 3 Image URL:</label><input id="s3" class="inp">
</div>

<button onclick="saveAll()" style="width:100%;background:#0f766e;color:#fff;padding:16px;border-radius:14px;font-weight:900;margin:12px 0">💾 SAVE ALL - সব আপডেট</button>

<div class="card"><h2>Withdraw Requests</h2><div id="wdList"></div></div>

<script>
let qp=new URLSearchParams(location.search);let aid=qp.get('id')||'8807178385';
function load(){fetch(`/api/get_full?id=${aid}`).then(r=>r.json()).then(d=>{
document.getElementById('myAdTitle').value=d.settings.my_ad_title;
document.getElementById('myAdDesc').value=d.settings.my_ad_desc;
document.getElementById('adTitle').value=d.settings.admin_msg_title;
document.getElementById('adDesc').value=d.settings.admin_msg_desc;
document.getElementById('ytLink').value=d.tasks[0].link;
document.getElementById('chLink').value=d.tasks[1].link;
document.getElementById('fbLink').value=d.tasks[2].link;
document.getElementById('c1').value=d.tasks[3].link;
document.getElementById('c2').value=d.tasks[4].link;
document.getElementById('c3').value=d.tasks[5].link;
document.getElementById('payTime').value=d.settings.payment_time;
document.getElementById('payRule').value=d.settings.payment_rules;
document.getElementById('minW').value=d.settings.min_withdraw;
document.getElementById('appName').value=d.settings.app_name;
document.getElementById('perAd').value=d.settings.ad_reward;
document.getElementById('wel').value=d.settings.welcome_bonus;
document.getElementById('s1').value=d.slider[0].img;
document.getElementById('s2').value=d.slider[1].img;
document.getElementById('s3').value=d.slider[2].img;
});
fetch(`/api/admin/withdraws?id=${aid}`).then(r=>r.json()).then(d=>{let l=document.getElementById('wdList');l.innerHTML='';d.forEach(w=>{l.innerHTML+=`<div style="display:flex;justify-content:space-between;padding:8px;background:#f9fafb;margin:6px 0;border-radius:10px"><div>${w.uid} - ${w.method} - ${w.num} - ৳${w.amt}</div><button onclick="approve('${w.uid}','${w.amt}')" style="background:green;color:#fff;padding:4px 10px;border-radius:6px">Ok</button></div>`})})
}
function saveAll(){
let data={
myAdTitle:document.getElementById('myAdTitle').value,
myAdDesc:document.getElementById('myAdDesc').value,
adTitle:document.getElementById('adTitle').value,
adDesc:document.getElementById('adDesc').value,
yt:document.getElementById('ytLink').value,
ch:document.getElementById('chLink').value,
fb:document.getElementById('fbLink').value,
c1:document.getElementById('c1').value,
c2:document.getElementById('c2').value,
c3:document.getElementById('c3').value,
payTime:document.getElementById('payTime').value,
payRule:document.getElementById('payRule').value,
minW:document.getElementById('minW').value,
appName:document.getElementById('appName').value,
perAd:document.getElementById('perAd').value,
wel:document.getElementById('wel').value,
s1:document.getElementById('s1').value,
s2:document.getElementById('s2').value,
s3:document.getElementById('s3').value
};
fetch(`/api/admin/save_all?id=${aid}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(()=>alert('✅ সব Save হয়েছে'))
}
function approve(uid,amt){fetch(`/api/admin/approve?id=${aid}&uid=${uid}&amt=${amt}`).then(()=>{alert('Done');load()})}
load();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page():
    if not is_admin(request.args.get('id')): return "Unauthorized",403
    return render_template_string(ADMIN_HTML.replace("{{ADMIN_ID}}",str(ADMIN_ID)))
@app.route('/health')
def health(): return "ok",200

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385'); d=load_db()
    if uid not in d['users']:
        d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'last_daily':''}
        save_db(d)
    return jsonify({"user":d['users'][uid],"settings":d['settings'],"slider":d['slider'],"tasks":d['tasks']})

@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); d=load_db()
    if d['users'][uid]['ads_watched']>=d['settings']['ad_limit']: return jsonify({"msg":"Limit Done"})
    d['users'][uid]['balance']+=d['settings']['ad_reward']; d['users'][uid]['ads_watched']+=1; save_db(d)
    return jsonify({"msg":f"✅ ৳{d['settings']['ad_reward']} যোগ"})

@app.route('/api/daily')
def daily():
    uid=request.args.get('id'); d=load_db(); today=str(datetime.date.today())
    if d['users'][uid].get('last_daily')==today: return jsonify({"msg":"আজ নিয়েছো"})
    d['users'][uid]['balance']+=d['settings']['daily_bonus']; d['users'][uid]['last_daily']=today; save_db(d)
    return jsonify({"msg":"✅ ৳10 বোনাস"})

@app.route('/api/withdraw')
def wd():
    uid=request.args.get('id'); amt=int(request.args.get('amt') or 0); num=request.args.get('num'); meth=request.args.get('method','bKash'); d=load_db()
    if amt<d['settings']['min_withdraw']: return jsonify({"msg":f"Min {d['settings']['min_withdraw']}"})
    if d['users'][uid]['balance']<amt: return jsonify({"msg":"Balance কম"})
    d['users'][uid]['balance']-=amt; d['withdraws'].append({"uid":uid,"amt":amt,"num":num,"method":meth}); save_db(d)
    return jsonify({"msg":"✅ Request গেছে"})

@app.route('/api/admin/withdraws')
def admin_wd():
    if not is_admin(request.args.get('id')): return jsonify([])
    d=load_db(); return jsonify(d['withdraws'])

@app.route('/api/admin/approve')
def approve():
    if not is_admin(request.args.get('id')): return jsonify({"error":"no"})
    d=load_db(); uid=request.args.get('uid'); amt=request.args.get('amt')
    d['withdraws']=[w for w in d['withdraws'] if not (w['uid']==uid and str(w['amt'])==str(amt))]; save_db(d); return jsonify({"ok":True})

@app.route('/api/admin/save_all',methods=['POST'])
def save_all():
    if not is_admin(request.args.get('id')): return jsonify({"error":"no"})
    data=request.json; d=load_db()
    d['settings']['my_ad_title']=data.get('myAdTitle'); d['settings']['my_ad_desc']=data.get('myAdDesc')
    d['settings']['admin_msg_title']=data.get('adTitle'); d['settings']['admin_msg_desc']=data.get('adDesc')
    d['settings']['payment_time']=data.get('payTime'); d['settings']['payment_rules']=data.get('payRule')
    d['settings']['min_withdraw']=int(data.get('minW') or 1000)
    d['settings']['app_name']=data.get('appName'); d['settings']['ad_reward']=int(data.get('perAd') or 1)
    d['settings']['welcome_bonus']=int(data.get('wel') or 60)
    d['tasks'][0]['link']=data.get('yt'); d['tasks'][1]['link']=data.get('ch'); d['tasks'][2]['link']=data.get('fb')
    d['tasks'][3]['link']=data.get('c1'); d['tasks'][4]['link']=data.get('c2'); d['tasks'][5]['link']=data.get('c3')
    d['slider'][0]['img']=data.get('s1'); d['slider'][1]['img']=data.get('s2'); d['slider'][2]['img']=data.get('s3')
    save_db(d); return jsonify({"ok":True})

async def start(update: Update, context):
    uid=str(update.effective_user.id); d=load_db()
    if uid not in d['users']: d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'last_daily':''}; save_db(d)
    kb=[[InlineKeyboardButton("🚀 Open App", web_app={"url":f"{SELF_URL}/?id={uid}"})],
        [InlineKeyboardButton("👑 Admin", web_app={"url":f"{SELF_URL}/admin?id={uid}"})]]
    await update.message.reply_text("Welcome ✅", reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    app_bot=Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.run_polling()

if __name__=='__main__':
    threading.Thread(target=run_bot,daemon=True).start()
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
