from pathlib import Path
import zipfile, textwrap, json, os, shutil, re

root = Path("/mnt/data/Protidiner_Kaj_BD_AZ_FINAL")
if root.exists():
    shutil.rmtree(root)
root.mkdir(parents=True)

main_py = r'''# Protidiner Kaj BD — A-Z Telegram Mini App
# Single-file Flask + SQLite starter/production-ready foundation.
# Configure BOT_TOKEN and ADMIN_SECRET as environment variables before deployment.

import os, sqlite3, secrets, hashlib, hmac, json, csv, io, time
from datetime import datetime, date, timedelta
from urllib.parse import parse_qsl, quote
from flask import Flask, request, jsonify, render_template_string, send_file

APP = Flask(__name__)
APP.config["MAX_CONTENT_LENGTH"] = 600 * 1024
DB = os.environ.get("DB_PATH", "protidiner_kaj_bd.sqlite3")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_ID = os.environ.get("ADMIN_ID", "8807178385").strip()
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "").strip()

DEFAULTS = {
    "app_name":"প্রতিদিনের কাজ BD","currency":"৳","daily_bonus":"5",
    "ad_daily_limit":"5","ad_reward":"2","referral_reward":"10","referral_diamond":"5",
    "diamond_name":"Diamond","min_withdraw":"100","channel_link":"https://t.me/ProtidinerKajBD",
    "group_link":"https://t.me/+hb8X-V4buToxYmJl","bot_username":"@ProtidinerKaj_BD_Bot",
    "bot_link":"https://t.me/ProtidinerKaj_BD_Bot",
    "ad_script_1":"<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>",
    "ad_script_2":"<script src='//libtl.com/sdk.js' data-zone='11798857' data-sdk='show_11798857'></script>",
    "ad_link":"https://omg10.com/4/11760259",
    "support_text":"সাপোর্ট প্রয়োজন হলে নিচের বক্সে আপনার সমস্যা লিখে পাঠান।",
    "primary":"#7c3aed","accent":"#06b6d4","background":"#070b1a",
    "welcome_text":"প্রতিদিন কাজ করুন, Diamond ও Balance সংগ্রহ করুন।",
    "maintenance":"0"
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings(k TEXT PRIMARY KEY,v TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY, username TEXT DEFAULT '', first_name TEXT DEFAULT '',
 photo TEXT DEFAULT '', balance INTEGER DEFAULT 0, diamonds INTEGER DEFAULT 0,
 total_earned INTEGER DEFAULT 0, total_withdrawn INTEGER DEFAULT 0, level_id INTEGER DEFAULT 1,
 referrer_id INTEGER, referrals INTEGER DEFAULT 0, banned INTEGER DEFAULT 0,
 created_at TEXT NOT NULL, last_seen TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS ledger(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,amount INTEGER,kind TEXT,note TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS diamond_ledger(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,amount INTEGER,kind TEXT,note TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS tasks(
 id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,description TEXT,reward INTEGER DEFAULT 0,
 diamond_reward INTEGER DEFAULT 0,url TEXT DEFAULT '',daily_limit INTEGER DEFAULT 1,active INTEGER DEFAULT 1,
 created_at TEXT);
CREATE TABLE IF NOT EXISTS task_claims(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,task_id INTEGER,claim_date TEXT,created_at TEXT,
 UNIQUE(user_id,task_id,claim_date));
CREATE TABLE IF NOT EXISTS daily_claims(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,claim_date TEXT,created_at TEXT,
 UNIQUE(user_id,claim_date));
CREATE TABLE IF NOT EXISTS ad_sessions(
 token TEXT PRIMARY KEY,user_id INTEGER,created_at TEXT,expires_at TEXT,used INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS ad_claims(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,claim_date TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS withdrawals(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,amount INTEGER,method TEXT,account TEXT,
 status TEXT DEFAULT 'pending',created_at TEXT,updated_at TEXT);
CREATE TABLE IF NOT EXISTS support(
 id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,message TEXT,reply TEXT DEFAULT '',
 status TEXT DEFAULT 'open',created_at TEXT,replied_at TEXT);
CREATE TABLE IF NOT EXISTS levels(
 id INTEGER PRIMARY KEY, name TEXT, min_earned INTEGER, diamond_bonus INTEGER DEFAULT 0, active INTEGER DEFAULT 1);
"""

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
    c=db(); c.executescript(SCHEMA)
    for k,v in DEFAULTS.items():
        c.execute("INSERT OR IGNORE INTO settings(k,v) VALUES(?,?)",(k,v))
    if c.execute("SELECT COUNT(*) n FROM levels").fetchone()["n"]==0:
        c.executemany("INSERT INTO levels(id,name,min_earned,diamond_bonus) VALUES(?,?,?,?)",
                      [(1,"Starter",0,0),(2,"Bronze",5000,5),(3,"Silver",20000,15),(4,"Gold",50000,30),(5,"Diamond",100000,60)])
    if c.execute("SELECT COUNT(*) n FROM tasks").fetchone()["n"]==0:
        now=iso()
        c.execute("""INSERT INTO tasks(title,description,reward,diamond_reward,url,daily_limit,active,created_at)
                     VALUES(?,?,?,?,?,?,?,?)""",
                  ("কমিউনিটি ভিজিট","চ্যানেল/গ্রুপ ভিজিট করে Task সম্পন্ন করুন",2,1,DEFAULTS["channel_link"],1,1,now))
    c.commit(); c.close()

def iso(): return datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
def today(): return date.today().isoformat()
def s(k): 
    c=db(); r=c.execute("SELECT v FROM settings WHERE k=?",(k,)).fetchone(); c.close()
    return r["v"] if r else DEFAULTS.get(k,"")
def money(x): return round(int(x)/100,2)
def paisa(x):
    try:return int(round(float(x)*100))
    except:return 0

def auth_telegram(init_data):
    if not BOT_TOKEN: return None
    try:
        vals=dict(parse_qsl(init_data,keep_blank_values=True))
        check=vals.pop("hash",None)
        if not check:return None
        data="\n".join(f"{k}={vals[k]}" for k in sorted(vals))
        secret=hmac.new(b"WebAppData",BOT_TOKEN.encode(),hashlib.sha256).digest()
        good=hmac.new(secret,data.encode(),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(good,check):return None
        if vals.get("auth_date") and time.time()-int(vals["auth_date"])>86400:return None
        return json.loads(vals["user"])
    except:return None

def current_user():
    init_data=request.headers.get("X-Telegram-Init-Data","")
    u=auth_telegram(init_data)
    if u: return int(u["id"]),u
    # Demo mode is enabled only when BOT_TOKEN is absent.
    if not BOT_TOKEN:
        uid=request.headers.get("X-Demo-User-ID") or request.args.get("id") or "8807178385"
        try:return int(uid),{"id":int(uid),"username":"demo_user","first_name":"Demo User"}
        except:return None,None
    return None,None

def ensure_user():
    uid,tg=current_user()
    if not uid:return None
    c=db(); now=iso()
    old=c.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone()
    if not old:
        ref=None
        start=request.headers.get("X-Telegram-Start-Param","") or request.args.get("start","")
        if start.startswith("ref_"):
            try: ref=int(start[4:])
            except: ref=None
        c.execute("""INSERT INTO users(id,username,first_name,referrer_id,created_at,last_seen)
                     VALUES(?,?,?,?,?,?)""",(uid,tg.get("username",""),tg.get("first_name",""),ref,now,now))
        if ref and ref!=uid and c.execute("SELECT id FROM users WHERE id=?",(ref,)).fetchone():
            rw=paisa(s("referral_reward")); rd=int(s("referral_diamond") or 0)
            if rw:
                c.execute("UPDATE users SET balance=balance+?,total_earned=total_earned+?,referrals=referrals+1 WHERE id=?",(rw,rw,ref))
                c.execute("INSERT INTO ledger(user_id,amount,kind,note,created_at) VALUES(?,?,?,?,?)",(ref,rw,"referral","Referral reward",now))
            if rd:
                c.execute("UPDATE users SET diamonds=diamonds+? WHERE id=?",(rd,ref))
                c.execute("INSERT INTO diamond_ledger(user_id,amount,kind,note,created_at) VALUES(?,?,?,?,?)",(ref,rd,"referral","Referral diamond",now))
    else:
        c.execute("UPDATE users SET username=?,first_name=?,last_seen=? WHERE id=?",
                  (tg.get("username",""),tg.get("first_name",""),now,uid))
    # calculate level
    earned=c.execute("SELECT total_earned FROM users WHERE id=?",(uid,)).fetchone()["total_earned"]
    lv=c.execute("SELECT id FROM levels WHERE min_earned<=? AND active=1 ORDER BY min_earned DESC LIMIT 1",(earned,)).fetchone()
    if lv:c.execute("UPDATE users SET level_id=? WHERE id=?",(lv["id"],uid))
    c.commit(); r=c.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone(); c.close()
    return r

def require_user():
    u=ensure_user()
    if not u: return None, (jsonify({"ok":False,"error":"Telegram authentication required"}),401)
    if u["banned"]: return None,(jsonify({"ok":False,"error":"Account is blocked"}),403)
    return u,None

def add_money(c,uid,amount,kind,note):
    if amount==0:return
    c.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+? WHERE id=?",(amount,max(amount,0),uid))
    c.execute("INSERT INTO ledger(user_id,amount,kind,note,created_at) VALUES(?,?,?,?,?)",(uid,amount,kind,note,iso()))
def add_diamond(c,uid,amount,kind,note):
    if amount:
        c.execute("UPDATE users SET diamonds=diamonds+? WHERE id=?",(amount,uid))
        c.execute("INSERT INTO diamond_ledger(user_id,amount,kind,note,created_at) VALUES(?,?,?,?,?)",(uid,amount,kind,note,iso()))

def admin_ok():
    if ADMIN_SECRET and request.args.get("key")==ADMIN_SECRET:return True
    return request.args.get("id")==ADMIN_ID

USER_HTML = r"""<!doctype html>
<html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>{{app_name}}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<script src="//libtl.com/sdk.js" data-zone="11798857" data-sdk="show_11798857"></script>
<style>
:root{--p:{{primary}};--a:{{accent}};--bg:{{background}}}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 20% 0%,#25115c 0,#0b1028 34%,var(--bg) 75%);color:#fff;font-family:system-ui,-apple-system,Segoe UI,sans-serif;min-height:100vh}button,input,select,textarea{font:inherit}.wrap{max-width:560px;margin:auto;padding:18px 14px 100px}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}.brand{font-weight:900;font-size:20px}.pill{background:#ffffff12;border:1px solid #ffffff1c;border-radius:99px;padding:8px 12px}.glass{background:linear-gradient(145deg,#ffffff13,#ffffff06);border:1px solid #ffffff16;box-shadow:0 16px 45px #0005;backdrop-filter:blur(16px);border-radius:22px}.hero{padding:20px;margin-bottom:12px;position:relative;overflow:hidden}.hero:after{content:"";position:absolute;width:160px;height:160px;border-radius:50%;right:-60px;top:-70px;background:#7c3aed55;filter:blur(10px)}.small{color:#aeb7d5;font-size:13px}.balance{font-size:37px;font-weight:950;margin:7px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.card{padding:16px;margin:10px 0}.value{font-size:22px;font-weight:900;margin-top:5px}.btn{border:0;border-radius:16px;padding:13px 15px;color:white;font-weight:800;cursor:pointer;background:linear-gradient(135deg,var(--p),#2563eb);box-shadow:0 8px 24px #0004}.btn.alt{background:#ffffff10;border:1px solid #ffffff18}.btn.danger{background:#be123c}.full{width:100%}.input,textarea,select{width:100%;background:#080d21;color:#fff;border:1px solid #ffffff18;border-radius:16px;padding:14px;margin:7px 0;outline:none}.task{display:flex;justify-content:space-between;gap:12px;align-items:center}.tag{font-size:12px;padding:5px 8px;border-radius:99px;background:#06b6d422;color:#7dd3fc}.progress{height:8px;background:#ffffff10;border-radius:9px;overflow:hidden}.bar{height:100%;background:linear-gradient(90deg,var(--p),var(--a));width:0}.nav{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);width:min(540px,calc(100% - 20px));display:grid;grid-template-columns:repeat(5,1fr);gap:4px;padding:8px;background:#090d1ddd;border:1px solid #ffffff18;border-radius:22px;backdrop-filter:blur(18px);z-index:9}.nav button{border:0;background:none;color:#aeb7d5;padding:8px 3px;border-radius:14px;font-size:11px}.nav button.active{background:#7c3aed2c;color:#fff}.page{display:none}.page.active{display:block}.photo{width:74px;height:74px;border-radius:50%;object-fit:cover;border:2px solid #ffffff33}.row{display:flex;align-items:center;gap:12px}.hr{height:1px;background:#ffffff10;margin:14px 0}.toast{position:fixed;top:15px;left:50%;transform:translateX(-50%);background:#11182e;border:1px solid #ffffff20;padding:10px 15px;border-radius:99px;display:none;z-index:99}
</style></head><body><div class="toast" id="toast"></div><main class="wrap">
<div class="top"><div class="brand">💎 {{app_name}}</div><div class="pill" id="level">Level 1</div></div>

<section id="home" class="page active">
<div class="glass hero"><div class="small">আপনার Balance</div><div class="balance" id="bal">৳0</div><div class="small">কাজ করুন • Reward নিন • Diamond জমা করুন</div></div>
<div class="grid"><div class="glass card"><div class="small">💎 Diamond</div><div class="value" id="dia">0</div></div><div class="glass card"><div class="small">👥 Referral</div><div class="value" id="refs">0</div></div></div>
<div class="glass card"><div class="row"><div style="font-size:28px">🎁</div><div><b>Daily Bonus</b><div class="small">প্রতিদিন একবার</div></div></div><button class="btn full" style="margin-top:12px" onclick="bonus()">আজকের Bonus নিন</button></div>
<div class="glass card"><b>📺 Daily Ads</b><div class="small" style="margin:7px 0 10px">আজ <span id="ads">0</span> / <span id="adlim">0</span> বিজ্ঞাপন</div><div class="progress"><div class="bar" id="adbar"></div></div><button class="btn full" style="margin-top:12px" onclick="watchAd()">Watch Ad & Earn</button></div>
<div class="glass card"><b>⚡ Quick Start</b><p class="small">{{welcome}}</p><button class="btn alt full" onclick="go('earn')">কাজ শুরু করুন →</button></div>
</section>

<section id="earn" class="page"><div class="glass card"><h2>💰 Earn Tasks</h2><div id="tasks"></div></div></section>
<section id="diamond" class="page"><div class="glass card"><h2>💎 Diamond Center</h2><div class="value" id="d2">0 Diamond</div><div class="hr"></div><div class="small">Referral, Task ও Admin-configured reward থেকে Diamond জমবে।</div><div id="levels" style="margin-top:14px"></div></div>
<div class="glass card"><h3>👥 Referral Center</h3><div class="small">আপনার referral link</div><input class="input" id="ref" readonly><button class="btn full" onclick="shareRef()">Share Referral</button></div></section>

<section id="withdraw" class="page"><div class="glass card"><h2>💸 Withdraw</h2><div class="small">Minimum: ৳<span id="minw">0</span></div><input class="input" id="wamount" type="number" placeholder="Amount"><select id="wmethod" class="input"><option>bKash</option><option>Nagad</option><option>Rocket</option><option>Bank</option></select><input class="input" id="waccount" placeholder="Account / Number"><button class="btn full" onclick="withdraw()">Withdraw Request</button></div><div class="glass card"><h3>Withdrawal History</h3><div id="whistory"></div></div></section>

<section id="profile" class="page"><div class="glass card"><div class="row"><img class="photo" id="photo" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect width='100' height='100' fill='%23141b38'/%3E%3Ctext x='50' y='58' text-anchor='middle' font-size='42' fill='white'%3E%F0%9F%91%A4%3C/text%3E%3C/svg%3E"><div><h2 id="name">User</h2><div class="small" id="uname">@user</div></div></div><input type="file" id="photoFile" accept="image/*" class="input"><button class="btn alt full" onclick="uploadPhoto()">Profile Photo Save</button></div>
<div class="glass card"><h3>🆘 Support</h3><div class="small">{{support}}</div><textarea id="supportMsg" rows="4" placeholder="আপনার সমস্যা লিখুন..."></textarea><button class="btn full" onclick="sendSupport()">Send to Admin</button></div>
<div class="glass card"><h3>🌐 Community</h3><div class="grid"><button class="btn alt" onclick="openUrl('{{channel}}')">Channel</button><button class="btn alt" onclick="openUrl('{{group}}')">Group</button></div></div>
</section></main>
<nav class="nav">{% for x in [('home','⌂','Home'),('earn','⚡','Earn'),('diamond','💎','Diamond'),('withdraw','💸','Withdraw'),('profile','👤','Profile')] %}<button onclick="go('{{x[0]}}')" id="n-{{x[0]}}">{{x[1]}}<br>{{x[2]}}</button>{% endfor %}</nav>
<script>
const tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand()}
const H={'X-Telegram-Init-Data':tg?.initData||''};
async function api(u,opt={}){opt.headers={...(opt.headers||{}),...H};let r=await fetch(u,opt);let j=await r.json();if(!j.ok&&j.error)toast(j.error);return j}
function toast(x){let e=document.getElementById('toast');e.textContent=x;e.style.display='block';setTimeout(()=>e.style.display='none',2200)}
function go(id){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));document.getElementById('n-'+id).classList.add('active');if(id==='earn')loadTasks();if(id==='withdraw')loadW();if(id==='diamond')loadLevels()}
function openUrl(u){if(tg?.openTelegramLink&&u.includes('t.me'))tg.openTelegramLink(u);else window.open(u,'_blank')}
async function load(){let j=await api('/api/me');if(!j.ok)return;let u=j.user;document.getElementById('bal').textContent='৳'+u.balance;document.getElementById('dia').textContent=u.diamonds;document.getElementById('d2').textContent=u.diamonds+' Diamond';document.getElementById('refs').textContent=u.referrals;document.getElementById('level').textContent='Level '+u.level_id;document.getElementById('name').textContent=u.first_name||'User';document.getElementById('uname').textContent=u.username?'@'+u.username:'Telegram User';if(u.photo)document.getElementById('photo').src=u.photo;document.getElementById('ads').textContent=u.ads_today;document.getElementById('adlim').textContent=u.ad_limit;document.getElementById('adbar').style.width=Math.min(100,u.ads_today/u.ad_limit*100)+'%';document.getElementById('minw').textContent=u.min_withdraw;document.getElementById('ref').value=u.referral_link}
async function bonus(){let j=await api('/api/bonus',{method:'POST'});if(j.ok){toast('🎁 Bonus credited');load()}}
async function watchAd(){let st=await api('/api/ad/start',{method:'POST'});if(!st.ok)return;let fn=window['show_11764581']||window['show_11798857'];try{if(fn)await fn();else if(tg?.openLink)tg.openLink('{{ad_link}}');else window.open('{{ad_link}}','_blank')}catch(e){}let j=await api('/api/ad/claim',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:st.token})});if(j.ok){toast('💰 Ad reward credited');load()}}
async function loadTasks(){let j=await api('/api/tasks');let d=document.getElementById('tasks');d.innerHTML='';(j.tasks||[]).forEach(t=>{let e=document.createElement('div');e.className='glass card';e.innerHTML=`<div class="task"><div><b>${t.title}</b><div class="small">${t.description||''}</div><div style="margin-top:7px"><span class="tag">৳${t.reward}</span> <span class="tag">💎${t.diamond_reward}</span></div></div><button class="btn" onclick="claimTask(${t.id},'${encodeURIComponent(t.url||'')}')">Claim</button></div>`;d.appendChild(e)})}
async function claimTask(id,url){if(url){try{openUrl(decodeURIComponent(url))}catch(e){}}let j=await api('/api/task/claim',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:id})});if(j.ok){toast('✅ Task reward added');load();loadTasks()}}
async function loadLevels(){let j=await api('/api/levels');let e=document.getElementById('levels');e.innerHTML=(j.levels||[]).map(x=>`<div class="glass card"><b>${x.name}</b><div class="small">Minimum earned: ৳${x.min_earned} • 💎 bonus ${x.diamond_bonus}</div></div>`).join('')}
async function shareRef(){let u=document.getElementById('ref').value;let share='https://t.me/share/url?url='+encodeURIComponent(u)+'&text='+encodeURIComponent('প্রতিদিনের কাজ BD-তে Join করুন');if(tg?.openTelegramLink)tg.openTelegramLink(share);else navigator.clipboard?.writeText(u);toast('Referral link ready')}
async function withdraw(){let body={amount:document.getElementById('wamount').value,method:document.getElementById('wmethod').value,account:document.getElementById('waccount').value};let j=await api('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(j.ok){toast('Withdrawal submitted');document.getElementById('wamount').value='';document.getElementById('waccount').value='';loadW();load()}}
async function loadW(){let j=await api('/api/withdrawals');document.getElementById('whistory').innerHTML=(j.items||[]).map(x=>`<div class="hr"></div><b>৳${x.amount}</b> • ${x.method}<br><span class="small">${x.account} • ${x.status}</span>`).join('')||'<span class="small">No requests yet.</span>'}
async function sendSupport(){let m=document.getElementById('supportMsg').value.trim();if(!m)return toast('Message লিখুন');let j=await api('/api/support',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});if(j.ok){toast('Sent to admin');document.getElementById('supportMsg').value=''}}
async function uploadPhoto(){let f=document.getElementById('photoFile').files[0];if(!f)return toast('Photo নির্বাচন করুন');if(f.size>450000)return toast('Photo 450KB-এর মধ্যে দিন');let r=new FileReader();r.onload=async()=>{let j=await api('/api/profile/photo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({photo:r.result})});if(j.ok){toast('Photo saved');load()}};r.readAsDataURL(f)}
load();go('home');
</script></body></html>"""

ADMIN_HTML = r"""<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin — {{app_name}}</title><style>
*{box-sizing:border-box}body{margin:0;background:#070b1a;color:#fff;font-family:system-ui;padding:18px}.wrap{max-width:1250px;margin:auto}.tabs{display:flex;gap:8px;overflow:auto;margin:15px 0}.tabs button{white-space:nowrap;border:1px solid #ffffff18;background:#11182d;color:#fff;padding:11px 14px;border-radius:12px}.tab{display:none}.tab.active{display:block}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}.card{background:#ffffff08;border:1px solid #ffffff14;border-radius:18px;padding:16px;margin:10px 0}.kpi{font-size:28px;font-weight:900}.input,textarea,select{width:100%;background:#080d21;color:#fff;border:1px solid #ffffff18;border-radius:12px;padding:11px;margin:5px 0}.btn{border:0;border-radius:12px;padding:10px 13px;background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;font-weight:800}.danger{background:#be123c}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.table{overflow:auto}.table table{width:100%;border-collapse:collapse}.table td,.table th{padding:9px;border-bottom:1px solid #ffffff10;text-align:left;white-space:nowrap}.muted{color:#9da8c7;font-size:13px}
</style></head><body><div class="wrap"><h1>💎 {{app_name}} — Admin Control Center</h1><div class="muted">A-Z Central Control • Admin ID: {{admin_id}}</div>
<div class="tabs">{% for id,name in [('dash','Dashboard'),('users','Users'),('tasks','Tasks'),('levels','Levels'),('withdrawals','Withdrawals'),('support','Support'),('settings','Settings'),('export','Export')] %}<button onclick="tab('{{id}}')">{{name}}</button>{% endfor %}</div>
<section id="dash" class="tab active"><div class="grid" id="stats"></div><div class="card"><h3>⚡ Quick Reward Controls</h3><div class="row"><input class="input" id="adlimit" placeholder="Daily Ads" style="max-width:180px"><input class="input" id="adreward" placeholder="Ad Reward" style="max-width:180px"><input class="input" id="refreward" placeholder="Referral Reward" style="max-width:180px"><input class="input" id="refdia" placeholder="Referral Diamond" style="max-width:180px"><button class="btn" onclick="quickSave()">Save</button></div></div></section>
<section id="users" class="tab"><div class="card"><input class="input" id="useq" placeholder="Search ID / username / name" oninput="users()"><div class="table" id="ut"></div></div></section>
<section id="tasks" class="tab"><div class="card"><h3>Add Task</h3><input class="input" id="tt" placeholder="Title"><input class="input" id="td" placeholder="Description"><input class="input" id="tr" placeholder="Reward ৳"><input class="input" id="tdd" placeholder="Diamond reward"><input class="input" id="tu" placeholder="URL"><input class="input" id="tl" placeholder="Daily limit"><button class="btn" onclick="addTask()">Add Task</button></div><div class="card" id="tasklist"></div></section>
<section id="levels" class="tab"><div class="card"><h3>Add Level</h3><input class="input" id="ln" placeholder="Level name"><input class="input" id="lm" placeholder="Minimum earned ৳"><input class="input" id="ld" placeholder="Diamond bonus"><button class="btn" onclick="addLevel()">Add Level</button></div><div class="card" id="levellist"></div></section>
<section id="withdrawals" class="tab"><div class="card"><button class="btn" onclick="withdrawals()">Refresh</button><div class="table" id="wt"></div></div></section>
<section id="support" class="tab"><div class="card"><div class="table" id="st"></div></div></section>
<section id="settings" class="tab"><div class="card"><div id="settingsBox"></div><button class="btn" onclick="saveSettings()">Save ALL Settings</button></div></section>
<section id="export" class="tab"><div class="card"><h3>Export Data</h3><button class="btn" onclick="location.href='/api/admin/export?id={{admin_id}}{% if key %}&key={{key}}{% endif %}'">Download CSV</button><p class="muted">Users, ledger, withdrawals and support data export.</p></div></section></div>
<script>
const KEY=new URLSearchParams(location.search).get('key')||'';const ID='{{admin_id}}';function q(u){return u+'?id='+ID+(KEY?'&key='+encodeURIComponent(KEY):'')}async function api(u,o={}){let r=await fetch(q(u),o);return await r.json()}function tab(id){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');if(id==='dash')stats();if(id==='users')users();if(id==='tasks')tasks();if(id==='levels')levels();if(id==='withdrawals')withdrawals();if(id==='support')support();if(id==='settings')settings()}
async function stats(){let j=await api('/api/admin/stats');document.getElementById('stats').innerHTML=Object.entries(j).filter(([k])=>k!=='ok').map(([k,v])=>`<div class="card"><div class="muted">${k}</div><div class="kpi">${v}</div></div>`).join('');document.getElementById('adlimit').value=j.ad_daily_limit;document.getElementById('adreward').value=j.ad_reward;document.getElementById('refreward').value=j.referral_reward;document.getElementById('refdia').value=j.referral_diamond}
async function quickSave(){let vals={ad_daily_limit:adlimit.value,ad_reward:adreward.value,referral_reward:refreward.value,referral_diamond:refdia.value};await api('/api/admin/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(vals)});stats()}
async function users(){let j=await api('/api/admin/users?q='+encodeURIComponent(document.getElementById('useq').value));document.getElementById('ut').innerHTML='<table><tr><th>ID</th><th>User</th><th>Balance</th><th>Diamond</th><th>Refs</th><th>Action</th></tr>'+j.users.map(u=>`<tr><td>${u.id}</td><td>${u.first_name} ${u.username?'@'+u.username:''}</td><td>৳${u.balance}</td><td>💎${u.diamonds}</td><td>${u.referrals}</td><td><button class="btn" onclick="adjust(${u.id})">Adjust</button> <button class="btn danger" onclick="ban(${u.id},${u.banned?0:1})">${u.banned?'Unban':'Ban'}</button></td></tr>`).join('')+'</table>'}
async function adjust(id){let a=prompt('Balance adjustment (+/- ৳):','0');if(a===null)return;let d=prompt('Diamond adjustment (+/-):','0');if(d===null)return;await api('/api/admin/user/adjust',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:id,amount:a,diamonds:d,note:'Admin adjustment'})});users()}
async function ban(id,b){await api('/api/admin/user/ban',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:id,banned:b})});users()}
async function addTask(){let x={title:tt.value,description:td.value,reward:tr.value,diamond_reward:tdd.value,url:tu.value,daily_limit:tl.value};await api('/api/admin/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(x)});tasks()}
async function tasks(){let j=await api('/api/admin/tasks');document.getElementById('tasklist').innerHTML=j.tasks.map(t=>`<div class="card"><b>${t.title}</b> — ৳${t.reward} 💎${t.diamond_reward} — ${t.active?'ACTIVE':'OFF'} <button class="btn" onclick="taskToggle(${t.id})">Toggle</button> <button class="btn danger" onclick="taskDelete(${t.id})">Delete</button><div class="muted">${t.description||''}</div></div>`).join('')}
async function taskToggle(id){await api('/api/admin/tasks/toggle',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});tasks()}async function taskDelete(id){await api('/api/admin/tasks/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});tasks()}
async function addLevel(){await api('/api/admin/levels',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:ln.value,min_earned:lm.value,diamond_bonus:ld.value})});levels()}
async function levels(){let j=await api('/api/admin/levels');document.getElementById('levellist').innerHTML=j.levels.map(x=>`<div class="card"><b>${x.id}. ${x.name}</b> — Min ৳${x.min_earned}, 💎${x.diamond_bonus} <button class="btn danger" onclick="levelDelete(${x.id})">Delete</button></div>`).join('')}
async function levelDelete(id){await api('/api/admin/levels/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});levels()}
async function withdrawals(){let j=await api('/api/admin/withdrawals');document.getElementById('wt').innerHTML='<table><tr><th>ID</th><th>User</th><th>Amount</th><th>Method</th><th>Account</th><th>Status</th><th>Action</th></tr>'+j.items.map(x=>`<tr><td>${x.id}</td><td>${x.user_id}</td><td>৳${x.amount}</td><td>${x.method}</td><td>${x.account}</td><td>${x.status}</td><td>${x.status==='pending'?`<button class="btn" onclick="wstatus(${x.id},'approved')">Approve</button> <button class="btn danger" onclick="wstatus(${x.id},'rejected')">Reject</button>`:''}</td></tr>`).join('')+'</table>'}
async function wstatus(id,status){await api('/api/admin/withdrawals/status',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,status})});withdrawals()}
async function support(){let j=await api('/api/admin/support');document.getElementById('st').innerHTML='<table><tr><th>ID</th><th>User</th><th>Message</th><th>Status</th><th>Reply</th></tr>'+j.items.map(x=>`<tr><td>${x.id}</td><td>${x.user_id}</td><td>${x.message}</td><td>${x.status}</td><td>${x.status==='open'?`<button class="btn" onclick="reply(${x.id})">Reply</button>`:x.reply}</td></tr>`).join('')+'</table>'}
async function reply(id){let r=prompt('Reply:');if(r===null)return;await api('/api/admin/support/reply',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,reply:r})});support()}
async function settings(){let j=await api('/api/admin/settings');let b=document.getElementById('settingsBox');b.innerHTML=Object.entries(j.settings).map(([k,v])=>`<label class="muted">${k}</label><textarea data-k="${k}" rows="${String(v).length>120?3:1}">${v}</textarea>`).join('')}
async function saveSettings(){let out={};document.querySelectorAll('#settingsBox [data-k]').forEach(x=>out[x.dataset.k]=x.value);await api('/api/admin/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(out)});alert('All settings saved')}
stats();
</script></body></html>"""

@APP.get("/")
def index(): return render_template_string(USER_HTML,**{**DEFAULTS,**{k:s(k) for k in DEFAULTS}})
@APP.get("/app")
def app_page(): return index()

@APP.get("/api/me")
def me():
    u,err=require_user()
    if err:return err
    c=db(); ad=c.execute("SELECT COUNT(*) n FROM ad_claims WHERE user_id=? AND claim_date=?",(u["id"],today())).fetchone()["n"]; c.close()
    return jsonify(ok=True,user={**dict(u),"balance":money(u["balance"]),"total_earned":money(u["total_earned"]),"total_withdrawn":money(u["total_withdrawn"]),
        "ads_today":ad,"ad_limit":int(s("ad_daily_limit") or 0),"min_withdraw":float(s("min_withdraw") or 0),
        "referral_link":f"https://t.me/{s('bot_username').lstrip('@')}?start=ref_{u['id']}"})

@APP.get("/api/tasks")
def api_tasks():
    u,err=require_user()
    if err:return err
    c=db(); rows=c.execute("SELECT * FROM tasks WHERE active=1 ORDER BY id DESC").fetchall(); out=[]
    for t in rows:
        n=c.execute("SELECT COUNT(*) n FROM task_claims WHERE user_id=? AND task_id=? AND claim_date=?",(u["id"],t["id"],today())).fetchone()["n"]
        if n<int(t["daily_limit"]): out.append({**dict(t),"reward":money(t["reward"])})
    c.close(); return jsonify(ok=True,tasks=out)

@APP.post("/api/task/claim")
def task_claim():
    u,err=require_user()
    if err:return err
    data=request.get_json(silent=True) or {}; tid=int(data.get("task_id",0)); c=db()
    t=c.execute("SELECT * FROM tasks WHERE id=? AND active=1",(tid,)).fetchone()
    if not t:c.close();return jsonify(ok=False,error="Task not found"),404
    try:
        c.execute("INSERT INTO task_claims(user_id,task_id,claim_date,created_at) VALUES(?,?,?,?)",(u["id"],tid,today(),iso()))
    except sqlite3.IntegrityError:c.close();return jsonify(ok=False,error="আজকের Task limit শেষ"),400
    add_money(c,u["id"],t["reward"],"task",t["title"]);add_diamond(c,u["id"],t["diamond_reward"],"task",t["title"]);c.commit();c.close()
    return jsonify(ok=True)

@APP.post("/api/bonus")
def bonus():
    u,err=require_user()
    if err:return err
    c=db()
    try:c.execute("INSERT INTO daily_claims(user_id,claim_date,created_at) VALUES(?,?,?)",(u["id"],today(),iso()))
    except sqlite3.IntegrityError:c.close();return jsonify(ok=False,error="আজকের Bonus নেওয়া হয়েছে"),400
    add_money(c,u["id"],paisa(s("daily_bonus")),"daily_bonus","Daily Bonus");c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/ad/start")
def ad_start():
    u,err=require_user()
    if err:return err
    c=db(); n=c.execute("SELECT COUNT(*) n FROM ad_claims WHERE user_id=? AND claim_date=?",(u["id"],today())).fetchone()["n"]
    if n>=int(s("ad_daily_limit") or 0):c.close();return jsonify(ok=False,error="আজকের Ad limit শেষ"),400
    tok=secrets.token_urlsafe(32); now=datetime.utcnow(); exp=now+timedelta(minutes=10)
    c.execute("INSERT INTO ad_sessions(token,user_id,created_at,expires_at) VALUES(?,?,?,?)",(tok,u["id"],now.isoformat(),exp.isoformat()));c.commit();c.close()
    return jsonify(ok=True,token=tok)

@APP.post("/api/ad/claim")
def ad_claim():
    u,err=require_user()
    if err:return err
    tok=(request.get_json(silent=True) or {}).get("token","");c=db();r=c.execute("SELECT * FROM ad_sessions WHERE token=? AND user_id=?",(tok,u["id"])).fetchone()
    if not r or r["used"] or datetime.fromisoformat(r["expires_at"])<datetime.utcnow():c.close();return jsonify(ok=False,error="Ad session invalid/expired"),400
    n=c.execute("SELECT COUNT(*) n FROM ad_claims WHERE user_id=? AND claim_date=?",(u["id"],today())).fetchone()["n"]
    if n>=int(s("ad_daily_limit") or 0):c.close();return jsonify(ok=False,error="Daily limit reached"),400
    c.execute("UPDATE ad_sessions SET used=1 WHERE token=?",(tok,));c.execute("INSERT INTO ad_claims(user_id,claim_date,created_at) VALUES(?,?,?)",(u["id"],today(),iso()))
    add_money(c,u["id"],paisa(s("ad_reward")),"ad","Ad reward");c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/withdraw")
def withdraw():
    u,err=require_user()
    if err:return err
    d=request.get_json(silent=True) or {}; amount=paisa(d.get("amount"));method=str(d.get("method","")).strip();account=str(d.get("account","")).strip()
    if amount<paisa(s("min_withdraw")):return jsonify(ok=False,error=f"Minimum withdraw ৳{s('min_withdraw')}"),400
    if not method or not account:return jsonify(ok=False,error="Method ও account দিন"),400
    c=db();r=c.execute("SELECT balance FROM users WHERE id=?",(u["id"],)).fetchone()
    if r["balance"]<amount:c.close();return jsonify(ok=False,error="Insufficient balance"),400
    c.execute("UPDATE users SET balance=balance-? WHERE id=?",(amount,u["id"]))
    c.execute("INSERT INTO withdrawals(user_id,amount,method,account,created_at,updated_at) VALUES(?,?,?,?,?,?)",(u["id"],amount,method,account,iso(),iso()))
    c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/withdrawals")
def withdrawals_user():
    u,err=require_user()
    if err:return err
    c=db();rows=c.execute("SELECT id,amount,method,account,status,created_at FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 50",(u["id"],)).fetchall();c.close()
    return jsonify(ok=True,items=[{**dict(x),"amount":money(x["amount"])} for x in rows])

@APP.post("/api/support")
def support_send():
    u,err=require_user()
    if err:return err
    m=str((request.get_json(silent=True) or {}).get("message","")).strip()
    if not m:return jsonify(ok=False,error="Message লিখুন"),400
    c=db();c.execute("INSERT INTO support(user_id,message,created_at) VALUES(?,?,?)",(u["id"],m,iso()));c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/profile/photo")
def profile_photo():
    u,err=require_user()
    if err:return err
    p=(request.get_json(silent=True) or {}).get("photo","")
    if len(p)>500000:return jsonify(ok=False,error="Photo too large"),400
    c=db();c.execute("UPDATE users SET photo=? WHERE id=?",(p,u["id"]));c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/levels")
def levels_public():
    u,err=require_user()
    if err:return err
    c=db();r=c.execute("SELECT * FROM levels WHERE active=1 ORDER BY min_earned").fetchall();c.close();return jsonify(ok=True,levels=[{**dict(x),"min_earned":money(x["min_earned"])} for x in r])

def admin_page_allowed():
    return admin_ok()

@APP.get("/admin")
def admin_page():
    if not admin_page_allowed():return "Unauthorized",403
    return render_template_string(ADMIN_HTML,app_name=s("app_name"),admin_id=ADMIN_ID,key=request.args.get("key",""))

def admin_guard():
    return None if admin_ok() else (jsonify(ok=False,error="Unauthorized"),403)

@APP.get("/api/admin/stats")
def a_stats():
    e=admin_guard()
    if e:return e
    c=db(); q=lambda sql:c.execute(sql).fetchone()[0]
    out={"users":q("SELECT COUNT(*) FROM users"),"banned":q("SELECT COUNT(*) FROM users WHERE banned=1"),
         "pending_withdrawals":q("SELECT COUNT(*) FROM withdrawals WHERE status='pending'"),
         "open_support":q("SELECT COUNT(*) FROM support WHERE status='open'"),
         "tasks":q("SELECT COUNT(*) FROM tasks WHERE active=1"),"total_balance":money(q("SELECT COALESCE(SUM(balance),0) FROM users")),
         "total_diamonds":q("SELECT COALESCE(SUM(diamonds),0) FROM users"),"ad_daily_limit":s("ad_daily_limit"),
         "ad_reward":s("ad_reward"),"referral_reward":s("referral_reward"),"referral_diamond":s("referral_diamond")}
    c.close();return jsonify(ok=True,**out)

@APP.get("/api/admin/users")
def a_users():
    e=admin_guard()
    if e:return e
    q=request.args.get("q","").strip();c=db()
    rows=c.execute("SELECT * FROM users WHERE CAST(id AS TEXT) LIKE ? OR username LIKE ? OR first_name LIKE ? ORDER BY id DESC LIMIT 200",
                   (f"%{q}%",f"%{q}%",f"%{q}%")).fetchall();c.close()
    return jsonify(ok=True,users=[{**dict(x),"balance":money(x["balance"]),"total_earned":money(x["total_earned"])} for x in rows])

@APP.post("/api/admin/user/adjust")
def a_adjust():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};uid=int(d.get("user_id")); amount=paisa(d.get("amount",0)); dia=int(d.get("diamonds",0));c=db()
    if not c.execute("SELECT id FROM users WHERE id=?",(uid,)).fetchone():c.close();return jsonify(ok=False,error="User not found"),404
    add_money(c,uid,amount,"admin",d.get("note","Admin adjustment"));add_diamond(c,uid,dia,"admin","Admin adjustment");c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/admin/user/ban")
def a_ban():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};c=db();c.execute("UPDATE users SET banned=? WHERE id=?",(int(bool(d.get("banned"))),int(d.get("user_id"))));c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/admin/tasks")
def a_tasks():
    e=admin_guard()
    if e:return e
    c=db();r=c.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall();c.close();return jsonify(ok=True,tasks=[{**dict(x),"reward":money(x["reward"])} for x in r])

@APP.post("/api/admin/tasks")
def a_task_add():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};c=db()
    c.execute("INSERT INTO tasks(title,description,reward,diamond_reward,url,daily_limit,active,created_at) VALUES(?,?,?,?,?,?,1,?)",
              (d.get("title",""),d.get("description",""),paisa(d.get("reward",0)),int(d.get("diamond_reward",0)),d.get("url",""),int(d.get("daily_limit",1)),iso()))
    c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/admin/tasks/toggle")
def a_task_toggle():
    e=admin_guard()
    if e:return e
    c=db();c.execute("UPDATE tasks SET active=1-active WHERE id=?",(int((request.get_json() or {}).get("id")),));c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/admin/tasks/delete")
def a_task_delete():
    e=admin_guard()
    if e:return e
    c=db();c.execute("DELETE FROM tasks WHERE id=?",(int((request.get_json() or {}).get("id")),));c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/admin/levels")
def a_levels():
    e=admin_guard()
    if e:return e
    c=db();r=c.execute("SELECT * FROM levels ORDER BY id").fetchall();c.close();return jsonify(ok=True,levels=[{**dict(x),"min_earned":money(x["min_earned"])} for x in r])

@APP.post("/api/admin/levels")
def a_level_add():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};c=db();nid=(c.execute("SELECT COALESCE(MAX(id),0)+1 FROM levels").fetchone()[0])
    c.execute("INSERT INTO levels(id,name,min_earned,diamond_bonus,active) VALUES(?,?,?,?,1)",(nid,d.get("name","Level"),paisa(d.get("min_earned",0)),int(d.get("diamond_bonus",0))))
    c.commit();c.close();return jsonify(ok=True)

@APP.post("/api/admin/levels/delete")
def a_level_delete():
    e=admin_guard()
    if e:return e
    lid=int((request.get_json() or {}).get("id")); 
    if lid==1:return jsonify(ok=False,error="Starter level cannot be deleted"),400
    c=db();c.execute("DELETE FROM levels WHERE id=?",(lid,));c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/admin/withdrawals")
def a_withdrawals():
    e=admin_guard()
    if e:return e
    c=db();r=c.execute("SELECT * FROM withdrawals ORDER BY id DESC LIMIT 300").fetchall();c.close();return jsonify(ok=True,items=[{**dict(x),"amount":money(x["amount"])} for x in r])

@APP.post("/api/admin/withdrawals/status")
def a_wstatus():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};wid=int(d.get("id"));status=d.get("status");c=db();r=c.execute("SELECT * FROM withdrawals WHERE id=?",(wid,)).fetchone()
    if not r or status not in ("approved","rejected"):c.close();return jsonify(ok=False,error="Invalid request"),400
    if r["status"]!="pending":c.close();return jsonify(ok=False,error="Already processed"),400
    if status=="rejected":c.execute("UPDATE users SET balance=balance+? WHERE id=?",(r["amount"],r["user_id"]))
    if status=="approved":c.execute("UPDATE users SET total_withdrawn=total_withdrawn+? WHERE id=?",(r["amount"],r["user_id"]))
    c.execute("UPDATE withdrawals SET status=?,updated_at=? WHERE id=?",(status,iso(),wid));c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/admin/support")
def a_support():
    e=admin_guard()
    if e:return e
    c=db();r=c.execute("SELECT * FROM support ORDER BY id DESC LIMIT 300").fetchall();c.close();return jsonify(ok=True,items=[dict(x) for x in r])

@APP.post("/api/admin/support/reply")
def a_reply():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};c=db();c.execute("UPDATE support SET reply=?,status='closed',replied_at=? WHERE id=?",(d.get("reply",""),iso(),int(d.get("id"))));c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/admin/settings")
def a_settings():
    e=admin_guard()
    if e:return e
    c=db();r=c.execute("SELECT k,v FROM settings ORDER BY k").fetchall();c.close();return jsonify(ok=True,settings={x["k"]:x["v"] for x in r})

@APP.post("/api/admin/settings")
def a_settings_save():
    e=admin_guard()
    if e:return e
    d=request.get_json(silent=True) or {};c=db()
    for k,v in d.items():
        if k in DEFAULTS:c.execute("INSERT INTO settings(k,v) VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v",(k,str(v)))
    c.commit();c.close();return jsonify(ok=True)

@APP.get("/api/admin/export")
def a_export():
    e=admin_guard()
    if e:return e
    c=db();out=io.StringIO();w=csv.writer(out);w.writerow(["user_id","username","first_name","balance","diamonds","total_earned","referrals","created_at"])
    for r in c.execute("SELECT * FROM users ORDER BY id"):w.writerow([r["id"],r["username"],r["first_name"],money(r["balance"]),r["diamonds"],money(r["total_earned"]),r["referrals"],r["created_at"]])
    c.close();data=io.BytesIO(out.getvalue().encode("utf-8-sig"));data.seek(0);return send_file(data,mimetype="text/csv",as_attachment=True,download_name="protidiner_kaj_users.csv")

if __name__=="__main__":
    init()
    APP.run(host="0.0.0.0",port=int(os.environ.get("PORT","5000")))
'''

requirements = "Flask>=3.0,<4\nGunicorn>=22,<24\n"

readme = """# প্রতিদিনের কাজ BD — A-Z Final Package

এই ফাইলে Telegram Mini App + Admin Control Center-এর সম্পূর্ণ foundation একসাথে আছে।

## Included
- Premium dark purple/royal-blue/diamond glass UI
- Telegram WebApp authentication (BOT_TOKEN দিলে real validation)
- Demo mode (BOT_TOKEN না থাকলে)
- Home / Earn / Diamond / Withdraw / Profile
- Daily Bonus
- Daily Ads + supplied LibTL SDK scripts
- Ad session + daily limit
- Tasks + money + diamond rewards
- Referral link + referral money + diamond rewards
- Level system
- Balance + Diamond ledger
- Profile photo
- Withdraw request/history
- bKash/Nagad/Rocket/Bank method fields
- Support ticket + admin reply
- Channel + Group buttons
- Admin dashboard
- Admin users/search/ban/unban/balance/diamond adjustment
- Admin tasks CRUD + toggle
- Admin levels CRUD
- Admin withdrawals approve/reject + refund on reject
- Admin support reply
- Admin settings: all important links/rewards/scripts/text/colors
- CSV export
- SQLite database

## Supplied configuration
Admin ID: 8807178385
Bot: @ProtidinerKaj_BD_Bot
Bot URL: https://t.me/ProtidinerKaj_BD_Bot
Channel: https://t.me/ProtidinerKajBD
Group: https://t.me/+hb8X-V4buToxYmJl
Ad link: https://omg10.com/4/11760259
Ad SDK zones: 11764581, 11798857

## Local run
1. Install Python 3.11+
2. `pip install -r requirements.txt`
3. Set environment:
   - BOT_TOKEN=YOUR_BOT_TOKEN
   - ADMIN_ID=8807178385
   - ADMIN_SECRET=MAKE_A_STRONG_SECRET
4. `python main.py`
5. Open `/app`
6. Admin: `/admin?id=8807178385&key=YOUR_SECRET`

## Render
- Build: `pip install -r requirements.txt`
- Start: `gunicorn main:APP`
- Environment variables: BOT_TOKEN, ADMIN_ID, ADMIN_SECRET, DB_PATH
- For SQLite persistence, attach persistent disk and set DB_PATH to a path on that disk, e.g. `/var/data/protidiner_kaj_bd.sqlite3`.
- For multi-instance production, PostgreSQL is preferable.

## Telegram
Set your Mini App/Web App URL in BotFather after deploying. The bot must be configured to open the deployed `/app` URL.

## Important ad verification note
The supplied SDK scripts are loaded in the user page and the server uses a short-lived ad session token. Final anti-fraud/payment-grade verification should use the ad provider's official server callback/API if available; do not rely only on client-side completion.

## Security
Never publish BOT_TOKEN or ADMIN_SECRET. Change ADMIN_SECRET before deployment.
"""

env_example = """BOT_TOKEN=PASTE_YOUR_BOT_TOKEN
ADMIN_ID=8807178385
ADMIN_SECRET=CHANGE_THIS_TO_A_LONG_RANDOM_SECRET
DB_PATH=protidiner_kaj_bd.sqlite3
"""

deploy = """# Render quick deploy
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn main:APP

Environment Variables:
BOT_TOKEN = your real Telegram bot token
ADMIN_ID = 8807178385
ADMIN_SECRET = strong secret
DB_PATH = /var/data/protidiner_kaj_bd.sqlite3

After deploy:
https://YOUR-APP.onrender.com/app
Admin:
https://YOUR-APP.onrender.com/admin?id=8807178385&key=YOUR_SECRET
"""

(root/"main.py").write_text(main_py,encoding="utf-8")
(root/"requirements.txt").write_text(requirements,encoding="utf-8")
(root/"README_AZ_BANGLA.md").write_text(readme,encoding="utf-8")
(root/".env.example").write_text(env_example,encoding="utf-8")
(root/"RENDER_DEPLOY.md").write_text(deploy,encoding="utf-8")

# Add a simple launcher and a config file inside the same package.
(root/"run.sh").write_text("#!/bin/sh\npython main.py\n",encoding="utf-8")
(root/"START_HERE.txt").write_text(
"""প্রথমে README_AZ_BANGLA.md পড়ুন।
এই প্যাকেজে main.py-তেই User App + API + Admin Panel + Database schema আছে।
BOT_TOKEN এবং ADMIN_SECRET সেট করে deploy করুন।
""",encoding="utf-8")

# Validate syntax and zip integrity.
import py_compile
py_compile.compile(str(root/"main.py"),doraise=True)

zip_path = Path("/mnt/data/Protidiner_Kaj_BD_AZ_FINAL.zip")
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if p.is_file():
            z.write(p,p.relative_to(root))
with zipfile.ZipFile(zip_path,"r") as z:
    bad=z.testzip()
    names=z.namelist()
    assert bad is None
    required={"main.py","requirements.txt","README_AZ_BANGLA.md",".env.example","RENDER_DEPLOY.md","START_HERE.txt"}
    assert required.issubset(set(names))
print(f"CREATED: {zip_path} | size={zip_path.stat().st_size} bytes | files={len(names)} | zip_test=OK")
