from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import sqlite3, time, os
from datetime import datetime

app = FastAPI()
DB_PATH = "database.db"
ADMIN_ID = os.getenv("ADMIN_ID", "8807178385")

DEFAULTS = {
    "welcome_bonus": "20", "ref_bonus": "25", "task_reward": "10",
    "ad_reward": "10", "daily_ad_limit": "20", "ad_cooldown": "60",
    "min_withdraw": "100", "app_name": "Protidiner Kaj BD",
    "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "admin_photo": "https://cdn-icons-png.flaticon.com/512/149/149071.png",
    "support_link": "https://t.me/ProtidinerKaj_BD_Bot",
    "monetag_enabled": "1", "custom_ad_enabled": "0",
    "custom_ad_image": "", "custom_ad_link": "", "custom_ad_title": "Special Offer"
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER DEFAULT 0, ref_count INTEGER DEFAULT 0, last_task INTEGER DEFAULT 0, last_ad INTEGER DEFAULT 0, referred_by TEXT, custom_name TEXT DEFAULT '', custom_photo TEXT DEFAULT '', total_earned INTEGER DEFAULT 0, ad_today INTEGER DEFAULT 0, last_ad_date TEXT DEFAULT '', is_banned INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, amount INTEGER, method TEXT, number TEXT, status TEXT DEFAULT 'pending', date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    for k,v in DEFAULTS.items():
        c.execute("INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)", (k,v))
    conn.commit()
    conn.close()
init_db()

def get_setting(k):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (k,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else DEFAULTS.get(k,"")

def get_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT key,value FROM settings")
    d = dict(c.fetchall())
    conn.close()
    for k,v in DEFAULTS.items():
        d.setdefault(k,v)
    return d

class ProfileUpdate(BaseModel):
    user_id: str
    name: str = ""
    photo: str = ""

class WithdrawReq(BaseModel):
    user_id: str
    amount: int
    method: str
    number: str

class AdminAction(BaseModel):
    admin_id: str
    user_id: str = ""
    amount: int = 0
    withdraw_id: int = 0
    action: str = ""
    settings: dict = {}

def home_html(uid, settings):
    wb = settings.get("welcome_bonus","20")
    rb = settings.get("ref_bonus","25")
    tb = settings.get("task_reward","10")
    ab = settings.get("ad_reward","10")
    dl = settings.get("daily_ad_limit","20")
    app_name = settings.get("app_name","Protidiner Kaj BD")
    logo = settings.get("logo_url","")
    admin_photo = settings.get("admin_photo","")
    support = settings.get("support_link","")

    html = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600&display=swap" rel="stylesheet">
<style>
*{font-family:'Hind Siliguri',sans-serif;box-sizing:border-box}body{background:#f5f7fb;margin:0;padding:0 0 85px 0}
.header{background:linear-gradient(135deg,#006a4e,#00b894);padding:18px 16px 45px 16px;color:white;border-radius:0 0 28px 28px}
.logo{display:flex;align-items:center;gap:10px}.logo img{width:38px;height:38px;border-radius:10px;background:white;padding:4px}
#profilePic{width:66px;height:66px;border-radius:50%;border:3px solid white;object-fit:cover;background:white}
.balance-card{background:white;margin:-32px 16px 14px 16px;border-radius:20px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,0.1);display:flex;justify-content:space-between;text-align:center;position:relative;z-index:2}
.card{background:white;margin:12px 16px;border-radius:18px;padding:16px;box-shadow:0 4px 15px rgba(0,0,0,0.05)}
.btn{width:100%;padding:14px;border-radius:12px;border:none;font-weight:700;cursor:pointer;font-size:15px}
.btn-green{background:#00b894;color:white}.btn-blue{background:#0984e3;color:white}.btn-dark{background:#2d3436;color:white}.btn-yellow{background:#fdcb6e;color:#2d3436}
.ref-box{background:#e8f8f5;border:1.5px dashed #00b894;padding:12px;border-radius:12px;font-size:12px;word-break:break-all;cursor:pointer}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #eee;z-index:999}
.nav-item{text-align:center;font-size:11px;color:#636e72;cursor:pointer;flex:1}.nav-item.active{color:#00b894;font-weight:700}.nav-item div{font-size:22px}
.page{display:none}.page.active{display:block}
#welcomeModal,#editModal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:10000;justify-content:center;align-items:center;padding:20px}
.modal-box{background:white;padding:25px;border-radius:24px;width:100%;max-width:360px;text-align:center}
</style></head><body>
<div id="welcomeModal"><div class="modal-box"><div style="font-size:60px">🎉</div><h2 style="color:#00b894">স্বাগতম!</h2><h1 style="background:#d1f2eb;color:#00b894;padding:12px;border-radius:12px">"""+wb+""" TK বোনাস</h1><button class="btn btn-green" onclick="closeModal()">শুরু করুন</button></div></div>
<div id="editModal"><div class="modal-box"><h3>প্রোফাইল এডিট</h3><input id="newName" type="text" placeholder="নতুন নাম" style="width:100%;padding:12px;border-radius:10px;border:1.5px solid #ddd"><input id="newPhoto" type="file" accept="image/*" style="width:100%;margin-top:12px"><img id="preview" style="width:90px;height:90px;border-radius:50%;display:none;margin:14px auto"><button class="btn btn-green" onclick="saveProfile()">সেভ</button><button class="btn" style="background:#dfe6e9;margin-top:8px" onclick="document.getElementById('editModal').style.display='none'">বাতিল</button></div></div>

<div class="header"><div style="display:flex;justify-content:space-between;align-items:center"><div class="logo"><img src='"""+logo+"""'><div><div style="font-weight:700">"""+app_name+"""</div><div style="font-size:11px;opacity:0.9">Earn Daily</div></div></div><span id="adLeftBadge" style="background:#ff7675;padding:4px 10px;border-radius:20px;font-size:11px">Ad: 20</span></div></div>

<div class="balance-card"><div><p style="margin:0;font-size:11px;color:#636e72">ব্যালেন্স</p><h2 id="bal" style="margin:0">0 TK</h2></div><div style="width:1px;background:#eee"></div><div><p style="margin:0;font-size:11px;color:#636e72">মোট আয়</p><h2 id="totalEarn" style="margin:0;color:#00b894">0 TK</h2></div><div style="width:1px;background:#eee"></div><div><p style="margin:0;font-size:11px;color:#636e72">রেফার</p><h2 id="refCount" style="margin:0">0</h2></div></div>

<div id="page-home" class="page active">
<div class="card" style="text-align:center"><img id="profilePic" src="https://cdn-icons-png.flaticon.com/512/149/149071.png"><h3 id="profileName">Loading</h3><p id="uid_show" style="font-size:12px;color:#636e72">ID:...</p><button onclick="openEdit()" style="padding:6px 14px;border-radius:20px;border:1.5px solid #00b894;background:white;color:#00b894">এডিট</button></div>
<div class="card"><div id="customAdArea"></div><button id="adBtn" class="btn btn-green" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন - """+ab+""" TK</button><div style="background:#dfe6e9;height:8px;border-radius:10px;margin-top:10px;overflow:hidden"><div id="adProgress" style="background:#00b894;height:100%;width:100%"></div></div><p id="adProgressText" style="font-size:11px;text-align:right;color:#636e72">"""+dl+"""/"""+dl+""" বাকি</p></div>
<div class="card"><h4 style="margin:0">🔗 রেফার লিংক</h4><div class="ref-box" onclick="copyRef()" style="margin-top:10px"><span id="refLink">Loading</span></div><button class="btn btn-yellow" style="margin-top:10px" onclick="copyRef()">📤 শেয়ার</button></div>
</div>

<div id="page-tasks" class="page"><div class="card"><h3>🎯 টাস্ক</h3><button id="taskBtn" class="btn btn-blue" onclick="completeTask()">🎁 ডেইলি চেক-ইন - """+tb+""" TK</button><button id="adBtn2" class="btn btn-green" style="margin-top:10px" onclick="watchAd()">🎬 Ad - """+ab+""" TK</button></div></div>
<div id="page-invite" class="page"><div class="card"><h3>👥 ইনভাইট</h3><div style="background:linear-gradient(135deg,#00b894,#00cec9);color:white;padding:16px;border-radius:14px;text-align:center"><h1 style="margin:0">"""+rb+""" TK</h1><p>প্রতি রেফারে</p></div><div class="ref-box" style="margin-top:14px" onclick="copyRef()"><span id="refLink2">Loading</span></div></div></div>
<div id="page-wallet" class="page"><div class="card"><h3>💰 ওয়ালেট</h3><p>বর্তমান: <b id="bal2">0 TK</b></p><p>মোট: <b id="totalEarn2">0 TK</b></p></div><div class="card"><h4>🏦 টাকা তুলুন</h4><select id="method" style="width:100%;padding:12px;border-radius:10px;border:1.5px solid #ddd"><option>বিকাশ</option><option>নগদ</option></select><input id="number" placeholder="নাম্বার" style="width:100%;padding:12px;border-radius:10px;border:1.5px solid #ddd;margin-top:8px"><input id="amount" type="number" placeholder="পরিমাণ" style="width:100%;padding:12px;border-radius:10px;border:1.5px solid #ddd;margin-top:8px"><button class="btn btn-green" style="margin-top:12px" onclick="doWithdraw()">Withdraw</button></div><div class="card" id="wdHistory"><h4>History</h4></div></div>
<div id="page-profile" class="page"><div class="card" style="text-align:center"><img id="profilePic2" src="https://cdn-icons-png.flaticon.com/512/149/149071.png" style="width:90px;height:90px;border-radius:50%;border:3px solid #00b894"><h2 id="profileName2">Loading</h2><p id="uid_show2" style="color:#636e72">ID:...</p><button class="btn btn-blue" onclick="openEdit()">এডিট</button></div><div class="card"><h4>🛡️ সাপোর্ট</h4><div style="display:flex;gap:12px;align-items:center"><img src='"""+admin_photo+"""' style="width:48px;height:48px;border-radius:50%"><div><div style="font-weight:600">Admin</div><a href='"""+support+"""' style="font-size:13px;color:#0984e3">মেসেজ করুন</a></div></div></div></div>

<div class="bottom-nav">
<div class="nav-item active" onclick="showPage('home',this)"><div>🏠</div>Home</div>
<div class="nav-item" onclick="showPage('tasks',this)"><div>🎯</div>Tasks</div>
<div class="nav-item" onclick="showPage('invite',this)"><div>👥</div>Invite</div>
<div class="nav-item" onclick="showPage('wallet',this)"><div>💰</div>Wallet</div>
<div class="nav-item" onclick="showPage('profile',this)"><div>👤</div>Profile</div>
</div>

<script>
let userId = "USERIDPLACEHOLDER";
let urlParams = new URLSearchParams(window.location.search);
let paramId = urlParams.get('id');
let startParam = urlParams.get('start');
function getTgId(){try{if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user) return Telegram.WebApp.initDataUnsafe.user.id.toString();}catch(e){} return null;}
let tgId = getTgId();
let tgUser = null;
try{tgUser = window.Telegram.WebApp.initDataUnsafe.user;}catch(e){}
if(tgId){userId = tgId;} else if(paramId && paramId!= "guest" && paramId!= "null"){userId = paramId;} else if(userId == "guest"){userId = "user_" + Math.floor(Math.random()*1000000);}

function showPage(p,el){
document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
document.getElementById('page-'+p).classList.add('active');
document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));
if(el) el.classList.add('active');
if(p=='wallet') loadWithdrawHistory();
}
document.getElementById('uid_show').innerText = 'ID: ' + userId;
document.getElementById('uid_show2').innerText = 'ID: ' + userId;
document.getElementById('refLink').innerText = 'https://t.me/ProtidinerKaj_BD_Bot?start=' + userId;
document.getElementById('refLink2').innerText = 'https://t.me/ProtidinerKaj_BD_Bot?start=' + userId;
document.getElementById('profileName').innerText = 'User ' + userId.toString().substring(0,6);
document.getElementById('profileName2').innerText = 'User ' + userId.toString().substring(0,6);
if(tgUser){
 if(tgUser.photo_url){document.getElementById('profilePic').src = tgUser.photo_url; document.getElementById('profilePic2').src = tgUser.photo_url;}
 let n = (tgUser.first_name||'') + ' ' + (tgUser.last_name||'');
 if(n.trim()){document.getElementById('profileName').innerText = n.trim(); document.getElementById('profileName2').innerText = n.trim();}
}
function closeModal(){document.getElementById('welcomeModal').style.display='none'; localStorage.setItem('welcomed_'+userId,'1');}
function loadBalance(){
 let ln = localStorage.getItem('my_name_'+userId);
 let lp = localStorage.getItem('my_photo_'+userId);
 if(ln){document.getElementById('profileName').innerText = ln; document.getElementById('profileName2').innerText = ln;}
 if(lp){document.getElementById('profilePic').src = lp; document.getElementById('profilePic2').src = lp;}
 fetch('/api/balance?user_id='+userId+'&start='+(startParam||'')).then(r=>r.json()).then(d=>{
  if(d.banned){document.body.innerHTML='<div style="text-align:center;padding:50px"><h2>⛔ ব্যান</h2></div>'; return;}
  document.getElementById('bal').innerText = d.balance + ' TK';
  document.getElementById('bal2').innerText = d.balance + ' TK';
  document.getElementById('refCount').innerText = d.ref_count;
  document.getElementById('totalEarn').innerText = d.total_earned + ' TK';
  document.getElementById('totalEarn2').innerText = d.total_earned + ' TK';
  document.getElementById('adLeftBadge').innerText = 'Ad: ' + d.ad_left;
  document.getElementById('adProgress').style.width = (d.ad_left / """+dl+""" * 100) + '%';
  document.getElementById('adProgressText').innerText = d.ad_left + '/' + """+dl+""" + ' বাকি';
  if(d.custom_name){document.getElementById('profileName').innerText = d.custom_name; document.getElementById('profileName2').innerText = d.custom_name; localStorage.setItem('my_name_'+userId,d.custom_name);}
  if(d.custom_photo){document.getElementById('profilePic').src = d.custom_photo; document.getElementById('profilePic2').src = d.custom_photo; localStorage.setItem('my_photo_'+userId,d.custom_photo);}
  if(d.is_new &&!localStorage.getItem('welcomed_'+userId)) document.getElementById('welcomeModal').style.display='flex';
  let abtn = document.getElementById('adBtn');
  let abtn2 = document.getElementById('adBtn2');
  if(d.ad_left <= 0){abtn.innerText = 'লিমিট শেষ'; abtn.disabled=true; abtn2.innerText='লিমিট শেষ'; abtn2.disabled=true;} else {abtn.disabled=false; abtn.innerText='🎬 বিজ্ঞাপন - """+ab+""" TK (বাকি '+d.ad_left+' টি)'; abtn2.disabled=false; abtn2.innerText='🎬 Ad - """+ab+""" TK (বাকি '+d.ad_left+')';}
  let tbtn = document.getElementById('taskBtn');
  if(d.can_task){tbtn.disabled=false; tbtn.innerText='🎁 ডেইলি চেক-ইন - """+tb+""" TK';} else {tbtn.disabled=true; tbtn.innerText='আজকের চেক-ইন শেষ';}
  if(d.custom_ad && d.custom_ad.enabled == '1' && d.custom_ad.image){
   document.getElementById('customAdArea').innerHTML = '<div style="background:linear-gradient(135deg,#fdcb6e,#e17055);border-radius:14px;padding:12px;display:flex;gap:12px;align-items:center;margin-bottom:12px;cursor:pointer" onclick="window.open(&quot;'+d.custom_ad.link+'&quot;)"><img src="'+d.custom_ad.image+'" style="width:60px;height:60px;border-radius:10px"><div><div style="font-weight:700">'+d.custom_ad.title+'</div><div style="font-size:12px">ট্যাপ করুন</div></div></div>';
  }
 });
}
loadBalance();
function completeTask(){fetch('/api/task?user_id='+userId).then(r=>r.text()).then(a=>{alert(a); loadBalance();});}
function copyRef(){let t='https://t.me/ProtidinerKaj_BD_Bot?start='+userId; navigator.clipboard.writeText(t).then(()=>alert('✅ কপি হয়েছে!\\n'+t));}
function openEdit(){document.getElementById('editModal').style.display='flex';}
document.getElementById('newPhoto').addEventListener('change', function(e){let f=e.target.files[0]; if(!f) return; let r=new FileReader(); r.onload=function(ev){let img=document.getElementById('preview'); img.src=ev.target.result; img.setAttribute('data-base64',ev.target.result); img.style.display='block';}; r.readAsDataURL(f);});
function saveProfile(){
 let n=document.getElementById('newName').value.trim();
 let p=document.getElementById('preview').getAttribute('data-base64')||'';
 if(n){document.getElementById('profileName').innerText=n; document.getElementById('profileName2').innerText=n; localStorage.setItem('my_name_'+userId,n);}
 if(p){document.getElementById('profilePic').src=p; document.getElementById('profilePic2').src=p; localStorage.setItem('my_photo_'+userId,p);}
 fetch('/api/update_profile',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user_id:userId, name:n, photo:p})}).then(()=>{document.getElementById('editModal').style.display='none'; alert('✅ সেভ হয়েছে!');});
}
function doWithdraw(){let m=document.getElementById('method').value; let n=document.getElementById('number').value; let a=document.getElementById('amount').value; if(!n||!a){alert('পূরণ করুন'); return;} fetch('/api/withdraw',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user_id:userId, amount:parseInt(a), method:m, number:n})}).then(r=>r.json()).then(d=>{alert(d.msg); if(d.status=='ok'){loadBalance(); loadWithdrawHistory();}});}
function loadWithdrawHistory(){fetch('/api/withdraw_history?user_id='+userId).then(r=>r.json()).then(d=>{let h=document.getElementById('wdHistory'); if(!d.length){h.innerHTML='<h4>History</h4><p style="font-size:12px">নেই</p>'; return;} let html='<h4>History</h4>'; d.forEach(x=>{html+='<div style="background:#f8f9fa;padding:10px;border-radius:10px;margin-top:8px;font-size:13px"><b>'+x.amount+' TK</b> - '+x.method+' - '+x.status+'<br><small>'+x.date+'</small></div>';}); h.innerHTML=html;});}
let timerStarted=false;
function watchAd(){
 if(timerStarted) return;
 if(typeof show_11764581!== 'function'){alert('Ad লোড হচ্ছে, 2 সেকেন্ড পর আবার চাপুন'); return;}
 timerStarted=true;
 let btn=document.getElementById('adBtn');
 let old=btn.innerText;
 btn.innerText='লোড হচ্ছে...';
 btn.disabled=true;
 show_11764581().then(()=>{
  btn.innerText='যাচাই হচ্ছে...';
  fetch('/api/ad?user_id='+userId).then(r=>r.text()).then(a=>{
   alert(a); loadBalance();
   btn.innerText='Done! 60s';
   setTimeout(()=>{btn.innerText=old; btn.disabled=false; timerStarted=false; loadBalance();},60000);
  });
 }).catch(()=>{timerStarted=false; btn.innerText=old; btn.disabled=false; alert('Ad সম্পূর্ণ দেখেননি');});
}
</script></body></html>
"""
    html = html.replace("USERIDPLACEHOLDER", uid)
    return html

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    uid = request.query_params.get("id", "guest")
    start = request.query_params.get("start", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id=?", (uid,))
    if not c.fetchone() and uid!= "guest" and not uid.startswith("user_"):
        c.execute("INSERT INTO users (user_id,balance,referred_by,total_earned,ad_today,last_ad_date) VALUES (?,?,?,?,?,?)", (uid, int(get_setting("welcome_bonus")), start, int(get_setting("welcome_bonus")), 0, ""))
        if start and start!= uid:
            c.execute("SELECT user_id FROM users WHERE user_id=?", (start,))
            if c.fetchone():
                c.execute("UPDATE users SET balance=balance+?, ref_count=ref_count+1, total_earned=total_earned+? WHERE user_id=?", (int(get_setting("ref_bonus")), int(get_setting("ref_bonus")), start))
        conn.commit()
    conn.close()
    settings = get_all()
    return HTMLResponse(home_html(uid, settings))

@app.get("/api/balance")
async def balance(user_id: str, start: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT balance,ref_count,custom_name,custom_photo,total_earned,ad_today,last_ad_date,last_task,is_banned FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row and user_id!= "guest" and not user_id.startswith("guest_"):
        c.execute("INSERT INTO users (user_id,balance,referred_by,total_earned,ad_today,last_ad_date) VALUES (?,?,?,?,?,?)", (user_id, int(get_setting("welcome_bonus")), start, int(get_setting("welcome_bonus")), 0, ""))
        if start and start!= user_id:
            c.execute("SELECT user_id FROM users WHERE user_id=?", (start,))
            if c.fetchone():
                c.execute("UPDATE users SET balance=balance+?, ref_count=ref_count+1, total_earned=total_earned+? WHERE user_id=?", (int(get_setting("ref_bonus")), int(get_setting("ref_bonus")), start))
        conn.commit()
        c.execute("SELECT balance,ref_count,custom_name,custom_photo,total_earned,ad_today,last_ad_date,last_task,is_banned FROM users WHERE user_id=?", (user_id,))
        row = c.fetchone()
    s = get_all()
    conn.close()
    if not row:
        return JSONResponse({"balance":0,"ref_count":0,"is_new":True,"custom_name":"","custom_photo":"","total_earned":0,"ad_left":int(s.get("daily_ad_limit","20")),"can_task":True,"banned":False,"custom_ad":{"enabled":s.get("custom_ad_enabled","0"),"image":s.get("custom_ad_image",""),"link":s.get("custom_ad_link",""),"title":s.get("custom_ad_title","")}})
    if row[8] == 1:
        return JSONResponse({"banned":True})
    ad_today = row[5] or 0
    last_date = row[6] or ""
    last_task = row[7] or 0
    if last_date!= today:
        ad_today = 0
    can_task = (int(time.time()) - last_task) > 86400
    return JSONResponse({
        "balance": row[0], "ref_count": row[1], "is_new": False,
        "custom_name": row[2] or "", "custom_photo": row[3] or "",
        "total_earned": row[4] or row[0],
        "ad_left": int(s.get("daily_ad_limit","20")) - ad_today,
        "can_task": can_task, "banned": False,
        "custom_ad": {"enabled": s.get("custom_ad_enabled","0"), "image": s.get("custom_ad_image",""), "link": s.get("custom_ad_link",""), "title": s.get("custom_ad_title","")}
    })

@app.get("/api/task")
async def task(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_task,is_banned FROM users WHERE user_id=?", (user_id,))
    r = c.fetchone()
    if not r:
        conn.close()
        return HTMLResponse("User নেই")
    if r[1] == 1:
        conn.close()
        return HTMLResponse("ব্যান")
    if int(time.time()) - (r[0] or 0) < 86400:
        conn.close()
        return HTMLResponse("আজকের চেক-ইন করেছেন")
    c.execute("UPDATE users SET balance=balance+?, last_task=?, total_earned=total_earned+? WHERE user_id=?", (int(get_setting("task_reward")), int(time.time()), int(get_setting("task_reward")), user_id))
    conn.commit()
    conn.close()
    return HTMLResponse(f"{get_setting('task_reward')} TK যোগ হয়েছে!")

@app.get("/api/ad")
async def ad(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT last_ad,ad_today,last_ad_date,is_banned FROM users WHERE user_id=?", (user_id,))
    r = c.fetchone()
    if not r:
        conn.close()
        return HTMLResponse("User নেই")
    if r[3] == 1:
        conn.close()
        return HTMLResponse("ব্যান")
    last_ad, ad_today, last_date = r[0] or 0, r[1] or 0, r[2] or ""
    if last_date!= today:
        ad_today = 0
    if ad_today >= int(get_setting("daily_ad_limit")):
        conn.close()
        return HTMLResponse("আজকের লিমিট শেষ!")
    if int(time.time()) - last_ad < int(get_setting("ad_cooldown")):
        conn.close()
        return HTMLResponse(f"{int(get_setting('ad_cooldown')) - (int(time.time()) - last_ad)} সেকেন্ড পর")
    c.execute("UPDATE users SET balance=balance+?, last_ad=?, total_earned=total_earned+?, ad_today=?, last_ad_date=? WHERE user_id=?", (int(get_setting("ad_reward")), int(time.time()), int(get_setting("ad_reward")), ad_today+1, today, user_id))
    conn.commit()
    conn.close()
    return HTMLResponse(f"{get_setting('ad_reward')} TK যোগ হয়েছে!")

@app.post("/api/update_profile")
async def update_profile(data: ProfileUpdate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if data.name:
        c.execute("UPDATE users SET custom_name=? WHERE user_id=?", (data.name, data.user_id))
    if data.photo and "data:image" in data.photo and len(data.photo) < 900000:
        c.execute("UPDATE users SET custom_photo=? WHERE user_id=?", (data.photo, data.user_id))
    conn.commit()
    conn.close()
    return JSONResponse({"status":"ok"})

@app.post("/api/withdraw")
async def withdraw_req(data: WithdrawReq):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (data.user_id,))
    r = c.fetchone()
    if not r or r[0] < data.amount:
        conn.close()
        return JSONResponse({"status":"error","msg":"ব্যালেন্স কম"})
    if data.amount < int(get_setting("min_withdraw")):
        conn.close()
        return JSONResponse({"status":"error","msg":f"মিনিমাম {get_setting('min_withdraw')} TK"})
    c.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (data.amount, data.user_id))
    c.execute("INSERT INTO withdraws (user_id,amount,method,number,date) VALUES (?,?,?,?,?)", (data.user_id, data.amount, data.method, data.number, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    return JSONResponse({"status":"ok","msg":"Withdraw Request পাঠানো হয়েছে!"})

@app.get("/api/withdraw_history")
async def wd_hist(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT amount,method,number,status,date FROM withdraws WHERE user_id=? ORDER BY id DESC LIMIT 20", (user_id,))
    rows = c.fetchall()
    conn.close()
    return JSONResponse([{"amount":r[0],"method":r[1],"number":r[2],"status":r[3],"date":r[4]} for r in rows])

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    uid = request.query_params.get("id","")
    if uid!= ADMIN_ID:
        return HTMLResponse(f"<h2 style='text-align:center;margin-top:50px'>⛔ Admin Only<br>Your ID: {uid}</h2>")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(balance) FROM users")
    stats = c.fetchone()
    c.execute("SELECT COUNT(*) FROM withdraws WHERE status='pending'")
    pending = c.fetchone()
    c.execute("SELECT user_id,balance,ref_count,total_earned,is_banned FROM users ORDER BY balance DESC LIMIT 50")
    users = c.fetchall()
    c.execute("SELECT id,user_id,amount,method,number,status,date FROM withdraws ORDER BY id DESC LIMIT 50")
    wds = c.fetchall()
    c.execute("SELECT key,value FROM settings")
    settings = dict(c.fetchall())
    conn.close()
    user_rows = "".join([f"<tr><td>{u[0][:10]}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td><td>{'BAN' if u[4]==1 else 'OK'}</td><td><button onclick=\"editBal('{u[0]}')\">Edit</button> <button onclick=\"banUser('{u[0]}')\">Ban</button></td></tr>" for u in users])
    wd_rows = "".join([f"<tr><td>{w[0]}</td><td>{w[1][:8]}</td><td>{w[2]}</td><td>{w[3]} {w[4]}</td><td>{w[5]}</td><td><button onclick=\"wdAction({w[0]},'paid')\">Paid</button> <button onclick=\"wdAction({w[0]},'reject')\">Reject</button></td></tr>" for w in wds])
    return HTMLResponse(f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{{font-family:sans-serif;background:#f4f6fb;padding:12px}}.card{{background:white;border-radius:16px;padding:16px;margin-bottom:14px}} table{{width:100%;border-collapse:collapse;font-size:12px}} th,td{{border:1px solid #eee;padding:6px}} th{{background:#2d3436;color:white}} button{{padding:6px 10px;border-radius:6px;border:none;background:#00b894;color:white;cursor:pointer;margin:2px}} input{{padding:8px;border-radius:6px;border:1px solid #ddd;width:100%;margin-top:4px}}
</style></head><body>
<h2>👑 Admin - {settings.get('app_name','')}</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><div style="background:white;padding:14px;border-radius:14px;text-align:center"><h3>{stats[0] or 0}</h3>Total Users</div><div style="background:white;padding:14px;border-radius:14px;text-align:center"><h3>{pending[0] or 0}</h3>Pending WD</div></div>

<div class="card"><h3>Settings</h3>
Welcome: <input id="welcome_bonus" value="{settings.get('welcome_bonus','20')}">
Ref: <input id="ref_bonus" value="{settings.get('ref_bonus','25')}">
Task: <input id="task_reward" value="{settings.get('task_reward','10')}">
Ad Reward: <input id="ad_reward" value="{settings.get('ad_reward','10')}">
Ad Limit: <input id="daily_ad_limit" value="{settings.get('daily_ad_limit','20')}">
Min WD: <input id="min_withdraw" value="{settings.get('min_withdraw','100')}">
<button onclick="saveSettings()" style="width:100%;margin-top:10px;padding:12px;background:#2d3436">Save Settings</button></div>

<div class="card"><h3>Appearance</h3>
App Name: <input id="app_name" value="{settings.get('app_name','')}">
Logo URL: <input id="logo_url" value="{settings.get('logo_url','')}">
Admin Photo: <input id="admin_photo" value="{settings.get('admin_photo','')}">
Support Link: <input id="support_link" value="{settings.get('support_link','')}">
<button onclick="saveAppearance()" style="width:100%;margin-top:10px;background:#0984e3;padding:12px">Save Appearance</button></div>

<div class="card"><h3>Custom Ad - Your Own Ad</h3>
Enabled 1/0: <input id="custom_ad_enabled" value="{settings.get('custom_ad_enabled','0')}">
Title: <input id="custom_ad_title" value="{settings.get('custom_ad_title','')}">
Image URL: <input id="custom_ad_image" value="{settings.get('custom_ad_image','')}">
Link URL: <input id="custom_ad_link" value="{settings.get('custom_ad_link','')}">
<button onclick="saveAds()" style="width:100%;margin-top:10px;background:#e17055;padding:12px">Save Ads</button></div>

<div class="card"><h3>Withdraw</h3><table><tr><th>ID</th><th>User</th><th>Amt</th><th>Method</th><th>Status</th><th>Action</th></tr>{wd_rows}</table></div>
<div class="card"><h3>Users</h3><table><tr><th>ID</th><th>Bal</th><th>Ref</th><th>Total</th><th>St</th><th>Act</th></tr>{user_rows}</table></div>
<script>
function editBal(uid){{let amt=prompt('Amount +100 or -50'); if(!amt) return; fetch('/api/admin/action',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{admin_id:'{uid}', user_id:uid, amount:parseInt(amt), action:'balance'}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); location.reload();}});}}
function banUser(uid){{fetch('/api/admin/action',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{admin_id:'{uid}', user_id:uid, action:'ban'}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); location.reload();}});}}
function wdAction(id,act){{fetch('/api/admin/action',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{admin_id:'{uid}', withdraw_id:id, action:act}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); location.reload();}});}}
function saveSettings(){{let s={{}}; ['welcome_bonus','ref_bonus','task_reward','ad_reward','daily_ad_limit','min_withdraw'].forEach(k=>s[k]=document.getElementById(k).value); fetch('/api/admin/settings',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{admin_id:'{uid}', settings:s}})}}).then(r=>r.json()).then(d=>alert(d.msg));}}
function saveAppearance(){{let s={{}}; ['app_name','logo_url','admin_photo','support_link'].forEach(k=>s[k]=document.getElementById(k).value); fetch('/api/admin/settings',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{admin_id:'{uid}', settings:s}})}}).then(r=>r.json()).then(d=>alert(d.msg));}}
function saveAds(){{let s={{}}; ['custom_ad_enabled','custom_ad_image','custom_ad_link','custom_ad_title'].forEach(k=>s[k]=document.getElementById(k).value); fetch('/api/admin/settings',{{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{admin_id:'{uid}', settings:s}})}}).then(r=>r.json()).then(d=>alert(d.msg));}}
</script></body></html>
""")

@app.post("/api/admin/settings")
async def admin_settings(data: AdminAction):
    if data.admin_id!= ADMIN_ID:
        return JSONResponse({"msg":"Unauthorized"})
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for k,v in data.settings.items():
        c.execute("INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)", (k,str(v)))
    conn.commit()
    conn.close()
    return JSONResponse({"msg":"Save হয়েছে!"})

@app.post("/api/admin/action")
async def admin_action(data: AdminAction):
    if data.admin_id!= ADMIN_ID:
        return JSONResponse({"msg":"Unauthorized"})
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if data.action == 'balance':
        c.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+? WHERE user_id=?", (data.amount, data.amount if data.amount>0 else 0, data.user_id))
    elif data.action == 'ban':
        c.execute("SELECT is_banned FROM users WHERE user_id=?", (data.user_id,))
        r = c.fetchone()
        if r:
            c.execute("UPDATE users SET is_banned=? WHERE user_id=?", (0 if r[0]==1 else 1, data.user_id))
    elif data.action in ['paid','reject']:
        if data.action == 'paid':
            c.execute("UPDATE withdraws SET status='paid' WHERE id=?", (data.withdraw_id,))
        else:
            c.execute("SELECT user_id,amount FROM withdraws WHERE id=?", (data.withdraw_id,))
            r = c.fetchone()
            if r:
                c.execute("UPDATE users SET balance=balance+? WHERE user_id=?", (r[1], r[0]))
            c.execute("UPDATE withdraws SET status='rejected' WHERE id=?", (data.withdraw_id,))
    conn.commit()
    conn.close()
    return JSONResponse({"msg":f"{data.action} Done!"})
