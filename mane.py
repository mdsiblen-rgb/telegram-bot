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
                "slider1": "🎉 Daily Bonus Available Today",
                "slider2": "📢 Company Sponsored - 100% Safe",
                "slider3": "🎁 50 Ads দেখলে ৳100 বোনাস!",
                "slider4": "💰 100% Payment Guaranteed",
                "slider5": "🔥 প্রতিদিন কাজ করুন",
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
    u = db["users"][uid]
    if u.get("last")!= today:
        u["company"] = 0
        u["popup"] = 0
        u["last"] = today
    return u

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/get')
def api_get():
    db = load_db()
    uid = request.args.get('id', '8807178385')
    u = get_user(db, uid)
    save_db(db)
    user_withdraws = [w for w in db["withdraws"] if w["uid"] == uid]
    return jsonify({"user": u, "settings": db["settings"], "withdraws": user_withdraws})

@app.route('/api/reward')
def reward():
    db = load_db()
    uid = request.args.get('id', '8807178385')
    t = request.args.get('type', 'company')
    u = get_user(db, uid)
    if t == 'company':
        if u["company"] >= 30:
            return jsonify({"msg": "Limit"})
        u["company"] += 1
        u["balance"] += 2
    else:
        if u["popup"] >= 20:
            return jsonify({"msg": "Limit"})
        u["popup"] += 1
        u["balance"] += 3
    u["total"] = u["company"] + u["popup"]
    save_db(db)
    return jsonify({"msg": "ok"})

@app.route('/api/task/done', methods=['POST'])
def task_done():
    db = load_db()
    j = request.json
    uid = j.get('id')
    tid = str(j.get('tid'))
    amt = int(j.get('amt', 20))
    u = get_user(db, uid)
    if tid not in u["tasks"]:
        u["tasks"].append(tid)
        u["balance"] += amt
    save_db(db)
    return jsonify({"msg": f"✅ ৳{amt} Bonus যোগ হয়েছে"})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    db = load_db()
    j = request.json
    uid = j.get('id')
    u = get_user(db, uid)
    amt = int(j.get('amt', 0))
    if amt < 500:
        return jsonify({"msg": "❌ মিনিমাম ৳500"})
    if u["balance"] < amt:
        return jsonify({"msg": "❌ ব্যালেন্স কম"})
    u["balance"] -= amt
    db["withdraws"].append({
        "uid": str(uid),
        "amt": amt,
        "num": j.get('num'),
        "method": j.get('method'),
        "status": "Pending",
        "time": str(datetime.now())[:16]
    })
    save_db(db)
    return jsonify({"msg": f"✅ {j.get('method')} এ ৳{amt} রিকোয়েস্ট পাঠানো হয়েছে"})

@app.route('/api/profile/save', methods=['POST'])
def profile_save():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    if j.get('name'):
        u["name"] = j.get('name')
    if j.get('img'):
        u["img"] = j.get('img')
    save_db(db)
    return jsonify({"msg": "✅ Profile Save হয়েছে"})

HTML = """<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#000;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.header{background:#0a0a18;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bottomNav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;justify-content:space-around;padding:10px 0 14px;border-radius:24px 24px 0 0;z-index:99;border-top:1px solid #1e1e3a}
.navItem{text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.navItem.active{color:#fff}.navItem span{font-size:24px;display:block}
.page{display:none}.page.active{display:block}
.btn{width:100%;padding:16px;border:none;border-radius:16px;font-weight:800;color:#fff;margin:7px 0;cursor:pointer}
.btn-purple{background:#6d28d9}.btn-green{background:#16a34a}.btn-dark{background:#232336}
/* Home */
.sliderWrap{position:relative;margin:12px}.slider{height:130px;border-radius:24px;display:flex;align-items:center;justify-content:center;font-weight:800;position:relative;background:linear-gradient(90deg,#ff9a00,#ff3d00);overflow:hidden}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;transition:1s}.slide.active{opacity:1}
.balanceCard{background:linear-gradient(135deg,#2a5bff,#00d1b2);border-radius:24px;padding:20px;text-align:center;margin:12px}
.dotWrap{display:flex;gap:6px;justify-content:center;margin-top:10px}.dot{width:8px;height:8px;background:#fff4;border-radius:50%}.dot.active{background:#fff;width:22px}
/* Task */
.taskContainer{background:#0f0f1f;border-radius:24px;padding:12px;margin:12px;border:1px solid #1e1e2e}
.taskRow{display:flex;align-items:center;justify-content:space-between;background:#17172a;border:1px solid #22223a;border-radius:16px;padding:12px 14px;margin:10px 0}
.referBox{background:linear-gradient(135deg,#6d28d9,#7c3aed);border-radius:20px;padding:16px;margin:12px}
.referLinkBox{background:#2a1a6a;border-radius:12px;padding:10px;font-size:12px;word-break:break-all;color:#c4b5fd;margin-top:10px}
.teleBox{background:linear-gradient(90deg,#0ea5e9,#0284c7);border-radius:20px;padding:16px;margin:12px;display:flex;justify-content:space-between;align-items:center}
.rulesBox{background:#151528;border-radius:20px;padding:16px;margin:12px;border:1px solid #222}
/* Wallet */
.walletBalanceCard{background:linear-gradient(135deg,#1e293b,#2d3a4f);border-radius:24px;padding:24px;text-align:center;margin:12px;border:1px solid #1e293b}
.withdrawBox{background:#131326;border-radius:24px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.methodCard{display:flex;align-items:center;gap:12px;background:#1a1a30;border:2px solid #25253d;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.methodCard.active{border-color:#e2136e;background:#201530}
.methodIcon{width:52px;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px}
.inputField{width:100%;background:#0e0e20;border:1px solid #25253d;border-radius:14px;padding:14px;color:#fff;margin:8px 0;font-size:14px}
.withdrawBtn{width:100%;background:linear-gradient(90deg,#e2136e,#ff8c00);border:none;border-radius:14px;padding:16px;font-weight:900;color:#fff;font-size:16px;margin-top:12px;cursor:pointer}
/* Support */
.supportTopBox{background:linear-gradient(135deg,#6d28d9,#4f46e5);border-radius:24px;padding:20px;margin:12px;text-align:center}
.contactBox{background:#131326;border-radius:20px;padding:14px;margin:12px;border:1px solid #1e1e3a}
.contactRow{display:flex;align-items:center;gap:12px;background:#1a1a30;border:1.5px solid #25253d;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.videoBox{background:#000;border:2px solid #ff8c00;border-radius:20px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer}
.faqBox{background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.trustedBox{background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px;text-align:center}
/* Profile */
.profileTopCard{background:linear-gradient(180deg,#162040,#0f172a);border-radius:24px;padding:20px;margin:12px;border:1px solid #1e293b;text-align:center}
.avatarWrap{width:120px;height:120px;border-radius:50%;margin:0 auto;position:relative;border:3px solid #6d4cff;display:flex;align-items:center;justify-content:center;background:#0f172a;overflow:hidden;cursor:pointer}
.avatarImg{width:100%;height:100%;object-fit:cover;display:none}
.statsBox{background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.statsGrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px}
.statCard{background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;text-align:center}
.settingsBox{background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.settingRow{display:flex;align-items:center;gap:12px;background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;margin:10px 0;cursor:pointer}
</style></head><body>
<div class="header"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:900">Protidiner Kaj BD <span style="background:#22c55e;padding:2px 6px;border-radius:50%;font-size:10px">✓</span></div><div style="font-size:11px;color:#9ca3af">Admin: SHIBLI NOMAN</div></div></div><div style="width:42px;height:42px;border-radius:50%;background:#1e1e3a;border:2px solid #6d4cff;display:flex;align-items:center;justify-content:center" onclick="goP('profile')">👤</div></div>

<!-- 1st PAGE - HOME -->
<div id="p-home" class="page active">
<div class="sliderWrap"><div class="slider"><div id="s1" class="slide active"><span id="st1">Daily Bonus</span></div><div id="s2" class="slide"><span id="st2">Company Safe</span></div><div id="s3" class="slide"><span id="st3">Bonus</span></div><div id="s4" class="slide"><span id="st4">Payment</span></div><div id="s5" class="slide"><span id="st5">কাজ</span></div></div><div style="height:130px"></div><div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div></div>
<div class="balanceCard"><div style="font-size:13px" id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:56px;font-weight:900" id="balHome">৳1120</div><div style="display:flex;gap:6px;justify-content:center;margin-top:10px"><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bC">Company 0/30</span><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bP">Popup 0/20</span><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bT">Total 0</span></div></div>
<div style="background:#15151f;border-radius:24px;padding:14px;margin:12px"><button class="btn btn-purple" onclick="doR('company')">📺 COMPANY ADS (৳2) - <span id="btnC">0/30</span></button><button class="btn btn-green" onclick="doR('popup')">💰 POPUP ADS (৳3) - <span id="btnP">0/20</span></button><button class="btn btn-dark" onclick="goP('tasks')">📋 TASK BONUS - 5 টা/দিন</button></div>
<div style="border:2px solid #f59e0b;border-radius:20px;padding:14px;margin:12px;background:#12121e"><div style="font-weight:800">🎉 আজকের স্পেশাল অফার</div><div style="font-size:13px;color:#9ca3af;margin-top:4px">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</div></div>
</div>

<!-- 2nd PAGE - TASK -->
<div id="p-tasks" class="page">
<div class="taskContainer"><div style="font-size:20px;font-weight:900;margin-bottom:12px">📋 Task Bonus - দিনে 5 টা</div>
<div class="taskRow"><div style="display:flex;align-items:center;gap:12px"><div style="width:44px;height:44px;border-radius:12px;background:#0ea5e922;display:flex;align-items:center;justify-content:center">✈️</div><div><b>Telegram Channel Join</b><div style="font-size:12px;color:#9ca3af">চ্যানেলে জয়েন করুন • ৳25</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('tele',25)">৳25</button></div>
<div class="taskRow"><div style="display:flex;align-items:center;gap:12px"><div style="width:44px;height:44px;border-radius:12px;background:#f59e0b22;display:flex;align-items:center;justify-content:center">▶️</div><div><b>YouTube Subscribe</b><div style="font-size:12px;color:#9ca3af">সাবস্ক্রাইব + লাইক • ৳30</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('yt',30)">৳30</button></div>
<div class="taskRow"><div style="display:flex;align-items:center;gap:12px"><div style="width:44px;height:44px;border-radius:12px;background:#22c55e22;display:flex;align-items:center;justify-content:center">👍</div><div><b>Facebook Page Like</b><div style="font-size:12px;color:#9ca3af">পেজে লাইক দিন • ৳20</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('fb',20)">৳20</button></div>
<div class="taskRow"><div style="display:flex;align-items:center;gap:12px"><div style="width:44px;height:44px;border-radius:12px;background:#fff1;display:flex;align-items:center;justify-content:center">👥</div><div><b>Refer Friend</b><div style="font-size:12px;color:#9ca3af">১ জন রেফার = ৳50 • ৳50</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="goP('profile')">৳50</button></div>
<div class="taskRow"><div style="display:flex;align-items:center;gap:12px"><div style="width:44px;height:44px;border-radius:12px;background:#22c55e22;display:flex;align-items:center;justify-content:center">✅</div><div><b>Daily Check-in</b><div style="font-size:12px;color:#9ca3af">প্রতিদিন একবার • ৳15</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('check',15)">৳15</button></div>
</div>
<div class="referBox"><div style="font-size:18px;font-weight:900">🎁 Refer & Earn ৳50</div><div class="referLinkBox" id="refLinkT">https://telegram-bot-1-v77g.onrender.com/?ref=8807178385</div><button style="background:#fff;color:#4c1d95;border:none;width:100%;padding:12px;border-radius:12px;font-weight:900;margin-top:12px" onclick="copyRefer()">📋 লিংক কপি</button></div>
<div class="teleBox"><div><div style="font-size:18px;font-weight:900">📢 Telegram Channel</div><div style="font-size:12px;opacity:.8">আপডেট ও প্রুফ</div></div><button style="background:#fff;color:#0ea5e9;border:none;padding:10px 18px;border-radius:20px;font-weight:800" onclick="window.open('https://t.me/','_blank')">Join ✈️</button></div>
<div class="rulesBox"><div style="font-size:18px;font-weight:900">⚠️ Task নিয়ম</div><div style="margin-top:10px;font-size:13px;color:#9ca3af;line-height:1.8">- প্রতিদিন 5 টা Task<br>- লিংকে গিয়ে জয়েন করুন<br>- Verify করলে টাকা যোগ</div></div>
</div>

<!-- 3rd PAGE - WALLET -->
<div id="p-wallet" class="page">
<div class="walletBalanceCard"><div style="font-size:13px;color:#94a3b8">ব্যালেন্স</div><div style="font-size:56px;font-weight:900" id="wBal">৳1120</div><div style="font-size:13px;color:#94a3b8">Min ৳500</div></div>
<div class="withdrawBox"><div style="font-size:18px;font-weight:900;margin-bottom:12px">💸 Withdraw Method</div>
<div id="bkCard" class="methodCard active" onclick="selPay('bKash')"><div class="methodIcon" style="background:#e2136e">৳</div><div><b>bKash</b><div style="font-size:12px;color:#9ca3af">Personal • Instant Payment</div></div><div style="margin-left:auto;color:#22c55e;font-size:22px" id="bkCheck">✓</div></div>
<div id="ngCard" class="methodCard" onclick="selPay('Nagad')"><div class="methodIcon" style="background:#ff8c00">৳</div><div><b>Nagad</b><div style="font-size:12px;color:#9ca3af">Personal • Fast Withdraw</div></div><div style="margin-left:auto;color:#22c55e;font-size:22px;display:none" id="ngCheck">✓</div></div>
<input id="accNum" class="inputField" placeholder="01XXXXXXXXXX"><input id="wdAmt" class="inputField" type="number" placeholder="500"><button class="withdrawBtn" onclick="doWd()">🚀 Withdraw করুন</button></div>
<div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:16px;margin:12px"><div style="font-size:18px;font-weight:900">✅ Withdraw নিয়ম</div><div style="margin-top:10px;font-size:14px;line-height:1.9">- মিনিমাম ৳500<br>- Personal নাম্বার দিন<br>- 24 ঘণ্টায় পেমেন্ট</div></div>
<div style="background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a"><div style="font-size:18px;font-weight:900">📜 History</div><div id="wdHistory" style="margin-top:8px;font-size:13px;color:#9ca3af">কোনো Withdraw নেই</div></div>
</div>

<!-- 4th PAGE - SUPPORT -->
<div id="p-support" class="page">
<div class="supportTopBox"><div style="background:#00000030;border-radius:50px;padding:10px 16px;font-size:13px;display:inline-block">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:40px;margin:10px 0">💬</div><div style="font-size:22px;font-weight:900">আমরা আছি আপনার পাশে</div><div style="font-size:13px;margin-top:6px;opacity:.85">২৪ ঘণ্টা সাপোর্ট • 100% Trusted • SHIBLI NOMAN Team</div></div>
<div class="contactBox"><div style="font-size:18px;font-weight:900;margin-bottom:12px">🚀 দ্রুত যোগাযোগ করুন</div>
<div class="contactRow" style="border-color:#0ea5e9" onclick="window.open('https://t.me/','_blank')"><div style="width:52px;height:52px;border-radius:14px;background:#0ea5e9;display:flex;align-items:center;justify-content:center">✈️</div><div><div style="font-weight:700">Telegram Support (Fast Reply)</div><div style="font-size:12px;color:#9ca3af">2 মিনিটে রিপ্লাই • 9AM-12AM</div></div><div style="margin-left:auto">➡️</div></div>
<div class="contactRow" onclick="window.open('https://wa.me/8801','_blank')"><div style="width:52px;height:52px;border-radius:14px;background:#22c55e;display:flex;align-items:center;justify-content:center">💬</div><div><div style="font-weight:700">WhatsApp Support</div><div style="font-size:12px;color:#9ca3af">01XXXXXXXXXX</div></div><div style="margin-left:auto">➡️</div></div>
<div class="contactRow" onclick="window.location.href='mailto:support@protidinerkajbd.com'"><div style="width:52px;height:52px;border-radius:14px;background:#f59e0b;display:flex;align-items:center;justify-content:center">📧</div><div><div style="font-weight:700">Email Support</div><div style="font-size:12px;color:#9ca3af">support@protidinerkajbd.com</div></div><div style="margin-left:auto">➡️</div></div>
</div>
<div style="background:#131326;border-radius:20px;padding:16px;margin:12px;border:1px solid #1e1e3a"><div style="font-size:18px;font-weight:900;margin-bottom:12px">🎥 কিভাবে কাজ করবেন?</div><div class="videoBox" onclick="window.open('https://youtube.com/','_blank')"><div style="width:78px;height:78px;background:linear-gradient(135deg,#ff8c00,#f59e0b);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:40px">▶️</div><div style="background:#ff8c00;color:#fff;padding:8px 18px;border-radius:20px;font-weight:800;margin-top:16px">Tutorial - 2 মিনিটে শিখুন</div></div></div>
<div class="faqBox"><div style="font-size:20px;font-weight:900;margin-bottom:12px">❓ FAQ</div><div style="background:#1a1a30;border-radius:14px;padding:14px;margin:10px 0"><b>Q: টাকা কখন পাবো?</b><div style="font-size:13px;color:#9ca3af">A: 24 ঘণ্টার মধ্যে bKash/Nagad এ।</div></div><div style="background:#1a1a30;border-radius:14px;padding:14px;margin:10px 0"><b>Q: VPN চলবে?</b><div style="font-size:13px;color:#9ca3af">A: না, ব্যান হবে।</div></div><div style="background:#1a1a30;border-radius:14px;padding:14px;margin:10px 0"><b>Q: 1 ফোনে কয়টা একাউন্ট?</b><div style="font-size:13px;color:#9ca3af">A: 1 টা।</div></div><div style="background:#1a1a30;border-radius:14px;padding:14px;margin:10px 0"><b>Q: Refer বোনাস?</b><div style="font-size:13px;color:#9ca3af">A: 1 জন = ৳50 সাথে সাথে।</div></div></div>
<div class="trustedBox"><div style="font-size:20px;font-weight:900">🛡️ 100% Trusted</div><div style="font-size:13px;margin-top:6px;opacity:.9">50k+ ইউজার, 100% পেমেন্ট গ্যারান্টি।</div></div>
</div>

<!-- 5th PAGE - PROFILE -->
<div id="p-profile" class="page">
<div class="profileTopCard">
<div class="avatarWrap" onclick="openGallery()"><img id="avImg" class="avatarImg"><div id="avIcon" style="font-size:60px">👤</div><div style="position:absolute;bottom:0;right:5px;width:32px;height:32px;background:#1e293b;border:2px solid #6d4cff;border-radius:50%;display:flex;align-items:center;justify-content:center">📸</div></div>
<div style="margin-top:14px;font-size:20px;font-weight:800" id="pNameTop">User 8385</div><div style="font-size:12px;color:#9ca3af" id="pIdTop">ID: 8807178385</div><div style="background:#6d4cff;color:#fff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:700;display:inline-block;margin-top:8px">🏅 Bronze Member</div>
<input id="nameIn" style="width:100%;background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:14px;color:#fff;margin-top:14px;text-align:center" placeholder="আপনার নাম লিখুন">
<button style="width:100%;background:#6d4cff;border:none;border-radius:14px;padding:14px;color:#fff;font-weight:800;margin-top:12px" onclick="openGallery()">📸 গ্যালারি থেকে ছবি নিন</button>
<button style="width:100%;background:#22c55e;border:none;border-radius:14px;padding:14px;color:#fff;font-weight:800;margin-top:10px" onclick="saveProfile()">💾 Save Profile</button>
<div style="font-size:11px;color:#64748b;margin-top:8px">ছবিতে বা বাটনে ক্লিক → গ্যালারি খুলবে → Save দিন</div>
<input type="file" id="fileIn" accept="image/*" style="display:none" onchange="handleFile(this)">
</div>
<div class="statsBox"><div style="font-size:18px;font-weight:900">📊 পরিসংখ্যান</div><div class="statsGrid">
<div class="statCard"><div>💰</div><div style="font-size:18px;font-weight:900" id="sBal">৳1120</div><div style="font-size:11px;color:#9ca3af">ব্যালেন্স</div></div>
<div class="statCard"><div>📺</div><div style="font-size:18px;font-weight:900" id="sAds">0</div><div style="font-size:11px;color:#9ca3af">Ads</div></div>
<div class="statCard"><div>📋</div><div style="font-size:18px;font-weight:900" id="sTask">0</div><div style="font-size:11px;color:#9ca3af">Task</div></div>
<div class="statCard"><div>👥</div><div style="font-size:18px;font-weight:900">0</div><div style="font-size:11px;color:#9ca3af">Total Work</div></div>
<div class="statCard"><div>📅</div><div style="font-size:16px;font-weight:900" id="sDate">2026-09-13</div><div style="font-size:11px;color:#9ca3af">Join Date</div></div>
<div class="statCard"><div style="background:#a855f7;padding:2px 6px;border-radius:4px;font-size:12px;display:inline-block">ID</div><div style="font-size:12px;font-weight:900;margin-top:6px" id="sId">8807178385</div><div style="font-size:11px;color:#9ca3af">User ID</div></div>
</div></div>
<div class="settingsBox"><div style="font-size:18px;font-weight:900">⚙️ সেটিংস</div>
<div class="settingRow" onclick="goP('wallet')"><div style="width:50px;height:50px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center">💸</div><div><div style="font-weight:700">Withdraw History</div><div style="font-size:12px;color:#9ca3af">আপনার পেমেন্ট দেখুন</div></div><div style="margin-left:auto">➡️</div></div>
<div class="settingRow" onclick="copyRefer()"><div style="width:50px;height:50px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center">🔗</div><div style="flex:1"><div style="font-weight:700">My Refer Link</div><div style="font-size:11px;color:#9ca3af;word-break:break-all" id="refLink">https://telegram-bot-1-v77g.onrender.com/?ref=8807178385</div></div><div>📋</div></div>
<div class="settingRow"><div style="width:50px;height:50px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center">⭐</div><div><div style="font-weight:700">App Rate করুন</div><div style="font-size:12px;color:#9ca3af">5 Star দিন</div></div><div style="margin-left:auto">➡️</div></div>
</div>
<div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px;text-align:center"><div style="font-size:20px;font-weight:900">🛡️ Verified User</div><div style="font-size:13px;margin-top:4px;opacity:.9">আপনার একাউন্ট 100% Safe • 24h Support</div></div>
</div>

<div class="bottomNav"><div class="navItem active" id="n-home" onclick="goP('home')"><span>🏠</span>Home</div><div class="navItem" id="n-tasks" onclick="goP('tasks')"><span>📋</span>Task</div><div class="navItem" id="n-wallet" onclick="goP('wallet')"><span>💰</span>Wallet</div><div class="navItem" id="n-support" onclick="goP('support')"><span>💬</span>Support</div><div class="navItem" id="n-profile" onclick="goP('profile')"><span>👤</span>Profile</div></div>

<script>
let uid='8807178385',method='bKash',tempImg='',cur=0;
function goP(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.navItem').forEach(e=>e.classList.remove('active'));document.getElementById('n-'+p).classList.add('active');}
function init(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{let u=d.user;let s=d.settings;for(let i=1;i<=5;i++){let el=document.getElementById('st'+i);if(el)el.innerText=s['slider'+i]||'';}document.getElementById('balHome').innerText='৳'+u.balance;document.getElementById('wBal').innerText='৳'+u.balance;document.getElementById('bC').innerText='Company '+u.company+'/30';document.getElementById('bP').innerText='Popup '+u.popup+'/20';document.getElementById('bT').innerText='Total '+u.total;document.getElementById('btnC').innerText=u.company+'/30';document.getElementById('btnP').innerText=u.popup+'/20';document.getElementById('pNameTop').innerText=u.name;document.getElementById('pIdTop').innerText='ID: '+u.id;document.getElementById('nameIn').value=u.name;document.getElementById('sBal').innerText='৳'+u.balance;document.getElementById('sAds').innerText=u.company+u.popup;document.getElementById('sTask').innerText=u.tasks.length;document.getElementById('sDate').innerText=u.join;document.getElementById('sId').innerText=u.id;document.getElementById('refLink').innerText='https://telegram-bot-1-v77g.onrender.com/?ref='+u.id;document.getElementById('refLinkT').innerText='https://telegram-bot-1-v77g.onrender.com/?ref='+u.id;if(u.img){document.getElementById('avImg').src=u.img;document.getElementById('avImg').style.display='block';document.getElementById('avIcon').style.display='none';tempImg=u.img;}let hist=d.withdraws;let hEl=document.getElementById('wdHistory');if(hist.length>0){hEl.innerHTML=hist.map(h=>`<div style="background:#0e0e20;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between"><span>${h.method} - ৳${h.amt}</span><span style="color:#f59e0b">${h.status}</span></div>`).join('');}else{hEl.innerText='কোনো Withdraw নেই';}});}
function doR(t){fetch('/api/reward?id='+uid+'&type='+t).then(()=>{init();if(typeof show_11764581==='function')show_11764581();});}
function doTask(id,amt){if(id!='check'){let s='';if(id=='tele')s='https://t.me/';if(id=='yt')s='https://youtube.com/';if(id=='fb')s='https://facebook.com/';if(s)window.open(s,'_blank');}fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function selPay(m){method=m;document.getElementById('bkCard').classList.toggle('active',m=='bKash');document.getElementById('ngCard').classList.toggle('active',m=='Nagad');document.getElementById('bkCheck').style.display=m=='bKash'?'block':'none';document.getElementById('ngCheck').style.display=m=='Nagad'?'block':'none';}
function doWd(){let num=document.getElementById('accNum').value;let amt=document.getElementById('wdAmt').value;if(!num||!amt){alert('নাম্বার ও টাকা দিন');return;}fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:method})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function openGallery(){document.getElementById('fileIn').click();}
function handleFile(inp){let f=inp.files[0];let r=new FileReader();r.onload=e=>{tempImg=e.target.result;document.getElementById('avImg').src=tempImg;document.getElementById('avImg').style.display='block';document.getElementById('avIcon').style.display='none';};r.readAsDataURL(f);}
function saveProfile(){let n=document.getElementById('nameIn').value;fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:tempImg})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function copyRefer(){let t=document.getElementById('refLink').innerText;navigator.clipboard.writeText(t);alert('✅ Refer Link কপি হয়েছে');}
setInterval(()=>{cur=(cur+1)%5;for(let i=1;i<=5;i++){let s=document.getElementById('s'+i);let d=document.getElementById('d'+i);if(s)s.classList.toggle('active',i-1==cur);if(d)d.classList.toggle('active',i-1==cur);}},3000);
init();
</script></body></html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
