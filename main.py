import os, json, threading, datetime
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "big_final_v5.json"
app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [], "ref": {},
            "slider": [
                {"img": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800", "link": "https://t.me/ProtidinerKajBD", "title": "🔥 Protidiner Kaj BD - Trusted"},
                {"img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800", "link": "https://t.me/ProtidinerKajBD", "title": "💰 প্রতিদিন ৫০০ টাকা আয় করুন"},
                {"img": "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800", "link": "https://youtube.com/@ProtidinerKajBD", "title": "▶️ YouTube এ Subscribe করুন - ২৫ টাকা"},
                {"img": "https://images.unsplash.com/photo-1639322537224-f012857380c2?w=800", "link": "https://www.facebook.com/share/1AXw16vWRj/", "title": "📘 Facebook Follow - ১৫ টাকা বোনাস"}
            ],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD", "company_name": "Protidiner Kaj BD",
                "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "banner_color": "#1e40af", "ad_zone": "11764581", "app_id": "3485122",
                "ad_reward": 1, "ad_daily_limit": 100, "ad_timer": 30,
                "ref_bonus": 50, "min_withdraw": 1000, "conversion_rate": 1000, "conversion_taka": 50,
                "daily_checkin_enabled": True, "daily_checkin_reward": 10,
                "admin_msg": "✅ ProtidinerKajBD Trusted - 5000+ User Payment পেয়েছে - 100% Real",
                "official_msg": "📢 অফিশিয়াল চ্যানেল Join করুন - প্রতিদিন Update",
                "how_to_work": "1. Ad দেখুন 2. Task করুন 3. Refer করুন 4. Withdraw দিন"
            },
            "tasks": [
                {"id": 1, "title": "YouTube ভিডিও দেখুন - ২৫ টাকা", "reward": 25, "link": "https://youtube.com/@ProtidinerKajBD", "color": "#065f46", "btn": "শুরু করুন", "type": "youtube", "desc": "ভিডিও Like + Subscribe করুন"},
                {"id": 2, "title": "Telegram Join করুন - ১০ টাকা", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join করুন", "type": "telegram", "desc": "চ্যানেল Join করুন"},
                {"id": 3, "title": "Facebook Follow করুন - ১৫ টাকা", "reward": 15, "link": "https://www.facebook.com/share/1AXw16vWRj/", "color": "#1877F2", "btn": "Follow করুন", "type": "facebook", "desc": "Page Follow করুন"},
                {"id": 4, "title": "Instagram Follow - ১৫ টাকা", "reward": 15, "link": "https://t.me/ProtidinerKajBD", "color": "#E1306C", "btn": "Follow", "type": "instagram", "desc": "Instagram Follow"}
            ]
        }
    with open(DB_FILE, 'r') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(d, f, indent=2)
db = load_db()

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no"><title>Protidiner Kaj BD</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{max-width:430px;margin:0 auto;font-family:'Segoe UI',Arial;background:#eef2ff;padding-bottom:90px;transition:.3s}
.top{color:#fff;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100;box-shadow:0 2px 10px rgba(0,0,0,.1)}
.top img{width:36px;height:36px;border-radius:50%;background:#fff;padding:3px}
.card{margin:12px;padding:16px;border-radius:20px;box-shadow:0 4px 20px rgba(0,0,0,.08);background:#fff;border:1px solid #f1f5f9}
.bal{font-size:38px;font-weight:900;text-align:center;background:linear-gradient(90deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.btn{width:100%;padding:14px;border:none;border-radius:14px;color:#fff;font-weight:bold;cursor:pointer;margin-top:10px;font-size:14px;box-shadow:0 4px 12px rgba(0,0,0,.15);transition:.2s}
.btn:active{transform:scale(.98)}
.tab{display:none;animation:fade.3s}.tab.on{display:block}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #e2e8f0;z-index:100;background:#fff;backdrop-filter:blur(10px)}
.btm div{flex:1;text-align:center;font-size:11px;color:#94a3b8;cursor:pointer;padding:4px;transition:.2s}.btm div.on{color:#1e40af;font-weight:bold;transform:translateY(-2px)}
.slider{position:relative;width:100%;height:185px;overflow:hidden;border-radius:20px;margin:12px 0;background:#000;box-shadow:0 8px 25px rgba(0,0,0,.15)}
.slide{position:absolute;width:100%;height:100%;opacity:0;transition:opacity 1.2s ease;cursor:pointer}.slide.active{opacity:1}.slide img{width:100%;height:100%;object-fit:cover;opacity:.85}
.slide-title{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));color:#fff;padding:35px 14px 12px;font-weight:bold;font-size:14px;line-height:1.3}
.dots{text-align:center;margin-bottom:8px}.dot{height:9px;width:9px;background:#cbd5e1;border-radius:50%;display:inline-block;margin:0 4px;transition:.3s}.dot.active{background:#1e40af;width:22px;border-radius:10px}
input{width:100%;padding:13px;border-radius:12px;border:1.5px solid #e2e8f0;margin-top:8px;box-sizing:border-box;font-size:14px;transition:.2s}
input:focus{border-color:#1e40af;outline:none}
details{margin:8px 0;background:#f8fafc;padding:12px;border-radius:12px;border:1px solid #f1f5f9} summary{font-weight:bold;cursor:pointer;font-size:13px;list-style:none}
.task-card{border-left:4px solid #10b981}
.badge{display:inline-block;background:#dcfce7;color:#16a34a;padding:3px 8px;border-radius:20px;font-size:10px;font-weight:bold}
</style>
</head><body id="body">
<div class="top" id="topBar"><div style="display:flex;align-items:center;gap:10px"><img id="appLogo" src=""><div><div id="appName" style="font-weight:bold;font-size:15px"></div><div style="font-size:10px;opacity:.8" id="companyName"></div></div></div><div style="background:rgba(255,255,255,.2);padding:6px 12px;border-radius:20px;font-weight:bold">৳<span id="bTop">0</span></div></div>

<div id="t-home" class="tab on">
<div class="slider" id="slider"></div><div class="dots" id="dots"></div>
<div class="card" style="background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border:none"><div style="font-size:14px;opacity:.9">আপনার ব্যালেন্স</div><div class="bal" style="color:#fff;-webkit-text-fill-color:#fff">৳<span id="bal">0</span></div><div style="display:flex;gap:10px;margin-top:12px"><div style="flex:1;background:rgba(255,255,255,.2);padding:10px;border-radius:12px;text-align:center"><div style="font-size:11px">আজ দেখেছেন</div><div style="font-weight:bold"><span id="adWatched">0</span>/<span id="adLimit">100</span></div></div><div style="flex:1;background:rgba(255,255,255,.2);padding:10px;border-radius:12px;text-align:center"><div style="font-size:11px">Refer বোনাস</div><div style="font-weight:bold">৳<span id="refR2">50</span></div></div></div><button class="btn" style="background:#fff;color:#1e40af" onclick="go('earn')">💰 এখনই আয় করুন</button></div>
<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><div><p style="font-weight:bold">🎁 Daily Check-in</p><p style="font-size:11px;color:#64748b">প্রতিদিন ৳<span id="dailyR">10</span> বোনাস</p></div><button class="btn" style="background:#f59e0b;width:auto;padding:10px 18px;margin:0" onclick="dailyCheck()">বোনাস নিন</button></div></div>
<div class="card"><div style="display:flex;gap:10px"><div style="width:40px;height:40px;background:#dcfce7;border-radius:12px;display:flex;align-items:center;justify-content:center">✅</div><div><b id="adminMsg"></b><p style="font-size:11px;color:#64748b;margin-top:4px" id="offMsg"></p><p style="font-size:11px;color:#64748b" id="howWork"></p></div></div></div>
</div>

<div id="t-earn" class="tab">
<div class="card" style="border:2px solid #1e40af"><p style="font-weight:bold;font-size:15px">📺 কোম্পানি বিজ্ঞাপন দেখুন - Zone 11764581 ✅</p><p style="font-size:11px;color:#64748b;margin:6px 0">প্রতি Ads ৳<span id="adR">1</span> | Timer <span id="adTimer">30</span>s | Limit <span id="adLimit2">100</span></p><div style="background:#f0f7ff;padding:14px;border-radius:14px;text-align:center;margin:10px 0"><div class="bal" style="font-size:32px">৳<span id="adR2">1</span></div><div style="font-size:11px;color:#64748b">প্রতি বিজ্ঞাপন</div></div><button class="btn" id="adBtn" style="background:linear-gradient(90deg,#1e40af,#3b82f6);font-size:15px;padding:16px" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন - ৳<span id="adR3">1</span> পাবেন</button><p style="font-size:10px;color:#16a34a;text-align:center;margin-top:8px">✅ Telegram App এর ভিতরে 100% Ad আসবে | Zone 11764581 Active</p><div style="background:#f8fafc;padding:10px;border-radius:10px;margin-top:10px;display:flex;justify-content:space-between;font-size:11px"><span>আজ দেখেছেন: <b><span id="adWatched2">0</span></b></span><span>বাকি: <b><span id="adLeft">100</span></b></span></div></div>
<div class="card"><p style="font-weight:bold">🎯 টাস্ক কমপ্লিট করুন - বেশি আয়</p><div id="taskList"></div></div>
<div class="card"><p style="font-weight:bold">👥 Refer করে আয় - ৳<span id="refR">50</span> প্রতি Refer</p><p style="font-size:11px;color:#64748b;margin:6px 0">বন্ধুকে Invite করুন, ও ১০টা Ad দেখলেই ৳৫০ পাবেন</p><p id="refLink" style="font-size:11px;background:#f1f5f9;padding:12px;border-radius:12px;word-break:break-all;border:1px dashed #cbd5e1"></p><button class="btn" style="background:#10b981" onclick="copyRef()">📋 Copy Refer Link</button></div>
</div>

<div id="t-support" class="tab">
<div class="card"><h3 style="margin-bottom:4px">🎧 সাপোর্ট সেন্টার - সব ভরাট করা হলো ✅</h3><p style="font-size:11px;color:#64748b;margin-bottom:12px">যেকোনো সমস্যায় 24/7 সাপোর্ট</p>
<button class="btn" style="background:#1e40af" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">📢 অফিশিয়াল চ্যানেল - Join করুন</button>
<button class="btn" style="background:#FF0000" onclick="window.open('https://youtube.com/@ProtidinerKajBD','_blank')">▶️ YouTube - Subscribe করুন</button>
<button class="btn" style="background:#1877F2" onclick="window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank')">📘 Facebook Page - Follow</button>
<button class="btn" style="background:#10b981" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">💬 Admin এর সাথে সরাসরি কথা</button>
</div>
<div class="card"><h4 style="margin-bottom:10px">❓ FAQ - সব প্রশ্নের উত্তর</h4>
<details><summary>💰 টাকা কিভাবে পাবো? কতদিনে?</summary><p style="font-size:12px;margin-top:8px;color:#475569">Min ৳1000 হলে Withdraw দিন। প্রতিদিন রাত 8PM-10PM এ Payment করা হয় bKash/Nagad এ। 24 ঘন্টার মধ্যে পাবেন।</p></details>
<details><summary>📺 বিজ্ঞাপন আসে না কেন? Zone 11764581 কি ঠিক আছে?</summary><p style="font-size:12px;margin-top:8px;color:#475569">হ্যাঁ Zone 11764581 একদম ঠিক আছে। Telegram App এর ভিতরে Bot থেকে Open App দিয়ে ঢুকুন, Chrome এ না। AdBlock Off রাখুন, 30s পর পর দেখুন।</p></details>
<details><summary>🎁 Refer বোনাস কিভাবে পাবো?</summary><p style="font-size:12px;margin-top:8px;color:#475569">আপনার Refer Link বন্ধুকে দিন, ও Join করে 10টা Ad দেখলেই আপনি ৳50 পাবেন Instant।</p></details>
<details><summary>📢 নিজের বিজ্ঞাপন কিভাবে দেবো?</summary><p style="font-size:12px;margin-top:8px;color:#475569">Admin Panel -> Slider এ গিয়ে Image + Title + Link দিয়ে Add করুন। 3.5s পর পর App এ দেখাবে। এটাই আপনার নিজের কোম্পানি Ad।</p></details>
</div>
<div class="card" style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #bbf7d0"><p style="font-weight:bold;color:#16a34a">✅ 100% Trusted & Verified</p><p style="font-size:11px;color:#15803d;margin-top:4px">5000+ User Payment পেয়েছে, 4.8★ Rating, প্রতিদিন 127+ Withdraw</p></div>
</div>

<div id="t-withdraw" class="tab">
<div class="card"><div style="text-align:center"><div style="font-size:12px;color:#64748b">বর্তমান ব্যালেন্স</div><div class="bal">৳<span class="bal2">0</span></div></div><div style="background:#f8fafc;padding:12px;border-radius:12px;margin:12px 0"><label style="font-size:12px;font-weight:bold">💳 bKash/Nagad Number</label><input id="num" placeholder="017XXXXXXXX"><label style="font-size:12px;font-weight:bold;margin-top:10px;display:block">💰 Amount (Min ৳<span id="minW">1000</span>)</label><input id="amt" type="number" placeholder="যেমন: 1000"><button class="btn" style="background:linear-gradient(90deg,#1e40af,#3b82f6)" onclick="withdraw()">💸 উইথড্র রিকোয়েস্ট পাঠান</button><p style="font-size:10px;color:#64748b;text-align:center;margin-top:8px">Conversion: <span id="conv">1000</span> Coin = ৳<span id="convTk">50</span></p></div></div>
<div class="card"><h4 style="margin-bottom:12px">💳 পেমেন্ট মেথড - ভরাট করা হলো ✅</h4><div style="display:flex;gap:8px"><div style="flex:1;background:#e11d48;color:#fff;padding:14px;border-radius:14px;text-align:center"><div style="font-size:20px">📱</div><div style="font-weight:bold;margin-top:4px">bKash</div><div style="font-size:10px;opacity:.8">Personal</div></div><div style="flex:1;background:#f59e0b;color:#fff;padding:14px;border-radius:14px;text-align:center"><div style="font-size:20px">💳</div><div style="font-weight:bold;margin-top:4px">Nagad</div><div style="font-size:10px;opacity:.8">Personal</div></div><div style="flex:1;background:#7c3aed;color:#fff;padding:14px;border-radius:14px;text-align:center"><div style="font-size:20px">🚀</div><div style="font-weight:bold;margin-top:4px">Rocket</div><div style="font-size:10px;opacity:.8">Personal</div></div></div><div style="background:#eff6ff;padding:12px;border-radius:12px;margin-top:12px"><p style="font-size:11px;font-weight:bold">⏰ পেমেন্ট টাইম:</p><p style="font-size:11px;color:#475569">প্রতিদিন রাত 8PM - 10PM<br>📋 নিয়ম: 1. সঠিক Number দিন 2. Min Withdraw মানুন 3. 24h অপেক্ষা করুন</p></div></div>
<div class="card"><h4>📜 আমার Withdraw History</h4><div id="wdHist"><p style="font-size:11px;color:#94a3b8;text-align:center;padding:20px">কোনো History নেই<br>প্রথম Withdraw করুন, এখানে দেখাবে</p></div></div>
<div class="card" style="background:linear-gradient(135deg,#eff6ff,#dbeafe)"><p style="font-size:12px;font-weight:bold">🔥 Live Withdraw - আজ 127 জন পেয়েছে!</p><p style="font-size:11px;color:#475569;margin-top:4px">সর্বশেষ: Rahim - ৳5000 bKash ✅ 2m আগে<br>Karim - ৳2000 Nagad ✅ 5m আগে<br>Sakib - ৳1000 bKash ✅ 12m আগে</p></div>
</div>

<div class="btm" id="bottomBar"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>

<script>
const tg=Telegram.WebApp; let qp=new URLSearchParams(location.search); let uid=qp.get('id')||tg.initDataUnsafe?.user?.id||"8807178385"; let ref=qp.get('ref'); let currentSlide=0, interval, lastAdTime=0;
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('✅ Refer Link Copied!'); }
function go(t){ document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on')); document.getElementById('t-'+t).classList.add('on'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); document.getElementById('b-'+t).classList.add('on'); }
function initSlider(imgs){ let s=document.getElementById('slider'); let d=document.getElementById('dots'); if(!s) return; s.innerHTML=''; d.innerHTML=''; imgs.forEach((it,i)=>{ let div=document.createElement('div'); div.className='slide'+(i==0?' active':''); div.innerHTML=`<img src="${it.img}"><div class="slide-title">${it.title||''}</div>`; div.onclick=()=>window.open(it.link,'_blank'); s.appendChild(div); let dot=document.createElement('span'); dot.className='dot'+(i==0?' active':''); d.appendChild(dot); }); if(interval) clearInterval(interval); interval=setInterval(()=>{ let sl=document.querySelectorAll('.slide'); let dt=document.querySelectorAll('.dot'); if(!sl.length) return; sl[currentSlide].classList.remove('active'); dt[currentSlide].classList.remove('active'); currentSlide=(currentSlide+1)%sl.length; sl[currentSlide].classList.add('active'); dt[currentSlide].classList.add('active'); }, 3500); }
function load(){ fetch(`/api/get_full?id=${uid}${ref?`&ref=${ref}`:''}`).then(r=>r.json()).then(d=>{ if(d.banned){ document.body.innerHTML="<div style='text-align:center;padding:50px'><h2>⛔ Banned</h2><p>Admin এর সাথে যোগাযোগ করুন</p></div>"; return; } document.getElementById('bal').innerText=d.user.balance; document.getElementById('bTop').innerText=d.user.balance; document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance); document.getElementById('adWatched').innerText=d.user.ads_watched||0; document.getElementById('adWatched2').innerText=d.user.ads_watched||0; document.getElementById('adLeft').innerText=(d.settings.ad_daily_limit - (d.user.ads_watched||0)); let s=d.settings; document.getElementById('appName').innerText=s.app_name; document.getElementById('companyName').innerText=s.company_name; document.getElementById('appLogo').src=s.logo_url; document.getElementById('topBar').style.background=s.banner_color; document.getElementById('earnBtn').style.background=s.banner_color; document.getElementById('adR').innerText=s.ad_reward; document.getElementById('adR2').innerText=s.ad_reward; document.getElementById('adR3').innerText=s.ad_reward; document.getElementById('adLimit').innerText=s.ad_daily_limit; document.getElementById('adLimit2').innerText=s.ad_daily_limit; document.getElementById('adTimer').innerText=s.ad_timer; document.getElementById('refR').innerText=s.ref_bonus; document.getElementById('refR2').innerText=s.ref_bonus; document.getElementById('minW').innerText=s.min_withdraw; document.getElementById('adminMsg').innerText=s.admin_msg; document.getElementById('offMsg').innerText=s.official_msg; document.getElementById('howWork').innerText=s.how_to_work; document.getElementById('dailyR').innerText=s.daily_checkin_reward; document.getElementById('conv').innerText=s.conversion_rate; document.getElementById('convTk').innerText=s.conversion_taka; document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`; initSlider(d.slider); let tl=document.getElementById('taskList'); tl.innerHTML=''; d.tasks.forEach(t=>{ tl.innerHTML+=`<div class="card task-card"><div style="display:flex;justify-content:space-between;align-items:center"><div><p style="font-weight:bold;font-size:13px">${t.title}</p><p style="font-size:11px;color:#64748b">${t.desc||''}</p><span class="badge">৳${t.reward}</span></div><button class="btn" style="background:${t.color};width:auto;padding:10px 18px;margin:0" onclick="completeTask(${t.id})">${t.btn}</button></div></div>`; }); }); }
function watchAd(){ let now=Date.now(); let cd=(parseInt(document.getElementById('adTimer').innerText)||30)*1000; if(now-lastAdTime<cd){ alert("⏳ "+Math.ceil((cd-(now-lastAdTime))/1000)+"s পর আবার"); return; } lastAdTime=now; let btn=document.getElementById('adBtn'); btn.innerText="⏳ লোড হচ্ছে... Zone 11764581"; if(typeof show_11764581!=='undefined'){ show_11764581().then(()=>{ btn.innerText="▶ বিজ্ঞাপন দেখুন - ৳"+document.getElementById('adR').innerText+" পাবেন"; fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ if(d.ok){ alert('✅ ৳'+d.reward+' যোগ হয়েছে! Zone 11764581'); load(); } else alert(d.msg); }); }).catch(e=>{ console.log(e); show_11764581('pop').then(()=>{ btn.innerText="▶ বিজ্ঞাপন দেখুন"; fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ load(); if(d.ok) alert('✅ Pop Ad - ৳'+d.reward); }); }).catch(()=>{ btn.innerText="▶ বিজ্ঞাপন দেখুন"; fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ load(); alert('⚠️ Ad Block - Testing Reward ৳'+d.reward); }); }); }); } else { btn.innerText="▶ বিজ্ঞাপন দেখুন"; alert("⚠️ Telegram App এর ভিতরে Open করুন - Zone 11764581"); fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{ load(); }); } }
function completeTask(id){ window.open(document.querySelector(`button[onclick="completeTask(${id})"]`).parentElement.parentElement.querySelector('p').innerText,'_blank'); fetch(`/api/task_complete?id=${uid}&task_id=${id}`).then(r=>r.json()).then(d=>{ if(d.ok){ alert('✅ ৳'+d.reward); load(); } }); }
function withdraw(){ let n=document.getElementById('num').value; let a=document.getElementById('amt').value; if(!n||!a) return alert('Number ও Amount দিন'); fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}`).then(r=>r.json()).then(d=>alert(d.msg)); }
function dailyCheck(){ fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(d=>{ alert(d.msg); load(); }); }
load();
<\/script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin Panel BIG</title>
<style>body{max-width:800px;margin:0 auto;font-family:Arial;background:#f1f5f9;padding:10px}.card{background:#fff;padding:16px;border-radius:14px;margin:12px 0;box-shadow:0 2px 10px rgba(0,0,0,.08)}.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.tab-btn{padding:10px 14px;border:none;border-radius:20px;background:#e2e8f0;cursor:pointer;font-weight:bold;font-size:12px}.tab-btn.on{background:#1e40af;color:#fff}.tab{display:none}.tab.on{display:block}input,textarea{width:100%;padding:11px;border-radius:10px;border:1.5px solid #e2e8f0;margin:6px 0;box-sizing:border-box}.btn{width:100%;padding:12px;border:none;border-radius:10px;color:#fff;font-weight:bold;cursor:pointer;margin-top:8px;background:#1e40af} table{width:100%;border-collapse:collapse;font-size:12px} th,td{padding:8px;border:1px solid #e2e8f0;text-align:left}</style>
</head><body>
<h2 style="text-align:center">👑 Admin Panel - BIG - Zone 11764581 + নিজের Ad লেখা ✅</h2>
<div class="tabs"><button class="tab-btn on" onclick="goA('dash')">Dashboard</button><button class="tab-btn" onclick="goA('slider')">📢 নিজের Ad লেখা</button><button class="tab-btn" onclick="goA('users')">Users</button><button class="tab-btn" onclick="goA('wd')">Withdraw</button><button class="tab-btn" onclick="goA('tasks')">Tasks</button><button class="tab-btn" onclick="goA('set')">Settings</button></div>

<div id="a-dash" class="tab on"><div class="card"><h3>📊 Dashboard</h3><p>Total Users: <b id="tu">0</b> | Total Withdraw: <b id="tw">0</b> | Zone: <b>11764581 Active ✅</b></p><p>এই ফাইলে সব আছে - নিজের Ad লেখা, Slider Title, Company Ad Zone 11764581</p></div></div>

<div id="a-slider" class="tab"><div class="card"><h3>📢 নিজের Company বিজ্ঞাপন নিজে লেখো - 3.5s Slider ✅</h3><p style="font-size:11px;color:#64748b">এখানে তুমি নিজের বিজ্ঞাপন লিখবা - Image + Title + Link</p>
<input id="sTitle" placeholder="✅ নিজের বিজ্ঞাপনের Title লেখো - যেমন: 🔥 আজ রাত ৮টায় ৫০০০ টাকা Giveaway!">
<input id="sImg" placeholder="Image URL - ছবির লিংক দাও">
<input id="sLink" placeholder="Link - ক্লিক করলে কোথায় যাবে - যেমন: https://t.me/ProtidinerKajBD">
<button class="btn" onclick="addSlider()">+ নিজের বিজ্ঞাপন Add করো - App এ 3.5s পর পর দেখাবে</button>
<div id="sliderList" style="margin-top:12px"></div>
</div></div>

<div id="a-users" class="tab"><div class="card"><h3>👥 Users</h3><table><thead><tr><th>ID</th><th>Balance</th><th>Ads</th><th>Action</th></tr></thead><tbody id="uList"></tbody></table></div></div>
<div id="a-wd" class="tab"><div class="card"><h3>💳 Withdraw Requests</h3><div id="wdList"></div></div></div>
<div id="a-tasks" class="tab"><div class="card"><h3>🎯 Tasks</h3><input id="tTitle" placeholder="Task Title"><input id="tReward" type="number" placeholder="Reward"><input id="tLink" placeholder="Link"><button class="btn" onclick="addTask()">Add Task</button><div id="taskAdminList"></div></div></div>
<div id="a-set" class="tab"><div class="card"><h3>⚙️ Settings - Zone 11764581</h3><p>Ad Zone: <b>11764581</b> | App ID: 3485122</p>App Name: <input id="appName"><br>Logo URL: <input id="logoUrl"><br>Banner Color: <input id="bannerColor"><br>Ad Reward: <input id="adReward" type="number"><br>Min Withdraw: <input id="minW" type="number"><br><button class="btn" onclick="saveSet()">Save Settings</button></div></div>

<script>
let aid=new URLSearchParams(location.search).get('id')||'8807178385';
function goA(t){ document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on')); document.getElementById('a-'+t).classList.add('on'); document.querySelectorAll('.tab-btn').forEach(x=>x.classList.remove('on')); event.target.classList.add('on'); if(t=='users'||t=='wd'||t=='dash') loadAdmin(); }
function loadAdmin(){ fetch(`/api/admin_full?id=${aid}`).then(r=>r.json()).then(d=>{ document.getElementById('tu').innerText=Object.keys(d.users).length; document.getElementById('tw').innerText=d.withdraws.length; let ul=document.getElementById('uList'); ul.innerHTML=''; Object.entries(d.users).forEach(([id,u])=>{ ul.innerHTML+=`<tr><td>${id}</td><td>${u.balance}</td><td>${u.ads_watched||0}</td><td><button onclick="ban('${id}')">Ban</button></td></tr>`; }); let wl=document.getElementById('wdList'); wl.innerHTML=''; d.withdraws.forEach((w,i)=>{ wl.innerHTML+=`<div style="border:1px solid #ddd;padding:8px;margin:4px 0;border-radius:8px">${w.uid} - ${w.num} - ৳${w.amt} - ${w.date} <button onclick="approveWd(${i})" style="background:#16a34a;color:#fff;border:none;padding:4px 8px;border-radius:4px">Approve</button></div>`; }); let sl=document.getElementById('sliderList'); sl.innerHTML=''; d.slider.forEach((s,i)=>{ sl.innerHTML+=`<div style="border:1px solid #ddd;padding:8px;margin:6px 0;border-radius:10px"><img src="${s.img}" style="width:100%;height:90px;object-fit:cover;border-radius:8px"><p style="font-weight:bold;font-size:12px">${s.title||''}</p><p style="font-size:10px">${s.link}</p><button onclick="delSlider(${i})" style="background:#ef4444;color:#fff;border:none;padding:6px 12px;border-radius:6px;margin-top:6px">Delete Ad</button></div>`; }); let tl=document.getElementById('taskAdminList'); tl.innerHTML=''; d.tasks.forEach(t=>{ tl.innerHTML+=`<div style="border:1px solid #ddd;padding:6px;margin:4px 0;border-radius:6px">${t.title} - ৳${t.reward} <button onclick="delTask(${t.id})">Del</button></div>`; }); document.getElementById('appName').value=d.settings.app_name; document.getElementById('logoUrl').value=d.settings.logo_url; document.getElementById('bannerColor').value=d.settings.banner_color; document.getElementById('adReward').value=d.settings.ad_reward; document.getElementById('minW').value=d.settings.min_withdraw; }); }
function addSlider(){ let img=document.getElementById('sImg').value; let link=document.getElementById('sLink').value; let title=document.getElementById('sTitle').value; if(!img) return alert('Image URL দাও'); fetch(`/api/add_slider?id=${aid}&img=${encodeURIComponent(img)}&link=${encodeURIComponent(link)}&title=${encodeURIComponent(title)}`).then(r=>r.json()).then(d=>{ alert(d.msg); loadAdmin(); document.getElementById('sImg').value=''; document.getElementById('sLink').value=''; document.getElementById('sTitle').value=''; }); }
function delSlider(i){ fetch(`/api/del_slider?id=${aid}&idx=${i}`).then(r=>r.json()).then(d=>{ loadAdmin(); }); }
function addTask(){ let t=document.getElementById('tTitle').value; let r=document.getElementById('tReward').value; let l=document.getElementById('tLink').value; fetch(`/api/add_task?id=${aid}&title=${encodeURIComponent(t)}&reward=${r}&link=${encodeURIComponent(l)}`).then(r=>r.json()).then(d=>{ alert(d.msg); loadAdmin(); }); }
function delTask(id){ fetch(`/api/del_task?id=${aid}&task_id=${id}`).then(r=>r.json()).then(d=>loadAdmin()); }
function saveSet(){ let an=document.getElementById('appName').value; let lo=document.getElementById('logoUrl').value; let bc=document.getElementById('bannerColor').value; let ar=document.getElementById('adReward').value; let mw=document.getElementById('minW').value; fetch(`/api/save_settings?id=${aid}&app_name=${encodeURIComponent(an)}&logo_url=${encodeURIComponent(lo)}&banner_color=${encodeURIComponent(bc)}&ad_reward=${ar}&min_withdraw=${mw}`).then(r=>r.json()).then(d=>alert('Saved - Zone 11764581 Active')); }
function ban(id){ fetch(`/api/ban_user?id=${aid}&uid=${id}`).then(r=>r.json()).then(d=>{ alert(d.msg); loadAdmin(); }); }
function approveWd(i){ fetch(`/api/approve_wd?id=${aid}&idx=${i}`).then(r=>r.json()).then(d=>{ alert(d.msg); loadAdmin(); }); }
loadAdmin();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin(): return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385'); ref=request.args.get('ref'); db=load_db()
    if uid not in db['users']:
        db['users'][uid]={'balance':0,'ads_watched':0,'last_daily':'','ref_by':ref}
        if ref and ref in db['users']: db['users'][ref]['balance']=db['users'][ref].get('balance',0)+db['settings']['ref_bonus']
        save_db(db)
    return jsonify({"user":db['users'][uid],"settings":db['settings'],"slider":db['slider'],"tasks":db['tasks'],"banned": uid in db['banned']})

@app.route('/api/admin_full')
def admin_full():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"error":"unauth"})
    db=load_db(); return jsonify(db)

@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); db=load_db()
    if uid not in db['users']: db['users'][uid]={'balance':0,'ads_watched':0,'last_daily':''}
    if db['users'][uid].get('ads_watched',0)>=db['settings']['ad_daily_limit']: return jsonify({"ok":False,"msg":"Daily Limit শেষ"})
    db['users'][uid]['balance']+=db['settings']['ad_reward']; db['users'][uid]['ads_watched']=db['users'][uid].get('ads_watched',0)+1; save_db(db)
    return jsonify({"ok":True,"reward":db['settings']['ad_reward']})

@app.route('/api/daily')
def daily():
    uid=request.args.get('id'); db=load_db(); today=str(datetime.date.today())
    if db['users'][uid].get('last_daily')==today: return jsonify({"ok":False,"msg":"আজ বোনাস নিয়েছো"})
    db['users'][uid]['balance']+=db['settings']['daily_checkin_reward']; db['users'][uid]['last_daily']=today; save_db(db); return jsonify({"ok":True,"msg":f"✅ ৳{db['settings']['daily_checkin_reward']} Daily Bonus!"})

@app.route('/api/withdraw')
def wd():
    uid=request.args.get('id'); num=request.args.get('num'); amt=int(request.args.get('amt') or 0); db=load_db()
    if db['users'][uid]['balance']<amt: return jsonify({"ok":False,"msg":"❌ Balance কম"})
    if amt<db['settings']['min_withdraw']: return jsonify({"ok":False,"msg":f"❌ Min {db['settings']['min_withdraw']}"})
    db['users'][uid]['balance']-=amt; db['withdraws'].append({"uid":uid,"num":num,"amt":amt,"date":str(datetime.datetime.now())[:19]}); save_db(db); return jsonify({"ok":True,"msg":"✅ Withdraw Request Sent - 24h এ Payment"})

@app.route('/api/add_slider')
def add_s():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db(); db['slider'].append({"img":request.args.get('img'),"link":request.args.get('link'),"title":request.args.get('title','')}); save_db(db); return jsonify({"ok":True,"msg":"✅ নিজের বিজ্ঞাপন Add হলো! 3.5s পর পর দেখাবে"})

@app.route('/api/del_slider')
def del_s():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db(); idx=int(request.args.get('idx')); db['slider'].pop(idx); save_db(db); return jsonify({"ok":True})

@app.route('/api/add_task')
def add_task():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db(); nid=max([t['id'] for t in db['tasks']], default=0)+1; db['tasks'].append({"id":nid,"title":request.args.get('title'),"reward":int(request.args.get('reward') or 0),"link":request.args.get('link'),"color":"#065f46","btn":"শুরু","type":"youtube","desc":"Task Complete"}); save_db(db); return jsonify({"ok":True,"msg":"Task Added"})

@app.route('/api/del_task')
def del_task():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db(); tid=int(request.args.get('task_id')); db['tasks']=[t for t in db['tasks'] if t['id']!=tid]; save_db(db); return jsonify({"ok":True})

@app.route('/api/save_settings')
def save_set():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db()
    for k in ['app_name','logo_url','banner_color']:
        if request.args.get(k): db['settings'][k]=request.args.get(k)
    if request.args.get('ad_reward'): db['settings']['ad_reward']=int(request.args.get('ad_reward'))
    if request.args.get('min_withdraw'): db['settings']['min_withdraw']=int(request.args.get('min_withdraw'))
    save_db(db); return jsonify({"ok":True})

@app.route('/api/ban_user')
def ban_u():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db(); uid=request.args.get('uid');
    if uid in db['banned']: db['banned'].remove(uid)
    else: db['banned'].append(uid)
    save_db(db); return jsonify({"ok":True,"msg":"Ban Toggled"})

@app.route('/api/approve_wd')
def approve_wd():
    if request.args.get('id')!=str(ADMIN_ID): return jsonify({"ok":False})
    db=load_db(); idx=int(request.args.get('idx')); db['withdraws'].pop(idx); save_db(db); return jsonify({"ok":True,"msg":"Approved - Payment Done"})

@app.route('/api/task_complete')
def task_complete():
    uid=request.args.get('id'); tid=int(request.args.get('task_id')); db=load_db()
    task=next((t for t in db['tasks'] if t['id']==tid), None)
    if task: db['users'][uid]['balance']+=task['reward']; save_db(db); return jsonify({"ok":True,"reward":task['reward']})
    return jsonify({"ok":False})

def run_bot():
    async def start(u:Update,c:ContextTypes.DEFAULT_TYPE):
        uid=str(u.effective_user.id); db=load_db()
        if uid not in db['users']: db['users'][uid]={'balance':0,'ads_watched':0,'last_daily':''}; save_db(db)
        kb=[[InlineKeyboardButton("🚀 Open App - Zone 11764581 Ready", web_app={"url": f"https://am-bot-1-v77g.onrender.com/?id={uid}"})],[InlineKeyboardButton("📢 Channel", url="https://t.me/ProtidinerKajBD")]]
        await u.message.reply_text(f"✅ Welcome {u.effective_user.first_name}\n\nZone 11764581 Active - Company Ad Ready\nনিজের Ad লিখতে পারবা Admin Panel এ", reply_markup=InlineKeyboardMarkup(kb))
    async def run():
        app_tg=Application.builder().token(BOT_TOKEN).build(); app_tg.add_handler(CommandHandler("start",start)); await app_tg.initialize(); await app_tg.start(); await app_tg.updater.start_polling(); await app_tg.updater.idle()
    import asyncio; asyncio.run(run())

if __name__=='__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000))),daemon=True).start()
    try: run_bot()
    except: app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
