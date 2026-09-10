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
let urlParams = new URLSearchPar
