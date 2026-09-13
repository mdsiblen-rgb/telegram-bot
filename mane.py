# -*- coding: utf-8 -*-
# MASTER FINAL - 5 Page + bKash/Nagad Logo Admin + User Locking System
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def default_data():
    return {"users":{},"withdraws":[],"settings":{
        "bonus":1120,"ad_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"min_with":500,
        "slider1":"","slider2":"","slider3":"","slider4":"","slider5":"",
        "slider_text1":"🎉 Daily Bonus Available Today","slider_text2":"📢 Company Sponsored • 100% Safe","slider_text3":"💰 1120 TK Bonus","slider_text4":"🚀 Fast Payment","slider_text5":"👑 Protidiner Kaj BD",
        "balance_title":"💰 আপনার বর্তমান ব্যালেন্স","btn1_text":"COMPANY ADS (৳2)","btn2_text":"POPUP ADS (৳3)","btn3_text":"TASK BONUS - 5 টা/দিন","offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!",
        "task_page_title":"📋 Task Bonus - দিনে 5 টা","task1_title":"Telegram Channel Join","task1_bn":"চ্যানেলে জয়েন করুন","task1_reward":"25","task1_link":"https://t.me/","task1_icon":"✈️","task2_title":"YouTube Subscribe","task2_bn":"সাবস্ক্রাইব + লাইক","task2_reward":"30","task2_link":"https://youtube.com/","task2_icon":"▶️","task3_title":"Facebook Page Like","task3_bn":"পেজে লাইক দিন","task3_reward":"20","task3_link":"","task3_icon":"👍","task4_title":"Refer Friend","task4_bn":"১ জন রেফার = ৳50","task4_reward":"50","task4_icon":"👥","task5_title":"Daily Check-in","task5_bn":"প্রতিদিন একবার","task5_reward":"15","task5_icon":"✅",
        "refer_title":"🎁 Refer & Earn ৳50","telegram_title":"Telegram Channel","telegram_sub":"আপডেট ও প্রুফ","telegram_link":"https://t.me/",
        "wallet_balance_label":"ব্যালেন্স","wallet_min_label":"Min ৳500","wallet_method_title":"💸 Withdraw Method",
        "bkash_name":"bKash","bkash_sub":"Personal • Instant Payment","bkash_logo":"https://i.ibb.co/0jZzXQ0/bkash-logo.png","nagad_name":"Nagad","nagad_sub":"Personal • Fast Withdraw","nagad_logo":"https://i.ibb.co/XYZ/nagad-logo.png",
        "withdraw_btn_text":"🚀 Withdraw করুন","support_top_msg":"💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন","support_center_title":"আমরা আছি আপনার পাশে","support_center_sub":"২৪ ঘণ্টা সাপোর্ট • 100% Trusted","quick_contact_title":"🚀 দ্রুত যোগাযোগ করুন","tele_sup_title":"Telegram Support (Fast Reply)","tele_sup_sub":"2 মিনিটে রিপ্লাই • 9AM-12AM","tele_sup_link":"https://t.me/","wa_sup_title":"WhatsApp Support","wa_sup_number":"01XXXXXXXXX","wa_sup_link":"https://wa.me/8801","email_sup_title":"Email Support","email_sup_address":"support@protidinerkajbd.com","email_sup_link":"mailto:support@","how_work_title":"🎥 কিভাবে কাজ করবেন?","tutorial_btn_text":"Tutorial - 2 মিনিটে শিখুন","tutorial_click_text":"▶️ Click করলে ভিডিও চলবে","tutorial_youtube_link":"https://youtube.com/","step1":"Step 1: Ads দেখুন","step2":"Step 2: Task complete করুন","step3":"Step 3: ৳500 হলেই Withdraw","faq_q1":"Q: টাকা কখন পাবো?","faq_a1":"A: 24 ঘণ্টার মধ্যে","faq_q2":"Q: VPN চলবে?","faq_a2":"A: না, ব্যান হবে।","faq_q3":"Q: 1 ফোনে কয়টা একাউন্ট?","faq_a3":"A: 1 টা।","faq_q4":"Q: Refer বোনাস?","faq_a4":"A: 1 জন = ৳50","trusted_title":"🛡️ 100% Trusted","trusted_desc":"50k+ ইউজার, 100% পেমেন্ট গ্যারান্টি।","profile_title":"👤 My Profile","profile_lock_title":"🔒 লকিং সিস্টেম","zone":"11764581"
    }}

def load_db():
    if not os.path.exists(DB):
        d=default_data()
        with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d
    with open(DB,'r',encoding='utf-8') as f: return json.load(f)
def save_db(d):
    with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","profile_img":"","balance":1120,"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":today,"phone":uid}
    u=db["users"][uid]
    if u.get("last")!=today: u["ads_today"]=0; u["popup_today"]=0; u["tasks_done"]=[]; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin?id=8807178385",403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get')
def api_get():
    db=load_db(); uid=request.args.get('id','0'); u=get_user(db,uid); wds=[w for w in db["withdraws"] if w["uid"]==str(uid)]; save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"withdraws":wds})
@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id')); typ=request.args.get('type','company'); s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=int(s["company_limit"]): return jsonify({"msg":"লিমিট শেষ"})
        u["ads_today"]+=1; u["balance"]+=int(s["ad_reward"])
    else:
        if u["popup_today"]>=int(s["popup_limit"]): return jsonify({"msg":"লিমিট শেষ"})
        u["popup_today"]+=1; u["balance"]+=int(s["popup_reward"])
    u["total"]+=1; save_db(db); return jsonify({"msg":"৳ যোগ"})
@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid); s=db["settings"]
    if tid in u["tasks_done"]: return jsonify({"msg":"করা হয়েছে"})
    reward=int(s.get(f'task{tid}_reward','20')); u["tasks_done"].append(tid); u["balance"]+=reward; u["total"]+=1; save_db(db)
    return jsonify({"msg":f"✅ {reward} TK"})
@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0))
    if amt < int(s["min_with"]): return jsonify({"msg":f"মিনিমাম {s['min_with']}"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":uid,"amount":amt,"number":j.get('number',''),"method":j.get('method','bKash'),"status":"Pending","time":str(datetime.now())[:16]})
    save_db(db); return jsonify({"msg":"✅ Request"})
@app.route('/api/profile/update',methods=['POST'])
def profile_update():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); u["profile_img"]=j.get('img',''); save_db(db); return jsonify({"msg":"✅ Profile Update"})
@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db(); j=request.json
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ Save হয়েছে - Logo + Locking + All Pages"})

USER_HTML = """<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#0a0a14;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}
.top{padding:12px 16px;display:flex;justify-content:space-between;align-items:center;background:#0f0f1e;position:sticky;top:0;z-index:99;border-bottom:1px solid #1a1a2e}
.card{margin:12px;border-radius:20px;padding:14px;background:#15152a;border:1px solid #23233a}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;margin-top:8px;cursor:pointer}
.page{display:none}.page.active{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;padding:8px 0;border-radius:20px 20px 0 0;border-top:1px solid #23233a;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:700;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
#lockOverlay,#welcomeOverlay,#adOverlay{position:fixed;inset:0;z-index:999;display:none;justify-content:center;align-items:center;padding:20px}
#lockOverlay{display:flex;background:#0a0a14f2}#welcomeOverlay{background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2)}#adOverlay{background:#000e;flex-direction:column;color:#fff}
input{width:100%;padding:14px;border-radius:12px;border:1px solid #2a2a4a;background:#0e0e20;color:#fff;margin-top:8px}
.taskItem{display:flex;justify-content:space-between;align-items:center;background:#0e0e20;border:1px solid #23233a;border-radius:14px;padding:12px;margin:10px 0}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #2a2a4a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.payCard.active{border-color:#e2136e;background:#1e1e3a}.payLogo{width:56px;height:56px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:24px;overflow:hidden;background:#1e293b}.payLogo img{width:100%;height:100%;object-fit:cover}
.supportItem{display:flex;align-items:center;gap:12px;background:#0e0e20;border:1.5px solid #23233a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.blinkBox{animation:mitmit 1.2s infinite;border:2px solid #6d4cff!important}
@keyframes mitmit{0%{box-shadow:0 0 5px #6d4cff}50%{box-shadow:0 0 25px #6d4cff,0 0 40px #06b6d4;transform:scale(1.02)}100%{box-shadow:0 0 5px #6d4cff}}
.blinkBox2{animation:mitmit2 1.2s infinite 0.6s;border:2px solid #f59e0b!important}
@keyframes mitmit2{0%{box-shadow:0 0 5px #f59e0b}50%{box-shadow:0 0 25px #f59e0b,0 0 40px #ef4444;transform:scale(1.02)}100%{box-shadow:0 0 5px #f59e0b}}
.slider{position:relative;height:150px;border-radius:20px;overflow:hidden;margin:12px;background:#15152a}
.slide{position:absolute;inset:0;display:none;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:18px;padding:20px;background-size:cover;background-position:center}
.slide.active{display:flex}
.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px}.dot{width:8px;height:8px;border-radius:50%;background:#fff5}.dot.active{background:#fff}
</style></head><body>
<div class="top"><div style="display:flex;align-items:center;gap:10px"><div style="font-size:32px">👑</div><div><div style="font-weight:800">Protidiner Kaj BD <span style="background:#10b981;padding:2px 6px;border-radius:6px;font-size:10px">✓</span></div><div style="font-size:11px;color:#aaa">Admin: SHIBLI NOMAN</div></div></div><div style="width:48px;height:48px;border-radius:50%;border:2px solid #6d4cff;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden" id="topAv"><img id="topAvImg" src="" style="width:100%;height:100%;object-fit:cover;display:none"><span id="topAvTxt">👤</span></div></div>

<!-- LOCKING SYSTEM - USER LOCK -->
<div id="lockOverlay"><div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:340px;text-align:center"><div style="font-size:40px">🔒</div><h2 style="color:#6d4cff;margin-top:8px">নাম্বার দিয়ে লক করুন</h2><p style="font-size:12px;font-weight:800;margin-top:4px">নাম্বার দিয়ে লক করুন, নাম্বার দিয়ে লগইন করুন - ইউজার নিজে লক করতে পারবে</p><input id="phoneInput" type="tel" placeholder="01XXXXXXXXX" maxlength="11" style="background:#f5f3ff;color:#000;border:1px solid #ddd"><button class="btn" style="background:#6d4cff" onclick="sendOTP()">📲 OTP পাঠান</button><div id="otpSection" style="display:none;margin-top:10px"><input id="otpInput" placeholder="OTP 1234" maxlength="4" style="background:#f5f3ff;color:#000"><button class="btn" style="background:#10b981" onclick="verifyOTP()">✅ ভেরিফাই ও লক করুন</button></div><div style="font-size:10px;color:#666;margin-top:10px">একবার লক করলে এই ফোনে ওই নাম্বার ছাড়া ঢুকতে পারবে না</div></div></div>

<div id="welcomeOverlay"><div style="background:#fff;color:#000;padding:24px;border-radius:20px;text-align:center;width:100%;max-width:340px"><div style="font-size:50px">🎉</div><div id="bonusBox" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:14px;border-radius:14px;font-size:24px;font-weight:800;margin:12px 0">1120 TK বোনাস 💰</div><button class="btn" style="background:#6d4cff" onclick="closeWelcome()">🚀 শুরু করুন</button></div></div>
<div id="adOverlay"><h2>⏳ বিজ্ঞাপন...</h2><div id="timer" style="font-size:60px">15</div><div style="background:#fff3;width:80%;height:8px;border-radius:20px;margin-top:10px"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div></div>

<!-- HOME -->
<div id="p-home" class="page active">
<div class="slider blinkBox2"><div class="slide active" id="s1" style="background:linear-gradient(90deg,#f59e0b,#ef4444)"><span id="st1">🎉 Daily Bonus</span></div><div class="slide" id="s2" style="background:linear-gradient(90deg,#06b6d4,#3b82f6)"><span id="st2">📢 Sponsored</span></div><div class="slide" id="s3" style="background:linear-gradient(90deg,#10b981,#06b6d4)"><span id="st3">💰 Bonus</span></div><div class="slide" id="s4" style="background:linear-gradient(90deg,#6d4cff,#8b5cf6)"><span id="st4">🚀 Payment</span></div><div class="slide" id="s5" style="background:linear-gradient(90deg,#f59e0b,#ef4444)"><span id="st5">👑 Trusted</span></div><div class="dots"><div class="dot active"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>
<div class="card blinkBox" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4);border:none;text-align:center"><div id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:42px;font-weight:900" id="balMain">৳1120</div><div style="display:flex;gap:8px;justify-content:center;margin-top:10px"><span style="background:#0003;padding:6px 12px;border-radius:20px;font-size:12px" id="c1">Company 0/30</span><span style="background:#0003;padding:6px 12px;border-radius:20px;font-size:12px" id="c2">Popup 0/20</span></div></div>
<div class="card"><button class="btn" style="background:linear-gradient(90deg,#7c3aed,#4f46e5)" onclick="watchAd('company')" id="btn1">📺 COMPANY ADS</button><button class="btn" style="background:#10b981" onclick="watchAd('popup')" id="btn2">💰 POPUP ADS</button><button class="btn" style="background:#1e293b" onclick="goPage('tasks')">📋 TASK BONUS</button></div>
<div class="card" style="border:2px solid #f59e0b"><h3 id="offerTitle">🎉 আজকের স্পেশাল অফার</h3><p style="font-size:12px;color:#aaa" id="offerDesc">100 বোনাস!</p></div>
</div>

<div id="p-tasks" class="page"><div class="card"><h3>📋 Task Bonus</h3><div id="taskList"></div><div id="refLink" style="background:#0003;padding:10px;border-radius:10px;font-size:11px;word-break:break-all;margin-top:10px"></div><button class="btn" style="background:#fff;color:#6d4cff" onclick="copyRef()">📋 লিংক কপি</button></div></div>

<!-- WALLET WITH LOGO ADMIN CONTROL -->
<div id="p-wallet" class="page">
<div class="card" style="background:linear-gradient(135deg,#1e293b,#334155);text-align:center;border:none"><div>ব্যালেন্স</div><div style="font-size:48px;font-weight:900" id="walletBal">৳1120</div><div style="font-size:12px;opacity:.6">Min ৳500</div></div>
<div class="card"><h3>💸 Withdraw Method - লোগো এডমিন থেকে চেঞ্জ</h3>
<div id="bkashOpt" class="payCard active" onclick="selectMethod('bKash')"><div class="payLogo" id="bkashLogoBox"><img id="bkashImg" src="" style="display:none"><span id="bkashTxt">bK</span></div><div style="flex:1"><b id="bkashName">bKash</b><div style="font-size:11px;color:#aaa" id="bkashSub">Personal • Instant Payment</div></div><div style="color:#10b981">✓</div></div>
<div id="nagadOpt" class="payCard" onclick="selectMethod('Nagad')"><div class="payLogo" id="nagadLogoBox"><img id="nagadImg" src="" style="display:none"><span id="nagadTxt">Na</span></div><div style="flex:1"><b id="nagadName">Nagad</b><div style="font-size:11px;color:#aaa" id="nagadSub">Personal • Fast Withdraw</div></div></div>
<input id="accNum" placeholder="01XXXXXXXXX"><input id="amount" type="number" placeholder="500"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f59e0b)" onclick="doWithdraw()">🚀 Withdraw করুন</button>
</div>
<div class="card" style="background:linear-gradient(135deg,#065f46,#047857)"><h3>✅ Withdraw নিয়ম</h3><div style="font-size:13px;margin-top:8px">- মিনিমাম ৳500<br>- Personal নাম্বার<br>- 24 ঘণ্টায় পেমেন্ট</div></div><div class="card"><h3>📜 History</h3><div id="wHistory" style="font-size:12px;color:#aaa">কোনো Withdraw নেই</div></div>
</div>

<div id="p-support" class="page"><div class="card" style="background:linear-gradient(135deg,#6d4cff,#4f46e5);border:none;text-align:center;padding:20px"><div style="background:#0003;padding:10px;border-radius:14px;font-size:13px;font-weight:800" id="supTopMsg">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:20px;font-weight:900;margin-top:12px" id="supCenterTitle">আমরা আছি আপনার পাশে</div><div style="font-size:11px;opacity:.9" id="supCenterSub">২৪ ঘণ্টা সাপোর্ট • 100% Trusted</div></div><div class="card"><h3>🚀 দ্রুত যোগাযোগ করুন</h3><div class="supportItem" onclick="openLink('tele_sup_link')"><div style="width:52px;height:52px;background:#0ea5e9;border-radius:12px;display:flex;align-items:center;justify-content:center">✈️</div><div style="flex:1"><b id="teleSupTitle">Telegram Support</b><div style="font-size:11px;color:#aaa" id="teleSupSub">2 মিনিটে রিপ্লাই</div></div><div>➡️</div></div><div class="supportItem" onclick="openLink('wa_sup_link')"><div style="width:52px;height:52px;background:#22c55e;border-radius:12px;display:flex;align-items:center;justify-content:center">💬</div><div style="flex:1"><b id="waSupTitle">WhatsApp Support</b><div style="font-size:11px;color:#aaa" id="waSupNum">01XXXXXXXXX</div></div><div>➡️</div></div><div class="supportItem" onclick="openLink('email_sup_link')"><div style="width:52px;height:52px;background:#f59e0b;border-radius:12px;display:flex;align-items:center;justify-content:center">📧</div><div style="flex:1"><b id="emailSupTitle">Email Support</b><div style="font-size:11px;color:#aaa" id="emailSupAddr">support@protidinerkajbd.com</div></div><div>➡️</div></div></div><div class="card"><h3>🎥 কিভাবে কাজ করবেন?</h3><div onclick="openVideo()" style="margin-top:10px;background:#000;border:1.5px solid #f59e0b;border-radius:16px;height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer"><div style="width:80px;height:80px;background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:36px">▶️</div><div style="background:#f59e0b;color:#fff;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:800;margin-top:10px" id="tutBtn">Tutorial - 2 মিনিটে শিখুন</div></div></div></div>

<!-- PROFILE 5TH PAGE WITH LOCKING CONTROL -->
<div id="p-profile" class="page">
<div class="card" style="text-align:center"><div style="width:80px;height:80px;border-radius:50%;background:#1e293b;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:40px;overflow:hidden" id="profAv"><img id="profAvImg" src="" style="width:100%;height:100%;object-fit:cover;display:none"><span id="profAvTxt">👤</span></div><h3 id="profName" style="margin-top:10px">User</h3><p id="profPhone" style="font-size:12px;color:#aaa">01XXXXXXXXX</p><p style="font-size:11px;color:#10b981;margin-top:6px">Join: <span id="joinDate"></span></p></div>
<div class="card"><h3>🔒 লকিং সিস্টেম - ইউজার কন্ট্রোল</h3><p style="font-size:11px;color:#aaa">বর্তমান লক নাম্বার: <b id="currentLockNum" style="color:#fff">-</b></p><button class="btn" style="background:#ef4444;margin-top:10px" onclick="logoutLock()">🚪 লগআউট / অন্য নাম্বার দিয়ে লক করুন</button><div style="margin-top:12px"><p style="font-size:12px">প্রোফাইল ছবি URL (এডমিন + ইউজার):</p><input id="profileImgInput" placeholder="https://... ছবির লিংক"><button class="btn" style="background:#6d4cff" onclick="updateProfileImg()">💾 প্রোফাইল ছবি সেভ</button></div></div>
<div class="card"><h3>📊 My Stats</h3><div style="display:flex;gap:8px;margin-top:10px"><div style="flex:1;background:#0e0e20;padding:12px;border-radius:12px;text-align:center"><div style="font-size:20px;font-weight:800" id="statBal">৳0</div><div style="font-size:10px;color:#aaa">Balance</div></div><div style="flex:1;background:#0e0e20;padding:12px;border-radius:12px;text-align:center"><div style="font-size:20px;font-weight:800" id="statTotal">0</div><div style="font-size:10px;color:#aaa">Total Ads</div></div><div style="flex:1;background:#0e0e20;padding:12px;border-radius:12px;text-align:center"><div style="font-size:20px;font-weight:800" id="statTask">0/5</div><div style="font-size:10px;color:#aaa">Tasks</div></div></div></div>
</div>

<div class="btm"><div id="nav-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div><div id="nav-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div><div id="nav-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div><div id="nav-support" onclick="goPage('support')"><span>💬</span>Support</div><div id="nav-profile" onclick="goPage('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=localStorage.getItem('locked_phone')||''; let settings={}; let selected='bKash';
function initApp(){ if(!uid){document.getElementById('lockOverlay').style.display='flex';return;} document.getElementById('lockOverlay').style.display='none'; fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ settings=d.settings; let u=d.user; document.getElementById('balMain').innerText='৳'+u.balance; document.getElementById('walletBal').innerText='৳'+u.balance; document.getElementById('statBal').innerText='৳'+u.balance; document.getElementById('statTotal').innerText=u.total; document.getElementById('statTask').innerText=u.tasks_done.length+'/5'; document.getElementById('profName').innerText=u.name; document.getElementById('profPhone').innerText=u.phone; document.getElementById('joinDate').innerText=u.join_date; document.getElementById('currentLockNum').innerText=u.phone; document.getElementById('balTitle').innerText=settings.balance_title; document.getElementById('offerTitle').innerText=settings.offer_title; document.getElementById('offerDesc').innerText=settings.offer_desc; document.getElementById('supTopMsg').innerText=settings.support_top_msg; document.getElementById('supCenterTitle').innerText=settings.support_center_title; document.getElementById('supCenterSub').innerText=settings.support_center_sub; document.getElementById('teleSupTitle').innerText=settings.tele_sup_title; document.getElementById('teleSupSub').innerText=settings.tele_sup_sub; document.getElementById('waSupTitle').innerText=settings.wa_sup_title; document.getElementById('waSupNum').innerText=settings.wa_sup_number; document.getElementById('emailSupTitle').innerText=settings.email_sup_title; document.getElementById('emailSupAddr').innerText=settings.email_sup_address; document.getElementById('tutBtn').innerText=settings.tutorial_btn_text;
// bKash Nagad Logo Admin Control
document.getElementById('bkashName').innerText=settings.bkash_name; document.getElementById('bkashSub').innerText=settings.bkash_sub; document.getElementById('nagadName').innerText=settings.nagad_name; document.getElementById('nagadSub').innerText=settings.nagad_sub;
if(settings.bkash_logo && settings.bkash_logo.startsWith('http')){ document.getElementById('bkashImg').src=settings.bkash_logo; document.getElementById('bkashImg').style.display='block'; document.getElementById('bkashTxt').style.display='none'; document.getElementById('bkashLogoBox').style.background='#fff'; }
if(settings.nagad_logo && settings.nagad_logo.startsWith('http')){ document.getElementById('nagadImg').src=settings.nagad_logo; document.getElementById('nagadImg').style.display='block'; document.getElementById('nagadTxt').style.display='none'; document.getElementById('nagadLogoBox').style.background='#fff'; }
// slider + profile img
for(let i=1;i<=5;i++){ let img=settings['slider'+i]; if(img && img.startsWith('http')){ let el=document.getElementById('s'+i); if(el) el.style.background='url('+img+') center/cover'; } }
if(u.profile_img && u.profile_img.startsWith('http')){ document.getElementById('topAvImg').src=u.profile_img; document.getElementById('topAvImg').style.display='block'; document.getElementById('topAvTxt').style.display='none'; document.getElementById('profAvImg').src=u.profile_img; document.getElementById('profAvImg').style.display='block'; document.getElementById('profAvTxt').style.display='none'; }
let tHtml=''; for(let i=1;i<=5;i++){ let title=settings['task'+i+'_title']; if(!title) continue; let bn=settings['task'+i+'_bn']; let rw=settings['task'+i+'_reward']; let icon=settings['task'+i+'_icon']; let done=u.tasks_done.includes(i); tHtml+=`<div class="taskItem"><div style="display:flex;align-items:center;gap:12px"><div style="width:44px;height:44px;background:#1e293b;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px">${icon}</div><div><b>${title}</b><div style="font-size:11px;color:#aaa">${bn} • ৳${rw}</div></div></div><button class="btn" style="width:auto;padding:10px 16px;background:${done?'#10b981':'#6d4cff'}" onclick="doTask(${i})">${done?'✓':`৳${rw}`}</button></div>`; }
document.getElementById('taskList').innerHTML=tHtml; document.getElementById('c1').innerText='Company '+u.ads_today+'/'+settings.company_limit; document.getElementById('c2').innerText='Popup '+u.popup_today+'/'+settings.popup_limit;
let wh=''; d.withdraws.slice(-5).reverse().forEach(w=>{ wh+=`<div style="background:#0e0e20;padding:10px;border-radius:10px;margin-top:6px">💸 ${w.method} ৳${w.amount} - ${w.status}</div>`; }); if(wh) document.getElementById('wHistory').innerHTML=wh;
});}
function sendOTP(){ let p=document.getElementById('phoneInput').value; if(p.length!=11){alert('11 digit নাম্বার দিন');return;} alert('OTP: 1234 (Demo)'); document.getElementById('otpSection').style.display='block';}
function verifyOTP(){ let o=document.getElementById('otpInput').value; let p=document.getElementById('phoneInput').value; if(o!='1234'){alert('OTP ভুল - 1234 দিন');return;} localStorage.setItem('locked_phone',p); uid=p; document.getElementById('lockOverlay').style.display='none'; initApp(); document.getElementById('welcomeOverlay').style.display='flex';}
function closeWelcome(){ document.getElementById('welcomeOverlay').style.display='none'; localStorage.setItem('welcomed_'+uid,'1');}
function goPage(p){ document.querySelectorAll('.page').forEach(e=>e.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on')); document.getElementById('nav-'+p).classList.add('on');}
function watchAd(t){ document.getElementById('adOverlay').style.display='flex'; let tt=15; let ti=setInterval(()=>{tt--; document.getElementById('timer').innerText=tt; document.getElementById('timerProg').style.width=(tt/15*100)+'%'; if(tt<=0){clearInterval(ti); document.getElementById('adOverlay').style.display='none'; fetch('/api/reward?id='+uid+'&type='+t).then(r=>r.json()).then(d=>{alert(d.msg); initApp();});}},1000); if(typeof show_11764581==='function'){show_11764581();}}
function doTask(id){ fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); }); }
function selectMethod(m){ selected=m; document.getElementById('bkashOpt').classList.toggle('active',m==='bKash'); document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad');}
function doWithdraw(){ let a=document.getElementById('amount').value; let n=document.getElementById('accNum').value; if(!a||!n){alert('নাম্বার + এমাউন্ট দিন');return;} fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,amount:a,method:selected})}).then(r=>r.json()).then(d=>{alert(d.msg); initApp();});}
function openLink(k){ let link=settings[k]; if(link) window.open(link,'_blank'); }
function openVideo(){ let link=settings.tutorial_youtube_link; if(link) window.open(link,'_blank'); }
function copyRef(){ navigator.clipboard.writeText(window.location.origin+'/?ref='+uid); alert('✅ কপি');}
function logoutLock(){ if(confirm('লগআউট করে অন্য নাম্বার দিয়ে লক করবেন?')){ localStorage.removeItem('locked_phone'); location.reload(); } }
function updateProfileImg(){ let img=document.getElementById('profileImgInput').value; if(!img.startsWith('http')){alert('https:// লিংক দিন');return;} fetch('/api/profile/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,img:img})}).then(r=>r.json()).then(d=>{alert(d.msg); initApp();});}
initApp();
setInterval(()=>{ let cur=document.querySelector('.slide.active'); if(!cur) return; let next=cur.nextElementSibling; if(!next||!next.classList.contains('slide')){ document.querySelectorAll('.slide').forEach(s=>s.classList.remove('active')); document.querySelectorAll('.dot').forEach(s=>s.classList.remove('active')); document.getElementById('s1').classList.add('active'); document.querySelectorAll('.dot')[0].classList.add('active'); } else { document.querySelectorAll('.slide').forEach(s=>s.classList.remove('active')); document.querySelectorAll('.dot').forEach(s=>s.classList.remove('active')); next.classList.add('active'); let idx=[...document.querySelectorAll('.slide')].indexOf(next); document.querySelectorAll('.dot')[idx].classList.add('active'); } },3000);
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin Master</title><style>*{box-sizing:border-box;font-family:system-ui}body{background:#070710;color:#fff;max-width:700px;margin:0 auto;padding:16px}.card{background:#15152a;border:1px solid #222;border-radius:14px;padding:14px;margin:10px 0}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}.btn{padding:12px 16px;border:none;border-radius:8px;font-weight:800;background:#6d4cff;color:#fff;cursor:pointer;margin-top:8px;width:100%}</style></head><body>
<h2>👑 Master Admin - Logo + Locking + All Pages</h2>
<div class="card" style="border:2px solid #e2136e"><h3>💳 bKash / Nagad লোগো - এডমিন থেকে পরিবর্তন</h3>
bKash Name: <input id="bkash_name"><br>bKash Sub: <input id="bkash_sub"><br>bKash Logo URL: <input id="bkash_logo" placeholder="https://i.ibb.co/.../bkash.png"><br>
Nagad Name: <input id="nagad_name"><br>Nagad Sub: <input id="nagad_sub"><br>Nagad Logo URL: <input id="nagad_logo" placeholder="https://i.ibb.co/.../nagad.png"><br>
<p style="font-size:11px;color:#aaa;margin-top:6px">* Logo URL এ সরাসরি ছবির লিংক দিন, সাথে সাথে Wallet এ চেঞ্জ হবে</p>
</div>
<div class="card" style="border:2px solid #f59e0b"><h3>🖼️ Slider 5 ছবি - উপরের বক্স</h3>
S1 Img: <input id="slider1"> S1 Text: <input id="slider_text1"><br>
S2 Img: <input id="slider2"> S2 Text: <input id="slider_text2"><br>
S3 Img: <input id="slider3"> S3 Text: <input id="slider_text3"><br>
S4 Img: <input id="slider4"> S4 Text: <input id="slider_text4"><br>
S5 Img: <input id="slider5"> S5 Text: <input id="slider_text5"><br>
</div>
<div class="card"><h3>🔒 লকিং সিস্টেম - ইউজার জন্য</h3><p style="font-size:11px;color:#aaa">ইউজার নিজে নাম্বার দিয়ে লক করবে, OTP 1234 দিয়ে ভেরিফাই। এডমিনে কোনো সেটিং লাগে না, অটো কাজ করে। লক নাম্বার = ইউজার ID</p></div>
<div class="card"><h3>📋 Support - YouTube ভিডিও লিংক</h3>Video Link: <input id="tutorial_youtube_link"><br>Telegram Link: <input id="tele_sup_link"><br>WhatsApp Link: <input id="wa_sup_link"><br>Email Link: <input id="email_sup_link"></div>
<button class="btn" onclick="save()">💾 Save - Logo + Locking + All</button><div id="msg" style="color:#10b981;margin-top:10px"></div>
<script>
function load(){ fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{ let s=d.settings; for(let k in s){ let el=document.getElementById(k); if(el) el.value=s[k]; } }); }
function save(){ let data={}; document.querySelectorAll('input').forEach(e=>{ if(e.id) data[e.id]=e.value; }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ document.getElementById('msg').innerText=d.msg; alert(d.msg); }); }
load();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
