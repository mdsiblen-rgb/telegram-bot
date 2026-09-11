import os, json, threading, datetime, time, requests
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db_final_400_lines.json"
SELF_URL = "https://am-bot-1-v77g.onrender.com"
app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [], "refer_logs": [],
            "slider": [
                {"img": "https://img.freepik.com/free-vector/flat-design-earn-money-banner_23-2149439772.jpg", "link": "https://t.me/ProtidinerKajBD", "title": "🔥 প্রতিদিনের কাজ BD - Official"},
                {"img": "https://img.freepik.com/free-vector/gradient-refer-friend-banner_23-2149373488.jpg", "link": "https://t.me/ProtidinerKajBD", "title": "💰 Refer করে ৳50 বোনাস জিতুন"},
                {"img": "https://img.freepik.com/free-vector/flat-design-affiliate-marketing-banner_23-2149443391.jpg", "link": "https://youtube.com/@ProtidinerKajBD", "title": "▶️ YouTube Subscribe করুন - ৳25"}
            ],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD",
                "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "banner_color": "#1e40af", "bg_color": "#eef2ff", "card_bg": "#ffffff",
                "balance_c1": "#1e3a8a", "balance_c2": "#3b82f6",
                "ad_btn": "#1e40af", "wd_btn": "#1e40af", "checkin_btn": "#f59e0b",
                "ad_zone": "11764581", "ad_reward": 1, "ad_daily_limit": 100, "ad_timer": 30,
                "ref_bonus": 50, "min_withdraw": 1000, "welcome_bonus": 30, "daily_bonus": 10,
                "home_notice": "🔥 আজ রাত 8টায় 5000 টাকা Giveaway! সবাই Active থাকুন - Admin"
            },
            "tasks": [
                {"id": 1, "title": "YouTube ভিডিও দেখুন - 1 মিনিট", "reward": 25, "link": "https://youtube.com/@ProtidinerKajBD", "color": "#065f46", "btn": "শুরু করুন"},
                {"id": 2, "title": "Telegram Channel Join করুন", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join করুন"},
                {"id": 3, "title": "Facebook Page Follow করুন", "reward": 15, "link": "https://www.facebook.com/share/1AXw16vWRj/", "color": "#1877F2", "btn": "Follow করুন"}
            ]
        }
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(f, d, indent=2)

# === ANTI SLEEP SYSTEM ===
def keep_alive():
    while True:
        try:
            time.sleep(240)
            requests.get(f"{SELF_URL}/health", timeout=10)
            requests.get(f"{SELF_URL}/ping", timeout=10)
            print("✅ Self Ping OK - Bot জেগে আছে")
        except: pass
threading.Thread(target=keep_alive, daemon=True).start()

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{max-width:430px;margin:0 auto;font-family:Arial;padding-bottom:90px}
.top{color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
.top img{width:36px;height:36px;border-radius:50%;background:#fff;padding:2px}
.bal-card{margin:12px;color:#fff;padding:18px;border-radius:20px;text-align:center}
.bal-big{font-size:48px;font-weight:900;margin:10px 0}.bal-mini{display:flex;gap:10px;margin-top:12px}
.bal-mini div{flex:1;background:rgba(255,255,255,.2);padding:10px;border-radius:12px;font-size:13px}
.card{margin:12px;padding:14px;border-radius:18px;box-shadow:0 4px 12px rgba(0,0,0,.06)}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:bold;cursor:pointer;margin-top:8px;color:#fff}
.tab{display:none}.tab.on{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;display:flex;justify-content:space-around;background:#fff;padding:10px 0;border-top:1px solid #ddd;z-index:99}
.btm div{flex:1;text-align:center;font-size:12px;color:#888;cursor:pointer}.btm div.on{color:#1e40af;font-weight:bold}
.slider{position:relative;width:calc(100% - 24px);margin:12px;height:165px;overflow:hidden;border-radius:18px;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.1)}
.slide{position:absolute;inset:0;opacity:0;transition:opacity.8s;cursor:pointer}.slide.active{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover}
.slide-title{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.7));color:#fff;padding:25px 12px 10px;font-weight:bold;font-size:13px}
.dots{text-align:center;margin-top:4px}.dot{height:7px;width:7px;background:#bbb;border-radius:50%;display:inline-block;margin:0 3px}.dot.active{background:#1e40af}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:8px;box-sizing:border-box}
.meth{flex:1;background:#fff;border-radius:14px;padding:12px 6px;text-align:center;cursor:pointer;border:2px solid #ddd;transition:.2s;position:relative}
.meth.sel{border-width:3px!important;transform:scale(1.03);box-shadow:0 4px 12px rgba(0,0,0,.15)}
.meth.sel:after{content:'✓';position:absolute;top:4px;right:6px;background:#1e40af;color:#fff;width:18px;height:18px;border-radius:50%;font-size:12px;line-height:18px}
.task-item{display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid #eee;border-radius:12px;margin:8px 0}
.wd-info{background:#f8fafc;padding:10px;border-radius:10px;margin:10px 0;font-size:12px;text-align:center;border:1px solid #e2e8f0}
</style></head><body id="body">
<div class="top" id="topBar"><div style="display:flex;align-items:center;gap:8px"><img id="appLogo" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"><span id="appName">প্রতিদিনের কাজ BD</span></div><span>৳<span id="bTop">0</span></span></div>

<div id="t-home" class="tab on">
<div class="slider" id="sliderBox"></div><div class="dots" id="dotsBox"></div>
<div class="bal-card" id="balCard"><p>আপনার ব্যালেন্স</p><div class="bal-big">৳<span id="bal">0</span></div>
<div class="bal-mini"><div>আজ দেখেছেন<br><b><span id="adWatched">0</span>/100</b></div><div>Refer বোনাস<br><b>৳<span id="refBonus">50</span></b></div></div>
<button class="btn" id="earnBtn" style="background:#fff;margin-top:14px" onclick="go('earn')">💰 এখনই আয় করুন</button></div>
<div class="card" id="dailyCard"><div style="display:flex;justify-content:space-between;align-items:center"><div><b>🎁 Daily Check-in</b><br><small>প্রতিদিন ৳<span id="dailyR">10</span> বোনাস</small></div><button class="btn" id="checkinBtn" style="width:auto;padding:10px 18px" onclick="dailyCheck()">বোনাস নিন</button></div></div>
<div class="card" id="homeNoticeBox" style="background:linear-gradient(135deg,#fef3c7,#fde68a);border:2px dashed #f59e0b;display:none"><h4 style="margin:0;color:#92400e">📢 অ্যাডমিন নোটিশ</h4><p id="homeNoticeText" style="margin:8px 0 0;font-weight:bold;color:#78350f;line-height:1.6"></p></div>
<div class="card" id="trustCard"><div style="display:flex;gap:10px;align-items:center"><div style="background:#dcfce7;padding:10px;border-radius:10px">✅</div><div><b>Protidiner Kaj BD Trusted</b><br><small>5000+ User Payment পেয়েছে</small></div></div></div>
<div class="card" style="background:#f0fdf4;text-align:center"><b>🔥 আজ 127 জন Withdraw করেছে - Live</b></div>
</div>

<div id="t-earn" class="tab">
<div class="card"><h3>📺 কোম্পানি বিজ্ঞাপন - Zone 11764581</h3><p>প্রতি Ads ৳<span id="adR">1</span> | Timer 30s | Daily Limit 100</p>
<div style="font-size:40px;text-align:center;font-weight:900;color:#1e40af">৳<span id="adR2">1</span></div>
<button class="btn" id="adBtn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button>
<p style="font-size:11px;color:green;margin-top:6px">✅ Telegram App থেকে Open করলে 100% Ad আসবে - Zone 11764581 OK</p>
<p style="font-size:11px">Watched Today: <span id="adWatched2">0</span> / <span id="adLimit">100</span></p></div>
<div id="taskList" class="card"><h3>📋 অন্যান্য কাজ - কোম্পানির সাথে যুক্ত</h3><div id="tasksContainer"></div></div>
<div class="card"><p>👥 Refer করে আয় - প্রতি Refer ৳<span id="refR">50</span></p><p style="font-size:11px;color:#666">আপনার Refer Link:</p>
<p id="refLink" style="font-size:11px;background:#f1f5f9;padding:10px;border-radius:8px;word-break:break-all;border:1px dashed #aaa"></p>
<button class="btn" style="background:#10b981" onclick="navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ Copied!')">Copy Refer Link</button></div>
</div>

<div id="t-support" class="tab">
<div class="card"><h3>🎧 সাপোর্ট সেন্টার - কোম্পানি লিংক</h3>
<button class="btn" style="background:#1e40af" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">📢 অফিশিয়াল চ্যানেল Join</button>
<button class="btn" style="background:#FF0000" onclick="window.open('https://youtube.com/@ProtidinerKajBD','_blank')">▶️ YouTube Channel Subscribe</button>
<button class="btn" style="background:#1877F2" onclick="window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank')">📘 Facebook Page Follow</button>
<button class="btn" style="background:#10b981" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">💬 Admin এর সাথে Chat</button></div>
<div class="card"><h4>❓ FAQ</h4><p style="font-size:12px;line-height:1.6">Q: Ad আসে না কেন?<br>A: Telegram App থেকে Open করুন, Zone 11764581 Active।<br><br>Q: Payment কখন?<br>A: প্রতিদিন রাত 8PM - 10PM</p></div>
</div>

<div id="t-withdraw" class="tab">
<div class="card">
<h3>💳 উইথড্র - বিকাশ নগদ সিস্টেম</h3>
<div style="font-size:36px;text-align:center;font-weight:900">৳<span class="bal2">0</span></div>
<div class="wd-info"><span id="wdMsg">সর্বনিম্ন উইথড্র ৳1000 - আপনার আর <b id="needAmt">245</b> টাকা লাগবে</span></div>
</div>

<div class="card">
<h4>💳 পেমেন্ট মেথড - বিকাশ + নগদ - অরিজিনাল লোগো ✅ FINAL</h4>
<div style="display:flex;gap:12px">
<div onclick="selectMethod('bKash')" id="m-bKash" class="meth sel" style="border-color:#e11d48">
<img src="https://upload.wikimedia.org/wikipedia/commons/b/bd/BKash_Logo.png" style="height:34px;width:auto;display:block;margin:0 auto;object-fit:contain" onerror="this.src='https://i.ibb.co/5T6g6yq/bkash.png'">
<div style="font-weight:bold;color:#e11d48;margin-top:8px;font-size:14px">bKash</div><div style="font-size:10px;color:#666">Personal</div>
</div>
<div onclick="selectMethod('Nagad')" id="m-Nagad" class="meth" style="border-color:#f59e0b">
<img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Nagad_Logo.png" style="height:34px;width:auto;display:block;margin:0 auto;object-fit:contain" onerror="this.src='https://i.ibb.co/1v9k9Zq/nagad.png'">
<div style="font-weight:bold;color:#e11d48;margin-top:8px;font-size:14px">Nagad</div><div style="font-size:10px;color:#666">Personal</div>
</div>
</div>
<p style="font-size:11px;margin-top:12px;line-height:1.6">⏰ পেমেন্ট টাইম: প্রতিদিন রাত 8PM - 10PM<br>📋 নিয়ম: 1. ভুল Number দিবেন না 2. Min ৳1000 হলে Withdraw</p>
<input type="hidden" id="selectedMethod" value="bKash">
<input id="wNum" placeholder="bKash Personal Number">
<input id="wAmt" type="number" placeholder="Amount - Min 1000">
<button class="btn" id="wdBtn" onclick="doWithdraw()">উইথড্র রিকোয়েস্ট করুন</button>
</div>

<div class="card"><h4>📜 আমার Withdraw History</h4><div id="wdHistory"><p style="font-size:11px;color:#888">কোনো History নেই</p></div></div>
</div>

<div class="btm" id="btmBar"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>

<script>
const tg=Telegram.WebApp;let qp=new URLSearchParams(location.search);let uid=qp.get('id')||tg.initDataUnsafe?.user?.id||"8807178385";
let curSlide=0,slideInt,curMeth='bKash';
function go(t){document.querySelectorAll('.tab').forEach(e=>e.classList.remove('on'));document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));document.getElementById('b-'+t).classList.add('on');}
function selectMethod(m){curMeth=m;document.getElementById('selectedMethod').value=m;document.querySelectorAll('.meth').forEach(e=>{e.classList.remove('sel');e.style.borderWidth='2px';e.style.transform='scale(1)';e.style.boxShadow='none';});let el=document.getElementById('m-'+m);el.classList.add('sel');el.style.borderWidth='3px';el.style.transform='scale(1.03)';el.style.boxShadow='0 4px 12px rgba(0,0,0,.15)';document.getElementById('wNum').placeholder=m+' Personal Number';}
function initSlider(imgs){let box=document.getElementById('sliderBox');let dots=document.getElementById('dotsBox');if(!imgs||!imgs.length){box.innerHTML='<div style="padding:40px;text-align:center;color:#888">No Ad</div>';return;}box.innerHTML='';dots.innerHTML='';imgs.forEach((it,i)=>{let d=document.createElement('div');d.className='slide'+(i==0?' active':'');d.innerHTML=`<img src="${it.img}" onerror="this.src='https://via.placeholder.com/400x200?text=Ad'"><div class="slide-title">${it.title||''}</div>`;d.onclick=()=>window.open(it.link,'_blank');box.appendChild(d);let dot=document.createElement('span');dot.className='dot'+(i==0?' active':'');dots.appendChild(dot);});if(slideInt)clearInterval(slideInt);slideInt=setInterval(()=>{let s=document.querySelectorAll('.slide');let ds=document.querySelectorAll('.dot');if(!s.length)return;s[curSlide].classList.remove('active');ds[curSlide].classList.remove('active');curSlide=(curSlide+1)%s.length;s[curSlide].classList.add('active');ds[curSlide].classList.add('active');},3500);}
function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{if(d.banned){document.body.innerHTML="<h2 style='text-align:center;margin-top:50px'>⛔ Banned</h2>";return;}document.getElementById('bal').innerText=d.user.balance;document.getElementById('bTop').innerText=d.user.balance;document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance);document.getElementById('adWatched').innerText=d.user.ads_watched||0;document.getElementById('adWatched2').innerText=d.user.ads_watched||0;let s=d.settings;document.getElementById('appName').innerText=s.app_name;document.getElementById('appLogo').src=s.logo_url;document.getElementById('body').style.background=s.bg_color;document.getElementById('topBar').style.background=s.banner_color;document.getElementById('balCard').style.background=`linear-gradient(135deg,${s.balance_c1},${s.balance_c2})`;document.getElementById('adBtn').style.background=s.ad_btn;document.getElementById('wdBtn').style.background=s.wd_btn;document.getElementById('checkinBtn').style.background=s.checkin_btn;document.getElementById('earnBtn').style.color=s.ad_btn;document.querySelectorAll('.card').forEach(c=>{if(c.id!='homeNoticeBox')c.style.background=s.card_bg;});document.getElementById('adR').innerText=s.ad_reward;document.getElementById('adR2').innerText=s.ad_reward;document.getElementById('adLimit').innerText=s.ad_daily_limit;document.getElementById('refBonus').innerText=s.ref_bonus;document.getElementById('refR').innerText=s.ref_bonus;document.getElementById('dailyR').innerText=s.daily_bonus;document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;if(s.home_notice){document.getElementById('homeNoticeBox').style.display='block';document.getElementById('homeNoticeText').innerText=s.home_notice;}let need=Math.max(0,s.min_withdraw-d.user.balance);document.getElementById('needAmt').innerText=need;if(d.user.balance>=s.min_withdraw)document.getElementById('wdMsg').innerHTML=`✅ আপনি <b>${s.min_withdraw} টাকা</b> Withdraw করতে পারবেন`;initSlider(d.slider);let tc=document.getElementById('tasksContainer');tc.innerHTML='';if(d.tasks){d.tasks.forEach(t=>{tc.innerHTML+=`<div class="task-item"><div><b>${t.title}</b><br><small>৳${t.reward}</small></div><button class="btn" style="width:auto;background:${t.color};padding:8px 14px" onclick="window.open('${t.link}','_blank')">${t.btn}</button></div>`;});}});}
function watchAd(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{alert('✅ ৳'+d.reward+' যোগ হলো');load();});});}else{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{alert('Test ৳'+d.reward+' | Telegram App এ Real Ad আসবে');load();});}}
function doWithdraw(){let n=document.getElementById('wNum').value;let a=document.getElementById('wAmt').value;if(!n||!a)return alert('Number & Amount দাও');fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}&method=${curMeth}`).then(r=>r.json()).then(d=>alert(d.msg));}
function dailyCheck(){fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(d=>{alert(d.msg);load();});}
load();
</script></body></html>
"""

ADMIN_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>FINAL ADMIN</title>
<style>body{max-width:700px;margin:0 auto;font-family:Arial;background:#f1f5f9;padding:12px}.card{background:#fff;padding:14px;border-radius:12px;margin:12px 0;box-shadow:0 2px 8px rgba(0,0,0,.06)}input{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:1px solid #ddd;box-sizing:border-box}input[type=color]{height:45px;padding:2px}.btn{width:100%;padding:12px;border:none;border-radius:8px;color:#fff;font-weight:bold;background:#1e40af;cursor:pointer;margin-top:6px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}table{width:100%;font-size:12px;border-collapse:collapse}th,td{border:1px solid #ddd;padding:6px;text-align:left}th{background:#f8fafc}</style></head><body>
<h2 style="text-align:center">🔥 FINAL ADMIN - 400+ Lines - Anti Sleep + bKash/Nagad</h2>
<div class="card" style="border:2px solid #22c55e;background:#f0fdf4"><h3>✅ Bot Status - ঘুমাবে না - Anti Sleep Active</h3><p style="font-size:13px;line-height:1.6">✅ Auto Self-Ping প্রতি 4 মিনিটে চলছে<br>✅ /health Endpoint OK<br>✅ Render Free Spin Down Delay Fix করা<br>⚠️ Render এ <b>My project Needs attention</b> লাল দেখালে: My Workspace > Projects > My project এর ভিতরে কোনো Service নাই তাই লাল। তুমি ওই Project Delete করে দাও, শুধু Ungrouped Services এ telegram-bot-1 Active থাকলেই হবে। এটা কোনো সমস্যা না।<br>🔥 100% চালু রাখতে UptimeRobot.com এ গিয়ে https://telegram-bot-1-v77g.onrender.com/health লিংক Add করো প্রতি 5 মিনিটে Ping</p></div>
<div class="card" style="border:2px solid #f59e0b;background:#fffbeb"><h3>🎨 সব রং + লোগো + নাম</h3><label>App Name</label><input id="app_name"><label>Logo URL</label><input id="logo_url"><label>Banner Color</label><input type="color" id="banner_color"><label>Background Color</label><input type="color" id="bg_color"><label>Card BG</label><input type="color" id="card_bg"><div class="grid"><div><label>Balance C1</label><input type="color" id="balance_c1"></div><div><label>Balance C2</label><input type="color" id="balance_c2"></div></div><div class="grid"><div><label>Ad Btn</label><input type="color" id="ad_btn"></div><div><label>Wd Btn</label><input type="color" id="wd_btn"></div></div><label>Checkin Btn</label><input type="color" id="checkin_btn"><label>Home Notice</label><input id="home_notice"><button class="btn" style="background:#f59e0b;color:#000" onclick="saveDesign()">💾 Save Design</button></div>
<div class="card" style="border:2px solid #10b981;background:#f0fdf4"><h3>💰 টাকা সেটিং</h3><div class="grid"><div><label>Welcome Bonus</label><input id="welcome_bonus" type="number"></div><div><label>Ad Reward</label><input id="ad_reward" type="number"></div><div><label>Refer Bonus</label><input id="ref_bonus" type="number"></div><div><label>Min Withdraw</label><input id="min_withdraw" type="number"></div><div><label>Daily Bonus</label><input id="daily_bonus" type="number"></div><div><label>Ad Zone</label><input id="ad_zone"></div></div><button class="btn" style="background:#10b981" onclick="saveMoney()">💾 Save Money</button></div>
<div class="card"><h3>📊 Dashboard</h3><div id="stats" style="font-weight:bold;line-height:1.6"></div></div>
<div class="card"><h3>👥 User List</h3><table><thead><tr><th>ID</th><th>Bal</th><th>Ads</th><th>Ref</th></tr></thead><tbody id="userTable"></tbody></table></div>
<div class="card"><h3>💸 Withdraw - bKash/Nagad Only</h3><table><thead><tr><th>UID</th><th>Method</th><th>Num</th><th>Amt</th><th>Date</th></tr></thead><tbody id="wdTable"></tbody></table></div>
<div class="card"><h3>🎁 Refer Log</h3><table><thead><tr><th>Ref</th><th>New</th><th>Bonus</th><th>Date</th></tr></thead><tbody id="refTable"></tbody></table></div>
<div class="card"><h3>📢 Slider - 3.5s</h3><input id="sTitle" placeholder="Title"><input id="sImg" placeholder="Image URL"><input id="sLink" placeholder="Link"><button class="btn" onclick="addSlider()">+ Add Slider</button><div id="sliderList"></div></div>
<script>
let aid=new URLSearchParams(location.search).get('id')||'8807178385';
function loadAll(){fetch(`/api/pro_stats?id=${aid}`).then(r=>r.json()).then(d=>{document.getElementById('app_name').value=d.settings.app_name;document.getElementById('logo_url').value=d.settings.logo_url;document.getElementById('banner_color').value=d.settings.banner_color;document.getElementById('bg_color').value=d.settings.bg_color;document.getElementById('card_bg').value=d.settings.card_bg;document.getElementById('balance_c1').value=d.settings.balance_c1;document.getElementById('balance_c2').value=d.settings.balance_c2;document.getElementById('ad_btn').value=d.settings.ad_btn;document.getElementById('wd_btn').value=d.settings.wd_btn;document.getElementById('checkin_btn').value=d.settings.checkin_btn;document.getElementById('home_notice').value=d.settings.home_notice||'';document.getElementById('welcome_bonus').value=d.settings.welcome_bonus;document.getElementById('ad_reward').value=d.settings.ad_reward;document.getElementById('ref_bonus').value=d.settings.ref_bonus;document.getElementById('min_withdraw').value=d.settings.min_withdraw;document.getElementById('daily_bonus').value=d.settings.daily_bonus;document.getElementById('ad_zone').value=d.settings.ad_zone;document.getElementById('stats').innerHTML=`Users: ${d.total_users}<br>Balance: ৳${d.total_balance}<br>Withdraws: ${d.total_withdraws}<br>Today Join: ${d.today_join||0}`;let ut=document.getElementById('userTable');ut.innerHTML='';d.users.forEach(u=>{ut.innerHTML+=`<tr><td>${u.id}</td><td>৳${u.balance}</td><td>${u.ads}</td><td>${u.ref_count}</td></tr>`;});let wt=document.getElementById('wdTable');wt.innerHTML='';d.withdraws.forEach(w=>{wt.innerHTML+=`<tr><td>${w.uid}</td><td>${w.method}</td><td>${w.num}</td><td>৳${w.amt}</td><td>${(w.date||'').slice(0,16)}</td></tr>`;});let rt=document.getElementById('refTable');rt.innerHTML='';if(d.ref_logs){d.ref_logs.forEach(r=>{rt.innerHTML+=`<tr><td>${r.referrer}</td><td>${r.new_user}</td><td>৳${r.bonus}</td><td>${(r.date||'').slice(0,16)}</td></tr>`;});}let sl=document.getElementById('sliderList');sl.innerHTML='';d.slider.forEach((s,i)=>{sl.innerHTML+=`<div style="border:1px solid #ddd;padding:8px;margin:8px 0;border-radius:10px"><img src="${s.img}" style="width:100%;height:70px;object-fit:cover;border-radius:8px"><p style="font-weight:bold;margin:6px 0">${s.title}</p><button onclick="delS(${i})" style="background:#ef4444;color:#fff;border:none;padding:6px 12px;border-radius:6px;cursor:pointer">Delete</button></div>`;});});}
function saveDesign(){let q=new URLSearchParams({id:aid, app_name:document.getElementById('app_name').value, logo_url:document.getElementById('logo_url').value, banner_color:document.getElementById('banner_color').value, bg_color:document.getElementById('bg_color').value, card_bg:document.getElementById('card_bg').value, balance_c1:document.getElementById('balance_c1').value, balance_c2:document.getElementById('balance_c2').value, ad_btn:document.getElementById('ad_btn').value, wd_btn:document.getElementById('wd_btn').value, checkin_btn:document.getElementById('checkin_btn').value, home_notice:document.getElementById('home_notice').value});fetch(`/api/save_design?id=${aid}&`+q.toString()).then(r=>r.json()).then(d=>alert(d.msg));}
function saveMoney(){let q=new URLSearchParams({id:aid, welcome_bonus:document.getElementById('welcome_bonus').value, ad_reward:document.getElementById('ad_reward').value, ref_bonus:document.getElementById('ref_bonus').value, min_withdraw:document.getElementById('min_withdraw').value, daily_bonus:document.getElementById('daily_bonus').value, ad_zone:document.getElementById('ad_zone').value});fetch(`/api/save_money?id=${aid}&`+q.toString()).then(r=>r.json()).then(d=>alert(d.msg));}
function addSlider(){let img=document.getElementById('sImg').value;let link=document.getElementById('sLink').value;let title=document.getElementById('sTitle').value;if(!img)return alert('Image URL দাও');fetch(`/api/add_slider?id=${aid}&img=${encodeURIComponent(img)}&link=${encodeURIComponent(link)}&title=${encodeURIComponent(title)}`).then(r=>r.json()).then(d=>{alert(d.msg);loadAll();});}
function delS(i){fetch(`/api/del_slider?id=${aid}&idx=${i}`).then(r=>r.json()).then(d=>loadAll());}
loadAll();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)

@app.route('/admin')
def admin_page(): return render_template_string(ADMIN_HTML)

@app.route('/health')
def health(): return jsonify({"status":"ok","bot":"alive","time":str(datetime.datetime.now())}),200

@app.route('/ping')
def ping(): return jsonify({"pong":True}),200

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385'); ref=request.args.get('ref'); d=load_db()
    if uid not in d['users']:
        d['users'][uid]={'balance': d['settings']['welcome_bonus'], 'ads_watched':0, 'ref_count':0, 'last_daily':''}
        if ref and ref!=uid and ref in d['users']:
            d['users'][ref]['balance']=d['users'][ref].get('balance',0)+d['settings']['ref_bonus']
            d['users'][ref]['ref_count']=d['users'][ref].get('ref_count',0)+1
            d['refer_logs'].append({"referrer":ref,"new_user":uid,"bonus":d['settings']['ref_bonus'],"date":str(datetime.datetime.now())})
        save_db(d)
    return jsonify({"user":d['users'][uid],"settings":d['settings'],"slider":d['slider'],"tasks":d.get('tasks',[]),"banned":uid in d['banned']})

@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); d=load_db()
    if uid not in d['users']: d['users'][uid]={'balance':0,'ads_watched':0,'ref_count':0,'last_daily':''}
    d['users'][uid]['balance']+=d['settings']['ad_reward']; d['users'][uid]['ads_watched']=d['users'][uid].get('ads_watched',0)+1; save_db(d)
    return jsonify({"ok":True,"reward":d['settings']['ad_reward']})

@app.route('/api/daily')
def daily():
    uid=request.args.get('id'); d=load_db(); today=str(datetime.date.today())
    if d['users'][uid].get('last_daily')==today: return jsonify({"ok":False,"msg":"আজকের বোনাস নিয়েছো"})
    d['users'][uid]['balance']+=d['settings']['daily_bonus']; d['users'][uid]['last_daily']=today; save_db(d)
    return jsonify({"ok":True,"msg":f"✅ ৳{d['settings']['daily_bonus']} Daily Bonus!"})

@app.route('/api/withdraw')
def wd():
    uid=request.args.get('id'); num=request.args.get('num'); amt=int(request.args.get('amt') or 0); method=request.args.get('method','bKash'); d=load_db()
    if d['users'][uid]['balance']<amt: return jsonify({"ok":False,"msg":"Balance কম"})
    if amt<d['settings']['min_withdraw']: return jsonify({"ok":False,"msg":f"Min {d['settings']['min_withdraw']} টাকা"})
    d['users'][uid]['balance']-=amt; d['withdraws'].append({"uid":uid,"num":num,"amt":amt,"method":method,"date":str(datetime.datetime.now())}); save_db(d)
    return jsonify({"ok":True,"msg":f"✅ {method} - ৳{amt} Request OK!"})

@app.route('/api/pro_stats')
def pro_stats():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"error":"not admin"})
    d=load_db()
    users_list=[{"id":k,"balance":v.get('balance',0),"ads":v.get('ads_watched',0),"ref_count":v.get('ref_count',0)} for k,v in list(d['users'].items())[-100:]]
    return jsonify({"total_users":len(d['users']), "total_balance":sum([u.get('balance',0) for u in d['users'].values()]), "total_withdraws":len(d['withdraws']), "today_join":len([r for r in d.get('refer_logs',[]) if str(datetime.date.today()) in r.get('date','')]), "users":users_list[::-1], "withdraws":d['withdraws'][::-1][:100], "ref_logs":d.get('refer_logs',[])[::-1][:100], "slider":d['slider'], "settings":d['settings']})

@app.route('/api/save_design')
def save_design():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"ok":False})
    d=load_db(); s=d['settings']
    for k in ["app_name","logo_url","banner_color","bg_color","card_bg","balance_c1","balance_c2","ad_btn","wd_btn","checkin_btn","home_notice"]:
        if request.args.get(k): s[k]=request.args.get(k)
    save_db(d); return jsonify({"ok":True,"msg":"✅ Design Save!"})

@app.route('/api/save_money')
def save_money():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"ok":False})
    d=load_db(); s=d['settings']
    s['welcome_bonus']=int(request.args.get('welcome_bonus',s['welcome_bonus'])); s['ad_reward']=int(request.args.get('ad_reward',s['ad_reward'])); s['ref_bonus']=int(request.args.get('ref_bonus',s['ref_bonus'])); s['min_withdraw']=int(request.args.get('min_withdraw',s['min_withdraw'])); s['daily_bonus']=int(request.args.get('daily_bonus',s['daily_bonus'])); s['ad_zone']=request.args.get('ad_zone',s['ad_zone']); save_db(d); return jsonify({"ok":True,"msg":"✅ Money Save!"})

@app.route('/api/add_slider')
def add_slider():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"ok":False})
    d=load_db(); d['slider'].append({"img":request.args.get('img'),"link":request.args.get('link'),"title":request.args.get('title','')}); save_db(d); return jsonify({"ok":True,"msg":"✅ Slider Add - 3.5s"})

@app.route('/api/del_slider')
def del_slider():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"ok":False})
    d=load_db(); idx=int(request.args.get('idx') or 0)
    if 0<=idx<len(d['slider']): d['slider'].pop(idx); save_db(d)
    return jsonify({"ok":True})

def run_bot():
    async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
        uid=str(u.effective_user.id); d=load_db()
        if uid not in d['users']: d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'ref_count':0,'last_daily':''}; save_db(d)
        kb=[[InlineKeyboardButton("🚀 Open App - Zone 11764581", web_app={"url": f"{SELF_URL}/?id={uid}"})]]
        await u.message.reply_text(f"Welcome {u.effective_user.first_name} ✅\n🎁 {d['settings']['welcome_bonus']} Bonus!\nZone 11764581 Ready", reply_markup=InlineKeyboardMarkup(kb))
    async def runner():
        while True:
            try:
                app_tg=Application.builder().token(BOT_TOKEN).build()
                app_tg.add_handler(CommandHandler("start", start))
                await app_tg.initialize(); await app_tg.start(); await app_tg.updater.start_polling(); await app_tg.updater.idle()
            except Exception as e:
                print(f"Bot error {e}, restarting in 5s"); time.sleep(5)
    import asyncio; asyncio.run(runner())

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000))), daemon=True).start()
    try: run_bot()
    except: app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
