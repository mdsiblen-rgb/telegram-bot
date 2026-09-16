
import os, json, hmac, hashlib, secrets, urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
ADMIN_KEY = os.getenv("ADMIN_KEY", "CHANGE_ME")
ALLOW_DEMO_UID = os.getenv("ALLOW_DEMO_UID", "false").lower() == "true"

BD_TZ = timezone(timedelta(hours=6))

def now_bd():
    return datetime.now(BD_TZ).replace(tzinfo=None)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(64), unique=True, index=True, nullable=False)
    username = Column(String(255), default="")
    first_name = Column(String(255), default="")
    last_name = Column(String(255), default="")
    balance = Column(Float, default=0)
    diamonds = Column(Integer, default=0)
    total_earned = Column(Float, default=0)
    referral_code = Column(String(64), unique=True, index=True)
    referred_by = Column(String(64), nullable=True)
    level = Column(Integer, default=1)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=now_bd)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, index=True)
    value = Column(Text, default="")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    link = Column(Text, default="")
    cash_reward = Column(Float, default=0)
    diamond_reward = Column(Integer, default=0)
    daily_limit = Column(Integer, default=1)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=now_bd)

class TaskClaim(Base):
    __tablename__ = "task_claims"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), index=True)
    claimed_at = Column(DateTime, default=now_bd)

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    method = Column(String(30))
    number = Column(String(50))
    amount = Column(Float)
    status = Column(String(30), default="pending")
    admin_note = Column(Text, default="")
    created_at = Column(DateTime, default=now_bd)
    processed_at = Column(DateTime, nullable=True)

class SupportMessage(Base):
    __tablename__ = "support_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(Text)
    reply = Column(Text, default="")
    status = Column(String(30), default="open")
    created_at = Column(DateTime, default=now_bd)
    replied_at = Column(DateTime, nullable=True)

class Ledger(Base):
    __tablename__ = "ledger"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    amount = Column(Float, default=0)
    diamonds = Column(Integer, default=0)
    kind = Column(String(50))
    note = Column(Text, default="")
    created_at = Column(DateTime, default=now_bd)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255))
    message = Column(Text)
    created_at = Column(DateTime, default=now_bd)

Base.metadata.create_all(engine)

DEFAULTS = {
    "app_name": "Earn Mini App",
    "logo_url": "",
    "primary_color": "#19a974",
    "welcome_text": "স্বাগতম! কাজ করে রিওয়ার্ড সংগ্রহ করুন।",
    "min_withdraw": "100",
    "ref_reward": "10",
    "daily_bonus": "5",
    "diamond_rate": "100",
    "company_channel_link": "",
    "company_group_link": "",
    "company_bot_link": "",
    "company_ad_link": "",
    "direct_link": "",
    "support_link": "",
    "withdraw_notice": "উইথড্র করার আগে তথ্য সঠিকভাবে দিন।",
    "maintenance": "false",
    "bot_username": BOT_USERNAME,
    "level_config": json.dumps([
        {"level": 1, "required": 0},
        {"level": 2, "required": 100},
        {"level": 3, "required": 500},
        {"level": 4, "required": 1000},
        {"level": 5, "required": 2500}
    ], ensure_ascii=False),
}

def get_settings(db):
    data = {k: v for k, v in DEFAULTS.items()}
    for row in db.query(Setting).all():
        data[row.key] = row.value
    return data

def set_setting(db, key, value):
    row = db.query(Setting).filter(Setting.key == key).first()
    if row:
        row.value = str(value)
    else:
        db.add(Setting(key=key, value=str(value)))

def seed_settings():
    db = SessionLocal()
    try:
        for k, v in DEFAULTS.items():
            if not db.query(Setting).filter(Setting.key == k).first():
                db.add(Setting(key=k, value=v))
        db.commit()
    finally:
        db.close()

seed_settings()

app = FastAPI(title="Telegram Mini App + Admin")

def admin_guard(x_admin_key: Optional[str]):
    if not x_admin_key or not hmac.compare_digest(x_admin_key, ADMIN_KEY):
        raise HTTPException(401, "Admin key required")

def parse_telegram_init_data(init_data: str):
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not configured")
    parsed = urllib.parse.parse_qs(init_data, keep_blank_values=True)
    received_hash = parsed.pop("hash", [None])[0]
    if not received_hash:
        raise ValueError("Missing hash")
    check = "\n".join(f"{k}={v[0]}" for k, v in sorted(parsed.items()))
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated, received_hash):
        raise ValueError("Invalid Telegram initData")
    user_raw = parsed.get("user", [""])[0]
    return json.loads(user_raw)

def get_or_create_user(db, tg):
    tid = str(tg["id"])
    user = db.query(User).filter(User.telegram_id == tid).first()
    if not user:
        code = secrets.token_hex(4).upper()
        while db.query(User).filter(User.referral_code == code).first():
            code = secrets.token_hex(4).upper()
        user = User(
            telegram_id=tid,
            username=tg.get("username", ""),
            first_name=tg.get("first_name", ""),
            last_name=tg.get("last_name", ""),
            referral_code=code,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.username = tg.get("username", user.username or "")
        user.first_name = tg.get("first_name", user.first_name or "")
        user.last_name = tg.get("last_name", user.last_name or "")
        db.commit()
    return user

def user_from_request(db, request: Request):
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    if init_data and BOT_TOKEN:
        try:
            return get_or_create_user(db, parse_telegram_init_data(init_data))
        except Exception:
            raise HTTPException(401, "Invalid Telegram session")
    if ALLOW_DEMO_UID:
        uid = request.headers.get("X-Demo-Uid") or request.query_params.get("uid")
        if uid:
            return get_or_create_user(db, {"id": str(uid), "first_name": "Demo"})
    raise HTTPException(401, "Open this app inside Telegram")

def add_reward(db, user, amount=0, diamonds=0, kind="reward", note=""):
    user.balance += float(amount or 0)
    user.diamonds += int(diamonds or 0)
    user.total_earned += max(float(amount or 0), 0)
    db.add(Ledger(user_id=user.id, amount=amount or 0, diamonds=diamonds or 0, kind=kind, note=note))
    user.level = calculate_level(user.total_earned, get_settings(db))
    db.commit()

def calculate_level(total, settings):
    try:
        levels = json.loads(settings.get("level_config", "[]"))
        current = 1
        for x in levels:
            if float(total) >= float(x.get("required", 0)):
                current = int(x.get("level", current))
        return current
    except Exception:
        return 1

def today_claims(db, user_id, task_id):
    start = now_bd().replace(hour=0, minute=0, second=0, microsecond=0)
    return db.query(TaskClaim).filter(
        TaskClaim.user_id == user_id,
        TaskClaim.task_id == task_id,
        TaskClaim.claimed_at >= start
    ).count()

# ---------------------------------------------------------------------------
# SINGLE-FILE FRONTEND — all UI is embedded in this main.py
# ---------------------------------------------------------------------------
INDEX_HTML = '\n<!doctype html>\n<html lang="bn">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">\n<title>Earn Mini App</title>\n<script src="https://telegram.org/js/telegram-web-app.js"></script>\n<style>\n:root{--primary:#19a974;--bg:#f5f7fb;--card:#fff;--text:#172033;--muted:#748094}\n*{box-sizing:border-box}body{margin:0;background:var(--bg);font-family:Arial,sans-serif;color:var(--text);padding-bottom:84px}\nheader{padding:18px 16px;background:linear-gradient(135deg,var(--primary),#087f5b);color:white;border-radius:0 0 24px 24px}\n.top{display:flex;align-items:center;justify-content:space-between}.avatar{width:48px;height:48px;border-radius:50%;background:#ffffff33;display:grid;place-items:center;font-weight:800;font-size:20px}\nh1{font-size:20px;margin:0 0 4px}p{margin:4px 0}.muted{color:var(--muted);font-size:13px}.white-muted{color:#e5fff6;font-size:13px}\n.container{padding:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.card{background:var(--card);border-radius:18px;padding:15px;margin-bottom:12px;box-shadow:0 4px 18px #1020300d}.stat{font-size:22px;font-weight:800}.label{font-size:12px;color:var(--muted)}\n.btn{border:0;border-radius:13px;padding:12px 14px;font-weight:700;cursor:pointer;background:var(--primary);color:#fff}.btn.secondary{background:#eaf7f2;color:#087f5b}.btn.danger{background:#ffe8e8;color:#b42318}.btn.full{width:100%}\n.task{display:flex;justify-content:space-between;gap:10px;align-items:center}.task h3{margin:0;font-size:15px}.task p{font-size:12px;color:var(--muted)}\ninput,select,textarea{width:100%;padding:12px;border:1px solid #dbe2ea;border-radius:12px;margin:5px 0 10px;background:#fff}\n.bottom{position:fixed;bottom:0;left:0;right:0;height:76px;background:#fff;border-top:1px solid #e8edf2;display:grid;grid-template-columns:repeat(5,1fr);z-index:10}\n.nav{border:0;background:white;color:#7a8495;font-size:11px}.nav.active{color:var(--primary);font-weight:800}.nav b{display:block;font-size:20px;margin-bottom:3px}\n.page{display:none}.page.active{display:block}.row{display:flex;justify-content:space-between;align-items:center;gap:8px}.badge{padding:5px 9px;border-radius:20px;background:#eaf7f2;color:#087f5b;font-size:11px;font-weight:700}\n.modal{position:fixed;inset:0;background:#0008;display:none;align-items:end;z-index:20}.modal.open{display:flex}.sheet{background:#fff;width:100%;border-radius:22px 22px 0 0;padding:18px;max-height:90vh;overflow:auto}\n</style>\n</head>\n<body>\n<header>\n <div class="top">\n  <div><h1 id="appName">Earn Mini App</h1><div id="welcome" class="white-muted">স্বাগতম</div></div>\n  <div id="avatar" class="avatar">U</div>\n </div>\n <div style="margin-top:15px"><div class="white-muted">আপনার ব্যালেন্স</div><div style="font-size:30px;font-weight:900">৳ <span id="balance">0</span></div></div>\n</header>\n\n<div class="container">\n<section id="home" class="page active">\n <div class="grid">\n  <div class="card"><div class="label">💰 Balance</div><div class="stat">৳ <span id="hBalance">0</span></div></div>\n  <div class="card"><div class="label">💎 Diamonds</div><div class="stat"><span id="diamonds">0</span></div></div>\n  <div class="card"><div class="label">⭐ Level</div><div class="stat"><span id="level">1</span></div></div>\n  <div class="card"><div class="label">📈 Total Earned</div><div class="stat">৳ <span id="earned">0</span></div></div>\n </div>\n <div class="card">\n  <div class="row"><div><b>🎁 Daily Bonus</b><div class="muted">প্রতিদিন একবার</div></div><button class="btn" onclick="bonus()">Claim</button></div>\n </div>\n <div id="notice"></div>\n <div class="card"><b>⚡ দ্রুত কাজ</b><div id="homeTasks" style="margin-top:10px"></div></div>\n</section>\n\n<section id="tasks" class="page">\n <div class="card"><h2>📋 Tasks</h2><div class="muted">কাজ সম্পন্ন করে রিওয়ার্ড নিন</div></div>\n <div id="taskList"></div>\n</section>\n\n<section id="refer" class="page">\n <div class="card"><h2>👥 Referral</h2><div class="muted">বন্ধু আমন্ত্রণ করে রিওয়ার্ড পান</div>\n  <div style="margin-top:16px"><div class="label">আপনার Referral Code</div><div class="stat" id="refCode">—</div></div>\n  <div style="margin-top:10px"><div class="label">মোট Referral</div><div class="stat" id="refCount">0</div></div>\n  <button class="btn full" style="margin-top:15px" onclick="copyRef()">🔗 Link Copy</button>\n </div>\n</section>\n\n<section id="wallet" class="page">\n <div class="card"><h2>💳 Wallet</h2><div class="stat">৳ <span id="wBalance">0</span></div><div class="muted">Minimum Withdraw: ৳<span id="minW">100</span></div></div>\n <div class="card"><button class="btn full" onclick="openWithdraw()">💸 Withdraw</button></div>\n <div class="card"><b>Withdrawal History</b><div id="history" style="margin-top:10px"></div></div>\n</section>\n\n<section id="profile" class="page">\n <div class="card"><h2>👤 Profile</h2><div id="profileBox"></div></div>\n <div class="card"><button class="btn secondary full" onclick="openSupport()">💬 Support</button></div>\n <div class="card"><a id="supportLink" class="btn secondary full" style="display:block;text-align:center;text-decoration:none" target="_blank">🔗 Support Link</a></div>\n</section>\n</div>\n\n<nav class="bottom">\n <button class="nav active" onclick="showPage(\'home\',this)"><b>⌂</b>Home</button>\n <button class="nav" onclick="showPage(\'tasks\',this)"><b>✓</b>Tasks</button>\n <button class="nav" onclick="showPage(\'refer\',this)"><b>👥</b>Refer</button>\n <button class="nav" onclick="showPage(\'wallet\',this)"><b>৳</b>Wallet</button>\n <button class="nav" onclick="showPage(\'profile\',this)"><b>♙</b>Profile</button>\n</nav>\n\n<div id="modal" class="modal" onclick="if(event.target===this)closeModal()"><div class="sheet" id="sheet"></div></div>\n\n<script>\nconst tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand()}\nlet state={user:null,settings:{},ref:null};\nconst headers=()=>{const h={\'Content-Type\':\'application/json\'};if(tg?.initData)h[\'X-Telegram-Init-Data\']=tg.initData;return h}\nasync function api(path,opt={}){opt.headers={...headers(),...(opt.headers||{})};const r=await fetch(path,opt);const d=await r.json();if(!r.ok)throw new Error(d.detail||d.message||\'Request failed\');return d}\nfunction money(n){return Number(n||0).toFixed(2).replace(\'.00\',\'\')}\nfunction renderUser(u){state.user=u;[\'balance\',\'hBalance\',\'wBalance\'].forEach(id=>document.getElementById(id).textContent=money(u.balance));document.getElementById(\'diamonds\').textContent=u.diamonds;document.getElementById(\'level\').textContent=u.level;document.getElementById(\'earned\').textContent=money(u.total_earned);document.getElementById(\'avatar\').textContent=(u.first_name||\'U\')[0].toUpperCase();document.getElementById(\'profileBox\').innerHTML=`<b>${esc(u.first_name||\'User\')}</b><br><span class="muted">@${esc(u.username||\'none\')}</span><br><br>Telegram ID: ${esc(u.telegram_id)}<br>Level: ${u.level}`}\nfunction esc(s){return String(s??\'\').replace(/[&<>"\']/g,m=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[m]))}\nfunction showPage(id,el){document.querySelectorAll(\'.page\').forEach(x=>x.classList.remove(\'active\'));document.getElementById(id).classList.add(\'active\');document.querySelectorAll(\'.nav\').forEach(x=>x.classList.remove(\'active\'));el.classList.add(\'active\');if(id===\'tasks\')loadTasks();if(id===\'refer\')loadRef();if(id===\'wallet\')loadHistory()}\nasync function load(){try{const d=await api(\'/api/home\');state.settings=d.settings;renderUser(d.user);document.documentElement.style.setProperty(\'--primary\',d.settings.primary_color||\'#19a974\');document.getElementById(\'appName\').textContent=d.settings.app_name||\'Earn Mini App\';document.getElementById(\'welcome\').textContent=d.settings.welcome_text||\'\';document.getElementById(\'minW\').textContent=d.settings.min_withdraw||100;const sl=document.getElementById(\'supportLink\');if(d.settings.support_link){sl.href=d.settings.support_link}else sl.style.display=\'none\';document.getElementById(\'notice\').innerHTML=d.notifications?.length?`<div class="card"><b>📢 ${esc(d.notifications[0].title)}</b><p>${esc(d.notifications[0].message)}</p></div>`:\'\';renderTasks(d.tasks||[],\'homeTasks\',true)}catch(e){document.getElementById(\'notice\').innerHTML=`<div class="card"><b>⚠️ ${esc(e.message)}</b><p class="muted">Telegram Mini App হিসেবে খুলুন।</p></div>`}}\nfunction renderTasks(arr,id,compact=false){document.getElementById(id).innerHTML=arr.length?arr.map(t=>`<div class="card task"><div><h3>${esc(t.title)}</h3><p>${esc(t.description||\'\')}</p><span class="badge">৳${money(t.cash_reward)} + 💎${t.diamond_reward}</span></div>${t.link?`<button class="btn" onclick="claim(${t.id},\'${esc(t.link)}\')">Open</button>`:\'\'}</div>`).join(\'\'):\'<div class="muted">এখন কোনো টাস্ক নেই।</div>\'}\nasync function loadTasks(){try{const d=await api(\'/api/tasks\');document.getElementById(\'taskList\').innerHTML=d.map(t=>`<div class="card task"><div><h3>${esc(t.title)}</h3><p>${esc(t.description||\'\')}</p><span class="badge">৳${money(t.cash_reward)} + 💎${t.diamond_reward} | আজ ${t.claimed_today}/${t.daily_limit}</span></div><button class="btn" ${t.remaining<=0?\'disabled\':\'\'} onclick="claim(${t.id},\'${esc(t.link)}\')">${t.remaining<=0?\'Done\':\'Open\'}</button></div>`).join(\'\')||\'<div class="muted">কোনো টাস্ক নেই।</div>\'}catch(e){alert(e.message)}}\nasync function claim(id,link){if(link){try{if(tg?.openLink)tg.openLink(link);else window.open(link,\'_blank\')}catch{window.open(link,\'_blank\')}}try{const d=await api(\'/api/tasks/claim\',{method:\'POST\',body:JSON.stringify({task_id:id})});renderUser(d.user);alert(`রিওয়ার্ড যোগ হয়েছে: ৳${money(d.reward.cash)} + 💎${d.reward.diamonds}`);loadTasks()}catch(e){alert(e.message)}}\nasync function bonus(){try{const d=await api(\'/api/daily-bonus\',{method:\'POST\'});renderUser(d.user);alert(`🎁 ৳${money(d.amount)} যোগ হয়েছে`)}catch(e){alert(e.message)}}\nasync function loadRef(){try{const d=await api(\'/api/referral\');state.ref=d;document.getElementById(\'refCode\').textContent=d.code;document.getElementById(\'refCount\').textContent=d.count}catch(e){alert(e.message)}}\nfunction copyRef(){if(!state.ref?.link)return alert(\'Bot username Admin Settings-এ সেট করুন\');navigator.clipboard?.writeText(state.ref.link);alert(\'Referral link copied\')}\nfunction openModal(html){document.getElementById(\'sheet\').innerHTML=html;document.getElementById(\'modal\').classList.add(\'open\')}\nfunction closeModal(){document.getElementById(\'modal\').classList.remove(\'open\')}\nfunction openWithdraw(){openModal(`<h2>💸 Withdraw</h2><label>Method</label><select id="wm"><option>bKash</option><option>Nagad</option></select><label>Number</label><input id="wn" placeholder="01XXXXXXXXX"><label>Amount</label><input id="wa" type="number" placeholder="${state.settings.min_withdraw||100}"><p class="muted">${esc(state.settings.withdraw_notice||\'\')}</p><button class="btn full" onclick="sendWithdraw()">Submit</button>`)}\nasync function sendWithdraw(){try{const d=await api(\'/api/withdraw\',{method:\'POST\',body:JSON.stringify({method:document.getElementById(\'wm\').value,number:document.getElementById(\'wn\').value,amount:Number(document.getElementById(\'wa\').value)})});renderUser(d.user);closeModal();loadHistory();alert(d.message)}catch(e){alert(e.message)}}\nasync function loadHistory(){try{const d=await api(\'/api/withdrawals\');document.getElementById(\'history\').innerHTML=d.length?d.map(x=>`<div style="padding:10px 0;border-bottom:1px solid #eee"><b>৳${money(x.amount)}</b> · ${esc(x.method)} · ${esc(x.status)}<div class="muted">${esc(x.created_at)}</div></div>`).join(\'\'):\'<div class="muted">কোনো রেকর্ড নেই।</div>\'}catch(e){}}\nfunction openSupport(){openModal(`<h2>💬 Support</h2><textarea id="sm" rows="5" placeholder="আপনার সমস্যাটি লিখুন"></textarea><button class="btn full" onclick="sendSupport()">Send</button><div id="supportOld" style="margin-top:15px"></div>`);loadSupport()}\nasync function sendSupport(){try{await api(\'/api/support\',{method:\'POST\',body:JSON.stringify({message:document.getElementById(\'sm\').value})});document.getElementById(\'sm\').value=\'\';alert(\'মেসেজ পাঠানো হয়েছে\');loadSupport()}catch(e){alert(e.message)}}\nasync function loadSupport(){try{const d=await api(\'/api/support\');document.getElementById(\'supportOld\').innerHTML=d.map(x=>`<div class="card"><b>You:</b> ${esc(x.message)}<br><b>Admin:</b> ${esc(x.reply||\'অপেক্ষমাণ\')}</div>`).join(\'\')}catch(e){}}\nload();\n</script>\n</body>\n</html>\n'

ADMIN_HTML = '\n<!doctype html>\n<html lang="bn">\n<head>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Admin Panel</title>\n<style>\n*{box-sizing:border-box}body{margin:0;background:#f4f6f9;font-family:Arial;color:#172033}.layout{display:flex;min-height:100vh}.side{width:230px;background:#101828;color:#fff;padding:18px;position:fixed;height:100vh}.side h2{margin:0 0 20px}.side button{width:100%;border:0;background:transparent;color:#d0d5dd;text-align:left;padding:12px;border-radius:10px;margin:2px 0;cursor:pointer}.side button.active,.side button:hover{background:#1d2939;color:#fff}.main{margin-left:230px;width:calc(100% - 230px);padding:22px}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.key{max-width:330px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#fff;border-radius:15px;padding:16px;box-shadow:0 3px 15px #00000009;margin-bottom:14px}.num{font-size:26px;font-weight:800}.muted{color:#667085;font-size:13px}input,select,textarea{width:100%;padding:10px;border:1px solid #d0d5dd;border-radius:9px;margin:5px 0 10px}.btn{border:0;background:#12a56b;color:#fff;padding:10px 14px;border-radius:9px;cursor:pointer}.btn.red{background:#d92d20}.btn.gray{background:#667085}.row{display:flex;gap:8px;align-items:center}.page{display:none}.page.active{display:block}table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:10px;border-bottom:1px solid #eaecf0;text-align:left;font-size:13px}th{background:#f9fafb}.scroll{overflow:auto}.formgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:800px){.side{width:70px}.side h2{font-size:0}.side button{font-size:0;text-align:center}.side button:first-letter{font-size:18px}.main{margin-left:70px;width:calc(100% - 70px)}.grid{grid-template-columns:1fr 1fr}.formgrid{grid-template-columns:1fr}}\n</style>\n</head>\n<body>\n<div class="layout">\n<aside class="side"><h2>⚙️ Admin</h2>\n<button class="active" onclick="page(\'dash\',this)">📊 Dashboard</button>\n<button onclick="page(\'users\',this)">👥 Users</button>\n<button onclick="page(\'tasks\',this)">📋 Tasks</button>\n<button onclick="page(\'withdraw\',this)">💸 Withdraw</button>\n<button onclick="page(\'support\',this)">💬 Support</button>\n<button onclick="page(\'settings\',this)">🔗 Ads & Settings</button>\n<button onclick="page(\'broadcast\',this)">📢 Broadcast</button>\n<button onclick="page(\'ledger\',this)">📒 Ledger</button>\n</aside>\n<main class="main">\n<div class="top"><div><h1 id="title">Dashboard</h1><div class="muted">A–Z control panel</div></div><input class="key" id="key" type="password" placeholder="ADMIN_KEY"></div>\n\n<section id="dash" class="page active"><div class="grid" id="stats"></div><div class="card"><b>সিস্টেম</b><p class="muted">Admin key সেট করার পর সব ডাটা ও কন্ট্রোল এখানে পাওয়া যাবে।</p></div></section>\n\n<section id="users" class="page"><div class="card"><div class="row"><input id="uq" placeholder="Telegram ID / username / name"><button class="btn" onclick="loadUsers()">Search</button></div></div><div class="card scroll"><table><thead><tr><th>ID</th><th>User</th><th>Balance</th><th>Diamond</th><th>Level</th><th>Action</th></tr></thead><tbody id="usersTable"></tbody></table></div></section>\n\n<section id="tasks" class="page"><div class="card"><h3>নতুন Task</h3><div class="formgrid"><input id="tt" placeholder="Title"><input id="tl" placeholder="Link"><input id="tc" type="number" placeholder="Cash reward"><input id="td" type="number" placeholder="Diamond reward"><input id="tlim" type="number" value="1" placeholder="Daily limit"><input id="tdesc" placeholder="Description"></div><button class="btn" onclick="addTask()">Add Task</button></div><div id="tasksBox"></div></section>\n\n<section id="withdraw" class="page"><div class="card scroll"><table><thead><tr><th>ID</th><th>User</th><th>Method</th><th>Number</th><th>Amount</th><th>Status</th><th>Action</th></tr></thead><tbody id="wTable"></tbody></table></div></section>\n\n<section id="support" class="page"><div id="supportBox"></div></section>\n\n<section id="settings" class="page"><div class="card"><h3>App + Company Links + Earning Settings</h3><div class="formgrid">\n<label>App Name<input id="s_app_name"></label><label>Logo URL<input id="s_logo_url"></label>\n<label>Primary Color<input id="s_primary_color"></label><label>Min Withdraw<input id="s_min_withdraw"></label>\n<label>Referral Reward<input id="s_ref_reward"></label><label>Daily Bonus<input id="s_daily_bonus"></label>\n<label>Diamond Rate<input id="s_diamond_rate"></label><label>Bot Username<input id="s_bot_username"></label>\n<label>Company Channel Link<input id="s_company_channel_link"></label><label>Company Group Link<input id="s_company_group_link"></label>\n<label>Company Bot Link<input id="s_company_bot_link"></label><label>Company Ad Link<input id="s_company_ad_link"></label>\n<label>Direct Link<input id="s_direct_link"></label><label>Support Link<input id="s_support_link"></label>\n<label>Welcome Text<input id="s_welcome_text"></label><label>Withdraw Notice<input id="s_withdraw_notice"></label>\n<label>Maintenance<input id="s_maintenance"></label>\n</div><label>Level Config JSON<textarea id="s_level_config" rows="5"></textarea></label><button class="btn" onclick="saveSettings()">Save All Settings</button></div></section>\n\n<section id="broadcast" class="page"><div class="card"><h3>📢 Broadcast</h3><input id="bt" placeholder="Title"><textarea id="bm" rows="7" placeholder="Message"></textarea><button class="btn" onclick="broadcast()">Send to All</button></div></section>\n<section id="ledger" class="page"><div class="card scroll"><table><thead><tr><th>User</th><th>Amount</th><th>Diamond</th><th>Type</th><th>Note</th><th>Date</th></tr></thead><tbody id="lTable"></tbody></table></div></section>\n</main></div>\n<script>\nlet current=\'dash\';\nfunction key(){return document.getElementById(\'key\').value.trim()}\nasync function api(path,opt={}){opt.headers={\'Content-Type\':\'application/json\',\'X-Admin-Key\':key(),...(opt.headers||{})};const r=await fetch(path,opt);const d=await r.json();if(!r.ok)throw new Error(d.detail||\'Request failed\');return d}\nfunction page(id,el){document.querySelectorAll(\'.page\').forEach(x=>x.classList.remove(\'active\'));document.getElementById(id).classList.add(\'active\');document.querySelectorAll(\'.side button\').forEach(x=>x.classList.remove(\'active\'));el.classList.add(\'active\');current=id;document.getElementById(\'title\').textContent=el.textContent.trim();loadPage(id)}\nasync function loadPage(id){try{if(id===\'dash\')await dashboard();if(id===\'users\')await loadUsers();if(id===\'tasks\')await loadTasks();if(id===\'withdraw\')await loadWithdraw();if(id===\'support\')await loadSupport();if(id===\'settings\')await loadSettings();if(id===\'ledger\')await loadLedger()}catch(e){alert(e.message)}}\nasync function dashboard(){const d=await api(\'/api/admin/dashboard\');document.getElementById(\'stats\').innerHTML=Object.entries(d).map(([k,v])=>`<div class="card"><div class="muted">${k}</div><div class="num">${v}</div></div>`).join(\'\')}\nfunction esc(s){return String(s??\'\').replace(/[&<>"\']/g,m=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[m]))}\nasync function loadUsers(){const d=await api(\'/api/admin/users?q=\'+encodeURIComponent(document.getElementById(\'uq\').value));document.getElementById(\'usersTable\').innerHTML=d.map(u=>`<tr><td>${u.id}</td><td>${esc(u.first_name)}<br><span class="muted">${esc(u.username)} / ${u.telegram_id}</span></td><td>৳${u.balance}</td><td>${u.diamonds}</td><td>${u.level}</td><td><button class="btn" onclick="adjust(${u.id},\'add\')">+ টাকা</button> <button class="btn gray" onclick="adjust(${u.id},\'diamond\')">+💎</button> <button class="btn red" onclick="ban(${u.id},${!u.banned})">${u.banned?\'Unban\':\'Ban\'}</button></td></tr>`).join(\'\')}\nasync function adjust(id,type){let val=prompt(type===\'add\'?\'টাকার পরিমাণ (+/-)\':\'ডায়মন্ড (+/-)\');if(val===null)return;const body=type===\'add\'?{amount:Number(val)}:{diamonds:Number(val)};await api(\'/api/admin/users/\'+id+\'/adjust\',{method:\'POST\',body:JSON.stringify(body)});loadUsers()}\nasync function ban(id,v){await api(\'/api/admin/users/\'+id+\'/adjust\',{method:\'POST\',body:JSON.stringify({ban:v})});loadUsers()}\nasync function loadTasks(){const d=await api(\'/api/admin/tasks\');document.getElementById(\'tasksBox\').innerHTML=d.map(t=>`<div class="card"><div class="row"><div><b>${esc(t.title)}</b><div class="muted">${esc(t.link)} | ৳${t.cash_reward} + 💎${t.diamond_reward} | daily ${t.daily_limit}</div></div><button class="btn red" onclick="delTask(${t.id})">Delete</button></div></div>`).join(\'\')}\nasync function addTask(){await api(\'/api/admin/tasks\',{method:\'POST\',body:JSON.stringify({title:document.getElementById(\'tt\').value,description:document.getElementById(\'tdesc\').value,link:document.getElementById(\'tl\').value,cash_reward:Number(document.getElementById(\'tc\').value||0),diamond_reward:Number(document.getElementById(\'td\').value||0),daily_limit:Number(document.getElementById(\'tlim\').value||1),active:true})});alert(\'Task added\');loadTasks()}\nasync function delTask(id){if(!confirm(\'Delete?\'))return;await api(\'/api/admin/tasks/\'+id,{method:\'DELETE\'});loadTasks()}\nasync function loadWithdraw(){const d=await api(\'/api/admin/withdrawals\');document.getElementById(\'wTable\').innerHTML=d.map(x=>`<tr><td>${x.id}</td><td>${esc(x.name)}<br>${x.telegram_id}</td><td>${x.method}</td><td>${x.number}</td><td>৳${x.amount}</td><td>${x.status}</td><td>${x.status===\'pending\'?`<button class="btn" onclick="wd(${x.id},\'approved\')">Approve</button> <button class="btn red" onclick="wd(${x.id},\'rejected\')">Reject</button>`:\'—\'}</td></tr>`).join(\'\')}\nasync function wd(id,status){await api(\'/api/admin/withdrawals/\'+id,{method:\'POST\',body:JSON.stringify({status,note:\'\'})});loadWithdraw()}\nasync function loadSupport(){const d=await api(\'/api/admin/support\');document.getElementById(\'supportBox\').innerHTML=d.map(x=>`<div class="card"><b>#${x.id} ${esc(x.name)} (${x.telegram_id})</b><p>${esc(x.message)}</p><div class="muted">Reply: ${esc(x.reply||\'\')}</div>${x.status===\'open\'?`<div class="row"><input id="r${x.id}" placeholder="Reply"><button class="btn" onclick="reply(${x.id})">Send</button></div>`:\'\'}</div>`).join(\'\')}\nasync function reply(id){await api(\'/api/admin/support/\'+id+\'/reply\',{method:\'POST\',body:JSON.stringify({reply:document.getElementById(\'r\'+id).value})});loadSupport()}\nasync function loadSettings(){const d=await api(\'/api/admin/settings\');Object.keys(d).forEach(k=>{const e=document.getElementById(\'s_\'+k);if(e)e.value=d[k]})}\nasync function saveSettings(){const keys=[\'app_name\',\'logo_url\',\'primary_color\',\'min_withdraw\',\'ref_reward\',\'daily_bonus\',\'diamond_rate\',\'bot_username\',\'company_channel_link\',\'company_group_link\',\'company_bot_link\',\'company_ad_link\',\'direct_link\',\'support_link\',\'welcome_text\',\'withdraw_notice\',\'maintenance\',\'level_config\'];const values={};keys.forEach(k=>values[k]=document.getElementById(\'s_\'+k).value);await api(\'/api/admin/settings\',{method:\'PUT\',body:JSON.stringify({values})});alert(\'Settings saved\')}\nasync function broadcast(){await api(\'/api/admin/broadcast\',{method:\'POST\',body:JSON.stringify({title:document.getElementById(\'bt\').value,message:document.getElementById(\'bm\').value})});alert(\'Broadcast queued/sent\')}\nasync function loadLedger(){const d=await api(\'/api/admin/ledger\');document.getElementById(\'lTable\').innerHTML=d.map(x=>`<tr><td>${x.telegram_id}</td><td>${x.amount}</td><td>${x.diamonds}</td><td>${esc(x.kind)}</td><td>${esc(x.note)}</td><td>${esc(x.created_at)}</td></tr>`).join(\'\')}\n</script>\n</body></html>\n'

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(INDEX_HTML)

@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    return HTMLResponse(ADMIN_HTML)

@app.get("/health")
def health():
    return {"ok": True, "service": "telegram-mini-app"}

@app.post("/api/auth")
def auth(request: Request):
    db = SessionLocal()
    try:
        user = user_from_request(db, request)
        if user.banned:
            raise HTTPException(403, "আপনার অ্যাকাউন্ট ব্লক করা হয়েছে")
        settings = get_settings(db)
        return {"user": serialize_user(user), "settings": public_settings(settings)}
    finally:
        db.close()

def serialize_user(u):
    return {
        "id": u.id, "telegram_id": u.telegram_id, "username": u.username,
        "first_name": u.first_name, "last_name": u.last_name,
        "balance": round(u.balance, 2), "diamonds": u.diamonds,
        "total_earned": round(u.total_earned, 2), "level": u.level,
        "referral_code": u.referral_code, "banned": u.banned
    }

def public_settings(s):
    return {k: s.get(k, "") for k in DEFAULTS.keys() if k != "level_config"}

@app.get("/api/home")
def home(request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        s = get_settings(db)
        tasks = db.query(Task).filter(Task.active == True).order_by(Task.id.desc()).limit(6).all()
        notes = db.query(Notification).filter(
            (Notification.user_id == None) | (Notification.user_id == u.id)
        ).order_by(Notification.id.desc()).limit(5).all()
        return {
            "user": serialize_user(u),
            "settings": public_settings(s),
            "tasks": [serialize_task(x) for x in tasks],
            "notifications": [{"title": n.title, "message": n.message} for n in notes]
        }
    finally:
        db.close()

def serialize_task(t):
    return {
        "id": t.id, "title": t.title, "description": t.description,
        "link": t.link, "cash_reward": t.cash_reward,
        "diamond_reward": t.diamond_reward, "daily_limit": t.daily_limit,
        "active": t.active
    }

@app.get("/api/tasks")
def tasks(request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        items = []
        for t in db.query(Task).filter(Task.active == True).order_by(Task.id.desc()).all():
            used = today_claims(db, u.id, t.id)
            items.append({**serialize_task(t), "claimed_today": used, "remaining": max(t.daily_limit-used, 0)})
        return items
    finally:
        db.close()

class ClaimBody(BaseModel):
    task_id: int

@app.post("/api/tasks/claim")
def claim_task(body: ClaimBody, request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        t = db.query(Task).filter(Task.id == body.task_id, Task.active == True).first()
        if not t:
            raise HTTPException(404, "Task not found")
        used = today_claims(db, u.id, t.id)
        if used >= t.daily_limit:
            raise HTTPException(400, "আজকের এই টাস্ক লিমিট শেষ")
        db.add(TaskClaim(user_id=u.id, task_id=t.id))
        add_reward(db, u, t.cash_reward, t.diamond_reward, "task", t.title)
        return {"ok": True, "user": serialize_user(u), "reward": {"cash": t.cash_reward, "diamonds": t.diamond_reward}}
    finally:
        db.close()

@app.post("/api/daily-bonus")
def daily_bonus(request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        start = now_bd().replace(hour=0, minute=0, second=0, microsecond=0)
        already = db.query(Ledger).filter(
            Ledger.user_id == u.id, Ledger.kind == "daily_bonus", Ledger.created_at >= start
        ).first()
        if already:
            raise HTTPException(400, "আজকের বোনাস নেওয়া হয়েছে")
        amount = float(get_settings(db).get("daily_bonus", "5"))
        add_reward(db, u, amount, 0, "daily_bonus", "Daily bonus")
        return {"ok": True, "user": serialize_user(u), "amount": amount}
    finally:
        db.close()

@app.get("/api/referral")
def referral(request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        count = db.query(User).filter(User.referred_by == u.referral_code).count()
        reward = float(get_settings(db).get("ref_reward", "10"))
        username = get_settings(db).get("bot_username") or BOT_USERNAME
        link = f"https://t.me/{username}?start=ref_{u.referral_code}" if username else ""
        return {"code": u.referral_code, "count": count, "reward": reward, "link": link}
    finally:
        db.close()

class WithdrawBody(BaseModel):
    method: str
    number: str
    amount: float

@app.post("/api/withdraw")
def withdraw(body: WithdrawBody, request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        s = get_settings(db)
        minimum = float(s.get("min_withdraw", "100"))
        if body.amount < minimum:
            raise HTTPException(400, f"সর্বনিম্ন উইথড্র {minimum} টাকা")
        if body.amount > u.balance:
            raise HTTPException(400, "ব্যালেন্স পর্যাপ্ত নয়")
        if body.method.lower() not in ("bkash", "nagad"):
            raise HTTPException(400, "শুধু bKash বা Nagad")
        if len(body.number.strip()) < 10:
            raise HTTPException(400, "সঠিক নম্বর দিন")
        u.balance -= body.amount
        db.add(Ledger(user_id=u.id, amount=-body.amount, kind="withdraw_request", note=body.method))
        w = Withdrawal(user_id=u.id, method=body.method.lower(), number=body.number.strip(), amount=body.amount)
        db.add(w)
        db.commit()
        return {"ok": True, "message": "উইথড্র রিকোয়েস্ট জমা হয়েছে", "user": serialize_user(u)}
    finally:
        db.close()

@app.get("/api/withdrawals")
def withdrawals(request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        rows = db.query(Withdrawal).filter(Withdrawal.user_id == u.id).order_by(Withdrawal.id.desc()).limit(30).all()
        return [{"id": x.id, "method": x.method, "number": x.number, "amount": x.amount,
                 "status": x.status, "created_at": str(x.created_at)} for x in rows]
    finally:
        db.close()

class SupportBody(BaseModel):
    message: str

@app.post("/api/support")
def support(body: SupportBody, request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        if not body.message.strip():
            raise HTTPException(400, "মেসেজ লিখুন")
        db.add(SupportMessage(user_id=u.id, message=body.message.strip()))
        db.commit()
        return {"ok": True}
    finally:
        db.close()

@app.get("/api/support")
def support_list(request: Request):
    db = SessionLocal()
    try:
        u = user_from_request(db, request)
        rows = db.query(SupportMessage).filter(SupportMessage.user_id == u.id).order_by(SupportMessage.id.desc()).limit(20).all()
        return [{"id": x.id, "message": x.message, "reply": x.reply, "status": x.status} for x in rows]
    finally:
        db.close()

# ---------------- ADMIN API ----------------

def admin_db(key):
    admin_guard(key)
    return SessionLocal()

@app.get("/api/admin/dashboard")
def admin_dashboard(x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        return {
            "users": db.query(User).count(),
            "active_users": db.query(User).filter(User.banned == False).count(),
            "balance": round(db.query(func.coalesce(func.sum(User.balance), 0)).scalar() or 0, 2),
            "diamonds": int(db.query(func.coalesce(func.sum(User.diamonds), 0)).scalar() or 0),
            "withdraw_pending": db.query(Withdrawal).filter(Withdrawal.status == "pending").count(),
            "withdraw_total": round(db.query(func.coalesce(func.sum(Withdrawal.amount), 0)).scalar() or 0, 2),
            "tasks": db.query(Task).count(),
            "support_open": db.query(SupportMessage).filter(SupportMessage.status == "open").count()
        }
    finally:
        db.close()

@app.get("/api/admin/settings")
def admin_settings(x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        return get_settings(db)
    finally:
        db.close()

class SettingsBody(BaseModel):
    values: dict

@app.put("/api/admin/settings")
def update_settings(body: SettingsBody, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        for k, v in body.values.items():
            if k in DEFAULTS:
                set_setting(db, k, v)
        db.commit()
        return get_settings(db)
    finally:
        db.close()

@app.get("/api/admin/users")
def admin_users(x_admin_key: Optional[str] = Header(None), q: str = ""):
    db = admin_db(x_admin_key)
    try:
        query = db.query(User).order_by(User.id.desc())
        if q.strip():
            like = f"%{q.strip()}%"
            query = query.filter((User.telegram_id.like(like)) | (User.username.like(like)) | (User.first_name.like(like)))
        return [serialize_user(x) for x in query.limit(200).all()]
    finally:
        db.close()

class UserAdjustBody(BaseModel):
    amount: float = 0
    diamonds: int = 0
    ban: Optional[bool] = None

@app.post("/api/admin/users/{user_id}/adjust")
def adjust_user(user_id: int, body: UserAdjustBody, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if not u: raise HTTPException(404, "User not found")
        u.balance += body.amount
        u.diamonds += body.diamonds
        if body.ban is not None: u.banned = body.ban
        if body.amount or body.diamonds:
            db.add(Ledger(user_id=u.id, amount=body.amount, diamonds=body.diamonds, kind="admin_adjust", note="Admin adjustment"))
        db.commit()
        return serialize_user(u)
    finally:
        db.close()

class TaskBody(BaseModel):
    title: str
    description: str = ""
    link: str = ""
    cash_reward: float = 0
    diamond_reward: int = 0
    daily_limit: int = 1
    active: bool = True

@app.get("/api/admin/tasks")
def admin_tasks(x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        return [serialize_task(x) for x in db.query(Task).order_by(Task.id.desc()).all()]
    finally:
        db.close()

@app.post("/api/admin/tasks")
def create_task(body: TaskBody, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        t = Task(**body.model_dump())
        db.add(t); db.commit(); db.refresh(t)
        return serialize_task(t)
    finally:
        db.close()

@app.put("/api/admin/tasks/{task_id}")
def edit_task(task_id: int, body: TaskBody, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        t = db.query(Task).filter(Task.id == task_id).first()
        if not t: raise HTTPException(404, "Task not found")
        for k, v in body.model_dump().items(): setattr(t, k, v)
        db.commit()
        return serialize_task(t)
    finally:
        db.close()

@app.delete("/api/admin/tasks/{task_id}")
def delete_task(task_id: int, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        t = db.query(Task).filter(Task.id == task_id).first()
        if not t: raise HTTPException(404, "Task not found")
        db.delete(t); db.commit()
        return {"ok": True}
    finally:
        db.close()

@app.get("/api/admin/withdrawals")
def admin_withdrawals(x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        rows = db.query(Withdrawal, User).join(User, Withdrawal.user_id == User.id).order_by(Withdrawal.id.desc()).limit(300).all()
        return [{"id": w.id, "user_id": u.id, "telegram_id": u.telegram_id, "name": u.first_name,
                 "method": w.method, "number": w.number, "amount": w.amount, "status": w.status,
                 "created_at": str(w.created_at)} for w,u in rows]
    finally:
        db.close()

class WithdrawalAction(BaseModel):
    status: str
    note: str = ""

@app.post("/api/admin/withdrawals/{wid}")
def action_withdrawal(wid: int, body: WithdrawalAction, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        w = db.query(Withdrawal).filter(Withdrawal.id == wid).first()
        if not w: raise HTTPException(404, "Withdrawal not found")
        if body.status not in ("approved", "rejected", "pending"):
            raise HTTPException(400, "Invalid status")
        if w.status == "pending" and body.status == "rejected":
            u = db.query(User).filter(User.id == w.user_id).first()
            u.balance += w.amount
            db.add(Ledger(user_id=u.id, amount=w.amount, kind="withdraw_refund", note="Withdrawal rejected"))
        w.status = body.status
        w.admin_note = body.note
        w.processed_at = now_bd() if body.status != "pending" else None
        db.commit()
        return {"ok": True}
    finally:
        db.close()

@app.get("/api/admin/support")
def admin_support(x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        rows = db.query(SupportMessage, User).join(User, SupportMessage.user_id == User.id).order_by(SupportMessage.id.desc()).limit(300).all()
        return [{"id": m.id, "user_id": u.id, "telegram_id": u.telegram_id, "name": u.first_name,
                 "message": m.message, "reply": m.reply, "status": m.status,
                 "created_at": str(m.created_at)} for m,u in rows]
    finally:
        db.close()

class ReplyBody(BaseModel):
    reply: str

@app.post("/api/admin/support/{sid}/reply")
async def reply_support(sid: int, body: ReplyBody, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        m = db.query(SupportMessage).filter(SupportMessage.id == sid).first()
        if not m: raise HTTPException(404, "Message not found")
        m.reply = body.reply
        m.status = "replied"
        m.replied_at = now_bd()
        db.commit()
        if BOT_TOKEN:
            u = db.query(User).filter(User.id == m.user_id).first()
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    await client.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                                      json={"chat_id": u.telegram_id, "text": f"📩 Support Reply\n\n{body.reply}"})
            except Exception:
                pass
        return {"ok": True}
    finally:
        db.close()

class BroadcastBody(BaseModel):
    title: str
    message: str

@app.post("/api/admin/broadcast")
async def broadcast(body: BroadcastBody, x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        users = db.query(User).filter(User.banned == False).all()
        for u in users:
            db.add(Notification(user_id=u.id, title=body.title, message=body.message))
        db.commit()
        sent = 0
        if BOT_TOKEN:
            async with httpx.AsyncClient(timeout=15) as client:
                for u in users:
                    try:
                        r = await client.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                                              json={"chat_id": u.telegram_id, "text": f"📢 {body.title}\n\n{body.message}"})
                        if r.is_success: sent += 1
                    except Exception:
                        continue
        return {"ok": True, "notifications": len(users), "telegram_sent": sent}
    finally:
        db.close()

@app.get("/api/admin/ledger")
def admin_ledger(x_admin_key: Optional[str] = Header(None)):
    db = admin_db(x_admin_key)
    try:
        rows = db.query(Ledger, User).join(User, Ledger.user_id == User.id).order_by(Ledger.id.desc()).limit(500).all()
        return [{"id": l.id, "user_id": u.id, "telegram_id": u.telegram_id, "amount": l.amount,
                 "diamonds": l.diamonds, "kind": l.kind, "note": l.note, "created_at": str(l.created_at)} for l,u in rows]
    finally:
        db.close()
