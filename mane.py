# -*- coding: utf-8 -*-
# FINAL A-Z - ALL + MITMIT BLINK - 2 BOXES - EXACT LIKE SCREENSHOT
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
            "nagad_name":"Nagad",
            "zone":"11764581",
            "support_link":"https://t.me/",
            "tutorial_link":"https://youtube.com/"
        },
        "tasks":[
            {"id":1,"title":"Telegram Channel Join","bn":"চ্যানেলে জয়েন করুন","reward":25,"icon":"✈️","color":"#3b82f6"},
            {"id":2,"title":"YouTube Subscribe","bn":"সাবস্ক্রাইব + লাইক","reward":30,"icon":"▶️","color":"#f59e0b"},
            {"id":3,"title":"Facebook Page Like","bn":"পেজে লাইক দিন","reward":20,"icon":"👍","color":"#facc15"},
            {"id":4,"title":"Refer Friend","bn":"১ জন রেফার = ৳50","reward":50,"icon":"👥","color":"#fff"},
            {"id":5,"title":"Daily Check-in","bn":"প্রতিদিন একবার","reward":15,"icon":"✅","color":"#22c55e"}
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
                db["settings"]["bkash_logo"]=""; db["settings"]["nagad_logo"]=""
                db["settings"]["bkash_name"]="bKash"; db["settings"]["nagad_name"]="Nagad"
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
    if u.get("last")!=today: u["ads_today"]=0; u["popup_today"]=0; u["tasks_done"]=[]; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only?id=8807178385",403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get')
def api_get():
    db=load_db(); uid=request.args.get('id','0'); u=get_user(db,uid); save_db(db)
    wds=[w for w in db["withdraws"] if w["uid"]==str(uid)]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":wds,"all_withdraws":db["withdraws"],"all_users":db["users"]})
@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id')); typ=request.args.get('type','company'); s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":"লিমিট শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":"লিমিট শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save_db(db); return jsonify({"msg":f"৳{s['ad_reward'] if typ=='company' else s['popup_reward']} যোগ"})
@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid)
    if tid in u["tasks_done"]: return jsonify({"msg":"করা হয়েছে"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    u["tasks_done"].append(tid); u["balance"]+=t["reward"]; u["total"]+=1; save_db(db)
    return jsonify({"msg":f"✅ {t['title']} ৳{t['reward']}"})
@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']}"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"status":"Pending","time":str(datetime.now())[:16]})
    save_db(db); return jsonify({"msg":f"✅ {method} ৳{amt} Request"})
@app.route('/api/user/update',methods=['POST'])
def user_update():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid)
    if 'name' in j and j['name']: u["name"]=str(j['name'])[:25]
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save_db(db); return jsonify({"msg":"✅ সেভ হয়েছে"})
@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db(); j=request.json
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ Save হয়েছে"})
@app.route('/api/admin/balance',methods=['POST'])
def admin_balance():
    db=load_db(); j=request.json; uid=str(j.get('phone')); amt=int(j.get('amount',0)); typ=j.get('type','add')
    if uid not in db["users"]: return jsonify({"msg":"ইউজার নেই"})
    if typ=='add': db["users"][uid]["balance"]+=amt
    else: db["users"][uid]["balance"]-=amt
    if db["users"][uid]["balance"]<0: db["users"][uid]["balance"]=0
    save_db(db); return jsonify({"msg":f"✅ {uid} {typ} {amt} - New {db['users'][uid]['balance']}"})

USER_HTML = """<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#0a0a14;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}
.top{padding:12px 16px;display:flex;justify-content:space-between;align-items:center;background:#0f0f1e;position:sticky;top:0;z-index:99;border-bottom:1px solid #1a1a2e}
.card{margin:12px;border-radius:20px;padding:14px;background:#15152a;border:1px solid #23233a;position:relative;overflow:hidden}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;margin-top:8px;cursor:pointer}
.page{display:none}.page.active{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;padding:8px 0 10px;border-radius:20px 20px 0 0;border-top:1px solid #23233a;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:700;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
#lockOverlay,#welcomeOverlay,#adOverlay{position:fixed;inset:0;z-index:999;display:none;justify-content:center;align-items:center;padding:20px}
#lockOverlay{display:flex;background:#0a0a14f2}#welcomeOverlay{background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2)}#adOverlay{background:#000e;flex-direction:column;color:#fff}
input{width:100%;padding:14px;border-radius:12px;border:1px solid #2a2a4a;background:#0e0e20;color:#fff;margin-top:8px}
.taskItem{display:flex;justify-content:space-between;align-items:center;background:#0e0e20;border:1px solid #23233a;border-radius:14px;padding:12px;margin:10px 0}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #2a2a4a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.payCard.active{border-color:#e2136e;background:#1e1e3a}.payLogo{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:22px;overflow:hidden;background:#333}.payLogo img{width:100%;height:100%;object-fit:cover}
.statBox{background:#0e0e20;border:1px solid #23233a;border-radius:14px;padding:12px;text-align:center;flex:1}
/* --- মিটমিট 2 বক্স --- */
.blinkBox{animation:mitmit 1.2s infinite;border:2px solid #6d4cff!important}
@keyframes mitmit{0%{box-shadow:0 0 5px #6d4cff,0 0 10px #6d4cff88;transform:scale(1)}50%{box-shadow:0 0 20px #6d4cff,0 0 35px #06b6d4,0 0 50px #6d4cff88;transform:scale(1.02);border-color:#06b6d4!important}100%{box-shadow:0 0 5px #6d4cff,0 0 10px #6d4cff88;transform:scale(1)}}
.blinkBox2{animation:mitmit2 1.2s infinite 0.6s;border:2px solid #f59e0b!important}
@keyframes mitmit2{0%{box-shadow:0 0 5px #f59e0b,0 0 10px #f59e0b88;transform:scale(1)}50%{box-shadow:0 0 20px #f59e0b,0 0 35px #ef4444,0 0 50px #f59e0b88;transform:scale(1.02);border-color:#ef4444!important}100%{box-shadow:0 0 5px #f59e0b,0 0 10px #f59e0b88;transform:scale(1)}}
</style></head><body>
<div class="top"><div style="display:flex;align-items:center;gap:10px"><div style="font-size:32px">👑</div><div><div style="font-weight:800;display:flex;align-items:center;gap:6px">Protidiner Kaj BD <span style="background:#10b981;color:#fff;font-size:12px;padding:2px 6px;border-radius:6px">✓</span></div><div style="font-size:11px;color:#aaa">Admin: SHIBLI NOMAN</div></div></div><div style="width:52px;height:52px;border-radius:50%;border:2px solid #6d4cff;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden;font-size:28px" id="topAv">👤</div></div>
<div id="lockOverlay"><div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:360px;text-align:center"><div style="font-size:44px">🔐</div><h2 style="color:#6d4cff;margin:6px 0">নাম্বার দিয়ে লক করুন</h2><p style="font-size:13px;font-weight:800;color:#000">নাম্বার দিয়ে লক করুন, নাম্বার দিয়ে লগইন করুন</p><p style="font-size:11px;color:#666;margin-top:4px">এক নাম্বারে এক ID • অন্য কেউ ঢুকতে পারবে না</p><input id="phoneInput" type="tel" placeholder="01XXXXXXXXX" maxlength="11" style="background:#f5f3ff;color:#000"><button class="btn" style="background:linear-gradient(135deg,#6d4cff,#8b5cf6)" onclick="sendOTP()">📲 OTP পাঠান</button><div id="otpSection" style="display:none"><input id="otpInput" type="text" placeholder="OTP 1234" maxlength="4" style="background:#f5f3ff;color:#000"><button class="btn" style="background:#10b981" onclick="verifyOTP()">✅ ভেরিফাই</button></div></div></div>
<div id="welcomeOverlay"><div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:360px;text-align:center"><div style="font-size:56px">🎉</div><h2 style="color:#6d4cff">স্বাগতম!</h2><div id="bonusBox" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:14px;border-radius:14px;font-size:28px;font-weight:800;margin:12px 0">1120 TK বোনাস 💰</div><p style="font-size:11px;color:#666">আপনি <b id="bonusText">1120 TK</b> বোনাস পেয়েছেন<br>নাম্বার <b id="welcomePhone"></b> লক হয়েছে</p><button class="btn" style="background:linear-gradient(135deg,#6d4cff,#8b5cf6)" onclick="closeWelcome()">🚀 কাজ শুরু করুন</button></div></div>
<div id="adOverlay"><h2>⏳ বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:64px;font-weight:800">15</div><p>15 সেকেন্ড দেখুন</p><div style="background:#fff3;width:80%;height:8px;border-radius:20px;margin-top:12px;overflow:hidden"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div></div>
<div id="p-home" class="page active">
<div class="blinkBox2" style="margin:12px;border-radius:20px;height:140px;background:linear-gradient(90deg,#f59e0b,#ef4444);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:18px">🎉 Daily Bonus Available Today - ছবি বক্স মিটমিট</div>
<div class="card blinkBox" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4);border:none;text-align:center"><div style="font-size:12px;opacity:.9">💰 আপনার বর্তমান ব্যালেন্স - মিটমিট করবে</div><div style="font-size:42px;font-weight:900;margin:6px 0" id="balMain">৳1120</div><div style="display:flex;gap:8px;justify-content:center;margin-top:10px"><span style="background:#0003;padding:6px 12px;border-radius:20px;font-size:12px" id="compChip">Company 0/30</span><span style="background:#0003;padding:6px 12px;border-radius:20px;font-size:12px" id="popChip">Popup 0/20</span><span style="background:#0003;padding:6px 12px;border-radius:20px;font-size:12px" id="totalChip">Total 0</span></div></div>
<div class="card" style="padding:10px"><button class="btn" style="background:linear-gradient(90deg,#7c3aed,#4f46e5)" onclick="watchAd('company')" id="companyBtn">📺 COMPANY ADS (৳2) - 0/30</button><button class="btn" style="background:#10b981" onclick="watchAd('popup')" id="popupBtn">💰 POPUP ADS (৳3) - 0/20</button><button class="btn" style="background:#1e293b;border:1px solid #334155" onclick="goPage('tasks')">📋 TASK BONUS - 5 টা/দিন</button></div>
<div class="card" style="border:1.5px solid #f59e0b"><h3>🎉 আজকের স্পেশাল অফার</h3><p style="font-size:12px;color:#aaa;margin-top:6px">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</p></div>
</div>
<div id="p-tasks" class="page"><div class="card"><h3>📋 Task Bonus - দিনে 5 টা</h3><div id="taskList"></div><div style="margin-top:16px;background:linear-gradient(135deg,#6d4cff,#4f46e5);border-radius:18px;padding:16px"><h3>🎁 Refer & Earn ৳50</h3><div id="refLink" style="background:#0003;padding:10px;border-radius:10px;font-size:11px;word-break:break-all;margin-top:8px"></div><button class="btn" style="background:#fff;color:#6d4cff;margin-top:10px" onclick="copyRef()">📋 লিংক কপি</button></div></div></div>
<div id="p-wallet" class="page"><div class="card"><h3>💸 Withdraw Method - Logo Admin থেকে চেঞ্জ হবে</h3><div id="bkashOpt" class="payCard active" onclick="selectMethod('bKash')"><div class="payLogo" style="background:#e2136e"><img id="bkashImg" src="" style="display:none"><span id="bkashTxt">৳</span></div><div style="flex:1"><b id="bkashName">bKash</b><div style="font-size:11px;color:#aaa">Personal • Instant</div></div><div style="color:#10b981;font-size:20px">✓</div></div><div id="nagadOpt" class="payCard" onclick="selectMethod('Nagad')"><div class="payLogo" style="background:#f6921e"><img id="nagadImg" src="" style="display:none"><span id="nagadTxt">৳</span></div><div style="flex:1"><b id="nagadName">Nagad</b><div style="font-size:11px;color:#aaa">Personal • Fast</div></div></div><input id="accNum" placeholder="01XXXXXXXXX" readonly><input id="amount" type="number" placeholder="500"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f59e0b)" onclick="doWithdraw()">🚀 Withdraw করুন</button></div><div class="card" style="background:linear-gradient(135deg,#065f46,#047857)"><h3>✅ Withdraw নিয়ম</h3><div style="font-size:13px;margin-top:8px">- মিনিমাম ৳500<br>- Personal নাম্বার<br>- 24 ঘণ্টায় পেমেন্ট</div></div><div class="card"><h3>📜 History</h3><div id="wHistory" style="font-size:12px;color:#aaa">কোনো Withdraw নেই</div></div></div>
<div id="p-support" class="page"><div class="card"><h3>🎬 কিভাবে কাজ করবেন?</h3><div style="margin-top:10px;background:#000;border:1.5px solid #f59e0b;border-radius:16px;height:160px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div style="width:80px;height:80px;background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:36px">▶️</div><div style="background:#f59e0b;color:#fff;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:800;margin-top:10px">Tutorial - 2 মিনিটে শিখুন</div></div></div><div class="card"><h3>❓ FAQ</h3><div class="taskItem"><div><b>Q: টাকা কখন পাবো?</b><div style="font-size:11px;color:#aaa">A: 24 ঘণ্টায়</div></div></div></div></div>
<div id="p-profile" class="page"><div class="card blinkBox" style="text-align:center"><div style="width:110px;height:110px;border-radius:50%;border:3px solid #6d4cff;margin:0 auto;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden;font-size:50px;position:relative"><span id="profileEmoji">👤</span><img id="profileImg" style="display:none;width:100%;height:100%;object-fit:cover"></div><h2 id="uName" style="margin-top:12px">User 8385</h2><p style="font-size:11px;color:#aaa">ID: <span id="uidShow">8807178385</span></p><div style="background:#6d4cff;color:#fff;padding:6px 14px;border-radius:20px;display:inline-block;font-size:12px;margin-top:8px">🏅 Bronze Member</div><input id="editName" placeholder="আপনার নাম" style="margin-top:14px;text-align:center"><button class="btn" style="background:#10b981" onclick="saveProfile()">💾 Save Profile</button></div><div class="card blinkBox2"><h3>📊 পরিসংখ্যান - মিটমিট</h3><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px"><div class="statBox"><div style="font-size:18px;font-weight:800" id="statBal">৳1120</div><div style="font-size:10px;color:#aaa">ব্যালেন্স</div></div><div class="statBox"><div style="font-size:18px;font-weight:800" id="statAds">0</div><div style="font-size:10px;color:#aaa">Ads</div></div><div class="statBox"><div style="font-size:18px;font-weight:800" id="statTask">0</div><div style="font-size:10px;color:#aaa">Task</div></div></div></div><div class="card"><h3>⚙️ সেটিংস</h3><div class="taskItem" onclick="goPage('wallet')"><div>💸 Withdraw History</div><div>➡️</div></div><div class="taskItem" onclick="copyRef()"><div>🔗 My Refer Link<div style="font-size:10px;color:#aaa" id="refLink2">https://...</div></div><div>📋</div></div></div></div>
<div class="btm"><div id="nav-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div><div id="nav-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div><div id="nav-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div><div id="nav-support" onclick="goPage('support')"><span>💬</span>Support</div><div id="nav-profile" onclick="goPage('profile')"><span>👤</span>Profile</div></div>
<script>
let uid=localStorage.getItem('locked_phone')||'8807178385';let selected='bKash';let settings={};
function initApp(){if(!uid){document.getElementById('lockOverlay').style.display='flex';return;}document.getElementById('lockOverlay').style.display='none';fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{settings=d.settings;let u=d.user;document.getElementById('balMain').innerText='৳'+u.balance;document.getElementById('statBal').innerText='৳'+u.balance;document.getElementById('uidShow').innerText=u.phone;document.getElementById('accNum').value=u.phone;document.getElementById('welcomePhone').innerText=u.phone;document.getElementById('bonusBox').innerText=settings.bonus+' TK বোনাস 💰';document.getElementById('bonusText').innerText=settings.bonus+' TK';document.getElementById('compChip').innerText='Company '+u.ads_today+'/'+settings.company_limit;document.getElementById('popChip').innerText='Popup '+u.popup_today+'/'+settings.popup_limit;document.getElementById('totalChip').innerText='Total '+u.total;document.getElementById('companyBtn').innerText='📺 COMPANY ADS (৳'+settings.ad_reward+') - '+u.ads_today+'/'+settings.company_limit;document.getElementById('popupBtn').innerText='💰 POPUP ADS (৳'+settings.popup_reward+') - '+u.popup_today+'/'+settings.popup_limit;document.getElementById('bkashName').innerText=settings.bkash_name;document.getElementById('nagadName').innerText=settings.nagad_name;if(settings.bkash_logo && settings.bkash_logo.startsWith('http')){document.getElementById('bkashImg').src=settings.bkash_logo;document.getElementById('bkashImg').style.display='block';document.getElementById('bkashTxt').style.display='none';}if(settings.nagad_logo && settings.nagad_logo.startsWith('http')){document.getElementById('nagadImg').src=settings.nagad_logo;document.getElementById('nagadImg').style.display='block';document.getElementById('nagadTxt').style.display='none';}document.getElementById('uName').innerText=u.name;document.getElementById('statAds').innerText=u.ads_today;document.getElementById('statTask').innerText=u.tasks_done.length;document.getElementById('refLink').innerText=window.location.origin+'/?ref='+uid;document.getElementById('refLink2').innerText=window.location.origin+'/?ref='+uid;let tHtml='';d.tasks.forEach(t=>{let done=u.tasks_done.includes(t.id);tHtml+=`<div class="taskItem"><div><b>${t.icon} ${t.title}</b><div style="font-size:11px;color:#aaa">${t.bn}</div></div><button class="btn" style="width:auto;padding:8px 16px;background:${done?'#10b981':'#6d4cff'}" onclick="doTask(${t.id})">${done?'✓':t.reward+' TK'}</button></div>`;});document.getElementById('taskList').innerHTML=tHtml;let wh='';d.withdraws.slice(-5).reverse().forEach(w=>{wh+=`<div style="background:#0e0e20;padding:10px;border-radius:10px;margin-top:6px">💸 ${w.method} ৳${w.amount} - ${w.status}</div>`;});if(wh)document.getElementById('wHistory').innerHTML=wh;if(!localStorage.getItem('welcomed_'+uid)){document.getElementById('welcomeOverlay').style.display='flex';}});}
function sendOTP(){let p=document.getElementById('phoneInput').value;if(p.length!=11||!p.startsWith('01')){alert('সঠিক নাম্বার');return;}alert('OTP: 1234');document.getElementById('otpSection').style.display='block';}
function verifyOTP(){let o=document.getElementById('otpInput').value;let p=document.getElementById('phoneInput').value;if(o!='1234'){alert('ভুল OTP');return;}localStorage.setItem('locked_phone',p);uid=p;document.getElementById('lockOverlay').style.display='none';fetch('/api/get?id='+p).then(()=>{initApp();document.getElementById('welcomeOverlay').style.display='flex';});}
function closeWelcome(){document.getElementById('welcomeOverlay').style.display='none';localStorage.setItem('welcomed_'+uid,'1');}
function goPage(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));document.getElementById('nav-'+p).classList.add('on');}
function watchAd(type){document.getElementById('adOverlay').style.display='flex';let t=15;document.getElementById('timer').innerText=t;let ti=setInterval(()=>{t--;document.getElementById('timer').innerText=t;document.getElementById('timerProg').style.width=(t/15*100)+'%';if(t<=0){clearInterval(ti);document.getElementById('adOverlay').style.display='none';fetch('/api/reward?id='+uid+'&type='+type).then(r=>r.json()).then(d=>{alert(d.msg);initApp();});}},1000);if(typeof show_11764581==='function'){show_11764581();}}
function doTask(id){fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:id})}).then(r=>r.json()).then(d=>{alert(d.msg);initApp();});}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ কপি');}
function selectMethod(m){selected=m;document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad');}
function doWithdraw(){let a=document.getElementById('amount').value;let n=document.getElementById('accNum').value;fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,amount:a,method:selected})}).then(r=>r.json()).then(d=>{alert(d.msg);initApp();});}
function saveProfile(){let nm=document.getElementById('editName').value;fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:nm})}).then(r=>r.json()).then(d=>{alert(d.msg);initApp();});}
initApp();
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin</title><style>*{box-sizing:border-box;font-family:system-ui}body{background:#070710;color:#fff;max-width:700px;margin:0 auto;padding:16px}.card{background:#15152a;border:1px solid #222;border-radius:14px;padding:14px;margin:10px 0}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}.btn{padding:10px 16px;border:none;border-radius:8px;font-weight:800;background:#6d4cff;color:#fff;cursor:pointer;margin-top:8px}table{width:100%;border-collapse:collapse;margin-top:8px}th,td{border:1px solid #333;padding:6px;font-size:11px}th{background:#0e0e20}</style></head><body>
<h2>👑 Admin - Logo Control + MITMIT</h2>
<div class="card"><h3>⚙️ Settings</h3>Bonus: <input id="bonus" type="number"><br>Ad Reward: <input id="ad_reward" type="number"><br>Min Withdraw: <input id="min_with" type="number"><br><button class="btn" onclick="save()">💾 Save</button></div>
<div class="card" style="border:2px solid #e2136e"><h3>🖼️ bKash / Nagad Logo - এডমিন থেকে চেঞ্জ</h3>bKash Name: <input id="bkash_name"><br>bKash Logo URL: <input id="bkash_logo" placeholder="https://...png"><br>Nagad Name: <input id="nagad_name"><br>Nagad Logo URL: <input id="nagad_logo" placeholder="https://...png"><br><button class="btn" style="background:#e2136e" onclick="save()">💾 Logo Save</button></div>
<div class="card"><h3>💸 Balance Add</h3><input id="admPhone" placeholder="Phone"><input id="admAmount" type="number"><div style="display:flex;gap:8px"><button class="btn" style="background:#10b981" onclick="bal('add')">+ যোগ</button><button class="btn" style="background:#ef4444" onclick="bal('minus')">- মাইনাস</button></div><div id="admMsg"></div></div>
<div class="card"><h3>👥 Users</h3><div id="userList"></div></div>
<script>
function load(){fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{let s=d.settings;document.getElementById('bonus').value=s.bonus;document.getElementById('ad_reward').value=s.ad_reward;document.getElementById('min_with').value=s.min_with;document.getElementById('bkash_name').value=s.bkash_name;document.getElementById('nagad_name').value=s.nagad_name;document.getElementById('bkash_logo').value=s.bkash_logo;document.getElementById('nagad_logo').value=s.nagad_logo;let uhtml='<table><tr><th>Phone</th><th>Name</th><th>Bal</th></tr>';Object.values(d.all_users).forEach(u=>{uhtml+=`<tr><td>${u.phone}</td><td>${u.name}</td><td>${u.balance}</td></tr>`;});uhtml+='</table>';document.getElementById('userList').innerHTML=uhtml;});}
function save(){let data={};document.querySelectorAll('input').forEach(e=>{if(e.id &&!e.id.startsWith('adm')) data[e.id]=e.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{alert(d.msg);load();});}
function bal(t){let p=document.getElementById('admPhone').value;let a=document.getElementById('admAmount').value;fetch('/api/admin/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:p,amount:a,type:t})}).then(r=>r.json()).then(d=>{document.getElementById('admMsg').innerText=d.msg;alert(d.msg);load();});}
load();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
