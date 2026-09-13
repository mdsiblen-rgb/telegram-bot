# -*- coding: utf-8 -*-
# PRO MAX FINAL - Crown + Profile + Rocket/Bkash/Nagad + Banner + Admin Editable
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'
def default():
    return {"users":{},"withdraws":[],"supports":[],"settings":{"app_name":"Protidiner Kaj BD","app_logo":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","admin_name":"MD Emon","admin_id":"8807178385","admin_logo":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","bonus":1120,"reward":2,"limit":50,"min_with":500,"zone":"11764581","company":"Google Ads Partner","banners":["https://i.ibb.co/2kR5zM2S/google-ads-banner.jpg","https://cdn.dribbble.com/userupload/12345678/file/original.jpg"]},"tasks":[{"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"},{"title":"Telegram Join","reward":20,"link":"https://t.me","icon":"✈️"},{"title":"Facebook Follow","reward":15,"link":"https://facebook.com","icon":"👍"}]}
def load():
    if not os.path.exists(DB):
        d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save(d): json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
def getu(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":f"User-{uid[-4:]}","pic":"https://cdn-icons-png.flaticon.com/512/149/149071.png","balance":db["settings"]["bonus"],"ads_today":0,"total":0,"last":today,"claimed":[]}
    u=db["users"][uid]
    if u["last"]!=today: u["ads_today"]=0; u["last"]=today
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
    db=load(); u=getu(db,request.args.get('id'))
    if u["ads_today"]>=db["settings"]["limit"]: return jsonify({"msg":"আজকের লিমিট শেষ"})
    u["ads_today"]+=1; u["total"]+=1; u["balance"]+=db["settings"]["reward"]; save(db)
    return jsonify({"msg":f"৳{db['settings']['reward']} যোগ হয়েছে!"})
@app.route('/api/claim')
def api_claim():
    db=load(); idx=int(request.args.get('idx')); u=getu(db,request.args.get('id'))
    if idx in u["claimed"]: return jsonify({"msg":"Done"})
    u["claimed"].append(idx); u["balance"]+=db["tasks"][idx]["reward"]; save(db); return jsonify({"msg":"Bonus যোগ হয়েছে"})
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
    db=load(); j=request.json; u=getu(db,j['id']); u["name"]=j.get('name',u["name"]); u["pic"]=j.get('pic',u["pic"]); save(db); return jsonify({"msg":"প্রোফাইল আপডেট হয়েছে"})
@app.route('/api/admin/save',methods=['POST'])
def api_asave():
    db=load(); j=request.json; db["settings"].update(j); save(db); return jsonify({"msg":"Saved"})

USER = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.top{position:sticky;top:0;z-index:99;background:rgba(10,10,25,0.9);backdrop-filter:blur(20px);padding:12px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{background:linear-gradient(180deg,rgba(255,255,255,0.09),rgba(255,255,255,0.03));border:1px solid rgba(255,255,255,0.1);margin:12px;border-radius:20px;padding:16px}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:900;font-size:14px;color:#fff;cursor:pointer;margin-top:10px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(12,10,30,0.97);display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;border-top:1px solid rgba(255,255,255,0.1);z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:10px;cursor:pointer}.btm div.on{color:#fff}
.page{display:none}.page.active{display:block}
.method-card{display:flex;align-items:center;gap:10px;padding:14px;border-radius:14px;border:2px solid transparent;background:#0f0f1f;margin-top:8px;cursor:pointer}
.method-card.active{border-color:#6d4cff;background:rgba(109,76,255,0.15)}
.banner{width:100%;height:120px;border-radius:14px;background:linear-gradient(90deg,#4285f4,#34a853);display:flex;align-items:center;justify-content:center;font-weight:900;margin-bottom:12px}
input,select,textarea{width:100%;padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.15);background:#0f0f1f;color:#fff;margin-top:8px}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><img id="appLogo" style="width:40px;height:40px;border-radius:12px"><div><div style="font-weight:900;display:flex;gap:5px;align-items:center"><span>👑</span><span id="appName"></span></div><small style="color:#00ff88;font-size:11px">Zone 11764581 • Auto OFF ✅</small></div></div><div style="display:flex;gap:8px;align-items:center"><img id="userPic" style="width:34px;height:34px;border-radius:50%;border:2px solid #6d4cff"><span>🔔</span></div></div>

<div id="p-home" class="page active">
<div class="banner" id="compBanner">📢 Google Sponsored • Zone 11764581</div>
<div class="card" style="text-align:center"><div style="opacity:0.6;font-size:13px">আপনার ব্যালেন্স</div><div style="font-size:42px;font-weight:900">৳<span id="bal">0</span></div><small>আজ <span id="ads">0</span>/50 Ads • Total <span id="total">0</span></small><div style="background:rgba(0,0,0,0.4);height:6px;border-radius:10px;margin-top:10px"><div id="prog" style="height:6px;background:linear-gradient(90deg,#6d4cff,#00ff88);width:0%;border-radius:10px"></div></div></div>
<div class="card"><button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS দেখুন (৳2) - Zone 11764581</button><button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS - বেশি ইনকাম</button><button class="btn" style="background:#1e293b" onclick="nav('task')">📋 TASK BONUS</button><button class="btn" style="background:#334155" onclick="nav('profile')">👤 MY PROFILE - নাম/ছবি পাল্টান</button></div>
</div>

<div id="p-task" class="page"><div class="card"><h3>📋 Task Bonus</h3><div id="taskList"></div></div></div>

<div id="p-wallet" class="page">
<div class="card"><h3>💰 Wallet - ৳<span id="bal2">0</span></h3>
<div style="margin-top:12px"><b>Withdraw Method Select করুন:</b>
<div class="method-card active" onclick="selMethod('Bkash',this)"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/BKash_Logo.svg/1200px-BKash_Logo.svg.png" style="width:36px;height:36px;object-fit:contain;background:#fff;border-radius:6px;padding:4px"><div><b>Bkash</b><br><small>পার্সোনাল</small></div></div>
<div class="method-card" onclick="selMethod('Nagad',this)"><img src="https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png" style="width:36px;height:36px;object-fit:contain;background:#fff;border-radius:6px;padding:4px"><div><b>Nagad</b><br><small>পার্সোনাল</small></div></div>
<div class="method-card" onclick="selMethod('Rocket',this)"><img src="https://www.dutch-bangla.com/images/rocket-logo.png" style="width:36px;height:36px;object-fit:contain;background:#fff;border-radius:6px;padding:4px"><div><b>Rocket</b><br><small>DBBL</small></div></div>
</div>
<input id="wNum" placeholder="আপনার নাম্বার দিন"><button class="btn" style="background:#00c853;margin-top:12px" onclick="doWith()">Withdraw করুন</button><small style="opacity:0.6">Min ৳500 • 24h এ পেমেন্ট</small></div>
</div>

<div id="p-support" class="page"><div class="card"><h3>💬 Support Box</h3><textarea id="supMsg" placeholder="আপনার সমস্যা লিখুন..."></textarea><button class="btn" style="background:#6d4cff" onclick="doSup()">পাঠান</button></div><div class="card"><b>📞 Admin:</b> <span id="adminName"></span></div></div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center"><img id="pPic" style="width:80px;height:80px;border-radius:50%;border:3px solid #6d4cff"><h3 style="margin-top:10px">👑 <span id="pName"></span></h3></div>
<div class="card"><b>প্রোফাইল পাল্টান</b><input id="newName" placeholder="নতুন নাম"><input id="newPic" placeholder="ছবির লিংক (https://...)"><button class="btn" style="background:#6d4cff" onclick="saveProfile()">Save করুন</button><small style="opacity:0.6">আপনি চাইলে নিজের নাম ও ছবি পাল্টাতে পারবেন, এডমিন প্যানেল থেকেও পাল্টানো যাবে</small></div>
</div>

<div class="btm">
<div class="on" onclick="nav('home')" id="b-home">🏠<br>Home</div>
<div onclick="nav('task')" id="b-task">📋<br>Task</div>
<div onclick="nav('wallet')" id="b-wallet">💰<br>Wallet</div>
<div onclick="nav('support')" id="b-support">💬<br>Support</div>
<div onclick="nav('profile')" id="b-profile">👤<br>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let curMethod='Bkash';
function selMethod(m,el){curMethod=m;document.querySelectorAll('.method-card').forEach(x=>x.classList.remove('active'));el.classList.add('active');}
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());
 document.getElementById('bal').innerText=r.user.balance;document.getElementById('bal2').innerText=r.user.balance;
 document.getElementById('ads').innerText=r.user.ads_today;document.getElementById('total').innerText=r.user.total;
 document.getElementById('prog').style.width=(r.user.ads_today/50*100)+'%';
 document.getElementById('appName').innerText=r.settings.app_name;document.getElementById('appLogo').src=r.settings.app_logo;
 document.getElementById('adminName').innerText=r.settings.admin_name+' ('+r.settings.admin_id+')';
 document.getElementById('userPic').src=r.user.pic;document.getElementById('pPic').src=r.user.pic;document.getElementById('pName').innerText=r.user.name;
 let tl=document.getElementById('taskList');tl.innerHTML='';r.tasks.forEach((t,i)=>{
  let done=r.user.claimed.includes(i);
  tl.innerHTML+=`<div class="card" style="display:flex;justify-content:space-between;align-items:center"><div>${t.icon} ${t.title} - ৳${t.reward}</div><button class="btn" style="width:auto;padding:10px 16px;background:${done?'#334155':'#6d4cff'}" onclick="claim(${i})">${done?'Done':'Claim'}</button></div>`;
 });
}
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');load();}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে...');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid).then(x=>x.json()).then(d=>{alert(d.msg);load();});}).catch(e=>{});}
function claim(i){fetch('/api/claim?idx='+i+'&id='+uid).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
function doWith(){let n=document.getElementById('wNum').value;if(!n){alert('Number দিন');return;}fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:n,method:curMethod})}).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
function doSup(){let m=document.getElementById('supMsg').value;if(!m){alert('লিখুন');return;}fetch('/api/support',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,msg:m})}).then(x=>x.json()).then(d=>{alert(d.msg);document.getElementById('supMsg').value='';});}
function saveProfile(){let nm=document.getElementById('newName').value;let pic=document.getElementById('newPic').value;fetch('/api/profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:nm||undefined,pic:pic||undefined})}).then(x=>x.json()).then(d=>{alert(d.msg);load();});}
load();
</script></body></html>
"""

ADMIN = """
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;padding:16px;background:#0f0f0f;color:#fff}input{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:10px 0}.btn{padding:12px;width:100%;border:none;border-radius:8px;background:#6d4cff;color:#fff;font-weight:900;cursor:pointer}</style></head><body>
<h2>👑 Admin Panel - Protidiner Kaj BD</h2>
<div class="card"><h3>App Settings - এখানে সব পাল্টাতে পারবে</h3>
App Name: <input id="app_name"><br>App Logo URL: <input id="app_logo"><br>Admin Name: <input id="admin_name"><br>Admin ID: <input id="admin_id"><br>Bonus: <input id="bonus" type="number"><br>Per Ad Reward: <input id="reward" type="number"><br>Min Withdraw: <input id="min_with" type="number"><br>
<button class="btn" onclick="save()">Save All - সব পাল্টে যাবে</button></div>
<div class="card"><h3>Live Data</h3><pre id="data" style="white-space:pre-wrap;font-size:12px"></pre></div>
<script>
async function load(){let r=await fetch('/api/get?id=8807178385').then(x=>x.json());document.getElementById('app_name').value=r.settings.app_name;document.getElementById('app_logo').value=r.settings.app_logo;document.getElementById('admin_name').value=r.settings.admin_name;document.getElementById('admin_id').value=r.settings.admin_id;document.getElementById('bonus').value=r.settings.bonus;document.getElementById('reward').value=r.settings.reward;document.getElementById('min_with').value=r.settings.min_with;document.getElementById('data').innerText=JSON.stringify(r,null,2);}
async function save(){let d={app_name:document.getElementById('app_name').value,app_logo:document.getElementById('app_logo').value,admin_name:document.getElementById('admin_name').value,admin_id:document.getElementById('admin_id').value,bonus:parseInt(document.getElementById('bonus').value),reward:parseInt(document.getElementById('reward').value),min_with:parseInt(document.getElementById('min_with').value)};await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});alert('Saved - এখন ইউজার অ্যাপে 👑 সহ নতুন নাম/লোগো দেখাবে');load();}
load();
</script></body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
