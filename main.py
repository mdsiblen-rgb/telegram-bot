import os, hmac, hashlib, json, sqlite3, secrets, base64, time, csv, io
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import parse_qsl
from functools import wraps
from flask import Flask, request, jsonify, render_template_string, Response

APP = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "protidiner_kaj_bd.db")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8807178385"))
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "").strip()
PORT = int(os.environ.get("PORT", "10000"))

DEFAULTS = {
    "app_name": "প্রতিদিনের কাজ BD",
    "currency": "৳",
    "daily_bonus": "5",
    "ad_daily_limit": "5",
    "ad_reward": "2",
    "referral_reward": "10",
    "referral_diamond": "5",
    "diamond_name": "Diamond",
    "min_withdraw": "100",
    "channel_link": "https://t.me/ProtidinerKajBD",
    "group_link": "https://t.me/+hb8X-V4buToxYmJl",
    "bot_username": "@ProtidinerKaj_BD_Bot",
    "ad_script_1": "<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>",
    "ad_script_2": "<script src='//libtl.com/sdk.js' data-zone='11798857' data-sdk='show_11798857'></script>",
    "ad_link": "https://omg10.com/4/11760259",
    "support_text": "সমস্যা হলে নিচের ফর্মে লিখুন। অ্যাডমিন যত দ্রুত সম্ভব উত্তর দেবেন।",
    "primary": "#7c3aed",
    "accent": "#06b6d4",
    "background": "#070b1a",
    "maintenance": "0",
}

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def today():
    return date.today().isoformat()

def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init_db():
    c = db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT,
      photo TEXT, balance INTEGER NOT NULL DEFAULT 0, total_earned INTEGER NOT NULL DEFAULT 0,
      total_withdrawn INTEGER NOT NULL DEFAULT 0, referral_by INTEGER, referral_count INTEGER NOT NULL DEFAULT 0,
      banned INTEGER NOT NULL DEFAULT 0, joined_at TEXT NOT NULL, last_active TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS money_ledger(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, amount INTEGER NOT NULL,
      reason TEXT NOT NULL, ref_id TEXT, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS diamonds(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, amount INTEGER NOT NULL,
      reason TEXT NOT NULL, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS levels(
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, min_earned INTEGER NOT NULL,
      diamond_reward INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS tasks(
      id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT,
      url TEXT, reward INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1,
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS task_claims(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, task_id INTEGER NOT NULL,
      claimed_at TEXT NOT NULL, UNIQUE(user_id, task_id)
    );
    CREATE TABLE IF NOT EXISTS daily_claims(
      user_id INTEGER NOT NULL, claim_date TEXT NOT NULL, reward INTEGER NOT NULL,
      PRIMARY KEY(user_id, claim_date)
    );
    CREATE TABLE IF NOT EXISTS ad_claims(
      user_id INTEGER NOT NULL, claim_date TEXT NOT NULL, count INTEGER NOT NULL DEFAULT 0,
      PRIMARY KEY(user_id, claim_date)
    );
    CREATE TABLE IF NOT EXISTS ad_sessions(
      token TEXT PRIMARY KEY, user_id INTEGER NOT NULL, created_at INTEGER NOT NULL,
      expires_at INTEGER NOT NULL, used INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS withdrawals(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, method TEXT NOT NULL,
      account TEXT NOT NULL, amount INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
      admin_note TEXT, created_at TEXT NOT NULL, processed_at TEXT
    );
    CREATE TABLE IF NOT EXISTS support(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, message TEXT NOT NULL,
      reply TEXT, status TEXT NOT NULL DEFAULT 'open', created_at TEXT NOT NULL, replied_at TEXT
    );
    """)
    for k,v in DEFAULTS.items():
        c.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)", (k,v))
    if c.execute("SELECT COUNT(*) FROM levels").fetchone()[0] == 0:
        c.executemany("INSERT INTO levels(name,min_earned,diamond_reward) VALUES(?,?,?)", [
            ("Bronze",0,0),("Silver",1000,10),("Gold",5000,25),("Platinum",15000,50),("Diamond",50000,100)
        ])
    c.commit(); c.close()

def setting(k):
    c=db(); r=c.execute("SELECT value FROM settings WHERE key=?", (k,)).fetchone(); c.close()
    return r["value"] if r else DEFAULTS.get(k,"")

def set_setting(k,v):
    c=db(); c.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(k,str(v))); c.commit(); c.close()

def paisa(x):
    d=Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(d*100)

def money(x):
    return f"{Decimal(x)/100:.2f}".rstrip("0").rstrip(".")

def user_row(uid):
    c=db(); r=c.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone(); c.close(); return r

def diamond_balance(uid):
    c=db(); r=c.execute("SELECT COALESCE(SUM(amount),0) n FROM diamonds WHERE user_id=?", (uid,)).fetchone(); c.close(); return r["n"]

def current_level(uid):
    u=user_row(uid)
    c=db(); r=c.execute("SELECT * FROM levels WHERE active=1 AND min_earned<=? ORDER BY min_earned DESC LIMIT 1",(u["total_earned"],)).fetchone(); c.close()
    return r

def add_money(uid, amount, reason, ref_id=""):
    if amount == 0: return
    c=db()
    c.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+?, last_active=? WHERE id=?",(amount, max(amount,0), now(), uid))
    c.execute("INSERT INTO money_ledger(user_id,amount,reason,ref_id,created_at) VALUES(?,?,?,?,?)",(uid,amount,reason,ref_id,now()))
    c.commit(); c.close()

def add_diamond(uid, amount, reason):
    if amount == 0: return
    c=db(); c.execute("INSERT INTO diamonds(user_id,amount,reason,created_at) VALUES(?,?,?,?)",(uid,amount,reason,now())); c.commit(); c.close()

def telegram_validate(init_data):
    if not BOT_TOKEN:
        return None
    try:
        vals=dict(parse_qsl(init_data, keep_blank_values=True))
        supplied=vals.pop("hash", None)
        if not supplied: return None
        data_check="\n".join(f"{k}={vals[k]}" for k in sorted(vals))
        secret=hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calc=hmac.new(secret,data_check.encode(),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc,supplied): return None
        if int(time.time())-int(vals.get("auth_date","0")) > 86400: return None
        u=json.loads(vals.get("user","{}"))
        return u, vals.get("start_param","")
    except Exception:
        return None

def demo_or_telegram_user():
    init_data=request.headers.get("X-Telegram-Init-Data","")
    if init_data and BOT_TOKEN:
        v=telegram_validate(init_data)
        if v: return v
        return None
    # Development/demo mode only. Production should set BOT_TOKEN.
    uid=request.headers.get("X-Demo-User-ID") or request.args.get("id")
    if uid and uid.isdigit():
        return {"id":int(uid),"username":"demo_user","first_name":"Demo"}, ""
    return None

def ensure_user(tg, start_param=""):
    uid=int(tg["id"]); c=db()
    r=c.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone()
    if not r:
        ref=None
        if start_param.startswith("ref_") and start_param[4:].isdigit():
            x=int(start_param[4:])
            if x != uid and c.execute("SELECT id FROM users WHERE id=?",(x,)).fetchone(): ref=x
        c.execute("""INSERT INTO users(id,username,first_name,last_name,photo,referral_by,joined_at,last_active)
                     VALUES(?,?,?,?,?,?,?,?)""",(uid,tg.get("username",""),tg.get("first_name",""),tg.get("last_name",""),
                     tg.get("photo_url",""),ref,now(),now()))
        c.commit()
        if ref:
            c.execute("UPDATE users SET referral_count=referral_count+1 WHERE id=?",(ref,)); c.commit()
            add_money(ref,paisa(setting("referral_reward")),"Referral reward",str(uid))
            add_diamond(ref,int(setting("referral_diamond") or 0),"Referral diamond")
    else:
        c.execute("""UPDATE users SET username=?,first_name=?,last_name=?,last_active=?,
                     photo=CASE WHEN photo='' OR photo IS NULL THEN ? ELSE photo END WHERE id=?""",
                  (tg.get("username",""),tg.get("first_name",""),tg.get("last_name",""),now(),tg.get("photo_url",""),uid))
        c.commit()
    c.close()
    return uid

def auth(f):
    @wraps(f)
    def w(*a,**kw):
        x=demo_or_telegram_user()
        if not x: return jsonify({"ok":False,"error":"Telegram authentication failed"}),401
        uid=ensure_user(*x)
        u=user_row(uid)
        if u["banned"]: return jsonify({"ok":False,"error":"আপনার অ্যাকাউন্ট সাময়িকভাবে বন্ধ আছে।"}),403
        return f(uid,*a,**kw)
    return w

def admin_ok():
    q=request.args.get("key","")
    if ADMIN_SECRET and hmac.compare_digest(q,ADMIN_SECRET): return True
    return request.args.get("id","") == str(ADMIN_ID)

@APP.route("/")
def index():
    return "Protidiner Kaj BD API is running."

USER_HTML = r"""<!doctype html>
<html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>{{app}}</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
:root{--p:{{primary}};--a:{{accent}};--bg:{{background}};--card:rgba(18,25,52,.78);--line:rgba(255,255,255,.09);--txt:#f8fafc;--muted:#a7b0c4}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 20% 0%,rgba(124,58,237,.25),transparent 35%),radial-gradient(circle at 100% 20%,rgba(6,182,212,.18),transparent 30%),var(--bg);color:var(--txt);font-family:system-ui,-apple-system,Segoe UI,sans-serif;min-height:100vh}
.wrap{max-width:560px;margin:auto;padding:14px 14px 92px}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.brand{font-weight:800;font-size:20px}.online{font-size:11px;color:#67e8f9;background:rgba(6,182,212,.1);padding:7px 10px;border:1px solid rgba(103,232,249,.2);border-radius:999px}
.hero{padding:20px;border:1px solid var(--line);border-radius:26px;background:linear-gradient(135deg,rgba(124,58,237,.92),rgba(37,99,235,.72) 55%,rgba(6,182,212,.62));box-shadow:0 18px 50px rgba(0,0,0,.3);position:relative;overflow:hidden}.hero:after{content:"";position:absolute;width:170px;height:170px;border-radius:50%;right:-50px;top:-60px;background:rgba(255,255,255,.1);filter:blur(2px)}
.small{font-size:12px;color:#dbeafe}.bal{font-size:38px;font-weight:900;margin:6px 0}.herorow{display:flex;gap:10px;position:relative;z-index:2}.mini{flex:1;background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.14);padding:11px;border-radius:16px}.mini b{display:block;font-size:16px;margin-top:3px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-top:13px}.card{background:var(--card);border:1px solid var(--line);border-radius:21px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.16);backdrop-filter:blur(12px)}.wide{grid-column:1/-1}.title{font-size:16px;font-weight:800;margin-bottom:10px}.muted{color:var(--muted);font-size:12px;line-height:1.55}
button,.btn{border:0;color:white;background:linear-gradient(135deg,var(--p),#2563eb);padding:12px 14px;border-radius:14px;font-weight:800;cursor:pointer;width:100%;box-shadow:0 8px 22px rgba(37,99,235,.22)}button.alt{background:rgba(255,255,255,.07);border:1px solid var(--line);box-shadow:none}button.green{background:linear-gradient(135deg,#059669,#06b6d4)}button.danger{background:linear-gradient(135deg,#dc2626,#be123c)}
input,textarea,select{width:100%;background:#0d142b;color:white;border:1px solid var(--line);border-radius:14px;padding:13px;font:inherit;outline:none}textarea{min-height:125px;resize:vertical}.row{display:flex;gap:9px}.row>*{flex:1}.progress{height:10px;background:#0b1124;border-radius:99px;overflow:hidden}.bar{height:100%;background:linear-gradient(90deg,var(--a),var(--p));border-radius:99px}.task{display:flex;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}.task:last-child{border:0}.ico{width:44px;height:44px;display:grid;place-items:center;border-radius:15px;background:rgba(124,58,237,.16);font-size:22px}.taskmain{flex:1}.taskmain b{display:block}.taskmain span{font-size:11px;color:#a7b0c4}.bottom{position:fixed;left:50%;bottom:9px;transform:translateX(-50%);width:min(532px,calc(100% - 18px));display:grid;grid-template-columns:repeat(5,1fr);gap:6px;background:rgba(8,12,29,.92);border:1px solid var(--line);padding:7px;border-radius:21px;backdrop-filter:blur(18px);z-index:20}.nav{background:transparent!important;box-shadow:none!important;border:0!important;padding:8px 2px!important;color:#93a4c3!important;font-size:10px}.nav.active{color:#fff!important;background:rgba(124,58,237,.18)!important}.nav i{display:block;font-style:normal;font-size:19px;margin-bottom:2px}.hidden{display:none}.avatar{width:76px;height:76px;border-radius:24px;object-fit:cover;border:2px solid rgba(255,255,255,.18);background:#151c36}.toast{position:fixed;top:15px;left:50%;transform:translateX(-50%);background:#111827;color:white;padding:12px 16px;border-radius:14px;z-index:50;display:none;border:1px solid var(--line)}
</style></head><body><div class="wrap">
<div class="top"><div class="brand">💎 {{app}}</div><div class="online">● ONLINE</div></div>
<div id="toast" class="toast"></div>
<section id="home">
<div class="hero"><div class="small">আপনার বর্তমান ব্যালেন্স</div><div class="bal" id="bal">৳0</div><div class="heroRow heroRow"><div class="mini"><span class="small">💎 {{diamond}}</span><b id="dia">0</b></div><div class="mini"><span class="small">🏆 Level</span><b id="level">Bronze</b></div></div></div>
<div class="grid"><div class="card"><div class="title">📺 আজকের Ads</div><div class="muted"><b id="ads">0/0</b> দেখা হয়েছে</div><div class="progress" style="margin:10px 0"><div class="bar" id="adbar" style="width:0%"></div></div><button onclick="watchAd()">▶️ Ad দেখুন</button></div>
<div class="card"><div class="title">🎁 Daily Bonus</div><div class="muted">প্রতিদিন একবার বোনাস</div><button class="green" onclick="bonus()">আজকের বোনাস</button></div>
<div class="card wide"><div class="title">🚀 দ্রুত শুরু করুন</div><div class="row"><button onclick="show('tasks')">💰 কাজ</button><button onclick="show('ref')">👥 Invite</button></div></div></div></section>
<section id="tasks" class="hidden"><div class="card"><div class="title">💰 Earning Tasks</div><div id="tasklist"></div></div></section>
<section id="ref" class="hidden"><div class="card"><div class="title">👥 Referral Center</div><div class="muted">আপনার লিংক শেয়ার করে বন্ধু আনুন এবং {{diamond}} ও রিওয়ার্ড পান।</div><input id="reflink" readonly style="margin:12px 0"><div class="row"><button onclick="copyRef()">📋 Copy</button><button class="green" onclick="shareRef()">📤 Share</button></div><div class="card" style="margin-top:12px;background:rgba(124,58,237,.08)"><b id="refcount">0</b> জন আপনার মাধ্যমে যুক্ত হয়েছে</div></div></section>
<section id="withdraw" class="hidden"><div class="card"><div class="title">💸 Withdraw</div><div class="muted">Minimum: {{currency}}<span id="minw">100</span></div><input id="wamount" type="number" placeholder="টাকার পরিমাণ" style="margin:12px 0"><select id="wmethod"><option>bKash</option><option>Nagad</option><option>Rocket</option></select><input id="waccount" placeholder="অ্যাকাউন্ট নম্বর" style="margin:10px 0"><button onclick="withdraw()">Withdraw Request</button><div id="whistory" style="margin-top:15px"></div></div></section>
<section id="profile" class="hidden"><div class="card"><div class="title">👤 My Profile</div><div class="row" style="align-items:center"><img id="avatar" class="avatar" src=""><div><b id="pname"></b><div class="muted" id="puser"></div></div></div><input type="file" id="photo" accept="image/*" style="margin:14px 0"><button onclick="uploadPhoto()">📸 Profile Photo Save</button><div class="grid" style="margin-top:14px"><div class="mini card">💰 Earned <b id="earned">৳0</b></div><div class="mini card">👥 Referral <b id="rnum">0</b></div></div></div>
<div class="card" style="margin-top:12px"><div class="title">💬 Support</div><div class="muted">{{support}}</div><textarea id="supportmsg" placeholder="আপনার সমস্যাটি বিস্তারিত লিখুন..."></textarea><button style="margin-top:9px" onclick="support()">Send Message</button></div></section>
</div><div class="bottom">
<button class="nav active" onclick="show('home',this)"><i>⌂</i>Home</button><button class="nav" onclick="show('tasks',this)"><i>⚡</i>Earn</button><button class="nav" onclick="show('ref',this)"><i>💎</i>Diamond</button><button class="nav" onclick="show('withdraw',this)"><i>💸</i>Withdraw</button><button class="nav" onclick="show('profile',this)"><i>👤</i>Profile</button>
</div>
<script>
const tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand()}
const H=()=>({'Content-Type':'application/json','X-Telegram-Init-Data':tg?.initData||''});
async function api(url,opt={}){let r=await fetch(url,{...opt,headers:{...H(),...(opt.headers||{})}});let j=await r.json();if(!j.ok&&j.error)toast(j.error);return j}
function toast(s){let x=document.getElementById('toast');x.textContent=s;x.style.display='block';setTimeout(()=>x.style.display='none',2400)}
function show(id,el){['home','tasks','ref','withdraw','profile'].forEach(x=>document.getElementById(x).classList.toggle('hidden',x!==id));document.querySelectorAll('.nav').forEach(x=>x.classList.remove('active'));if(el)el.classList.add('active'); if(id==='tasks')loadTasks();if(id==='withdraw')loadWithdraw()}
async function load(){let j=await api('/api/me');if(!j.ok)return;let u=j.user;document.getElementById('bal').textContent='{{currency}}'+u.balance;document.getElementById('dia').textContent=u.diamonds;document.getElementById('level').textContent=u.level;document.getElementById('ads').textContent=u.ads+' / '+u.ad_limit;document.getElementById('adbar').style.width=(u.ad_limit?Math.min(100,u.ads/u.ad_limit*100):0)+'%';document.getElementById('refcount').textContent=u.referrals;document.getElementById('rnum').textContent=u.referrals;document.getElementById('earned').textContent='{{currency}}'+u.earned;document.getElementById('pname').textContent=(u.first_name+' '+(u.last_name||'')).trim();document.getElementById('puser').textContent=u.username?'@'+u.username:'Telegram User';document.getElementById('avatar').src=u.photo||'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2276%22 height=%2276%22><rect width=%22100%%22 height=%22100%%22 rx=%2224%22 fill=%22%23151c36%22/><text x=%2250%%22 y=%2258%%22 text-anchor=%22middle%22 font-size=%2230%22>👤</text></svg>';document.getElementById('reflink').value='https://t.me/{{bot}}?start=ref_'+u.id;document.getElementById('minw').textContent='{{minw}}'}
async function loadTasks(){let j=await api('/api/tasks');if(!j.ok)return;document.getElementById('tasklist').innerHTML=j.tasks.length?j.tasks.map(t=>`<div class="task"><div class="ico">⚡</div><div class="taskmain"><b>${esc(t.title)}</b><span>${esc(t.description||'')} · +{{currency}}${t.reward}</span></div>${t.claimed?'<button class="alt" disabled>✓ Done</button>':`<button onclick="claim(${t.id},'${esc(t.url||'')}')">Start</button>`}</div>`).join(''):'<div class="muted">এখন কোনো কাজ নেই।</div>'}
function esc(s){return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll("'","&#039;")}
async function claim(id,url){if(url)window.open(url,'_blank');let j=await api('/api/task/claim',{method:'POST',body:JSON.stringify({task_id:id})});if(j.ok){toast('কাজের রিওয়ার্ড যোগ হয়েছে');load()}}
async function bonus(){let j=await api('/api/bonus',{method:'POST'});if(j.ok){toast('🎁 Bonus যোগ হয়েছে');load()}}
async function watchAd(){let s=await api('/api/ad/start',{method:'POST'});if(!s.ok)return;try{let ok=false;let fn=window['show_11764581'];if(typeof fn==='function'){let r=fn();if(r&&typeof r.then==='function')await r;ok=true}else{let fn2=window['show_11798857'];if(typeof fn2==='function'){let r=fn2();if(r&&typeof r.then==='function')await r;ok=true}}if(!ok){toast('Ad provider এখনো লোড হয়নি, আবার চেষ্টা করুন');return}let j=await api('/api/ad/claim',{method:'POST',body:JSON.stringify({token:s.token})});if(j.ok){toast('🎉 Ad reward যোগ হয়েছে');load()}}catch(e){toast('Ad সম্পন্ন হয়নি')}}
async function withdraw(){let a=document.getElementById('wamount').value,m=document.getElementById('wmethod').value,ac=document.getElementById('waccount').value.trim();let j=await api('/api/withdraw',{method:'POST',body:JSON.stringify({amount:a,method:m,account:ac})});if(j.ok){toast('Withdrawal request পাঠানো হয়েছে');document.getElementById('wamount').value='';load();loadWithdraw()}}
async function loadWithdraw(){let j=await api('/api/withdrawals');if(j.ok)document.getElementById('whistory').innerHTML=j.items.map(x=>`<div class="task"><div class="taskmain"><b>{{currency}}${x.amount} · ${x.method}</b><span>${x.status} · ${x.created_at}</span></div></div>`).join('')||'<div class="muted">কোনো withdrawal নেই।</div>'}
async function support(){let m=document.getElementById('supportmsg').value.trim();if(!m)return toast('মেসেজ লিখুন');let j=await api('/api/support',{method:'POST',body:JSON.stringify({message:m})});if(j.ok){toast('মেসেজ পাঠানো হয়েছে');document.getElementById('supportmsg').value=''}}
async function uploadPhoto(){let f=document.getElementById('photo').files[0];if(!f)return toast('ছবি নির্বাচন করুন');let im=new Image(),rd=new FileReader();rd.onload=()=>{im.onload=async()=>{let c=document.createElement('canvas'),z=Math.min(1,256/Math.max(im.width,im.height));c.width=im.width*z;c.height=im.height*z;c.getContext('2d').drawImage(im,0,0,c.width,c.height);let j=await api('/api/profile/photo',{method:'POST',body:JSON.stringify({photo:c.toDataURL('image/jpeg',.78)})});if(j.ok){toast('Profile photo save হয়েছে');load()}};im.src=rd.result};rd.readAsDataURL(f)}
function copyRef(){navigator.clipboard.writeText(document.getElementById('reflink').value);toast('লিংক কপি হয়েছে')}
function shareRef(){let u=document.getElementById('reflink').value;let t='প্রতিদিনের কাজ BD-তে যোগ দিন এবং কাজ করে রিওয়ার্ড নিন!';if(tg?.openTelegramLink)tg.openTelegramLink('https://t.me/share/url?url='+encodeURIComponent(u)+'&text='+encodeURIComponent(t));else window.open('https://t.me/share/url?url='+encodeURIComponent(u)+'&text='+encodeURIComponent(t),'_blank')}
load()
</script></body></html>"""

@APP.route("/app")
def app_page():
    return render_template_string(USER_HTML, app=setting("app_name"),currency=setting("currency"),diamond=setting("diamond_name"),
        primary=setting("primary"),accent=setting("accent"),background=setting("background"),support=setting("support_text"),
        bot=setting("bot_username").lstrip("@"),minw=money(paisa(setting("min_withdraw"))))

@APP.route("/api/me")
@auth
def me(uid):
    u=user_row(uid); c=db(); a=c.execute("SELECT count FROM ad_claims WHERE user_id=? AND claim_date=?",(uid,today())).fetchone()
    ref=c.execute("SELECT referral_count FROM users WHERE id=?",(uid,)).fetchone()["referral_count"]; c.close()
    lv=current_level(uid)
    return jsonify(ok=True,user={"id":uid,"username":u["username"],"first_name":u["first_name"],"last_name":u["last_name"],
      "photo":u["photo"],"balance":money(u["balance"]),"earned":money(u["total_earned"]),"diamonds":diamond_balance(uid),
      "level":lv["name"] if lv else "Beginner","referrals":ref,"ads":a["count"] if a else 0,"ad_limit":int(setting("ad_daily_limit") or 0)})

@APP.route("/api/tasks")
@auth
def tasks(uid):
    c=db(); rows=c.execute("""SELECT t.*,CASE WHEN tc.id IS NULL THEN 0 ELSE 1 END claimed
       FROM tasks t LEFT JOIN task_claims tc ON tc.task_id=t.id AND tc.user_id=? WHERE t.active=1 ORDER BY t.id DESC""",(uid,)).fetchall();c.close()
    return jsonify(ok=True,tasks=[{"id":r["id"],"title":r["title"],"description":r["description"],"url":r["url"],"reward":money(r["reward"]),"claimed":bool(r["claimed"])} for r in rows])

@APP.route("/api/task/claim",methods=["POST"])
@auth
def task_claim(uid):
    tid=int((request.json or {}).get("task_id",0)); c=db()
    t=c.execute("SELECT * FROM tasks WHERE id=? AND active=1",(tid,)).fetchone()
    if not t: c.close(); return jsonify(ok=False,error="Task পাওয়া যায়নি")
    try:
        c.execute("INSERT INTO task_claims(user_id,task_id,claimed_at) VALUES(?,?,?)",(uid,tid,now()));c.commit()
    except sqlite3.IntegrityError:
        c.close();return jsonify(ok=False,error="এই কাজটি আগে করা হয়েছে")
    c.close();add_money(uid,t["reward"],"Task reward",str(tid));return jsonify(ok=True)

@APP.route("/api/bonus",methods=["POST"])
@auth
def bonus(uid):
    c=db()
    try:c.execute("INSERT INTO daily_claims(user_id,claim_date,reward) VALUES(?,?,?)",(uid,today(),paisa(setting("daily_bonus"))));c.commit()
    except sqlite3.IntegrityError:c.close();return jsonify(ok=False,error="আজকের Bonus নেওয়া হয়ে গেছে")
    c.close();add_money(uid,paisa(setting("daily_bonus")),"Daily bonus");return jsonify(ok=True)

@APP.route("/api/ad/start",methods=["POST"])
@auth
def ad_start(uid):
    limit=int(setting("ad_daily_limit") or 0); c=db(); r=c.execute("SELECT count FROM ad_claims WHERE user_id=? AND claim_date=?",(uid,today())).fetchone(); n=r["count"] if r else 0
    if n>=limit:c.close();return jsonify(ok=False,error="আজকের Ad limit শেষ")
    token=secrets.token_urlsafe(32); ts=int(time.time());c.execute("INSERT INTO ad_sessions VALUES(?,?,?,?,0)",(token,uid,ts,ts+600));c.commit();c.close();return jsonify(ok=True,token=token)

@APP.route("/api/ad/claim",methods=["POST"])
@auth
def ad_claim(uid):
    token=(request.json or {}).get("token",""); c=db();s=c.execute("SELECT * FROM ad_sessions WHERE token=? AND user_id=?",(token,uid)).fetchone()
    if not s or s["used"] or s["expires_at"]<int(time.time()):c.close();return jsonify(ok=False,error="Ad session invalid/expired")
    r=c.execute("SELECT count FROM ad_claims WHERE user_id=? AND claim_date=?",(uid,today())).fetchone();n=r["count"] if r else 0;limit=int(setting("ad_daily_limit") or 0)
    if n>=limit:c.close();return jsonify(ok=False,error="আজকের Ad limit শেষ")
    c.execute("UPDATE ad_sessions SET used=1 WHERE token=?",(token,))
    if r:c.execute("UPDATE ad_claims SET count=count+1 WHERE user_id=? AND claim_date=?",(uid,today()))
    else:c.execute("INSERT INTO ad_claims(user_id,claim_date,count) VALUES(?,?,1)",(uid,today()))
    c.commit();c.close();add_money(uid,paisa(setting("ad_reward")),"Ad reward");return jsonify(ok=True)

@APP.route("/api/withdraw",methods=["POST"])
@auth
def withdraw(uid):
    d=request.json or {}; amount=paisa(d.get("amount",0));method=str(d.get("method","")).strip();account=str(d.get("account","")).strip()
    minw=paisa(setting("min_withdraw"))
    if amount<minw:return jsonify(ok=False,error=f"Minimum withdrawal {setting('currency')}{money(minw)}")
    if not method or len(account)<5:return jsonify(ok=False,error="Method ও account ঠিকভাবে দিন")
    c=db();u=c.execute("SELECT balance FROM users WHERE id=?",(uid,)).fetchone()
    if u["balance"]<amount:c.close();return jsonify(ok=False,error="পর্যাপ্ত ব্যালেন্স নেই")
    c.execute("UPDATE users SET balance=balance-? WHERE id=?",(amount,uid))
    c.execute("INSERT INTO withdrawals(user_id,method,account,amount,created_at) VALUES(?,?,?,?,?)",(uid,method,account,amount,now()))
    c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/withdrawals")
@auth
def withdrawals(uid):
    c=db();rows=c.execute("SELECT * FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 20",(uid,)).fetchall();c.close()
    return jsonify(ok=True,items=[{"amount":money(x["amount"]),"method":x["method"],"status":x["status"],"created_at":x["created_at"]} for x in rows])

@APP.route("/api/support",methods=["POST"])
@auth
def support(uid):
    m=str((request.json or {}).get("message","")).strip()
    if not m:return jsonify(ok=False,error="Message লিখুন")
    c=db();c.execute("INSERT INTO support(user_id,message,created_at) VALUES(?,?,?)",(uid,m,now()));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/profile/photo",methods=["POST"])
@auth
def photo(uid):
    p=str((request.json or {}).get("photo",""))
    if not p.startswith("data:image/"):return jsonify(ok=False,error="Invalid image")
    if len(p)>450000:return jsonify(ok=False,error="ছবিটি অনেক বড়")
    c=db();c.execute("UPDATE users SET photo=? WHERE id=?",(p,uid));c.commit();c.close();return jsonify(ok=True)

ADMIN_HTML = r"""<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin • {{app}}</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#070b1a;color:#f8fafc;font-family:system-ui,-apple-system,Segoe UI,sans-serif}.wrap{max-width:1250px;margin:auto;padding:22px}.head{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.brand{font-size:25px;font-weight:900}.tag{background:linear-gradient(135deg,#7c3aed,#06b6d4);padding:9px 14px;border-radius:999px}.tabs{display:flex;gap:8px;overflow:auto;margin-bottom:14px}.tab{white-space:nowrap;padding:11px 15px;border-radius:13px;background:#11182f;border:1px solid #24304d;color:#cbd5e1;cursor:pointer}.tab.on{background:linear-gradient(135deg,#7c3aed,#2563eb);color:white}.panel{background:rgba(17,24,39,.82);border:1px solid #24304d;border-radius:20px;padding:18px;box-shadow:0 15px 40px rgba(0,0,0,.18)}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.stat{padding:17px;border-radius:17px;background:linear-gradient(135deg,rgba(124,58,237,.17),rgba(6,182,212,.08));border:1px solid #26324e}.stat small{color:#94a3b8}.stat b{display:block;font-size:25px;margin-top:4px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px;border-bottom:1px solid #202b45;font-size:13px}input,textarea,select{width:100%;background:#0b1124;color:white;border:1px solid #293552;border-radius:12px;padding:11px;margin:4px 0}button{border:0;border-radius:11px;padding:10px 13px;background:linear-gradient(135deg,#7c3aed,#2563eb);color:white;font-weight:800;cursor:pointer}.danger{background:#be123c}.green{background:#059669}.muted{color:#94a3b8;font-size:12px}.section{display:none}.section.on{display:block}.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}.wide{grid-column:1/-1}@media(max-width:800px){.grid{grid-template-columns:1fr 1fr}.row{grid-template-columns:1fr}.wrap{padding:12px}table{min-width:800px}.scroll{overflow:auto}} 
</style></head><body><div class="wrap"><div class="head"><div class="brand">💎 {{app}} <span style="font-size:12px;color:#94a3b8">ADMIN CONTROL CENTER</span></div><div class="tag">A → Z</div></div>
<div class="tabs"><button class="tab on" onclick="tab('dash',this)">Dashboard</button><button class="tab" onclick="tab('users',this)">Users</button><button class="tab" onclick="tab('tasks',this)">Tasks</button><button class="tab" onclick="tab('levels',this)">Levels</button><button class="tab" onclick="tab('withdraws',this)">Withdrawals</button><button class="tab" onclick="tab('support',this)">Support</button><button class="tab" onclick="tab('settings',this)">Settings</button></div>
<div id="dash" class="section on"><div class="grid" id="stats"></div><div class="panel" style="margin-top:14px"><h3>Quick Control</h3><div class="row"><div><label>Ad daily limit</label><input id="qlimit" type="number"></div><div><label>Ad reward</label><input id="qreward" type="number" step=".01"></div><div><label>Referral reward</label><input id="qref" type="number" step=".01"></div><div><label>Referral diamond</label><input id="qdia" type="number"></div></div><button onclick="saveQuick()">Save Controls</button></div></div>
<div id="users" class="section"><div class="panel"><h3>👥 User Management</h3><input id="search" placeholder="ID / username / নাম দিয়ে খুঁজুন" oninput="loadUsers()"><div class="scroll"><table><thead><tr><th>ID</th><th>User</th><th>Balance</th><th>Earned</th><th>Diamond</th><th>Referrer</th><th>Joined</th><th>Action</th></tr></thead><tbody id="usersbody"></tbody></table></div></div></div>
<div id="tasks" class="section"><div class="panel"><h3>⚡ Task Manager</h3><div class="row"><input id="tt" placeholder="Task title"><input id="tr" placeholder="Reward" type="number" step=".01"><input id="tu" placeholder="URL"><input id="td" placeholder="Description"></div><button onclick="addTask()">+ Add Task</button><div class="scroll" style="margin-top:12px"><table><tbody id="taskbody"></tbody></table></div></div></div>
<div id="levels" class="section"><div class="panel"><h3>🏆 Level System</h3><div class="row"><input id="ln" placeholder="Level name"><input id="lm" type="number" step=".01" placeholder="Minimum earned"><input id="ld" type="number" placeholder="Diamond reward"></div><button onclick="addLevel()">+ Add Level</button><div class="scroll" style="margin-top:12px"><table><tbody id="levelbody"></tbody></table></div></div></div>
<div id="withdraws" class="section"><div class="panel"><h3>💸 Withdrawal Requests</h3><div class="scroll"><table><tbody id="wbody"></tbody></table></div></div></div>
<div id="support" class="section"><div class="panel"><h3>💬 Support Inbox</h3><div id="supportbody"></div></div></div>
<div id="settings" class="section"><div class="panel"><h3>⚙️ All Settings</h3><div class="row" id="settingsform"></div><button onclick="saveSettings()">Save Everything</button><button class="green" onclick="exportCSV()" style="margin-left:7px">Export Users CSV</button></div></div>
</div><script>
const KEY=new URLSearchParams(location.search).get('key')||'';const Q=KEY?'&key='+encodeURIComponent(KEY):'';async function api(u,o={}){let r=await fetch(u+(u.includes('?')?'&':'?')+'id={{admin}}'+Q,{...o,headers:{'Content-Type':'application/json',...(o.headers||{})}});return await r.json()}
function tab(id,el){document.querySelectorAll('.section').forEach(x=>x.classList.remove('on'));document.getElementById(id).classList.add('on');document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));el.classList.add('on');if(id==='dash')loadDash();if(id==='users')loadUsers();if(id==='tasks')loadTasks();if(id==='levels')loadLevels();if(id==='withdraws')loadWithdraws();if(id==='support')loadSupport();if(id==='settings')loadSettings()}
async function loadDash(){let j=await api('/api/admin/stats');document.getElementById('stats').innerHTML=[['Users',j.users],['Active Today',j.active],['Total Balance','৳'+j.balance],['Total Earned','৳'+j.earned],['Withdrawn','৳'+j.withdrawn],['Diamonds','💎'+j.diamonds],['Pending Withdraw',j.pending],['Open Support',j.open_support]].map(x=>`<div class="stat"><small>${x[0]}</small><b>${x[1]}</b></div>`).join('');document.getElementById('qlimit').value=j.ad_limit;document.getElementById('qreward').value=j.ad_reward;document.getElementById('qref').value=j.ref_reward;document.getElementById('qdia').value=j.ref_diamond}
async function saveQuick(){let j=await api('/api/admin/settings',{method:'POST',body:JSON.stringify({ad_daily_limit:qlimit.value,ad_reward:qreward.value,referral_reward:qref.value,referral_diamond:qdia.value})});alert(j.ok?'Saved':'Error')}
async function loadUsers(){let j=await api('/api/admin/users?q='+encodeURIComponent(document.getElementById('search').value));document.getElementById('usersbody').innerHTML=j.users.map(x=>`<tr><td>${x.id}</td><td><b>${x.name}</b><br><span class="muted">${x.username||''}</span></td><td>৳${x.balance}</td><td>৳${x.earned}</td><td>💎${x.diamond}</td><td>${x.ref||'-'}</td><td>${x.joined}</td><td><button onclick="adjust(${x.id})">Adjust</button> <button class="danger" onclick="ban(${x.id},${x.banned?0:1})">${x.banned?'Unban':'Ban'}</button></td></tr>`).join('')}
async function adjust(id){let a=prompt('Balance adjustment (+/- টাকা):','0');if(a===null)return;let d=prompt('Diamond adjustment (+/-):','0');if(d===null)return;let j=await api('/api/admin/user/adjust',{method:'POST',body:JSON.stringify({id,amount:a,diamond:d})});alert(j.ok?'Updated':'Error');loadUsers()}
async function ban(id,b){let j=await api('/api/admin/user/ban',{method:'POST',body:JSON.stringify({id,banned:b})});if(j.ok)loadUsers()}
async function loadTasks(){let j=await api('/api/admin/tasks');document.getElementById('taskbody').innerHTML=j.tasks.map(x=>`<tr><td>${x.title}</td><td>৳${x.reward}</td><td>${x.url||''}</td><td>${x.active?'ON':'OFF'}</td><td><button onclick="toggleTask(${x.id},${x.active?0:1})">Toggle</button><button class="danger" onclick="delTask(${x.id})">Delete</button></td></tr>`).join('')}
async function addTask(){let j=await api('/api/admin/tasks',{method:'POST',body:JSON.stringify({title:tt.value,reward:tr.value,url:tu.value,description:td.value})});if(j.ok){tt.value=tr.value=tu.value=td.value='';loadTasks()}}
async function toggleTask(id,a){await api('/api/admin/tasks/toggle',{method:'POST',body:JSON.stringify({id,active:a})});loadTasks()}async function delTask(id){await api('/api/admin/tasks/delete',{method:'POST',body:JSON.stringify({id})});loadTasks()}
async function loadLevels(){let j=await api('/api/admin/levels');document.getElementById('levelbody').innerHTML=j.levels.map(x=>`<tr><td>${x.name}</td><td>${x.min}</td><td>💎${x.diamond}</td><td><button class="danger" onclick="delLevel(${x.id})">Delete</button></td></tr>`).join('')}
async function addLevel(){let j=await api('/api/admin/levels',{method:'POST',body:JSON.stringify({name:ln.value,min:lm.value,diamond:ld.value})});if(j.ok)loadLevels()}
async function delLevel(id){await api('/api/admin/levels/delete',{method:'POST',body:JSON.stringify({id})});loadLevels()}
async function loadWithdraws(){let j=await api('/api/admin/withdrawals');document.getElementById('wbody').innerHTML=j.items.map(x=>`<tr><td>#${x.id}</td><td>${x.user}</td><td>৳${x.amount}</td><td>${x.method}<br>${x.account}</td><td>${x.status}</td><td>${x.status==='pending'?`<button class="green" onclick="wd(${x.id},'approved')">Approve</button><button class="danger" onclick="wd(${x.id},'rejected')">Reject</button>`:''}</td></tr>`).join('')}
async function wd(id,s){let note=prompt('Admin note','');await api('/api/admin/withdrawals/status',{method:'POST',body:JSON.stringify({id,status:s,note})});loadWithdraws();loadDash()}
async function loadSupport(){let j=await api('/api/admin/support');document.getElementById('supportbody').innerHTML=j.items.map(x=>`<div class="panel" style="margin:9px 0"><b>#${x.id} · ${x.user}</b><div class="muted">${x.created}</div><p>${x.message}</p>${x.reply?'<div style="color:#67e8f9">Reply: '+x.reply+'</div>':`<textarea id="sp${x.id}" placeholder="Reply..."></textarea><button onclick="reply(${x.id})">Reply</button>`}</div>`).join('')}
async function reply(id){let m=document.getElementById('sp'+id).value;await api('/api/admin/support/reply',{method:'POST',body:JSON.stringify({id,reply:m})});loadSupport()}
async function loadSettings(){let j=await api('/api/admin/settings');document.getElementById('settingsform').innerHTML=j.items.map(x=>`<div><label>${x.key}</label><input data-key="${x.key}" value="${String(x.value).replaceAll('"','&quot;')}"></div>`).join('')}
async function saveSettings(){let o={};document.querySelectorAll('#settingsform input').forEach(x=>o[x.dataset.key]=x.value);let j=await api('/api/admin/settings',{method:'POST',body:JSON.stringify(o)});alert(j.ok?'সব Settings Save হয়েছে':'Error')}
function exportCSV(){location.href='/api/admin/export?id={{admin}}'+Q}
loadDash()
</script></body></html>"""

def admin_route():
    if not admin_ok(): return "Unauthorized",401
    return render_template_string(ADMIN_HTML,app=setting("app_name"),admin=ADMIN_ID)

@APP.route("/admin")
def admin(): return admin_route()

def admin_guard(f):
    @wraps(f)
    def w(*a,**kw):
        if not admin_ok(): return jsonify(ok=False,error="Unauthorized"),401
        return f(*a,**kw)
    return w

@APP.route("/api/admin/stats")
@admin_guard
def admin_stats():
    c=db()
    users=c.execute("SELECT COUNT(*) n FROM users").fetchone()["n"];active=c.execute("SELECT COUNT(*) n FROM users WHERE substr(last_active,1,10)=?",(today(),)).fetchone()["n"]
    balance=c.execute("SELECT COALESCE(SUM(balance),0)n FROM users").fetchone()["n"];earned=c.execute("SELECT COALESCE(SUM(total_earned),0)n FROM users").fetchone()["n"];withdrawn=c.execute("SELECT COALESCE(SUM(total_withdrawn),0)n FROM users").fetchone()["n"]
    diamonds=c.execute("SELECT COALESCE(SUM(amount),0)n FROM diamonds").fetchone()["n"];pending=c.execute("SELECT COUNT(*) n FROM withdrawals WHERE status='pending'").fetchone()["n"];open_s=c.execute("SELECT COUNT(*) n FROM support WHERE status='open'").fetchone()["n"];c.close()
    return jsonify(ok=True,users=users,active=active,balance=money(balance),earned=money(earned),withdrawn=money(withdrawn),diamonds=diamonds,pending=pending,open_support=open_s,ad_limit=int(setting("ad_daily_limit")),ad_reward=setting("ad_reward"),ref_reward=setting("referral_reward"),ref_diamond=int(setting("referral_diamond")))

@APP.route("/api/admin/users")
@admin_guard
def admin_users():
    q=request.args.get("q","").strip();c=db()
    if q:
        rows=c.execute("""SELECT u.*,COALESCE((SELECT SUM(amount) FROM diamonds d WHERE d.user_id=u.id),0) diamond
          FROM users u WHERE CAST(u.id AS TEXT)=? OR u.username LIKE ? OR u.first_name LIKE ? OR u.last_name LIKE ? ORDER BY u.id DESC LIMIT 100""",(q,"%"+q+"%","%"+q+"%","%"+q+"%")).fetchall()
    else: rows=c.execute("""SELECT u.*,COALESCE((SELECT SUM(amount) FROM diamonds d WHERE d.user_id=u.id),0) diamond FROM users u ORDER BY u.id DESC LIMIT 100""").fetchall()
    out=[]
    for r in rows:
        ref=c.execute("SELECT username,first_name,id FROM users WHERE id=?",(r["referral_by"],)).fetchone() if r["referral_by"] else None
        out.append({"id":r["id"],"name":(r["first_name"]+" "+(r["last_name"] or "")).strip(),"username":r["username"],"balance":money(r["balance"]),"earned":money(r["total_earned"]),"diamond":r["diamond"],"ref":("@"+ref["username"] if ref and ref["username"] else (ref["first_name"] if ref else "")),"joined":r["joined_at"],"banned":r["banned"]})
    c.close();return jsonify(ok=True,users=out)

@APP.route("/api/admin/user/adjust",methods=["POST"])
@admin_guard
def admin_adjust():
    d=request.json or {};uid=int(d.get("id"));amount=paisa(d.get("amount",0));dia=int(d.get("diamond",0))
    add_money(uid,amount,"Admin adjustment");add_diamond(uid,dia,"Admin diamond adjustment");return jsonify(ok=True)

@APP.route("/api/admin/user/ban",methods=["POST"])
@admin_guard
def admin_ban():
    d=request.json or {};c=db();c.execute("UPDATE users SET banned=? WHERE id=?",(int(d.get("banned",1)),int(d["id"])));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/admin/tasks",methods=["GET","POST"])
@admin_guard
def admin_tasks():
    c=db()
    if request.method=="POST":
        d=request.json or {};c.execute("INSERT INTO tasks(title,description,url,reward,created_at) VALUES(?,?,?,?,?)",(d.get("title",""),d.get("description",""),d.get("url",""),paisa(d.get("reward",0)),now()));c.commit()
    rows=c.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall();c.close()
    return jsonify(ok=True,tasks=[{"id":r["id"],"title":r["title"],"description":r["description"],"url":r["url"],"reward":money(r["reward"]),"active":r["active"]} for r in rows])

@APP.route("/api/admin/tasks/toggle",methods=["POST"])
@admin_guard
def task_toggle():
    d=request.json or {};c=db();c.execute("UPDATE tasks SET active=? WHERE id=?",(int(d["active"]),int(d["id"])));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/admin/tasks/delete",methods=["POST"])
@admin_guard
def task_delete():
    d=request.json or {};c=db();c.execute("DELETE FROM tasks WHERE id=?",(int(d["id"]),));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/admin/levels",methods=["GET","POST"])
@admin_guard
def admin_levels():
    c=db()
    if request.method=="POST":
        d=request.json or {};c.execute("INSERT INTO levels(name,min_earned,diamond_reward) VALUES(?,?,?)",(d.get("name","Level"),paisa(d.get("min",0)),int(d.get("diamond",0))));c.commit()
    rows=c.execute("SELECT * FROM levels ORDER BY min_earned").fetchall();c.close();return jsonify(ok=True,levels=[{"id":r["id"],"name":r["name"],"min":money(r["min_earned"]),"diamond":r["diamond_reward"]} for r in rows])

@APP.route("/api/admin/levels/delete",methods=["POST"])
@admin_guard
def level_delete():
    d=request.json or {};c=db();c.execute("DELETE FROM levels WHERE id=?",(int(d["id"]),));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/admin/withdrawals")
@admin_guard
def admin_withdrawals():
    c=db();rows=c.execute("""SELECT w.*,u.first_name,u.last_name,u.username FROM withdrawals w JOIN users u ON u.id=w.user_id ORDER BY w.id DESC LIMIT 200""").fetchall();c.close()
    return jsonify(ok=True,items=[{"id":r["id"],"user":f'{r["user_id"]} {r["first_name"]} @{r["username"] or ""}',"amount":money(r["amount"]),"method":r["method"],"account":r["account"],"status":r["status"]} for r in rows])

@APP.route("/api/admin/withdrawals/status",methods=["POST"])
@admin_guard
def admin_wstatus():
    d=request.json or {};wid=int(d["id"]);status=d["status"];c=db();w=c.execute("SELECT * FROM withdrawals WHERE id=?",(wid,)).fetchone()
    if not w or w["status"]!="pending":c.close();return jsonify(ok=False,error="Already processed")
    if status=="rejected":c.execute("UPDATE users SET balance=balance+? WHERE id=?",(w["amount"],w["user_id"]))
    elif status=="approved":c.execute("UPDATE users SET total_withdrawn=total_withdrawn+? WHERE id=?",(w["amount"],w["user_id"]))
    else:c.close();return jsonify(ok=False,error="Invalid status")
    c.execute("UPDATE withdrawals SET status=?,admin_note=?,processed_at=? WHERE id=?",(status,d.get("note",""),now(),wid));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/admin/support")
@admin_guard
def admin_support():
    c=db();rows=c.execute("""SELECT s.*,u.first_name,u.username FROM support s JOIN users u ON u.id=s.user_id ORDER BY s.id DESC LIMIT 200""").fetchall();c.close()
    return jsonify(ok=True,items=[{"id":r["id"],"user":f'{r["user_id"]} {r["first_name"]} @{r["username"] or ""}',"message":r["message"],"reply":r["reply"],"created":r["created_at"]} for r in rows])

@APP.route("/api/admin/support/reply",methods=["POST"])
@admin_guard
def admin_reply():
    d=request.json or {};c=db();c.execute("UPDATE support SET reply=?,status='replied',replied_at=? WHERE id=?",(d.get("reply",""),now(),int(d["id"])));c.commit();c.close();return jsonify(ok=True)

@APP.route("/api/admin/settings",methods=["GET","POST"])
@admin_guard
def admin_settings():
    if request.method=="POST":
        for k,v in (request.json or {}).items():
            if k in DEFAULTS:set_setting(k,v)
    c=db();rows=c.execute("SELECT key,value FROM settings ORDER BY key").fetchall();c.close();return jsonify(ok=True,items=[{"key":r["key"],"value":r["value"]} for r in rows])

@APP.route("/api/admin/export")
@admin_guard
def export_users():
    c=db();rows=c.execute("SELECT id,username,first_name,last_name,balance,total_earned,total_withdrawn,referral_by,referral_count,joined_at,last_active,banned FROM users ORDER BY id").fetchall();c.close()
    out=io.StringIO();w=csv.writer(out);w.writerow(rows[0].keys() if rows else ["id"]);[w.writerow(list(r)) for r in rows]
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=users.csv"})

init_db()

if __name__=="__main__":
    APP.run(host="0.0.0.0",port=PORT)
