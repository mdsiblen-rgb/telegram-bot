import os, json, threading, datetime, time, requests
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db.json"
SELF_URL = "https://telegram-bot-1-v77g.onrender.com"
app = Flask(__name__)

# Database - Auto Migrate Old File
def load_db():
    if not os.path.exists(DB_FILE) and os.path.exists("db_final_400_lines.json"):
        try:
            with open("db_final_400_lines.json",'r') as f: d=json.load(f)
            with open(DB_FILE,'w') as nf: json.dump(d,nf)
            return d
        except: pass
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [], "blacklisted_ips": [],
            "slider": [
                {"img":"https://img.freepik.com/free-vector/flat-design-earn-money-banner_23-2149439772.jpg","link":"https://t.me/ProtidinerKajBD","title":"🔥 প্রতিদিনের কাজ BD Official"},
                {"img":"https://img.freepik.com/free-vector/gradient-refer-friend-banner_23-2149373488.jpg","link":"https://t.me/ProtidinerKajBD","title":"💰 Refer ৳10 বোনাস"},
                {"img":"https://img.freepik.com/free-vector/flat-design-affiliate-marketing-banner_23-2149443391.jpg","link":"https://youtube.com/@ProtidinerKajBD","title":"▶️ YouTube Subscribe"}
            ],
            "settings":{
                "app_name":"প্রতিদিনের কাজ BD","ad_zone":"11764581","ad_reward":0.20,"ad_daily_limit":50,
                "ref_bonus":10,"min_withdraw":1000,"welcome_bonus":30,"daily_bonus":10,
                "ad_timer":30,"home_notice":"🔥 আজ রাত 8টায় পেমেন্ট ক্লিয়ার!"
            },
            "tasks":[
                {"id":1,"title":"YouTube ভিডিও দেখুন","reward":5,"link":"https://youtube.com/@ProtidinerKajBD","color":"#065f46","btn":"শুরু করুন"},
                {"id":2,"title":"Telegram Channel Join","reward":3,"link":"https://t.me/ProtidinerKajBD","color":"#1e40af","btn":"Join করুন"},
                {"id":3,"title":"Facebook Follow","reward":3,"link":"https://www.facebook.com/share/1AXw16vWRj/","color":"#1877F2","btn":"Follow"}
            ]
        }
    with open(DB_FILE,'r') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE,'w') as f: json.dump(f,d,indent=2)

# Keep Alive
def keep_alive():
    while True:
        try: time.sleep(240); requests.get(f"{SELF_URL}/health",timeout=10)
        except: pass
threading.Thread(target=keep_alive,daemon=True).start()

# MINI APP HTML - PROFESSIONAL
USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{max-width:430px;margin:0 auto;font-family:Arial;padding-bottom:90px;background:#eef2ff}
.top{background:#1e40af;color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
.bal-card{margin:12px;color:#fff;padding:18px;border-radius:20px;text-align:center;background:linear-gradient(135deg,#1e3a8a,#3b82f6)}
.bal-big{font-size:48px;font-weight:900}
.card{margin:12px;padding:14px;border-radius:18px;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.06)}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:bold;cursor:pointer;color:#fff;background:#1e40af;margin-top:8px}
.tab{display:none}.tab.on{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;display:flex;justify-content:space-around;background:#fff;padding:10px 0;border-top:1px solid #ddd;z-index:99}
.btm div{flex:1;text-align:center;font-size:12px;color:#888;cursor:pointer}.btm div.on{color:#1e40af;font-weight:bold}
.slider{position:relative;width:calc(100% - 24px);margin:12px;height:165px;overflow:hidden;border-radius:18px;background:#fff}
.slide{position:absolute;inset:0;opacity:0;transition:opacity.8s;cursor:pointer}.slide.active{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover}
.slide-title{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.7));color:#fff;padding:25px 12px 10px;font-weight:bold}
.dots{text-align:center}.dot{height:7px;width:7px;background:#bbb;border-radius:50%;display:inline-block;margin:0 3px}.dot.active{background:#1e40af}
.meth{flex:1;background:#fff;border-radius:16px;padding:14px 6px;text-align:center;cursor:pointer;border:2px solid #e5e7eb;position:relative}
.meth.sel{border-color:#1e40af!important;border-width:3px!important}
.meth.sel:after{content:'✓';position:absolute;top:6px;right:8px;background:#1e40af;color:#fff;width:20px;height:20px;border-radius:50%;line-height:20px;text-align:center}
.meth img{height:36px;width:auto;margin:0 auto 6px;display:block}
.task-item{display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid #eee;border-radius:12px;margin:8px 0}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:8px;box-sizing:border-box}
</style></head><body>
<div class="top"><div style="display:flex;gap:8px;align-items:center"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:32px;height:32px;border-radius:50%;background:#fff">প্রতিদিনের কাজ BD</div><span>৳<span id="bTop">0</span></span></div>
<div id="t-home" class="tab on">
<div class="slider" id="sliderBox"></div><div class="dots" id="dotsBox"></div>
<div class="bal-card"><p>আপনার ব্যালেন্স</p><div class="bal-big">৳<span id="bal">0</span></div><div style="display:flex;gap:10px;margin-top:10px"><div style="flex:1;background:rgba(255,255,255,.25);padding:8px;border-radius:10px">আজ <b><span id="adWatched">0</span>/50</b></div><div style="flex:1;background:rgba(255,255,255,.25);padding:8px;border-radius:10px">Refer <b>৳10</b></div></div><button class="btn" style="background:#fff;color:#1e40af;margin-top:10px" onclick="go('earn')">💰 এখনই আয় করুন</button></div>
<div class="card" style="display:flex;justify-content:space-between;align-items:center"><div><b>🎁 Daily Check-in</b><br><small>৳10 বোনাস</small></div><button class="btn" style="width:auto;background:#f59e0b;padding:10px 16px" onclick="dailyCheck()">নিন</button></div>
<div class="card" id="homeNoticeBox" style="display:none;background:#fef3c7;border:2px dashed #f59e0b"><h4 style="margin:0">📢 নোটিশ</h4><p id="homeNoticeText"></p></div>
</div>
<div id="t-earn" class="tab">
<div class="card"><h3>📺 কোম্পানি বিজ্ঞাপন Zone 11764581</h3><div style="font-size:48px;text-align:center;font-weight:900;color:#1e40af">৳<span id="adR2">0.20</span></div><button class="btn" id="adBtn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button><p style="font-size:11px;color:green">✅ পুরো Ad দেখলে তবেই টাকা - Reward Verification ON</p><p style="font-size:11px">Watched: <span id="adWatched2">0</span>/50 | Timer: <span id="timer">Ready</span></p></div>
<div class="card"><h3>📋 কোম্পানির সাথে যুক্ত কাজ</h3><div id="tasksContainer"></div></div>
<div class="card"><h4>👥 Refer Link</h4><div id="refLink" style="font-size:11px;background:#f1f5f9;padding:12px;border-radius:8px;word-break:break-all;border:1px dashed #94a3b8;font-weight:bold">Loading...</div><button class="btn" style="background:#10b981" onclick="navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('Copied!')">Copy Link</button></div>
</div>
<div id="t-support" class="tab"><div class="card"><h3>🎧 সাপোর্ট</h3><button class="btn" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">📢 Channel</button><button class="btn" style="background:#FF0000" onclick="window.open('https://youtube.com/@ProtidinerKajBD','_blank')">▶️ YouTube</button><button class="btn" style="background:#1877F2" onclick="window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank')">📘 Facebook</button></div></div>
<div id="t-withdraw" class="tab"><div class="card"><h3>💳 উইথড্র - bKash Nagad</h3><div style="font-size:40px;text-align:center;font-weight:900">৳<span class="bal2">0</span></div><div style="background:#f8fafc;padding:10px;border-radius:10px;text-align:center;font-size:12px">Min 1000 - আর <b id="needAmt">0</b> লাগবে - <span id="wdMsg"></span></div></div><div class="card"><h4>💳 মেথড - Original Logo</h4><div style="display:flex;gap:12px"><div onclick="selectMethod('bKash')" id="m-bKash" class="meth sel"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/BKash_Logo.png/250px-BKash_Logo.png" onerror="this.src='https://i.ibb.co/0X1s0KZ/bkash.png'"><div style="font-weight:900;color:#e2136e">bKash</div><div style="font-size:10px">Personal</div></div><div onclick="selectMethod('Nagad')" id="m-Nagad" class="meth"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Nagad_Logo.png/250px-Nagad_Logo.png" onerror="this.src='https://i.ibb.co/6W8g6Tq/nagad.png'"><div style="font-weight:900;color:#ff6c00">Nagad</div><div style="font-size:10px">Personal</div></div></div><input id="wNum" placeholder="bKash Number"><input id="wAmt" type="number" placeholder="Amount Min 1000"><button class="btn" onclick="doWithdraw()">উইথড্র করুন</button></div></div>
<div class="btm"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>
<script>
const tg=Telegram.WebApp;let qp=new URLSearchParams(location.search);let uid=qp.get('id')||tg.initDataUnsafe?.user?.id||"8807178385";
let curSlide=0,slideInt,curMeth='bKash',cooldown=0;
function go(t){document.querySelectorAll('.tab').forEach(e=>e.classList.remove('on'));document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));document.getElementById('b-'+t).classList.add('on');}
function selectMethod(m){curMeth=m;document.querySelectorAll('.meth').forEach(e=>e.classList.remove('sel'));document.getElementById('m-'+m).classList.add('sel');document.getElementById('wNum').placeholder=m+' Number';}
function initSlider(imgs){let box=document.getElementById('sliderBox');let dots=document.getElementById('dotsBox');if(!imgs||!imgs.length)return;box.innerHTML='';dots.innerHTML='';imgs.forEach((it,i)=>{let d=document.createElement('div');d.className='slide'+(i==0?' active':'');d.innerHTML=`<img src="${it.img}"><div class="slide-title">${it.title}</div>`;d.onclick=()=>window.open(it.link,'_blank');box.appendChild(d);let dot=document.createElement('span');dot.className='dot'+(i==0?' active':'');dots.appendChild(dot);});if(slideInt)clearInterval(slideInt);slideInt=setInterval(()=>{let s=document.querySelectorAll('.slide');let ds=document.querySelectorAll('.dot');s[curSlide].classList.remove('active');ds[curSlide].classList.remove('active');curSlide=(curSlide+1)%s.length;s[curSlide].classList.add('active');ds[curSlide].classList.add('active');},3500);}
function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{if(d.banned){document.body.innerHTML='<h2 style=text-align:center;margin-top:100px>🚫 Banned</h2>';return;}document.getElementById('bal').innerText=d.user.balance.toFixed(2);document.getElementById('bTop').innerText=d.user.balance.toFixed(2);document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance.toFixed(2));document.getElementById('adWatched').innerText=d.user.ads_watched||0;document.getElementById('adWatched2').innerText=d.user.ads_watched||0;let s=d.settings;document.getElementById('adR2').innerText=s.ad_reward;document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;if(s.home_notice){document.getElementById('homeNoticeBox').style.display='block';document.getElementById('homeNoticeText').innerText=s.home_notice;}let need=Math.max(0,s.min_withdraw-d.user.balance);document.getElementById('needAmt').innerText=need.toFixed(0);document.getElementById('wdMsg').innerText=d.user.balance>=s.min_withdraw?'পারবেন':'লাগবে';cooldown=s.ad_timer;initSlider(d.slider);let tc=document.getElementById('tasksContainer');tc.innerHTML='';d.tasks.forEach(t=>{tc.innerHTML+=`<div class="task-item"><div><b>${t.title}</b><br><small>৳${t.reward}</small></div><button class="btn" style="width:auto;background:${t.color};padding:8px 14px" onclick="window.open('${t.link}','_blank')">${t.btn}</button></div>`;});});}
function watchAd(){let btn=document.getElementById('adBtn');if(cooldown>0 && window.lastAd && Date.now()-window.lastAd<cooldown*1000){alert(cooldown+'s পর আবার');return;}if(typeof show_11764581!=='undefined'){btn.innerText='Loading...';show_11764581().then(()=>{window.lastAd=Date.now();fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{if(d.reward>0){alert('✅ ৳'+d.reward);}else{alert(d.msg);}btn.innerText='▶ বিজ্ঞাপন দেখুন';load();});}).catch(()=>{btn.innerText='▶ বিজ্ঞাপন দেখুন';alert('পুরো Ad দেখুন');});}else{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{alert(d.msg);load();});}}
function doWithdraw(){let n=document.getElementById('wNum').value;let a=document.getElementById('wAmt').value;if(!n||!a)return alert('দাও');fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}&method=${curMeth}`).then(r=>r.json()).then(d=>alert(d.msg));}
function dailyCheck(){fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(d=>{alert(d.msg);load();});}
load();
</script></body></html>
"""

# ADMIN WEB PANEL
ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin</title>
<style>body{max-width:900px;margin:0 auto;font-family:Arial;padding:12px;background:#f1f5f9}.card{background:#fff;padding:14px;border-radius:12px;margin:10px 0;box-shadow:0 2px 8px rgba(0,0,0,.06)}.btn{padding:10px 14px;border:none;border-radius:8px;font-weight:bold;cursor:pointer;color:#fff;background:#1e40af;margin:4px}input{padding:10px;border-radius:8px;border:1px solid #ddd;margin:4px}</style></head><body>
<h2>📊 Admin Control - প্রতিদিনের কাজ BD</h2>
<div class="card"><h3>📊 Dashboard</h3><div id="stats">Loading...</div></div>
<div class="card"><h3>💰 Withdrawal Request</h3><div id="wdList">Loading...</div></div>
<div class="card"><h3>⚙️ App Settings - CPM & Limit</h3>
Ad Reward: <input id="adR" type="number" step="0.01"> <button class="btn" onclick="setRate()">Set Rate</button><br>
Daily Limit: <input id="adL" type="number"> <button class="btn" onclick="setLimit()">Set Limit</button><br>
Min Withdraw: <input id="minW" type="number"> <button class="btn" onclick="setMin()">Set Min</button><br>
Ref Bonus: <input id="refB" type="number"> <button class="btn" onclick="setRef()">Set Ref</button><br>
Home Notice: <input id="notice" style="width:60%"> <button class="btn" onclick="setNotice()">Set Notice</button>
</div>
<div class="card"><h3>🚫 User Management</h3><input id="searchId" placeholder="User ID"><button class="btn" onclick="searchUser()">Search</button><div id="userRes"></div></div>
<div class="card"><h3>📋 Task & Slider</h3><div id="taskList"></div><input id="tTitle" placeholder="Title"><input id="tReward" placeholder="Reward"><input id="tLink" placeholder="Link"><button class="btn" onclick="addTask()">Add Task</button></div>
<script>
let qp=new URLSearchParams(location.search);let adminId=qp.get('id')||'8807178385';
function load(){fetch(`/api/admin/stats?id=${adminId}`).then(r=>r.json()).then(d=>{document.getElementById('stats').innerHTML=`Total Users: ${d.total}<br>Pending WD: ${d.pending}<br>Today Earning Est: $${d.earning}`;let wl=document.getElementById('wdList');wl.innerHTML='';d.withdraws.forEach(w=>{wl.innerHTML+=`<div style="border:1px solid #ddd;padding:8px;margin:4px;border-radius:8px">${w.uid} - ${w.method} ${w.num} - ৳${w.amt} <button class="btn" style="background:green" onclick="approveWd('${w.uid}','${w.amt}')">Approve</button><button class="btn" style="background:red" onclick="rejectWd('${w.uid}','${w.amt}')">Reject</button></div>`;});});fetch(`/api/get_full?id=${adminId}`).then(r=>r.json()).then(d=>{document.getElementById('adR').value=d.settings.ad_reward;document.getElementById('adL').value=d.settings.ad_daily_limit;document.getElementById('minW').value=d.settings.min_withdraw;document.getElementById('refB').value=d.settings.ref_bonus;document.getElementById('notice').value=d.settings.home_notice;let tl=document.getElementById('taskList');tl.innerHTML='';d.tasks.forEach(t=>{tl.innerHTML+=`<div>${t.title} - ৳${t.reward}</div>`;});});}
function setRate(){fetch(`/api/admin/set_rate?id=${adminId}&rate=${document.getElementById('adR').value}`).then(()=>{alert('OK');load();});}
function setLimit(){fetch(`/api/admin/set_limit?id=${adminId}&limit=${document.getElementById('adL').value}`).then(()=>{alert('OK');load();});}
function setMin(){fetch(`/api/admin/set_min?id=${adminId}&min=${document.getElementById('minW').value}`).then(()=>{alert('OK');load();});}
function setRef(){fetch(`/api/admin/set_ref?id=${adminId}&ref=${document.getElementById('refB').value}`).then(()=>{alert('OK');load();});}
function setNotice(){fetch(`/api/admin/set_notice?id=${adminId}&notice=${encodeURIComponent(document.getElementById('notice').value)}`).then(()=>{alert('OK');load();});}
function searchUser(){let uid=document.getElementById('searchId').value;fetch(`/api/admin/user?id=${adminId}&uid=${uid}`).then(r=>r.json()).then(d=>{document.getElementById('userRes').innerHTML=d.found?`Balance: ${d.user.balance}<br>Ads: ${d.user.ads_watched}<br><button class="btn" onclick="ban('${uid}')">Ban</button> <button class="btn" style="background:green" onclick="unban('${uid}')">Unban</button> <input id="addBal" placeholder="Add Amount"><button class="btn" onclick="addBal('${uid}')">Add Balance</button>`:'Not Found';});}
function ban(uid){fetch(`/api/admin/ban?id=${adminId}&uid=${uid}`).then(()=>alert('Banned'));}
function unban(uid){fetch(`/api/admin/unban?id=${adminId}&uid=${uid}`).then(()=>alert('Unbanned'));}
function addBal(uid){fetch(`/api/admin/addbal?id=${adminId}&uid=${uid}&amt=${document.getElementById('addBal').value}`).then(()=>alert('Added'));}
function approveWd(uid,amt){fetch(`/api/admin/approve?id=${adminId}&uid=${uid}&amt=${amt}`).then(()=>{alert('Approved');load();});}
function rejectWd(uid,amt){fetch(`/api/admin/reject?id=${adminId}&uid=${uid}&amt=${amt}`).then(()=>{alert('Rejected & Refunded');load();});}
function addTask(){let t=document.getElementById('tTitle').value;let r=document.getElementById('tReward').value;let l=document.getElementById('tLink').value;fetch(`/api/admin/add_task?id=${adminId}&title=${encodeURIComponent(t)}&reward=${r}&link=${encodeURIComponent(l)}`).then(()=>{alert('Added');load();});}
load();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page(): return render_template_string(ADMIN_HTML)
@app.route('/health')
def health(): return "ok",200

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385'); d=load_db()
    ip=request.headers.get('X-Forwarded-For', request.remote_addr)
    if uid in d['banned'] or ip in d['blacklisted_ips']: return jsonify({"banned":True})
    if uid not in d['users']:
        d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'ref_count':0,'last_daily':'','ip':ip,'last_ad_time':0}
        save_db(d)
    else:
        if d['users'][uid].get('balance',0)==0 and d['users'][uid].get('ads_watched',0)==0:
            d['users'][uid]['balance']=d['settings']['welcome_bonus']; save_db(d)
    return jsonify({"user":d['users'][uid],"settings":d['settings'],"slider":d['slider'],"tasks":d.get('tasks',[]),"banned":False})

@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); d=load_db(); now=time.time()
    if uid not in d['users']: return jsonify({"msg":"User not found","reward":0})
    if d['users'][uid].get('ads_watched',0) >= d['settings']['ad_daily_limit']:
        return jsonify({"msg":f"Daily Limit {d['settings']['ad_daily_limit']} Done","reward":0})
    if now - d['users'][uid].get('last_ad_time',0) < d['settings']['ad_timer']:
        return jsonify({"msg":f"{d['settings']['ad_timer']}s পর আবার","reward":0})
    d['users'][uid]['balance']+=d['settings']['ad_reward']
    d['users'][uid]['ads_watched']=d['users'][uid].get('ads_watched',0)+1
    d['users'][uid]['last_ad_time']=now
    save_db(d)
    return jsonify({"reward":d['settings']['ad_reward'],"msg":f"✅ ৳{d['settings']['ad_reward']} যোগ"})

@app.route('/api/daily')
def daily():
    uid=request.args.get('id'); d=load_db(); today=str(datetime.date.today())
    if d['users'][uid].get('last_daily')==today: return jsonify({"msg":"আজ নিয়েছো"})
    d['users'][uid]['balance']+=d['settings']['daily_bonus']; d['users'][uid]['last_daily']=today; save_db(d)
    return jsonify({"msg":f"✅ ৳{d['settings']['daily_bonus']} Daily!"})

@app.route('/api/withdraw')
def wd_req():
    uid=request.args.get('id'); num=request.args.get('num'); amt=int(float(request.args.get('amt') or 0)); method=request.args.get('method','bKash'); d=load_db()
    if d['users'][uid]['balance']<amt: return jsonify({"msg":"Balance কম"})
    if amt<d['settings']['min_withdraw']: return jsonify({"msg":f"Min {d['settings']['min_withdraw']}"})
    d['users'][uid]['balance']-=amt
    d['withdraws'].append({"uid":uid,"num":num,"amt":amt,"method":method,"date":str(datetime.datetime.now())})
    save_db(d)
    return jsonify({"msg":f"✅ {method} ৳{amt} Request OK - Admin Approve করবে"})

# ADMIN APIS
def is_admin(req_id):
    return str(req_id)==str(ADMIN_ID)

@app.route('/api/admin/stats')
def admin_stats():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db()
    return jsonify({"total":len(d['users']),"pending":len(d['withdraws']),"earning":len(d['users'])*0.5,"withdraws":d['withdraws'][-20:]})

@app.route('/api/admin/set_rate')
def admin_set_rate():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db(); d['settings']['ad_reward']=float(request.args.get('rate')); save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/set_limit')
def admin_set_limit():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db(); d['settings']['ad_daily_limit']=int(request.args.get('limit')); save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/set_min')
def admin_set_min():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db(); d['settings']['min_withdraw']=int(request.args.get('min')); save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/set_ref')
def admin_set_ref():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db(); d['settings']['ref_bonus']=int(request.args.get('ref')); save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/set_notice')
def admin_set_notice():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db(); d['settings']['home_notice']=request.args.get('notice'); save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/user')
def admin_user():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    uid=request.args.get('uid'); d=load_db()
    if uid in d['users']: return jsonify({"found":True,"user":d['users'][uid]})
    return jsonify({"found":False})
@app.route('/api/admin/ban')
def admin_ban():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    uid=request.args.get('uid'); d=load_db()
    if uid not in d['banned']: d['banned'].append(uid)
    save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/unban')
def admin_unban():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    uid=request.args.get('uid'); d=load_db()
    if uid in d['banned']: d['banned'].remove(uid)
    save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/addbal')
def admin_addbal():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    uid=request.args.get('uid'); amt=float(request.args.get('amt')); d=load_db()
    if uid in d['users']: d['users'][uid]['balance']+=amt; save_db(d)
    return jsonify({"ok":True})
@app.route('/api/admin/approve')
def admin_approve():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    uid=request.args.get('uid'); d=load_db(); d['withdraws']=[w for w in d['withdraws'] if w['uid']!=uid]; save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/reject')
def admin_reject():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    uid=request.args.get('uid'); amt=float(request.args.get('amt')); d=load_db()
    if uid in d['users']: d['users'][uid]['balance']+=amt
    d['withdraws']=[w for w in d['withdraws'] if w['uid']!=uid]; save_db(d); return jsonify({"ok":True})
@app.route('/api/admin/add_task')
def admin_add_task():
    if not is_admin(request.args.get('id')): return jsonify({"error":"not admin"})
    d=load_db(); d['tasks'].append({"id":len(d['tasks'])+1,"title":request.args.get('title'),"reward":int(request.args.get('reward')),"link":request.args.get('link'),"color":"#1e40af","btn":"শুরু করুন"}); save_db(d); return jsonify({"ok":True})

# TELEGRAM BOT - ADMIN CONTROL
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id); d=load_db()
    if uid not in d['users']:
        d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'ref_count':0,'last_daily':'','ip':'','last_ad_time':0}
        save_db(d)
    kb=[[InlineKeyboardButton("🚀 Open App", web_app={"url": f"{SELF_URL}/?id={uid}"})]]
    if str(uid)==str(ADMIN_ID):
        kb.append([InlineKeyboardButton("📊 Admin Panel", web_app={"url": f"{SELF_URL}/admin?id={uid}"})])
    await update.message.reply_text(f"Welcome {update.effective_user.first_name} ✅\nZone 11764581 Ready", reply_markup=InlineKeyboardMarkup(kb))

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id)!=str(ADMIN_ID): return
    d=load_db()
    text=f"📊 --- অ্যাডমিন ড্যাশবোর্ড ---\n👤 মোট ইউজার: {len(d['users'])}\n💸 পেন্ডিং: {len(d['withdraws'])}\n💵 আজকের আয় Est: ${len(d['users'])*0.5}\n━━━━━━━━━━━━━━━"
    kb=[
        [InlineKeyboardButton(f"💰 উইথড্রাল {len(d['withdraws'])}", callback_data="adm_wd"),
         InlineKeyboardButton("🚫 ইউজার ম্যানেজমেন্ট", callback_data="adm_users")],
        [InlineKeyboardButton("📢 ব্রডকাস্ট", callback_data="adm_broadcast"),
         InlineKeyboardButton("⚙️ অ্যাপ সেটিংস", callback_data="adm_settings")],
        [InlineKeyboardButton("🌐 Web Admin Open", web_app={"url": f"{SELF_URL}/admin?id={ADMIN_ID}"})]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query; data=query.data; d=load_db()
    if str(query.from_user.id)!=str(ADMIN_ID): return
    if data=="adm_wd":
        if not d['withdraws']: await query.edit_message_text("No Pending"); return
        txt="💸 Pending Withdraw:\n"
        kb=[]
        for w in d['withdraws'][-5:]:
            txt+=f"{w['uid']} - {w['method']} {w['num']} - ৳{w['amt']}\n"
            kb.append([InlineKeyboardButton(f"✅ {w['uid']} Approve", callback_data=f"approve_{w['uid']}_{w['amt']}"), InlineKeyboardButton(f"❌ Reject", callback_data=f"reject_{w['uid']}_{w['amt']}")])
        kb.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
        await query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("approve_"):
        _, uid, amt = data.split("_"); amt=float(amt)
        d['withdraws']=[w for w in d['withdraws'] if w['uid']!=uid]; save_db(d)
        await context.bot.send_message(uid, f"✅ আপনার ৳{amt} পাঠানো হয়েছে!")
        await query.edit_message_text(f"✅ Paid {uid} ৳{amt}")
    elif data.startswith("reject_"):
        _, uid, amt = data.split("_"); amt=float(amt)
        if uid in d['users']: d['users'][uid]['balance']+=amt
        d['withdraws']=[w for w in d['withdraws'] if w['uid']!=uid]; save_db(d)
        await context.bot.send_message(uid, f"❌ {amt} টাকা বাতিল, Balance ফেরত গেছে")
        await query.edit_message_text(f"❌ Rejected {uid}")
    elif data=="adm_users":
        await query.edit_message_text("🚫 User Management\n/search 88071xxxx - User দেখুন\n/ban 88071xxxx - Ban\n/unban 88071xxxx - Unban", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))
    elif data=="adm_settings":
        s=d['settings']
        await query.edit_message_text(f"⚙️ Settings\nAd Reward: {s['ad_reward']}\nDaily Limit: {s['ad_daily_limit']}\nMin WD: {s['min_withdraw']}\n\n/set_rate 0.20\n/set_limit 50", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))
    elif data=="back":
        await admin_cmd(update, context)

def run_bot():
    app_bot=Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start_cmd))
    app_bot.add_handler(CommandHandler("admin", admin_cmd))
    app_bot.add_handler(CallbackQueryHandler(callback_handler))
    print("Bot Started - Final Professional")
    app_bot.run_polling(drop_pending_updates=True)

if __name__=='__main__':
    threading.Thread(target=run_bot,daemon=True).start()
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)),use_reloader=False)
