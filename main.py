import os, json, threading, datetime
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db_final_fix.json"
app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [],
            "slider": [
                {"img": "https://img.freepik.com/free-vector/flat-design-earn-money-banner_23-2149439772.jpg", "link": "https://t.me/ProtidinerKajBD", "title": "🔥 প্রতিদিনের কাজ BD"},
                {"img": "https://img.freepik.com/free-vector/gradient-refer-friend-banner_23-2149373488.jpg", "link": "https://t.me/ProtidinerKajBD", "title": "💰 Refer করে ৳50 বোনাস"},
                {"img": "https://img.freepik.com/free-vector/flat-design-affiliate-marketing-banner_23-2149443391.jpg", "link": "https://youtube.com/@ProtidinerKajBD", "title": "▶️ YouTube Join করুন"}
            ],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD",
                "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "banner_color": "#1e40af",
                "ad_zone": "11764581",
                "ad_reward": 1, "ad_daily_limit": 100, "ad_timer": 30,
                "ref_bonus": 50, "min_withdraw": 1000,
                "daily_checkin_reward": 10
            },
            "tasks": [
                {"id": 1, "title": "YouTube ভিডিও দেখুন", "reward": 25, "link": "https://youtube.com/@ProtidinerKajBD", "color": "#065f46", "btn": "শুরু করুন"},
                {"id": 2, "title": "Telegram Join করুন", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join করুন"},
                {"id": 3, "title": "Facebook Follow", "reward": 15, "link": "https://www.facebook.com/share/1AXw16vWRj/", "color": "#1877F2", "btn": "Follow করুন"}
            ]
        }
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(d, f, indent=2)

db = load_db()

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
body{max-width:430px;margin:0 auto;font-family:Arial;background:#eef2ff;padding-bottom:90px}
.top{color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;background:#1e40af}
.top img{width:36px;height:36px;border-radius:50%;background:#fff;padding:2px}
.bal-card{margin:12px;background:linear-gradient(135deg,#1e3a8a,#3b82f6);color:#fff;padding:18px;border-radius:20px;text-align:center}
.bal-big{font-size:48px;font-weight:900;margin:10px 0}
.bal-mini{display:flex;gap:10px;margin-top:12px}
.bal-mini div{flex:1;background:rgba(255,255,255,.2);padding:10px;border-radius:14px}
.card{background:#fff;margin:12px;padding:14px;border-radius:18px;box-shadow:0 4px 12px rgba(0,0,0,.06)}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:bold;cursor:pointer;margin-top:8px}
.tab{display:none}.tab.on{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;display:flex;justify-content:space-around;background:#fff;padding:10px 0;border-top:1px solid #ddd;z-index:99}
.btm div{flex:1;text-align:center;font-size:12px;color:#888;cursor:pointer}.btm div.on{color:#1e40af;font-weight:bold}
.slider{position:relative;width:calc(100% - 24px);margin:12px;height:165px;overflow:hidden;border-radius:18px;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.1)}
.slide{position:absolute;inset:0;opacity:0;transition:opacity.8s;cursor:pointer}.slide.active{opacity:1}.slide img{width:100%;height:100%;object-fit:cover}
.slide-title{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.7));color:#fff;padding:25px 12px 10px;font-weight:bold;font-size:13px}
.dots{text-align:center;margin-top:-4px;margin-bottom:8px}.dot{height:7px;width:7px;background:#bbb;border-radius:50%;display:inline-block;margin:0 3px}.dot.active{background:#1e40af}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:8px;box-sizing:border-box}
</style>
</head><body>
<div class="top"><div style="display:flex;align-items:center;gap:8px"><img id="appLogo" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'"><span id="appName">প্রতিদিনের কাজ BD</span></div><span>৳<span id="bTop">0</span></span></div>

<div id="t-home" class="tab on">
<div class="slider" id="sliderBox"></div><div class="dots" id="dotsBox"></div>
<div class="bal-card"><p>আপনার ব্যালেন্স</p><div class="bal-big">৳<span id="bal">0</span></div><div class="bal-mini"><div>আজ দেখেছেন<br><b><span id="adWatched">0</span>/100</b></div><div>Refer বোনাস<br><b>৳<span id="refBonus">50</span></b></div></div><button class="btn" style="background:#fff;color:#1e40af;margin-top:14px" onclick="go('earn')">💰 এখনই আয় করুন</button></div>
<div class="card" style="display:flex;justify-content:space-between;align-items:center"><div><b>🎁 Daily Check-in</b><br><small>প্রতিদিন ৳<span id="dailyR">10</span> বোনাস</small></div><button class="btn" style="width:auto;background:#f59e0b;padding:10px 18px;color:#fff" onclick="dailyCheck()">বোনাস নিন</button></div>
<div class="card"><div style="display:flex;gap:10px;align-items:center"><div style="background:#dcfce7;padding:10px;border-radius:10px">✅</div><div><b>Protidiner Kaj BD Trusted</b><br><small>5000+ User Payment পেয়েছে</small></div></div></div>
</div>

<div id="t-earn" class="tab">
<div class="card"><h3>📺 কোম্পানি বিজ্ঞাপন - Zone 11764581</h3><p>প্রতি Ads ৳<span id="adR">1</span> | Timer 30s</p><div style="font-size:40px;text-align:center;font-weight:900">৳<span id="adR2">1</span></div><button class="btn" id="adBtn" style="background:#1e40af;color:#fff" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button><p style="font-size:11px;color:green">✅ Telegram App এ Open করলে 100% Ad আসবে | Chrome এ Testing Reward</p><p style="font-size:11px">Watched: <span id="adWatched2">0</span> / <span id="adLimit">100</span></p></div>
<div id="taskList"></div>
<div class="card"><p>👥 Refer ৳<span id="refR">50</span></p><p id="refLink" style="font-size:11px;background:#f1f5f9;padding:8px;border-radius:8px;word-break:break-all"></p><button class="btn" style="background:#10b981;color:#fff" onclick="navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('Copied')">Copy Link</button></div>
</div>

<div id="t-support" class="tab">
<div class="card"><h3>🎧 সাপোর্ট সেন্টার - ফিটফাট ✅</h3><button class="btn" style="background:#1e40af;color:#fff" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">📢 অফিশিয়াল চ্যানেল</button><button class="btn" style="background:#FF0000;color:#fff" onclick="window.open('https://youtube.com/@ProtidinerKajBD','_blank')">▶️ YouTube Channel</button><button class="btn" style="background:#1877F2;color:#fff" onclick="window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank')">📘 Facebook Page</button><button class="btn" style="background:#10b981;color:#fff" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">💬 Admin এর সাথে কথা বলুন</button></div>
<div class="card"><h4>❓ FAQ</h4><details><summary>💰 টাকা কিভাবে পাবো?</summary><p style="font-size:12px">Min ৳1000 হলে Withdraw দিন, 24h এ পাবেন।</p></details><details><summary>📺 Ad আসে না কেন?</summary><p style="font-size:12px">Telegram App এর ভিতরে Bot থেকে Open App দিয়ে ঢুকুন, Zone 11764581 এখন ঠিক আছে।</p></details><details><summary>🎁 Refer বোনাস?</summary><p style="font-size:12px">প্রতি Refer এ ৳50 পাবেন।</p></details></div>
<div class="card" style="background:#f0fdf4;text-align:center"><b>✅ 100% Trusted - ProtidinerKajBD</b><br><small>5000+ User Payment পেয়েছে</small></div>
</div>

<div id="t-withdraw" class="tab">
<div class="card"><h3>💳 উইথড্র - ফিটফাট ✅</h3><div style="font-size:36px;text-align:center;font-weight:900">৳<span class="bal2">0</span></div><input id="wNum" placeholder="bKash/Nagad Number"><input id="wAmt" type="number" placeholder="Amount - Min 1000"><button class="btn" style="background:#1e40af;color:#fff" onclick="doWithdraw()">উইথড্র রিকোয়েস্ট করুন</button></div>
<div class="card"><h4>💳 পেমেন্ট মেথড</h4><div style="display:flex;gap:8px"><div style="flex:1;background:#e11d48;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:bold">bKash</div><div style="flex:1;background:#f59e0b;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:bold">Nagad</div><div style="flex:1;background:#0ea5e9;color:#fff;padding:12px;border-radius:10px;text-align:center;font-weight:bold">Rocket</div></div><p style="font-size:11px;margin-top:10px">⏰ পেমেন্ট টাইম: প্রতিদিন রাত 8PM - 10PM<br>📋 নিয়ম: 1. ভুল Number দিবেন না 2. Min ৳1000</p></div>
<div class="card"><h4>📜 আমার Withdraw History</h4><div id="wdHistory"><p style="font-size:11px;color:#888">কোনো History নেই, প্রথম Withdraw করুন</p></div></div>
<div class="card" style="background:#eff6ff"><p style="font-size:12px">🔥 আজ 127 জন Withdraw করেছে - সর্বশেষ ৳5000 bKash Payment Done!</p></div>
</div>

<div class="btm"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>

<script>
const tg=Telegram.WebApp;
let qp=new URLSearchParams(location.search);
let uid=qp.get('id')||tg.initDataUnsafe?.user?.id||"8807178385";
let ref=qp.get('ref');
let curSlide=0, slideInt, lastAd=0;

function go(t){
 document.querySelectorAll('.tab').forEach(e=>e.classList.remove('on'));
 document.getElementById('t-'+t).classList.add('on');
 document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));
 document.getElementById('b-'+t).classList.add('on');
}

function initSlider(imgs){
 let box=document.getElementById('sliderBox');
 let dots=document.getElementById('dotsBox');
 if(!imgs ||!imgs.length){ box.innerHTML='<div style="padding:40px;text-align:center">No Ads - Add from Admin</div>'; return; }
 box.innerHTML=''; dots.innerHTML='';
 imgs.forEach((it,i)=>{
  let d=document.createElement('div');
  d.className='slide'+(i==0?' active':'');
  d.innerHTML=`<img src="${it.img}" onerror="this.src='https://via.placeholder.com/400x200?text=Ad'"><div class="slide-title">${it.title||'Protidiner Kaj BD'}</div>`;
  d.onclick=()=>window.open(it.link,'_blank');
  box.appendChild(d);
  let dot=document.createElement('span');
  dot.className='dot'+(i==0?' active':'');
  dots.appendChild(dot);
 });
 if(slideInt) clearInterval(slideInt);
 slideInt=setInterval(()=>{
  let slides=document.querySelectorAll('.slide');
  let ds=document.querySelectorAll('.dot');
  if(!slides.length) return;
  slides[curSlide].classList.remove('active');
  ds[curSlide].classList.remove('active');
  curSlide=(curSlide+1)%slides.length;
  slides[curSlide].classList.add('active');
  ds[curSlide].classList.add('active');
 },3500);
}

function load(){
 fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{
  if(d.banned){ document.body.innerHTML="<h2 style='text-align:center;margin-top:50px'>⛔ Banned</h2>"; return; }
  document.getElementById('bal').innerText=d.user.balance;
  document.getElementById('bTop').innerText=d.user.balance;
  document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance);
  document.getElementById('adWatched').innerText=d.user.ads_watched||0;
  document.getElementById('adWatched2').innerText=d.user.ads_watched||0;
  let s=d.settings;
  document.getElementById('appName').innerText=s.app_name;
  document.getElementById('appLogo').src=s.logo_url;
  document.getElementById('adR').innerText=s.ad_reward;
  document.getElementById('adR2').innerText=s.ad_reward;
  document.getElementById('adLimit').innerText=s.ad_daily_limit;
  document.getElementById('refBonus').innerText=s.ref_bonus;
  document.getElementById('refR').innerText=s.ref_bonus;
  document.getElementById('dailyR').innerText=s.daily_checkin_reward;
  document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;
  initSlider(d.slider);
  let tl=document.getElementById('taskList'); tl.innerHTML='';
  d.tasks.forEach(t=>{
   tl.innerHTML+=`<div class="card"><div style="display:flex;justify-content:space-between"><b>${t.title}</b><b style="color:green">৳${t.reward}</b></div><button class="btn" style="background:${t.color};color:#fff" onclick="window.open('${t.link}','_blank')">${t.btn}</button></div>`;
  });
 });
}

function watchAd(){
 let now=Date.now();
 if(now-lastAd < 30000){ alert("⏳ 30 সেকেন্ড পর আবার"); return; }
 let btn=document.getElementById('adBtn');
 btn.innerText="⏳ বিজ্ঞাপন লোড হচ্ছে...";

 if(typeof show_11764581!== 'undefined'){
  show_11764581().then(()=>{
   lastAd=Date.now();
   btn.innerText="▶ বিজ্ঞাপন দেখুন";
   fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{
    if(d.ok){ alert('✅ ৳'+d.reward+' যোগ হলো! (Company Ad Zone 11764581)'); load(); }
   });
  }).catch(()=>{
   show_11764581('pop').then(()=>{
    lastAd=Date.now();
    btn.innerText="▶ বিজ্ঞাপন দেখুন";
    fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ load(); });
   }).catch(()=>{
    btn.innerText="▶ বিজ্ঞাপন দেখুন";
    fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ alert('⚠️ Ad Block আছে, Testing Reward ৳'+d.reward); load(); });
   });
  });
 } else {
  btn.innerText="▶ বিজ্ঞাপন দেখুন";
  alert("Telegram App এর ভিতরে Open করো ভাই, তাহলে কোম্পানি Ad আসবে। Chrome এ AdBlock থাকে");
  fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ load(); });
 }
}

function doWithdraw(){
 let n=document.getElementById('wNum').value;
 let a=document.getElementById('wAmt').value;
 if(!n||!a) return alert("Number ও Amount দাও");
 fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}`).then(r=>r.json()).then(d=>alert(d.msg));
}

function dailyCheck(){
 fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(d=>{ alert(d.msg); load(); });
}

load();
</script>
</body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin</title>
<style>body{max-width:600px;margin:0 auto;font-family:Arial;padding:12px;background:#f1f5f9}.card{background:#fff;padding:14px;border-radius:12px;margin:10px 0}input{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:1px solid #ddd;box-sizing:border-box}.btn{width:100%;padding:12px;border:none;border-radius:8px;color:#fff;font-weight:bold;background:#1e40af;cursor:pointer;margin-top:6px}</style>
</head><body>
<h2>Admin - নিজের Ad লেখো ✅</h2>
<div class="card"><h3>📢 নিজের বিজ্ঞাপন লেখো - Slider 3.5s</h3>
<input id="sTitle" placeholder="Title লেখো - যেমন: 🔥 আজ 5000 টাকা Giveaway!">
<input id="sImg" placeholder="Image URL - https://...">
<input id="sLink" placeholder="Link - https://t.me/...">
<button class="btn" onclick="addSlider()">+ Add করো - নিজের বিজ্ঞাপন</button>
<div id="list"></div>
</div>
<script>
let aid=new URLSearchParams(location.search).get('id')||'8807178385';
function loadA(){ fetch(`/api/get_full?id=${aid}`).then(r=>r.json()).then(d=>{ let l=document.getElementById('list'); l.innerHTML=''; d.slider.forEach((s,i)=>{ l.innerHTML+=`<div style="border:1px solid #ddd;padding:8px;margin:6px 0;border-radius:8px"><img src="${s.img}" style="width:100%;height:80px;object-fit:cover"><p>${s.title}</p><button onclick="delS(${i})" style="background:#ef4444;color:#fff;border:none;padding:6px 12px;border-radius:6px">Delete</button></div>`; }); }); }
function addSlider(){ let img=document.getElementById('sImg').value; let link=document.getElementById('sLink').value; let title=document.getElementById('sTitle').value; if(!img) return alert('Image দাও'); fetch(`/api/add_slider?id=${aid}&img=${encodeURIComponent(img)}&link=${encodeURIComponent(link)}&title=${encodeURIComponent(title)}`).then(r=>r.json()).then(d=>{ alert(d.msg); loadA(); }); }
function delS(i){ fetch(`/api/del_slider?id=${aid}&idx=${i}`).then(r=>r.json()).then(d=>loadA()); }
loadA();
</script>
</body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id','8807178385')
    d = load_db()
    if uid not in d['users']:
        d['users'][uid] = {'balance':0,'ads_watched':0,'last_daily':''}
        save_db(d)
    return jsonify({"user": d['users'][uid], "settings": d['settings'], "slider": d['slider'], "tasks": d['tasks'], "banned": uid in d['banned']})

@app.route('/api/reward')
def reward():
    uid = request.args.get('id')
    d = load_db()
    if uid not in d['users']: d['users'][uid] = {'balance':0,'ads_watched':0,'last_daily':''}
    d['users'][uid]['balance'] += d['settings']['ad_reward']
    d['users'][uid]['ads_watched'] = d['users'][uid].get('ads_watched',0)+1
    save_db(d)
    return jsonify({"ok":True,"reward":d['settings']['ad_reward']})

@app.route('/api/daily')
def daily():
    uid = request.args.get('id')
    d = load_db()
    today = str(datetime.date.today())
    if d['users'][uid].get('last_daily') == today:
        return jsonify({"ok":False,"msg":"আজ বোনাস নিয়েছো"})
    d['users'][uid]['balance'] += d['settings']['daily_checkin_reward']
    d['users'][uid]['last_daily'] = today
    save_db(d)
    return jsonify({"ok":True,"msg": f"✅ ৳{d['settings']['daily_checkin_reward']} Daily Bonus!"})

@app.route('/api/withdraw')
def wd():
    uid = request.args.get('id'); num = request.args.get('num'); amt = int(request.args.get('amt') or 0)
    d = load_db()
    if d['users'][uid]['balance'] < amt: return jsonify({"ok":False,"msg":"Balance কম"})
    if amt < d['settings']['min_withdraw']: return jsonify({"ok":False,"msg":f"Min {d['settings']['min_withdraw']} লাগবে"})
    d['users'][uid]['balance'] -= amt
    d['withdraws'].append({"uid":uid,"num":num,"amt":amt,"date":str(datetime.datetime.now())})
    save_db(d)
    return jsonify({"ok":True,"msg":"✅ Withdraw Request Sent - 24h এ পাবেন"})

@app.route('/api/add_slider')
def add_slider():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"ok":False})
    d = load_db()
    d['slider'].append({"img":request.args.get('img'),"link":request.args.get('link'),"title":request.args.get('title','')})
    save_db(d)
    return jsonify({"ok":True,"msg":"✅ নিজের বিজ্ঞাপন Add হলো - 3.5s পর পর দেখাবে!"})

@app.route('/api/del_slider')
def del_slider():
    if request.args.get('id')!= str(ADMIN_ID): return jsonify({"ok":False})
    d = load_db(); idx = int(request.args.get('idx') or 0)
    if 0 <= idx < len(d['slider']): d['slider'].pop(idx)
    save_db(d)
    return jsonify({"ok":True})

def run_bot():
    async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
        uid = str(u.effective_user.id)
        d = load_db()
        if uid not in d['users']: d['users'][uid]={'balance':0,'ads_watched':0,'last_daily':''}; save_db(d)
        kb = [[InlineKeyboardButton("🚀 Open App - Zone 11764581", web_app={"url": f"https://am-bot-1-v77g.onrender.com/?id={uid}"})]]
        await u.message.reply_text(f"Welcome {u.effective_user.first_name} ✅\nZone 11764581 Ready - Ad 100% আসবে Telegram এ", reply_markup=InlineKeyboardMarkup(kb))
    async def runner():
        app_tg = Application.builder().token(BOT_TOKEN).build()
        app_tg.add_handler(CommandHandler("start", start))
        await app_tg.initialize(); await app_tg.start()
        await app_tg.updater.start_polling(); await app_tg.updater.idle()
    import asyncio; asyncio.run(runner())

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000))), daemon=True).start()
    try: run_bot()
    except: app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
