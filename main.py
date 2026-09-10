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
        "theme": "#0f766e",
        "welcome": 150,
        "ref_bonus": 180,
        "ad_reward": 15,
        "ad_limit": 12,
        "min_wd": 1000,
        "notice_title": "অফিশিয়াল নোটিশ",
        "notice_text": "✨ আমাদের প্ল্যাটফর্মে ইনকাম করা এখন আগের চেয়ে আরও সহজ ও বিশ্বাসযোগ্য।\n🚀 ঘরে বসেই অল্প সময় দিয়ে আয় করার দারুণ সুযোগ।\n👉 দ্রুত পেমেন্ট সিস্টেম।\n🌟 নতুনদের জন্য সহজ এবং সবার জন্য লাভজনক একটি প্ল্যাটফর্ম।\n💸 প্রতিটি রেফারে পাবেন 180 টাকা।\n📺 প্রতিটি বিজ্ঞাপন দেখলে পাবেন 15 টাকা।\n🎁 একাউন্ট খুললেই সাথে সাথে 150 টাকা বোনাস।\n🏦 1000 টাকা হলেই উইথড্র করতে পারবেন বিকাশ ও নগদের মাধ্যমে।( সম্পূর্ণ অটোমেশন সিস্টেম)",
        "admin_username": "@PAYMENT_ADMIN_C_TASK",
        "channel_username": "@ctask247",
        "video_link": "https://youtube.com",
        "tasks": [
            {"id": "yt", "title": "YouTube video", "reward": 25, "icon": "youtube", "link": "https://youtube.com"},
            {"id": "tg", "title": "Join telegram", "reward": 10, "icon": "telegram", "link": "https://t.me/ctask247"}
        ]
    }
}

def load_db():
    if not os.path.exists(DB_FILE): return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
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
<script src='//libtl.com/sdk.js' data-zone='11760259' data-sdk='show_11760259'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
:root{{--t:{s['theme']}}}; *{{font-family:system-ui}} body{{margin:0;background:#eef8f6;padding-bottom:80px}}
.topbar{{background:#b2e2dc;display:flex;align-items:center;justify-content:space-between;padding:12px 15px;position:sticky;top:0;z-index:10}}
.header{{background:var(--t);color:white;padding:15px;display:flex;align-items:center;gap:12px}}
.avatar{{width:50px;height:50px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--t);font-weight:bold;font-size:20px}}
.card{{background:white;border-radius:22px;padding:15px;margin:12px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}}
.balance-big{{font-size:42px;font-weight:800;color:{s['theme']};text-align:center}}
.ref-box{{background:#f1f5f4;border:1px solid #ddd;border-radius:14px;padding:12px;display:flex;justify-content:space-between;align-items:center;margin:10px 0}}
.green-btn{{background:var(--t);color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;font-size:16px}}
.dark-card{{background:#1a3c34;color:white;border-radius:22px;padding:18px;margin:12px}}
.notice-head{{background:#2d4a44;border-radius:12px;padding:10px;display:flex;align-items:center;gap:8px;margin-bottom:12px}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #e5e7eb;z-index:100}}
.b-item{{text-align:center;font-size:11px;color:#9ca3af;cursor:pointer}}.b-item.active{{color:var(--t)}}.b-item i{{font-size:22px;display:block;margin-bottom:2px}}
.page{{display:none}}.page.active{{display:block}}
.ad-card{{background:var(--t);color:white;border-radius:26px;padding:20px;text-align:center;margin:12px}}
.task-row{{display:flex;justify-content:space-between;align-items:center;padding:14px;background:white;border-radius:18px;margin:10px 12px}}
.method{{border:2px solid #e5e7eb;border-radius:16px;padding:12px;text-align:center;flex:1;cursor:pointer}}.method.sel{{border-color:#e11d48;background:#fff1f2}}
.w-input{{width:93%;padding:14px;border:1px solid #ddd;border-radius:14px;margin:6px 0}}
.support-row{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:white;border-radius:18px;margin:10px 12px}}
</style></head><body>

<div class="topbar"><i class="fa-solid fa-xmark" style="font-size:20px"></i><b>{s['app_name'][:20]}</b><div><i class="fa-solid fa-chevron-down"></i> &nbsp; <i class="fa-solid fa-ellipsis-vertical"></i></div></div>
<div class="header"><div class="avatar">৳</div><div><div id="uName" style="font-weight:bold">User</div><div id="uBal" style="font-size:14px;opacity:0.9">৳0.00</div></div><i class="fa-solid fa-circle-check" style="margin-left:auto;background:rgba(255,255,255,0.2);padding:6px;border-radius:50%"></i></div>

<!-- P1 HOME -->
<div id="p1" class="page active">
<div class="card"><div class="balance-big" id="mainBal">৳110.00</div></div>
<div style="padding:0 12px;color:#6b7280;font-size:13px">আপনার রেফারাল লিংক:</div>
<div class="ref-box"><div id="refLink" style="font-size:13px;overflow:hidden">https://t.me/...</div><div style="border:1px solid #e5e7eb;padding:6px;border-radius:8px"><i class="fa-regular fa-copy" onclick="copyRef()"></i></div></div>
<button class="green-btn" style="margin:0 12px;width:calc(100% - 24px)" onclick="shareRef()"><i class="fa-solid fa-link"></i> রেফার লিংক শেয়ার করুন</button>

<div class="dark-card">
<div style="font-weight:bold;margin-bottom:10px">📢 অফিশিয়াল নোটিশ</div>
<div class="notice-head">🪙 Communitytask</div>
<div style="font-size:13px;line-height:22px;white-space:pre-line;background:#2a4e47;padding:14px;border-radius:14px">{s['notice_text']}</div>
<div style="text-align:center;margin-top:12px">👉 আয় শুরু করুন আজ থেকেই 💚</div>
</div>
</div>

<!-- P2 EARN -->
<div id="p2" class="page">
<div class="ad-card">
<div style="font-size:14px;opacity:0.9">প্রতি বিজ্ঞাপনে নিশ্চিত আয়</div>
<div style="font-size:52px;font-weight:800;margin:5px 0">৳{s['ad_reward']}.00</div>
<div style="display:flex;gap:10px;margin-top:15px">
<div style="flex:1;background:rgba(255,255,255,0.15);padding:10px;border-radius:14px"><div style="font-size:12px">আজকের বিজ্ঞাপন দেখা</div><div style="font-size:20px;font-weight:bold;margin-top:4px"><span id="todayAds">0</span> টি</div></div>
<div style="flex:1;background:rgba(255,255,255,0.15);padding:10px;border-radius:14px"><div style="font-size:12px">আজকের বিজ্ঞাপন আয়</div><div style="font-size:20px;font-weight:bold;margin-top:4px">৳ <span id="todayEarn">0.00</span></div></div>
</div>
<button onclick="watchAd()" style="background:white;color:var(--t);border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;margin-top:15px">▶ বিজ্ঞাপন শুরু করুন (<span id="leftAds">{s['ad_limit']}</span> টি বাকি | আজ <span id="progTxt">0/{s['ad_limit']}</span>)</button>
</div>
<div id="taskList"></div>
</div>

<!-- P3 SUPPORT -->
<div id="p3" class="page">
<div class="support-row" onclick="openLink('https://t.me/{s['admin_username'].replace('@','')}')"><div style="display:flex;gap:12px;align-items:center"><div style="background:#0ea5e9;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center"><i class="fa-brands fa-telegram"></i></div><div><b>Admin কে Message করুন</b><div style="font-size:12px;color:#888">{s['admin_username']}</div></div></div><i class="fa-solid fa-arrow-right" style="color:var(--t)"></i></div>
<div class="support-row" onclick="openLink('https://t.me/{s['channel_username'].replace('@','')}')"><div style="display:flex;gap:12px;align-items:center"><div style="background:#0ea5e9;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center"><i class="fa-brands fa-telegram"></i></div><div><b>অফিশিয়াল চ্যানেল</b><div style="font-size:12px;color:#888">{s['channel_username']}</div></div></div><i class="fa-solid fa-arrow-right" style="color:var(--t)"></i></div>
<div style="background:#ef4444;color:white;border-radius:20px;padding:16px;margin:12px;display:flex;justify-content:space-between;align-items:center" onclick="openLink('{s['video_link']}')"><div style="display:flex;gap:12px;align-items:center"><div style="background:#fbbf24;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center">▶️</div><div><b>কিভাবে কাজ করবেন?</b><div style="font-size:12px">ভিডিও দেখুন এবং সহজেই শিখুন</div></div></div><i class="fa-solid fa-arrow-right"></i></div>
<div class="card" style="font-size:13px;line-height:22px">
<b>🌟 কাস্টমার সার্ভিস নোট</b><br><br>
🔹 আপনার যেকোনো সমস্যা, প্রশ্ন বা সাহায্যের জন্য আমাদের এডমিন সবসময় প্রস্তুত।<br>
👉 প্রয়োজনে নির্দ্বিধায় এডমিনকে মেসেজ করুন।<br><br>
🔹 সকল আপডেট, ঘোষণা ও পেমেন্ট প্রুফ পেতে আমাদের টেলিগ্রাম চ্যানেলে যুক্ত থাকুন। 📢<br><br>
📌 চ্যানেলে আপনি পাবেন:<br>
✅ নতুন আপডেট ✅ পেমেন্ট প্রুফ 💸<br>
✅ অফার ও বোনাস 🎁 ✅ গুরুত্বপূর্ণ নোটিশ<br><br>
⚡ এখনই জয়েন করুন এবং আপডেটেড থাকুন!
</div>
<div style="text-align:center;padding:15px;color:var(--t)"><b>⚡ দ্রুত সাপোর্টের জন্য</b><br><span style="font-size:13px">Telegram এ Admin কে message করুন</span></div>
</div>

<!-- P4 WITHDRAW -->
<div id="p4" class="page">
<div style="background:var(--t);color:white;border-radius:0 0 28px 28px;padding:25px;text-align:center">
<div style="font-size:13px;opacity:0.9">আপনার ব্যালেন্স</div>
<div style="font-size:48px;font-weight:800" id="wBalBig">৳0.00</div>
<div style="display:flex;gap:10px;justify-content:center;margin-top:10px">
<div style="background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:20px;font-size:12px">মিনিমাম: ৳{s['min_wd']}.00</div>
<div style="background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:20px;font-size:12px">• ৳<span id="remain">0</span> বাকি</div>
</div>
</div>

<div class="card">
<div style="background:var(--t);color:white;margin:-15px -15px 15px -15px;padding:12px 15px;border-radius:22px 22px 0 0;display:flex;gap:10px;align-items:center"><div style="background:rgba(255,255,255,0.2);padding:8px;border-radius:10px">💳</div><div><b>টাকা উত্তোলন</b><div style="font-size:12px;opacity:0.9">BKash / Nagad এ পেমেন্ট পান</div></div></div>
<div style="font-size:13px;color:#6b7280;margin-bottom:8px">পেমেন্ট মেথড</div>
<div style="display:flex;gap:10px">
<div class="method sel" id="bkM" onclick="setM('Bkash')"><div style="font-size:36px;color:#e2136e">◈</div><div style="font-size:20px">Bkash</div><div style="color:#e2136e;font-size:12px;margin-top:5px">✓ Selected</div></div>
<div class="method" id="ngM" onclick="setM('Nagad')"><div style="font-size:36px;color:#f59e0b">◎</div><div style="font-size:20px">Nagad</div><div style="color:#f59e0b;font-size:12px;margin-top:5px">Tap to select</div></div>
</div>
<div style="margin-top:12px;font-size:13px">📞 একাউন্ট নম্বর</div>
<input id="wNum" class="w-input" placeholder="01XXXXXXXXX">
<div style="font-size:13px">💵 টাকার পরিমাণ</div>
<input id="wAmt" type="number" class="w-input" placeholder="৳ 0.00">
<div style="font-size:11px;color:#888">মিনিমাম: ৳{s['min_wd']}.00</div>
<button id="wdBtn" onclick="withdraw()" style="background:#9ca3af;color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;margin-top:12px">• ব্যালেন্স যথেষ্ট নয়</button>
</div>
<div style="padding:0 12px"><b>🕒 উইথড্র হিস্ট্রি</b><div id="wHist" style="text-align:center;padding:30px;color:#888">কোন উইথড্র হিস্ট্রি নেই</div></div>
</div>

<!-- P5 PROFILE -->
<div id="p5" class="page">
<div style="background:var(--t);border-radius:22px;padding:18px;margin:12px;display:flex;gap:15px;align-items:center;color:white">
<div class="avatar" style="width:60px;height:60px">৳</div><div><div style="font-size:18px;font-weight:bold" id="pName">SHIBLI NOMAN</div><div style="font-size:12px;opacity:0.8" id="pUser">@user</div><div style="background:rgba(255,255,255,0.2);display:inline-block;padding:3px 10px;border-radius:20px;font-size:12px;margin-top:5px">ID: <span id="pId">8807...</span></div></div></div>
<div class="card" style="background:var(--t);color:white;display:flex;justify-content:space-between"><div>💼 বর্তমান ব্যালেন্স</div><div style="font-weight:bold;font-size:20px" id="pBal">৳0.00</div></div>
<div class="card" style="background:var(--t);color:white;display:flex;justify-content:space-between"><div>✅ মোট সফল উইথড্র</div><div style="font-weight:bold;font-size:20px" id="pSucc">৳0.00</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 12px">
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">📅 আজকের মোট আয়</div><div style="font-weight:bold;color:var(--t)" id="pToday">৳0.00</div></div>
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">📅 গতকালের আয়</div><div style="font-weight:bold" id="pYes">৳0.00</div></div>
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">▶ মোট বিজ্ঞাপন দেখেছেন</div><div style="font-weight:bold;color:var(--t)" id="pAdTotal">0 টি</div></div>
<div class="card" style="margin:0"><div style="font-size:12px;color:#888">👥 মোট রেফার</div><div style="font-weight:bold;color:orange" id="pRefTotal">0 জন</div></div>
</div>
<div class="card" style="display:flex;justify-content:space-between"><div>🪪 ইউজার আইডি</div><div style="color:var(--t);text-decoration:underline" id="pUid2">0000</div></div>
<div class="card" style="display:flex;justify-content:space-between"><div>📊 মোট আয়</div><div id="pTotal">৳0.00</div></div>
<div style="display:flex;gap:10px;margin:12px"><button class="green-btn" style="background:#1a3c34"><i class="fa-regular fa-clock"></i> আয়ের ইতিহাস</button><button class="green-btn" style="background:orange">📋 Rules</button></div>
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
function nav(n){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active')); document.getElementById('p'+n).classList.add('active'); document.querySelectorAll('.b-item').forEach(b=>b.classList.remove('active')); document.getElementById('b'+n).classList.add('active');}}
function setM(m){{wMethod=m; document.getElementById('bkM').classList.toggle('sel',m=='Bkash'); document.getElementById('ngM').classList.toggle('sel',m=='Nagad');}}
function openLink(u){{window.open(u,'_blank');}}
function copyRef(){{navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied!');}}
function shareRef(){{let l=document.getElementById('refLink').innerText; if(navigator.share) navigator.share({{title:'{s['app_name']}',text:l,url:l}}); else copyRef();}}
async function init(){{
 let ref=new URLSearchParams(window.location.search).get("start")||new URLSearchParams(window.location.search).get("ref");
 let res=await fetch("/api/register",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{user_id:uid,name:uname,ref:ref}})}});
 let d=await res.json();
 document.getElementById('uName').innerText=d.name||uname; document.getElementById('uBal').innerText='৳'+d.balance.toFixed(2); document.getElementById('mainBal').innerText='৳'+d.balance.toFixed(2);
 document.getElementById('wBalBig').innerText='৳'+d.balance.toFixed(2); document.getElementById('pBal').innerText='৳'+d.balance.toFixed(2); document.getElementById('pTotal').innerText='৳'+d.total.toFixed(2);
 document.getElementById('pName').innerText=(d.name||uname).toUpperCase(); document.getElementById('pUser').innerText='@'+uid; document.getElementById('pId').innerText=uid; document.getElementById('pUid2').innerText=uid.slice(-6);
 document.getElementById('todayAds').innerText=d.today_ads||0; document.getElementById('todayEarn').innerText=((d.today_ads||0)*{s['ad_reward']}).toFixed(2);
 document.getElementById('leftAds').innerText=adLimit-(d.today_ads||0); document.getElementById('progTxt').innerText=(d.today_ads||0)+'/'+adLimit;
 document.getElementById('pAdTotal').innerText=(d.total_ads||0)+' টি'; document.getElementById('pRefTotal').innerText=(d.ref_count||0)+' জন';
 document.getElementById('remain').innerText=Math.max(0,{s['min_wd']}-d.balance).toFixed(2);
 document.getElementById('refLink').innerText='https://t.me/ProtidinerKajBDBot?start='+uid;
 // wd btn
 let min={s['min_wd']}; if(d.balance>=min){{document.getElementById('wdBtn').style.background='var(--t)'; document.getElementById('wdBtn').innerText='উত্তোলন করুন';}} else {{document.getElementById('wdBtn').style.background='#9ca3af'; document.getElementById('wdBtn').innerText='• ব্যালেন্স যথেষ্ট নয়';}}
 // tasks
 let tHtml=''; let tasks={s['tasks'].__repr__().replace("'",'"')};
 // tasks from server
 if(d.tasks) tasks=d.tasks;
 tasks.forEach(t=>{{ let icon=t.icon=='youtube'?'<div style=\"background:#e11d48;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center\"><i class=\"fa-brands fa-youtube\"></i></div>':'<div style=\"background:#0ea5e9;color:white;width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center\"><i class=\"fa-brands fa-telegram\"></i></div>';
 tHtml+=`<div class="task-row"><div style="display:flex;gap:10px;align-items:center">${{icon}}<div><b>${{t.title}}</b><div style="color:{s['theme']};font-weight:bold">৳${{t.reward}}.00</div></div></div><button class="green-btn" style="width:auto;padding:8px 18px" onclick="doTask('${{t.id}}')">শুরু করুন</button></div>`;}});
 document.getElementById('taskList').innerHTML=tHtml;
 if(d.history && d.history.length>0){{let h=''; d.history.slice().reverse().forEach(x=>{{h+=`<div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee;font-size:12px'><span>${{x.method}} ${{x.number}}</span><span>৳${{x.amount}}</span><span style='color:${{x.status=='PENDING'?'orange':'green'}}'>${{x.status}}</span></div>`}}); document.getElementById('wHist').innerHTML=h;}}
}}
init();
async function watchAd(){{ if(typeof show_11760259!=='function'){{alert('Ad Loading...');return;}} await show_11760259().then(async ()=>{{ let r=await fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid}})}}); let d=await r.json(); if(d.error){{alert(d.error);return;}} init(); alert('✅ ৳{s['ad_reward']} যোগ হয়েছে!');}});}}
async function doTask(id){{let r=await fetch('/api/do_task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid,task_id:id}})}}); let d=await r.json(); if(d.ok){{init(); if(d.link) window.open(d.link,'_blank'); else alert('✅ Task Complete!');}}}}
async function withdraw(){{let num=document.getElementById('wNum').value; let amt=parseInt(document.getElementById('wAmt').value); if(!num||num.length<11){{alert('সঠিক নাম্বার দিন');return;}} if(!amt){{alert('Amount দিন');return;}} let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:uid,amount:amt,method:wMethod,number:num}})}}); let d=await r.json(); if(d.ok){{alert('✅ Request গেছে!'); init();}} else alert(d.error);}}
</script></body></html>
    """

@app.route("/admin")
def admin():
    if request.args.get("id")!=ADMIN_ID: return "Unauthorized",403
    db=load_db(); s=db["settings"]
    tasks_json=json.dumps(s["tasks"],ensure_ascii=False,indent=2)
    return f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Admin FINAL</title>
<style>body{{font-family:system-ui;background:#eef2f7;padding:10px}}.card{{background:white;padding:14px;border-radius:16px;margin-bottom:12px}} input,textarea{{width:95%;padding:10px;margin:5px 0;border:1px solid #ddd;border-radius:10px}}.btn{{border:none;padding:10px 14px;border-radius:10px;color:white;cursor:pointer;font-weight:bold}}.save{{background:#0f766e;width:100%;padding:14px}} table{{width:100%;border-collapse:collapse}} th{{background:#1f2937;color:white;padding:8px;font-size:11px}} td{{padding:7px;border-bottom:1px solid #eee;font-size:11px;text-align:center}}.tab{{display:inline-block;padding:7px 12px;background:#dfe6e9;border-radius:20px;margin:3px;cursor:pointer;font-size:12px}}.tab.active{{background:#0f766e;color:white}}</style>
</head><body>
<h2>👑 ADMIN - {s['app_name']}</h2>
<div class="card"><div class="tab active" onclick="showT('set')" id="t1">⚙️ Settings</div><div class="tab" onclick="showT('ad')" id="t2">📺 বিজ্ঞাপন Edit</div><div class="tab" onclick="showT('users')" id="t3">👥 Users</div><div class="tab" onclick="showT('wd')" id="t4">💸 Withdraw</div></div>

<div id="tab-set" class="card"><h3>Full Control - A to Z</h3>
App Name:<input id="app_name" value="{s['app_name']}">
Theme Color (তোমার কালার):<input id="theme" value="{s['theme']}">
Welcome Bonus (নতুন ইউজার):<input id="welcome" type="number" value="{s['welcome']}">
Refer Bonus:<input id="ref_bonus" type="number" value="{s['ref_bonus']}">
Ad Reward (প্রতি Ad এ):<input id="ad_reward" type="number" value="{s['ad_reward']}">
Ad Limit (দিনে কয়টা):<input id="ad_limit" type="number" value="{s['ad_limit']}">
Min Withdraw:<input id="min_wd" type="number" value="{s['min_wd']}">
Admin Username:<input id="admin_username" value="{s['admin_username']}">
Channel Username:<input id="channel_username" value="{s['channel_username']}">
Video Link:<input id="video_link" value="{s['video_link']}">
Notice Title:<input id="notice_title" value="{s['notice_title']}">
Notice Text (প্রথম পেইজের লেখা - তুমি নিজে Edit করতে পারবে):<textarea id="notice_text" rows="8">{s['notice_text']}</textarea>
<button class="btn save" onclick="saveSet()">💾 Save Settings</button></div>

<div id="tab-ad" class="card" style="display:none"><h3>📺 বিজ্ঞাপন / Task Edit - প্রথম পেইজের বিজ্ঞাপন সিস্টেম</h3>
<p style="font-size:12px;color:#666">এখানে তুমি নিজে বিজ্ঞাপন বসাতে পারবে। Format: YouTube, Telegram, বা Monetag Ad</p>
<textarea id="tasks" rows="12" style="font-family:monospace">{tasks_json}</textarea>
<div style="font-size:11px;color:#888">Example: {{"title":"My Ad","reward":20,"icon":"youtube","link":"https://..."}}<br>icon: youtube / telegram<br>Reward তুমি নিজে বসাবে, Link তুমি নিজে বসাবে। Save দিলে App এ সাথে সাথে চলে আসবে।</div>
<button class="btn save" onclick="saveTasks()">📺 Update Ads</button></div>

<div id="tab-users" class="card" style="display:none"><h3>Users</h3><table><tr><th>ID</th><th>Name</th><th>Bal</th><th>Ref</th><th>Ads</th><th>Action</th></tr><tbody id="users"></tbody></table></div>
<div id="tab-wd" class="card" style="display:none"><h3>Withdraw - Bkash/Nagad</h3><table><tr><th>User</th><th>Method</th><th>Number</th><th>Amt</th><th>Status</th><th>Action</th></tr><tbody id="wds"></tbody></table></div>

<script>
function showT(t){{document.getElementById('tab-set').style.display=t=='set'?'block':'none';document.getElementById('tab-ad').style.display=t=='ad'?'block':'none';document.getElementById('tab-users').style.display=t=='users'?'block':'none';document.getElementById('tab-wd').style.display=t=='wd'?'block':'none';document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById('t'+(t=='set'?1:t=='ad'?2:t=='users'?3:4)).classList.add('active'); load();}}
async function load(){{let r=await fetch('/api/admin/data?id={ADMIN_ID}'); let db=await r.json(); let u=''; for(let id in db.users){{let x=db.users[id]; u+=`<tr><td>${{x.id.slice(-6)}}</td><td>${{x.name||''}}</td><td>${{x.balance}}</td><td>${{x.ref_count}}</td><td>${{x.today_ads||0}}</td><td><button class="btn" style="background:#10b981" onclick="editU('${{x.id}}')">Edit</button></td></tr>`}} document.getElementById('users').innerHTML=u; let w=''; db.withdraws.slice().reverse().forEach(o=>{{w+=`<tr><td>${{o.user.slice(-6)}}</td><td>${{o.method}}</td><td>${{o.number}}</td><td>${{o.amount}}</td><td>${{o.status}}</td><td><button class="btn" style="background:#0ea5e9" onclick="approve('${{o.id}}')">Approve</button></td></tr>`}}); document.getElementById('wds').innerHTML=w;}}
async function saveSet(){{let d={{app_name:document.getElementById('app_name').value,theme:document.getElementById('theme').value,welcome:parseInt(document.getElementById('welcome').value),ref_bonus:parseInt(document.getElementById('ref_bonus').value),ad_reward:parseInt(document.getElementById('ad_reward').value),ad_limit:parseInt(document.getElementById('ad_limit').value),min_wd:parseInt(document.getElementById('min_wd').value),admin_username:document.getElementById('admin_username').value,channel_username:document.getElementById('channel_username').value,video_link:document.getElementById('video_link').value,notice_title:document.getElementById('notice_title').value,notice_text:document.getElementById('notice_text').value}}; await fetch('/api/admin/settings',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}}); alert('✅ Saved!'); location.reload();}}
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
        if ref and ref in db["users"]: db["users"][ref]["balance"]+=s["ref_bonus"]; db["users"][ref]["total"]+=s["ref_bonus"]; db["users"][ref]["ref_count"]+=1
        save_db(db)
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y"); save_db(db)
    u["history"]=[w for w in db["withdraws"] if w["user"]==uid][-5:]
    u["tasks"]=s["tasks"]
    return jsonify(u)

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid=str(request.json.get("user_id")); db=load_db(); s=db["settings"]
    if uid not in db["users"]: return jsonify({"error":"not found"}),404
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"): u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y")
    if u.get("today_ads",0)>=s["ad_limit"]: return jsonify({"error":f"আজ {s['ad_limit']} টা শেষ!"}),400
    u["balance"]+=s["ad_reward"]; u["total"]+=s["ad_reward"]; u["today_ads"]=u.get("today_ads",0)+1; u["total_ads"]=u.get("total_ads",0)+1; save_db(db); return jsonify(u)

@app.route("/api/do_task", methods=["POST"])
def do_task():
    uid=str(request.json.get("user_id")); tid=request.json.get("task_id"); db=load_db()
    if uid not in db["users"]: return jsonify({"error":"no"}),404
    task=next((t for t in db["settings"]["tasks"] if t["id"]==tid), None)
    if not task: return jsonify({"ok":True})
    db["users"][uid]["balance"]+=task["reward"]; db["users"][uid]["total"]+=task["reward"]; save_db(db)
    return jsonify({"ok":True,"link":task.get("link")})

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
