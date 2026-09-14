import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

def load_db():
    if not os.path.exists(DB):
        d = {
            "users": {},
            "withdraws": [],
            "settings": {
                "app_name": "Protidiner Kaj BD",
                "admin_name": "SHIBLI NOMAN",
                "app_logo": "👑",
                "slider1": "🎉 Daily Bonus Available Today",
                "slider2": "📢 Company Sponsored - 100% Safe",
                "slider3": "🎁 50 Ads দেখলে ৳100 বোনাস!",
                "slider4": "💰 100% Payment Guaranteed",
                "slider5": "🔥 প্রতিদিন কাজ করুন",
                "company_reward": 2,
                "popup_reward": 3,
                "company_limit": 30,
                "popup_limit": 20,
                "balance_target": 2000,
                "min_withdraw": 500,
                "tele_link": "https://t.me/",
                "yt_link": "https://youtube.com/",
                "fb_link": "https://facebook.com/"
            }
        }
        with open(DB, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        return d
    with open(DB, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def get_user(db, uid):
    uid = str(uid)
    today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "name": "User 8385",
            "balance": 1120,
            "company": 0,
            "popup": 0,
            "total": 0,
            "tasks": [],
            "img": "",
            "join": "2026-09-13",
            "last": today
        }
    return db["users"][uid]

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/admin')
def admin_panel():
    if request.args.get('id')!= '8807178385':
        return "Use /admin?id=8807178385", 403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get')
def api_get():
    db = load_db()
    uid = request.args.get('id', '8807178385')
    u = get_user(db, uid)
    save_db(db)
    uw = [w for w in db["withdraws"] if w["uid"] == uid]
    return jsonify({"user": u, "settings": db["settings"], "withdraws": uw})

@app.route('/api/admin/get')
def admin_get():
    return jsonify(load_db())

@app.route('/api/admin/save', methods=['POST'])
def admin_save():
    db = load_db()
    db["settings"].update(request.json.get('settings', {}))
    save_db(db)
    return jsonify({"msg": "✅ Save হয়েছে"})

@app.route('/api/admin/balance', methods=['POST'])
def admin_bal():
    db = load_db()
    j = request.json
    uid = str(j.get('uid'))
    amt = int(j.get('amt', 0))
    if uid in db["users"]:
        db["users"][uid]["balance"] += amt
        save_db(db)
        return jsonify({"msg": f"✅ ৳{amt} Done"})
    return jsonify({"msg": "User নাই"})

@app.route('/api/reward')
def reward():
    db = load_db()
    uid = request.args.get('id')
    t = request.args.get('type')
    u = get_user(db, uid)
    s = db["settings"]
    if t == 'company':
        if u["company"] >= int(s["company_limit"]):
            return jsonify({"msg": "Limit"})
        u["company"] += 1
        u["balance"] += int(s["company_reward"])
    else:
        if u["popup"] >= int(s["popup_limit"]):
            return jsonify({"msg": "Limit"})
        u["popup"] += 1
        u["balance"] += int(s["popup_reward"])
    u["total"] = u["company"] + u["popup"]
    save_db(db)
    return jsonify({"ok": 1})

@app.route('/api/task/done', methods=['POST'])
def task_done():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    tid = str(j.get('tid'))
    amt = int(j.get('amt', 20))
    if tid not in u["tasks"]:
        u["tasks"].append(tid)
        u["balance"] += amt
    save_db(db)
    return jsonify({"msg": f"✅ ৳{amt} Bonus যোগ হয়েছে"})

@app.route('/api/withdraw', methods=['POST'])
def wd():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    amt = int(j.get('amt', 0))
    if amt < int(db["settings"]["min_withdraw"]):
        return jsonify({"msg": f"❌ মিনিমাম ৳{db['settings']['min_withdraw']}"})
    if u["balance"] < amt:
        return jsonify({"msg": "❌ ব্যালেন্স কম"})
    u["balance"] -= amt
    db["withdraws"].append({"uid": u["id"], "amt": amt, "num": j.get('num'), "method": j.get('method'), "status": "Pending", "time": str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg": "✅ Withdraw পাঠানো হয়েছে"})

@app.route('/api/profile/save', methods=['POST'])
def ps():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    u["name"] = j.get('name', u["name"])
    if j.get('img'):
        u["img"] = j.get('img')
    save_db(db)
    return jsonify({"msg": "✅ Profile Save হয়েছে"})

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>
body{background:#070710;color:#fff;max-width:900px;margin:0 auto;padding:12px;font-family:system-ui}
.card{background:#15152a;border-radius:16px;padding:16px;margin:12px 0;border:1px solid #222}
input{width:100%;padding:12px;border-radius:10px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:6px}
label{font-size:11px;color:#aaa;margin-top:10px;display:block}
.btn{width:100%;padding:14px;background:#6d4cff;border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:14px}
</style></head><body>
<h2 style="text-align:center">👑 Admin - Full Control - Protidiner Kaj BD</h2>
<div class="card">
<h3>🎨 A to Z Control</h3>
<label>App Name</label><input id="app_name">
<label>Admin Name</label><input id="admin_name">
<label>Slider 1 (কমলা ব্যানার)</label><input id="slider1">
<label>Slider 2</label><input id="slider2">
<label>Slider 3</label><input id="slider3">
<label>Slider 4</label><input id="slider4">
<label>Slider 5</label><input id="slider5">
<label>Company Reward ৳</label><input id="company_reward" type="number">
<label>Popup Reward ৳</label><input id="popup_reward" type="number">
<label>Company Limit</label><input id="company_limit" type="number">
<label>Popup Limit</label><input id="popup_limit" type="number">
<label>Balance Target (লাল বার কততে 100% ভরবে)</label><input id="balance_target" type="number">
<label>Min Withdraw</label><input id="min_withdraw" type="number">
<button class="btn" onclick="saveAll()">💾 SAVE EVERYTHING</button>
</div>
<div class="card"><h3>💰 টাকা বাড়ানো/কমানো</h3><label>User ID</label><input id="uid"><label>Amount (+100 বা -50)</label><input id="amt" type="number"><button class="btn" onclick="addBal()">Update Balance</button></div>
<script>
function load(){fetch('/api/admin/get').then(r=>r.json()).then(d=>{for(let k in d.settings){let e=document.getElementById(k);if(e)e.value=d.settings[k];}});}
function saveAll(){let s={};document.querySelectorAll('input').forEach(e=>{if(e.id!='uid'&&e.id!='amt')s[e.id]=e.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:s})}).then(r=>r.json()).then(d=>alert(d.msg));}
function addBal(){fetch('/api/admin/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uid:document.getElementById('uid').value,amt:document.getElementById('amt').value})}).then(r=>r.json()).then(d=>alert(d.msg));}
load();
</script></body></html>
"""

HTML = """<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#000;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.header{background:#0a0a18;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bottomNav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;justify-content:space-around;padding:10px 0 14px;border-radius:24px 24px 0 0;z-index:99;border-top:1px solid #1e1e3a}
.navItem{text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.navItem.active{color:#fff}.navItem span{font-size:24px;display:block}
.page{display:none}.page.active{display:block}
.sliderWrap{margin:8px 12px 0 12px}.slider{height:145px;border-radius:24px;background:linear-gradient(90deg,#ff9a00,#ff5500);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;transition:.8s;font-size:20px;font-weight:700;text-align:center;padding:10px}.slide.active{opacity:1}
.dotWrap{display:flex;gap:6px;justify-content:center;margin:6px 0 0 0}.dot{width:6px;height:6px;background:#fff4;border-radius:50%}.dot.active{background:#fff;width:20px}
.balanceCard{background:linear-gradient(135deg,#1e3a8a,#2563eb,#06b6d4);border-radius:24px;padding:18px 16px 14px 16px;text-align:center;margin:10px 12px 10px 12px;border:1px solid #2a5bff}
.pill{background:#00000035;padding:7px 14px;border-radius:20px;font-size:13px;font-weight:600;border:1px solid #ffffff15}
.longBar{width:100%;height:6px;background:#00000040;border-radius:10px;margin-top:14px;overflow:hidden}.longBarFill{height:100%;background:linear-gradient(90deg,#ff0000,#ff3333);border-radius:10px;width:0%;transition:1s}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:800;color:#fff;margin:6px 0;cursor:pointer}
.btn-purple{background:#6d28d9}.btn-green{background:#16a34a}.btn-dark{background:#232336}
.taskContainer{background:#0f0f1f;border-radius:24px;padding:12px;margin:12px;border:1px solid #1e1e2e}
.taskRow{display:flex;align-items:center;justify-content:space-between;background:#17172a;border:1px solid #22223a;border-radius:16px;padding:12px 14px;margin:10px 0}
.referBox{background:linear-gradient(135deg,#6d28d9,#7c3aed);border-radius:20px;padding:16px;margin:12px}
.referLinkBox{background:#2a1a6a;border-radius:12px;padding:10px;font-size:12px;word-break:break-all;color:#c4b5fd;margin-top:10px}
.teleBox{background:linear-gradient(90deg,#0ea5e9,#0284c7);border-radius:20px;padding:16px;margin:12px;display:flex;justify-content:space-between;align-items:center}
.rulesBox{background:#151528;border-radius:20px;padding:16px;margin:12px;border:1px solid #222}
.walletBalanceCard{background:linear-gradient(135deg,#1e293b,#2d3a4f);border-radius:24px;padding:24px;text-align:center;margin:12px;border:1px solid #1e293b}
.withdrawBox{background:#131326;border-radius:24px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.methodCard{display:flex;align-items:center;gap:12px;background:#1a1a30;border:2px solid #25253d;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.methodCard.active{border-color:#e2136e;background:#201530}
.inputField{width:100%;background:#0e0e20;border:1px solid #25253d;border-radius:14px;padding:14px;color:#fff;margin:8px 0;font-size:14px}
.withdrawBtn{width:100%;background:linear-gradient(90deg,#e2136e,#ff8c00);border:none;border-radius:14px;padding:16px;font-weight:900;color:#fff;font-size:16px;margin-top:12px;cursor:pointer}
.supportTopBox{background:linear-gradient(135deg,#6d28d9,#4f46e5);border-radius:24px;padding:20px;margin:12px;text-align:center}
.contactBox{background:#131326;border-radius:20px;padding:14px;margin:12px;border:1px solid #1e1e3a}
.contactRow{display:flex;align-items:center;gap:12px;background:#1a1a30;border:1.5px solid #25253d;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.faqBox{background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.trustedBox{background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px;text-align:center}
.profileTopCard{background:linear-gradient(180deg,#162040,#0f172a);border-radius:24px;padding:20px;margin:12px;border:1px solid #1e293b;text-align:center}
.avatarWrap{width:120px;height:120px;border-radius:50%;margin:0 auto;position:relative;border:3px solid #6d4cff;display:flex;align-items:center;justify-content:center;background:#0f172a;overflow:hidden;cursor:pointer}
.statsBox{background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.statsGrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px}
.statCard{background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;text-align:center}
</style></head><body>
<div class="header"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:900">Protidiner Kaj BD <span style="background:#22c55e;padding:2px 6px;border-radius:50%;font-size:10px">✓</span></div><div style="font-size:11px;color:#9ca3af">Admin: SHIBLI NOMAN</div></div></div><div style="width:42px;height:42px;border-radius:50%;background:#1e1e3a;border:2px solid #6d4cff;display:flex;align-items:center;justify-content:center" onclick="goP('profile')">👤</div></div>

<!-- 1 HOME - YOUR SCREENSHOT EXACT -->
<div id="p-home" class="page active">
<div class="sliderWrap"><div class="slider"><div id="s1" class="slide active"><span id="st1">Daily Bonus Available Today</span></div><div id="s2" class="slide"><span id="st2">Company Sponsored - 100% Safe</span></div><div id="s3" class="slide"><span id="st3">50 Ads দেখলে ৳100 বোনাস!</span></div><div id="s4" class="slide"><span id="st4">100% Payment Guaranteed</span></div><div id="s5" class="slide"><span id="st5">প্রতিদিন কাজ করুন</span></div></div><div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div></div>

<div class="balanceCard">
<div style="font-size:14px;color:#e0f2fe">💰 আপনার বর্তমান ব্যালেন্স</div>
<div style="font-size:54px;font-weight:900;margin:6px 0" id="balHome">৳1120</div>
<div style="display:flex;gap:8px;justify-content:center;margin-top:10px"><span class="pill" id="bC">Company 0/30</span><span class="pill" id="bP">Popup 0/20</span><span class="pill" id="bT">Total 0</span></div>
<div class="longBar"><div id="progBar" class="longBarFill"></div></div>
</div>

<div style="background:#0f0f1f;border-radius:24px;padding:12px;margin:0 12px 12px 12px;border:1px solid #1e1e2e"><button class="btn btn-purple" onclick="doR('company')">📺 COMPANY ADS (৳<span id="cr">2</span>) - <span id="btnC">0/30</span></button><button class="btn btn-green" onclick="doR('popup')">💰 POPUP ADS (৳<span id="pr">3</span>) - <span id="btnP">0/20</span></button><button class="btn btn-dark" onclick="goP('tasks')">📋 TASK BONUS - 5 টা/দিন</button></div>

<div style="border:1.5px solid #f59e0b;border-radius:18px;padding:14px;margin:12px;background:#12121e"><div style="font-weight:800">🎉 আজকের স্পেশাল অফার</div><div style="font-size:13px;color:#9ca3af;margin-top:4px">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</div></div>
</div>

<!-- 2 TASK -->
<div id="p-tasks" class="page">
<div class="taskContainer"><div style="font-size:20px;font-weight:900;margin-bottom:12px">📋 Task Bonus - দিনে 5 টা</div>
<div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;border-radius:12px;background:#0ea5e922;display:flex;align-items:center;justify-content:center">✈️</div><div><b>Telegram Channel Join</b><div style="font-size:12px;color:#9ca3af">৳25</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('tele',25)">৳25</button></div>
<div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;border-radius:12px;background:#f59e0b22;display:flex;align-items:center;justify-content:center">▶️</div><div><b>YouTube Subscribe</b><div style="font-size:12px;color:#9ca3af">৳30</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('yt',30)">৳30</button></div>
<div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;border-radius:12px;background:#22c55e22;display:flex;align-items:center;justify-content:center">👍</div><div><b>Facebook Page Like</b><div style="font-size:12px;color:#9ca3af">৳20</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('fb',20)">৳20</button></div>
<div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;border-radius:12px;background:#fff1;display:flex;align-items:center;justify-content:center">👥</div><div><b>Refer Friend</b><div style="font-size:12px;color:#9ca3af">৳50</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="goP('profile')">৳50</button></div>
<div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;border-radius:12px;background:#22c55e22;display:flex;align-items:center;justify-content:center">✅</div><div><b>Daily Check-in</b><div style="font-size:12px;color:#9ca3af">৳15</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('check',15)">৳15</button></div>
</div>
<div class="referBox"><div style="font-size:18px;font-weight:900">🎁 Refer & Earn ৳50</div><div class="referLinkBox" id="refLinkT">https://...</div><button style="background:#fff;color:#4c1d95;border:none;width:100%;padding:12px;border-radius:12px;font-weight:900;margin-top:12px" onclick="copyRefer()">📋 লিংক কপি</button></div>
<div class="teleBox"><div><div style="font-size:18px;font-weight:900">📢 Telegram Channel</div><div style="font-size:12px;opacity:.8">আপডেট ও প্রুফ</div></div><button style="background:#fff;color:#0ea5e9;border:none;padding:10px 18px;border-radius:20px;font-weight:800" onclick="window.open('https://t.me/','_blank')">Join ✈️</button></div>
<div class="rulesBox"><div style="font-size:18px;font-weight:900">⚠️ Task নিয়ম</div><div style="margin-top:10px;font-size:13px;color:#9ca3af;line-height:1.8">- প্রতিদিন 5 টা Task<br>- লিংকে গিয়ে জয়েন করুন<br>- Verify করলে টাকা যোগ</div></div>
</div>

<!-- 3 WALLET -->
<div id="p-wallet" class="page">
<div class="walletBalanceCard"><div style="font-size:13px;color:#94a3b8">ব্যালেন্স</div><div style="font-size:56px;font-weight:900" id="wBal">৳1120</div><div style="font-size:13px;color:#94a3b8">Min ৳500</div></div>
<div class="withdrawBox"><div style="font-size:18px;font-weight:900;margin-bottom:12px">💸 Withdraw Method</div>
<div class="methodCard active"><div style="width:52px;height:52px;background:#e2136e;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900">৳</div><div><b>bKash</b><div style="font-size:12px;color:#9ca3af">Personal • Instant</div></div><div style="margin-left:auto;color:#22c55e">✓</div></div>
<div class="methodCard"><div style="width:52px;height:52px;background:#ff8c00;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900">৳</div><div><b>Nagad</b><div style="font-size:12px;color:#9ca3af">Personal • Fast</div></div></div>
<input id="accNum" class="inputField" placeholder="01XXXXXXXXXX"><input id="wdAmt" class="inputField" type="number" placeholder="500"><button class="withdrawBtn" onclick="doWd()">🚀 Withdraw করুন</button></div>
<div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:16px;margin:12px"><div style="font-size:18px;font-weight:900">✅ Withdraw নিয়ম</div><div style="margin-top:10px;font-size:14px;line-height:1.9">- মিনিমাম ৳500<br>- Personal নাম্বার দিন<br>- 24 ঘণ্টায় পেমেন্ট</div></div>
</div>

<!-- 4 SUPPORT -->
<div id="p-support" class="page">
<div class="supportTopBox"><div style="font-size:22px;font-weight:900">আমরা আছি আপনার পাশে</div><div style="font-size:13px;margin-top:6px;opacity:.85">২৪ ঘণ্টা সাপোর্ট • 100% Trusted</div></div>
<div class="contactBox"><div class="contactRow" onclick="window.open('https://t.me/','_blank')"><div style="width:52px;height:52px;border-radius:14px;background:#0ea5e9;display:flex;align-items:center;justify-content:center">✈️</div><div><div style="font-weight:700">Telegram Support</div><div style="font-size:12px;color:#9ca3af">2 মিনিটে রিপ্লাই</div></div><div style="margin-left:auto">➡️</div></div>
<div class="contactRow"><div style="width:52px;height:52px;border-radius:14px;background:#22c55e;display:flex;align-items:center;justify-content:center">💬</div><div><div style="font-weight:700">WhatsApp Support</div><div style="font-size:12px;color:#9ca3af">01XXXXXXXXXX</div></div><div style="margin-left:auto">➡️</div></div></div>
<div class="faqBox"><div style="font-size:20px;font-weight:900;margin-bottom:12px">❓ FAQ</div><div style="background:#1a1a30;border-radius:14px;padding:14px;margin:10px 0"><b>Q: টাকা কখন পাবো?</b><div style="font-size:13px;color:#9ca3af">A: 24 ঘণ্টার মধ্যে।</div></div><div style="background:#1a1a30;border-radius:14px;padding:14px;margin:10px 0"><b>Q: VPN চলবে?</b><div style="font-size:13px;color:#9ca3af">A: না।</div></div></div>
<div class="trustedBox"><div style="font-size:20px;font-weight:900">🛡️ 100% Trusted</div><div style="font-size:13px;margin-top:6px;opacity:.9">50k+ ইউজার, 100% পেমেন্ট গ্যারান্টি।</div></div>
</div>

<!-- 5 PROFILE -->
<div id="p-profile" class="page">
<div class="profileTopCard"><div class="avatarWrap"><div style="font-size:60px">👤</div></div><div style="margin-top:14px;font-size:20px;font-weight:800" id="pNameTop">User 8385</div><div style="font-size:12px;color:#9ca3af">ID: 8807178385</div><div style="background:#6d4cff;color:#fff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:700;display:inline-block;margin-top:8px">🏅 Bronze Member</div></div>
<div class="statsBox"><div style="font-size:18px;font-weight:900">📊 পরিসংখ্যান</div><div class="statsGrid"><div class="statCard"><div>💰</div><div style="font-size:18px;font-weight:900" id="sBal">৳1120</div><div style="font-size:11px;color:#9ca3af">ব্যালেন্স</div></div><div class="statCard"><div>📺</div><div style="font-size:18px;font-weight:900" id="sAds">0</div><div style="font-size:11px;color:#9ca3af">Ads</div></div><div class="statCard"><div>📋</div><div style="font-size:18px;font-weight:900" id="sTask">0</div><div style="font-size:11px;color:#9ca3af">Task</div></div></div></div>
<div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px;text-align:center"><div style="font-size:20px;font-weight:900">🛡️ Verified User</div><div style="font-size:13px;margin-top:4px;opacity:.9">আপনার একাউন্ট 100% Safe</div></div>
</div>

<div class="bottomNav"><div class="navItem active" id="n-home" onclick="goP('home')"><span>🏠</span>Home</div><div class="navItem" id="n-tasks" onclick="goP('tasks')"><span>📋</span>Task</div><div class="navItem" id="n-wallet" onclick="goP('wallet')"><span>💰</span>Wallet</div><div class="navItem" id="n-support" onclick="goP('support')"><span>💬</span>Support</div><div class="navItem" id="n-profile" onclick="goP('profile')"><span>👤</span>Profile</div></div>

<script>
let uid='8807178385',cur=0;
function goP(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.navItem').forEach(e=>e.classList.remove('active'));document.getElementById('n-'+p).classList.add('active');}
function init(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{let u=d.user;let s=d.settings;for(let i=1;i<=5;i++){let el=document.getElementById('st'+i);if(el)el.innerText=s['slider'+i]||'';}document.getElementById('balHome').innerText='৳'+u.balance;document.getElementById('wBal').innerText='৳'+u.balance;document.getElementById('bC').innerText='Company '+u.company+'/'+s.company_limit;document.getElementById('bP').innerText='Popup '+u.popup+'/'+s.popup_limit;document.getElementById('bT').innerText='Total '+u.total;document.getElementById('btnC').innerText=u.company+'/'+s.company_limit;document.getElementById('btnP').innerText=u.popup+'/'+s.popup_limit;document.getElementById('cr').innerText=s.company_reward;document.getElementById('pr').innerText=s.popup_reward;document.getElementById('sBal').innerText='৳'+u.balance;document.getElementById('sAds').innerText=u.total;document.getElementById('pNameTop').innerText=u.name;let pct=Math.min(100,Math.round((u.balance/parseInt(s.balance_target||2000))*100));document.getElementById('progBar').style.width=pct+'%';document.getElementById('refLinkT').innerText='https://telegram-bot-1-v77g.onrender.com/?ref='+u.id;});}
function doR(t){fetch('/api/reward?id='+uid+'&type='+t).then(()=>{init();if(typeof show_11764581==='function')show_11764581();});}
function doTask(id,amt){fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function doWd(){let num=document.getElementById('accNum').value;let amt=document.getElementById('wdAmt').value;if(!num||!amt){alert('নাম্বার ও টাকা দিন');return;}fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:'bKash'})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function copyRefer(){let t=document.getElementById('refLinkT').innerText;navigator.clipboard.writeText(t);alert('✅ Refer Link কপি হয়েছে');}
setInterval(()=>{cur=(cur+1)%5;for(let i=1;i<=5;i++){let s=document.getElementById('s'+i);let d=document.getElementById('d'+i);if(s)s.classList.toggle('active',i-1==cur);if(d)d.classList.toggle('active',i-1==cur);}},3000);
init();
</script></body></html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
