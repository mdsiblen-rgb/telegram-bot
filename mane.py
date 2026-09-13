# -*- coding: utf-8 -*-
# Protidiner Kaj BD - FINAL EXACT DESIGN LIKE SCREENSHOT + NUMBER LOCK + LOGO CONTROL
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def default_data():
    return {
        "users":{},
        "withdraws":[],
        "settings":{
            "app_name":"Protidiner Kaj BD",
            "admin_name":"SHIBLI NOMAN",
            "bonus":1120,
            "ad_reward":2,
            "popup_reward":3,
            "company_limit":30,
            "popup_limit":20,
            "task_limit":5,
            "min_with":500,
            "bkash_logo":"",
            "nagad_logo":"",
            "bkash_name":"bKash",
            "bkash_sub":"Personal • Instant Payment",
            "nagad_name":"Nagad",
            "nagad_sub":"Personal • Fast Withdraw",
            "zone":"11764581",
            "tutorial_video":"https://youtube.com/",
            "support_link":"https://t.me/"
        },
        "tasks":[
            {"id":1,"title":"Telegram Channel Join","sub":"চ্যানেলে জয়েন করুন • ৳25","reward":25,"icon":"✈️","color":"#3b82f6"},
            {"id":2,"title":"YouTube Subscribe","sub":"সাবস্ক্রাইব + লাইক • ৳30","reward":30,"icon":"▶️","color":"#f97316"},
            {"id":3,"title":"Facebook Page Like","sub":"পেজে লাইক দিন • ৳20","reward":20,"icon":"👍","color":"#eab308"},
            {"id":4,"title":"Refer Friend","sub":"১ জন রেফার = ৳50 • ৳50","reward":50,"icon":"👥","color":"#1f2937"},
            {"id":5,"title":"Daily Check-in","sub":"প্রতিদিন একবার • ৳15","reward":15,"icon":"✅","color":"#22c55e"}
        ]
    }

def load_db():
    if not os.path.exists(DB):
        d=default_data()
        with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d
    try:
        with open(DB,'r',encoding='utf-8') as f:
            db=json.load(f)
            if "bkash_logo" not in db["settings"]:
                db["settings"]["bkash_logo"]=""; db["settings"]["nagad_logo"]=""; db["settings"]["bkash_name"]="bKash"; db["settings"]["bkash_sub"]="Personal • Instant Payment"; db["settings"]["nagad_name"]="Nagad"; db["settings"]["nagad_sub"]="Personal • Fast Withdraw"
            return db
    except:
        d=default_data()
        with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d

def save_db(d):
    with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","profile_img":"","balance":db["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":today,"phone":uid}
    u=db["users"][uid]
    if u.get("last")!=today:
        u["ads_today"]=0; u["popup_today"]=0; u["tasks_done"]=[]; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER_HTML)

@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only?id=8807178385",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get')
def api_get():
    db=load_db(); u=get_user(db,request.args.get('id','0')); save_db(db)
    wds=[w for w in db["withdraws"] if w["uid"]==str(request.args.get('id','0'))]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":wds,"all_withdraws":db["withdraws"],"all_users":db["users"]})

@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id')); typ=request.args.get('type','company'); s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":f"Limit {s['company_limit']} শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"Limit {s['popup_limit']} শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save_db(db); return jsonify({"msg":f"৳{s['ad_reward'] if typ=='company' else s['popup_reward']} যোগ"})

@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid)
    if tid in u["tasks_done"]: return jsonify({"msg":"আজকে করা হয়েছে"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    if not t: return jsonify({"msg":"Task নেই"})
    u["tasks_done"].append(tid); u["balance"]+=t["reward"]; u["total"]+=1; save_db(db)
    return jsonify({"msg":f"✅ {t['title']} - ৳{t['reward']} যোগ"})

@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    if len(num)<11: return jsonify({"msg":"সঠিক নাম্বার দিন"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"status":"Pending","time":str(datetime.now())[:16]})
    save_db(db); return jsonify({"msg":f"✅ {method} ৳{amt} Request সফল"})

@app.route('/api/user/update',methods=['POST'])
def user_update():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid)
    if 'name' in j: u["name"]=str(j['name'])[:25]
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save_db(db); return jsonify({"msg":"✅ প্রোফাইল সেভ হয়েছে","user":u})

@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db(); j=request.json
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ সব Save হয়েছে - Logo সহ"})

@app.route('/api/admin/balance',methods=['POST'])
def admin_balance():
    db=load_db(); j=request.json; uid=str(j.get('phone')); amt=int(j.get('amount',0)); typ=j.get('type','add')
    if uid not in db["users"]: return jsonify({"msg":"ইউজার নেই"})
    if typ=='add': db["users"][uid]["balance"]+=amt
    else: db["users"][uid]["balance"]-=amt
    if db["users"][uid]["balance"]<0: db["users"][uid]["balance"]=0
    save_db(db); return jsonify({"msg":f"✅ {uid} {typ} {amt} - New {db['users'][uid]['balance']}"})

USER_HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD</title>
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,-apple-system}
body{background:#070711;color:#fff;max-width:430px;margin:0 auto;padding-bottom:100px}
.top{padding:12px 14px;display:flex;justify-content:space-between;align-items:center;background:#0b0b1e;position:sticky;top:0;z-index:99;border-bottom:1px solid #1a1a2e}
.top-left{display:flex;align-items:center;gap:8px}
.crown{font-size:28px}
.app-name{font-weight:800;font-size:16px;display:flex;align-items:center;gap:6px}
.verified{background:#22c55e;color:#fff;font-size:10px;padding:2px 6px;border-radius:6px}
.admin-text{font-size:11px;color:#9ca3af}
.profile-top{width:44px;height:44px;border-radius:50%;background:#1a1a2e;border:2.5px solid #7c3aed;display:flex;align-items:center;justify-content:center;font-size:20px;overflow:hidden}
.profile-top img{width:100%;height:100%;object-fit:cover}
.card{margin:12px;border-radius:20px;padding:14px;background:#121228;border:1px solid #1e1e3a;position:relative}
.orange-banner{background:linear-gradient(90deg,#f59e0b,#ef4444);border-radius:20px;padding:32px 16px;text-align:center;font-weight:800;font-size:18px;margin:12px;border:none}
.balance-card{background:linear-gradient(90deg,#1e3a8a,#06b6d4,#10b981);border-radius:20px;padding:20px;text-align:center}
.balance-card h1{font-size:52px;font-weight:900;margin:6px 0}
.badges{display:flex;gap:6px;justify-content:center;margin-top:8px;flex-wrap:wrap}
.badges span{background:#00000040;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:600}
.btn-purple{background:linear-gradient(90deg,#7c3aed,#4f46e5);border:none;color:#fff;width:100%;padding:14px;border-radius:14px;font-weight:800;font-size:14px;margin-top:8px;cursor:pointer}
.btn-green{background:#16a34a;border:none;color:#fff;width:100%;padding:14px;border-radius:14px;font-weight:800;font-size:14px;margin-top:8px;cursor:pointer}
.btn-grey{background:#1e293b;border:none;color:#fff;width:100%;padding:14px;border-radius:14px;font-weight:800;font-size:14px;margin-top:8px;cursor:pointer}
.task-item{display:flex;justify-content:space-between;align-items:center;background:#0e0e24;border:1px solid #1e1e3a;border-radius:14px;padding:12px;margin:8px 0}
.task-left{display:flex;align-items:center;gap:10px}
.task-icon{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px}
.task-reward{background:#7c3aed;color:#fff;padding:8px 16px;border-radius:10px;font-weight:800;font-size:14px;cursor:pointer;border:none}
.payCard{display:flex;align-items:center;gap:12px;background:#121228;border:2px solid #1e1e3a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.payCard.active{border-color:#ec4899;background:#1a1030}
.payLogo{width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:22px;overflow:hidden}
.payLogo img{width:100%;height:100%;object-fit:cover}
.bk-bg{background:#e60076}.ng-bg{background:#f7941d}
.withdraw-input{background:#0e0e24;border:1px solid #1e1e3a;border-radius:12px;padding:14px;width:100%;color:#fff;margin:8px 0;outline:none}
.withdraw-btn{background:linear-gradient(90deg,#ec4899,#f59e0b);border:none;width:100%;padding:16px;border-radius:14px;font-weight:800;color:#fff;font-size:15px;cursor:pointer;margin-top:8px}
.green-box{background:linear-gradient(180deg,#065f46,#064e3b);border:1px solid #10b981;border-radius:16px;padding:14px;margin:12px}
.history-box{background:#121228;border:1px solid #1e1e3a;border-radius:16px;padding:14px;margin:12px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0b0b1e;display:flex;padding:8px 0 10px;border-radius:20px 20px 0 0;border-top:1px solid #1e1e3a;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:700;cursor:pointer}
.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
#lockOverlay,#welcomeOverlay,#adOverlay{position:fixed;inset:0;z-index:9999;display:none;justify-content:center;align-items:center;padding:20px}
#lockOverlay{display:flex;background:#070711f5}#welcomeOverlay{background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2)}#adOverlay{background:#000f;flex-direction:column;color:#fff}
.stat-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:10px}
.stat{ background:#0e0e24;border:1px solid #1e1e3a;border-radius:14px;padding:12px;text-align:center}
.stat b{font-size:20px;display:block}
</style></head><body>

<div class="top">
<div class="top-left"><div class="crown">👑</div><div><div class="app-name">Protidiner Kaj BD <span class="verified">✓</span></div><div class="admin-text">Admin: SHIBLI NOMAN</div></div></div>
<div class="profile-top" onclick="goPage('profile')" id="topP">👤</div>
</div>

<div id="lockOverlay">
<div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:360px;text-align:center">
<div style="font-size:48px">🔐</div>
<h2 style="color:#6d4cff;margin:8px 0">নাম্বার দিয়ে লক করুন</h2>
<p style="font-size:14px;font-weight:800;color:#000">নাম্বার দিয়ে লক করুন, নাম্বার দিয়ে লগইন করুন</p>
<p style="font-size:11px;color:#666;margin-top:4px">একবার লক করলে অন্য কেউ ঢুকতে পারবে না, টাকা আপনার নাম্বারে যাবে</p>
<input id="phoneInput" type="tel" placeholder="01XXXXXXXXX - 11 digit" maxlength="11" style="background:#f3f0ff;color:#000;border:1.5px solid #ddd;padding:14px;border-radius:12px;width:100%;margin-top:12px">
<button style="background:linear-gradient(90deg,#7c3aed,#4f46e5);color:#fff;border:none;width:100%;padding:14px;border-radius:12px;font-weight:800;margin-top:10px;cursor:pointer" onclick="sendOTP()">📲 OTP পাঠান</button>
<div id="otpSection" style="display:none;margin-top:10px">
<input id="otpInput" type="text" placeholder="OTP দিন - ডেমো 1234" maxlength="4" style="background:#f3f0ff;color:#000;border:1.5px solid #ddd;padding:14px;border-radius:12px;width:100%">
<button style="background:#16a34a;color:#fff;border:none;width:100%;padding:14px;border-radius:12px;font-weight:800;margin-top:8px;cursor:pointer" onclick="verifyOTP()">✅ ভেরিফাই করুন</button>
<p style="font-size:10px;color:#888;margin-top:6px">ডেমো OTP: 1234</p>
</div>
</div>
</div>

<div id="welcomeOverlay">
<div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:360px;text-align:center">
<div style="font-size:56px">🎉</div><h2 style="color:#6d4cff">স্বাগতম!</h2>
<div id="bonusBox" style="background:linear-gradient(90deg,#7c3aed,#4f46e5);color:#fff;padding:16px;border-radius:14px;font-size:30px;font-weight:800;margin:12px 0">1120 TK বোনাস 💰</div>
<p style="font-size:11px;color:#666">আপনি <b id="bonusText">1120 TK</b> Welcome Bonus পেয়েছেন<br>নাম্বার <b id="welcomePhone"></b> Lock হয়েছে</p>
<button style="background:linear-gradient(90deg,#7c3aed,#4f46e5);color:#fff;border:none;width:100%;padding:14px;border-radius:12px;font-weight:800;margin-top:12px;cursor:pointer" onclick="closeWelcome()">🚀 কাজ শুরু করুন</button>
</div>
</div>

<!-- HOME PAGE 1 -->
<div id="p-home" class="page active">
<div class="orange-banner">🎉 Daily Bonus Available Today</div>
<div class="balance-card">
<div style="font-size:13px">💰 আপনার বর্তমান ব্যালেন্স</div>
<h1 id="balMain">৳1120</h1>
<div class="badges"><span id="cBadge">Company 0/30</span><span id="pBadge">Popup 0/20</span><span id="tBadge">Total 0</span></div>
<div style="background:#0003;height:6px;border-radius:10px;margin-top:12px"><div id="prog" style="background:#fff;height:100%;width:0%;border-radius:10px"></div></div>
</div>
<div class="card">
<button class="btn-purple" onclick="watchAd('company')">📺 COMPANY ADS (৳2) - <span id="adCount">0/30</span></button>
<button class="btn-green" onclick="watchAd('popup')">💰 POPUP ADS (৳3) - <span id="popCount">0/20</span></button>
<button class="btn-grey">📋 TASK BONUS - 5 টা/দিন</button>
</div>
<div class="card" style="border-color:#f59e0b">
<div style="font-weight:800;margin-bottom:10px">🎉 আজকের স্পেশাল অফার</div>
<div style="background:#000;height:140px;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:2px solid #f59e0b">
<div style="font-size:48px">▶️</div>
<div style="background:#f59e0b;color:#000;padding:6px 14px;border-radius:20px;font-weight:800;font-size:12px;margin-top:8px">Tutorial - 2 মিনিটে শিখুন</div>
<div style="font-size:11px;color:#aaa;margin-top:6px">▶️ Click করলে ভিডিও চলবে</div>
</div>
<div style="font-size:12px;color:#aaa;margin-top:10px">Step 1: Ads দেখুন<br>Step 2: Task complete করুন<br>Step 3: ৳500 হলেই Withdraw</div>
</div>
</div>

<!-- TASK PAGE 2 -->
<div id="p-tasks" class="page">
<div class="card"><div style="font-weight:800;font-size:16px;margin-bottom:10px">📋 Task Bonus - দিনে 5 টা</div><div id="taskList"></div>
<div style="background:linear-gradient(90deg,#7c3aed,#4f46e5);border-radius:16px;padding:16px;margin-top:14px">
<div style="font-weight:800">🎁 Refer & Earn ৳50</div>
<div id="refLinkTask" style="background:#00000040;padding:10px;border-radius:10px;font-size:11px;margin-top:8px;word-break:break-all"></div>
<button style="background:#fff;color:#7c3aed;border:none;width:100%;padding:12px;border-radius:10px;font-weight:800;margin-top:8px;cursor:pointer" onclick="copyRef()">📋 লিংক কপি</button>
</div>
</div>
</div>

<!-- WALLET PAGE 3 -->
<div id="p-wallet" class="page">
<div class="card"><div style="font-weight:800">💳 Withdraw Method</div>
<div id="bkashOpt" class="payCard active" onclick="selectMethod('bKash')"><div class="payLogo bk-bg"><img id="bkashImg" style="display:none"><span id="bkashIcon">৳</span></div><div style="flex:1"><b id="bkashName">bKash</b><div style="font-size:11px;color:#aaa" id="bkashSub">Personal • Instant Payment</div></div><div style="color:#22c55e;font-weight:800" id="bkashCheck">✓</div></div>
<div id="nagadOpt" class="payCard" onclick="selectMethod('Nagad')"><div class="payLogo ng-bg"><img id="nagadImg" style="display:none"><span id="nagadIcon">৳</span></div><div style="flex:1"><b id="nagadName">Nagad</b><div style="font-size:11px;color:#aaa" id="nagadSub">Personal • Fast Withdraw</div></div><div style="color:#6b7280" id="nagadCheck">○</div></div>
<input id="accNum" class="withdraw-input" placeholder="01XXXXXXXXX" readonly>
<input id="amount" class="withdraw-input" type="number" placeholder="500">
<button class="withdraw-btn" onclick="doWithdraw()">🚀 Withdraw করুন</button>
</div>
<div class="green-box"><div style="font-weight:800">✅ Withdraw নিয়ম</div><div style="font-size:12px;margin-top:6px;color:#a7f3d0">- মিনিমাম ৳500<br>- Personal নাম্বার দিন<br>- 24 ঘণ্টায় পেমেন্ট</div></div>
<div class="history-box"><div style="font-weight:800">📜 History</div><div style="font-size:12px;color:#9ca3af;margin-top:6px" id="wHistory">কোনো Withdraw নেই</div></div>
</div>

<!-- SUPPORT PAGE 4 -->
<div id="p-support" class="page">
<div class="card"><div style="font-weight:800">🎬 কিভাবে কাজ করবেন?</div>
<div style="background:#000;height:160px;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:2px solid #f59e0b;margin-top:10px">
<div style="font-size:52px">▶️</div><div style="background:#f59e0b;color:#000;padding:6px 14px;border-radius:20px;font-weight:800;font-size:12px;margin-top:8px">Tutorial - 2 মিনিটে শিখুন</div>
<div style="font-size:11px;color:#aaa;margin-top:6px">▶️ Click করলে ভিডিও চলবে</div>
</div>
<div style="font-size:13px;color:#aaa;margin-top:10px">Step 1: Ads দেখুন<br>Step 2: Task complete করুন<br>Step 3: ৳500 হলেই Withdraw</div>
</div>
<div class="card"><div style="font-weight:800;font-size:16px">❓ FAQ</div>
<div style="background:#0e0e24;border:1px solid #1e1e3a;border-radius:12px;padding:12px;margin-top:8px"><b>Q: টাকা কখন পাবো?</b><div style="font-size:12px;color:#aaa">A: 24 ঘণ্টার মধ্যে bKash/Nagad এ।</div></div>
<div style="background:#0e0e24;border:1px solid #1e1e3a;border-radius:12px;padding:12px;margin-top:8px"><b>Q: VPN চলবে?</b><div style="font-size:12px;color:#aaa">A: না, ব্যান হবে।</div></div>
<div style="background:#0e0e24;border:1px solid #1e1e3a;border-radius:12px;padding:12px;margin-top:8px"><b>Q: 1 ফোনে কয়টা একাউন্ট?</b><div style="font-size:12px;color:#aaa">A: 1 টা।</div></div>
<div style="background:#0e0e24;border:1px solid #1e1e3a;border-radius:12px;padding:12px;margin-top:8px"><b>Q: Refer বোনাস?</b><div style="font-size:12px;color:#aaa">A: 1 জন = ৳50 সাথে সাথে।</div></div>
</div>
<div class="green-box" style="text-align:center"><div style="font-weight:800">🛡️ 100% Trusted</div><div style="font-size:11px;color:#a7f3d0;margin-top:4px">50k+ ইউজার, 100% পেমেন্ট গ্যারান্টি। সমস্যা হলে Telegram এ মেসেজ দিন।</div></div>
</div>

<!-- PROFILE PAGE 5 -->
<div id="p-profile" class="page">
<div class="card" style="text-align:center">
<div style="width:90px;height:90px;border-radius:50%;background:#1a1a2e;border:3px solid #7c3aed;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:40px;position:relative;overflow:hidden" id="profileCircle">👤<img id="profileImg" style="display:none;width:100%;height:100%;object-fit:cover"><div style="position:absolute;bottom:0;right:0;background:#7c3aed;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px">📷</div></div>
<div style="font-weight:800;font-size:18px;margin-top:10px" id="uName">User 8385</div><div style="font-size:12px;color:#aaa" id="uidShow">ID: 8807178385</div>
<div style="background:#7c3aed;display:inline-block;padding:4px 12px;border-radius:20px;font-size:11px;margin-top:6px">🏅 Bronze Member</div>
<input id="nameInput" class="withdraw-input" placeholder="আপনার নাম লিখুন" style="text-align:center">
<button class="btn-purple" onclick="document.getElementById('fileInput').click()">📸 গ্যালারি থেকে ছবি নিন</button><input type="file" id="fileInput" accept="image/*" style="display:none">
<button class="btn-green" onclick="saveProfile()">💾 Save Profile</button>
<div style="font-size:10px;color:#6b7280;margin-top:6px">ছবিতে বা বাটনে ক্লিক → গ্যালারি খুলবে → Save দিন</div>
</div>
<div class="card"><div style="font-weight:800">📊 পরিসংখ্যান</div>
<div class="stat-grid">
<div class="stat"><div style="font-size:22px">💰</div><b id="statBal">৳1120</b><div style="font-size:10px;color:#aaa">ব্যালেন্স</div></div>
<div class="stat"><div style="font-size:22px">📺</div><b id="statAds">0</b><div style="font-size:10px;color:#aaa">Ads</div></div>
<div class="stat"><div style="font-size:22px">📋</div><b id="statTask">0</b><div style="font-size:10px;color:#aaa">Task</div></div>
<div class="stat"><div style="font-size:22px">👥</div><b id="statTotal">0</b><div style="font-size:10px;color:#aaa">Total Work</div></div>
<div class="stat"><div style="font-size:22px">📅</div><b id="statDate" style="font-size:12px">2026-09-13</b><div style="font-size:10px;color:#aaa">Join Date</div></div>
<div class="stat"><div style="font-size:22px">🆔</div><b id="statID" style="font-size:11px">8807178385</b><div style="font-size:10px;color:#aaa">User ID</div></div>
</div>
</div>
<div class="card"><div style="font-weight:800">⚙️ সেটিংস</div>
<div class="task-item" style="cursor:pointer" onclick="goPage('wallet')"><div class="task-left"><div class="task-icon" style="background:#065f46">💸</div><div><b>Withdraw History</b><div style="font-size:11px;color:#aaa">আপনার পেমেন্ট দেখুন</div></div></div><div>➡️</div></div>
<div class="task-item"><div class="task-left"><div class="task-icon" style="background:#1e293b">🔗</div><div><b>My Refer Link</b><div style="font-size:10px;color:#aaa;word-break:break-all" id="myRefLink"></div></div></div><div style="cursor:pointer" onclick="copyRef()">📋</div></div>
<div class="task-item"><div class="task-left"><div class="task-icon" style="background:#1e293b">⭐</div><div><b>App Rate করুন</b><div style="font-size:11px;color:#aaa">5 Star দিন</div></div></div><div>➡️</div></div>
</div>
<div class="green-box" style="text-align:center"><div style="font-weight:800">🛡️ Verified User</div><div style="font-size:11px;color:#a7f3d0">আপনার একাউন্ট 100% Safe • 24h Support</div></div>
</div>

<div id="adOverlay"><h2>⏳ বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:64px;font-weight:900">15</div><div style="background:#ffffff33;width:80%;height:8px;border-radius:20px;margin-top:10px;overflow:hidden"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div></div>

<div class="btm">
<div id="nav-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div>
<div id="nav-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div>
<div id="nav-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div>
<div id="nav-support" onclick="goPage('support')"><span>💬</span>Support</div>
<div id="nav-profile" onclick="goPage('profile')"><span>👤</span>Profile</div>
</div>

<script>
let uid=localStorage.getItem('locked_phone')||'';
let selected='bKash';
let settings={};
function initApp(){
 if(!uid){ document.getElementById('lockOverlay').style.display='flex'; return; }
 document.getElementById('lockOverlay').style.display='none';
 fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{
  settings=d.settings; let u=d.user;
  document.getElementById('balMain').innerText='৳'+u.balance;
  document.getElementById('statBal').innerText='৳'+u.balance;
  document.getElementById('statAds').innerText=u.ads_today;
  document.getElementById('statTask').innerText=u.tasks_done.length;
  document.getElementById('statTotal').innerText=u.total;
  document.getElementById('statDate').innerText=u.join_date;
  document.getElementById('statID').innerText=u.id;
  document.getElementById('uidShow').innerText='ID: '+u.id;
  document.getElementById('uName').innerText=u.name||'User '+u.id.slice(-4);
  document.getElementById('nameInput').value=u.name||'';
  document.getElementById('welcomePhone').innerText=uid;
  document.getElementById('bonusBox').innerText=settings.bonus+' TK বোনাস 💰';
  document.getElementById('bonusText').innerText=settings.bonus+' TK';
  document.getElementById('accNum').value=uid;
  document.getElementById('myRefLink').innerText=window.location.origin+'/?ref='+uid;
  document.getElementById('refLinkTask').innerText=window.location.origin+'/?ref='+uid;
  document.getElementById('bkashName').innerText=settings.bkash_name;
  document.getElementById('bkashSub').innerText=settings.bkash_sub;
  document.getElementById('nagadName').innerText=settings.nagad_name;
  document.getElementById('nagadSub').innerText=settings.nagad_sub;
  if(settings.bkash_logo && settings.bkash_logo.startsWith('http')){
   document.getElementById('bkashImg').src=settings.bkash_logo;
   document.getElementById('bkashImg').style.display='block';
   document.getElementById('bkashIcon').style.display='none';
  }
  if(settings.nagad_logo && settings.nagad_logo.startsWith('http')){
   document.getElementById('nagadImg').src=settings.nagad_logo;
   document.getElementById('nagadImg').style.display='block';
   document.getElementById('nagadIcon').style.display='none';
  }
  if(u.profile_img){
   document.getElementById('profileImg').src=u.profile_img;
   document.getElementById('profileImg').style.display='block';
   document.getElementById('topP').innerHTML='<img src="'+u.profile_img+'" style="width:100%;height:100%;object-fit:cover">';
  }
  document.getElementById('cBadge').innerText='Company '+u.ads_today+'/'+settings.company_limit;
  document.getElementById('pBadge').innerText='Popup '+u.popup_today+'/'+settings.popup_limit;
  document.getElementById('tBadge').innerText='Total '+u.total;
  document.getElementById('adCount').innerText=u.ads_today+'/'+settings.company_limit;
  document.getElementById('popCount').innerText=u.popup_today+'/'+settings.popup_limit;
  document.getElementById('prog').style.width=(u.ads_today/settings.company_limit*100)+'%';
  let tHtml='';
  d.tasks.forEach(t=>{
   let done=u.tasks_done.includes(t.id);
   tHtml+=`<div class="task-item"><div class="task-left"><div class="task-icon" style="background:${t.color}">${t.icon}</div><div><b>${t.title}</b><div style="font-size:11px;color:#aaa">${t.sub}</div></div></div><button class="task-reward" style="background:${done?'#16a34a':'#7c3aed'}" onclick="doTask(${t.id})" ${done?'disabled':''}>${done?'✓':'৳'+t.reward}</button></div>`;
  });
  document.getElementById('taskList').innerHTML=tHtml;
  let wh='';
  d.withdraws.slice(-5).reverse().forEach(w=>{ wh+=`<div style="background:#0e0e24;padding:8px;border-radius:8px;margin-top:6px;font-size:11px">💸 ${w.method} ৳${w.amount} - ${w.status} - ${w.time}</div>`; });
  document.getElementById('wHistory').innerHTML=wh||'কোনো Withdraw নেই';
  if(!localStorage.getItem('welcomed_'+uid)){ document.getElementById('welcomeOverlay').style.display='flex'; }
 });
}
function sendOTP(){
 let p=document.getElementById('phoneInput').value;
 if(p.length!=11 ||!p.startsWith('01')){ alert('সঠিক 11 ডিজিট নাম্বার দিন - 01XXXXXXXXX'); return; }
 alert('✅ OTP পাঠানো হয়েছে: 1234\\nNumber: '+p);
 document.getElementById('otpSection').style.display='block';
}
function verifyOTP(){
 let o=document.getElementById('otpInput').value;
 let p=document.getElementById('phoneInput').value;
 if(o!='1234'){ alert('ভুল OTP! ডেমো OTP 1234'); return; }
 localStorage.setItem('locked_phone',p); uid=p;
 document.getElementById('lockOverlay').style.display='none';
 fetch('/api/get?id='+p).then(()=>{ initApp(); document.getElementById('welcomeOverlay').style.display='flex'; });
}
function closeWelcome(){ document.getElementById('welcomeOverlay').style.display='none'; localStorage.setItem('welcomed_'+uid,'1'); }
function goPage(p){
 document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));
 document.getElementById('p-'+p).classList.add('active');
 document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));
 document.getElementById('nav-'+p).classList.add('on');
 window.scrollTo(0,0);
}
function watchAd(type){
 document.getElementById('adOverlay').style.display='flex';
 let t=15; document.getElementById('timer').innerText=t;
 let ti=setInterval(()=>{
  t--; document.getElementById('timer').innerText=t;
  document.getElementById('timerProg').style.width=(t/15*100)+'%';
  if(t<=0){
   clearInterval(ti); document.getElementById('adOverlay').style.display='none';
   fetch('/api/reward?id='+uid+'&type='+type).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); });
  }
 },1000);
 if(typeof show_11764581==='function'){ try{show_11764581();}catch(e){} }
}
function doTask(id){
 fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); });
}
function copyRef(){
 let link=window.location.origin+'/?ref='+uid;
 navigator.clipboard.writeText(link); alert('✅ লিংক কপি হয়েছে: '+link);
}
function selectMethod(m){
 selected=m;
 document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');
 document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad');
 document.getElementById('bkashCheck').innerText=m==='bKash'?'✓':'○';
 document.getElementById('bkashCheck').style.color=m==='bKash'?'#22c55e':'#6b7280';
 document.getElementById('nagadCheck').innerText=m==='Nagad'?'✓':'○';
 document.getElementById('nagadCheck').style.color=m==='Nagad'?'#22c55e':'#6b7280';
}
function doWithdraw(){
 let a=document.getElementById('amount').value;
 let n=document.getElementById('accNum').value;
 if(!a){ alert('Amount দিন'); return; }
 fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,amount:a,method:selected})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); });
}
function saveProfile(){
 let nm=document.getElementById('nameInput').value;
 let img=document.getElementById('profileImg').src;
 let data={id:uid,name:nm};
 if(img && img.startsWith('data:')) data.profile_img=img;
 else if(document.getElementById('profileImg').style.display!=='none') data.profile_img=document.getElementById('profileImg').src;
 fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); });
}
document.getElementById('fileInput').addEventListener('change',function(e){
 let f=e.target.files[0]; let r=new FileReader();
 r.onload=function(ev){
  document.getElementById('profileImg').src=ev.target.result;
  document.getElementById('profileImg').style.display='block';
 };
 r.readAsDataURL(f);
});
initApp();
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin Panel</title>
<style>*{box-sizing:border-box;font-family:system-ui}body{background:#070711;color:#fff;max-width:700px;margin:0 auto;padding:16px}.card{background:#121228;border:1px solid #1e1e3a;border-radius:14px;padding:14px;margin:10px 0}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0e0e24;color:#fff;margin-top:6px}.btn{padding:10px 16px;border:none;border-radius:8px;font-weight:800;background:#7c3aed;color:#fff;cursor:pointer;margin-top:8px}table{width:100%;border-collapse:collapse;margin-top:8px}th,td{border:1px solid #333;padding:6px;font-size:11px}th{background:#0e0e24}</style></head><body>
<h2>👑 Admin Panel - EXACT DESIGN + Logo Control</h2>
<div class="card"><h3>⚙️ General</h3>App Name: <input id="app_name"><br>Bonus: <input id="bonus" type="number"><br>Ad Reward: <input id="ad_reward" type="number"><br>Min Withdraw: <input id="min_with" type="number"><br><button class="btn" onclick="save()">💾 Save</button></div>
<div class="card"><h3>🖼️ bKash / Nagad Logo Change - এডমিন থেকে পরিবর্তন</h3>
bKash Name: <input id="bkash_name" placeholder="bKash"><br>bKash Sub: <input id="bkash_sub" placeholder="Personal • Instant Payment"><br>bKash Logo URL (Direct Image Link): <input id="bkash_logo" placeholder="https://i.ibb.co/.../bkash.png"><br><br>
Nagad Name: <input id="nagad_name" placeholder="Nagad"><br>Nagad Sub: <input id="nagad_sub" placeholder="Personal • Fast Withdraw"><br>Nagad Logo URL: <input id="nagad_logo" placeholder="https://i.ibb.co/.../nagad.png"><br>
<button class="btn" onclick="save()">💾 Logo Save করুন</button>
<p style="font-size:10px;color:#aaa;margin-top:6px">Tip: imgbb.com এ ছবি আপলোড করে Direct Link বসান - তাহলে App এ লোগো চেঞ্জ হবে</p>
</div>
<div class="card"><h3>💸 Balance Add/Minus</h3><input id="admPhone" placeholder="Phone 01XXXXXXXXX"><input id="admAmount" type="number" placeholder="Amount"><div style="display:flex;gap:8px"><button class="btn" style="background:#16a34a" onclick="bal('add')">+ যোগ</button><button class="btn" style="background:#ef4444" onclick="bal('minus')">- মাইনাস</button></div><div id="admMsg" style="font-size:12px;margin-top:6px"></div></div>
<div class="card"><h3>👥 Users - Locked Numbers</h3><div id="userList"></div></div>
<div class="card"><h3>💰 Withdraw</h3><div id="withdrawList"></div></div>
<script>
function load(){
 fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{
  let s=d.settings;
  document.getElementById('app_name').value=s.app_name||'';document.getElementById('bonus').value=s.bonus||1120;document.getElementById('ad_reward').value=s.ad_reward||2;document.getElementById('min_with').value=s.min_with||500;
  document.getElementById('bkash_name').value=s.bkash_name||'';document.getElementById('bkash_sub').value=s.bkash_sub||'';document.getElementById('bkash_logo').value=s.bkash_logo||'';
  document.getElementById('nagad_name').value=s.nagad_name||'';document.getElementById('nagad_sub').value=s.nagad_sub||'';document.getElementById('nagad_logo').value=s.nagad_logo||'';
  let uhtml='<table><tr><th>Phone (Locked ID)</th><th>Name</th><th>Bal</th><th>Join</th></tr>';Object.values(d.all_users).forEach(u=>{uhtml+=`<tr><td>${u.phone}</td><td>${u.name}</td><td>${u.balance}</td><td>${u.join_date}</td></tr>`;});uhtml+='</table>';document.getElementById('userList').innerHTML=uhtml;
  let whtml='<table><tr><th>Phone</th><th>Amt</th><th>Method</th><th>Num</th><th>Time</th></tr>';d.all_withdraws.slice(-50).reverse().forEach(w=>{whtml+=`<tr><td>${w.uid}</td><td>${w.amount}</td><td>${w.method}</td><td>${w.number}</td><td>${w.time}</td></tr>`;});whtml+='</table>';document.getElementById('withdrawList').innerHTML=whtml;
 });
}
function save(){
 let data={};document.querySelectorAll('input').forEach(e=>{if(e.id &&!e.id.startsWith('adm')) data[e.id]=e.value;});
 fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{alert(d.msg);load();});
}
function bal(t){let p=document.getElementById('admPhone').value;let a=document.getElementById('admAmount').value;fetch('/api/admin/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:p,amount:a,type:t})}).then(r=>r.json()).then(d=>{document.getElementById('admMsg').innerText=d.msg;alert(d.msg);load();});}
load();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
