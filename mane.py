# FINAL ONE FILE - ALL FEATURES - BIG ADMIN 8807178385 - REFER + WITHDRAW + USER LINE + COMPANY AD + LOGO
import os, json, time
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
BIG_ADMIN_ID = "8807178385"

def default_db():
    return {"users":{}, "withdraws":[], "settings":{
        "app_name":"Protidiner Kaj BD","top_header_text":"Search or edit profile header...","pro_banner_title":"PRO MEMBER BONUS LIVE NOW","pro_banner_sub":"LIVE NOW","pro_banner_desc":"Unlock 20% extra withdrawal limit • Ends in 12:34:50","pro_bonus_amount":50,
        "bkash_logo":"https://i.ibb.co.com/8g7R2G0/bkash.png","nagad_logo":"https://i.ibb.co.com/BV7W9nH/nagad.png","rocket_logo":"https://i.ibb.co.com/0y0L0p0/rocket.png",
        "welcome_bonus":60,"ad_reward":2,"min_withdraw":1000,"task_cooldown_hours":1,"refer_bonus":20,
        "admin_profile_pic":"https://i.pravatar.cc/150?img=68","admin_real_name":"ADMIN • BIG ADMIN 8807178385","user_line_text":"LIVE USERS - MITMIT - 8807178385",
        "company_ads":[
            {"id":1,"title":"My Company Offer - 50% OFF","img":"https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg","link":"https://t.me","btn":"Shop Now"},
            {"id":2,"title":"New Product Launch","img":"https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg","link":"https://facebook.com","btn":"Visit Now"}
        ]
    },"tasks":[
        {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","btn":"Join & Get 25 Tk"},
        {"title":"Telegram Join","reward":10,"link":"https://t.me","color":"#1e40af","btn":"Join & Get 10 Tk"},
        {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9","btn":"Join & Get 15 Tk"}
    ]}

def load_db():
    if not os.path.exists(DB_FILE): d=default_db(); save_db(d); return d
    with open(DB_FILE,'r',encoding='utf-8') as f: d=json.load(f)
    dd=default_db()
    for k,v in dd["settings"].items():
        if k not in d["settings"]: d["settings"][k]=v
    return d
def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False)
def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}" if uid!=BIG_ADMIN_ID else "BIG ADMIN","real_name":db["settings"]["admin_real_name"],"pic":"","balance":db["settings"]["welcome_bonus"],"task_times":{},"total_earn":db["settings"]["welcome_bonus"],"pro_bonus_date":"","join_time":str(datetime.now())[:19],"referred_by":"","refer_count":0,"refer_earn":0,"total_withdraw":0}
    for k in ["refer_count","refer_earn","total_withdraw","referred_by"]:
        if k not in db["users"][uid]: db["users"][uid][k]=0 if k!="referred_by" else ""
    return db["users"][uid]

@app.route('/health')
def health(): return "OK FINAL",200
@app.route('/')
def index(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin():
    if request.args.get('id')!=BIG_ADMIN_ID: return f"Need?id={BIG_ADMIN_ID}",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id',BIG_ADMIN_ID); ref=request.args.get('ref'); db=load_db()
    is_new=str(uid) not in db["users"]; u=get_user(db,uid)
    if is_new and ref and ref!=uid and ref in db["users"]:
        u["referred_by"]=ref; r=db["users"][ref]; r["refer_count"]=r.get("refer_count",0)+1; r["refer_earn"]=r.get("refer_earn",0)+db["settings"]["refer_bonus"]; r["balance"]+=db["settings"]["refer_bonus"]; r["total_earn"]+=db["settings"]["refer_bonus"]
    save_db(db)
    total_users=len(db["users"]); total_withdraw=sum([w["amount"] for w in db["withdraws"]])
    top_ref=sorted(db["users"].values(), key=lambda x: x.get("refer_count",0), reverse=True)[:20]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"stats":{"total_users":total_users,"online":total_users,"total_withdraw":total_withdraw,"total_withdraw_count":len(db["withdraws"])},"top_referrers":top_ref,"recent_users":list(db["users"].values())[-15:][::-1],"recent_withdraws":db["withdraws"][-20:][::-1],"all_withdraws":db["withdraws"]})

@app.route('/api/reward')
def reward():
    db=load_db(); u=get_user(db,request.args.get('id')); u["balance"]+=db["settings"]["ad_reward"]; u["total_earn"]+=db["settings"]["ad_reward"]; save_db(db); return jsonify({"msg":f"৳{db['settings']['ad_reward']} Added"})
@app.route('/api/pro_bonus')
def pro_bonus():
    db=load_db(); uid=request.args.get('id'); u=get_user(db,uid); today=str(datetime.now().date())
    if u.get("pro_bonus_date")==today: return jsonify({"msg":"⏰ আজকের Bonus নেওয়া হয়েছে"})
    b=int(db["settings"]["pro_bonus_amount"]); u["balance"]+=b; u["total_earn"]+=b; u["pro_bonus_date"]=today; save_db(db); return jsonify({"msg":f"🎁 PRO BONUS ৳{b} Added!"})
@app.route('/api/claim_task')
def claim_task():
    db=load_db(); idx=int(request.args.get('idx')); uid=request.args.get('id'); u=get_user(db,uid); now=time.time(); last=float(u["task_times"].get(str(idx),0)); cd=int(db["settings"]["task_cooldown_hours"])*3600
    if last!=0 and (now-last)<cd: return jsonify({"msg":f"⏰ Wait {int((cd-(now-last))/60)}m"})
    u["task_times"][str(idx)]=now; u["balance"]+=db["tasks"][idx]["reward"]; u["total_earn"]+=db["tasks"][idx]["reward"]; save_db(db); return jsonify({"msg":f"✅ ৳{db['tasks'][idx]['reward']} Added"})
@app.route('/api/withdraw')
def withdraw():
    db=load_db(); uid=request.args.get('id'); amt=int(request.args.get('amount',0)); num=request.args.get('number'); method=request.args.get('method','bKash'); u=get_user(db,uid)
    if amt<db["settings"]["min_withdraw"]: return jsonify({"msg":f"Min {db['settings']['min_withdraw']}"})
    if u["balance"]<amt: return jsonify({"msg":"Low Balance"})
    u["balance"]-=amt; u["total_withdraw"]=u.get("total_withdraw",0)+amt; db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"time":str(datetime.now())[:19],"name":u["name"]}); save_db(db); return jsonify({"msg":f"{method} Withdraw Success - {amt} Tk"})

@app.route('/api/admin/full')
def a_full(): return jsonify(load_db())
@app.route('/api/admin/save_settings',methods=['POST'])
def a_save():
    db=load_db(); j=request.json
    for k,v in j.get("settings",{}).items():
        if k=="company_ads": db["settings"][k]=v
        else:
            if k in ["pro_bonus_amount","task_cooldown_hours","welcome_bonus","ad_reward","min_withdraw","refer_bonus"]:
                try: db["settings"][k]=int(v)
                except: db["settings"][k]=v
            else: db["settings"][k]=v
    if "tasks" in j: db["tasks"]=j["tasks"]
    if "company_ads" in j: db["settings"]["company_ads"]=j["company_ads"]
    save_db(db); return jsonify({"msg":"Saved - Live"})
@app.route('/api/admin/search_user')
def a_search():
    db=load_db(); u=db["users"].get(str(request.args.get('id')))
    if not u: return jsonify({"found":False})
    return jsonify({"found":True,"user":u})
@app.route('/api/admin/update_user',methods=['POST'])
def a_update():
    db=load_db(); j=request.json; uid=str(j.get('target_id')); u=db["users"].get(uid)
    if not u: return jsonify({"msg":"User নাই"})
    if j.get('name'): u['name']=j['name']
    if j.get('real_name'): u['real_name']=j['real_name']
    if j.get('balance') is not None:
        try: u['balance']=int(j['balance'])
        except: pass
    if j.get('pic') is not None: u['pic']=j['pic']
    save_db(db); return jsonify({"msg":f"✅ {uid} Updated - Live"})
@app.route('/api/admin/delete_user')
def a_delete():
    db=load_db(); uid=str(request.args.get('id'));
    if uid in db["users"]: del db["users"][uid]; save_db(db); return jsonify({"msg":"Deleted"})
    return jsonify({"msg":"Not Found"})
@app.route('/api/admin/approve_withdraw')
def a_approve():
    db=load_db(); idx=int(request.args.get('idx',0))
    if 0<=idx<len(db["withdraws"]): db["withdraws"].pop(idx); save_db(db); return jsonify({"msg":"Approved"})

USER_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>FINAL</title><script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script><style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#070e1f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:100px}.top-search{background:#0f1b33;margin:12px;border-radius:24px;padding:12px 16px;display:flex;align-items:center;gap:12px;border:1px solid #1e3a5f}.search-input{flex:1;background:transparent;border:none;color:#8aa0bf;font-size:14px;outline:none}.pro-banner{background:linear-gradient(135deg,#0f3a5f,#0a2a4a);margin:12px;border-radius:18px;padding:16px;display:flex;justify-content:space-between;align-items:center;border:1px solid #1e5a8a;cursor:pointer}.user-line{background:linear-gradient(90deg,#0f172a,#1e293b);margin:12px;border-radius:14px;padding:12px;border:1px solid #22c55e;display:flex;justify-content:space-between}.profile-card{background:#0d1a33;margin:12px;border-radius:20px;padding:18px;display:flex;gap:16px;align-items:center;border:1px solid #1e3a5f}.avatar-ring{width:72px;height:72px;border-radius:50%;padding:3px;background:linear-gradient(135deg,#22c55e,#38bdf8)}.avatar-ring img{width:100%;height:100%;border-radius:50%;object-fit:cover;background:#fff}.balance-card{background:linear-gradient(135deg,#0f2a4a,#0d1f3a);margin:12px;border-radius:16px;padding:16px;border:1px solid #1e3a5f}.mini-cards{display:flex;gap:10px;margin:12px}.mini{flex:1;background:#0d1a33;border-radius:14px;padding:14px;border:1px solid #1e3a5f}.live-box{margin:12px;background:#0a162d;border:2px solid #22c55e;border-radius:16px;padding:16px;box-shadow:0 0 20px rgba(34,197,94,0.4)}.company-ad{margin:12px;border-radius:18px;overflow:hidden;position:relative;border:2px solid #22c55e}.company-ad img{width:100%;height:160px;object-fit:cover}.company-ad-overlay{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.9));padding:14px}.card{background:#162032;margin:12px;border-radius:18px;padding:16px;border:1px solid #22314a}.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;font-size:15px;cursor:pointer}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0a1222;display:flex;border-top:1px solid #1e293b;padding:8px 0 10px 0;z-index:99}.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;padding:8px 2px;font-weight:700;cursor:pointer}.btm div.on{color:#22c55e}.btm div span.icon{font-size:24px;display:block}.inp{width:100%;padding:12px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}.method-card{display:flex;gap:10px;margin-top:12px}.method{flex:1;background:#0f172a;border:2px solid #334155;border-radius:14px;padding:12px;text-align:center;cursor:pointer}.method.active{border-color:#22c55e;background:rgba(34,197,94,0.15)}.method-logo{width:60px;height:60px;border-radius:12px;display:flex;align-items:center;justify-content:center;margin:0 auto;color:#fff;font-weight:900;font-size:11px}.bkash-bg{background:#e2136e}.nagad-bg{background:#f97316}.rocket-bg{background:#7c3aed}</style></head><body>
<div class="top-search"><span onclick="go('more')">☰</span><input class="search-input" id="topSearch" readonly><span onclick="editProfile()">✏️</span></div>
<div class="pro-banner" onclick="claimProBonus()"><div><div style="font-weight:900;font-size:14px"><span id="proTitle"></span> <span style="color:#4ade80" id="proSub"></span></div><div style="font-size:11px;opacity:.7;margin-top:4px" id="proDesc"></div></div><div style="font-size:32px">🎁</div></div>
<div id="p-home">
<div class="user-line"><div><div style="font-weight:900;color:#4ade80;font-size:13px" id="userLineText">LIVE USERS</div><div style="font-size:11px;opacity:.7;margin-top:2px"><span id="totalUsers">0</span> Users • <span id="onlineUsers">0</span> Online • ID: <span id="myId">8807178385</span></div><div style="font-size:10px;color:#fbbf24;margin-top:4px">Refer: <span id="myReferCount">0</span> জন • Earn: ৳<span id="myReferEarn">0</span></div></div><div style="text-align:right"><div style="font-weight:900;color:#22c55e">৳ <span id="totalWithdrawAmt">0</span></div><div style="font-size:10px;opacity:.6"><span id="totalWithdrawCount">0</span> Withdraw</div><div style="font-size:10px;color:#38bdf8;margin-top:4px">You Withdraw: ৳<span id="myWithdraw">0</span></div></div></div>
<div class="profile-card"><div class="avatar-ring"><img id="mainAvatar" src=""></div><div style="flex:1"><div style="font-weight:900;font-size:16px;display:flex;align-items:center;gap:6px"><span id="pRealName">ADMIN</span> 👑<span style="width:20px;height:20px;background:#22c55e;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:12px">✓</span></div><div style="font-size:12px;color:#4ade80;margin-top:2px">📍 <span id="pNameSub">BIG ADMIN</span> • ID: <span id="pIdShow"></span></div></div></div>
<div class="balance-card"><div style="font-size:11px;opacity:.6">TOTAL BALANCE</div><div style="font-size:28px;font-weight:900;color:#4ade80;margin-top:4px">৳ <span id="bal">60</span></div></div>
<div class="mini-cards"><div class="mini" style="border-color:#22c55e"><div style="font-size:10px;opacity:.6">AVAILABLE</div><div style="font-weight:900">৳ <span id="availBal">0</span></div></div><div class="mini"><div style="font-size:10px;opacity:.6">PENDING</div><div style="font-weight:900">৳ 0</div></div></div>
<div id="companyAdsTop"></div>
<div class="live-box"><div style="display:flex;align-items:center;gap:8px"><div style="width:10px;height:10px;background:#22c55e;border-radius:50%"></div><div style="font-weight:900;color:#4ade80">LIVE WITHDRAW - MITMIT - 8807178385</div></div><div style="font-weight:800;margin-top:6px">— up to ৳ 10,000 <span style="color:#4ade80">- MITMIT GREEN LIVE</span></div><button class="btn" style="background:#86efac;color:#000;width:auto;padding:8px 16px;border-radius:20px;margin-top:10px;font-size:13px" onclick="go('wallet')">Withdraw Now →</button></div>
<div class="card"><b>Watch ADS</b><br><button class="btn" style="background:linear-gradient(90deg,#0ea5e9,#0284c7);margin-top:10px" onclick="watchAd()" id="adBtn">Watch ADS</button><div style="margin-top:12px" id="homeTasks"></div></div>
<div id="companyAdsMid"></div>
<div class="card"><b>👥 Live Users - ID সহ - ইউজার দেখতে পাবে</b><div id="recentUsersList" style="margin-top:10px"></div></div>
<div class="card"><b>💸 Live Withdraw - Recent</b><div id="recentWithdrawList" style="margin-top:10px"></div></div>
</div>
<div id="p-wallet" style="display:none"><div class="card"><b>Wallet</b><div style="font-size:36px;font-weight:900;color:#22c55e">৳ <span id="wBal">0</span></div></div><div class="card" style="border:2px solid #22c55e"><b>💰 Select Method - Logo সহ</b><div class="method-card"><div class="method active" id="m-bkash" onclick="selectMethod('bKash')"><div class="method-logo bkash-bg">bKash</div><div style="font-weight:900;margin-top:8px;color:#e2136e">bKash</div></div><div class="method" id="m-nagad" onclick="selectMethod('Nagad')"><div class="method-logo nagad-bg">Nagad</div><div style="font-weight:900;margin-top:8px;color:#f97316">Nagad</div></div><div class="method" id="m-rocket" onclick="selectMethod('Rocket')"><div class="method-logo rocket-bg">Rocket</div><div style="font-weight:900;margin-top:8px;color:#7c3aed">Rocket</div></div></div><input class="inp" id="wAmt" placeholder="Amount" type="number"><input class="inp" id="wNum" placeholder="Number" style="margin-top:10px"><button class="btn" style="background:#22c55e;margin-top:12px" onclick="doWithdraw()">Withdraw Now - <span id="selMethodText">bKash</span></button></div><div class="live-box"><div style="display:flex;align-items:center;gap:8px"><div style="width:12px;height:12px;background:#22c55e;border-radius:50%"></div><div style="font-weight:900;color:#4ade80">Live Withdraw - MITMIT - 8807178385</div></div></div><div id="companyAdsWallet"></div></div>
<div id="p-tasks" style="display:none"><div class="card"><div id="allTasks"></div></div><div id="companyAdsTasks"></div></div>
<div id="p-history" style="display:none"><div class="card"><b>Refer - <span id="referBonus">20</span> Tk - তোমার Refer</b><div class="inp" id="refLink" style="word-break:break-all"></div><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyRef()">Copy Refer Link - ID সহ</button><div style="margin-top:12px"><div style="display:flex;justify-content:space-between"><span>Refer Count:</span><b style="color:#22c55e"><span id="refCount">0</span> জন</b></div><div style="display:flex;justify-content:space-between;margin-top:6px"><span>Refer Earn:</span><b style="color:#22c55e">৳<span id="refEarn">0</span></b></div><div style="display:flex;justify-content:space-between;margin-top:6px"><span>Total Withdraw:</span><b>৳<span id="refWithdraw">0</span></b></div><div style="margin-top:8px;font-size:11px;opacity:.6">Your ID: <span id="refId"></span> • Referred By: <span id="referredBy">None</span></div></div></div></div>
<div id="p-more" style="display:none"><div class="card"><b>Support</b><div id="supDesc" style="white-space:pre-line;margin-top:8px"></div><div style="margin-top:12px"><div class="inp">ID: <span id="moreId"></span><br>Name: <span id="moreName"></span><br>Balance: ৳<span id="moreBal"></span><br>Refer: <span id="moreRefer"></span> জন<br>Withdraw: ৳<span id="moreW"></span></div></div></div></div>
<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span class="icon">🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span class="icon">📋</span>Tasks</div><div id="b-wallet" onclick="go('wallet')"><span class="icon">💰</span>Wallet</div><div id="b-history" onclick="go('history')"><span class="icon">📊</span>History</div><div id="b-more" onclick="go('more')"><span class="icon">⚙️</span>More</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let selectedMethod='bKash';
function go(p){['home','tasks','wallet','history','more'].forEach(x=>{let el=document.getElementById('p-'+x);if(el)el.style.display=x==p?'block':'none';let b=document.getElementById('b-'+x);if(b)b.classList.toggle('on',x==p);});}
function selectMethod(m){selectedMethod=m;document.querySelectorAll('.method').forEach(e=>e.classList.remove('active'));document.getElementById('m-'+m.toLowerCase()).classList.add('active');document.getElementById('selMethodText').innerText=m;}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText).then(()=>alert('✅ Refer Link Copied'));}
function claimProBonus(){fetch('/api/pro_bonus?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function watchAd(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});});}else{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});}}
function visitOnly(i){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{window.open(d.tasks[i].link,'_blank');});}
function claim(i){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{window.open(d.tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});},3000);});}
function doWithdraw(){let a=document.getElementById('wAmt').value;let n=document.getElementById('wNum').value;if(!a||!n){alert('Amount & Number');return;}fetch(`/api/withdraw?id=${uid}&amount=${a}&number=${n}&method=${selectedMethod}`).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function editProfile(){let name=prompt('New Name:');if(name){fetch('/api/admin/update_user',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_id:uid,name:name,real_name:name})}).then(()=>load());}}
function openCompanyAd(l){window.open(l,'_blank');}
function load(){fetch('/api/get_full?id='+uid+'&ref='+new URLSearchParams(location.search).get('ref')||'').then(r=>r.json()).then(d=>{
document.getElementById('topSearch').value=d.settings.top_header_text;document.getElementById('proTitle').innerText=d.settings.pro_banner_title;document.getElementById('proSub').innerText=d.settings.pro_banner_sub;document.getElementById('proDesc').innerText=d.settings.pro_banner_desc;document.getElementById('adBtn').innerText='Watch ADS - ৳'+d.settings.ad_reward;document.getElementById('referBonus').innerText=d.settings.refer_bonus;
document.getElementById('userLineText').innerText=d.settings.user_line_text;document.getElementById('totalUsers').innerText=d.stats.total_users;document.getElementById('onlineUsers').innerText=d.stats.online;document.getElementById('totalWithdrawAmt').innerText=d.stats.total_withdraw;document.getElementById('totalWithdrawCount').innerText=d.stats.total_withdraw_count;
document.getElementById('myId').innerText=d.user.id;document.getElementById('pIdShow').innerText=d.user.id;document.getElementById('refId').innerText=d.user.id;document.getElementById('moreId').innerText=d.user.id;document.getElementById('moreName').innerText=d.user.name;document.getElementById('moreBal').innerText=d.user.balance;document.getElementById('myReferCount').innerText=d.user.refer_count||0;document.getElementById('myReferEarn').innerText=d.user.refer_earn||0;document.getElementById('myWithdraw').innerText=d.user.total_withdraw||0;document.getElementById('moreRefer').innerText=d.user.refer_count||0;document.getElementById('moreW').innerText=d.user.total_withdraw||0;
document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id;document.getElementById('refCount').innerText=d.user.refer_count||0;document.getElementById('refEarn').innerText=d.user.refer_earn||0;document.getElementById('refWithdraw').innerText=d.user.total_withdraw||0;document.getElementById('referredBy').innerText=d.user.referred_by||'None';
document.getElementById('wBal').innerText=d.user.balance;document.getElementById('bal').innerText=d.user.balance;document.getElementById('availBal').innerText=d.user.balance;document.getElementById('pRealName').innerText=d.user.real_name||d.user.name;document.getElementById('pNameSub').innerText=d.user.name;document.getElementById('mainAvatar').src=d.user.pic||d.settings.admin_profile_pic;document.getElementById('minW').innerText=d.settings.min_withdraw;
let adsHtml='';d.settings.company_ads.forEach(ad=>{adsHtml+=`<div class="company-ad" onclick="openCompanyAd('${ad.link}')"><img src="${ad.img}"><div class="company-ad-overlay"><div style="font-weight:900">${ad.title}</div><button class="btn" style="background:#22c55e;width:auto;padding:6px 14px;margin-top:6px;font-size:12px">${ad.btn}</button></div></div>`;});document.getElementById('companyAdsTop').innerHTML=adsHtml;document.getElementById('companyAdsMid').innerHTML=adsHtml;document.getElementById('companyAdsWallet').innerHTML=adsHtml;document.getElementById('companyAdsTasks').innerHTML=adsHtml;
let uHtml='';d.recent_users.forEach(u=>{uHtml+=`<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e293b"><div>👤 ${u.name} • ID:${u.id.slice(-4)} • Ref:${u.referred_by||'None'} • ${u.refer_count||0} Refer</div><div style="color:#22c55e">৳${u.balance}</div></div>`;});document.getElementById('recentUsersList').innerHTML=uHtml;
let wHtml='';d.recent_withdraws.forEach(w=>{wHtml+=`<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e293b"><div>💸 ${w.name} • ID:${w.uid.slice(-4)} • ${w.method} - ${w.number}</div><div style="color:#22c55e">৳${w.amount}</div></div>`;});document.getElementById('recentWithdrawList').innerHTML=wHtml;
let ht='';d.tasks.forEach((t,i)=>{let tt=d.user.task_times?d.user.task_times[String(i)]:0;let now=Date.now()/1000;let cool=d.settings.task_cooldown_hours*3600;let rem=tt?cool-(now-tt):0;if(rem>0){let h=Math.floor(rem/3600);let m=Math.floor((rem%3600)/60);ht+=`<div class="card" style="margin:8px 0"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div style="color:#22c55e">৳${t.reward}</div></div><div style="display:flex;gap:8px;margin-top:10px"><button class="btn" style="background:#dc2626;flex:1" disabled>⏰ ${h}h ${m}m</button><button class="btn" style="background:#334155;flex:1" onclick="visitOnly(${i})">Visit</button></div></div>`;}else{ht+=`<div class="card" style="margin:8px 0"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div style="color:#22c55e">৳${t.reward}</div></div><div style="display:flex;gap:8px;margin-top:10px"><button class="btn" style="background:${t.color};flex:1" onclick="claim(${i})">${t.btn}</button><button class="btn" style="background:#334155;flex:1" onclick="visitOnly(${i})">Visit</button></div></div>`;}});document.getElementById('homeTasks').innerHTML=ht;document.getElementById('allTasks').innerHTML=ht;});}
load();setInterval(load,5000);
</script></body></html>"""

ADMIN_HTML = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>ADMIN FINAL REFER</title><style>body{background:#0f172a;color:#fff;padding:12px;font-family:sans-serif;max-width:900px;margin:0 auto}.card{background:#1e293b;padding:16px;border-radius:14px;margin:12px 0;border:1px solid #2a3f63}input{width:100%;padding:11px;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff;margin:6px 0}button{padding:12px;border:none;border-radius:10px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}label{font-size:11px;opacity:.7;margin-top:8px;display:block;color:#38bdf8}.ad-edit{background:#0f172a;padding:12px;border-radius:12px;margin:10px 0;border:1px solid #334155}.stat{display:flex;gap:10px}.stat div{flex:1;background:#0f172a;padding:14px;border-radius:12px;text-align:center;border:1px solid #22c55e}table{width:100%;font-size:12px;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid #334155;text-align:left}</style></head><body>
<h2 style="color:#22c55e">🔧 ADMIN FINAL - REFER + WITHDRAW - 8807178385</h2>
<div class="stat"><div><div style="font-size:22px;font-weight:900" id="stUsers">0</div><div style="font-size:11px">Total Users</div></div><div><div style="font-size:22px;font-weight:900" id="stWithdraw">0</div><div style="font-size:11px">Withdraw</div></div><div><div style="font-size:22px;font-weight:900" id="stTotal">0</div><div style="font-size:11px">Total ৳</div></div><div><div style="font-size:22px;font-weight:900" id="stRefer">0</div><div style="font-size:11px">Total Refer</div></div></div>

<div class="card" style="border:3px solid #fbbf24"><h3>👑 Profile Edit - ID দিয়ে - Balance + Name + Pic</h3><input id="edit_target_id" value="8807178385"><button style="background:#f59e0b;width:100%" onclick="searchUser()">🔍 Search User - ID দিয়ে দেখো কত Refer, Withdraw</button><div id="userEditBox" style="display:none;margin-top:12px;background:#0f172a;padding:12px;border-radius:12px"><label>Name</label><input id="edit_name"><label>Real Name</label><input id="edit_real_name"><label>Balance</label><input id="edit_balance" type="number"><label>Pic URL</label><input id="edit_pic"><div id="edit_extra" style="margin-top:10px;font-size:12px"></div><div style="display:flex;gap:8px;margin-top:12px"><button style="background:#22c55e;flex:1" onclick="saveUserProfile()">💾 Save Profile</button><button style="background:#dc2626;flex:1" onclick="deleteUser()">🗑️ Delete</button></div></div></div>

<div class="card" style="border:3px solid #22c55e"><h3>🏆 Refer Report - কে কতটা Refer করলো - Admin দেখবে</h3><div id="referLeaderboard"></div></div>

<div class="card" style="border:2px solid #f59e0b"><h3>💸 Withdraw Report - কে কত টাকা Withdraw করলো - ID সহ</h3><div id="withdrawReport"></div></div>

<div class="card" style="border:2px solid #22c55e"><h3>👥 All Users - ID + Refer + Withdraw - সব দেখবে</h3><div id="allUsersReport"></div></div>

<div class="card" style="border:2px solid #38bdf8"><h3>Settings Edit</h3><label>User Line Text</label><input id="user_line_text"><label>Top Header</label><input id="top_header_text"><label>PRO Bonus</label><input id="pro_bonus_amount" type="number"><label>Refer Bonus - 20 Tk</label><input id="refer_bonus" type="number"><label>Min Withdraw</label><input id="min_withdraw" type="number"></div>

<div class="card" style="border:2px solid #22c55e"><h3>🏢 Company Ads - Unlimited</h3><div id="companyAdsEdit"></div><button style="background:#22c55e;width:100%;margin-top:10px" onclick="addCompanyAd()">➕ Add Company Ad</button></div>

<div class="card"><h3>Tasks</h3><div id="tasksEdit"></div><button style="background:#22c55e;width:100%" onclick="addTask()">Add Task</button></div>

<div class="card" style="background:linear-gradient(90deg,#22c55e,#16a34a)"><button style="background:#fff;color:#16a34a;width:100%;padding:20px;font-weight:900;font-size:18px" onclick="saveAll()">💾 SAVE ALL - FINAL</button></div>

<script>let DB={};function load(){fetch('/api/admin/full?id=8807178385').then(r=>r.json()).then(d=>{DB=d;for(let k in d.settings){let el=document.getElementById(k);if(el && typeof d.settings[k]!=='object')el.value=d.settings[k];}
document.getElementById('stUsers').innerText=Object.keys(d.users).length;document.getElementById('stWithdraw').innerText=d.withdraws.length;document.getElementById('stTotal').innerText=d.withdraws.reduce((s,w)=>s+w.amount,0);document.getElementById('stRefer').innerText=Object.values(d.users).reduce((s,u)=>s+(u.refer_count||0),0);
let refHtml='<table><tr style="background:#0f172a"><th>ID</th><th>Name</th><th>Refer Count</th><th>Refer Earn</th><th>Withdraw</th></tr>';let topRef=Object.values(d.users).sort((a,b)=>(b.refer_count||0)-(a.refer_count||0)).slice(0,20);topRef.forEach(u=>{refHtml+=`<tr><td>${u.id}</td><td>${u.name}</td><td style="color:#22c55e;font-weight:900">${u.refer_count||0} জন</td><td>৳${u.refer_earn||0}</td><td>৳${u.total_withdraw||0}</td></tr>`;});refHtml+='</table>';document.getElementById('referLeaderboard').innerHTML=refHtml;
let wHtml='';d.withdraws.slice(-20).reverse().forEach((w,i)=>{wHtml+=`<div style="background:#0f172a;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between"><div>💰 ID:${w.uid} - ${w.name}<br>${w.method} ${w.number} - ৳${w.amount}<br><small>${w.time}</small></div><button style="background:#22c55e" onclick="approveW(${d.withdraws.length-1-i})">Approve</button></div>`;});document.getElementById('withdrawReport').innerHTML=wHtml||'No withdraw';
let allHtml='<table><tr style="background:#0f172a"><th>ID</th><th>Name</th><th>Balance</th><th>Refer</th><th>Withdraw</th><th>Action</th></tr>';Object.values(d.users).forEach(u=>{allHtml+=`<tr><td>${u.id}<br><small>By:${u.referred_by||'Direct'}</small></td><td>${u.name}</td><td>৳${u.balance}</td><td>${u.refer_count||0} জন<br>৳${u.refer_earn||0}</td><td>৳${u.total_withdraw||0}</td><td><button style="background:#334155;padding:4px 8px" onclick="quickEdit('${u.id}')">Edit</button></td></tr>`;});allHtml+='</table>';document.getElementById('allUsersReport').innerHTML=allHtml;
let caHtml='';d.settings.company_ads.forEach((ad,i)=>{caHtml+=`<div class="ad-edit"><b>Ad ${i+1}</b><button style="float:right;background:#dc2626;padding:6px" onclick="delCompanyAd(${i})">Delete</button><label>Title</label><input id="ca_title_${i}" value="${ad.title}"><label>Image</label><input id="ca_img_${i}" value="${ad.img}"><label>Link</label><input id="ca_link_${i}" value="${ad.link}"><label>Btn</label><input id="ca_btn_${i}" value="${ad.btn}"></div>`;});document.getElementById('companyAdsEdit').innerHTML=caHtml;
let h='';d.tasks.forEach((t,i)=>{h+=`<div style="background:#0f172a;padding:10px;border-radius:10px;margin:6px 0"><b>Task ${i+1}</b><input id="task_title_${i}" value="${t.title}"><input id="task_link_${i}" value="${t.link}"><input id="task_reward_${i}" type="number" value="${t.reward}"><input id="task_color_${i}" value="${t.color}"><input id="task_btn_${i}" value="${t.btn}"></div>`;});document.getElementById('tasksEdit').innerHTML=h;
});}
function quickEdit(id){document.getElementById('edit_target_id').value=id;searchUser();window.scrollTo(0,0);}
function addCompanyAd(){DB.settings.company_ads.push({id:Date.now(),title:"New Offer",img:"https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",link:"https://t.me",btn:"Shop Now"});saveTemp();load();}
function delCompanyAd(i){DB.settings.company_ads.splice(i,1);saveTemp();load();}
function addTask(){DB.tasks.push({title:"New",link:"https://t.me",reward:20,color:"#2563eb",btn:"Join"});load();}
function searchUser(){let id=document.getElementById('edit_target_id').value;fetch('/api/admin/search_user?id='+id).then(r=>r.json()).then(d=>{if(!d.found){alert('User নাই');return;}document.getElementById('userEditBox').style.display='block';document.getElementById('edit_name').value=d.user.name;document.getElementById('edit_real_name').value=d.user.real_name;document.getElementById('edit_balance').value=d.user.balance;document.getElementById('edit_pic').value=d.user.pic||'';document.getElementById('edit_extra').innerHTML=`<b>Refer Count:</b> ${d.user.refer_count||0} জন - <b>Earn:</b> ৳${d.user.refer_earn||0}<br><b>Total Withdraw:</b> ৳${d.user.total_withdraw||0}<br><b>Referred By:</b> ${d.user.referred_by||'Direct'}<br><b>Join:</b> ${d.user.join_time||''}`;});}
function saveUserProfile(){let data={target_id:document.getElementById('edit_target_id').value,name:document.getElementById('edit_name').value,real_name:document.getElementById('edit_real_name').value,balance:document.getElementById('edit_balance').value,pic:document.getElementById('edit_pic').value};fetch('/api/admin/update_user',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function deleteUser(){if(!confirm('Delete?'))return;let id=document.getElementById('edit_target_id').value;fetch('/api/admin/delete_user?id='+id).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function approveW(i){fetch('/api/admin/approve_withdraw?idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function saveTemp(){fetch('/api/admin/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:DB.settings,tasks:DB.tasks,company_ads:DB.settings.company_ads})});}
function saveAll(){let s={};['top_header_text','user_line_text','pro_bonus_amount','refer_bonus','min_withdraw'].forEach(k=>{let el=document.getElementById(k);if(el)s[k]=el.value;});let company_ads=[];for(let i=0;i<DB.settings.company_ads.length;i++){let te=document.getElementById('ca_title_'+i);if(!te) continue;company_ads.push({id:DB.settings.company_ads[i].id,title:te.value,img:document.getElementById('ca_img_'+i).value,link:document.getElementById('ca_link_'+i).value,btn:document.getElementById('ca_btn_'+i).value});}let tasks=[];for(let i=0;i<DB.tasks.length;i++){let te=document.getElementById('task_title_'+i);if(!te) continue;tasks.push({title:te.value,link:document.getElementById('task_link_'+i).value,reward:parseInt(document.getElementById('task_reward_'+i).value)||20,color:document.getElementById('task_color_'+i).value,btn:document.getElementById('task_btn_'+i).value});}fetch('/api/admin/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:{...s,company_ads:company_ads},tasks:tasks,company_ads:company_ads})}).then(r=>r.json()).then(x=>{alert('✅ FINAL SAVED');load();});}load();</script></body></html>"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
