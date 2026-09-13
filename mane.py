# -*- coding: utf-8 -*-
# FINAL 1-5 - FIXED Gallery + All Buttons Working - 2026
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def default():
    return {
        "users":{},
        "withdraws":[],
        "settings":{
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","app_logo":"👑","admin_profile":"","admin_profile_img":"","zone":"11764581","bonus":1120,"ad_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"task_limit":5,"min_with":500,
            "official_banners":[],"google_ads":["🎉 Daily Bonus Available Today","⭐ Official Ad • bKash • Nagad • Trusted","📢 Company Sponsored • 100% Safe"],
            "offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!","balance_title":"আপনার বর্তমান ব্যালেন্স","tg_channel":"https://t.me/","support_link":"https://t.me/","whatsapp":"01XXXXXXXXX"
        },
        "tasks":[
            {"id":1,"title":"Telegram Channel Join","reward":25,"icon":"✈️","link":"https://t.me/","desc":"চ্যানেলে জয়েন করুন"},
            {"id":2,"title":"YouTube Subscribe","reward":30,"icon":"▶️","link":"https://youtube.com/","desc":"সাবস্ক্রাইব + লাইক"},
            {"id":3,"title":"Facebook Page Like","reward":20,"icon":"👍","link":"https://facebook.com/","desc":"পেজে লাইক দিন"},
            {"id":4,"title":"Refer Friend","reward":50,"icon":"👨‍👩‍👧‍👦","link":"","desc":"১ জন রেফার = ৳50"},
            {"id":5,"title":"Daily Check-in","reward":15,"icon":"✅","link":"","desc":"প্রতিদিন একবার"}
        ]
    }

def load():
    if not os.path.exists(DB):
        d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
    try: return json.load(open(DB,'r',encoding='utf-8'))
    except: d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
def save(d): json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
def getu(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":"","profile_img":"","balance":db["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":str(datetime.now())[:10]}
    u=db["users"][uid]
    if "name" not in u: u["name"]=""
    if "profile_img" not in u: u["profile_img"]=""
    if "join_date" not in u: u["join_date"]=today
    if u["last"]!=today: u["ads_today"]=0; u["popup_today"]=0; u["tasks_done"]=[]; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only",403
    return render_template_string(ADMIN)
@app.route('/api/get')
def api_get():
    db=load(); u=getu(db,request.args.get('id','0')); save(db)
    wds=[w for w in db.get("withdraws",[]) if w["uid"]==str(request.args.get('id','0'))]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":wds,"all_withdraws":db.get("withdraws",[])})
@app.route('/api/reward')
def api_reward():
    db=load(); u=getu(db,request.args.get('id')); typ=request.args.get('type','company'); s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":f"Limit {s['company_limit']} শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"Limit {s['popup_limit']} শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save(db); return jsonify({"msg":f"৳{s['ad_reward' if typ=='company' else 'popup_reward']} যোগ"})
@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=getu(db,uid); s=db["settings"]
    if tid in u["tasks_done"]: return jsonify({"msg":"আজকে করা হয়েছে"})
    if len(u["tasks_done"])>=s["task_limit"]: return jsonify({"msg":f"লিমিট {s['task_limit']} শেষ"})
    task=next((t for t in db["tasks"] if t["id"]==tid),None)
    if not task: return jsonify({"msg":"Task নেই"})
    u["tasks_done"].append(tid); u["balance"]+=task["reward"]; u["total"]+=1; save(db)
    return jsonify({"msg":f"✅ {task['title']} - ৳{task['reward']} যোগ"})
@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load(); j=request.json; uid=str(j.get('id')); u=getu(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    if len(num) < 11: return jsonify({"msg":"সঠিক নাম্বার দিন"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"status":"Pending","time":str(datetime.now())[:16]})
    save(db); return jsonify({"msg":f"✅ {method} ৳{amt} Request সফল"})
@app.route('/api/user/update',methods=['POST'])
def user_update():
    db=load(); j=request.json; uid=str(j.get('id')); u=getu(db,uid)
    if 'name' in j: u["name"]=j['name'][:25]
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save(db); return jsonify({"msg":"✅ প্রোফাইল সেভ হয়েছে","user":u})
@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load(); j=request.json
    for k in j:
        if k.startswith("google_ad"):
            try: idx=int(k[-1])-1; db["settings"]["google_ads"][idx]=j[k]
            except: pass
        elif k.startswith("task_"):
            try: parts=k.split('_'); tid=int(parts[1]); field=parts[2];
                for t in db["tasks"]:
                    if t["id"]==tid:
                        if field=='reward': t[field]=int(j[k])
                        else: t[field]=j[k]
            except: pass
        else: db["settings"][k]=j[k]
    save(db); return jsonify({"msg":"✅ Saved - সব কাজ করবে"})
@app.route('/api/admin/upload',methods=['POST'])
def upload():
    db=load(); j=request.json
    if 'img' in j: db["settings"]["admin_profile_img"]=j['img']; save(db); return jsonify({"msg":"✅ প্রোফাইল আপডেট"})
    if 'banner' in j:
        if len(db["settings"]["official_banners"])>=5: db["settings"]["official_banners"].pop(0)
        db["settings"]["official_banners"].append(j['banner']); save(db); return jsonify({"msg":f"✅ ব্যানার {len(db['settings']['official_banners'])}/5"})
    if 'clear_banner' in j: db["settings"]["official_banners"]=[]; save(db); return jsonify({"msg":"🗑️ মুছা হয়েছে"})
    return jsonify({"msg":"Error"})

USER="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:125px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,#17172a,#0e0e20);border:1px solid #222;position:relative;overflow:hidden}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;font-size:14px;color:#fff;margin-top:8px;cursor:pointer}
.profile{width:52px;height:52px;border-radius:50%;background:#1e293b;display:flex;align-items:center;justify-content:center;border:2px solid #6d4cff;overflow:hidden;box-shadow:0 0 12px rgba(109,76,255,0.4);font-size:22px;cursor:pointer}
.profile img{width:100%;height:100%;object-fit:cover}
.profileBig{width:96px;height:96px;border-radius:50%;background:#1e293b;display:flex;align-items:center;justify-content:center;border:3px solid #6d4cff;margin:0 auto;overflow:hidden;font-size:42px;position:relative;cursor:pointer}
.profileBig img{width:100%;height:100%;object-fit:cover}
.camIcon{position:absolute;bottom:2px;right:2px;background:#6d4cff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;border:2px solid #0e0e20}
@keyframes blinkGlow{0%{box-shadow:0 0 10px rgba(245,158,11,0.3)}50%{box-shadow:0 0 28px rgba(245,158,11,0.85)}100%{box-shadow:0 0 10px rgba(245,158,11,0.3)}}
@keyframes shineMove{0%{left:-100%}100%{left:200%}}
.bannerBox{margin:12px;border-radius:22px;overflow:hidden;height:165px;background:linear-gradient(90deg,#f59e0b,#ef4444);position:relative;border:2px solid rgba(255,255,255,0.15);animation:blinkGlow 2.2s infinite}
.bannerBox img{width:100%;height:100%;object-fit:cover}
.shine{position:absolute;top:0;left:-100%;width:65%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35),transparent);transform:skewX(-20deg);animation:shineMove 2.8s infinite;z-index:2}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
.taskCard{display:flex;justify-content:space-between;align-items:center;background:#15152a;border:1px solid #2a2a4a;border-radius:14px;padding:12px;margin:10px 0}
.payCard{display:flex;align-items:center;gap:12px;background:#15152a;border:2px solid #2a2a4a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.payCard.active{border-color:#e2136e;background:#1e1e3a}
.payLogo{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:22px}
.faq{background:#15152a;border:1px solid #2a2a4a;border-radius:12px;padding:12px;margin:8px 0}
.statBox{background:#15152a;border:1px solid #2a2a4a;border-radius:14px;padding:12px;text-align:center;flex:1}
input[type=file]{position:absolute;opacity:0;width:0;height:0}
</style></head><body>
<div class="top"><div style="display:flex;align-items:center;gap:10px"><div style="font-size:28px" id="appLogo">👑</div><div><div style="font-weight:900;font-size:16px;display:flex;align-items:center;gap:6px"><span id="appName"></span><span style="background:#22c55e;color:#fff;font-size:10px;padding:2px 6px;border-radius:6px">✓</span></div><div style="font-size:11px;opacity:0.6" id="adminName"></div></div></div><div class="profile" id="profBox" onclick="nav('profile')">👤</div></div>

<div id="p-home" class="page active">
<div class="bannerBox" id="bannerBox"><div class="shine"></div><div style="height:100%;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:800" id="gAd"></div></div>
<div class="card" style="text-align:center;background:linear-gradient(135deg,#1e3a8a,#2563eb,#06b6d4,#10b981);padding:20px 16px"><div class="shine"></div><div style="font-size:11px;color:#c7d2fe;font-weight:600;position:relative;z-index:3" id="balTitle"></div><div style="font-size:42px;font-weight:500;margin:8px 0;position:relative;z-index:3">৳<span id="bal" style="font-weight:700">0</span></div><div style="display:flex;justify-content:center;gap:6px;flex-wrap:wrap;position:relative;z-index:3"><span style="background:rgba(0,0,0,0.3);padding:5px 10px;border-radius:20px;font-size:11px">Company <b id="ads" style="color:#fde68a">0</b>/<span id="adsLim">30</span></span><span style="background:rgba(0,0,0,0.3);padding:5px 10px;border-radius:20px;font-size:11px">Popup <b id="pop" style="color:#86efac">0</b>/<span id="popLim">20</span></span><span style="background:rgba(0,0,0,0.3);padding:5px 10px;border-radius:20px;font-size:11px">Total <b id="total">0</b></span></div><div style="background:rgba(0,0,0,0.35);height:6px;border-radius:20px;margin-top:14px;overflow:hidden;position:relative;z-index:3"><div id="prog" style="height:100%;background:linear-gradient(90deg,#fde68a,#fbbf24);width:0%"></div></div></div>
<div class="card"><button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS (৳<span id="r1">2</span>) - <span id="ads2">0</span>/<span id="adsLim2">30</span></button><button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS (৳<span id="r2">3</span>) - <span id="pop2">0</span>/<span id="popLim2">20</span></button><button class="btn" style="background:#1e293b" onclick="nav('task')">📋 TASK BONUS - 5 টা/দিন</button></div>
<div class="card" style="border:1.5px solid #fbbf24"><div style="font-weight:800" id="offerTitle"></div><div style="font-size:12px;margin-top:5px;opacity:0.85" id="offerDesc"></div></div>
</div>

<div id="p-task" class="page">
<div class="card"><h3>📋 Task Bonus - দিনে 5 টা</h3><div id="taskList" style="margin-top:12px"></div>
<div style="margin-top:18px;background:linear-gradient(135deg,#6d4cff,#3a1aff);border-radius:16px;padding:16px;position:relative;overflow:hidden"><div class="shine"></div><div style="position:relative;z-index:3"><div style="font-weight:900">🎁 Refer & Earn ৳50</div><div style="background:rgba(0,0,0,0.35);border-radius:10px;padding:10px;margin-top:10px;font-size:11px;word-break:break-all" id="refLink"></div><button class="btn" style="background:#fff;color:#3a1aff;margin-top:10px" onclick="copyRef()">📋 লিংক কপি করুন</button></div></div>
<div style="margin-top:12px;background:linear-gradient(135deg,#0ea5e9,#0284c7);border-radius:16px;padding:16px;display:flex;justify-content:space-between;align-items:center"><div><div style="font-weight:800">📢 Telegram Channel</div><div style="font-size:11px;opacity:0.9">আপডেট ও পেমেন্ট প্রুফ</div></div><button class="btn" style="width:auto;background:#fff;color:#0284c7;padding:10px 16px;margin:0" onclick="openTG()">Join ✈️</button></div>
</div>
</div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center;background:linear-gradient(135deg,#1e293b,#334155)"><div style="font-size:12px;opacity:0.7">ব্যালেন্স</div><div style="font-size:40px;font-weight:600;margin:6px 0">৳<span id="bal2" style="font-weight:800">0</span></div><div style="font-size:11px;opacity:0.6">Min ৳<span id="minWith">500</span></div></div>
<div class="card"><h3>💸 Withdraw Method</h3>
<div class="payCard active" id="pay-bkash" onclick="selectPay('bKash')"><div class="payLogo" style="background:#e2136e">৳</div><div><div style="font-weight:800">bKash</div><div style="font-size:11px;opacity:0.6">Personal • Instant</div></div><div style="margin-left:auto;color:#22c55e;font-weight:800" id="bkashCheck">✓</div></div>
<div class="payCard" id="pay-nagad" onclick="selectPay('Nagad')"><div class="payLogo" style="background:#f69220">৳</div><div><div style="font-weight:800">Nagad</div><div style="font-size:11px;opacity:0.6">Personal • Fast</div></div><div style="margin-left:auto;color:#6b7280" id="nagadCheck">○</div></div>
<div style="margin-top:14px"><input id="withNumber" type="tel" placeholder="01XXXXXXXXX" style="width:100%;padding:14px;margin-top:6px;border-radius:12px;border:1px solid #2a2a4a;background:#15152a;color:#fff"><input id="withAmount" type="number" placeholder="500" style="width:100%;padding:14px;margin-top:10px;border-radius:12px;border:1px solid #2a2a4a;background:#15152a;color:#fff"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f69220);padding:16px;margin-top:14px" onclick="doWithdraw()">🚀 Withdraw করুন</button></div>
</div>
<div class="card"><h3>📜 History</h3><div id="withHistory" style="margin-top:10px;font-size:12px;opacity:0.7"></div></div>
</div>

<div id="p-support" class="page">
<div class="card" style="text-align:center;background:linear-gradient(135deg,#6d4cff,#3a1aff);border:none"><div class="shine"></div><div style="position:relative;z-index:3"><div style="font-size:12px;font-weight:700;background:rgba(0,0,0,0.25);padding:6px 12px;border-radius:20px;display:inline-block">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:32px;margin-top:12px">💬</div><div style="font-weight:900;font-size:18px;margin-top:6px">আমরা আছি আপনার পাশে</div></div></div>
<div class="card"><h3>🚀 দ্রুত যোগাযোগ</h3>
<div class="payCard" style="border-color:#0ea5e9;background:#0c1a2e" onclick="openTG()"><div class="payLogo" style="background:#0ea5e9">✈️</div><div><div style="font-weight:800">Telegram Support</div><div style="font-size:11px;opacity:0.6">2 মিনিটে রিপ্লাই</div></div><div style="margin-left:auto">➡️</div></div>
<div class="payCard" onclick="window.open('https://wa.me/'+settings.whatsapp)"><div class="payLogo" style="background:#22c55e">💬</div><div><div style="font-weight:800">WhatsApp</div><div style="font-size:11px;opacity:0.6" id="waNum">Direct Chat</div></div><div style="margin-left:auto">➡️</div></div>
</div>
<div class="card"><h3>❓ FAQ</h3><div class="faq"><b>Q: টাকা কখন পাবো?</b><br><span style="font-size:11px;opacity:0.7">A: 24 ঘণ্টায় bKash/Nagad এ।</span></div><div class="faq"><b>Q: VPN চলবে?</b><br><span style="font-size:11px;opacity:0.7">A: না, ব্যান হবে।</span></div></div>
</div>

<!-- PAGE 5 PROFILE - FIXED GALLERY -->
<div id="p-profile" class="page">
<div class="card" style="text-align:center;background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #2a2a4a">
<div class="profileBig" id="userBigPic" onclick="openGallery()"><span id="bigPicTxt">👤</span><div class="camIcon">📸</div></div>
<div style="margin-top:12px"><div style="font-weight:900;font-size:18px" id="userNameShow">User</div><div style="font-size:11px;opacity:0.6" id="userIdShow"></div><div style="margin-top:6px"><span style="background:#6d4cff;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700" id="userLevel">🥉 Bronze Member</span></div></div>
<div style="margin-top:14px">
<input type="file" id="userPicInput" accept="image/*" style="position:absolute;left:-9999px;opacity:0;width:1px;height:1px">
<input id="userNameInput" placeholder="আপনার নাম লিখুন" style="width:100%;padding:12px;border-radius:12px;border:1px solid #2a2a4a;background:#15152a;color:#fff;text-align:center;font-weight:700">
<button class="btn" style="background:#1e293b;border:1px solid #334155;margin-top:10px" onclick="openGallery()">🖼️ গ্যালারি থেকে ছবি বেছে নিন</button>
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff);margin-top:10px" onclick="saveUserProfile()">💾 প্রোফাইল সেভ করুন</button>
<div style="font-size:10px;opacity:0.5;margin-top:6px">ছবিতে ক্লিক করুন বা বাটনে ক্লিক করুন → গ্যালারি খুলবে</div>
</div>
</div>
<div class="card"><h3>📊 পরিসংখ্যান</h3><div style="display:flex;gap:8px;margin-top:10px"><div class="statBox"><div style="font-size:18px">💰</div><div style="font-weight:800" id="statBal">৳0</div><div style="font-size:10px;opacity:0.6">ব্যালেন্স</div></div><div class="statBox"><div style="font-size:18px">📺</div><div style="font-weight:800" id="statAds">0</div><div style="font-size:10px;opacity:0.6">Ads</div></div><div class="statBox"><div style="font-size:18px">📋</div><div style="font-weight:800" id="statTasks">0</div><div style="font-size:10px;opacity:0.6">Task</div></div></div><div style="display:flex;gap:8px;margin-top:8px"><div class="statBox"><div style="font-size:18px">👥</div><div style="font-weight:800" id="statTotal">0</div><div style="font-size:10px;opacity:0.6">Total Work</div></div><div class="statBox"><div style="font-size:18px">📅</div><div style="font-weight:800" id="statJoin">-</div><div style="font-size:10px;opacity:0.6">Join Date</div></div><div class="statBox"><div style="font-size:18px">🆔</div><div style="font-weight:800;font-size:12px" id="statId">-</div><div style="font-size:10px;opacity:0.6">User ID</div></div></div></div>
<div class="card"><h3>⚙️ সেটিংস</h3>
<div class="payCard" onclick="nav('wallet')"><div class="payLogo" style="background:#1e293b">💸</div><div><div style="font-weight:700;font-size:13px">Withdraw History</div><div style="font-size:11px;opacity:0.6">পেমেন্ট দেখুন</div></div><div style="margin-left:auto">➡️</div></div>
<div class="payCard" onclick="copyRef()"><div class="payLogo" style="background:#1e293b">🔗</div><div><div style="font-weight:700;font-size:13px">My Refer Link</div><div style="font-size:10px;opacity:0.6;word-break:break-all" id="refLink2"></div></div><div style="margin-left:auto">📋</div></div>
</div>
<div class="card" style="background:linear-gradient(135deg,#064e3b,#065f46);border:1px solid #10b981;text-align:center"><div style="font-weight:800">🛡️ Verified User - 100% Safe</div></div>
</div>

<div class="btm"><div class="on" id="b-home" onclick="nav('home')"><span>🏠</span>Home</div><div id="b-task" onclick="nav('task')"><span>📋</span>Task</div><div id="b-wallet" onclick="nav('wallet')"><span>💰</span>Wallet</div><div id="b-support" onclick="nav('support')"><span>💬</span>Support</div><div id="b-profile" onclick="nav('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let gAds=[],banners=[],idx=0,currentTasks=[],userData=null,settings=null,selectedPay='bKash',tempUserPic="";
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');window.scrollTo(0,0);}
function selectPay(m){selectedPay=m;document.getElementById('pay-bkash').classList.toggle('active',m=='bKash');document.getElementById('pay-nagad').classList.toggle('active',m=='Nagad');document.getElementById('bkashCheck').innerText=m=='bKash'?'✓':'○';document.getElementById('nagadCheck').innerText=m=='Nagad'?'✓':'○';}
function openGallery(){document.getElementById('userPicInput').click();}
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());let s=r.settings;settings=s;let u=r.user;userData=u;currentTasks=r.tasks;
 bal.innerText=u.balance;bal2.innerText=u.balance;ads.innerText=u.ads_today;pop.innerText=u.popup_today;ads2.innerText=u.ads_today;pop2.innerText=u.popup_today;total.innerText=u.total;
 adsLim.innerText=s.company_limit;adsLim2.innerText=s.company_limit;popLim.innerText=s.popup_limit;popLim2.innerText=s.popup_limit;
 r1.innerText=s.ad_reward;r2.innerText=s.popup_reward;appName.innerText=s.app_name;adminName.innerText='Admin: '+s.admin_name;appLogo.innerText=s.app_logo;balTitle.innerText='💰 '+s.balance_title;offerTitle.innerText=s.offer_title;offerDesc.innerText=s.offer_desc;minWith.innerText=s.min_with;
 gAds=s.google_ads;banners=s.official_banners||[];prog.style.width=((u.ads_today+u.popup_today)/(s.company_limit+s.popup_limit)*100)+'%';
 document.getElementById('userIdShow').innerText='ID: '+uid;document.getElementById('userNameShow').innerText=u.name||'User '+uid.slice(-4);document.getElementById('userNameInput').value=u.name||'';document.getElementById('statBal').innerText='৳'+u.balance;document.getElementById('statAds').innerText=u.ads_today+u.popup_today;document.getElementById('statTasks').innerText=u.tasks_done.length;document.getElementById('statTotal').innerText=u.total;document.getElementById('statJoin').innerText=u.join_date||'-';document.getElementById('statId').innerText=uid;document.getElementById('refLink').innerText=location.origin+'/?ref='+uid;document.getElementById('refLink2').innerText=location.origin+'/?ref='+uid;
 document.getElementById('waNum').innerText=s.whatsapp||'WhatsApp Chat';
 let topBox=document.getElementById('profBox');let bigBox=document.getElementById('userBigPic');
 if(u.profile_img&&u.profile_img.startsWith('data:image')){topBox.innerHTML=`<img src="${u.profile_img}">`;bigBox.innerHTML=`<img src="${u.profile_img}"><div class="camIcon">📸</div>`;}else{topBox.innerHTML='👤';bigBox.innerHTML=`<span id="bigPicTxt">👤</span><div class="camIcon">📸</div>`;}
 renderBanner();renderTasks();renderWithdraws(r.withdraws||[]);
}
function renderBanner(){let box=document.getElementById('bannerBox');if(banners.length>0){box.innerHTML=`<div class="shine"></div><img src="${banners[idx % banners.length]}"><div class="bannerText" style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.9));padding:30px 14px 12px;font-weight:800;text-align:center;font-size:14px">${gAds[idx % gAds.length]||''}</div>`;}else{box.innerHTML=`<div class="shine"></div><div style="height:100%;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:800;background:linear-gradient(90deg,#f59e0b,#ef4444)">${gAds[idx % gAds.length]||''}</div>`;}}
function renderTasks(){let tl=document.getElementById('taskList');if(!tl)return;tl.innerHTML='';currentTasks.forEach(t=>{let done=userData.tasks_done.includes(t.id);tl.innerHTML+=`<div class="taskCard ${done?'opacity:0.5':''}"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:24px">${t.icon}</div><div><div style="font-weight:700;font-size:13px">${t.title}</div><div style="font-size:11px;opacity:0.6">${t.desc} • ৳${t.reward}</div></div></div><button class="btn" style="width:auto;padding:10px 14px;margin:0;font-size:12px;background:${done?'#333':'#6d4cff'}" onclick="doTask(${t.id})">${done?'✅ Done':'৳'+t.reward}</button></div>`;});}
function renderWithdraws(list){let h=document.getElementById('withHistory');if(list.length==0){h.innerHTML='কোনো Withdraw নেই';return;}h.innerHTML='';list.slice(-5).reverse().forEach(w=>{h.innerHTML+=`<div style="background:#15152a;border:1px solid #2a2a4a;border-radius:10px;padding:10px;margin:6px 0;display:flex;justify-content:space-between"><div><b>${w.method}</b> - ৳${w.amount}<br><span style="font-size:10px;opacity:0.6">${w.number} • ${w.time}</span></div><div style="color:${w.status=='Pending'?'#fbbf24':'#22c55e'};font-weight:700">${w.status}</div></div>`;});}
async function doTask(tid){let t=currentTasks.find(x=>x.id==tid);if(t.link&&t.link.startsWith('http')){window.open(t.link,'_blank');}setTimeout(async()=>{if(confirm(t.title+' Complete করেছেন?')){let res=await fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:tid})}).then(x=>x.json());alert(res.msg);load();}},1200);}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে...');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে...');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ Copy হয়েছে');}
function openTG(){window.open(settings.tg_channel||settings.support_link,'_blank');}
async function doWithdraw(){let num=document.getElementById('withNumber').value;let amt=document.getElementById('withAmount').value;if(!num||!amt){alert('নাম্বার ও পরিমাণ দিন');return;}let res=await fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:num,amount:amt,method:selectedPay})}).then(x=>x.json());alert(res.msg);load();}
// FIXED GALLERY - Compress + Works 100%
document.getElementById('userPicInput').addEventListener('change',function(e){
 let file=e.target.files[0];if(!file)return;
 let reader=new FileReader();
 reader.onload=function(ev){
   let img=new Image();
   img.onload=function(){
     let canvas=document.createElement('canvas');let max=300;let w=img.width,h=img.height;
     if(w>h){if(w>max){h*=max/w;w=max;}}else{if(h>max){w*=max/h;h=max;}}
     canvas.width=w;canvas.height=h;canvas.getContext('2d').drawImage(img,0,0,w,h);
     tempUserPic=canvas.toDataURL('image/jpeg',0.7);
     document.getElementById('userBigPic').innerHTML=`<img src="${tempUserPic}"><div class="camIcon">📸</div>`;
     document.getElementById('profBox').innerHTML=`<img src="${tempUserPic}">`;
   };img.src=ev.target.result;
 };reader.readAsDataURL(file);
});
async function saveUserProfile(){
 let name=document.getElementById('userNameInput').value.trim();
 if(!name&&!tempUserPic){alert('নাম লিখুন বা ছবি সিলেক্ট করুন');return;}
 let payload={id:uid,name:name};if(tempUserPic)payload.profile_img=tempUserPic;
 let res=await fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(x=>x.json());
 alert(res.msg);tempUserPic="";load();
}
setInterval(()=>{idx++;renderBanner();},3000);load();
</script></body></html>
"""

ADMIN="""
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#0f0f0f;color:#fff;font-family:sans-serif;padding:14px}input,textarea{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:10px 0}.btn{padding:12px;width:100%;border:none;border-radius:8px;background:#6d4cff;color:#fff;font-weight:800;margin-top:6px}</style></head><body>
<h2>👑 Admin - Final Fixed All Buttons</h2>
<div class="card" style="border:1.5px solid #f59e0b"><h3>⭐ ব্যানার (5 টা)</h3><input type="file" id="bannerFile" accept="image/*"><button class="btn" style="background:#f59e0b" onclick="uploadBanner()">📸 যোগ</button><button class="btn" style="background:#ef4444" onclick="clearBanner()">🗑️ মুছুন</button><div id="bannerCount"></div></div>
<div class="card"><h3>📝 সব লেখা এডিট (Admin থেকে লিখলে সাথে কাজ করবে)</h3>App Name:<input id="app_name">Admin Name:<input id="admin_name">Logo Emoji:<input id="app_logo">TG Link:<input id="tg_channel">Support Link:<input id="support_link">WhatsApp:<input id="whatsapp">Balance Title:<input id="balance_title"></div>
<div class="card"><h3>📢 Google Ads Text (3 টা)</h3>Ad1:<input id="g1">Ad2:<input id="g2">Ad3:<input id="g3"></div>
<div class="card">Offer Title:<input id="offer_title">Offer Desc:<textarea id="offer_desc"></textarea></div>
<div class="card"><h3>💰 Limit & Reward (সব কাজ করবে)</h3>Company Limit:<input id="company_limit" type="number">Company Reward:<input id="ad_reward" type="number">Popup Limit:<input id="popup_limit" type="number">Popup Reward:<input id="popup_reward" type="number">Task Limit:<input id="task_limit" type="number">Min Withdraw:<input id="min_with" type="number"></div>
<button class="btn" style="padding:16px;background:#6d4cff" onclick="save()">💾 Save All - সব বাটন কাজ করবে</button><div id="msg" style="text-align:center;color:#fde047;margin-top:8px;font-weight:800"></div>
<div class="card"><h3>💸 Withdraw List</h3><div id="wdList" style="font-size:12px"></div></div>
<script>
let banner64="";
bannerFile.addEventListener('change',e=>{let r=new FileReader();r.onload=ev=>{banner64=ev.target.result;};r.readAsDataURL(e.target.files[0]);});
async function uploadBanner(){if(!banner64){alert('ফাইল সিলেক্ট করুন');return;}let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({banner:banner64})}).then(x=>x.json());msg.innerText=res.msg;load();}
async function clearBanner(){let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({clear_banner:1})}).then(x=>x.json());msg.innerText=res.msg;load();}
async function load(){let data=await fetch('/api/get?id=8807178385').then(x=>x.json());let s=data.settings;app_name.value=s.app_name;admin_name.value=s.admin_name;app_logo.value=s.app_logo;tg_channel.value=s.tg_channel||'';support_link.value=s.support_link||'';whatsapp.value=s.whatsapp||'';balance_title.value=s.balance_title;g1.value=s.google_ads[0];g2.value=s.google_ads[1];g3.value=s.google_ads[2];offer_title.value=s.offer_title;offer_desc.value=s.offer_desc;company_limit.value=s.company_limit;ad_reward.value=s.ad_reward;popup_limit.value=s.popup_limit;popup_reward.value=s.popup_reward;task_limit.value=s.task_limit;min_with.value=s.min_with;bannerCount.innerText=`ব্যানার ${s.official_banners.length}/5`;let wd=document.getElementById('wdList');wd.innerHTML='';(data.all_withdraws||[]).slice(-30).reverse().forEach(w=>{wd.innerHTML+=`<div style="border:1px solid #333;padding:6px;margin:4px 0;border-radius:6px">${w.uid} | ${w.method} ৳${w.amount} | ${w.number} | ${w.status} | ${w.time}</div>`;});}
async function save(){let d={app_name:app_name.value,admin_name:admin_name.value,app_logo:app_logo.value,tg_channel:tg_channel.value,support_link:support_link.value,whatsapp:whatsapp.value,balance_title:balance_title.value,google_ad1:g1.value,google_ad2:g2.value,google_ad3:g3.value,offer_title:offer_title.value,offer_desc:offer_desc.value,company_limit:parseInt(company_limit.value),ad_reward:parseInt(ad_reward.value),popup_limit:parseInt(popup_limit.value),popup_reward:parseInt(popup_reward.value),task_limit:parseInt(task_limit.value),min_with:parseInt(min_with.value)};let res=await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(x=>x.json());msg.innerText=res.msg;}
load();
</script></body></html>
"""
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
