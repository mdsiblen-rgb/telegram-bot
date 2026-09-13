# -*- coding: utf-8 -*-
# Protidiner Kaj BD - FINAL CLEAN A-Z 1-5 + Number Lock + Logo Admin Control
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
            "bonus":1120,
            "ad_reward":2,
            "popup_reward":3,
            "company_limit":30,
            "popup_limit":20,
            "task_limit":5,
            "min_with":500,
            "bkash_logo":"",
            "nagad_logo":"",
            "bkash_name":"bKash Personal",
            "nagad_name":"Nagad Personal",
            "zone":"11764581",
            "support_link":"https://t.me/"
        },
        "tasks":[
            {"id":1,"title":"Telegram Channel Join","reward":25,"icon":"✈️","desc":"চ্যানেলে জয়েন করুন"},
            {"id":2,"title":"YouTube Subscribe","reward":30,"icon":"▶️","desc":"সাবস্ক্রাইব করুন"},
            {"id":3,"title":"Facebook Page Like","reward":20,"icon":"👍","desc":"পেজে লাইক দিন"},
            {"id":4,"title":"Refer Friend","reward":50,"icon":"👥","desc":"১ জন রেফার = ৳50"},
            {"id":5,"title":"Daily Check-in","reward":15,"icon":"✅","desc":"প্রতিদিন একবার"}
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
                db["settings"]["bkash_logo"]=""
                db["settings"]["nagad_logo"]=""
                db["settings"]["bkash_name"]="bKash Personal"
                db["settings"]["nagad_name"]="Nagad Personal"
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
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","balance":db["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":today,"phone":uid}
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
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":"Limit শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":"Limit শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save_db(db); return jsonify({"msg":f"৳{s['ad_reward'] if typ=='company' else s['popup_reward']} যোগ হয়েছে"})
@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid)
    if tid in u["tasks_done"]: return jsonify({"msg":"আজকে করা হয়েছে"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    if not t: return jsonify({"msg":"Task নেই"})
    u["tasks_done"].append(tid); u["balance"]+=t["reward"]; u["total"]+=1; save_db(db)
    return jsonify({"msg":f"✅ {t['title']} ৳{t['reward']}"})
@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"status":"Pending","time":str(datetime.now())[:16]})
    save_db(db); return jsonify({"msg":f"✅ {method} ৳{amt} Request সফল"})
@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db(); j=request.json
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ Save হয়েছে - Logo সহ সব"})
@app.route('/api/admin/balance',methods=['POST'])
def admin_balance():
    db=load_db(); j=request.json; uid=str(j.get('phone')); amt=int(j.get('amount',0)); typ=j.get('type','add')
    if uid not in db["users"]: return jsonify({"msg":"ইউজার পাওয়া যায়নি"})
    if typ=='add': db["users"][uid]["balance"]+=amt
    else: db["users"][uid]["balance"]-=amt
    if db["users"][uid]["balance"]<0: db["users"][uid]["balance"]=0
    save_db(db); return jsonify({"msg":f"✅ {uid} {typ} {amt} TK - New {db['users'][uid]['balance']}"})

# --- USER HTML - FULL 1-5 PAGES CLEAN ---
USER_HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD</title>
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:120px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;position:sticky;top:0;z-index:99;border-bottom:1px solid #222}
.card{margin:12px;border-radius:18px;padding:16px;background:#15152a;border:1px solid #222}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;margin-top:8px;cursor:pointer;background:linear-gradient(135deg,#6d4cff,#8b5cf6)}
.page{display:none}.page.active{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0e0e20;display:flex;padding:10px 0;border-radius:20px 20px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:20px;display:block}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #222;border-radius:14px;padding:12px;margin:8px 0;cursor:pointer}
.payCard.active{border-color:#e2136e;background:#1a1a35}
.payLogo{width:48px;height:48px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;overflow:hidden;background:#333}
.payLogo img{width:100%;height:100%;object-fit:cover}
#lockOverlay,#welcomeOverlay,#adOverlay{position:fixed;inset:0;z-index:999;display:none;justify-content:center;align-items:center;padding:20px}
#lockOverlay{display:flex;background:#070710f2}
#welcomeOverlay{background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2)}
#adOverlay{background:#000e;flex-direction:column;color:#fff}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:8px}
</style></head><body>

<div class="top"><div><b>💎 Protidiner Kaj BD</b><div style="font-size:10px;color:#aaa">FINAL A-Z 1-5 CLEAN</div></div><div style="width:40px;height:40px;border-radius:50%;background:#222;display:flex;align-items:center;justify-content:center" onclick="goPage('profile')">👤</div></div>

<!-- LOCK -->
<div id="lockOverlay">
<div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:350px;text-align:center">
<div style="font-size:44px">🔐</div>
<h2 style="color:#6d4cff;margin:8px 0">নাম্বার দিয়ে লক করুন</h2>
<p style="font-size:13px;color:#000;font-weight:800">নাম্বার দিয়ে লক করুন, নাম্বার দিয়ে লগইন করুন</p>
<p style="font-size:11px;color:#666;margin-top:4px">একই নাম্বারে টাকা যাবে, সুরক্ষিত থাকবে</p>
<input id="phoneInput" type="tel" placeholder="01XXXXXXXXX" maxlength="11" style="background:#f5f3ff;color:#000">
<button class="btn" id="sendBtn" onclick="sendOTP()">📲 OTP পাঠান</button>
<div id="otpSection" style="display:none">
<input id="otpInput" type="text" placeholder="OTP 1234" maxlength="4" style="background:#f5f3ff;color:#000">
<button class="btn" onclick="verifyOTP()">✅ ভেরিফাই</button>
<p style="font-size:10px;color:#888;margin-top:4px">ডেমো OTP: 1234</p>
</div>
</div>
</div>

<!-- WELCOME -->
<div id="welcomeOverlay">
<div style="background:#fff;color:#000;padding:24px;border-radius:20px;width:100%;max-width:350px;text-align:center">
<div style="font-size:56px">🎉</div><h2 style="color:#6d4cff">স্বাগতম!</h2>
<div id="bonusBox" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:14px;border-radius:14px;font-size:28px;font-weight:800;margin:12px 0">1120 TK বোনাস 💰</div>
<p style="font-size:11px;color:#666">আপনি <b id="bonusText">1120 TK</b> বোনাস পেয়েছেন<br>নাম্বার <b id="welcomePhone"></b> লক হয়েছে</p>
<button class="btn" onclick="closeWelcome()">🚀 কাজ শুরু করুন</button>
</div>
</div>

<!-- PAGE 1 HOME -->
<div id="p-home" class="page active">
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5)">
<div style="font-size:12px;opacity:.9">আপনার বর্তমান ব্যালেন্স</div>
<div style="font-size:34px;font-weight:800" id="balMain">0 TK</div>
<div style="font-size:11px;background:#fff2;padding:4px 10px;border-radius:20px;display:inline-block;margin-top:6px" id="uidShow">ID: -</div>
</div>
<div class="card"><h3>🎬 Page 1 - Company Ads</h3><button class="btn" onclick="watchAd('company')">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button><p id="adText" style="text-align:right;font-size:11px;color:#aaa;margin-top:6px">0/30</p></div>
<div class="card"><h3>📢 Page 1 - Popup Ads</h3><button class="btn" style="background:#0ea5e9" onclick="watchAd('popup')">👁️ Popup Ad দেখুন</button><p id="popText" style="text-align:right;font-size:11px;color:#aaa;margin-top:6px">0/20</p></div>
<div class="card"><h3>🔗 Page 1 - রেফার লিংক</h3><div id="refLink" style="background:#0e0e20;border:1px dashed #6d4cff;padding:10px;border-radius:10px;word-break:break-all;font-size:12px;margin-top:6px"></div><button class="btn" style="background:#fbbf24;color:#000" onclick="copyRef()">📋 কপি করুন</button></div>
</div>

<!-- PAGE 2 TASKS -->
<div id="p-tasks" class="page">
<div class="card"><h3>🎯 Page 2 - ডেইলি টাস্ক - 5 টা</h3><div id="taskList"></div></div>
</div>

<!-- PAGE 3 INVITE -->
<div id="p-invite" class="page">
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);text-align:center">
<h1 style="font-size:44px">50 TK</h1><p>Page 3 - প্রতি রেফারে</p>
<div id="refLink2" style="background:#fff2;padding:10px;border-radius:10px;margin-top:10px;font-size:12px;word-break:break-all"></div>
<button class="btn" style="background:#fff;color:#6d4cff" onclick="copyRef()">Invite কপি</button>
</div>
</div>

<!-- PAGE 4 WALLET -->
<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><div style="font-size:11px;color:#aaa">Page 4 - Wallet</div><h1 id="bal2" style="font-size:36px;color:#6d4cff">0 TK</h1><div style="font-size:11px;background:#dcfce7;color:#166534;padding:4px 10px;border-radius:20px;display:inline-block">🔒 Locked: <span id="lockedNumShow">-</span></div></div>
<div class="card"><h3>🏦 Page 4 - টাকা তুলুন - Logo Admin Control</h3>
<div id="bkashOpt" class="payCard active" onclick="selectMethod('bKash')"><div class="payLogo" style="background:#e2136e"><img id="bkashImg" src="" style="display:none"><span id="bkashTxt">bK</span></div><div style="flex:1"><b id="bkashName">bKash Personal</b><div style="font-size:10px;color:#aaa">লক নাম্বারে যাবে</div></div><div>✓</div></div>
<div id="nagadOpt" class="payCard" onclick="selectMethod('Nagad')"><div class="payLogo" style="background:#f6921e"><img id="nagadImg" src="" style="display:none"><span id="nagadTxt">NG</span></div><div style="flex:1"><b id="nagadName">Nagad Personal</b><div style="font-size:10px;color:#aaa">লক নাম্বারে যাবে</div></div></div>
<input id="accNum" readonly placeholder="Locked Number"><input id="amount" type="number" placeholder="Amount - Min 500"><button class="btn" onclick="doWithdraw()">💸 Withdraw করুন</button><div id="wHistory" style="margin-top:10px"></div></div>
</div>

<!-- PAGE 5 PROFILE -->
<div id="p-profile" class="page">
<div class="card" style="text-align:center"><div style="width:80px;height:80px;border-radius:50%;background:#222;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:32px">👤</div><h3 id="uName" style="margin-top:10px">User</h3><p style="font-size:11px;color:#aaa">ID: <span id="uidShow2">-</span></p><div style="background:#0e0e20;padding:10px;border-radius:10px;margin-top:10px;font-size:12px;text-align:left"><b>🔒 Locked Number:</b> <span id="profilePhone">-</span><br><b>💰 Bonus:</b> <span id="profileBonus">1120 TK</span></div></div>
<div class="card"><h3>💬 Support</h3><button class="btn" style="background:#0ea5e9" onclick="window.open('https://t.me/','_blank')">📩 Telegram</button></div>
</div>

<div id="adOverlay"><h2>⏳ বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:60px;font-weight:800">15</div><div style="background:#fff3;width:80%;height:8px;border-radius:20px;margin-top:10px;overflow:hidden"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div></div>

<div class="btm">
<div id="nav-home" class="on" onclick="goPage('home')"><span>🏠</span>Home<br>Page 1</div>
<div id="nav-tasks" onclick="goPage('tasks')"><span>🎯</span>Tasks<br>Page 2</div>
<div id="nav-invite" onclick="goPage('invite')"><span>👥</span>Invite<br>Page 3</div>
<div id="nav-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet<br>Page 4</div>
<div id="nav-profile" onclick="goPage('profile')"><span>👤</span>Profile<br>Page 5</div>
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
  document.getElementById('balMain').innerText=u.balance+' TK';
  document.getElementById('bal2').innerText=u.balance+' TK';
  document.getElementById('uidShow').innerText='ID: '+uid;
  document.getElementById('uidShow2').innerText=uid;
  document.getElementById('lockedNumShow').innerText=uid;
  document.getElementById('profilePhone').innerText=uid;
  document.getElementById('welcomePhone').innerText=uid;
  document.getElementById('accNum').value=uid;
  document.getElementById('uName').innerText=u.name;
  document.getElementById('bonusBox').innerText=settings.bonus+' TK বোনাস 💰';
  document.getElementById('bonusText').innerText=settings.bonus+' TK';
  document.getElementById('profileBonus').innerText=settings.bonus+' TK';
  document.getElementById('bkashName').innerText=settings.bkash_name;
  document.getElementById('nagadName').innerText=settings.nagad_name;
  if(settings.bkash_logo && settings.bkash_logo.startsWith('http')){
   document.getElementById('bkashImg').src=settings.bkash_logo;
   document.getElementById('bkashImg').style.display='block';
   document.getElementById('bkashTxt').style.display='none';
  }
  if(settings.nagad_logo && settings.nagad_logo.startsWith('http')){
   document.getElementById('nagadImg').src=settings.nagad_logo;
   document.getElementById('nagadImg').style.display='block';
   document.getElementById('nagadTxt').style.display='none';
  }
  document.getElementById('adText').innerText=u.ads_today+'/'+settings.company_limit;
  document.getElementById('popText').innerText=u.popup_today+'/'+settings.popup_limit;
  document.getElementById('refLink').innerText=window.location.origin+'?start='+uid;
  document.getElementById('refLink2').innerText=window.location.origin+'?start='+uid;
  let tHtml=''; d.tasks.forEach(t=>{
   let done=u.tasks_done.includes(t.id);
   tHtml+=`<div style="display:flex;justify-content:space-between;align-items:center;background:#0e0e20;padding:10px;border-radius:10px;margin:8px 0"><div><b>${t.icon} ${t.title}</b><div style="font-size:10px;color:#aaa">${t.desc}</div></div><button class="btn" style="width:auto;padding:8px 12px;background:${done?'#10b981':'#6d4cff'}" onclick="doTask(${t.id})">${done?'✓ Done':t.reward+' TK'}</button></div>`;
  });
  document.getElementById('taskList').innerHTML=tHtml;
  let wh=''; d.withdraws.slice(-5).reverse().forEach(w=>{ wh+=`<div style="background:#0e0e20;padding:8px;border-radius:8px;margin-top:6px;font-size:11px">💸 ${w.method} ৳${w.amount} - ${w.status}</div>`; });
  document.getElementById('wHistory').innerHTML=wh;
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
 if(typeof show_11764581==='function'){ show_11764581(); }
}
function doTask(id){
 fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); });
}
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('✅ কপি হয়েছে'); }
function selectMethod(m){ selected=m; document.getElementById('bkashOpt').classList.toggle('active',m==='bKash'); document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad'); }
function doWithdraw(){
 let a=document.getElementById('amount').value;
 let n=document.getElementById('accNum').value;
 fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,amount:a,method:selected})}).then(r=>r.json()).then(d=>{ alert(d.msg); initApp(); });
}
initApp();
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin Panel</title>
<style>*{box-sizing:border-box;font-family:system-ui}body{background:#070710;color:#fff;max-width:700px;margin:0 auto;padding:16px}.card{background:#15152a;border:1px solid #222;border-radius:14px;padding:14px;margin:10px 0}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}.btn{padding:10px 16px;border:none;border-radius:8px;font-weight:800;background:#6d4cff;color:#fff;cursor:pointer;margin-top:8px}table{width:100%;border-collapse:collapse;margin-top:8px}th,td{border:1px solid #333;padding:6px;font-size:11px}th{background:#0e0e20}</style></head><body>
<h2>👑 Admin Panel - A-Z Full + Logo Control</h2>
<div class="card"><h3>⚙️ General Settings</h3>
App Name: <input id="app_name"><br>
Bonus Welcome: <input id="bonus" type="number"><br>
Ad Reward: <input id="ad_reward" type="number"><br>
Min Withdraw: <input id="min_with" type="number"><br>
<button class="btn" onclick="save()">💾 Save Settings</button>
</div>
<div class="card"><h3>🖼️ bKash / Nagad Logo Change - এডমিন থেকে পরিবর্তন করুন</h3>
<p style="font-size:11px;color:#aaa">এখানে লিংক বসালে App এ লোগো চেঞ্জ হবে</p>
bKash Name: <input id="bkash_name" placeholder="bKash Personal"><br>
bKash Logo URL: <input id="bkash_logo" placeholder="https://i.ibb.co/.../bkash.png"><br>
Nagad Name: <input id="nagad_name" placeholder="Nagad Personal"><br>
Nagad Logo URL: <input id="nagad_logo" placeholder="https://i.ibb.co/.../nagad.png"><br>
<button class="btn" onclick="save()">💾 Logo Save করুন</button>
</div>
<div class="card"><h3>💸 Balance Add/Minus</h3>
<input id="admPhone" placeholder="Phone 01XXXXXXXXX">
<input id="admAmount" type="number" placeholder="Amount">
<div style="display:flex;gap:8px"><button class="btn" style="background:#10b981" onclick="bal('add')">+ যোগ</button><button class="btn" style="background:#ef4444" onclick="bal('minus')">- মাইনাস</button></div>
<div id="admMsg" style="font-size:12px;margin-top:6px"></div>
</div>
<div class="card"><h3>👥 All Users - Locked Numbers</h3><div id="userList"></div></div>
<div class="card"><h3>💰 Withdraw List</h3><div id="withdrawList"></div></div>
<script>
function load(){
 fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{
  let s=d.settings;
  document.getElementById('app_name').value=s.app_name||'';
  document.getElementById('bonus').value=s.bonus||1120;
  document.getElementById('ad_reward').value=s.ad_reward||2;
  document.getElementById('min_with').value=s.min_with||500;
  document.getElementById('bkash_name').value=s.bkash_name||'';
  document.getElementById('nagad_name').value=s.nagad_name||'';
  document.getElementById('bkash_logo').value=s.bkash_logo||'';
  document.getElementById('nagad_logo').value=s.nagad_logo||'';
  let uhtml='<table><tr><th>Phone</th><th>Name</th><th>Balance</th></tr>';
  Object.values(d.all_users).forEach(u=>{ uhtml+=`<tr><td>${u.phone}</td><td>${u.name}</td><td>${u.balance}</td></tr>`; });
  uhtml+='</table>'; document.getElementById('userList').innerHTML=uhtml;
  let whtml='<table><tr><th>Phone</th><th>Amt</th><th>Method</th><th>Time</th></tr>';
  d.all_withdraws.slice(-30).reverse().forEach(w=>{ whtml+=`<tr><td>${w.uid}</td><td>${w.amount}</td><td>${w.method}</td><td>${w.time}</td></tr>`; });
  whtml+='</table>'; document.getElementById('withdrawList').innerHTML=whtml;
 });
}
function save(){
 let data={};
 document.querySelectorAll('input').forEach(e=>{ if(e.id &&!e.id.startsWith('adm')) data[e.id]=e.value; });
 fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ alert(d.msg); load(); });
}
function bal(t){
 let p=document.getElementById('admPhone').value;
 let a=document.getElementById('admAmount').value;
 fetch('/api/admin/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:p,amount:a,type:t})}).then(r=>r.json()).then(d=>{ document.getElementById('admMsg').innerText=d.msg; alert(d.msg); load(); });
}
load();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
