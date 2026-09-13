# -*- coding: utf-8 -*-
# FINAL 600+ LINES - MINI BOY - Wallet Empty Space Fixed
# Token 11764581 - Admin ID 8807178385
# Banner 3 Pic Slider + Wallet Bottom Admin Editable + Live Withdraw Auto
# Full A to Z - Nothing Cut - Everything Included
import os
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template_string
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database.json'

# =========================================================
# DEFAULT DATABASE - 11764581 - 8807178385
# =========================================================
def default_db():
    return {
        "users": {},
        "withdraws": [],
        "settings": {
            "app_name": "প্রতিদিনের কাজ BD - 11764581",
            "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "bkash_logo": "https://download.logo.wine/logo/BKash/bKash-Logo.wine.png",
            "nagad_logo": "https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png",
            "welcome_bonus": 60,
            "ad_reward": 2,
            "ad_limit": 100,
            "min_withdraw": 1000,
            "ref_bonus": 20,
            "official_title": "আফাশিয়াল নোটস - 11764581",
            "official_desc": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন - Token 11764581 - Admin 8807178385",
            "official_live": "LIVE",
            "home_ad_top_title": "🎬 🔥 স্পেশাল অফার - Mini Boy Ads",
            "home_ad_btn": "▶️ ADS দেখুন - Token 11764581",
            "home_ad_zone_text": "Zone: 11764581 - Token 11764581 - Admin 8807178385",
            "home_ad_zone": "11764581",
            "tasks_header": "📋 আজকের 9 টি টাস্ক - 11764581",
            "support_title": "💬 সাপোর্ট সেন্টার - 8807178385",
            "support_desc": "যেকোনো সমস্যায় যোগাযোগ করুন - Telegram: @ProtidinerKajBD - Admin ID 8807178385 - Token 11764581",
            "support_tg": "https://t.me/ProtidinerKajBD",
            "support_channel": "https://t.me/ProtidinerKajBD",
            "support_rules": "📜 নিয়ম: প্রতিদিন ১০০ টা Ad দেখতে হবে - Fake করলে Ban - Admin 8807178385",
            "ref_bottom_title": "📖 কিভাবে রেফার কাজ করে? - 11764581",
            "ref_bottom_desc": "আপনার লিংক শেয়ার করুন - প্রতি রেফারে ৳20 পাবেন - বন্ধু 60 টাকা বোনাস পাবে - Admin 8807178385",
            "banner1": "https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2": "https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3": "https://img.freepik.com/free-vector/earning-money-online-concept-landing-page_52683-25203.jpg",
            "wallet_bottom_title": "💳 Withdraw নিয়ম - Admin থেকে Change করতে পারবেন - 11764581",
            "wallet_bottom_desc": "১. Minimum ৳1000 হলে Withdraw দিতে পারবেন\n২. bKash / Nagad Number সঠিক ভাবে দিন\n৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন\n৪. ভুল Number দিলে টাকা পাবেন না, দায় আপনার\n৫. একাধিক Account করলে Ban হবেন\n\nএই লেখাটি Admin Panel থেকে যেকোনো সময় Change করতে পারবেন - Token 11764581 - Admin ID 8807178385",
            "wallet_rules": "⚠️ সতর্কতা: একাধিক Account করলে Ban হবেন। Fake Refer করলে Balance 0 করে দেওয়া হবে। ভুল Number এ টাকা গেলে Admin দায়ী নয়। - Admin 8807178385 - Token 11764581"
        },
        "tasks": [
            {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "👉 Claim - 25"},
            {"title": "Telegram Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "👉 Claim - 10"},
            {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "👉 Claim - 15"},
            {"title": "Website Visit", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "👉 Claim - 20"},
            {"title": "Group Join", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "👉 Claim - 20"},
            {"title": "Post Like", "reward": 20, "link": "https://t.me", "color": "#be123c", "btn": "👉 Claim - 20"},
            {"title": "Post Share", "reward": 20, "link": "https://t.me", "color": "#065f46", "btn": "👉 Claim - 20"},
            {"title": "Comment", "reward": 20, "link": "https://t.me", "color": "#2563eb", "btn": "👉 Claim - 20"},
            {"title": "Refer 3 Friend", "reward": 20, "link": "https://t.me", "color": "#d97706", "btn": "👉 Claim - 20"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d = default_db()
        save_db(d)
        return d
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        d = json.load(f)
        dd = default_db()
        for k, v in dd["settings"].items():
            if k not in d["settings"]:
                d["settings"][k] = v
        return d

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def get_user(db, uid):
    uid = str(uid)
    today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "balance": db["settings"]["welcome_bonus"],
            "ads_watched": 0,
            "ads_today": 0,
            "last_date": today,
            "claimed": [],
            "ref_count": 0,
            "total_earn": db["settings"]["welcome_bonus"]
        }
    u = db["users"][uid]
    if u.get("last_date")!= today:
        u["ads_today"] = 0
        u["last_date"] = today
    return u

@app.route('/health')
def health():
    return "OK - 11764581 - 8807178385", 200

@app.route('/')
def index():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin():
    if request.args.get('id')!= '8807178385':
        return "Need?id=8807178385 - Admin 8807178385 - Token 11764581", 403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id', '8807178385')
    db = load_db()
    u = get_user(db, uid)
    save_db(db)
    top = sorted(db["users"].values(), key=lambda x: x.get('ref_count', 0), reverse=True)[:5]
    recent = db["withdraws"][-20:][::-1]
    my = [w for w in db["withdraws"] if str(w["uid"]) == str(uid)]
    return jsonify({
        "user": u,
        "settings": db["settings"],
        "tasks": db["tasks"],
        "withdraws": my,
        "top_users": top,
        "recent_withdraws": recent
    })

@app.route('/api/reward')
def reward():
    db = load_db()
    u = get_user(db, request.args.get('id'))
    if u["ads_today"] >= db["settings"]["ad_limit"]:
        return jsonify({"msg": "আজকের লিমিট শেষ! - 11764581"})
    u["balance"] += db["settings"]["ad_reward"]
    u["total_earn"] += db["settings"]["ad_reward"]
    u["ads_watched"] += 1
    u["ads_today"] += 1
    save_db(db)
    return jsonify({"msg": f"৳{db['settings']['ad_reward']} পেয়েছেন! - 11764581"})

@app.route('/api/claim_task')
def claim_task():
    db = load_db()
    idx = int(request.args.get('idx'))
    uid = request.args.get('id')
    u = get_user(db, uid)
    if idx in u["claimed"]:
        return jsonify({"msg": "Already Done - 11764581"})
    u["claimed"].append(idx)
    u["balance"] += db["tasks"][idx]["reward"]
    u["total_earn"] += db["tasks"][idx]["reward"]
    save_db(db)
    return jsonify({"msg": "Task Complete! - 11764581"})

@app.route('/api/withdraw')
def withdraw():
    db = load_db()
    uid = request.args.get('id')
    amt = int(request.args.get('amount', 0))
    num = request.args.get('number')
    method = request.args.get('method', 'bKash')
    u = get_user(db, uid)
    if amt < db["settings"]["min_withdraw"]:
        return jsonify({"msg": f"Min {db['settings']['min_withdraw']} - 11764581"})
    if u["balance"] < amt:
        return jsonify({"msg": "Balance কম - 11764581"})
    u["balance"] -= amt
    db["withdraws"].append({
        "uid": uid,
        "amount": amt,
        "number": num,
        "method": method,
        "time": str(datetime.now())[:19],
        "status": "Pending - 11764581"
    })
    save_db(db)
    return jsonify({"msg": "Withdraw Success! - 11764581 - 8807178385"})

@app.route('/api/admin/full')
def a_full():
    return jsonify(load_db())

@app.route('/api/admin/save_settings', methods=['POST'])
def a_save():
    db = load_db()
    j = request.json
    for k, v in j.items():
        if k in db["settings"]:
            db["settings"][k] = v
        if k == "tasks":
            db["tasks"] = v
    save_db(db)
    return jsonify({"msg": "Saved! 8807178385 - 11764581 - Wallet Box + Banner Saved"})

@app.route('/api/admin/approve')
def a_approve():
    db = load_db()
    idx = int(request.args.get('idx', 0))
    if 0 <= idx < len(db["withdraws"]):
        db["withdraws"].pop(idx)
        save_db(db)
        return jsonify({"msg": "Approved - 11764581"})
    return jsonify({"msg": "Not found"})

# =================================================================
# USER HTML - 11764581 - 8807178385 - FULL
# =================================================================
USER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD 11764581 - 8807178385</title>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}
body{background:#0a1222;color:#fff;max-width:430px;margin:0 auto;padding-bottom:140px}
.top{background:linear-gradient(135deg,#1e3a8a,#0f172a);padding:14px;border-radius:0 0 24px 24px;display:flex;justify-content:space-between;align-items:center}
.bal{color:#22c55e;font-size:42px;font-weight:900}
.card{background:#162032;margin:12px;border-radius:18px;padding:14px;border:1px solid #23344a}
.btn{width:100%;padding:13px;border:none;border-radius:12px;font-weight:700;cursor:pointer;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#121d32;display:flex;border-top:1px solid #23344a;padding:8px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#94a3b8;font-size:12px;cursor:pointer}
.btm div.on{color:#38bdf8}
.inp{width:100%;padding:12px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}
.slider{position:relative;margin:12px;border-radius:18px;overflow:hidden;height:165px;border:1px solid #22314a;background:#000}
.slides{display:flex;transition:transform 0.6s ease;width:300%}
.slide{min-width:100%;height:165px}
.slide img{width:100%;height:165px;object-fit:cover}
.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px}
.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.4)}
.dot.on{background:#38bdf8;width:20px;border-radius:10px}
.badge{position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.6);padding:4px 10px;border-radius:20px;font-size:11px;border:1px solid #38bdf8}
.mcard{flex:1;background:#0f172a;border:2px solid #334155;border-radius:14px;padding:10px;text-align:center;cursor:pointer}
.mcard.sel{border-color:#e2136e}
.spacer{height:70px}
.live-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;animation:blink 1s infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0}100%{opacity:1}}
</style>
</head>
<body>
<div class="top">
<div>
<div>প্রতিদিনের কাজ BD - 11764581 - 8807178385</div>
<div class="bal">৳ <span id="bal">60</span></div>
<div>Ads: <span id="ads">0</span>/100 - 11764581</div>
</div>
<img id="cLogo" src="" style="width:48px;height:48px;border-radius:50%;background:#fff">
</div>

<div id="p-home">
<div class="card" style="background:linear-gradient(90deg,#1e40af,#0f766e);display:flex;justify-content:space-between">
<div><b id="offTitle"></b><br><small id="offDesc"></small></div>
<div style="background:#22c55e;color:#000;padding:10px;border-radius:50%;width:50px;height:50px;display:flex;align-items:center;justify-content:center;font-weight:800" id="offLive">LIVE</div>
</div>

<div class="slider">
<div class="badge">📢 কোম্পানির বিজ্ঞাপন - 11764581</div>
<div class="slides" id="slides">
<div class="slide"><img id="b1" src=""></div>
<div class="slide"><img id="b2" 
