import os
import json
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# ==========================================
# ⚠️ এখানে আপনার আসল টেলিগ্রাম আইডি বসান
# ==========================================
ADMIN_ID = 123456789  # <--- আপনার Telegram User ID এখানে দিন

DB_FILE = 'database.json'

# প্রাথমিক ডাটাবেজ সেটআপ (ফাইল না থাকলে অটো তৈরি হবে)
if not os.path.exists(DB_FILE):
    initial_db = {
        "config": {
            "app_name": "প্রতিদিনের কাজ BD",
            "min_withdraw": 1000,
            "refer_reward": 20,
            "daily_bonus": 10,
            "monetag_zone": "11764581",
            "admin_notice": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন।",
            "special_ad_title": "🔥 স্পেশাল অফার - আজকের বোনাস",
            "special_ad_link": "https://example.com"
        },
        "tasks": [
            {"id": "yt", "title": "YouTube Channel Subscribe", "reward": 25, "link": "https://youtube.com"},
            {"id": "tg", "title": "Telegram Channel Join", "reward": 10, "link": "https://t.me"},
            {"id": "fb", "title": "Facebook Page Follow", "reward": 15, "link": "https://facebook.com"},
            {"id": "task1", "title": "Company Task 1 - Website Visit", "reward": 20, "link": "https://google.com"},
            {"id": "task2", "title": "Company Task 2 - Telegram Group", "reward": 20, "link": "https://t.me"},
            {"id": "task3", "title": "Company Task 3 - Post Like", "reward": 20, "link": "https://facebook.com"},
            {"id": "task4", "title": "Company Task 4 - Post Share", "reward": 20, "link": "https://facebook.com"},
            {"id": "task5", "title": "Company Task 5 - Comment Task", "reward": 20, "link": "https://facebook.com"},
            {"id": "task6", "title": "Company Task 6 - Refer 3 Friend", "reward": 20, "link": "https://t.me"}
        ],
        "users": {},
        "withdraws": []
    }
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_db, f, indent=4, ensure_ascii=False)

def load_db():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ------------------------------------------
# API রুটের অংশ (ইউজার ডাটা ও অ্যাকশন হ্যান্ডলিং)
# ------------------------------------------
@app.route('/api/init', methods=['POST'])
def init_user():
    db = load_db()
    req = request.json
    uid = str(req.get('uid', '8801'))
    username = req.get('username', 'User')
    referred_by = req.get('referred_by')

    if uid not in db['users']:
        db['users'][uid] = {
            "uid": uid,
            "username": username,
            "balance": 60,
            "ads_watched": 0,
            "tasks_done": 0,
            "referred_count": 0,
            "daily_claimed": False
        }
        if referred_by and referred_by in db['users'] and referred_by != uid:
            db['users'][referred_by]['balance'] += db['config']['refer_reward']
            db['users'][referred_by]['referred_count'] += 1
        save_db(db)
    
    is_admin = (int(uid) == ADMIN_ID)
    return jsonify({"user": db['users'][uid], "config": db['config'], "tasks": db['tasks'], "is_admin": is_admin})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    db = load_db()
    req = request.json
    uid = str(req.get('uid'))
    amount = int(req.get('amount', 0))
    method = req.get('method')
    number = req.get('number')

    if uid in db['users'] and db['users'][uid]['balance'] >= amount and amount >= db['config']['min_withdraw']:
        db['users'][uid]['balance'] -= amount
        db['withdraws'].append({
            "uid": uid, "username": db['users'][uid]['username'],
            "amount": amount, "method": method, "number": number, "status": "Pending"
        })
        save_db(db)
        return jsonify({"success": True, "balance": db['users'][uid]['balance']})
    return jsonify({"success": False, "message": "ব্যালেন্স কম অথবা নিয়ম ভঙ্গ হয়েছে। "})

@app.route('/api/admin/update_config', methods=['POST'])
def update_config():
    req = request.json
    if int(req.get('admin_id')) != ADMIN_ID: return jsonify({"status": "Unauthorized"}), 403
    db = load_db()
    db['config'].update(req.get('config', {}))
    save_db(db)
    return jsonify({"success": True})

@app.route('/api/admin/data', methods=['POST'])
def admin_data():
    req = request.json
    if int(req.get('admin_id')) != ADMIN_ID: return jsonify({"status": "Unauthorized"}), 403
    db = load_db()
    return jsonify({"users_count": len(db['users']), "withdraws": db['withdraws'], "config": db['config'], "users": db['users']})

@app.route('/api/admin/action_withdraw', methods=['POST'])
def action_withdraw():
    req = request.json
    if int(req.get('admin_id')) != ADMIN_ID: return jsonify({"status": "Unauthorized"}), 403
    db = load_db()
    idx = req.get('index')
    status = req.get('status') # Approved / Rejected
    if idx < len(db['withdraws']):
        db['withdraws'][idx]['status'] = status
        save_db(db)
    return jsonify({"success": True})

# =========================================================================
# FRONTEND HTML & CSS (সম্পূর্ণ ব্লু ডার্ক থিম এবং প্রফেশনাল ইউআই)
# =========================================================================
USER_HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD - Mini App</title>
<script src="https://telegram.org"></script>
<link href="https://googleapis.com" rel="stylesheet">
<style>
* { font-family: 'Hind Siliguri', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0f24; color: #fff; max-width: 430px; margin: 0 auto; padding-bottom: 90px; }
.header { background: #111827; padding: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2937; }
.balance-section { background: linear-gradient(135deg, #1e40af, #1e3a8a); margin: 14px; padding: 20px; border-radius: 18px; text-align: center; box-shadow: 0 4px 15px rgba(30,64,175,0.3); }
.page { display: none; padding: 14px; }
.page.active { display: block; }
.card { background: #111c44; border-radius: 16px; padding: 16px; margin-bottom: 12px; border: 1px solid #1e295d; }
.btn { width: 100%; padding: 14px; border: none; border-radius: 12px; font-weight: 700; font-size: 15px; cursor: pointer; color: #fff; text-align: center; display: inline-block; text-decoration: none; }
.btn-blue { background: #2563eb; }
.btn-red { background: #dc2626; }
.btn-green { background: #059669; }
.input-field { width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #1e295d; background: #0f172a; color: #fff; margin-bottom: 10px; font-size: 15px; }
.btm-nav { position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 430px; background: #0f172a; display: flex; border-top: 1px solid #1e295d; padding: 10px 0; z-index: 100; }
.btm-nav div { flex: 1; text-align: center; color: #64748b; font-size: 12px; font-weight: 700; cursor: pointer; }
.btm-nav div.active { color: #3b82f6; }
.task-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #1e295d; }
</style>
</head>
<body>

<div class="header">
    <div>
        <h3 id="app_name_text">প্রতিদিনের কাজ BD</h3>
        <small style="color: #a1a1aa;">Ads: <span id="hdr_ads">0</span>/100 | Bonus: ৳<span id="hdr_bonus">60</span></small>
    </div>
    <div style="font-size: 24px; font-weight: bold; color: #10b981;">৳<span id="top_bal">60</span></div>
</div>

<div class="balance-section">
    <div style="font-size: 44px; font-weight: 900;">৳<span id="main_bal">60</span></div>
    <div style="color: #93c5fd; font-size: 14px;">আপনার বর্তমান ব্যালেন্স</div>
</div>

<!-- পৃষ্ঠা: হোম -->
<div id="p-home" class="page active">
    <div class="card" style="background: linear-gradient(90deg, #065f46, #0f766e);">
        <h4>📢 অফিসিয়াল নোটিশ</h4>
        <p id="notice_text" style="font-size: 13px; margin-top: 4px; color: #e2e8f0;"></p>
    </div>
    <div class="card">
        <h4 id="sp_title">🔥 স্পেশাল অফার</h4>
        <a id="sp_link" href="#" target="_blank" class="btn btn-blue" style="margin-top:10px;">▶ MINI BOY ADS দেখুন - ৳২ পাবেন</a>
    </div>
</div>

<!-- পৃষ্ঠা: টাস্ক -->
<div id="p-tasks" class="page">
    <div class="card">
        <h4 style="margin-bottom:12px;">📋 আজকের কাজসমূহ</h4>
        <div id="tasks_list"></div>
    </div>
</div>

<!-- পৃষ্ঠা: রেফার -->
<div id="p-refer" class="page">
    <div class="card" style="text-align:center;">
        <h4>🔗 রেফার করে আয় করুন</h4>
        <p style="font-size: 14px; margin: 8px 0; color:#94a3b8;">প্রতিটি সফল রেফারে পাবেন ৳২০ বোনাস!</p>
        <input type="text" id="refer_link_box" class="input-field" readonly>
        <button class="btn btn-blue" onclick="copyRefer()">লিংক কপি করুন</button>
    </div>
</div>

<!-- পৃষ্ঠা: ওয়ালেট/উইথড্র -->
<div id="p-wallet" class="page">
    <div class="card">
        <h4>💳 উইথড্র মেথড</h4>
        <p style="color:#64748b; font-size:13px; margin-bottom:12px;">Minimum: ৳<span id="min_wd_text">1000</span></p>
        <input type="number" id="wd_amount" placeholder="পরিমাণ (Amount)" class="input-field">
        <select id="wd_method" class="input-field">
            <option value="Bkash">بکاش (Bkash)</option>
            <option value="Nagad">নগদ (Nagad)</option>
        </select>
        <input type="text" id="wd_number" placeholder="মোবাইল নম্বর (Account Number)" class="input-field">
        <button class="btn btn-green" onclick="submitWithdraw()">উইথড্র করুন</button>
    </div>
</div>

<!-- পৃষ্ঠা: প্রোফাইল -->
<div id="p-profile" class="page">
