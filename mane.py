# -*- coding: utf-8 -*-
# FINAL FULL 1-5 - A to Z - NUMBER LOCK + OTP + 1120 BONUS + ADMIN + VIDEO SYSTEM
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
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","app_logo":"👑",
            "admin_profile_img":"","zone":"11764581","bonus":1120,"ad_reward":2,"popup_reward":3,
            "company_limit":30,"popup_limit":20,"task_limit":5,"min_with":500,
            "official_banners":[],"google_ads":["🎉 Daily Bonus Available","⭐ bKash • Nagad • Trusted","📢 100% Safe"],
            "offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!",
            "balance_title":"আপনার বর্তমান ব্যালেন্স",
            "tg_channel":"https://t.me/","support_link":"https://t.me/","whatsapp":"01XXXXXXXXX",
            "tutorial_video":"https://youtube.com/"
        },
        "tasks":[
            {"id":1,"title":"Telegram Channel Join","reward":25,"icon":"✈️","link":"https://t.me/","desc":"চ্যানেলে জয়েন করুন"},
            {"id":2,"title":"YouTube Subscribe","reward":30,"icon":"▶️","link":"https://youtube.com/","desc":"সাবস্ক্রাইব + লাইক"},
            {"id":3,"title":"Facebook Page Like","reward":20,"icon":"👍","link":"https://facebook.com/","desc":"পেজে লাইক দিন"},
            {"id":4,"title":"Refer Friend","reward":50,"icon":"👨‍👩‍👧‍👦","link":"","desc":"১ জন রেফার = ৳50"},
            {"id":5,"title":"Daily Check-in","reward":15,"icon":"✅","link":"","desc":"প্রতিদিন একবার"}
        ]
    }

def load_db():
    if not os.path.exists(DB):
        d=default_data()
        with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d
    try:
        with open(DB,'r',encoding='utf-8') as f: return json.load(f)
    except Exception:
        d=default_data()
        with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d

def save_db(d):
    with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","profile_img":"","balance":db["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":today,"phone":uid,"locked":True}
    u=db["users"][uid]
    if "phone" not in u: u["phone"]=uid
    if "locked" not in u: u["locked"]=True
    if "name" not in u: u["name"]=""
    if "profile_img" not in u: u["profile_img"]=""
    if "join_date" not in u: u["join_date"]=today
    if u.get("last")!=today:
        u["ads_today"]=0; u["popup_today"]=0; u["tasks_done"]=[]; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER_HTML)

@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only - Add?id=8807178385",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get')
def api_get():
    db=load_db(); uid=request.args.get('id','0'); u=get_user(db,uid); save_db(db)
    wds=[w for w in db.get("withdraws",[]) if w["uid"]==str(uid)]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":wds,"all_withdraws":db.get("withdraws",[]),"all_users":db["users"]})

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
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid); s=db["settings"]
    if tid in u["tasks_done"]: return jsonify({"msg":"আজকে করা হয়েছে"})
    if len(u["tasks_done"])>=s["task_limit"]: return jsonify({"msg":f"লিমিট {s['task_limit']} শেষ"})
    task=next((t for t in db["tasks"] if t["id"]==tid),None)
    if not task: return jsonify({"msg":"Task নেই"})
    u["tasks_done"].append(tid); u["balance"]+=task["reward"]; u["total"]+=1; save_db(db)
    return jsonify({"msg":f"✅ {task['title']} - ৳{task['reward']} যোগ"})

@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    if len(num) < 11: return jsonify({"msg":"সঠিক নাম্বার দিন"})
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
    for k in j:
        if k.startswith("google_ad"):
            try: idx=int(k[-1])-1; db["settings"]["google_ads"][idx]=j[k]
            except: pass
        elif k.startswith("task_"):
            try:
                parts=k.split('_'); tid=int(parts[1]); field='_'.join(parts[2:])
                for t in db["tasks"]:
                    if t["id"]==tid:
                        if field=='reward': t[field]=int(j[k])
                        else: t[field]=j[k]
            except: pass
        else: db["settings"][k]=j[k]
    save_db(db); return jsonify({"msg":"✅ Saved - সব Save হয়েছে"})

@app.route('/api/admin/balance',methods=['POST'])
def admin_balance():
    db=load_db(); j=request.json; uid=str(j.get('phone')); amt=int(j.get('amount',0)); typ=j.get('type','add')
    if uid not in db["users"]: return jsonify({"msg":"ইউজার পাওয়া যায়নি"})
    if typ=='add': db["users"][uid]["balance"]+=amt
    else: db["users"][uid]["balance"]-=amt;
    if db["users"][uid]["balance"]<0: db["users"][uid]["balance"]=0
    save_db(db); return jsonify({"msg":f"✅ {uid} তে {typ} {amt} TK সফল - New: {db['users'][uid]['balance']}"})

@app.route('/api/admin/upload',methods=['POST'])
def upload():
    db=load_db(); j=request.json
    if 'banner' in j:
        if len(db["settings"]["official_banners"])>=5: db["settings"]["official_banners"].pop(0)
        db["settings"]["official_banners"].append(j['banner']); save_db(db); return jsonify({"msg":f"✅ ব্যানার {len(db['settings']['official_banners'])}/5"})
    if 'clear_banner' in j: db["settings"]["official_banners"]=[]; save_db(db); return jsonify({"msg":"🗑️ মুছা হয়েছে"})
    return jsonify({"msg":"Error"})

USER_HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - A to Z Final</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:125px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,#17172a,#0e0e20);border:1px solid #222;position:relative;overflow:hidden}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;font-size:14px;color:#fff;margin-top:8px;cursor:pointer;background:linear-gradient(135deg,#6d4cff,#8b5cf6)}
.btn:disabled{opacity:.5}
.profile{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#1e293b,#334155);display:flex;align-items:center;justify-content:center;border:2px solid #6d4cff;overflow:hidden;font-size:26px;cursor:pointer}
.profile img{width:100%;height:100%;object-fit:cover}
.bannerBox{margin:12px;border-radius:22px;overflow:hidden;height:165px;background:linear-gradient(90deg,#f59e0b,#ef4444);position:relative;border:2px solid rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;text-align:center;padding:20px}
.page{display:none}.page.active{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.taskCard{display:flex;justify-content:space-between;align-items:center;background:#15152a;border:1px solid #2a2a4a;border-radius:14px;padding:12px;margin:10px 0}
.payCard{display:flex;align-items:center;gap:12px;background:#15152a;border:2px solid #2a2a4a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}.payCard.active{border-color:#e2136e;background:#1e1e3a}.payLogo{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:22px}
.bkash{background:#e2136e}.nagad{background:#f6921e}
#lockOverlay,#welcomeOverlay,#adOverlay{display:none;position:fixed;inset:0;z-index:999;justify-content:center;align-items:center;padding:20px}
#lockOverlay{display:flex;background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2)}#welcomeOverlay{background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2)}#adOverlay{background:#000e;flex-direction:column;color:#fff}
input{width:100%;padding:14px;border-radius:12px;border:1.5px solid #333;background:#0e0e20;color:#fff;margin-top:10px;outline:none}
</style></head><body>

<div class="top"><div><b id="appNameTop">💎 Protidiner Kaj BD</b><div style="font-size:11px;opacity:.7" id="lockInfoTop">Number Lock System</div></div><div class="profile" onclick="goPage('profile')" id="topProfile">👤</div></div>

<!-- NUMBER LOCK OVERLAY - PAGE 0 -->
<div id="lockOverlay">
<div style="background:#fff;color:#000;padding:26px;border-radius:22px;width:100%;max-width:360px;text-align:center">
<div style="font-size:50px">🔐</div><h2 style="color:#6d4cff;margin:6px 0">নাম্বার দিয়ে লক করুন</h2><p style="font-size:12px;color:#666">আপনার একাউন্ট সুরক্ষিত রাখতে নাম্বার দিন, OTP যাবে</p>
<input id="phoneInput" type="tel" placeholder="01XXXXXXXXX - 11 digit" maxlength="11" style="background:#f5f3ff;color:#000;border-color:#e9d5ff">
<button id="sendBtn" class="btn" onclick="sendOTP()">📲 OTP পাঠান</button>
<div id="otpSection" style="display:none"><input id="otpInput" type="text" placeholder="OTP দিন - ডেমো 1234" maxlength="4" style="background:#f5f3ff;color:#000;border-color:#e9d5ff"><button class="btn" onclick="verifyOTP()">✅ ভেরিফাই করুন</button><p style="font-size:11px;color:#888;margin-top:6px">ডেমো OTP: 1234 - পরে SMS API লাগবে</p></div>
<p style="font-size:10px;color:#999;margin-top:10px">এক নাম্বারে এক ID • অন্য কেউ ঢুকতে পারবে না</p>
</div>
</div>

<!-- WELCOME 1120 BONUS POPUP -->
<div id="welcomeOverlay">
<div style="background:#fff;color:#000;padding:26px;border-radius:22px;width:100%;max-width:360px;text-align:center;box-shadow:0 20px 40px #0004">
<div style="font-size:62px">🎉</div><h2 style="color:#6d4cff">স্বাগতম!</h2><p style="font-size:13px;color:#666">Protidiner Kaj BD তে আপনাকে স্বাগতম</p>
<div id="bonusBox" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:16px;font-size:32px;font-weight:800;margin:14px 0">1120 TK বোনাস 💰</div>
<p style="font-size:11px;color:#666">আপনি <b id="bonusText">1120 TK</b> Welcome Bonus পেয়েছেন<br>নাম্বার <b id="welcomePhone"></b> এর সাথে ID Lock হয়েছে</p>
<button class="btn" onclick="closeWelcome()">🚀 কাজ শুরু করুন</button>
</div>
</div>

<!-- PAGE 1 HOME -->
<div id="p-home" class="page active">
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5)"><div style="font-size:12px;opacity:.9" id="balanceTitle">আপনার বর্তমান ব্যালেন্স</div><div style="font-size:36px;font-weight:800" id="balMain">0 TK</div><div style="font-size:11px;background:#fff2;padding:4px 10px;border-radius:20px;display:inline-block;margin-top:6px" id="uidShow">ID: -</div><div style="font-size:11px;margin-top:4px" id="lockedShow">🔒 Locked: -</div></div>
<div class="bannerBox" id="mainBanner"><div><h3 id="offerTitle">🎉 আজকের স্পেশাল অফার</h3><p id="offerDesc" style="font-size:12px;margin-top:6px">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</p></div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><h3>🎬 Company Ads</h3><span style="font-size:11px;background:#fef3c7;color:#000;padding:4px 8px;border-radius:8px" id="adRewardTxt">2 TK / Ad</span></div><button class="btn" onclick="watchAd('company')">▶️ বিজ্ঞাপন দেখুন ও <span class="adR">2</span> TK নিন</button><div style="background:#222;height:10px;border-radius:20px;margin-top:14px;overflow:hidden"><div id="adProg" style="background:#6d4cff;height:100%;width:100%"></div></div><p id="adText" style="text-align:right;font-size:12px;color:#aaa;margin-top:6px">0/30</p></div>
<div class="card"><h3>📢 Google Popup Ads</h3><button class="btn" style="background:#0ea5e9" onclick="watchAd('popup')">👁️ Popup Ad দেখুন ও <span class="popR">3</span> TK নিন</button><p id="popText" style="text-align:right;font-size:12px;color:#aaa;margin-top:6px">0/20</p></div>
<div class="card"><h3>🔗 রেফার লিংক - 10 TK পাবেন</h3><div id="refLink" style="background:#0e0e20;border:1px dashed #6d4cff;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:12px;margin-top:8px"></div><div style="display:flex;gap:8px;margin-top:10px"><button class="btn" style="background:#fbbf24;color:#000;flex:1" onclick="copyRef()">📋 কপি</button><button class="btn" style="background:#0ea5e9;flex:1" onclick="shareRef()">📤 শেয়ার</button></div></div>
</div>

<!-- PAGE 2 TASKS -->
<div id="p-tasks" class="page"><div class="card"><h3>🎯 Page 2 - ডেইলি টাস্ক - 5 টা</h3><div id="taskList"></div></div></div>

<!-- PAGE 3 INVITE -->
<div id="p-invite" class="page"><div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);text-align:center"><h1 style="font-size:48px">50 TK</h1><p>Page 3 - প্রতি রেফারে</p><div id="refLink2" style="background:#fff2;padding:12px;border-radius:12px;margin-top:14px;font-size:12px;word-break:break-all"></div><button class="btn" style="background:#fff;color:#6d28d9" onclick="copyRef()">Invite লিংক কপি করুন</button></div><div class="card"><h3>📊 আপনার Invite</h3><div style="display:flex;gap:8px;margin-top:12px"><div style="background:#15152a;padding:14px;border-radius:14px;flex:1;text-align:center"><div id="myRef" style="font-size:22px;font-weight:800">0</div><div style="font-size:11px">জন</div></div><div style="background:#15152a;padding:14px;border-radius:14px;flex:1;text-align:center"><div id="myRefTk" style="font-size:22px;font-weight:800">0 TK</div><div style="font-size:11px">আয়</div></div></div></div></div>

<!-- PAGE 4 WALLET -->
<div id="p-wallet" class="page"><div class="card" style="text-align:center"><div style="font-size:12px;color:#aaa">Page 4 - Wallet</div><h1 id="bal2" style="font-size:38px;color:#6d4cff">0 TK</h1><div style="font-size:11px;background:#dcfce7;color:#166534;padding:4px 12px;border-radius:20px;display:inline-block">✓ Locked: <span id="lockedNumShow">-</span> • Min <span id="minWith">500</span> TK</div></div><div class="card"><h3>🏦 টাকা তুলুন - bKash Nagad Fixed</h3><div id="bkashOpt" class="payCard active" onclick="selectMethod('bKash')"><div class="payLogo bkash">bKash</div><div style="flex:1"><b>bKash Personal</b><div style="font-size:11px;color:#aaa">লক নাম্বারে যাবে</div></div><div>✓</div></div><div id="nagadOpt" class="payCard" onclick="selectMethod('Nagad')"><div class="payLogo nagad">নগদ</div><div style="flex:1"><b>Nagad Personal</b><div style="font-size:11px;color:#aaa">লক নাম্বারে যাবে</div></div></div><input id="accNum" placeholder="লক নাম্বার অটো বসবে" readonly><input id="amount" type="number" placeholder="Amount"><button class="btn" onclick="doWithdraw()">💸 Withdraw করুন</button><div id="withdrawHistory" style="margin-top:12px"></div></div></div>

<!-- PAGE 5 PROFILE -->
<div id="p-profile" class="page"><div class="card" style="text-align:center"><div style="width:100px;height:100px;border-radius:50%;background:#1e293b;display:flex;align-items:center;justify-content:center;border:3px solid #6d4cff;margin:0 auto;overflow:hidden;font-size:44px;position:relative" id="profileBig" onclick="document.getElementById('fileInput').click()"><span id="profileEmoji">👤</span><img id="profileImg" style="display:none;width:100%;height:100%;object-fit:cover"><div style="position:absolute;bottom:2px;right:2px;background:#6d4cff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center">📷</div></div><input type="file" id="fileInput" accept="image/*" style="display:none"><h2 id="uName" style="margin-top:10px">User</h2><p style="font-size:12px;color:#aaa">ID: <span id="uidShow2">-</span> • <span id="joinDate">-</span></p><div style="background:#15152a;padding:10px;border-radius:12px;margin-top:10px;font-size:12px;text-align:left"><b>🔒 Locked:</b> <span id="profilePhone">-</span><br><b>💰 Balance:</b> <span id="profileBal">0 TK</span><br><b>🎁 Bonus:</b> <span id="profileBonus">1120 TK</span></div><div style="display:flex;gap:8px;margin-top:10px"><input id="editName" placeholder="নতুন নাম"><button class="btn" style="width:auto;padding:12px 18px" onclick="saveProfile()">Save</button></div></div><div class="card"><h3>💬 Support</h3><button class="btn" style="background:#0ea5e9" onclick="openSupport()">📩 Telegram Support</button><p style="font-size:11px;color:#aaa;margin-top:8px">Tutorial: <a id="tutorialLink" href="#" target="_blank" style="color:#6d4cff">YouTube Video</a></p></div></div>

<div id="adOverlay"><h2>⏳ বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:64px;font-weight:800;margin:10px 0">15</div><p>15 সেকেন্ড দেখুন, তাহলেই টাকা পাবেন</p><div style="background:#fff3;width:80%;height:8px;border-radius:20px;margin-top:12px;overflow:hidden"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div></div>

<div class="btm"><div id="nav-home" class="on" onclick="goPage('home')"><span>🏠</span>Page 1<br>Home</div><div id="nav-tasks" onclick="goPage('tasks')"><span>🎯</span>Page 2<br>Tasks</div><div id="nav-invite" onclick="goPage('invite')"><span>👥</span>Page 3<br>Invite</div><div id="nav-wallet" onclick="goPage('wallet')"><span>💰</span>Page 4<br>Wallet</div><div id="nav-profile" onclick="goPage('profile')"><span>👤</span>Page 5<br>Profile</div></div>

<script>
let uid=localStorage.getItem('locked_phone')||''; let lockedPhone=uid; let settings={}; let user={}; let selected='bKash';
function initApp(){ if(!uid){ document.getElementById('lockOverlay').style.display='flex'; return; } document.getElementById('lockOverlay').style.display='none'; fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ settings=d.settings; user=d.user; document.getElementById('appNameTop').innerText='💎 '+settings.app_name; document.getElementById('balanceTitle').innerText=settings.balance_title; document.getElementById('offerTitle').innerText=settings.offer_title; document.getElementById('offerDesc').innerText=settings.offer_desc; document.getElementById('balMain').innerText=user.balance+' TK'; document.getElementById('bal2').innerText=user.balance+' TK'; document.getElementById('profileBal').innerText=user.balance+' TK'; document.getElementById('profileBonus').innerText=settings.bonus+' TK'; document.getElementById('bonusBox').innerText=settings.bonus+' TK বোনাস 💰'; document.getElementById('bonusText').innerText=settings.bonus+' TK'; document.getElementById('adRewardTxt').innerText=settings.ad_reward+' TK / Ad'; document.querySelectorAll('.adR').forEach(e=>e.innerText=settings.ad_reward); document.querySelectorAll('.popR').forEach(e=>e.innerText=settings.popup_reward); document.getElementById('minWith').innerText=settings.min_with; document.getElementById('adProg').style.width=( (settings.company_limit - user.ads_today)/settings.company_limit*100 )+'%'; document.getElementById('adText').innerText=user.ads_today+'/'+settings.company_limit; document.getElementById('popText').innerText=user.popup_today+'/'+settings.popup_limit; document.getElementById('uidShow').innerText='ID: '+uid.slice(-4)+' • Total: '+user.total; document.getElementById('uidShow2').innerText=uid; document.getElementById('joinDate').innerText=user.join_date; document.getElementById('lockedShow').innerText='🔒 Locked: '+uid; document.getElementById('lockedNumShow').innerText=uid; document.getElementById('profilePhone').innerText=uid; document.getElementById('welcomePhone').innerText=uid; document.getElementById('accNum').value=uid; document.getElementById('uName').innerText=user.name||'User '+uid.slice(-4); document.getElementById('editName').value=user.name||''; if(user.profile_img){ document.getElementById('profileImg').src=user.profile_img; document.getElementById('profileImg').style.display='block'; document.getElementById('profileEmoji').style.display='none'; } let link='https://t.me/'+window.location.hostname+'?start='+uid; document.getElementById('refLink').innerText=link; document.getElementById('refLink2').innerText=link; let tHtml=''; d.tasks.forEach(t=>{ let done=user.tasks_done.includes(t.id); tHtml+=`<div class="taskCard"><div><b>${t.icon} ${t.title}</b><div style="font-size:11px;color:#aaa">${t.desc} - ৳${t.reward}</div></div><button class="btn" style="width:auto;padding:8px 14px;background:${done?'#10b981':'#6d4cff'}" onclick="doTask(${t.id})" ${done?'disabled':''}>${done?'✓ Done':'৳'+t.reward}</button></div>`; }); document.getElementById('taskList').innerHTML=tHtml; let wh=''; d.withdraws.slice(-5).reverse().forEach(w=>{ wh+=`<div style="background:#15152a;padding:10px;border-radius:10px;margin-top:6px;font-size:12px">💸 ${w.method} ৳${w.amount} - ${w.status} - ${w.time}</div>`; }); document.getElementById('withdrawHistory').innerHTML=wh||'<p style="font-size:11px;color:#666">কোন Withdraw নেই</p>'; if(!localStorage.getItem('welcomed_'+uid)){ document.getElementById('welcomeOverlay').style.display='flex'; } }); }

function sendOTP(){ let p=document.getElementById('phoneInput').value; if(p.length!=11||!p.startsWith('01')){ alert('সঠিক 11 ডিজিট নাম্বার দিন'); return; } alert('✅ OTP পাঠানো হয়েছে: 1234\\nNumber: '+p); document.getElementById('otpSection').style.display='block'; document.getElementById('sendBtn').innerText='🔁 আবার পাঠান'; }
function verifyOTP(){ let o=document.getElementById('otpInput').value; let p=document.getElementById('phoneInput').value; if(o!='1234'){ alert('ভুল OTP! 1234 দিন'); return; } localStorage.setItem('locked_phone',p); uid=p; lockedPhone=p; document.getElementById('lockOverlay').style.display='none'; document.getElementById('welcomePhone').innerText=p; fetch('/api/get?id='+p).then(()=>{ initApp(); document.getElementById('welcomeOverlay').style.display='flex'; }); }
function closeWelcome(){ document.getElementById('welcomeOverlay').style.display='none'; localStorage.setItem('welcomed_'+uid,'1'); }
function goPage(p){ document.querySelectorAll('.page').forEach(e=>e.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on')); document.getElementById('nav-'+p).classList.add('on'); window.scrollTo(0,0); }
function watchAd(type){ if(!uid){ alert('আগে Lock করুন'); return; } document.getElementById('adOverlay').style.display='flex'; let t=15; document.getElementById('timer').innerText=t; let ti=setInterval(()=>{ t--; document.getElementById('timer').innerText=t; document.getElementById('timerProg').style.width=(t/15*100)+'%'; if(t<=0){ clearInterval(ti); document.getElementById('adOverlay').style.display='none'; fetch('/api/reward?id='+uid+'&type='+type).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); }); } },1000); if(typeof show_11764581==='function'){ show_11764581().then(()=>{}).catch(()=>{}); } }
function doTask(id){ fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); }); }
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('✅ কপি হয়েছে'); }
function shareRef(){ let l=document.getElementById('refLink').innerText; if(navigator.share){ navigator.share({title:'Join',text:l,url:l}); } else copyRef(); }
function selectMethod(m){ selected=m; document.getElementById('bkashOpt').classList.toggle('active',m==='bKash'); document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad'); }
function doWithdraw(){ let n=document.getElementById('accNum').value; let a=document.getElementById('amount').value; if(!n||!a){ alert('Number ও Amount দিন'); return; } fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,amount:a,method:selected})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); }); }
function openSupport(){ window.open(settings.support_link,'_blank'); }
document.getElementById('fileInput').addEventListener('change',function(e){ let f=e.target.files[0]; let r=new FileReader(); r.onload=function(ev){ let img=ev.target.result; fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,profile_img:img})}).then(()=>{ document.getElementById('profileImg').src=img; document.getElementById('profileImg').style.display='block'; document.getElementById('profileEmoji').style.display='none'; alert('✅ ছবি আপডেট'); }); }; r.readAsDataURL(f); });
function saveProfile(){ let nm=document.getElementById('editName').value; fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:nm})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); }); }
initApp();
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin Panel - A to Z</title><style>*{box-sizing:border-box;font-family:system-ui}body{background:#070710;color:#fff;max-width:800px;margin:0 auto;padding:20px}.card{background:#17172a;border:1px solid #222;border-radius:16px;padding:16px;margin:12px 0} input,textarea{width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:8px}.btn{padding:12px 18px;border:none;border-radius:10px;font-weight:800;cursor:pointer;background:linear-gradient(135deg,#6d4cff,#8b5cf6);color:#fff;margin-top:8px} table{width:100%;border-collapse:collapse;margin-top:10px} th,td{border:1px solid #333;padding:8px;font-size:12px;text-align:left} th{background:#0e0e20}</style></head><body>
<h2>👑 Admin Dashboard - A to Z Full Control - Number Lock System</h2>
<div class="card"><h3>⚙️ Settings - Bonus Control - আপনি টাকা যোগ করতে পারবেন</h3><div id="settingsForm"></div><button class="btn" onclick="saveSettings()">💾 Save All Settings</button><p style="font-size:11px;color:#aaa;margin-top:6px">Bonus 1120 চেঞ্জ করলে নতুন ইউজার ওই বোনাস পাবে</p></div>
<div class="card"><h3>💸 Balance Add/Minus - যেন আপনি টাকা যোগ করতে পারেন</h3><input id="admPhone" placeholder="Phone Number - 01XXXXXXXXX"><input id="admAmount" type="number" placeholder="Amount"><div style="display:flex;gap:8px"><button class="btn" style="background:#10b981" onclick="admBal('add')">+ যোগ করুন</button><button class="btn" style="background:#ef4444" onclick="admBal('minus')">- মাইনাস করুন</button></div><div id="admMsg" style="margin-top:8px;font-size:12px"></div></div>
<div class="card"><h3>👥 All Users - নাম্বার দিয়ে লকিং লিস্ট</h3><div id="userList"></div></div>
<div class="card"><h3>💰 Withdraw Requests</h3><div id="withdrawList"></div></div>
<script>
let db={};
function load(){ fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{ db=d; let s=d.settings; let html=''; html+=`App Name: <input id="app_name" value="${s.app_name}"><br>Bonus (Welcome): <input id="bonus" type="number" value="${s.bonus}"><br>Ad Reward: <input id="ad_reward" type="number" value="${s.ad_reward}"><br>Popup Reward: <input id="popup_reward" type="number" value="${s.popup_reward}"><br>Min Withdraw: <input id="min_with" type="number" value="${s.min_with}"><br>Company Limit: <input id="company_limit" type="number" value="${s.company_limit}"><br>Popup Limit: <input id="popup_limit" type="number" value="${s.popup_limit}"><br>Offer Title: <input id="offer_title" value="${s.offer_title}"><br>Offer Desc: <textarea id="offer_desc">${s.offer_desc}</textarea>`; document.getElementById('settingsForm').innerHTML=html; let uhtml='<table><tr><th>Phone (Locked ID)</th><th>Name</th><th>Balance</th><th>Ads</th><th>Join</th></tr>'; Object.values(d.all_users).forEach(u=>{ uhtml+=`<tr><td>${u.phone||u.id}</td><td>${u.name}</td><td>${u.balance} TK</td><td>${u.ads_today}</td><td>${u.join_date}</td></tr>`; }); uhtml+='</table>'; document.getElementById('userList').innerHTML=uhtml; let whtml='<table><tr><th>Phone</th><th>Amount</th><th>Method</th><th>Number</th><th>Status</th><th>Time</th></tr>'; d.all_withdraws.slice(-50).reverse().forEach(w=>{ whtml+=`<tr><td>${w.uid}</td><td>${w.amount}</td><td>${w.method}</td><td>${w.number}</td><td>${w.status}</td><td>${w.time}</td></tr>`; }); whtml+='</table>'; document.getElementById('withdrawList').innerHTML=whtml; }); }
function saveSettings(){ let data={}; document.querySelectorAll('#settingsForm input, #settingsForm textarea').forEach(e=>{ data[e.id]=e.value; }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>alert(d.msg)); }
function admBal(type){ let p=document.getElementById('admPhone').value; let a=document.getElementById('admAmount').value; if(!p||!a){ alert('Phone ও Amount দিন'); return; } fetch('/api/admin/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:p,amount:a,type:type})}).then(r=>r.json()).then(d=>{ document.getElementById('admMsg').innerText=d.msg; alert(d.msg); load(); }); }
load();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
