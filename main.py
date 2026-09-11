import os, json, threading, datetime
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "final_everything_db.json"
app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},
            "withdraws": [],
            "slider": [
                {"img": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800", "link": "https://t.me/ProtidinerKajBD"},
                {"img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800", "link": "https://t.me/ProtidinerKajBD"},
                {"img": "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800", "link": "https://youtube.com/@ProtidinerKajBD"}
            ],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD",
                "company_name": "Protidiner Kaj BD",
                "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "banner_color": "#1e40af",
                "ad_zone": "11764581",
                "app_id": "3485122",
                "ad_reward": 1,
                "ad_daily_limit": 100,
                "ad_timer": 30,
                "ref_bonus": 50,
                "min_withdraw": 1000,
                "channel_link": "https://t.me/ProtidinerKajBD",
                "youtube_link": "https://youtube.com/@ProtidinerKajBD",
                "fb_link": "https://www.facebook.com/share/1AXw16vWRj/",
                "admin_msg": "Admin Message - ProtidinerKajBD",
                "official_msg": "অফিশিয়াল চ্যানেল - ProtidinerKajBD",
                "how_to_work": "1. Slider Ads দেখুন 2. বিজ্ঞাপন দেখুন 3. Task করুন 4. Refer করুন 5. Withdraw করুন"
            },
            "tasks": [
                {"id": 1, "title": "YouTube ভিডিও দেখুন", "reward": 25, "link": "https://youtube.com/@ProtidinerKajBD", "color": "#065f46", "btn": "শুরু করুন"},
                {"id": 2, "title": "Telegram Channel Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join"},
                {"id": 3, "title": "Facebook Follow", "reward": 15, "link": "https://www.facebook.com/share/1AXw16vWRj/", "color": "#1877F2", "btn": "Follow"}
            ]
        }
    with open(DB_FILE, 'r') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(d, f, indent=2)
db = load_db()

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>App</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='3485122' data-sdk='show_11764581'></script>
<style>
body{max-width:430px;margin:0 auto;font-family:Arial;padding-bottom:90px;transition:all.3s}
.top{color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:20}
.top img{width:32px;height:32px;border-radius:50%;background:#fff;padding:2px}
.card{margin:12px;padding:16px;border-radius:20px;box-shadow:0 4px 15px rgba(0,0,0,.08);transition:all.3s}
.bal{font-size:40px;font-weight:900;text-align:center}
.btn{width:100%;padding:14px;border:none;border-radius:12px;color:#fff;font-weight:bold;cursor:pointer;margin-top:8px}
.tab{display:none}.tab.on{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #ddd;z-index:20}
.btm div{flex:1;text-align:center;font-size:11px;cursor:pointer}.btm div.on{font-weight:bold}
.slider{position:relative;width:100%;height:170px;overflow:hidden;border-radius:20px;margin:12px 0}
.slide{position:absolute;width:100%;height:100%;opacity:0;transition:opacity 1s ease;cursor:pointer}
.slide.active{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover}
.dots{text-align:center;margin-top:4px}
.dot{height:8px;width:8px;background:#bbb;border-radius:50%;display:inline-block;margin:0 3px}
.dot.active{background:#1e40af}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:6px;box-sizing:border-box}
</style>
</head><body id="body">
<div class="top" id="topBar"><div style="display:flex;align-items:center;gap:8px"><img id="appLogo" src=""><span id="appName">Loading</span></div><span>৳<span id="bTop">0</span></span></div>
<div id="t-home" class="tab on">
<div class="slider" id="slider"></div><div class="dots" id="dots"></div>
<div class="card" id="card1"><div class="bal" id="balColor">৳<span id="bal">0</span></div><button class="btn" id="earnBtn" onclick="go('earn')">💰 আয় করুন</button></div>
<div class="card" id="card2"><b id="adminMsg"></b><br><small>ProtidinerKajBD</small><br><br><b id="offMsg"></b><br><small id="howWork"></small></div>
</div>
<div id="t-earn" class="tab">
<div class="card" id="card3"><p>প্রতি Ads এ ৳<span id="adR">1</span></p><div class="bal">৳<span id="adR2">1</span></div><button class="btn" style="background:#1e40af" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button><p style="font-size:10px">Daily Limit: <span id="adLimit">100</span></p></div>
<div id="taskList"></div>
<div class="card"><p>👥 Refer ৳<span id="refR">50</span></p><p id="refLink" style="font-size:11px;background:#f1f5f9;padding:8px;border-radius:8px;word-break:break-all"></p><button class="btn" style="background:#10b981" onclick="copyRef()">Copy Link</button></div>
</div>
<div id="t-support" class="tab"><div class="card"><p>Support - Channel Join করুন</p><button class="btn" style="background:#111" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">Join Channel</button></div></div>
<div id="t-withdraw" class="tab"><div class="card"><div class="bal">৳<span class="bal2">0</span></div><input id="num" placeholder="bKash/Nagad Number"><input id="amt" type="number" placeholder="Amount"><button class="btn" style="background:#1e40af" onclick="withdraw()">উইথড্র</button><p>Min ৳<span id="minW">1000</span></p></div></div>
<div class="btm" id="bottomBar"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>
<script>
const tg = window.Telegram.WebApp;
let uid = new URLSearchParams(location.search).get('id') || tg.initDataUnsafe?.user?.id || "8807178385";
let ref = new URLSearchParams(location.search).get('ref');
let currentSlide=0, interval;
function applyTheme(){
  const th = tg.themeParams;
  document.getElementById('body').style.background = th.bg_color || "#eef2ff";
  document.getElementById('body').style.color = th.text_color || "#000";
  document.querySelectorAll('.card').forEach(c=>{ c.style.background = th.secondary_bg_color || "#fff"; });
}
function initSlider(imgs){
 let s=document.getElementById('slider'); let d=document.getElementById('dots'); if(!s) return;
 s.innerHTML=''; d.innerHTML='';
 imgs.forEach((it,i)=>{
  let div=document.createElement('div'); div.className='slide'+(i==0?' active':''); div.innerHTML=`<img src="${it.img}">`; div.onclick=()=>window.open(it.link,'_blank'); s.appendChild(div);
  let dot=document.createElement('span'); dot.className='dot'+(i==0?' active':''); d.appendChild(dot);
 });
 if(interval) clearInterval(interval);
 interval=setInterval(()=>{ let sl=document.querySelectorAll('.slide'); let dt=document.querySelectorAll('.dot'); if(!sl.length) return; sl[currentSlide].classList.remove('active'); dt[currentSlide].classList.remove('active'); currentSlide=(currentSlide+1)%sl.length; sl[currentSlide].classList.add('active'); dt[currentSlide].classList.add('active'); }, 3500);
}
document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied');}
function load(){
 fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.balance; document.getElementById('bTop').innerText=d.user.balance; document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance);
  let s=d.settings; document.getElementById('appName').innerText=s.app_name; document.getElementById('appLogo').src=s.logo_url; document.getElementById('topBar').style.background=s.banner_color; document.getElementById('earnBtn').style.background=s.banner_color; document.getElementById('balColor').style.color=s.banner_color; document.getElementById('adR').innerText=s.ad_reward; document.getElementById('adR2').innerText=s.ad_reward; document.getElementById('refR').innerText=s.ref_bonus; document.getElementById('minW').innerText=s.min_withdraw; document.getElementById('adminMsg').innerText=s.admin_msg; document.getElementById('offMsg').innerText=s.official_msg; document.getElementById('howWork').innerText=s.how_to_work; document.getElementById('adLimit').innerText=s.ad_daily_limit;
  initSlider(d.slider);
  let tl=document.getElementById('taskList'); tl.innerHTML=''; d.tasks.forEach(t=>{ tl.innerHTML+=`<div class="card"><p>${t.title} ৳${t.reward}</p><button class="btn" style="background:${t.color}" onclick="doTask(${t.id},'${t.link}')">${t.btn}</button></div>`; });
 });
}
function watchAd(){ show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ if(d.ok){alert('✅ ৳'+d.reward+' যোগ'); load();} else alert(d.msg);});}).catch(()=>{show_11764581('pop').then(()=>{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ if(d.ok) load();});});});}
function doTask(id,link){ window.open(link,'_blank'); fetch(`/api/do_task?id=${uid}&task_id=${id}`,{method:'POST'}).then(r=>r.json()).then(d=>{alert(d.msg); load();});}
function withdraw(){let n=document.getElementById('num').value; let a=document.getElementById('amt').value; if(!n||!a) return alert('দিন'); fetch(`/api/withdraw?id=${uid}&number=${n}&amount=${a}`,{method:'POST'}).then(r=>r.json()).then(d=>{alert(d.msg); load();});}
function go(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on')); document.getElementById('t-'+t).classList.add('on'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); document.getElementById('b-'+t).classList.add('on');}
if(ref && ref!=uid){fetch(`/api/refer?new_id=${uid}&ref_id=${ref}`,{method:'POST'});}
load(); tg.onEvent('themeChanged', applyTheme); applyTheme(); tg.ready(); tg.expand();
show_11764581({type:'inApp',inAppSettings:{frequency:2,capping:0.1,interval:30,timeout:5,everyPage:false}});
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>FINAL ADMIN</title>
<style>body{font-family:Arial;background:#0f172a;color:#fff;margin:0;padding:10px}.nav{display:flex;gap:5px;flex-wrap:wrap;margin:10px 0}.nav button{padding:9px 12px;border:none;border-radius:8px;background:#1e293b;color:#fff;cursor:pointer;font-size:11px}.nav button.on{background:#1e40af} table{width:100%;background:#1e293b;border-collapse:collapse;margin-top:8px} th,td{padding:6px;border:1px solid #334155;font-size:11px;text-align:center} th{background:#1e40af} input{padding:6px;border-radius:6px;border:none;margin:2px}.g{background:#10b981;color:#fff;padding:6px 10px;border:none;border-radius:6px;cursor:pointer}.r{background:#ef4444;color:#fff;padding:6px 10px;border:none;border-radius:6px;cursor:pointer}.b{background:#3b82f6;color:#fff;padding:6px 10px;border:none;border-radius:6px;cursor:pointer}.card{background:#1e293b;padding:12px;border-radius:12px;margin:8px 0}.tab{display:none}.tab.on{display:block} img.thumb{width:80px;height:45px;object-fit:cover;border-radius:6px}</style>
</head><body>
<h2>👑 EVERYTHING FINAL ADMIN - 8807178385</h2>
<p>Theme Dark/Light Auto ✅ | Slider 3.5s ✅ | Logo Edit ✅ | Monetag 11764581 ✅</p>
<div class="nav"><button onclick="show('dash')" id="n-dash" class="on">Dashboard</button><button onclick="show('users')" id="n-users">Users</button><button onclick="show('slider')" id="n-slider">Slider Image 3-4s</button><button onclick="show('tasks')" id="n-tasks">Tasks</button><button onclick="show('ads')" id="n-ads">Company Ads</button><button onclick="show('wd')" id="n-wd">Withdraw</button><button onclick="show('set')" id="n-set">Logo + App Edit</button><button onclick="show('broad')" id="n-broad">Broadcast</button></div>

<div id="t-dash" class="tab on"><div class="card"><p>Users: <b id="tu">0</b> | Balance: ৳<b id="tb">0</b> | Ads: <b id="ta">0</b> | Refer: <b id="tr">0</b> | WD: <b id="pw">0</b></p></div></div>
<div id="t-users" class="tab"><input id="search" placeholder="Search ID" onkeyup="loadUsers()"><table><thead><tr><th>ID</th><th>Bal</th><th>Ads</th><th>Ref By</th><th>Tasks</th><th>Action</th></tr></thead><tbody id="users"></tbody></table></div>
<div id="t-slider" class="tab"><div class="card"><h3>🖼️ কোম্পানি বিজ্ঞাপন ছবি - 3-4 সেকেন্ড পর পর পাল্টাবে</h3><input id="sl_img" placeholder="Image URL https://..." style="width:320px"><input id="sl_link" placeholder="Link https://..." style="width:200px"><button class="g" onclick="addSlider()">Add</button><p style="font-size:11px;color:#94a3b8">Direct Image Link দাও, 3.5s পর পর অটো Slider হবে। ইউজার ক্লিক করলে Link এ যাবে - কোম্পানি এড।</p></div><table><thead><tr><th>Image</th><th>Link</th><th>Del</th></tr></thead><tbody id="slt"></tbody></table></div>
<div id="t-tasks" class="tab"><div class="card"><input id="nt_title" placeholder="Title"><input id="nt_reward" type="number" placeholder="Reward"><input id="nt_link" placeholder="Link" style="width:200px"><button class="g" onclick="addTask()">Add Task</button></div><table><thead><tr><th>Title</th><th>Reward</th><th>Del</th></tr></thead><tbody id="taskt"></tbody></table></div>
<div id="t-ads" class="tab"><div class="card"><h3>🏢 Company Ads Control - Monetag</h3><p>Zone ID: <input id="s_zone"> App ID: <input id="s_app"> Reward: <input id="s_ad" type="number"> Daily Limit: <input id="s_lim" type="number"></p><button class="g" onclick="saveAds()">Save Ads</button></div></div>
<div id="t-wd" class="tab"><table><thead><tr><th>User</th><th>Number</th><th>Amt</th><th>Date</th><th>Action</th></tr></thead><tbody id="wdt"></tbody></table></div>
<div id="t-set" class="tab"><div class="card"><h3>🎨 Logo + Company Edit - Everything</h3><p>App Name: <input id="s_name" style="width:140px"> Company: <input id="s_comp" style="width:140px"> Logo URL: <input id="s_logo" style="width:260px"></p><p>Banner Color: <input id="s_banner" type="color"> Min WD: <input id="s_min" type="number"> Ref Bonus: <input id="s_ref" type="number"></p><p>Admin Msg: <input id="s_admin" style="width:300px"></p><p>How Work: <input id="s_how" style="width:400px"></p><button class="g" onclick="saveSet()">Save Everything</button></div></div>
<div id="t-broad" class="tab"><div class="card"><h3>📢 Broadcast - সব ইউজারকে মেসেজ</h3><input id="broad_msg" placeholder="Message লিখুন..." style="width:300px"><button class="g" onclick="sendBroad()">Send to All</button><p style="font-size:11px">Bot থেকেও /broadcast লিখে পাঠাতে পারবেন</p></div></div>
<script>
function show(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('on'));document.getElementById('n-'+t).classList.add('on'); if(t=='users') loadUsers(); if(t=='slider') loadSlider(); if(t=='tasks') loadTasks(); if(t=='wd') loadWD(); if(t=='dash') loadDash(); if(t=='set') loadSet(); if(t=='ads') loadAds();}
function loadDash(){fetch('/api/admin_stats?admin=8807178385').then(r=>r.json()).then(d=>{document.getElementById('tu').innerText=d.total_users; document.getElementById('tb').innerText=d.total_balance; document.getElementById('ta').innerText=d.total_ads; document.getElementById('tr').innerText=d.total_ref; document.getElementById('pw').innerText=d.pending_wd;});}
function loadUsers(){let s=document.getElementById('search').value.toLowerCase(); fetch('/api/all_users').then(r=>r.json()).then(data=>{let h='';for(let id in data){if(s &&!id.includes(s)) continue; let u=data[id]; h+=`<tr><td>${id}</td><td>৳${u.balance}</td><td>${u.ads_watched||0}</td><td>${u.referred_by||'-'}</td><td>${(u.tasks_done||[]).length}</td><td><input id="b_${id}" value="${u.balance}" style="width:45px"><button class="b" onclick="upd('${id}')">Upd</button><button class="g" onclick="add('${id}',10)">+10</button><button class="r" onclick="add('${id}',-10)">-10</button></td></tr>`;}document.getElementById('users').innerHTML=h;});}
function loadSlider(){fetch('/api/get_slider').then(r=>r.json()).then(arr=>{let h='';arr.forEach((it,i)=>{h+=`<tr><td><img class="thumb" src="${it.img}"><br>${it.img.substring(0,25)}...</td><td>${it.link.substring(0,20)}</td><td><button class="r" onclick="delSlider(${i})">Del</button></td></tr>`;});document.getElementById('slt').innerHTML=h;});}
function loadTasks(){fetch('/api/get_tasks').then(r=>r.json()).then(arr=>{let h='';arr.forEach(t=>{h+=`<tr><td>${t.title}</td><td>৳${t.reward}</td><td><button class="r" onclick="delTask(${t.id})">Del</button></td></tr>`;});document.getElementById('taskt').innerHTML=h;});}
function loadWD(){fetch('/api/wd_list?admin=8807178385').then(r=>r.json()).then(l=>{let h='';l.forEach((w,i)=>{h+=`<tr><td>${w.user_id}</td><td>${w.number}</td><td>৳${w.amount}</td><td>${w.date}</td><td><button class="g" onclick="apWD(${i})">Approve</button><button class="r" onclick="rjWD(${i})">Reject</button></td></tr>`});document.getElementById('wdt').innerHTML=h;});}
function loadSet(){fetch('/api/get_settings').then(r=>r.json()).then(s=>{document.getElementById('s_name').value=s.app_name; document.getElementById('s_comp').value=s.company_name; document.getElementById('s_logo').value=s.logo_url; document.getElementById('s_banner').value=s.banner_color; document.getElementById('s_min').value=s.min_withdraw; document.getElementById('s_ref').value=s.ref_bonus; document.getElementById('s_admin').value=s.admin_msg; document.getElementById('s_how').value=s.how_to_work;});}
function loadAds(){fetch('/api/get_settings').then(r=>r.json()).then(s=>{document.getElementById('s_zone').value=s.ad_zone; document.getElementById('s_app').value=s.app_id; document.getElementById('s_ad').value=s.ad_reward; document.getElementById('s_lim').value=s.ad_daily_limit;});}
function upd(id){let v=document.getElementById('b_'+id).value; fetch(`/api/admin_update?id=${id}&balance=${v}&admin=8807178385`).then(()=>loadUsers());}
function add(id,a){fetch(`/api/admin_add?id=${id}&amount=${a}&admin=8807178385`).then(()=>loadUsers());}
function apWD(i){fetch(`/api/wd_approve?index=${i}&admin=8807178385`).then(()=>loadWD());}
function rjWD(i){fetch(`/api/wd_reject?index=${i}&admin=8807178385`).then(()=>loadWD());}
function addSlider(){let d={img:document.getElementById('sl_img').value, link:document.getElementById('sl_link').value, admin:'8807178385'}; if(!d.img) return alert('Image URL দিন'); fetch('/api/add_slider',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>{alert('Added'); loadSlider();});}
function delSlider(i){fetch(`/api/del_slider?index=${i}&admin=8807178385`).then(()=>loadSlider());}
function addTask(){let d={title:document.getElementById('nt_title').value, reward:document.getElementById('nt_reward').value, link:document.getElementById('nt_link').value, admin:'8807178385'}; fetch('/api/add_task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>loadTasks());}
function delTask(id){fetch(`/api/del_task?id=${id}&admin=8807178385`).then(()=>loadTasks());}
function saveSet(){let d={app_name:document.getElementById('s_name').value, company_name:document.getElementById('s_comp').value, logo_url:document.getElementById('s_logo').value, banner_color:document.getElementById('s_banner').value, min_withdraw:document.getElementById('s_min').value, ref_bonus:document.getElementById('s_ref').value, admin_msg:document.getElementById('s_admin').value, how_to_work:document.getElementById('s_how').value, admin:'8807178385'}; fetch('/api/save_app',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>alert('Saved Everything')); }
function saveAds(){let d={ad_zone:document.getElementById('s_zone').value, app_id:document.getElementById('s_app').value, ad_reward:document.getElementById('s_ad').value, ad_daily_limit:document.getElementById('s_lim').value, admin:'8807178385'}; fetch('/api/save_ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>alert('Saved')); }
function sendBroad(){let msg=document.getElementById('broad_msg').value; if(!msg) return alert('Message লিখুন'); fetch(`/api/broadcast?msg=${encodeURIComponent(msg)}&admin=8807178385`).then(r=>r.json()).then(d=>alert(d.msg));}
loadDash();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_panel():
    if str(request.args.get('id'))!=str(ADMIN_ID): return "Not Authorized 8807178385 only",403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id')
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None,"tasks_done":[],"name":"User"}
    return jsonify({"user":db["users"][uid],"settings":db["settings"],"tasks":db["tasks"],"slider":db["slider"]})
@app.route('/api/get_slider')
def get_slider(): return jsonify(db["slider"])
@app.route('/api/get_tasks')
def get_tasks(): return jsonify(db["tasks"])
@app.route('/api/get_settings')
def get_settings(): return jsonify(db["settings"])
@app.route('/api/all_users')
def all_users(): return jsonify(db["users"])
@app.route('/api/reward')
def reward():
    uid=request.args.get('id')
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None,"tasks_done":[]}
    if db["users"][uid].get("ads_watched",0)>=int(db["settings"]["ad_daily_limit"]): return jsonify({"ok":False,"msg":f"Daily limit {db['settings']['ad_daily_limit']}"})
    db["users"][uid]["balance"]+=int(db["settings"]["ad_reward"]); db["users"][uid]["ads_watched"]+=1; save_db(db)
    return jsonify({"ok":True,"reward":db["settings"]["ad_reward"]})
@app.route('/api/do_task', methods=['POST'])
def do_task():
    uid=request.args.get('id'); task_id=int(request.args.get('task_id'))
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None,"tasks_done":[]}
    if task_id in db["users"][uid].get("tasks_done",[]): return jsonify({"ok":False,"msg":"Already done"})
    t=next((x for x in db["tasks"] if x["id"]==task_id),None)
    if not t: return jsonify({"ok":False,"msg":"Not found"})
    db["users"][uid]["balance"]+=int(t["reward"]); db["users"][uid]["tasks_done"].append(task_id); save_db(db)
    return jsonify({"ok":True,"msg":f"✅ ৳{t['reward']} যোগ হয়েছে"})
@app.route('/api/refer', methods=['POST'])
def refer():
    new_id=request.args.get('new_id'); ref_id=request.args.get('ref_id')
    if new_id not in db["users"]: db["users"][new_id]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None,"tasks_done":[]}
    if db["users"][new_id].get("referred_by"): return jsonify({"ok":False})
    if ref_id not in db["users"]: db["users"][ref_id]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None,"tasks_done":[]}
    if new_id==ref_id: return jsonify({"ok":False})
    db["users"][new_id]["referred_by"]=ref_id; db["users"][ref_id]["referrals"].append(new_id); db["users"][ref_id]["balance"]+=int(db["settings"]["ref_bonus"]); save_db(db); return jsonify({"ok":True})
@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    uid=request.args.get('id'); number=request.args.get('number'); amount=int(request.args.get('amount',0))
    if db["users"][uid]["balance"]<amount: return jsonify({"msg":"Balance কম"})
    if amount<int(db["settings"]["min_withdraw"]): return jsonify({"msg":f"Min {db['settings']['min_withdraw']} লাগবে"})
    db["users"][uid]["balance"]-=amount; db["withdraws"].append({"user_id":uid,"number":number,"amount":amount,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}); save_db(db); return jsonify({"msg":"✅ Request গেছে"})
@app.route('/api/wd_list')
def wd_list():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    return jsonify(db["withdraws"])
@app.route('/api/wd_approve')
def wd_approve():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    idx=int(request.args.get('index')); db["withdraws"].pop(idx); save_db(db); return jsonify({"ok":True})
@app.route('/api/wd_reject')
def wd_reject():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    idx=int(request.args.get('index')); w=db["withdraws"][idx]; db["users"][w["user_id"]]["balance"]+=w["amount"]; db["withdraws"].pop(idx); save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_update')
def admin_update():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); bal=int(request.args.get('balance')); db["users"][uid]["balance"]=bal; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_add')
def admin_add():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); amt=int(request.args.get('amount')); db["users"][uid]["balance"]+=amt; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_stats')
def admin_stats():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    return jsonify({"total_users":len(db["users"]),"total_balance":sum([u["balance"] for u in db["users"].values()]),"total_ads":sum([u.get("ads_watched",0) for u in db["users"].values()]),"total_ref":sum([len(u.get("referrals",[])) for u in db["users"].values()]),"pending_wd":len(db["withdraws"])})
@app.route('/api/add_slider', methods=['POST'])
def add_slider():
    d=request.json;
    if str(d.get('admin'))!=str(ADMIN_ID): return "No",403
    db["slider"].append({"img":d["img"],"link":d["link"]}); save_db(db); return jsonify({"ok":True})
@app.route('/api/del_slider')
def del_slider():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    idx=int(request.args.get('index')); db["slider"].pop(idx); save_db(db); return jsonify({"ok":True})
@app.route('/api/add_task', methods=['POST'])
def add_task():
    d=request.json;
    if str(d.get('admin'))!=str(ADMIN_ID): return "No",403
    nid=max([t["id"] for t in db["tasks"]], default=0)+1; db["tasks"].append({"id":nid,"title":d["title"],"reward":int(d["reward"]),"link":d["link"],"color":"#1e40af","btn":"শুরু করুন"}); save_db(db); return jsonify({"ok":True})
@app.route('/api/del_task')
def del_task():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    tid=int(request.args.get('id')); db["tasks"]=[t for t in db["tasks"] if t["id"]!=tid]; save_db(db); return jsonify({"ok":True})
@app.route('/api/save_app', methods=['POST'])
def save_app():
    d=request.json;
    if str(d.get('admin'))!=str(ADMIN_ID): return "No",403
    db["settings"]["app_name"]=d["app_name"]; db["settings"]["company_name"]=d["company_name"]; db["settings"]["logo_url"]=d["logo_url"]; db["settings"]["banner_color"]=d["banner_color"]; db["settings"]["min_withdraw"]=int(d["min_withdraw"]); db["settings"]["ref_bonus"]=int(d["ref_bonus"]); db["settings"]["admin_msg"]=d["admin_msg"]; db["settings"]["how_to_work"]=d["how_to_work"]; save_db(db); return jsonify({"ok":True})
@app.route('/api/save_ads', methods=['POST'])
def save_ads():
    d=request.json;
    if str(d.get('admin'))!=str(ADMIN_ID): return "No",403
    db["settings"]["ad_zone"]=d["ad_zone"]; db["settings"]["app_id"]=d["app_id"]; db["settings"]["ad_reward"]=int(d["ad_reward"]); db["settings"]["ad_daily_limit"]=int(d["ad_daily_limit"]); save_db(db); return jsonify({"ok":True})
@app.route('/api/broadcast')
def broadcast_api():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    msg=request.args.get('msg'); return jsonify({"msg":f"✅ Broadcast Ready: {msg} - Bot এ /broadcast দিয়ে পাঠান"})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id)
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None,"tasks_done":[],"name":update.effective_user.first_name}
    if context.args and context.args[0]!=uid:
        ref_id=context.args[0]
        if not db["users"][uid].get("referred_by") and ref_id in db["users"]:
            db["users"][uid]["referred_by"]=ref_id; db["users"][ref_id]["referrals"].append(uid); db["users"][ref_id]["balance"]+=int(db["settings"]["ref_bonus"])
    save_db(db)
    kb=[[InlineKeyboardButton("💰 Open Earning App", web_app={"url": f"https://am-bot-1-v77g.onrender.com/?id={uid}"})]]
    if str(uid)==str(ADMIN_ID): kb.append([InlineKeyboardButton("👑 FINAL ADMIN", url=f"https://am-bot-1-v77g.onrender.com/admin?id={uid}")])
    await update.message.reply_text(f"Welcome to {db['settings']['app_name']} ✅\nID: {uid}\nBalance: ৳{db['users'][uid]['balance']}\nRefer: https://t.me/ProtidinerKaj_BD_Bot?start={uid}", reply_markup=InlineKeyboardMarkup(kb))

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id)!=str(ADMIN_ID): return
    msg=" ".join(context.args)
    if not msg: await update.message.reply_text("Usage: /broadcast Your Message"); return
    count=0
    for uid in list(db["users"].keys()):
        try: await context.bot.send_message(chat_id=int(uid), text=f"📢 {msg}"); count+=1
        except: pass
    await update.message.reply_text(f"✅ Sent to {count} users")

def run_bot():
    try:
        application=Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("broadcast", broadcast_cmd))
        application.run_polling()
    except Exception as e: print(e)
def start_bot_thread(): threading.Thread(target=run_bot, daemon=True).start()
start_bot_thread()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
