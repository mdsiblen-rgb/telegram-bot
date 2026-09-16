"""
প্রতিদিনের কাজ BD — Telegram Mini App + Admin Panel
Single-file Flask application.

ENV variables required:
  BOT_TOKEN=your_telegram_bot_token
  ADMIN_ID=8807178385
  DATABASE_PATH=app.db                 # optional
  WEBAPP_URL=https://your-domain/...   # optional

Install:
  pip install flask requests gunicorn

Run:
  gunicorn main:app

Notes:
- This file is designed as a standalone Mini App backend. If your existing main.py
  already contains a Telegram bot, merge the Flask routes/templates into that file
  rather than running a second app.
- NEVER put BOT_TOKEN in public source code.
- Telegram WebApp authentication is verified with HMAC before user data is accepted.
"""

import os
import json
import hmac
import hashlib
import sqlite3
import time
import secrets
from urllib.parse import parse_qsl
from functools import wraps

import requests
from flask import Flask, request, jsonify, render_template_string, session, redirect

APP_NAME = "Protidiner Kaj BD"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8807178385"))
DB_PATH = os.getenv("DATABASE_PATH", "app.db")

DEFAULT_SETTINGS = {
    "app_name": "Protidiner Kaj BD",
    "welcome_title": "প্রতিদিনের কাজ BD",
    "welcome_text": "প্রতিদিন নতুন কাজ করুন, রিওয়ার্ড সংগ্রহ করুন এবং রেফার করে আয় বাড়ান।",
    "support_text": "যেকোনো সমস্যা বা সাহায্যের জন্য নিচের বক্সে আপনার মেসেজ লিখুন।",
    "currency": "৳",
    "min_withdraw": "100",
    "referral_bonus": "10",
    "daily_bonus": "5",
    "maintenance": "0",
    "support_username": "@ProtidinerKajBD",
    "channel_link": "https://t.me/ProtidinerKajBD",
    "group_link": "https://t.me/+hb8X-V4buToxYmJl",
    "bot_link": "https://t.me/ProtidinerKaj_BD_Bot",
    "ad_script_1": "<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>",
    "ad_script_2": "<script src='//libtl.com/sdk.js' data-zone='11798857' data-sdk='show_11798857'></script>",
    "ad_link": "https://omg10.com/4/11760259",
}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

# ---------- Database ----------

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT DEFAULT '',
        first_name TEXT DEFAULT '',
        balance REAL DEFAULT 0,
        referral_code TEXT UNIQUE,
        referred_by INTEGER DEFAULT NULL,
        total_earned REAL DEFAULT 0,
        total_withdrawn REAL DEFAULT 0,
        blocked INTEGER DEFAULT 0,
        created_at INTEGER NOT NULL,
        last_daily INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        url TEXT NOT NULL,
        reward REAL DEFAULT 0,
        task_type TEXT DEFAULT 'link',
        active INTEGER DEFAULT 1,
        created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS withdrawals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        method TEXT NOT NULL,
        account TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        note TEXT DEFAULT '',
        created_at INTEGER NOT NULL,
        processed_at INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS support (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        reply TEXT DEFAULT '',
        status TEXT DEFAULT 'open',
        created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS task_claims (
        user_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        claimed_at INTEGER NOT NULL,
        PRIMARY KEY(user_id, task_id)
    );
    """)
    for k, v in DEFAULT_SETTINGS.items():
        cur.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)", (k, v))
    con.commit()
    con.close()

init_db()

def get_settings():
    con = db()
    rows = con.execute("SELECT key,value FROM settings").fetchall()
    con.close()
    data = DEFAULT_SETTINGS.copy()
    data.update({r["key"]: r["value"] for r in rows})
    return data

def set_setting(key, value):
    con = db()
    con.execute("INSERT INTO settings(key,value) VALUES(?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))
    con.commit()
    con.close()

# ---------- Telegram WebApp auth ----------

def verify_init_data(init_data: str):
    if not init_data or not BOT_TOKEN:
        return None

    try:
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = pairs.pop("hash", None)
        if not received_hash:
            return None

        data_check_string = "\n".join(
            f"{k}={pairs[k]}" for k in sorted(pairs)
        )
        secret_key = hmac.new(
            b"WebAppData",
            BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        calculated = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(calculated, received_hash):
            return None

        # Reject old init data (> 24h).
        auth_date = int(pairs.get("auth_date", "0"))
        if auth_date and time.time() - auth_date > 86400:
            return None

        user = json.loads(pairs.get("user", "{}"))
        if not user.get("id"):
            return None
        return user
    except Exception:
        return None

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    con = db()
    row = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    con.close()
    return row

def ensure_user(tg_user):
    uid = int(tg_user["id"])
    username = tg_user.get("username", "")
    first_name = tg_user.get("first_name", "")
    con = db()
    row = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    if not row:
        code = f"U{uid}"
        con.execute("""
            INSERT INTO users(id,username,first_name,referral_code,created_at)
            VALUES(?,?,?,?,?)
        """, (uid, username, first_name, code, int(time.time())))
    else:
        con.execute("UPDATE users SET username=?, first_name=? WHERE id=?",
                    (username, first_name, uid))
    con.commit()
    con.close()

def api_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = request.headers.get("X-Telegram-Init-Data", "")
        tg_user = verify_init_data(data)
        if not tg_user:
            return jsonify({"ok": False, "error": "Telegram authentication required"}), 401
        ensure_user(tg_user)
        session["user_id"] = int(tg_user["id"])
        row = current_user()
        if row and row["blocked"]:
            return jsonify({"ok": False, "error": "আপনার অ্যাকাউন্ট ব্লক করা হয়েছে।"}), 403
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Admin panel accepts either a verified Telegram WebApp session or
        # a verified login generated by /admin/login.
        if session.get("admin_id") == ADMIN_ID:
            return fn(*args, **kwargs)
        data = request.headers.get("X-Telegram-Init-Data", "")
        tg_user = verify_init_data(data)
        if tg_user and int(tg_user["id"]) == ADMIN_ID:
            session["admin_id"] = ADMIN_ID
            return fn(*args, **kwargs)
        return jsonify({"ok": False, "error": "Admin access denied"}), 403
    return wrapper

# ---------- Main API ----------

@app.get("/")
def index():
    return render_template_string(MINI_APP_HTML, settings=get_settings())

@app.post("/api/login")
def login():
    tg_user = verify_init_data(request.json.get("initData", "") if request.is_json else "")
    if not tg_user:
        return jsonify({"ok": False, "error": "Invalid Telegram data"}), 401
    ensure_user(tg_user)
    session["user_id"] = int(tg_user["id"])
    return jsonify({"ok": True})

@app.get("/api/me")
@api_login_required
def me():
    u = current_user()
    s = get_settings()
    con = db()
    withdrawals = con.execute(
        "SELECT id,method,amount,status,created_at FROM withdrawals "
        "WHERE user_id=? ORDER BY id DESC LIMIT 10", (u["id"],)
    ).fetchall()
    supports = con.execute(
        "SELECT id,message,reply,status,created_at FROM support "
        "WHERE user_id=? ORDER BY id DESC LIMIT 10", (u["id"],)
    ).fetchall()
    con.close()
    return jsonify({
        "ok": True,
        "user": dict(u),
        "settings": s,
        "withdrawals": [dict(x) for x in withdrawals],
        "support": [dict(x) for x in supports],
    })

@app.get("/api/tasks")
@api_login_required
def tasks():
    u = current_user()
    con = db()
    rows = con.execute("""
        SELECT t.*, CASE WHEN c.user_id IS NULL THEN 0 ELSE 1 END AS claimed
        FROM tasks t
        LEFT JOIN task_claims c ON c.task_id=t.id AND c.user_id=?
        WHERE t.active=1 ORDER BY t.id DESC
    """, (u["id"],)).fetchall()
    con.close()
    return jsonify({"ok": True, "tasks": [dict(x) for x in rows]})

@app.post("/api/task/<int:task_id>/claim")
@api_login_required
def claim_task(task_id):
    uid = current_user()["id"]
    con = db()
    task = con.execute("SELECT * FROM tasks WHERE id=? AND active=1", (task_id,)).fetchone()
    if not task:
        con.close()
        return jsonify({"ok": False, "error": "Task not found"}), 404

    claimed = con.execute(
        "SELECT 1 FROM task_claims WHERE user_id=? AND task_id=?",
        (uid, task_id)
    ).fetchone()
    if claimed:
        con.close()
        return jsonify({"ok": False, "error": "এই কাজটি আগে সম্পন্ন করেছেন।"})

    con.execute("INSERT INTO task_claims(user_id,task_id,claimed_at) VALUES(?,?,?)",
                (uid, task_id, int(time.time())))
    con.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+? WHERE id=?",
                (task["reward"], task["reward"], uid))
    con.commit()
    con.close()
    return jsonify({"ok": True, "reward": task["reward"]})

@app.post("/api/daily")
@api_login_required
def daily():
    uid = current_user()["id"]
    s = get_settings()
    reward = float(s.get("daily_bonus", "5") or 0)
    now = int(time.time())
    con = db()
    u = con.execute("SELECT last_daily FROM users WHERE id=?", (uid,)).fetchone()
    if u and u["last_daily"] and now - u["last_daily"] < 86400:
        con.close()
        return jsonify({"ok": False, "error": "আজকের Daily Bonus নেওয়া হয়েছে।"})
    con.execute("UPDATE users SET balance=balance+?, total_earned=total_earned+?, last_daily=? WHERE id=?",
                (reward, reward, now, uid))
    con.commit()
    con.close()
    return jsonify({"ok": True, "reward": reward})

@app.post("/api/support")
@api_login_required
def support():
    uid = current_user()["id"]
    message = (request.json or {}).get("message", "").strip()
    if not message:
        return jsonify({"ok": False, "error": "মেসেজ লিখুন।"}), 400
    if len(message) > 2000:
        return jsonify({"ok": False, "error": "মেসেজ সর্বোচ্চ ২০০০ অক্ষর।"}), 400
    con = db()
    con.execute("INSERT INTO support(user_id,message,created_at) VALUES(?,?,?)",
                (uid, message, int(time.time())))
    con.commit()
    con.close()
    return jsonify({"ok": True, "message": "আপনার মেসেজ পাঠানো হয়েছে।"})

@app.post("/api/withdraw")
@api_login_required
def withdraw():
    uid = current_user()["id"]
    body = request.json or {}
    method = str(body.get("method", "")).strip()
    account = str(body.get("account", "")).strip()
    try:
        amount = float(body.get("amount", 0))
    except Exception:
        amount = 0

    s = get_settings()
    minimum = float(s.get("min_withdraw", "100") or 100)
    if method not in ("bKash", "Nagad", "Bank"):
        return jsonify({"ok": False, "error": "সঠিক পেমেন্ট মেথড নির্বাচন করুন।"}), 400
    if len(account) < 5:
        return jsonify({"ok": False, "error": "পেমেন্ট অ্যাকাউন্ট দিন।"}), 400
    if amount < minimum:
        return jsonify({"ok": False, "error": f"Minimum withdrawal {minimum:g} {s.get('currency','৳')}"}), 400

    con = db()
    u = con.execute("SELECT balance FROM users WHERE id=?", (uid,)).fetchone()
    if not u or u["balance"] < amount:
        con.close()
        return jsonify({"ok": False, "error": "আপনার পর্যাপ্ত ব্যালেন্স নেই।"}), 400

    con.execute("UPDATE users SET balance=balance-? WHERE id=?", (amount, uid))
    con.execute("""
        INSERT INTO withdrawals(user_id,method,account,amount,created_at)
        VALUES(?,?,?,?,?)
    """, (uid, method, account, amount, int(time.time())))
    con.commit()
    con.close()
    return jsonify({"ok": True, "message": "Withdrawal request submitted."})

@app.get("/api/referral")
@api_login_required
def referral():
    u = current_user()
    base = request.host_url.rstrip("/")
    code = u["referral_code"]
    link = f"{base}/?ref={code}"
    return jsonify({"ok": True, "code": code, "link": link})

# ---------- Admin API ----------

@app.get("/admin")
def admin_page():
    return render_template_string(ADMIN_HTML, admin_id=ADMIN_ID, settings=get_settings())

@app.post("/admin/session")
def admin_session():
    data = request.headers.get("X-Telegram-Init-Data", "")
    tg_user = verify_init_data(data)
    if not tg_user or int(tg_user["id"]) != ADMIN_ID:
        return jsonify({"ok": False, "error": "শুধু Admin Telegram account থেকে প্রবেশ করুন।"}), 403
    session["admin_id"] = ADMIN_ID
    return jsonify({"ok": True})

@app.get("/api/admin/stats")
@admin_required
def admin_stats():
    con = db()
    users = con.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
    active = con.execute("SELECT COUNT(*) c FROM users WHERE blocked=0").fetchone()["c"]
    pending = con.execute("SELECT COUNT(*) c FROM withdrawals WHERE status='pending'").fetchone()["c"]
    total_balance = con.execute("SELECT COALESCE(SUM(balance),0) x FROM users").fetchone()["x"]
    total_earned = con.execute("SELECT COALESCE(SUM(total_earned),0) x FROM users").fetchone()["x"]
    total_withdrawn = con.execute("SELECT COALESCE(SUM(total_withdrawn),0) x FROM users").fetchone()["x"]
    con.close()
    return jsonify({
        "ok": True, "users": users, "active": active, "pending": pending,
        "total_balance": total_balance, "total_earned": total_earned,
        "total_withdrawn": total_withdrawn
    })

@app.get("/api/admin/users")
@admin_required
def admin_users():
    q = request.args.get("q", "").strip()
    con = db()
    if q:
        rows = con.execute("""
            SELECT id,username,first_name,balance,total_earned,total_withdrawn,blocked,created_at
            FROM users WHERE CAST(id AS TEXT) LIKE ? OR username LIKE ? OR first_name LIKE ?
            ORDER BY id DESC LIMIT 100
        """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
    else:
        rows = con.execute("""
            SELECT id,username,first_name,balance,total_earned,total_withdrawn,blocked,created_at
            FROM users ORDER BY id DESC LIMIT 100
        """).fetchall()
    con.close()
    return jsonify({"ok": True, "users": [dict(x) for x in rows]})

@app.post("/api/admin/user/<int:uid>/balance")
@admin_required
def admin_balance(uid):
    amount = float((request.json or {}).get("amount", 0))
    con = db()
    con.execute("UPDATE users SET balance=balance+? WHERE id=?", (amount, uid))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.post("/api/admin/user/<int:uid>/block")
@admin_required
def admin_block(uid):
    blocked = int((request.json or {}).get("blocked", 1))
    con = db()
    con.execute("UPDATE users SET blocked=? WHERE id=?", (blocked, uid))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.get("/api/admin/tasks")
@admin_required
def admin_tasks():
    con = db()
    rows = con.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    con.close()
    return jsonify({"ok": True, "tasks": [dict(x) for x in rows]})

@app.post("/api/admin/tasks")
@admin_required
def admin_create_task():
    b = request.json or {}
    title = str(b.get("title", "")).strip()
    url = str(b.get("url", "")).strip()
    description = str(b.get("description", "")).strip()
    task_type = str(b.get("task_type", "link")).strip()
    reward = float(b.get("reward", 0))
    if not title or not url or reward < 0:
        return jsonify({"ok": False, "error": "Title, URL ও Reward সঠিকভাবে দিন।"}), 400
    con = db()
    con.execute("""
        INSERT INTO tasks(title,description,url,reward,task_type,active,created_at)
        VALUES(?,?,?,?,?,?,?)
    """, (title, description, url, reward, task_type, 1, int(time.time())))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.post("/api/admin/task/<int:tid>")
@admin_required
def admin_update_task(tid):
    b = request.json or {}
    con = db()
    task = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not task:
        con.close()
        return jsonify({"ok": False, "error": "Task not found"}), 404
    fields = ["title","description","url","reward","task_type","active"]
    vals = {k: b[k] for k in fields if k in b}
    if vals:
        sql = ", ".join(f"{k}=?" for k in vals)
        con.execute(f"UPDATE tasks SET {sql} WHERE id=?", (*vals.values(), tid))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.delete("/api/admin/task/<int:tid>")
@admin_required
def admin_delete_task(tid):
    con = db()
    con.execute("DELETE FROM tasks WHERE id=?", (tid,))
    con.execute("DELETE FROM task_claims WHERE task_id=?", (tid,))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.get("/api/admin/withdrawals")
@admin_required
def admin_withdrawals():
    con = db()
    rows = con.execute("""
        SELECT w.*, u.username,u.first_name
        FROM withdrawals w LEFT JOIN users u ON u.id=w.user_id
        ORDER BY w.id DESC LIMIT 200
    """).fetchall()
    con.close()
    return jsonify({"ok": True, "withdrawals": [dict(x) for x in rows]})

@app.post("/api/admin/withdrawal/<int:wid>")
@admin_required
def admin_withdrawal(wid):
    b = request.json or {}
    status = b.get("status")
    note = str(b.get("note", ""))
    if status not in ("approved", "rejected", "pending"):
        return jsonify({"ok": False, "error": "Invalid status"}), 400

    con = db()
    w = con.execute("SELECT * FROM withdrawals WHERE id=?", (wid,)).fetchone()
    if not w:
        con.close()
        return jsonify({"ok": False, "error": "Withdrawal not found"}), 404

    old = w["status"]
    # If rejected after money was reserved, refund once.
    if status == "rejected" and old != "rejected":
        con.execute("UPDATE users SET balance=balance+? WHERE id=?", (w["amount"], w["user_id"]))
    # If moving away from rejected back to pending/approved, take the refund back.
    if old == "rejected" and status != "rejected":
        con.execute("UPDATE users SET balance=balance-? WHERE id=?", (w["amount"], w["user_id"]))

    if status == "approved" and old != "approved":
        con.execute("UPDATE users SET total_withdrawn=total_withdrawn+? WHERE id=?",
                    (w["amount"], w["user_id"]))
    if old == "approved" and status != "approved":
        con.execute("UPDATE users SET total_withdrawn=total_withdrawn-? WHERE id=?",
                    (w["amount"], w["user_id"]))

    con.execute("UPDATE withdrawals SET status=?,note=?,processed_at=? WHERE id=?",
                (status, note, int(time.time()), wid))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.get("/api/admin/support")
@admin_required
def admin_support():
    con = db()
    rows = con.execute("""
        SELECT s.*,u.username,u.first_name
        FROM support s LEFT JOIN users u ON u.id=s.user_id
        ORDER BY s.id DESC LIMIT 200
    """).fetchall()
    con.close()
    return jsonify({"ok": True, "support": [dict(x) for x in rows]})

@app.post("/api/admin/support/<int:sid>")
@admin_required
def admin_support_reply(sid):
    b = request.json or {}
    reply = str(b.get("reply", "")).strip()
    status = str(b.get("status", "answered"))
    con = db()
    con.execute("UPDATE support SET reply=?,status=? WHERE id=?",
                (reply, status, sid))
    con.commit()
    con.close()
    return jsonify({"ok": True})

@app.get("/api/admin/settings")
@admin_required
def admin_settings():
    return jsonify({"ok": True, "settings": get_settings()})

@app.post("/api/admin/settings")
@admin_required
def admin_save_settings():
    b = request.json or {}
    for k in DEFAULT_SETTINGS:
        if k in b:
            set_setting(k, b[k])
    return jsonify({"ok": True, "settings": get_settings()})

# ---------- HTML: Mini App ----------

MINI_APP_HTML = r"""
<!doctype html>
<html lang="bn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>{{ settings.app_name }}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{box-sizing:border-box}body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#172033}
.app{max-width:560px;margin:auto;padding:14px 14px 90px}
.hero{background:linear-gradient(135deg,#111827,#334155);color:white;border-radius:24px;padding:22px;box-shadow:0 12px 35px #0002}
.hero h1{margin:0 0 8px;font-size:25px}.hero p{margin:0;opacity:.85;line-height:1.5}
.balance{margin-top:18px;background:#fff;color:#111827;border-radius:18px;padding:18px}
.balance small{color:#64748b}.amount{font-size:32px;font-weight:800;margin-top:4px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.card{background:#fff;border-radius:18px;padding:16px;box-shadow:0 5px 18px #0000000b}
.card h3{margin:0 0 7px;font-size:17px}.card p{margin:0;color:#64748b;font-size:13px;line-height:1.45}
.btn{border:0;border-radius:13px;padding:12px 14px;background:#111827;color:#fff;font-weight:700;width:100%;margin-top:10px}
.btn.secondary{background:#eef2f7;color:#111827}.btn.success{background:#166534}.btn.warn{background:#92400e}
.section{display:none;margin-top:16px}.section.active{display:block}
.input,.textarea,.select{width:100%;border:1px solid #e2e8f0;border-radius:12px;padding:12px;margin-top:8px;font-size:15px;background:#fff}
.textarea{min-height:100px;resize:vertical}
.task{background:#fff;border-radius:17px;padding:15px;margin:10px 0;border:1px solid #e8edf4}
.task .reward{font-weight:800;margin-top:7px}.task a{display:block;color:#2563eb;word-break:break-all;margin-top:7px;font-size:13px}
.nav{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #e5e7eb;display:flex;justify-content:center;z-index:20}
.nav button{border:0;background:white;padding:12px 8px;flex:1;max-width:112px;font-size:12px;color:#64748b}.nav button b{display:block;font-size:18px;margin-bottom:3px}.nav button.active{color:#111827;font-weight:800}
.row{display:flex;gap:8px}.row>*{flex:1}
.notice{padding:12px;border-radius:13px;background:#fff7ed;color:#9a3412;margin-top:12px}
.hidden{display:none!important}
</style>
</head>
<body>
<div class="app">
  <div class="hero">
    <h1 id="appName">{{ settings.welcome_title }}</h1>
    <p id="welcome">{{ settings.welcome_text }}</p>
    <div class="balance">
      <small>আপনার বর্তমান ব্যালেন্স</small>
      <div class="amount"><span id="currency">{{ settings.currency }}</span><span id="balance">0</span></div>
    </div>
  </div>

  <div id="home" class="section active">
    <div class="grid">
      <div class="card"><h3>💰 Earn</h3><p>নতুন কাজ সম্পন্ন করে Reward সংগ্রহ করুন।</p><button class="btn" onclick="showTab('earn')">কাজ দেখুন</button></div>
      <div class="card"><h3>👥 Invite</h3><p>বন্ধুদের ইনভাইট করে Referral Bonus পান।</p><button class="btn" onclick="showTab('invite')">Invite করুন</button></div>
      <div class="card"><h3>💳 Withdraw</h3><p>ন্যূনতম ব্যালেন্স হলে উত্তোলনের আবেদন করুন।</p><button class="btn" onclick="showTab('withdraw')">Withdraw</button></div>
      <div class="card"><h3>🎁 Daily Bonus</h3><p>প্রতিদিন একবার Daily Bonus নেওয়ার সুযোগ।</p><button class="btn success" onclick="dailyBonus()">Bonus নিন</button></div>
    </div>
    <div class="card" style="margin-top:12px"><h3>📢 আমাদের কমিউনিটি</h3>
      <button class="btn secondary" onclick="openLink('{{ settings.channel_link }}')">📢 Channel</button>
      <button class="btn secondary" onclick="openLink('{{ settings.group_link }}')">👥 Group</button>
      <button class="btn secondary" onclick="openLink('{{ settings.bot_link }}')">🤖 Bot</button>
    </div>
    <div id="homeNotice"></div>
  </div>

  <div id="earn" class="section">
    <div class="card"><h3>💰 Available Tasks</h3><p>কাজের লিংকে গিয়ে কাজ শেষ করার পর Claim করুন।</p></div>
    <div id="tasks"></div>
  </div>

  <div id="invite" class="section">
    <div class="card">
      <h3>👥 Referral Program</h3>
      <p>আপনার Referral Link বন্ধুদের পাঠান। Admin Panel থেকে Bonus পরিবর্তন করা যাবে।</p>
      <input id="refLink" class="input" readonly>
      <button class="btn" onclick="copyRef()">📋 Copy Referral Link</button>
      <button class="btn secondary" onclick="shareRef()">📤 Share</button>
    </div>
  </div>

  <div id="withdraw" class="section">
    <div class="card">
      <h3>💳 Withdraw Request</h3>
      <p>Minimum: <b id="minWithdraw">{{ settings.currency }}{{ settings.min_withdraw }}</b></p>
      <select id="method" class="select"><option>bKash</option><option>Nagad</option><option>Bank</option></select>
      <input id="account" class="input" placeholder="বিকাশ/নগদ নম্বর বা ব্যাংক তথ্য">
      <input id="amount" class="input" type="number" placeholder="Amount">
      <button class="btn" onclick="withdraw()">Submit Request</button>
      <div id="withdrawHistory"></div>
    </div>
  </div>

  <div id="profile" class="section">
    <div class="card"><h3>👤 Profile</h3>
      <p>ID: <b id="uid">-</b></p><p>Username: <b id="username">-</b></p>
      <p>Total Earned: <b id="earned">0</b></p>
      <p>Total Withdrawn: <b id="withdrawn">0</b></p>
    </div>
    <div class="card" style="margin-top:12px">
      <h3>🆘 Support</h3>
      <p>{{ settings.support_text }}</p>
      <textarea id="supportMsg" class="textarea" placeholder="আপনার সমস্যাটি লিখুন..."></textarea>
      <button class="btn" onclick="sendSupport()">মেসেজ পাঠান</button>
      <div id="supportHistory"></div>
    </div>
  </div>
</div>

<div class="nav">
  <button class="active" onclick="showTab('home')"><b>🏠</b>Home</button>
  <button onclick="showTab('earn')"><b>💰</b>Earn</button>
  <button onclick="showTab('invite')"><b>👥</b>Invite</button>
  <button onclick="showTab('withdraw')"><b>💳</b>Withdraw</button>
  <button onclick="showTab('profile')"><b>👤</b>Profile</button>
</div>

<script>
const tg = window.Telegram.WebApp;
tg.ready(); tg.expand();
const initData = tg.initData;

async function api(url, opts={}) {
  opts.headers = Object.assign({}, opts.headers||{}, {'X-Telegram-Init-Data':initData,'Content-Type':'application/json'});
  const r = await fetch(url, opts);
  const j = await r.json();
  if (!r.ok || j.ok===false) throw new Error(j.error||'Request failed');
  return j;
}
function toast(x){ try{tg.showAlert(x)}catch(e){alert(x)} }
function openLink(url){ tg.openLink(url); }
function showTab(id){
  document.querySelectorAll('.section').forEach(x=>x.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));
  const map={home:0,earn:1,invite:2,withdraw:3,profile:4};
  document.querySelectorAll('.nav button')[map[id]].classList.add('active');
  if(id==='earn') loadTasks();
}
async function login(){
  if(!initData){ toast('এই Mini App অবশ্যই Telegram-এর ভিতর থেকে খুলুন।'); return; }
  try{
    await api('/api/login',{method:'POST',body:JSON.stringify({initData})});
    await loadMe(); await loadReferral();
  }catch(e){toast(e.message)}
}
async function loadMe(){
  const j=await api('/api/me'); const u=j.user,s=j.settings;
  document.getElementById('balance').textContent=Number(u.balance).toFixed(2);
  document.getElementById('currency').textContent=s.currency;
  document.getElementById('uid').textContent=u.id;
  document.getElementById('username').textContent=u.username?'@'+u.username:'—';
  document.getElementById('earned').textContent=Number(u.total_earned).toFixed(2);
  document.getElementById('withdrawn').textContent=Number(u.total_withdrawn).toFixed(2);
  document.getElementById('minWithdraw').textContent=s.currency+s.min_withdraw;
  renderWithdrawals(j.withdrawals); renderSupport(j.support);
  if(s.maintenance==='1') document.getElementById('homeNotice').innerHTML='<div class="notice">⚠️ App এখন Maintenance Mode-এ আছে।</div>';
}
async function loadTasks(){
  try{
    const j=await api('/api/tasks'); const box=document.getElementById('tasks'); box.innerHTML='';
    if(!j.tasks.length){box.innerHTML='<div class="card" style="margin-top:12px">এখন কোনো Task নেই।</div>';return}
    j.tasks.forEach(t=>{
      const d=document.createElement('div'); d.className='task';
      d.innerHTML=`<b>${esc(t.title)}</b><div>${esc(t.description||'')}</div><a href="${esc(t.url)}" target="_blank">${esc(t.url)}</a><div class="reward">Reward: ${t.reward}</div>`;
      const b=document.createElement('button'); b.className='btn '+(t.claimed?'secondary':''); b.textContent=t.claimed?'✅ Claimed':'Claim Reward';
      b.disabled=!!t.claimed; b.onclick=async()=>{try{await api('/api/task/'+t.id+'/claim',{method:'POST'});toast('Reward যোগ হয়েছে।');loadMe();loadTasks()}catch(e){toast(e.message)}};
      d.appendChild(b);box.appendChild(d);
    });
  }catch(e){toast(e.message)}
}
async function dailyBonus(){try{const j=await api('/api/daily',{method:'POST'});toast('Daily Bonus +'+j.reward);loadMe()}catch(e){toast(e.message)}}
async function loadReferral(){try{const j=await api('/api/referral');document.getElementById('refLink').value=j.link}catch(e){}}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').value);toast('Referral link copied')}
function shareRef(){const x=document.getElementById('refLink').value;tg.openTelegramLink('https://t.me/share/url?url='+encodeURIComponent(x))}
async function withdraw(){
  try{const j=await api('/api/withdraw',{method:'POST',body:JSON.stringify({method:document.getElementById('method').value,account:document.getElementById('account').value,amount:document.getElementById('amount').value})});toast(j.message);document.getElementById('account').value='';document.getElementById('amount').value='';loadMe()}catch(e){toast(e.message)}
}
function renderWithdrawals(a){document.getElementById('withdrawHistory').innerHTML=a.length?'<hr><b>Recent Withdrawals</b>'+a.map(x=>`<p>#${x.id} — ${x.amount} — ${x.status}</p>`).join(''):' '}
async function sendSupport(){
  try{const m=document.getElementById('supportMsg').value.trim();const j=await api('/api/support',{method:'POST',body:JSON.stringify({message:m})});toast(j.message);document.getElementById('supportMsg').value='';loadMe()}catch(e){toast(e.message)}
}
function renderSupport(a){document.getElementById('supportHistory').innerHTML=a.length?'<hr><b>Previous Messages</b>'+a.map(x=>`<div class="task"><b>You:</b> ${esc(x.message)}<br><b>Admin:</b> ${esc(x.reply||'Pending')}</div>`).join(''):''}
function esc(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
login();
</script>
</body>
</html>
"""

# ---------- HTML: Admin ----------

ADMIN_HTML = r"""
<!doctype html><html lang="bn"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin — {{ settings.app_name }}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
body{font-family:Arial,sans-serif;background:#f3f5f9;margin:0;color:#172033}.wrap{max-width:1100px;margin:auto;padding:18px}
h1{margin:0}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.box,.panel{background:white;border-radius:16px;padding:16px;box-shadow:0 4px 18px #0000000a;margin-bottom:14px}.num{font-size:25px;font-weight:800;margin-top:5px}
.tabs{display:flex;gap:8px;overflow:auto;margin-bottom:14px}.tabs button{padding:10px 13px;border:0;border-radius:11px;background:#e8edf4;white-space:nowrap}.tabs button.active{background:#111827;color:#fff}
.tab{display:none}.tab.active{display:block}.input,.select,.textarea{width:100%;padding:11px;border:1px solid #dce2ea;border-radius:10px;margin:5px 0 9px;box-sizing:border-box}.textarea{min-height:90px}
.btn{border:0;border-radius:10px;padding:10px 13px;background:#111827;color:#fff;font-weight:700}.danger{background:#b91c1c}.ok{background:#166534}.muted{background:#e8edf4;color:#111827}
.table{width:100%;border-collapse:collapse;font-size:13px}.table th,.table td{padding:9px;border-bottom:1px solid #edf0f4;text-align:left;vertical-align:top}.scroll{overflow:auto}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}.wide{grid-column:1/-1}
@media(max-width:700px){.grid{grid-template-columns:1fr 1fr}.row{grid-template-columns:1fr}.wide{grid-column:auto}}
</style></head><body><div class="wrap">
<div class="top"><div><h1>⚙️ Admin Panel</h1><small>{{ settings.app_name }}</small></div><button class="btn" onclick="loginAdmin()">🔐 Verify Admin</button></div>
<div class="grid"><div class="box">Users<div class="num" id="users">0</div></div><div class="box">Active<div class="num" id="active">0</div></div><div class="box">Pending<div class="num" id="pending">0</div></div><div class="box">Balance<div class="num" id="bal">0</div></div></div>
<div class="tabs">
<button class="active" onclick="tab('dashboard',this)">📊 Dashboard</button>
<button onclick="tab('tasks',this)">🧩 Tasks</button>
<button onclick="tab('usersTab',this)">👥 Users</button>
<button onclick="tab('withdrawals',this)">💳 Withdrawals</button>
<button onclick="tab('support',this)">🆘 Support</button>
<button onclick="tab('settings',this)">⚙️ Settings</button>
</div>

<div id="dashboard" class="tab active panel"><h3>Quick Control</h3><p>সব Reward, Link, Task, Withdrawal ও Support এখান থেকে নিয়ন্ত্রণ করা যাবে।</p><button class="btn muted" onclick="refresh()">🔄 Refresh</button></div>

<div id="tasks" class="tab panel">
<h3>🧩 Task Management</h3>
<div class="row">
<div><input id="tt" class="input" placeholder="Task title"></div>
<div><input id="tr" class="input" type="number" placeholder="Reward"></div>
<div class="wide"><input id="tu" class="input" placeholder="Task URL"></div>
<div class="wide"><textarea id="td" class="textarea" placeholder="Description"></textarea></div>
</div><button class="btn ok" onclick="createTask()">➕ Add Task</button>
<div id="taskList" class="scroll" style="margin-top:15px"></div>
</div>

<div id="usersTab" class="tab panel">
<h3>👥 User Management</h3><input id="userSearch" class="input" placeholder="Search ID / username / name" oninput="loadUsers()"><div id="usersList" class="scroll"></div>
</div>

<div id="withdrawals" class="tab panel">
<h3>💳 Withdrawal Management</h3><div id="withdrawList" class="scroll"></div>
</div>

<div id="support" class="tab panel">
<h3>🆘 Support Inbox</h3><div id="supportList" class="scroll"></div>
</div>

<div id="settings" class="tab panel">
<h3>⚙️ All Main Settings</h3>
<div id="settingsForm"></div><button class="btn ok" onclick="saveSettings()">💾 Save All Settings</button>
</div>
</div>
<script>
const tg=window.Telegram.WebApp;tg.ready();tg.expand();const initData=tg.initData;
async function api(u,o={}){o.headers=Object.assign({},o.headers||{},{"X-Telegram-Init-Data":initData,"Content-Type":"application/json"});let r=await fetch(u,o),j=await r.json();if(!r.ok||j.ok===false)throw Error(j.error||'Error');return j}
async function loginAdmin(){try{await api('/admin/session',{method:'POST'});alert('Admin verified');refresh()}catch(e){alert(e.message)}}
function tab(id,b){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('active'));b.classList.add('active');if(id==='tasks')loadTasks();if(id==='usersTab')loadUsers();if(id==='withdrawals')loadWithdrawals();if(id==='support')loadSupport();if(id==='settings')loadSettings()}
async function refresh(){try{let j=await api('/api/admin/stats');users.textContent=j.users;active.textContent=j.active;pending.textContent=j.pending;bal.textContent=Number(j.total_balance).toFixed(2)}catch(e){alert(e.message)}}
async function createTask(){try{await api('/api/admin/tasks',{method:'POST',body:JSON.stringify({title:tt.value,reward:tr.value,url:tu.value,description:td.value})});tt.value=tr.value=tu.value=td.value='';loadTasks()}catch(e){alert(e.message)}}
async function loadTasks(){try{let j=await api('/api/admin/tasks');taskList.innerHTML='<table class="table"><tr><th>ID</th><th>Task</th><th>Reward</th><th>Action</th></tr>'+j.tasks.map(x=>`<tr><td>${x.id}</td><td><b>${esc(x.title)}</b><br>${esc(x.url)}</td><td>${x.reward}</td><td><button class="btn danger" onclick="delTask(${x.id})">Delete</button></td></tr>`).join('')+'</table>'}catch(e){alert(e.message)}}
async function delTask(id){if(!confirm('Delete?'))return;await api('/api/admin/task/'+id,{method:'DELETE'});loadTasks()}
async function loadUsers(){try{let q=encodeURIComponent(userSearch.value);let j=await api('/api/admin/users?q='+q);usersList.innerHTML='<table class="table"><tr><th>User</th><th>Balance</th><th>Earned</th><th>Action</th></tr>'+j.users.map(x=>`<tr><td>${x.id}<br>@${esc(x.username||'')}<br>${esc(x.first_name||'')}</td><td>${x.balance}</td><td>${x.total_earned}</td><td><button class="btn" onclick="addBal(${x.id})">+ Balance</button> <button class="btn ${x.blocked?'ok':'danger'}" onclick="blockUser(${x.id},${x.blocked?0:1})">${x.blocked?'Unblock':'Block'}</button></td></tr>`).join('')+'</table>'}catch(e){alert(e.message)}}
async function addBal(id){let a=prompt('Balance change (+/-):','10');if(a===null)return;await api('/api/admin/user/'+id+'/balance',{method:'POST',body:JSON.stringify({amount:a})});loadUsers();refresh()}
async function blockUser(id,b){await api('/api/admin/user/'+id+'/block',{method:'POST',body:JSON.stringify({blocked:b})});loadUsers()}
async function loadWithdrawals(){let j=await api('/api/admin/withdrawals');withdrawList.innerHTML='<table class="table"><tr><th>#</th><th>User</th><th>Method</th><th>Account</th><th>Amount</th><th>Status</th><th>Action</th></tr>'+j.withdrawals.map(x=>`<tr><td>${x.id}</td><td>${x.user_id}<br>@${esc(x.username||'')}</td><td>${x.method}</td><td>${esc(x.account)}</td><td>${x.amount}</td><td>${x.status}</td><td><button class="btn ok" onclick="wd(${x.id},'approved')">Approve</button> <button class="btn danger" onclick="wd(${x.id},'rejected')">Reject</button></td></tr>`).join('')+'</table>'}
async function wd(id,status){let note=prompt('Note (optional):','');await api('/api/admin/withdrawal/'+id,{method:'POST',body:JSON.stringify({status,note})});loadWithdrawals();refresh()}
async function loadSupport(){let j=await api('/api/admin/support');supportList.innerHTML=j.support.map(x=>`<div class="box"><b>#${x.id} User ${x.user_id} @${esc(x.username||'')}</b><p>${esc(x.message)}</p><p>Reply: ${esc(x.reply||'—')}</p><textarea id="rep${x.id}" class="textarea" placeholder="Reply"></textarea><button class="btn ok" onclick="reply(${x.id})">Send Reply</button></div>`).join('')}
async function reply(id){let r=document.getElementById('rep'+id).value;await api('/api/admin/support/'+id,{method:'POST',body:JSON.stringify({reply:r,status:'answered'})});loadSupport()}
async function loadSettings(){let j=await api('/api/admin/settings');settingsForm.innerHTML=Object.entries(j.settings).map(([k,v])=>`<label><b>${esc(k)}</b><input class="input sk" data-key="${esc(k)}" value="${esc(v)}"></label>`).join('')}
async function saveSettings(){let b={};document.querySelectorAll('.sk').forEach(x=>b[x.dataset.key]=x.value);await api('/api/admin/settings',{method:'POST',body:JSON.stringify(b)});alert('Saved');}
function esc(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
refresh();
</script></body></html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
