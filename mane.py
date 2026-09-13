# -*- coding: utf-8 -*-
# FINAL PRO - Crown at end + Admin name below + Offer Box + Daily Limit + Big Bottom Nav
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'
def default():
    return {"users":{},"withdraws":[],"supports":[],"settings":{"app_name":"Protidiner Kaj BD","app_logo":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","admin_name":"MD Emon - Owner","admin_id":"8807178385","bonus":1120,"ad_reward":2,"popup_reward":3,"task_reward":20,"company_limit":30,"popup_limit":20,"task_limit":5,"min_with":500,"zone":"11764581","offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস! দ্রুত কাজ করুন","offer_active":True},"tasks":[{"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"},{"title":"Telegram Join","reward":20,"link":"https://t.me","icon":"✈️"},{"title":"Facebook Follow","reward":15,"link":"https://facebook.com","icon":"👍"}]}
def load():
    if not os.path.exists(DB): d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save(d): json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
def getu(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":f"User-{uid[-4:]}","pic":"https://cdn-icons-png.flaticon.com/512/149/149071.png","balance":default()["settings"]["bonus"],"ads_today":0,"popup_today":0,"task_today":0,"total":0,"last":today,"claimed":[]}
    u=db["users"][uid]
    if u["last"]!=today: u["ads_today"]=0; u["popup_today"]=0; u["task_today"]=0; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER)
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "Admin only?id=8807178385",403
    return render_template_string(ADMIN)
@app.route('/api/get')
def api_get():
    db=load(); u=getu(db,request.args.get('id','0')); save(db)
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})
@app.route('/api/reward')
def api_reward():
    db=load(); u=getu(db,request.args.get('id')); typ=request.args.get('type','company')
    s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":f"Company Ads লিমিট {s['company_limit']} টা শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"Popup লিমিট {s['popup_limit']} টা শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save(db); return jsonify({"msg":f"৳{s['ad_reward' if typ=='company' else 'popup_reward']} যোগ হয়েছে!"})
@app.route('/api/claim')
def api_claim():
    db=load(); idx=int(request.args.get('idx')); u=getu(db,request.args.get('id')); s=db["settings"]
    if u["task_today"]>=s["task_limit"]: return jsonify({"msg":f"আজ Task লিমিট {s['task_limit']} টা শেষ"})
    if idx in u["claimed"]: return jsonify({"msg":"Done"})
    u["claimed"].append(idx); u["task_today"]+=1; u["balance"]+=db["tasks"][idx]["reward"]; save(db); return jsonify({"msg":"Bonus যোগ হয়েছে"})
@app.route('/api/withdraw',methods=['POST'])
def api_with():
    db=load(); j=request.json; u=getu(db,j['id'])
    if u["balance"]<db["settings"]["min_with"]: return jsonify({"msg":f"Min ৳{db['settings']['min_with']}"})
    db["withdraws"].append({"uid":j['id'],"amt":u["balance"],"num":j['num'],"method":j['method'],"time":str(datetime.now())}); u["balance"]=0; save(db); return jsonify({"msg":"Withdraw গেছে"})
@app.route('/api/support',methods=['POST'])
def api_sup():
    db=load(); j=request.json; db["supports"].append({"uid":j['id'],"msg":j['msg'],"time":str(datetime.now())}); save(db); return jsonify({"msg":"পাঠানো হয়েছে"})
@app.route('/api/profile',methods=['POST'])
def api_profile():
    db=load(); j=request.json; u=getu(db,j['id']); u["name"]=j.get('name',u["name"]); u["pic"]=j.get('pic',u["pic"]); save(db); return jsonify({"msg":"আপডেট হয়েছে"})
@app.route('/api/admin/save',methods=['POST'])
def api_asave():
    db=load(); j=request.json; db["settings"].update(j); save(db); return jsonify({"msg":"Saved"})

USER="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:130px}
.top{background:rgba(10,10,25,0.95);backdrop-filter:blur(20px);padding:12px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,0.08);position:sticky;top:0;z-index:99}
.card{background:linear-gradient(180deg,rgba(255,255,255,0.09),rgba(255,255,255,0.03));border:1px solid rgba(255,255,255,0.1);margin:12px;border-radius:20px;padding:16px}
.btn{width:100%;padding:17px;border:none;border-radius:14px;font-weight:900;font-size:15px;color:#fff;cursor:pointer;margin-top:10px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(12,10,30,0.98);display:flex;padding:12px 0 16px;border-radius:26px 26px 0 0;border-top:1px solid rgba(255,255,255,0.12);z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:13px;font-weight:700;cursor:pointer;line-height:1.2}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block;margin-bottom:2px}
.page{display:none}.page.active{display:block}
.method-card{display:flex;align-items:center;gap:10px;padding:14px;border-radius:14px;border:2px solid transparent;background:#0f0f1f;margin-top:8px;cursor:pointer}.method-card.active{border-color:#6d4cff;background:rgba(109,76,255,0.15)}
.banner{width:100%;height:110px;border-radius:16px;background:linear-gradient(90deg,#4285f4,#34a853,#fbbc05);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:18px;margin-bottom:12px}
input,textarea,select{width:100%;padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.15);background:#0f0f1f;color:#fff;margin-top:8px}
.offer{border:2px solid #fbbf24;background:linear-gradient(135deg,rgba(251,191,36,0.15),rgba(0,0,0,0.3));}
</style></head><body>
<div class="top">
<div style="display:flex;gap:10px;align-items:center">
<img id="appLogo" style="width:44px;height:44px;border-radius:12px;border:2px solid rgba(255,255,255,0.1)">
<div>
<div style="font-weight:900;font-size:17px;display:flex;gap:4px;align-items:center"><span id="appName"></span><span>👑</span></div>
<div style="font-size:12px;opacity:0.7"><span id="adminNameTop"></span></div>
<div style="font-size:11px;color:#00ff88">Zone 11764581 • Auto OFF ✅</div>
</div>
</div>
<div style="display:flex;gap:10px;align-items:center"><img id="userPic" style="width:38px;height:38px;border-radius:50%;border:2px solid #6d4cff"><span style="font-size:20px">🔔</span></div>
</div>

<div id="p-home" class="page active">
<div class="banner">📢 Google Sponsored • Zone 11764581</div>
<div class="card" style="text-align:center"><div style="opacity:0.6;font-size:13px">আপনার ব্যালেন্স</div><div style="font-size:44px;font-weight:900">৳<span id="bal">0</span></div><small>Company <span id="ads">0</span>/<span id="adsLim">30</span> • Popup <span id="pop">0</span>/<span id="popLim">20</span> • Total <span id="total">0</span></small><div style="background:rgba(0,0,0,0.4);height:7px;border-radius:10px;margin-top:10px"><div id="prog" style="height:7px;background:linear-gradient(90deg,#6d4cff,#00ff88);width:0%;border-radius:10px"></div></div></div>

<!-- এডমিন থেকে পরিবর্তন করতে পারবে এমন অফার বক্স -->
<div class="card offer" id="offerBox"><div style="font-weight:900;font-size:15px" id="offerTitle"></div><div style="font-size:13px;opacity:0.8;margin-top:6px" id="offerDesc"></div></div>

<div class="card">
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS দেখুন (৳<span id="r1">2</span>) - <span id="ads2">0</span>/<span id="adsLim2">30</span></button>
<button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS (৳<span id="r2">3</span>) - <span id="pop2">0</span>/<span id="popLim2">20</span></button>
<button class="btn" style="background:#1e293b" onclick="nav('task')">📋 TASK BONUS - <span id="taskLim">5</span> টা/দিন</button>
</div>
</div>

<div id="p-task" class="page"><div class="card"><h3>📋 Task Bonus</h3><small>Daily Limit: <span id="taskLim2"></span> টা - এডমিন থেকে পরিবর্তন করা যাবে</small><div id="taskList" style="margin-top:10px"></div></div></div>
<div id="p-wallet" class="page"><div class="card"><h3>💰 Wallet - ৳<span id="bal2">0</span></h3><div style="margin-top:12px"><b>Method:</b><div class="method-card active" onclick="selMethod('Bkash',this)"><img src="https://i.ibb.co/0jZ3QYv/bkash.png" style="width:36px;height:36px;background:#fff;border-radius:6px"><b>Bkash</b></div><div class="method-card" onclick="selMethod('Nagad',this)"><img src="https://i.ibb.co/6g2y0kQ/nagad.png" style="width:36px;height:36px;background:#fff;border-radius:6px"><b>Nagad</b></div><div class="method-card" onclick="selMethod('Rocket',this)"><img src="https://i.ibb.co/7gY8K2Z/rocket.png" style="width:36px;height:36px;background:#fff;border-radius:6px"><b>Rocket</b></div></div><input id="wNum" placeholder="নাম্বার দিন"><button class="btn" style="background:#00c853" onclick="doWith()">Withdraw</button></div></div>
<div id="p-support" class="page"><div class="card"><h3>💬 Support</h3><textarea id="supMsg"></textarea><button class="btn" style="background:#6d4cff" onclick="doSup()">পাঠান</button></div></div>
<div id="p-profile" class="page"><div class="card" style="text-align:center"><img id="pPic" style="width:80px;height:80px;border-radius:50%;border:3px solid #6d4cff"><h3>👑 <span id="pName"></span></h3></div><div class="card"><input id="newName" placeholder="নতুন নাম"><input id="newPic" placeholder="ছবির লিংক"><button class="btn" style="background:#6d4cff" onclick="saveProfile()">Save</button></div></div>

<div class="btm">
<div class="on" onclick="nav('home')" id="b-home"><span>🏠</span>Home</div>
<div onclick="nav('task')" id="b-task"><span>📋</span>Task</div>
<div onclick="nav('wallet')" id="b-wallet"><span>💰</span>Wallet</div>
<div onclick="nav('support')" id="b-support"><span>💬</span>Support</div>
<div onclick="nav('profile')" id="b-profile"><span>👤</span>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let curMethod='Bkash';
function selMethod(m,el){curMethod=m;document.querySelectorAll('.method-card').forEach(x=>x.classList.remove('active'));el.classList.add('active');}
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());
 document.getElementById('bal').innerText=r.user.balance;document.getElementById('bal2').innerText=r.user.balance;
 document.getElementById('ads').innerText=r.user.ads_today;document.getElementById('pop').innerText=r.user.popup_today;
 document.getElementById('ads2').innerText=r.user.ads_today;document.getElementById('pop2').innerText=r.user.popup_today;
 document.getElementById('adsLim').innerText=r.settings.company_limit;document.getElementById('adsLim2').innerText=r.settings.company_limit;
 document.getElementById('popLim').innerText=r.settings.popup_limit;document.getElementById('popLim2').innerText=r.settings.popup_limit;
 document.getElementById('taskLim').innerText=r.settings.task_limit;document.getElementById('taskLim2').innerText=r.settings.task_limit;
 document.getElementById('total').innerText=r.user.total;document.getElementById('r1').innerText=r.settings.ad_reward;document.getElementById('r2').innerText=r.settings.popup_reward;
 document.getElementById('appName').innerText=r.settings.app_name;document.getElementById('appLogo').src=r.settings.app_logo;
 document.getElementById('adminNameTop').innerText='Admin: '+r.settings.admin_name;
 document.getElementById('userPic').src=r.user.pic;document.getElementById('pPic').src=r.user.pic;document.getElementById('pName').innerText=r.user.name;
 document.getElementById('offerTitle').innerText=r.settings.offer_title;document.getElementById('offerDesc').innerText=r.settings.offer_desc;
 document.getElementById('offerBox').style.display=r.settings.offer_active?'block':'none';
 let prog=((r.user.ads_today+r.user.popup_today)/(r.settings.company_limit+r.settings.popup_limit)*100);document.getElementById('prog').style.width=prog+'%';
 let tl=document.getElementById('taskList');tl.innerHTML='';r.tasks.forEach((t,i)=>{
  let done=r.user.claimed.includes(i);
  tl.innerHTML+=`<div class="card" style="display:flex;justify-content:space-between;align-items:center"><div>${t.icon} ${t.title} - ৳${t.reward}</div><button class="btn" style="width:auto;padding:10px 16px;background:${done?'#334155':'#6d4cff'}" onclick="claim(${i})">${done?'Done':'Claim'}</button></div>`;
 });
}
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');load();}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(x=>x.json()).then(d=>{alert(d.msg);load();});}).catch(e=>{});}
function claim(i){fetch('/api/claim?idx='+i+'&id='+uid).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
function doWith(){let n=document.getElementById('wNum').value;if(!n){alert('Number দিন');return;}fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,method:curMethod})}).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
function doSup(){let m=document.getElementById('supMsg').value;if(!m){alert('লিখুন');return;}fetch('/api/support',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,msg:m})}).then(x=>x.json()).then(d=>{alert(d.msg);document.getElementById('supMsg').value='';});}
function saveProfile(){let nm=document.getElementById('newName').value;let pic=document.getElementById('newPic').value;fetch('/api/profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:nm||undefined,pic:pic||undefined})}).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
load();
</script></body></html>
"""
ADMIN="""
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;padding:16px;background:#0f0f0f;color:#fff}input,textarea{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:10px 0}.btn{padding:12px;width:100%;border:none;border-radius:8px;background:#6d4cff;color:#fff;font-weight:900;cursor:pointer}</style></head><body>
<h2>👑 Admin Panel - সব কিছু এখান থেকে পাল্টাতে পারবে</h2>
<div class="card"><h3>App & Admin Name</h3>App Name (মুকুট শেষে অটো আসবে):<input id="app_name">App Logo URL:<input id="app_logo">Admin Name (নিচে দেখাবে):<input id="admin_name"></div>
<div class="card"><h3>💰 Offer Box - প্রথম পেজে দেখাবে</h3>Offer Title:<input id="offer_title">Offer Description:<textarea id="offer_desc"></textarea>Active: <select id="offer_active" style="width:100%;padding:10px;background:#1a1a1a;color:#fff"><option value="true">Show</option><option value="false">Hide</option></select></div>
<div class="card"><h3>💸 Daily Limit & Taka - তুমি যা সেট করবে তাই হবে</h3>Company Ads Limit (প্রতিদিন):<input id="company_limit" type="number">Company Reward ৳:<input id="ad_reward" type="number">Popup Limit:<input id="popup_limit" type="number">Popup Reward ৳:<input id="popup_reward" type="number">Task Limit:<input id="task_limit" type="number">Min Withdraw:<input id="min_with" type="number"><button class="btn" onclick="save()">💾 Save All - সাথে সাথে অ্যাপে আপডেট হবে</button></div>
<div class="card"><pre id="data" style="font-size:11px;white-space:pre-wrap"></pre></div>
<script>
async function load(){let r=await fetch('/api/get?id=8807178385').then(x=>x.json());document.getElementById('app_name').value=r.settings.app_name;document.getElementById('app_logo').value=r.settings.app_logo;document.getElementById('admin_name').value=r.settings.admin_name;document.getElementById('offer_title').value=r.settings.offer_title;document.getElementById('offer_desc').value=r.settings.offer_desc;document.getElementById('company_limit').value=r.settings.company_limit;document.getElementById('ad_reward').value=r.settings.ad_reward;document.getElementById('popup_limit').value=r.settings.popup_limit;document.getElementById('popup_reward').value=r.settings.popup_reward;document.getElementById('task_limit').value=r.settings.task_limit;document.getElementById('min_with').value=r.settings.min_with;document.getElementById('data').innerText=JSON.stringify(r,null,2);}
async function save(){let d={app_name:document.getElementById('app_name').value,app_logo:document.getElementById('app_logo').value,admin_name:document.getElementById('admin_name').value,offer_title:document.getElementById('offer_title').value,offer_desc:document.getElementById('offer_desc').value,offer_active:document.getElementById('offer_active').value==='true',company_limit:parseInt(document.getElementById('company_limit').value),ad_reward:parseInt(document.getElementById('ad_reward').value),popup_limit:parseInt(document.getElementById('popup_limit').value),popup_reward:parseInt(document.getElementById('popup_reward').value),task_limit:parseInt(document.getElementById('task_limit').value),min_with:parseInt(document.getElementById('min_with').value)};await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});alert('Saved! এখন অ্যাপ রিফ্রেশ করলে সব নতুন দেখাবে');load();}
load();
</script></body></html>
"""
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
