# FINAL COMPLETE A TO Z - BIG ADMIN 8807178385 - TOKEN 11764581 - ONE FILE ONLY - PASTE IN app.py
# MEDIUM 5 BTN 30px icon 15px font 88px height + PROFILE BIG ENGLISH 26px FIXED + 5 NUMBER PAGE CLEAN + ${t.btn} BUG FIXED + 17 COMPANY LINKS + UNLIMITED ADD + JOIN THEN MONEY + 24H TIMER + BIG ADMIN EDITABLE ALL
import os, json, time
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database.json'
BIG_ADMIN_ID = "8807178385"
TOKEN = "11764581"

def default_db():
    return {
        "users": {},
        "withdraws": [],
        "settings": {
            "app_name": f"Protidiner Kaj BD - FINAL - BIG ADMIN {BIG_ADMIN_ID}",
            "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "bkash_logo": "https://download.logo.wine/logo/BKash/bKash-Logo.wine.png",
            "nagad_logo": "https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png",
            "welcome_bonus": 60,
            "ad_reward": 2,
            "ad_limit": 100,
            "min_withdraw": 1000,
            "ref_bonus": 20,
            "task_cooldown_hours": 24,
            "official_title": f"Official Notes - {TOKEN} - BIG ADMIN {BIG_ADMIN_ID}",
            "official_desc": f"Daily Ads and Tasks - Token {TOKEN} - Big Admin {BIG_ADMIN_ID} - FINAL",
            "official_live": "LIVE",
            "home_ad_top_title": f"Special Offer - Mini Boy Ads - BIG ADMIN {BIG_ADMIN_ID} FINAL",
            "home_ad_btn": f"Watch ADS - Token {TOKEN} - Claim 2 Tk - FINAL",
            "support_title": f"Support Center - {BIG_ADMIN_ID} - BIG ADMIN",
            "support_desc": f"Contact us\nTelegram: @ProtidinerKajBD\nBig Admin ID: {BIG_ADMIN_ID}\nToken: {TOKEN}\nFINAL BIG ADMIN FILE - A TO Z",
            "support_tg": "https://t.me/ProtidinerKajBD",
            "support_channel": "https://t.me/ProtidinerKajBD",
            "support_rules": f"Rules: 100 Ads daily - Fake Ban - Big Admin {BIG_ADMIN_ID}",
            "ref_bottom_title": f"How Refer Works? - BIG ADMIN {BIG_ADMIN_ID}",
            "ref_bottom_desc": f"1. Share link\n2. Friend join\n3. Get 20 Tk\n4. Instant balance\nBig Admin: {BIG_ADMIN_ID}",
            "banner1": "https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2": "https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3": "https://img.freepik.com/free-vector/earning-money-online-concept-landing-page_52683-25203.jpg",
            "wallet_bottom_title": "Withdraw Rules - Big Admin Can Change All - FINAL A TO Z",
            "wallet_bottom_desc": "1. Min 1000 Tk\n2. Correct bKash/Nagad Number\n3. Payment in 24h\n4. Wrong number your responsibility\n5. Multi account = Ban\nBig Admin Editable - FINAL",
            "wallet_rules": f"Fake Account = Ban - Big Admin {BIG_ADMIN_ID} - Token {TOKEN} - FINAL A TO Z"
        },
        "tasks": [
            {"title": "YouTube Subscribe - Company Link 1", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "Join & Get 25 Tk"},
            {"title": "Telegram Join - Company Link 2", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join & Get 10 Tk"},
            {"title": "Facebook Follow - Company Link 3", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "Join & Get 15 Tk"},
            {"title": "Website Visit - Company Link 4", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "Visit & Get 20 Tk"},
            {"title": "Group Join - Company Link 5", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "Join & Get 20 Tk"},
            {"title": "Post Like - Company Link 6", "reward": 20, "link": "https://t.me", "color": "#be123c", "btn": "Like & Get 20 Tk"},
            {"title": "Post Share - Company Link 7", "reward": 20, "link": "https://t.me", "color": "#065f46", "btn": "Share & Get 20 Tk"},
            {"title": "Comment Task - Company Link 8", "reward": 20, "link": "https://t.me", "color": "#2563eb", "btn": "Comment & Get 20 Tk"},
            {"title": "Refer 3 Friend - Company Link 9", "reward": 20, "link": "https://t.me", "color": "#d97706", "btn": "Refer & Get 20 Tk"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d = default_db()
        save_db(d)
        return d
    with open(DB_FILE,'r',encoding='utf-8') as f:
        try:
            d = json.load(f)
        except:
            d = default_db()
            save_db(d)
            return d
    dd = default_db()
    for k,v in dd["settings"].items():
        if k not in d["settings"]:
            d["settings"][k] = v
    if "tasks" not in d:
        d["tasks"] = dd["tasks"]
    return d

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f:
        json.dump(d,f,indent=2,ensure_ascii=False)

def get_user(db,uid):
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
            "task_times": {},
            "ref_count": 0,
            "total_earn": db["settings"]["welcome_bonus"],
            "is_big_admin": uid == BIG_ADMIN_ID
        }
    u = db["users"][uid]
    if u.get("last_date")!= today:
        u["ads_today"] = 0
        u["last_date"] = today
    if "task_times" not in u: u["task_times"] = {}
    if "claimed" not in u: u["claimed"] = []
    if "total_earn" not in u: u["total_earn"] = u["balance"]
    u["is_big_admin"] = uid == BIG_ADMIN_ID
    return u

@app.route('/health')
def health():
    return f"OK - BIG ADMIN FINAL A TO Z - ID {BIG_ADMIN_ID} - TOKEN {TOKEN} - MEDIUM 5 BTN + PROFILE BIG ENGLISH FIXED - ALL SYSTEM INSIDE",200

@app.route('/')
def index():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin():
    if request.args.get('id')!= BIG_ADMIN_ID:
        return f"Need?id={BIG_ADMIN_ID} - BIG ADMIN ONLY - TOKEN {TOKEN}",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id', BIG_ADMIN_ID)
    db = load_db()
    u = get_user(db, uid)
    save_db(db)
    return jsonify({
        "user": u,
        "settings": db["settings"],
        "tasks": db["tasks"],
        "withdraws": [w for w in db["withdraws"] if str(w["uid"]) == str(uid)],
        "recent_withdraws": db["withdraws"][-20:][::-1],
        "big_admin_id": BIG_ADMIN_ID,
        "token": TOKEN
    })

@app.route('/api/reward')
def reward():
    db = load_db()
    u = get_user(db, request.args.get('id'))
    u["balance"] += db["settings"]["ad_reward"]
    u["ads_watched"] += 1
    u["ads_today"] += 1
    u["total_earn"] += db["settings"]["ad_reward"]
    save_db(db)
    return jsonify({"msg": f"৳{db['settings']['ad_reward']} Added - BIG ADMIN {BIG_ADMIN_ID} - FINAL A TO Z"})

@app.route('/api/claim_task')
def claim_task():
    db = load_db()
    idx = int(request.args.get('idx'))
    uid = request.args.get('id')
    u = get_user(db, uid)
    now = time.time()
    last = float(u["task_times"].get(str(idx),0))
    cooldown = int(db["settings"].get("task_cooldown_hours",24)) * 3600
    if last!= 0 and (now - last) < cooldown:
        remain_h = int((cooldown - (now - last)) / 3600)
        remain_m = int(((cooldown - (now - last)) % 3600) / 60)
        return jsonify({"msg": f"⏰ Already Joined - {remain_h}h {remain_m}m পর আবার Join করতে পারবে - BIG ADMIN {BIG_ADMIN_ID} - TIMER {db['settings']['task_cooldown_hours']}h"})
    u["task_times"][str(idx)] = now
    if idx not in u["claimed"]:
        u["claimed"].append(idx)
    u["balance"] += db["tasks"][idx]["reward"]
    u["total_earn"] += db["tasks"][idx]["reward"]
    save_db(db)
    return jsonify({"msg": f"✅ Joined Success - ৳{db['tasks'][idx]['reward']} Added - Next {db['settings']['task_cooldown_hours']}h later - BIG ADMIN {BIG_ADMIN_ID}"})

@app.route('/api/withdraw')
def withdraw():
    db = load_db()
    uid = request.args.get('id')
    amt = int(request.args.get('amount',0))
    num = request.args.get('number')
    method = request.args.get('method','bKash')
    u = get_user(db, uid)
    if amt < db["settings"]["min_withdraw"]:
        return jsonify({"msg": f"Min {db['settings']['min_withdraw']} Tk - BIG ADMIN {BIG_ADMIN_ID}"})
    if u["balance"] < amt:
        return jsonify({"msg": "Low Balance - BIG ADMIN"})
    u["balance"] -= amt
    db["withdraws"].append({"uid": uid, "amount": amt, "number": num, "method": method, "time": str(datetime.now())[:19], "status": "Pending"})
    save_db(db)
    return jsonify({"msg": f"Withdraw Request Success - BIG ADMIN {BIG_ADMIN_ID} - TOKEN {TOKEN}"})

@app.route('/api/admin/full')
def a_full():
    return jsonify(load_db())

@app.route('/api/admin/save_settings',methods=['POST'])
def a_save():
    db = load_db()
    j = request.json
    for k,v in j.get("settings",{}).items():
        if k in db["settings"]:
            if k == "task_cooldown_hours":
                try: db["settings"][k] = int(v)
                except: db["settings"][k] = 24
            else:
                db["settings"][k] = v
    if "tasks" in j and isinstance(j["tasks"], list):
        db["tasks"] = j["tasks"]
    save_db(db)
    return jsonify({"msg": f"Saved - BIG ADMIN {BIG_ADMIN_ID} FINAL A TO Z - MEDIUM 5 BTN (30px icon,15px font,88px height) + PROFILE BIG ENGLISH 26px FIXED + 5 NUMBER PAGE CLEAN + ${{t.btn}} FIXED + 17 COMPANY LINKS + UNLIMITED ADD BUTTON SYSTEM + JOIN THEN MONEY + {db['settings']['task_cooldown_hours']}h TIMER - ALL INSIDE - TOKEN {TOKEN}"})

@app.route('/api/admin/approve')
def a_approve():
    db = load_db()
    idx = int(request.args.get('idx',0))
    if 0 <= idx < len(db["withdraws"]):
        db["withdraws"].pop(idx)
        save_db(db)
    return jsonify({"msg": f"Approved - BIG ADMIN {BIG_ADMIN_ID}"})

USER_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>BIG ADMIN FINAL A TO Z - 8807178385</title><script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script><style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#0a1222;color:#fff;max-width:430px;margin:0 auto;padding-bottom:180px}.top{background:linear-gradient(135deg,#1e3a8a,#0f172a);padding:16px;border-radius:0 0 24px 24px;display:flex;justify-content:space-between;align-items:center}.bal{color:#22c55e;font-size:44px;font-weight:900}.card{background:#162032;margin:12px;border-radius:18px;padding:16px;border:1px solid #22314a}.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;font-size:15px;cursor:pointer}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f1b33;display:flex;border-top:2px solid #1e3a5f;padding:8px 0 14px 0;z-index:99;height:88px}.btm div{flex:1;text-align:center;color:#7a8aa8;font-size:15px;padding:10px 3px;border-radius:12px;font-weight:700;cursor:pointer}.btm div.on{color:#38bdf8;background:rgba(56,189,248,0.15);transform:scale(1.08)}.btm div span.icon{font-size:30px;display:block;margin-bottom:4px}.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}.slider{position:relative;margin:12px;border-radius:18px;overflow:hidden;height:170px;border:1px solid #22314a;background:#000}.slides{display:flex;transition:transform 0.6s;width:300%}.slide{min-width:100%;height:170px}.slide img{width:100%;height:170px;object-fit:cover}.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px}.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.4)}.dot.on{background:#38bdf8;width:20px;border-radius:10px}.mcard{flex:1;background:#0f172a;border:2px solid #334155;border-radius:14px;padding:12px;text-align:center;cursor:pointer}.mcard.sel{border-color:#e2136e;background:rgba(226,19,110,0.1)}.spacer{height:100px}.profile-header{background:linear-gradient(135deg,#1e3a8a,#0f172a);margin:12px;border-radius:20px;padding:26px;text-align:center;border:2px solid #2a3f63}.profile-a
