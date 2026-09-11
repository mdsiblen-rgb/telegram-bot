from flask import Flask, request, jsonify
import json, os, time
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"
ADMIN_ID = "8807178385"

DEFAULT_DB = {
    "users": {},
    "withdraws": [],
    "settings": {
        "app_name": "Protidiner Kaj BD",
        "theme": "#6C5CE7",
        "welcome": 10,
        "ref_bonus": 10,
        "ad_reward": 1,
        "ad_limit": 30,
        "min_wd": 200,
        "bot_username": "ProtidinerKaj_BD_Bot",
        "channel_username": "ProtidinerKajBD",
        "group_link": "+hb8X-V4buToxYmJl",
        "admin_username": "ProtidinerKajBD",
        "video_link": "https://t.me/ProtidinerKajBD",
        "notice_title": "Communitytask",
        "notice_text": "✨ আমাদের প্ল্যাটফর্মে ইনকাম করা এখন আগের চেয়ে আরও সহজ ও বিশ্বাসযোগ্য।\n🚀 ঘরে বসেই অল্প সময় দিয়ে আয় করার দারুণ সুযোগ।\n👉 দ্রুত পেমেন্ট সিস্টেম।\n🌟 নতুনদের জন্য সহজ এবং সবার জন্য লাভজনক একটি প্ল্যাটফর্ম।\n💸 প্রতিটি রেফারে পাবেন 10 টাকা।\n📺 প্রতিটি বিজ্ঞাপন দেখলে পাবেন 1 টাকা।\n🎁 একাউন্ট খুললেই সাথে সাথে 10 টাকা বোনাস।\n🏦 200 টাকা হলেই উইথড্র করতে পারবেন বিকাশ ও নগদের মাধ্যমে।( সম্পূর্ণ অটোমেশন সিস্টেম)",
        "tasks": [
            {"id": "yt", "title": "YouTube video", "reward": 25, "icon": "youtube", "link": "https://youtube.com"},
            {"id": "tg", "title": "Join telegram", "reward": 10, "icon": "telegram", "link": "https://t.me/ProtidinerKajBD"}
        ]
    }
}

def load_db():
    if not os.path.exists(DB_FILE): return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE,"r",encoding="utf-8") as f:
            db=json.load(f)
            for k in DEFAULT_DB:
                if k not in db: db[k]=DEFAULT_DB[k]
            for k in DEFAULT_DB["settings"]:
                if k not in db["settings"]: db["settings"][k]=DEFAULT_DB["settings"][k]
            return db
    except: return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    db=load_db(); s=db["settings"]
    return f"""
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['app_name']}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<!-- ✅ YOUR MONETAG COMPANY CODE - ZONE 11764581 CONNECTED -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
:root{{--t:{s['theme']}}}; *{{font-family:system-ui}} body{{margin:0;background:#f5f7fb;padding-bottom:85px}}
.topbar{{background:#b8f0e8;display:flex;align-items:center;justify-content:space-between;padding:12px 15px;position:sticky;top:0;z-index:100}}
.header{{background:var(--t);color:white;padding:14px 15px;display:flex;align-items:center;gap:12px}}
.avatar{{width:52px;height:52px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--t);font-weight:bold;font-size:22px}}
.card{{background:white;border-radius:22px;padding:15px;margin:12px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}}
.balance-big{{font-size:42px;font-weight:800;color:var(--t);text-align:center}}
.ref-box{{background:#f1f5f4;border:1px solid #ddd;border-radius:14px;padding:12px;display:flex;justify-content:space-between;align-items:center;margin:10px 0;word-break:break-all}}
.green-btn{{background:var(--t);color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;font-size:16px;cursor:pointer}}
.dark-card{{background:#1a3c34;color:white;border-radius:22px;padding:18px;margin:12px}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #e5e7eb;z-index:100}}
.b-item{{text-align:center;font-size:11px;color:#9ca3af;cursor:pointer;flex:1}}.b-item.active{{color:var(--t)}}.b-item i{{font-size:22px;display:block;margin-bottom:2px}}
.page{{display:none}}.page.active{{display:block}}
.ad-card{{background:var(--t);color:white;border-radius:26px;padding:20px;text-align:center;margin:12px}}
.task-row{{display:flex;justify-content:space-between;align-items:center;padding:14px;background:white;border-radius:18px;margin:10px 12px}}
.method{{border:2px solid #e5e7eb;border-radius:16px;padding:12px;text-align:center;flex:1;cursor:pointer}}.method.sel{{border-color:var(--t);background:#f0efff}}
.w-input{{width:92%;padding:14px;border:1px solid #ddd;border-radius:14px;margin:6px 0}}
.support-row{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:white;border-radius:18px;margin:10px 12px;cursor:pointer}}
#topMenu{{position:absolute;top:50px;right:10px;background:white;border-radius:14px;box-shadow:0 8px 25px rgba(0,0,0,0.15);padding:8px 0;width:180px;display:none;z-index:200}}
#topMenu div{{padding:12px 16px;font-size:13px;cursor:pointer}} #topMenu div:hover{{background:#f3f4f6}}
</style></head><body>

<div class="topbar">
<i class="fa-solid fa-xmark" onclick="if(window.Telegram.WebApp) Telegram.WebApp.close(); else window.close();" style="cursor:pointer;font-size:20px"></i>
<b>{s['app_name']} - ✅ Monetag Connected</b>
<div style="display:flex;gap:14px;align-items:center">
<i class="fa-solid fa-chevron-down" onclick="toggleMenu()" style="cursor:pointer"></i>
<i class="fa-solid fa-ellipsis-vertical" onclick="toggleMenu()" style="cursor:pointer"></i>
</div>
<div id="topMenu">
<div onclick="alert('📢 {s['notice_text'].replace(chr(10),' ')}')"><i class="fa-solid fa-circle-info"></i> Rules</div>
<div onclick="window.open('https://t.me/{s['channel_username']}','_blank')"><i class="fa-brands fa-telegram"></i> Official Channel</div>
<div onclick="window.open('https://t.me/{s['bot_username']}','_blank')"><i class="fa-solid fa-robot"></i> Support</div>
<div onclick="toggleMenu()"><i class="fa-solid fa-xmark"></i> Close</div>
</div>
</div>

<div class="header"><div class="avatar">৳</div><div><div id="uName" style="font-weight:bold">User</div><div id="uBal" style="font-size:14px;opacity:0.9">৳0.00</div></div><i class="fa-solid fa-circle-check" style="margin-left:auto;background:rgba(255,255,255,0.25);padding:8px;border-radius:50%"></i></div>

<div id="p1" class="page active">
<div class="card"><div class="balance-big" id="mainBal">৳0.00</div><div style="text-align:center;font-size:12px;color:#888">বর্তমান ব্যালেন্স</div></div>
<div style="padding:0 12px;color:#6b7280;font-size:13px">আপনার রেফারাল লিংক:</div>
<div class="ref-box"><div id="refLink" style="font-size:13px">https://t.me/{s['bot_username']}?start=...</div><div style="border:1px solid #ddd;padding:8px;border-radius:8px;cursor:pointer" onclick="copyRef()"><i class="fa-regular fa-copy"></i></div></div>
<button class="green-btn" style="margin:0 12px;width:calc(100% - 24px)" onclick="shareRef()">🔗 রেফার লিংক শেয়ার করুন</button>
<div class="dark-card">
<div style="font-weight:bold;margin-bottom:10px">📢 অফিশিয়াল নোটিশ</div>
<div style="background:#2d4a44;border-radius:12px;padding:10px;display:flex;align-items:center;gap:8px;margin-bottom:12px">🪙 {s['notice_title']} - Zone 11764581 Active</div>
<div style="font-size:13px;line-height:22px;white-space:pre-line;background:#2a4e47;padding:14px;border-radius:14px">{s['notice_text']}</div>
<div style="text-align:center;margin-top:12px">👉 আয় শুরু করুন আজ থেকেই 💚</div>
</div>
</div>

<div id="p2" class="page">
<div class="ad-card">
<div style="font-size:14px;opacity:0.9">প্রতি বিজ্ঞাপনে নিশ্চিত আয়</div>
<div style="font-size:52px;font-weight:800;margin:5px 0">৳{s['ad_reward']}.00</div>
<div style="display:flex;gap:10px;margin-top:15px">
<div style="flex:1;background:rgba(255,255,255,0.18);padding:10px;border-radius:14px"><div style="font-size:12px">আজকের বিজ্ঞাপন দেখা</div><div style="font-size:20px;font-weight:bold;margin-top:4px"><span id="todayAds">0</span> টি</div></div>
<div style="flex:1;background:rgba(255,255,255,0.18);padding:10px;border-radius:14px"><div style="font-size:12px">আজকের বিজ্ঞাপন আয়</div><div style="font-size:20px;font-weight:bold;margin-top:4px">৳ <span id="todayEarn">0.00</span></div></div>
</div>
<button id="adBtn" onclick="watchAd()" style="background:white;color:var(--t);border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;margin-top:15px;cursor:pointer">▶ বিজ্ঞাপন শুরু করুন (<span id="leftAds">{s['ad_limit']}</span> টি বাকি | আজ <span id="progTxt">0/{s['ad_limit']}</span>)</button>
<div style="font-size:11px;margin-top:8px;opacity:0.8">✅ Connected: Monetag Zone 11764581 - Your Earnings $0.02</div>
</div>
<div id="taskList"></div>
</div>

<div id="p3" class="page">
<div class="support-row" onclick="openLink('https://t.me/{s['bot_username']}?start={ADMIN_ID}')"><div style="display:flex;gap:12px;align-items:center"><div style="background:#0ea5e9;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center"><i class="fa-brands fa-telegram"></i></div><div><b>Admin কে Message করুন</b><div style="font-size:12px;color:#888">@{s['bot_username']}</div></div></div><i class="fa-solid fa-arrow-right" style="color:var(--t)"></i></div>
<div class="support-row" onclick="openLink('https://t.me/{s['channel_username']}')"><div style="display:flex;gap:12px;align-items:center"><div style="background:#0ea5e9;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center"><i class="fa-brands fa-telegram"></i></div><div><b>অফিশিয়াল চ্যানেল</b><div style="font-size:12px;color:#888">@{s['channel_username']}</div></div></div><i class="fa-solid fa-arrow-right" style="color:var(--t)"></i></div>
<div style="background:#ef4444;color:white;border-radius:20px;padding:16px;margin:12px;display:flex;justify-content:space-between;align-items:center;cursor:pointer" onclick="openLink('{s['video_link']}')"><div style="display:flex;gap:12px;align-items:center"><div style="background:#fbbf24;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center">▶️</div><div><b>কিভাবে কাজ করবেন?</b><div style="font-size:12px">ভিডিও দেখুন এবং সহজেই শিখুন</div></div></div><i class="fa-solid fa-arrow-right"></i></div>
</div>

<div id="p4" class="page">
<div style="background:var(--t);color:white;border-radius:0 0 28px 28px;padding:25px;text-align:center">
<div style="font-size:13px;opacity:0.9">আপনার ব্যালেন্স</div>
<div style="font-size:48px;font-weight:800" id="wBalBig">৳0.00</div>
<div style="display:flex;gap:10px;justify-content:center;margin-top:10px">
<div style="background:rgba(255,255,255,0.25);padding:6px 14px;border-radius:20px;font-size:12px">মিনিমাম: ৳{s['min_wd']}.00</div>
<div style="background:rgba(255,255,255,0.25);padding:6px 14px;border-radius:20px;font-size:12px">• ৳<span id="remain">0</span> বাকি</div>
</div>
</div>
<div class="card">
<div style="background:var(--t);color:white;margin:-15px -15px 15px -15px;padding:12px 15px;border-radius:22px 22px 0 0;display:flex;gap:10px;align-items:center"><div style="background:rgba(255,255,255,0.25);padding:8px;border-radius:10px">💳</div><div><b>টাকা উত্তোলন</b><div style="font-size:12px;opacity:0.9">BKash / Nagad এ পেমেন্ট পান</div></div></div>
<div style="font-size:13px;color:#6b7280;margin-bottom:8px">পেমেন্ট মেথড</div>
<div style="display:flex;gap:10px">
<div class="method sel" id="bkM" onclick="setM('Bkash')"><div style="font-size:28px">◆</div><div>Bkash</div><div style="color:var(--t);font-size:11px;margin-top:4px" id="bkT">✓ Selected</div></div>
<div class="method" id="ngM" onclick="setM('Nagad')"><div style="font-size:28px">◎</div><div>Nagad</div><div style="font-size:11px;margin-top:4px" id="ngT">Tap to select</div></div>
</div>
<div style="margin-top:12px;font-size:13px">📞 একাউন্ট নম্বর</div>
<input id="wNum" class="w-input" placeholder="01XXXXXXXXX">
<div style="font-size:13px">💵 টাকার পরিমাণ</div>
<input id="wAmt" type="number" class="w-input" placeholder="৳ 0.00">
<div style="font-size:11px;color:#888">মিনিমাম: ৳{s['min_wd']}.00</div>
<button id="wdBtn" onclick="withdraw()" style="background:#9ca3af;color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;margin-top:12px;cursor:pointer">• ব্যালেন্স যথেষ্ট নয়</button>
</div>
<div style="padding:0 12px"><b>🕒 উইথড্র হিস্ট্রি</b><div id="wHist" style="text-align:center;padding:30px;color:#888">কোন উইথড্র হিস্ট্রি নেই</div></div>
</div>

<div id="p5" class="page">
<div style="background:var(--t);border-radius:22px;padding:18px;margin:12px;display:flex;gap:15px;align-items:center;color:white">
<div class="avatar" style="width:60px;height:60px">৳</div><div><div style="font-size:18px;font-weight:bold" id="pName">USER</div><div style="font-size:12px;opacity:0.8" id="pUser">@user</div><div style="background:rgba(255,255,255,0.25);display:inline-block;padding:3px 10px;border-radius:20px;font-size:12px;margin-top:5px">ID: <span id="pId">00000</span></div></div></div>
<div class="card" style="background:var(--t);color:white;display:flex;justify-content:space-between"><div>💼 বর্তমান ব্যালেন্স</div><div style="font-weight:bold;font-size:20px" id="pBal">৳0.00</div></div>
<div class="card" style="background:var(--t);color:white;display:flex;justify-content:space-between"><div>✅ মোট সফল উইথড্র</div><div style="font-weight:bold;font-size:20px" id="pSucc">৳0.00</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 12px">
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">📅 আজকের আয়</div><div style="font-weight:bold;color:var(--t)" id="pToday">৳0.00</div></div>
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">📅 গতকালের আয়</div><div style="font-weight:bold" id="pYes">৳0.00</div></div>
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">▶ মোট বিজ্ঞাপন</div><div style="font-weight:bold;color:var(--t)" id="pAdTotal">0 টি</div></div>
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">👥 মোট রেফার</div><div style="font-weight:bold;color:orange" id="pRefTotal">0 জন</div></div>
</div>
</div>

<div class="bottom">
<div class="b-item active" onclick="nav(1)" id="b1"><i class="fa-solid fa-house"></i>হোম</div>
<div class="b-item" onclick="nav(2)" id="b2"><i class="fa-solid fa-rectangle-list"></i>আয় করুন</div>
<div class="b-item" onclick="nav(3)" id="b3"><i class="fa-solid fa-circle-question"></i>সাপোর্ট</div>
<div class="b-item" onclick="nav(4)" id="b4"><i class="fa-solid fa-credit-card"></i>উইথড্র</div>
<div class="b-item" onclick="nav(5)" id="b5"><i class="fa-solid fa-user"></i>প্রোফাইল</div>
</div>

<script>
let uid="user_"+Math.floor(Math.random()*90000+10000); let uname="User"; let tg=window.Telegram.WebApp;
if(tg.initDataUnsafe?.user){{uid=tg.initDataUnsafe.user.id.toString(); uname=tg.initDataUnsafe.user.first_name;}}
let wMethod="Bkash"; let adLimit={s['ad_limit']};
function toggleMenu(){{let m=document.getElementById('topMenu'); m.style.display=m.style.display==='block'?'none':'block';}}
function nav(n){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active')); document.getElementById('p'+n).classList.add('active'); document.querySelectorAll('.b-item').forEach(b=>b.classList.remove('active')); document.getElementById('b'+n).classList.add('active'); document.getElementById('topMenu').style.display='none';}}
function setM(m){{wMethod=m; document.getElementById('bkM').classList.toggle('sel',m=='Bkash'); document.getElementById('ngM').classList.toggle('sel',m=='Nagad'); document.getElementById('bkT').innerText=m=='Bkash'?'✓ Selected':'Tap to select'; document.getElementById('ngT').innerText=m=='Nagad'?'✓ Selected':'Tap to select';}}
function openLink(u){{if(!u || u===''){{alert('লিংক সেট করা নেই! Admin থেকে সেট করুন'); return;}} window.open(u,'_blank');}}
function copyRef(){{let t=document.getElementById('refLink').innerText; if(navigator.clipboard){{navigator.clipboard.writeText(t).then(()=>alert('✅ কপি হয়েছে!')).catch(()=>{{let i=document.createElement('input'); i.value=t; document.body.appendChild(i); i.select(); document.execCommand('copy'); document.body.removeChild(i); alert('✅ কপি হয়েছে!');}});}} else{{let i=document.createElement('input'); i.value=t; document.body.appendChild(i); i.select(); document.execCommand('copy'); document.body.removeChild(i); alert('✅ কপি হয়েছে!');}}}}
function shareRef(){{let l=document.getElementById('refLink').innerText; if(navigator.share){{navigator.share({{title:'{s['app_name']}',text:l,url:l}}).catch(()=>copyRef());}} else copyRef();}}

async function init(){{
 try{{
 let ref=new URLSearchParams(window.location.search).get("start")||new URLSearchParams(window.location.search).get("ref");
 let res=await fetch("/api/register",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:uid,name:uname,ref:ref}})}});
 let d=await res.json();
 document.getElementById('uName').innerText=d.name||uname; document.getElementById('uBal').innerText='৳'+d.balance.toFixed(2); document.getElementById('mainBal').innerText='৳'+d.balance.toFixed(2);
 document.getElementById('wBalBig').innerText='৳'+d.balance.toFixed(2); document.getElementById('pBal').innerText='৳'+d.balance.toFixed(2);
 document.getElementById('pName').innerText=(d.name||uname).toUpperCase(); document.getElementById('pUser').innerText='@'+uid; document.getElementById('pId').innerText=uid;
 document.getElementById('todayAds').innerText=d.today_ads||0; document.getElementById('todayEarn').innerText=((d.today_ads||0)*{s['ad_reward']}).toFixed(2);
 document.getElementById('leftAds').innerText=adLimit-(d.today_ads||0); document.getElementById('progTxt').innerText=(d.today_ads||0)+'/'+adLimit;
 document.getElementById('pAdTotal').innerText=(d.total_ads||0)+' টি'; document.getElementById('pRefTotal').innerText=(d.ref_count||0)+' জন';
 document.getElementById('pToday').innerText='৳'+((d.today_ads||0)*{s['ad_reward']}).toFixed(2);
 document.getElementById('remain').innerText=Math.max(0,{s['min_wd']}-d.balance).toFixed(2);
 document.getElementById('refLink').innerText='https://t.me/{s['bot_username']}?start='+uid;
 let min={s['min_wd']}; let btn=document.getElementById('wdBtn'); if(d.balance>=min){{btn.style.background='var(--t)'; btn.innerText='উত্তোলন করুন';}} else {{btn.style.background='#9ca3af'; btn.innerText='• ব্যালেন্স যথেষ্ট নয় ( ৳'+(min-d.balance).toFixed(2)+' লাগবে )';}}
 let tHtml=''; let tasks=d.tasks||[]; tasks.forEach(t=>{{ let icon=t.icon=='youtube'?'<div style="background:#e11d48;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center"><i class="fa-brands fa-youtube"></i></div>':'<div style="background:#0ea5e9;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center"><i class="fa-brands fa-telegram"></i></div>';
 tHtml+=`<div class="task-row"><div style="display:flex;gap:10px;align-items:center">${{icon}}<div><b>${{t.title}}</b><div style="color:var(--t);font-weight:bold">৳${{t.reward}}.00</div></div></div><button class="green-btn" style="width:auto;padding:8px 18px" onclick="doTask('${{t.id}}')">শুরু করুন</button></div>`;}});
 document.getElementById('taskList').innerHTML=tHtml;
 if(d.history && d.history.length>0){{let h=''; d.history.slice().reverse().forEach(x=>{{h+=`<div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #eee;font-size:12px'><span>${{x.method}}<br>${{x.number}}</span><span>৳${{x.amount}}</span><span style='color:${{x.status=='PENDING'?'orange':'green'}};font-weight:bold'>${{x.status}}</span></div>`}}); document.getElementById('wHist').innerHTML=h;}}
 }}catch(e){{console.log(e);}}
}}
init();

async function watchAd(){{
 let btn=document.getElementById('adBtn'); let old=btn.innerHTML; btn.innerHTML='⏳ বিজ্ঞাপন লোড হচ্ছে...'; btn.disabled=true;
 try{{
  if(typeof show_11764581==='function'){{
   await show_11764581().then(async ()=>{{
    let r=await fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid}})}});
    let d=await r.json(); if(d.error){{alert(d.error);}} else {{alert('✅ ৳{s['ad_reward']} যোগ হয়েছে!'); init();}}
   }}).catch(async (e)=>{{
    console.log('Ad closed',e);
    let r=await fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid}})}});
    let d=await r.json(); if(!d.error){{alert('✅ ৳{s['ad_reward']} যোগ হয়েছে!'); init();}}
   }});
  }} else {{
   alert('Ad SDK লোড হচ্ছে, ২ সেকেন্ড পর আবার চাপুন...');
   setTimeout(async ()=>{{
     let r=await fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid}})}});
     let d=await r.json(); if(!d.error){{alert('✅ ৳{s['ad_reward']} যোগ হয়েছে! (Test)'); init();}}
   }},2000);
  }}
 }}catch(e){{alert('Ad Error: '+e.message);}}
 btn.innerHTML=old; btn.disabled=false;
}}

async function doTask(id){{
 let r=await fetch('/api/do_task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid,task_id:id}})}});
 let d=await r.json(); if(d.ok){{init(); if(d.link) window.open(d.link,'_blank'); alert('✅ Task Complete! ৳'+d.reward+' পেয়েছেন!');}}
}}
async function withdraw(){{
 let num=document.getElementById('wNum').value.trim(); let amt=parseInt(document.getElementById('wAmt').value);
 if(!num||num.length<11){{alert('সঠিক 11 ডিজিটের নাম্বার দিন');return;}}
 if(!amt||amt<{s['min_wd']}){{alert('মিনিমাম {s['min_wd']} টাকা');return;}}
 let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid,amount:amt,method:wMethod,number:num}})}});
 let d=await r.json(); if(d.ok){{alert('✅ Withdraw Request গেছে! ২৪ ঘন্টায় পাবেন'); init();}} else alert(d.error);
}}
document.addEventListener('click',function(e){{if(!e.target.closest('.topbar')){{document.getElementById('topMenu').style.display='none';}}}});
</script></body></html>
    """

@app.route("/admin")
def admin():
    if request.args.get("id")!=ADMIN_ID: return "Unauthorized - Add?id=8807178385",403
    db=load_db(); s=db["settings"]; tasks_json=json.dumps(s["tasks"],ensure_ascii=False,indent=2)
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Admin</title>
<style>body{{font-family:system-ui;background:#eef2f7;padding:10px}}.card{{background:white;padding:14px;border-radius:16px;margin-bottom:12px}} input,textarea{{width:95%;padding:10px;margin:5px 0;border:1px solid #ddd;border-radius:10px}}.btn{{border:none;padding:10px 14px;border-radius:10px;color:white;cursor:pointer;font-weight:bold}}.save{{background:{s['theme']};width:100%;padding:14px}} table{{width:100%;border-collapse:collapse}} th{{background:#1f2937;color:white;padding:8px;font-size:11px}} td{{padding:7px;border-bottom:1px solid #eee;font-size:11px;text-align:center}}.tab{{display:inline-block;padding:7px 12px;background:#dfe6e9;border-radius:20px;margin:3px;cursor:pointer;font-size:12px}}.tab.active{{background:{s['theme']};color:white}}</style>
</head><body>
<h2>👑 ADMIN - {s['app_name']} - ✅ 11764581 Connected</h2>
<div class="card"><div class="tab active" onclick="showT('set')" id="t1">⚙️ Settings</div><div class="tab" onclick="showT('ad')" id="t2">📺 Ads Edit</div><div class="tab" onclick="showT('users')" id="t3">👥 Users</div><div class="tab" onclick="showT('wd')" id="t4">💸 Withdraw</div></div>
<div id="tab-set" class="card"><h3>Full Control - Monetag ID 11764581 Active</h3>
App Name:<input id="app_name" value="{s['app_name']}">
Theme:<input id="theme" value="{s['theme']}">
Welcome:<input id="welcome" type="number" value="{s['welcome']}">
Ref Bonus:<input id="ref_bonus" type="number" value="{s['ref_bonus']}">
Ad Reward:<input id="ad_reward" type="number" value="{s['ad_reward']}">
Ad Limit:<input id="ad_limit" type="number" value="{s['ad_limit']}">
Min WD:<input id="min_wd" type="number" value="{s['min_wd']}">
Bot Username:<input id="bot_username" value="{s['bot_username']}">
Channel Username:<input id="channel_username" value="{s['channel_username']}">
Group Link:<input id="group_link" value="{s['group_link']}">
Video Link:<input id="video_link" value="{s['video_link']}">
Notice Text:<textarea id="notice_text" rows="6">{s['notice_text']}</textarea>
<button class="btn save" onclick="saveSet()">💾 Save All</button></div>
<div id="tab-ad" class="card" style="display:none"><h3>📺 বিজ্ঞাপন Task Edit</h3><textarea id="tasks" rows="10" style="font-family:monospace">{tasks_json}</textarea><button class="btn save" onclick="saveTasks()">📺 Update Ads</button></div>
<div id="tab-users" class="card" style="display:none"><h3>Users</h3><table><tr><th>ID</th><th>Name</th><th>Bal</th><th>Ref</th><th>Ads</th><th>Action</th></tr><tbody id="users"></tbody></table></div>
<div id="tab-wd" class="card" style="display:none"><h3>Withdraw</h3><table><tr><th>User</th><th>Method</th><th>Number</th><th>Amt</th><th>Status</th><th>Action</th></tr><tbody id="wds"></tbody></table></div>
<script>
function showT(t){{document.getElementById('tab-set').style.display=t=='set'?'block':'none';document.getElementById('tab-ad').style.display=t=='ad'?'block':'none';document.getElementById('tab-users').style.display=t=='users'?'block':'none';document.getElementById('tab-wd').style.display=t=='wd'?'block':'none';document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById('t'+(t=='set'?1:t=='ad'?2:t=='users'?3:4)).classList.add('active'); if(t!='set') load();}}
async function load(){{let r=await fetch('/api/admin/data?id={ADMIN_ID}'); let db=await r.json(); let u=''; for(let id in db.users){{let x=db.users[id]; u+=`<tr><td>${{x.id.slice(-6)}}</td><td>${{x.name||''}}</td><td>${{x.balance}}</td><td>${{x.ref_count}}</td><td>${{x.today_ads||0}}</td><td><button class="btn" style="background:#10b981" onclick="editU('${{x.id}}')">Edit</button></td></tr>`}} document.getElementById('users').innerHTML=u; let w=''; db.withdraws.slice().reverse().forEach(o=>{{w+=`<tr><td>${{o.user.slice(-6)}}<br>${{o.name}}</td><td>${{o.method}}</td><td>${{o.number}}</td><td>${{o.amount}}</td><td>${{o.status}}</td><td><button class="btn" style="background:#0ea5e9" onclick="approve('${{o.id}}')">Approve</button></td></tr>`}}); document.getElementById('wds').innerHTML=w;}}
async function saveSet(){{let d={{app_name:document.getElementById('app_name').value,theme:document.getElementById('theme').value,welcome:parseInt(document.getElementById('welcome').value),ref_bonus:parseInt(document.getElementById('ref_bonus').value),ad_reward:parseInt(document.getElementById('ad_reward').value),ad_limit:parseInt(document.getElementById('ad_limit').value),min_wd:parseInt(document.getElementById('min_wd').value),bot_username:document.getElementById('bot_username').value,channel_username:document.getElementById('channel_username').value,group_link:document.getElementById('group_link').value,video_link:document.getElementById('video_link').value,notice_text:document.getElementById('notice_text').value}}; await fetch('/api/admin/settings',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}}); alert('✅ Saved!'); location.reload();}}
async function saveTasks(){{let t=JSON.parse(document.getElementById('tasks').value); await fetch('/api/admin/tasks',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{tasks:t}})}}); alert('✅ Ads Updated!');}}
async function editU(id){{let b=prompt('New Balance?'); if(b===null) return; await fetch('/api/admin/edit',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:id,balance:b}})}}); load();}}
async function approve(id){{await fetch('/api/admin/approve_wd',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:id}})}}); load();}}
load();
</script></body></html>
    """

@app.route("/api/admin/data")
def admin_data():
    if request.args.get("id")!=ADMIN_ID: return jsonify({"error":"Unauth"}),403
    return jsonify(load_db())

@app.route("/api/admin/settings", methods=["POST"])
def admin_settings():
    db=load_db()
    for k,v in request.json.items(): db["settings"][k]=v
    save_db(db); return jsonify({"ok":True})

@app.route("/api/admin/tasks", methods=["POST"])
def admin_tasks():
    db=load_db(); db["settings"]["tasks"]=request.json.get("tasks",[]); save_db(db); return jsonify({"ok":True})

@app.route("/api/admin/edit", methods=["POST"])
def admin_edit():
    db=load_db(); uid=request.json.get("user_id")
    if uid in db["users"]: db["users"][uid]["balance"]=int(request.json.get("balance")); save_db(db)
    return jsonify({"ok":True})

@app.route("/api/admin/approve_wd", methods=["POST"])
def approve_wd():
    db=load_db(); wid=request.json.get("id")
    for w in db["withdraws"]:
        if w["id"]==wid: w["status"]="APPROVED"
    save_db(db); return jsonify({"ok":True})

@app.route("/api/register", methods=["POST"])
def register():
    data=request.json; uid=str(data.get("user_id")); db=load_db(); s=db["settings"]
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":data.get("name","User"),"balance":s["welcome"],"total":s["welcome"],"ref_count":0,"today_ads":0,"total_ads":0,"last_date":datetime.now().strftime("%d/%m/%Y"),"ref_by":data.get("ref")}
        ref=data.get("ref")
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["balance"]+=s["ref_bonus"]; db["users"][ref]["total"]+=s["ref_bonus"]; db["users"][ref]["ref_count"]+=1
        save_db(db)
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y"); save_db(db)
    u["history"]=[w for w in db["withdraws"] if w["user"]==uid][-10:]
    u["tasks"]=s["tasks"]
    return jsonify(u)

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid=str(request.json.get("user_id")); db=load_db(); s=db["settings"]
    if uid not in db["users"]: return jsonify({"error":"not found"}),404
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y")
    if u.get("today_ads",0)>=s["ad_limit"]: return jsonify({"error":f"আজ {s['ad_limit']} টা শেষ! কাল আবার"}),400
       u["balance"]+=s["ad_reward"]; u["total"]+=s["ad_reward"]; u["today_ads"]=u.get("today_ads",0)+1; u["total_ads"]=u.get("total_ads",0)+1; u["last_ads_time"]=datetime.now().strftime("%d/%m %I:%M %p"); save_db(db); return jsonify(u)
@app.route("/api/do_task", methods=["POST"])
def do_task():
    uid=str(request.json.get("user_id")); tid=request.json.get("task_id"); db=load_db()
    if uid not in db["users"]: return jsonify({"error":"no"}),404
    task=next((t for t in db["settings"]["tasks"] if t["id"]==tid), None)
    if not task: return jsonify({"ok":False}),404
    db["users"][uid]["balance"]+=task["reward"]; db["users"][uid]["total"]+=task["reward"]; save_db(db)
    return jsonify({"ok":True,"link":task.get("link"),"reward":task.get("reward")})

@app.route("/api/withdraw", methods=["POST"])
def withdraw_req():
    uid=str(request.json.get("user_id")); amt=int(request.json.get("amount",0)); method=request.json.get("method","Bkash"); number=request.json.get("number","")
    db=load_db(); s=db["settings"]
    if uid not in db["users"]: return jsonify({"error":"User not found"}),404
    if amt < s["min_wd"]: return jsonify({"error":f"Min {s['min_wd']} টাকা"}),400
    if db["users"][uid]["balance"] < amt: return jsonify({"error":"Balance কম"}),400
    if len(number)<11: return jsonify({"error":"নাম্বার ভুল"}),400
    db["users"][uid]["balance"]-=amt
    db["withdraws"].append({"id":str(int(time.time()*1000)),"user":uid,"name":db["users"][uid].get("name",""),"amount":amt,"method":method,"number":number,"status":"PENDING","date":datetime.now().strftime("%d/%m/%Y")})
    save_db(db); return jsonify({"ok":True})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
