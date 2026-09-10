from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import sqlite3, time, os, random
from datetime import datetime

app = FastAPI()
DB_PATH = "database.db"
ADMIN_ID = os.getenv("ADMIN_ID", "8807178385")

DEFAULT_SETTINGS = {
    "welcome_bonus": "20", "ref_bonus": "25", "task_reward": "10",
    "ad_reward": "10", "daily_ad_limit": "20", "ad_cooldown": "60",
    "min_withdraw": "100", "app_name": "Protidiner Kaj BD",
    "logo_url": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
    "admin_photo": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
    "support_link": "https://t.me/ProtidinerKaj_BD_Bot",
    "monetag_enabled": "1", "monetag_zone": "11764581",
    "custom_ad_enabled": "0", "custom_ad_image": "", "custom_ad_link": "", "custom_ad_title": "🔥 স্পেশাল অফার!",
    "streak_bonus": "10,15,20,30,40,60,100", "spin_enabled": "1"
}

def init_db():
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER DEFAULT 0, ref_count INTEGER DEFAULT 0, last_task INTEGER DEFAULT 0, last_ad INTEGER DEFAULT 0, referred_by TEXT, custom_name TEXT DEFAULT '', custom_photo TEXT DEFAULT '', total_earned INTEGER DEFAULT 0, ad_today INTEGER DEFAULT 0, last_ad_date TEXT DEFAULT '', is_banned INTEGER DEFAULT 0, streak INTEGER DEFAULT 0, last_streak TEXT DEFAULT '', last_spin TEXT DEFAULT '', level INTEGER DEFAULT 1)""")
    c.execute("""CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, amount INTEGER, method TEXT, number TEXT, status TEXT DEFAULT 'pending', date TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)""")
    for k,v in DEFAULT_SETTINGS.items(): c.execute("INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)", (k,str(v)))
    for q in ["ALTER TABLE users ADD COLUMN streak INTEGER DEFAULT 0","ALTER TABLE users ADD COLUMN last_streak TEXT DEFAULT ''","ALTER TABLE users ADD COLUMN last_spin TEXT DEFAULT ''","ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1"]:
        try: c.execute(q)
        except: pass
    conn.commit(); conn.close()
init_db()

def get_setting(k):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); c.execute("SELECT value FROM settings WHERE key=?", (k,)); r=c.fetchone(); conn.close()
    return r[0] if r else DEFAULT_SETTINGS.get(k,"")
def get_all_settings():
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); c.execute("SELECT key,value FROM settings"); d=dict(c.fetchall()); conn.close()
    for k,v in DEFAULT_SETTINGS.items(): d.setdefault(k,v); return d

class ProfileUpdate(BaseModel): user_id: str; name: str = ""; photo: str = ""
class WithdrawReq(BaseModel): user_id: str; amount: int; method: str; number: str
class AdminAction(BaseModel): admin_id: str; user_id: str = ""; amount: int = 0; withdraw_id: int = 0; action: str = ""; settings: dict = {}

def user_html(uid):
    s=get_all_settings(); logo=s.get('logo_url')
    streak_list=s.get('streak_bonus','10,15,20,30,40,60,100').split(',')
    return f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='{s.get("monetag_zone")}' data-sdk='show_{s.get("monetag_zone")}'></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<style>
*{{font-family:'Hind Siliguri', sans-serif; box-sizing:border-box;}} body{{background:#f5f7fb; margin:0; padding:0 0 85px 0;}}
.header{{background:linear-gradient(135deg,#006a4e,#00b894); padding:18px 16px 45px 16px; color:white; border-radius:0 0 28px 28px;}}
.balance-card{{background:white; margin:-32px 16px 14px 16px; border-radius:20px; padding:16px; box-shadow:0 10px 30px rgba(0,0,0,0.1); display:flex; justify-content:space-between; text-align:center; z-index:2; position:relative;}}
.card{{background:white; margin:12px 16px; border-radius:18px; padding:16px; box-shadow:0 4px 15px rgba(0,0,0,0.05);}}
.btn{{width:100%; padding:14px; border-radius:12px; border:none; font-weight:700; cursor:pointer; font-size:15px; display:flex; align-items:center; justify-content:center; gap:8px;}}
.btn-green{{background:linear-gradient(135deg,#00b894,#00a085); color:white;}}.btn-blue{{background:linear-gradient(135deg,#0984e3,#74b9ff); color:white;}}.btn-dark{{background:#2d3436; color:white;}}.btn-yellow{{background:#fdcb6e; color:#2d3436;}}.btn-purple{{background:linear-gradient(135deg,#6c5ce7,#a29bfe); color:white;}}
.bottom-nav{{position:fixed; bottom:0; left:0; right:0; background:white; display:flex; justify-content:space-around; padding:8px 0; border-top:1px solid #eee; z-index:999;}}
.nav-item{{text-align:center; font-size:11px; color:#636e72; flex:1;}}.nav-item.active{{color:#00b894; font-weight:700;}}.nav-item div{{font-size:22px;}}
.page{{display:none;}}.page.active{{display:block;}}
#welcomeModal,#streakModal,#spinModal,#editModal{{display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); backdrop-filter:blur(5px); z-index:10000; justify-content:center; align-items:center; padding:20px;}}
.modal-box{{background:white; padding:25px; border-radius:24px; width:100%; max-width:360px; text-align:center; animation:pop 0.4s ease;}} @keyframes pop{{from{{transform:scale(0.7);}} to{{transform:scale(1);}}}}
.level-badge{{background:linear-gradient(135deg,#fdcb6e,#e17055); color:#2d3436; padding:3px 12px; border-radius:20px; font-size:11px; font-weight:700;}}
.streak-grid{{display:grid; grid-template-columns:repeat(7,1fr); gap:6px; margin-top:12px;}}.streak-day{{background:#f1f2f6; border-radius:10px; padding:8px 2px; text-align:center; font-size:11px;}}.streak-day.active{{background:#00b894; color:white; border:2px solid #00a085;}}.streak-day.done{{background:#dfe6e9; color:#636e72;}}
.wheel{{width:180px; height:180px; border-radius:50%; border:6px solid #fdcb6e; margin:14px auto; background:conic-gradient(#00b894 0deg 60deg, #0984e3 60deg 120deg, #e17055 120deg 180deg, #fdcb6e 180deg 240deg, #6c5ce7 240deg 300deg, #00cec9 300deg 360deg); display:flex; align-items:center; justify-content:center; font-size:40px; transition:transform 3s cubic-bezier(0.2,0.8,0.2,1);}}
</style></head><body>

<div id="welcomeModal"><div class="modal-box"><div style="font-size:70px;">🎉</div><h2 style="color:#00b894; margin:8px 0;">ওয়াও! স্বাগতম!</h2><p>তুমি পেয়েছো</p><h1 style="background:linear-gradient(135deg,#d1f2eb,#a8e6cf); color:#006a4e; padding:14px; border-radius:14px; font-size:32px;">{s.get('welcome_bonus')} TK</h1><p style="font-size:13px; color:#636e72;">+ 7 দিনের Streak শুরু!</p><button class="btn btn-green" onclick="closeWelcome()">🚀 শুরু করি - ধন্যবাদ!</button></div></div>

<div id="streakModal"><div class="modal-box"><h3 style="margin:0;">🔥 7 দিনের Streak</h3><p style="font-size:12px; color:#636e72;">প্রতিদিন এসো, বেশি টাকা নাও</p><div class="streak-grid" id="streakGrid"></div><button id="claimStreakBtn" class="btn btn-green" style="margin-top:14px;" onclick="claimStreak()">🎁 আজকের বোনাস নিন</button><button class="btn" style="background:#dfe6e9; margin-top:8px;" onclick="document.getElementById('streakModal').style.display='none'">পরে</button></div></div>

<div id="spinModal"><div class="modal-box"><h3>🎡 Lucky Spin</h3><p style="font-size:12px; color:#636e72;">প্রতিদিন 1 বার ফ্রি ঘুরাও</p><div class="wheel" id="wheel">🎁</div><h2 id="spinResult" style="margin:10px 0; color:#00b894;">?</h2><button id="spinBtn" class="btn btn-purple" onclick="doSpin()">🎡 ঘুরান!</button><button class="btn" style="background:#dfe6e9; margin-top:8px;" onclick="document.getElementById('spinModal').style.display='none'">বন্ধ</button></div></div>

<div id="editModal"><div class="modal-box"><h3>⚙️ প্রোফাইল</h3><input id="newName" type="text" placeholder="নতুন নাম" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #dfe6e9;"><input id="newPhoto" type="file" accept="image/*" style="width:100%; margin-top:12px;"><img id="preview" data-base64="" style="width:90px; height:90px; border-radius:50%; display:none; margin:14px auto;"><button class="btn btn-green" onclick="saveProfile()">💾 সেভ</button><button class="btn" style="background:#dfe6e9; margin-top:8px;" onclick="document.getElementById('editModal').style.display='none'">বাতিল</button></div></div>

<div class="header"><div style="display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; gap:10px;"><img src="{logo}" style="width:38px; height:38px; border-radius:10px; background:white; padding:4px;"><div><div style="font-weight:700;">{s.get('app_name')}</div><div style="font-size:11px; opacity:0.9;"><span class="level-badge" id="levelBadge">LVL 1</span> <span id="adLeftBadge">Ad: 20</span></div></div></div><img id="headerProfile" src="https://cdn-icons-png.flaticon.com/512/149/149071.png" style="width:36px; height:36px; border-radius:50%; border:2px solid white;"></div></div>
<div class="balance-card"><div><p style="margin:0; font-size:11px; color:#636e72;">ব্যালেন্স</p><h2 id="bal" style="margin:2px 0 0 0;">0 TK</h2></div><div style="width:1px; background:#eee;"></div><div><p style="margin:0; font-size:11px; color:#636e72;">মোট আয়</p><h2 id="totalEarn" style="margin:2px 0 0 0; color:#00b894;">0 TK</h2></div><div style="width:1px; background:#eee;"></div><div><p style="margin:0; font-size:11px; color:#636e72;">Streak</p><h2 id="streakCount" style="margin:2px 0 0 0;">🔥0</h2></div></div>

<div id="page-home" class="page active">
  <div class="card" style="display:flex; gap:10px;">
    <div style="flex:1; background:linear-gradient(135deg,#00b894,#00cec9); color:white; border-radius:14px; padding:12px; text-align:center; cursor:pointer;" onclick="document.getElementById('streakModal').style.display='flex'; renderStreak()"><div style="font-size:24px;">🔥</div><div style="font-weight:700; font-size:13px;">Streak</div><div style="font-size:11px;" id="streakMini">Day 1</div></div>
    <div style="flex:1; background:linear-gradient(135deg,#6c5ce7,#a29bfe); color:white; border-radius:14px; padding:12px; text-align:center; cursor:pointer;" onclick="document.getElementById('spinModal').style.display='flex'"><div style="font-size:24px;">🎡</div><div style="font-weight:700; font-size:13px;">Spin</div><div style="font-size:11px;">Free Daily</div></div>
    <div style="flex:1; background:linear-gradient(135deg,#fdcb6e,#e17055); color:#2d3436; border-radius:14px; padding:12px; text-align:center; cursor:pointer;" onclick="showPage('invite',document.querySelectorAll('.nav-item')[2])"><div style="font-size:24px;">👥</div><div style="font-weight:700; font-size:13px;">Invite</div><div style="font-size:11px;" id="refMini">0 জন</div></div>
  </div>
  <div class="card"><h4 style="margin:0 0 8px 0;">📢 আজকের কাজ</h4><div id="customAdArea"></div><button id="adBtn" class="btn btn-green" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন</button><div style="background:#dfe6e9; height:8px; border-radius:10px; margin-top:10px; overflow:hidden;"><div id="adProgress" style="background:#00b894; height:100%; width:100%;"></div></div><p id="adProgressText" style="font-size:11px; text-align:right; margin:6px 0 0 0; color:#636e72;">20/20</p></div>
  <div class="card"><h4 style="margin:0;">🔗 রেফার লিংক</h4><div style="background:#e8f8f5; border:1.5px dashed #00b894; padding:12px; border-radius:12px; font-size:12px; word-break:break-all; cursor:pointer;" onclick="copyRef()"><span id="refLink">Loading...</span> 📋</div><button class="btn btn-yellow" style="margin-top:10px;" onclick="copyRef()">📤 শেয়ার করুন</button></div>
</div>

<div id="page-tasks" class="page"><div class="card"><h3>🎯 টাস্ক সেন্টার</h3><button id="taskBtn" class="btn btn-blue" onclick="completeTask()">🎁 ডেইলি চেক-ইন</button><div style="margin-top:14px; display:grid; gap:10px;"><div style="padding:12px; background:#f1f2f6; border-radius:12px; display:flex; justify-content:space-between; align-items:center;"><div><b>🔥 Streak বোনাস</b><br><small style="color:#636e72;">প্রতিদিন এসো</small></div><button class="btn btn-green" style="width:auto; padding:8px 14px;" onclick="document.getElementById('streakModal').style.display='flex'; renderStreak()">Open</button></div><div style="padding:12px; background:#f1f2f6; border-radius:12px; display:flex; justify-content:space-between; align-items:center;"><div><b>🎡 Lucky Spin</b><br><small style="color:#636e72;">প্রতিদিন ফ্রি</small></div><button class="btn btn-purple" style="width:auto; padding:8px 14px;" onclick="document.getElementById('spinModal').style.display='flex'">Spin</button></div><div style="padding:12px; background:#f1f2f6; border-radius:12px;"><h4 style="margin:0;">🎬 বিজ্ঞাপন টাস্ক</h4><button id="adBtn2" class="btn btn-green" onclick="watchAd()">Ad দেখুন</button></div></div></div></div>
<div id="page-invite" class="page"><div class="card"><h3>👥 ইনভাইট</h3><div style="background:linear-gradient(135deg,#00b894,#00cec9); color:white; padding:16px; border-radius:14px; text-align:center;"><h1 style="margin:0;">{s.get('ref_bonus')} TK</h1><p>প্রতি রেফারে</p></div><div style="background:#e8f8f5; border:1.5px dashed #00b894; padding:12px; border-radius:12px; margin-top:14px; font-size:12px;" onclick="copyRef()"><span id="refLink2">Loading...</span> 📋</div><button class="btn btn-green" style="margin-top:10px;" onclick="copyRef()">📋 কপি</button></div></div>
<div id="page-wallet" class="page"><div class="card"><h3>💰 ওয়ালেট</h3><p>বর্তমান: <b id="bal2">0 TK</b></p><p>মোট আয়: <b id="totalEarn2">0 TK</b></p><p>Level: <b id="levelText">LVL 1 - Beginner</b></p></div><div class="card"><h4>🏦 টাকা তুলুন</h4><select id="method" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #ddd;"><option>বিকাশ</option><option>নগদ</option></select><input id="number" placeholder="নাম্বার" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #ddd; margin-top:8px;"><input id="amount" type="number" placeholder="পরিমাণ" style="width:100%; padding:12px; border-radius:10px; border:1.5px solid #ddd; margin-top:8px;"><button class="btn btn-green" style="margin-top:12px;" onclick="doWithdraw()">Withdraw</button></div><div class="card" id="wdHistory"><h4>History</h4></div></div>
<div id="page-profile" class="page"><div class="card" style="text-align:center;"><img id="profilePic2" src="https://cdn-icons-png.flaticon.com/512/149/149071.png" style="width:90px; height:90px; border-radius:50%; border:3px solid #00b894;"><h2 id="profileName2">Loading...</h2><p id="uid_show2" style="color:#636e72; font-size:13px;">ID:...</p><p id="levelBadge2"></p><button class="btn btn-blue" onclick="openEdit()">✏️ এডিট</button></div></div>

<div class="bottom-nav"><div class="nav-item active" onclick="showPage('home',this)"><div>🏠</div>Home</div><div class="nav-item" onclick="showPage('tasks',this)"><div>🎯</div>Tasks</div><div class="nav-item" onclick="showPage('invite',this)"><div>👥</div>Invite</div><div class="nav-item" onclick="showPage('wallet',this)"><div>💰</div>Wallet</div><div class="nav-item" onclick="showPage('profile',this)"><div>👤</div>Profile</div></div>

<script>
let userId="{uid}"; let urlParams=new URLSearchParams(window.location.search); let paramId=urlParams.get('id'); let startParam=urlParams.get('start');
function getTgId(){{try{{if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user) return Telegram.WebApp.initDataUnsafe.user.id.toString();}}catch(e){{}} return null;}}
let tgId=getTgId(); if(tgId) userId=tgId; else if(paramId && paramId!="guest") userId=paramId; else if(userId=="guest") userId="user_"+Math.floor(Math.random()*1000000);
let streakBonuses=[{','.join(streak_list)}];
function showPage(p,el){{document.querySelectorAll('.page').forEach(x=>x.classList.remove('active')); document.getElementById('page-'+p).classList.add('active'); document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active')); if(el) el.classList.add('active'); if(p=='wallet') loadWithdrawHistory();}}
document.getElementById('refLink').innerText='https://t.me/ProtidinerKaj_BD_Bot?start='+userId; document.getElementById('refLink2').innerText='https://t.me/ProtidinerKaj_BD_Bot?start='+userId;
function confettiBlast(){{confetti({{particleCount:150, spread:80, origin:{{y:0.6}}}});}}
function loadBalance(){{
    fetch('/api/balance?user_id='+userId+'&start='+(startParam||'')).then(r=>r.json()).then(d=>{{
        if(d.banned){{document.body.innerHTML='<h2 style="text-align:center; margin-top:50px;">⛔ ব্যান</h2>'; return;}}
        document.getElementById('bal').innerText=d.balance+' TK'; document.getElementById('bal2').innerText=d.balance+' TK';
        document.getElementById('totalEarn').innerText=d.total_earned+' TK'; document.getElementById('totalEarn2').innerText=d.total_earned+' TK';
        document.getElementById('streakCount').innerText='🔥'+(d.streak||0); document.getElementById('streakMini').innerText='Day '+(d.streak+1);
        document.getElementById('refMini').innerText=(d.ref_count||0)+' জন';
        document.getElementById('adLeftBadge').innerText='Ad: '+d.ad_left;
        document.getElementById('adProgress').style.width=(d.ad_left/{s.get('daily_ad_limit')}*100)+'%';
        document.getElementById('adProgressText').innerText=d.ad_left+'/{s.get('daily_ad_limit')} বাকি';
        let lvl=d.level||1; let lvlName=['Beginner','Bronze','Silver','Gold','Platinum','Diamond'][Math.min(lvl-1,5)] || 'Beginner';
        document.getElementById('levelBadge').innerText='LVL '+lvl; document.getElementById('levelText').innerText='LVL '+lvl+' - '+lvlName; document.getElementById('levelBadge2').innerHTML='<span style="background:#fdcb6e; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;">'+lvlName+' - LVL '+lvl+'</span>';
        if(d.is_new &&!localStorage.getItem('welcomed_'+userId)){{document.getElementById('welcomeModal').style.display='flex'; confettiBlast();}}
        let abtn=document.getElementById('adBtn'); let abtn2=document.getElementById('adBtn2');
        if(d.ad_left<=0){{abtn.innerText='❌ লিমিট শেষ'; abtn.disabled=true; abtn2.innerText='❌ শেষ'; abtn2.disabled=true;}} else {{abtn.disabled=false; abtn.innerText='🎬 বিজ্ঞাপন - {s.get('ad_reward')} TK (বাকি '+d.ad_left+' টি)'; abtn2.disabled=false; abtn2.innerText='🎬 Ad - {s.get('ad_reward')} TK';}}
        let tbtn=document.getElementById('taskBtn'); if(d.can_task){{tbtn.disabled=false; tbtn.innerText='🎁 ডেইলি চেক-ইন - {s.get('task_reward')} TK';}} else {{tbtn.disabled=true; tbtn.innerText='✅ আজকের চেক-ইন শেষ';}}
        if(d.custom_ad && d.custom_ad.enabled=='1' && d.custom_ad.image){{document.getElementById('customAdArea').innerHTML='<div style="background:linear-gradient(135deg,#fdcb6e,#e17055); border-radius:14px; padding:12px; display:flex; gap:12px; align-items:center; margin-top:12px; cursor:pointer;" onclick="window.open(\\''+d.custom_ad.link+'\\')"><img src="'+d.custom_ad.image+'" style="width:60px; height:60px; border-radius:10px;"><div><div style="font-weight:700;">'+d.custom_ad.title+'</div><div style="font-size:12px;">ট্যাপ করুন</div></div></div>';}}
        window.userStreak=d.streak||0; window.canStreak=d.can_streak; window.canSpin=d.can_spin;
        renderStreak();
    }});
}}
loadBalance();
function closeWelcome(){{document.getElementById('welcomeModal').style.display='none'; localStorage.setItem('welcomed_'+userId,'1');}}
function renderStreak(){{let grid=document.getElementById('streakGrid'); if(!grid) return; let html=''; for(let i=0;i<7;i++){{let cls='streak-day'; if(i<window.userStreak) cls+=' done'; if(i==window.userStreak) cls+=' active'; html+='<div class="'+cls+'"><div>Day '+(i+1)+'</div><div style="font-weight:700;">'+streakBonuses[i]+' TK</div>'+(i<window.userStreak?'✅':'')+'</div>';}} grid.innerHTML=html; let btn=document.getElementById('claimStreakBtn'); if(window.canStreak){{btn.disabled=false; btn.innerText='🎁 Day '+(window.userStreak+1)+' - '+streakBonuses[window.userStreak]+' TK নিন';}} else {{btn.disabled=true; btn.innerText='✅ আজকের নেওয়া হয়েছে';}}}}
function claimStreak(){{fetch('/api/streak?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); confettiBlast(); loadBalance(); document.getElementById('streakModal').style.display='none';}});}}
function doSpin(){{if(!window.canSpin){{alert('⏳ আজকের Spin করেছেন, কাল আবার আসুন'); return;}} let wheel=document.getElementById('wheel'); wheel.style.transform='rotate('+(720+Math.random()*720)+'deg)'; document.getElementById('spinBtn').disabled=true; document.getElementById('spinBtn').innerText='⏳...'; setTimeout(()=>{{fetch('/api/spin?user_id='+userId).then(r=>r.text()).then(a=>{{document.getElementById('spinResult').innerText=a; confettiBlast(); alert(a); loadBalance(); document.getElementById('spinBtn').innerText='✅ Done';}});}},3000);}}
function completeTask(){{fetch('/api/task?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); confettiBlast(); loadBalance();}});}}
function copyRef(){{let t='https://t.me/ProtidinerKaj_BD_Bot?start='+userId; navigator.clipboard.writeText(t).then(()=>alert('✅ কপি!\\n'+t));}}
function openEdit(){{document.getElementById('editModal').style.display='flex';}}
document.getElementById('newPhoto').addEventListener('change', function(e){{let f=e.target.files[0]; if(!f) return; let r=new FileReader(); r.onload=function(ev){{let img=document.getElementById('preview'); img.src=ev.target.result; img.setAttribute('data-base64', ev.target.result); img.style.display='block';}}; r.readAsDataURL(f);}});
function saveProfile(){{let n=document.getElementById('newName').value.trim(); let p=document.getElementById('preview').getAttribute('data-base64')||''; fetch('/api/update_profile',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{user_id:userId, name:n, photo:p}})}}).then(()=>{{document.getElementById('editModal').style.display='none'; alert('✅ সেভ!'); loadBalance();}});}}
function doWithdraw(){{let m=document.getElementById('method').value; let n=document.getElementById('number').value; let a=document.getElementById('amount').value; if(!n||!a){{alert('পূরণ করুন'); return;}} fetch('/api/withdraw',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{user_id:userId, amount:parseInt(a), method:m, number:n}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); if(d.status=='ok'){{loadBalance(); loadWithdrawHistory();}}}});}}
function loadWithdrawHistory(){{fetch('/api/withdraw_history?user_id='+userId).then(r=>r.json()).then(d=>{{let h=document.getElementById('wdHistory'); if(!d.length){{h.innerHTML='<h4>History</h4><p>নেই</p>'; return;}} let html='<h4>History</h4>'; d.forEach(x=>{{html+='<div style="background:#f8f9fa; padding:10px; border-radius:10px; margin-top:8px; font-size:13px;"><b>'+x.amount+' TK</b> - '+x.status+'<br><small>'+x.date+'</small></div>';}}); h.innerHTML=html;}});}}
let timerStarted=false;
function watchAd(){{if(timerStarted) return; if(typeof show_{s.get('monetag_zone')}!=='function' && '{s.get('monetag_enabled')}'=='1'){{alert('Ad লোড হচ্ছে...'); return;}} timerStarted=true; let btn=document.getElementById('adBtn'); let old=btn.innerText; btn.innerText='⏳ লোড...'; btn.disabled=true; let doReward=()=>{{fetch('/api/ad?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); if(a.includes('যোগ')) confettiBlast(); loadBalance(); btn.innerText='✅ Done! 60s'; setTimeout(()=>{{btn.innerText=old; btn.disabled=false; timerStarted=false;}},60000);}});}}; if('{s.get('monetag_enabled')}'=='1'){{show_{s.get('monetag_zone')}().then(doReward).catch(()=>{{timerStarted=false; btn.innerText=old; btn.disabled=false;}});}} else {{doReward(); timerStarted=false;}}}}
</script></body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    uid=request.query_params.get("id","guest"); start=request.query_params.get("start","")
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id=?", (uid,))
    if not c.fetchone() and uid!="guest" and not uid.startswith("user_"):
        c.execute("INSERT INTO users (user_id,balance,referred_by,total_earned,ad_today,last_ad_date,streak,last_streak,level) VALUES (?,?,?,?,?,?,?,?,?)", (uid,int(get_setting("welcome_bonus")),start,int(get_setting("welcome_bonus")),0,"",0,"",1))
        if start and start!=uid:
            c.execute("SELECT user_id FROM users WHERE user_id=?", (start,))
            if c.fetchone(): c.execute("UPDATE users SET balance=balance+?, ref_count=ref_count+1, total_earned=total_earned+? WHERE user_id=?", (int(get_setting("ref_bonus")),int(get_setting("ref_bonus")),start))
        conn.commit()
    conn.close()
    return HTMLResponse(user_html(uid))

@app.get("/api/balance")
async def api_balance(user_id: str, start: str=""):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); today=datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT balance,ref_count,custom_name,custom_photo,total_earned,ad_today,last_ad_date,last_task,is_banned,streak,last_streak,last_spin,level FROM users WHERE user_id=?", (user_id,))
    row=c.fetchone()
    if not row and user_id!="guest" and not user_id.startswith("guest_"):
        c.execute("INSERT INTO users (user_id,balance,referred_by,total_earned,ad_today,last_ad_date,streak,last_streak,level) VALUES (?,?,?,?,?,?,?,?,?)", (user_id,int(get_setting("welcome_bonus")),start,int(get_setting("welcome_bonus")),0,"",0,"",1))
        if start and start!=user_id:
            c.execute("SELECT user_id FROM users WHERE user_id=?", (start,))
            if c.fetchone(): c.execute("UPDATE users SET balance=balance+?, ref_count=ref_count+1, total_earned=total_earned+? WHERE user_id=?", (int(get_setting("ref_bonus")),int(get_setting("ref_bonus")),start))
        conn.commit()
        c.execute("SELECT balance,ref_count,custom_name,custom_photo,total_earned,ad_today,last_ad_date,last_task,is_banned,streak,last_streak,last_spin,level FROM users WHERE user_id=?", (user_id,)); row=c.fetchone()
    s=get_all_settings(); conn.close()
    if not row: return JSONResponse({"balance":0,"ref_count":0,"is_new":True,"custom_name":"","custom_photo":"","total_earned":0,"ad_left":int(s.get("daily_ad_limit","20")),"can_task":True,"banned":False,"streak":0,"can_streak":True,"can_spin":True,"level":1,"custom_ad":{"enabled":s.get("custom_ad_enabled","0"),"image":s.get("custom_ad_image",""),"link":s.get("custom_ad_link",""),"title":s.get("custom_ad_title","")}})
    if row[8]==1: return JSONResponse({"banned":True})
    ad_today=row[5] or 0; last_date=row[6] or ""; last_task=row[7] or 0; streak=row[9] or 0; last_streak=row[10] or ""; last_spin=row[11] or ""; level=row[12] or 1
    if last_date!=today: ad_today=0
    can_task=(int(time.time())-last_task)>86400
    can_streak=last_streak!=today
    can_spin=last_spin!=today
    # Level calc
    total=row[4] or 0
    level = 1 + total//200
    return JSONResponse({"balance":row[0],"ref_count":row[1],"is_new":False,"custom_name":row[2] or "","custom_photo":row[3] or "","total_earned":total,"ad_left":int(s.get("daily_ad_limit","20"))-ad_today,"can_task":can_task,"banned":False,"streak":streak,"can_streak":can_streak,"can_spin":can_spin,"level":level,"custom_ad":{"enabled":s.get("custom_ad_enabled","0"),"image":s.get("custom_ad_image",""),"link":s.get("custom_ad_link",""),"title":s.get("custom_ad_title","")}})

@app.get("/api/streak")
async def api_streak(user_id: str):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); today=datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT streak,last_streak FROM users WHERE user_id=?", (user_id,)); r=c.fetchone()
    if not r: conn.close(); return HTMLResponse("❌ User নেই")
    streak,last=r[0] or 0, r[1] or ""
    if last==today: conn.close(); return HTMLResponse("✅ আজকের Streak নিয়েছেন")
    # Check if streak broken
    yesterday=(datetime.now().date().fromordinal(datetime.now().date().toordinal()-1)).strftime("%Y-%m-%d")
    if last!=yesterday and last!="": streak=0
    bonuses=[int(x) for x in get_setting("streak_bonus").split(",")]
    reward=bonuses[min(streak, len(bonuses)-1)]
    c.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+?, streak=?, last_streak=? WHERE user_id=?", (reward,reward,streak+1 if streak<6 else 0,today,user_id))
    conn.commit(); conn.close()
    return HTMLResponse(f"🔥 Day {streak+1} Streak! {reward} TK পেয়েছো! কাল আবার এসো, আরও বেশি পাবে!")

@app.get("/api/spin")
async def api_spin(user_id: str):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); today=datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT last_spin FROM users WHERE user_id=?", (user_id,)); r=c.fetchone()
    if not r: conn.close(); return HTMLResponse("❌ User নেই")
    if r[0]==today: conn.close(); return HTMLResponse("✅ আজ Spin করেছেন")
    reward=random.choice([5,10,10,15,20,30,50])
    c.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+?, last_spin=? WHERE user_id=?", (reward,reward,today,user_id))
    conn.commit(); conn.close()
    return HTMLResponse(f"🎡 Wow! Spin এ পেয়েছো {reward} TK!")

@app.get("/api/task")
async def api_task(user_id: str):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("SELECT last_task,is_banned FROM users WHERE user_id=?", (user_id,)); r=c.fetchone()
    if not r or r[1]==1: conn.close(); return HTMLResponse("⛔ ব্যান বা User নেই")
    if int(time.time())-(r[0] or 0)<86400: conn.close(); return HTMLResponse("⏳ আজ করেছেন")
    c.execute("UPDATE users SET balance=balance+?, last_task=?, total_earned=total_earned+? WHERE user_id=?", (int(get_setting("task_reward")),int(time.time()),int(get_setting("task_reward")),user_id)); conn.commit(); conn.close()
    return HTMLResponse(f"✅ {get_setting('task_reward')} TK যোগ!")

@app.get("/api/ad")
async def api_ad(user_id: str):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); today=datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT last_ad,ad_today,last_ad_date,is_banned FROM users WHERE user_id=?", (user_id,)); r=c.fetchone()
    if not r or r[3]==1: conn.close(); return HTMLResponse("⛔ ব্যান")
    last_ad,ad_today,last_date=r[0] or 0, r[1] or 0, r[2] or ""
    if last_date!=today: ad_today=0
    if ad_today>=int(get_setting("daily_ad_limit")): conn.close(); return HTMLResponse("❌ আজকের লিমিট শেষ!")
    if int(time.time())-last_ad<int(get_setting("ad_cooldown")): conn.close(); return HTMLResponse(f"⏳ {int(get_setting('ad_cooldown'))-(int(time.time())-last_ad)}s পর")
    c.execute("UPDATE users SET balance=balance+?, last_ad=?, total_earned=total_earned+?, ad_today=?, last_ad_date=? WHERE user_id=?", (int(get_setting("ad_reward")),int(time.time()),int(get_setting("ad_reward")),ad_today+1,today,user_id)); conn.commit(); conn.close()
    return HTMLResponse(f"🎉 {get_setting('ad_reward')} TK যোগ! বাকি {int(get_setting('daily_ad_limit'))-(ad_today+1)} টা")

@app.post("/api/update_profile")
async def upd(data: ProfileUpdate):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    if data.name: c.execute("UPDATE users SET custom_name=? WHERE user_id=?", (data.name,data.user_id))
    if data.photo and "data:image" in data.photo: c.execute("UPDATE users SET custom_photo=? WHERE user_id=?", (data.photo,data.user_id))
    conn.commit(); conn.close(); return JSONResponse({"status":"ok"})

@app.post("/api/withdraw")
async def wd(data: WithdrawReq):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); c.execute("SELECT balance FROM users WHERE user_id=?", (data.user_id,)); r=c.fetchone()
    if not r or r[0]<data.amount: conn.close(); return JSONResponse({"status":"error","msg":"ব্যালেন্স কম"})
    if data.amount<int(get_setting("min_withdraw")): conn.close(); return JSONResponse({"status":"error","msg":f"মিনিমাম {get_setting('min_withdraw')} TK"})
    c.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (data.amount,data.user_id))
    c.execute("INSERT INTO withdraws (user_id,amount,method,number,date) VALUES (?,?,?,?,?)", (data.user_id,data.amount,data.method,data.number,datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit(); conn.close(); return JSONResponse({"status":"ok","msg":"Withdraw Request Success!"})

@app.get("/api/withdraw_history")
async def wdh(user_id: str):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor(); c.execute("SELECT amount,method,number,status,date FROM withdraws WHERE user_id=? ORDER BY id DESC LIMIT 20", (user_id,)); rows=c.fetchall(); conn.close()
    return JSONResponse([{"amount":r[0],"method":r[1],"number":r[2],"status":r[3],"date":r[4]} for r in rows])

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    uid=request.query_params.get("id",""); s=get_all_settings()
    if uid!=ADMIN_ID: return HTMLResponse(f"<h2 style='text-align:center; margin-top:50px;'>⛔ Admin Only<br>Your ID: {uid}</h2>")
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("SELECT COUNT(*), SUM(balance), SUM(ref_count) FROM users"); stats=c.fetchone()
    c.execute("SELECT COUNT(*) FROM withdraws WHERE status='pending'"); pending=c.fetchone()
    c.execute("SELECT COUNT(*) FROM users WHERE last_ad_date=?", (datetime.now().strftime("%Y-%m-%d"),)); active=c.fetchone()
    c.execute("SELECT user_id,balance,ref_count,total_earned,streak,level,is_banned FROM users ORDER BY balance DESC LIMIT 100"); users=c.fetchall()
    c.execute("SELECT id,user_id,amount,method,number,status,date FROM withdraws ORDER BY id DESC LIMIT 100"); wds=c.fetchall()
    c.execute("SELECT key,value FROM settings"); settings=dict(c.fetchall()); conn.close()
    user_rows="".join([f"<tr><td>{u[0][:12]}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[4]}🔥{u[5]}LVL</td><td>{'🚫' if u[6]==1 else '✅'}</td><td><button onclick=\"editBal('{u[0]}')\">+/-</button> <button onclick=\"banUser('{u[0]}')\">Ban</button></td></tr>" for u in users])
    wd_rows="".join([f"<tr><td>{w[0]}</td><td>{w[1][:10]}</td><td>{w[2]} TK</td><td>{w[3]}<br>{w[4]}</td><td>{w[5]}</td><td><button onclick=\"wdAction({w[0]},'paid')\">Paid</button> <button onclick=\"wdAction({w[0]},'reject')\">Reject</button></td></tr>" for w in wds])
    return HTMLResponse(f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{{font-family:sans-serif; background:#f4f6fb; padding:12px;}}.card{{background:white; border-radius:16px; padding:16px; margin-bottom:14px;}}.stats{{display:grid; grid-template-columns:1fr 1fr; gap:10px;}}.stat{{background:white; padding:14px; border-radius:14px; text-align:center;}} table{{width:100%; border-collapse:collapse; font-size:12px;}} th,td{{border:1px solid #eee; padding:6px;}} th{{background:#2d3436; color:white;}} button{{padding:6px 10px; border-radius:6px; border:none; background:#00b894; color:white; cursor:pointer;}} input{{padding:8px; border-radius:6px; border:1px solid #ddd; width:100%; margin-top:4px;}}</style></head><body><h2>👑 Admin - {s.get('app_name')}</h2><div class='stats'><div class='stat'><h3>{stats[0] or 0}</h3>Users</div><div class='stat'><h3>{stats[1] or 0} TK</h3>Bal</div><div class='stat'><h3>{active[0] or 0}</h3>Active</div><div class='stat'><h3 style='color:red;'>{pending[0] or 0}</h3>Pending</div></div><div class='card'><h3>⚙️ Bonus Settings</h3><div style='display:grid; grid-template-columns:1fr 1fr; gap:8px;'><div>Welcome: <input id='welcome_bonus' value='{settings.get('welcome_bonus','20')}'></div><div>Ref: <input id='ref_bonus' value='{settings.get('ref_bonus','25')}'></div><div>Task: <input id='task_reward' value='{settings.get('task_reward','10')}'></div><div>Ad: <input id='ad_reward' value='{settings.get('ad_reward','10')}'></div><div>Streak (7 comma): <input id='streak_bonus' value='{settings.get('streak_bonus','10,15,20,30,40,60,100')}' style='grid-column:span 2;'></div></div><button onclick=\"saveSettings()\" style='width:100%; margin-top:10px; padding:12px; background:#2d3436;'>Save</button></div><div class='card'><h3>🎨 Appearance</h3>App Name: <input id='app_name' value='{settings.get('app_name','')}'><br>Logo URL: <input id='logo_url' value='{settings.get('logo_url','')}'><br>Admin Photo: <input id='admin_photo' value='{settings.get('admin_photo','')}'><button onclick=\"saveAppearance()\" style='width:100%; margin-top:10px; background:#0984e3; padding:12px;'>Save Appearance</button></div><div class='card'><h3>📢 Ads</h3>Monetag On (1): <input id='monetag_enabled' value='{settings.get('monetag_enabled','1')}'> Custom Ad On (1): <input id='custom_ad_enabled' value='{settings.get('custom_ad_enabled','0')}'> Custom Title: <input id='custom_ad_title' value='{settings.get('custom_ad_title','')}'> Custom Image: <input id='custom_ad_image' value='{settings.get('custom_ad_image','')}'> Custom Link: <input id='custom_ad_link' value='{settings.get('custom
