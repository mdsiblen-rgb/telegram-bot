# -*- coding: utf-8 -*-
# FINAL A-Z - Thin Balance + Full Task Page + Admin Control
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def default():
    return {
        "users":{},
        "settings":{
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","app_logo":"👑","admin_profile":"","admin_profile_img":"","zone":"11764581","bonus":1120,"ad_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"task_limit":5,"min_with":500,
            "official_banners":[],"google_ads":["🎉 Daily Bonus Available Today","⭐ Official Ad • bKash • Nagad • Daraz • Trusted","📢 Company Sponsored • 100% Safe"],
            "offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!","balance_title":"আপনার বর্তমান ব্যালেন্স"
        },
        "tasks":[
            {"id":1,"title":"Telegram Channel Join","reward":25,"icon":"✈️","link":"https://t.me/","desc":"চ্যানেলে জয়েন করুন"},
            {"id":2,"title":"YouTube Subscribe","reward":30,"icon":"▶️","link":"https://youtube.com/","desc":"সাবস্ক্রাইব + লাইক করুন"},
            {"id":3,"title":"Facebook Page Like","reward":20,"icon":"👍","link":"https://facebook.com/","desc":"পেজে লাইক দিন"},
            {"id":4,"title":"Refer Friend","reward":50,"icon":"👨‍👩‍👧‍👦","link":"","desc":"১ জন রেফার = ৳50"},
            {"id":5,"title":"Daily Check-in","reward":15,"icon":"✅","link":"","desc":"প্রতিদিন একবার"}
        ]
    }

def load():
    if not os.path.exists(DB): d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
    try: return json.load(open(DB,'r',encoding='utf-8'))
    except: d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
def save(d): json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
def getu(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"balance":db["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today}
    u=db["users"][uid]
    if u["last"]!=today: u["ads_today"]=0; u["popup_today"]=0; u["tasks_done"]=[]; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only",403
    return render_template_string(ADMIN)
@app.route('/api/get')
def api_get(): db=load(); u=getu(db,request.args.get('id','0')); save(db); return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})
@app.route('/api/reward')
def api_reward():
    db=load(); u=getu(db,request.args.get('id')); typ=request.args.get('type','company'); s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":"Limit শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":"Limit শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save(db); return jsonify({"msg":f"৳{s['ad_reward' if typ=='company' else 'popup_reward']} যোগ হয়েছে ✅"})
@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=getu(db,uid); s=db["settings"]
    if tid in u["tasks_done"]: return jsonify({"msg":"এই Task আজকে করা হয়েছে"})
    if len(u["tasks_done"])>=s["task_limit"]: return jsonify({"msg":f"আজকে {s['task_limit']} টা Task লিমিট শেষ"})
    task=next((t for t in db["tasks"] if t["id"]==tid),None)
    if not task: return jsonify({"msg":"Task পাওয়া যায়নি"})
    u["tasks_done"].append(tid); u["balance"]+=task["reward"]; u["total"]+=1; save(db)
    return jsonify({"msg":f"✅ {task['title']} - ৳{task['reward']} যোগ হয়েছে"})
@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load(); j=request.json
    for k in j:
        if k.startswith("google_ad"):
            try: idx=int(k[-1])-1; db["settings"]["google_ads"][idx]=j[k]
            except: pass
        elif k.startswith("task_"):
            try:
                # task_1_title, task_1_reward, task_1_link etc
                parts=k.split('_'); tid=int(parts[1]); field=parts[2]
                for t in db["tasks"]:
                    if t["id"]==tid:
                        if field=="reward": t[field]=int(j[k])
                        else: t[field]=j[k]
            except: pass
        else: db["settings"][k]=j[k]
    save(db); return jsonify({"msg":"✅ Saved - সাথে সাথে আপডেট"})
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
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:800;font-size:14px;color:#fff;margin-top:10px;cursor:pointer}
.profile{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#1e293b,#334155);display:flex;align-items:center;justify-content:center;border:2px solid #6d4cff;overflow:hidden;box-shadow:0 0 15px rgba(109,76,255,0.4);font-size:26px}
.profile img{width:100%;height:100%;object-fit:cover}
@keyframes blinkGlow{0%{box-shadow:0 0 10px rgba(245,158,11,0.3)}50%{box-shadow:0 0 28px rgba(245,158,11,0.85),0 0 45px rgba(239,68,68,0.5)}100%{box-shadow:0 0 10px rgba(245,158,11,0.3)}}
@keyframes shineMove{0%{left:-100%}100%{left:200%}}
.bannerBox{margin:12px;border-radius:22px;overflow:hidden;height:168px;background:linear-gradient(90deg,#f59e0b,#ef4444);position:relative;border:2px solid rgba(255,255,255,0.15);animation:blinkGlow 2.2s infinite ease-in-out}
.bannerBox img{width:100%;height:100%;object-fit:cover}
.bannerText{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.9));padding:30px 14px 12px;font-weight:800;text-align:center;font-size:14px}
.shine{position:absolute;top:0;left:-100%;width:65%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35),transparent);transform:skewX(-20deg);animation:shineMove 2.8s infinite;z-index:2}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
.taskCard{display:flex;justify-content:space-between;align-items:center;background:#15152a;border:1px solid #2a2a4a;border-radius:14px;padding:12px;margin:10px 0}
.taskDone{opacity:0.5;pointer-events:none}
</style></head><body>

<div class="top">
<div style="display:flex;align-items:center;gap:10px">
<div style="font-size:28px" id="appLogo">👑</div>
<div>
<div style="font-weight:900;font-size:16px;display:flex;align-items:center;gap:6px"><span id="appName">Protidiner Kaj BD</span><span style="background:#22c55e;color:#fff;font-size:10px;padding:2px 6px;border-radius:6px">✓</span></div>
<div style="font-size:11px;opacity:0.6" id="adminName">Admin: SHIBLI NOMAN</div>
</div>
</div>
<div class="profile" id="profBox">👤</div>
</div>

<div id="p-home" class="page active">
<div class="bannerBox" id="bannerBox"><div class="shine"></div><div style="height:100%;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:800" id="gAd">Loading...</div></div>

<!-- টাকার বক্স - এখন চিকন ও সুন্দর -->
<div class="card" style="text-align:center;background:linear-gradient(135deg,#1e3a8a,#2563eb,#06b6d4,#10b981);padding:20px 16px;border:1px solid rgba(255,255,255,0.18);box-shadow:0 8px 30px rgba(59,130,246,0.25)">
<div class="shine"></div>
<div style="font-size:11px;letter-spacing:1.5px;color:#c7d2fe;font-weight:600;opacity:0.9" id="balTitle">আপনার বর্তমান ব্যালেন্স</div>
<div style="font-size:44px;font-weight:500;margin:8px 0;color:#fff;letter-spacing:0.5px;font-family:'Inter',system-ui">৳<span id="bal" style="font-weight:700">0</span></div>
<div style="display:flex;justify-content:center;gap:6px;flex-wrap:wrap">
<span style="background:rgba(0,0,0,0.3);padding:5px 10px;border-radius:20px;font-size:11px">Company <b id="ads" style="color:#fde68a">0</b>/<span id="adsLim">30</span></span>
<span style="background:rgba(0,0,0,0.3);padding:5px 10px;border-radius:20px;font-size:11px">Popup <b id="pop" style="color:#86efac">0</b>/<span id="popLim">20</span></span>
<span style="background:rgba(0,0,0,0.3);padding:5px 10px;border-radius:20px;font-size:11px">Total <b id="total">0</b></span>
</div>
<div style="background:rgba(0,0,0,0.35);height:6px;border-radius:20px;margin-top:14px;overflow:hidden"><div id="prog" style="height:100%;background:linear-gradient(90deg,#fde68a,#fbbf24);width:0%;border-radius:20px;transition:width 1s"></div></div>
</div>

<div class="card">
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS (৳<span id="r1">2</span>) - <span id="ads2">0</span>/<span id="adsLim2">30</span></button>
<button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS (৳<span id="r2">3</span>) - <span id="pop2">0</span>/<span id="popLim2">20</span></button>
<button class="btn" style="background:#1e293b" onclick="nav('task')">📋 TASK BONUS - 5 টা/দিন দেখুন</button>
</div>
<div class="card" style="border:1.5px solid #fbbf24;background:linear-gradient(135deg,rgba(251,191,36,0.12),#0e0e20)"><div style="font-weight:800;font-size:14px" id="offerTitle"></div><div style="font-size:12px;margin-top:5px;opacity:0.85" id="offerDesc"></div></div>
</div>

<div id="p-task" class="page">
<div class="card"><h3 style="font-size:16px">📋 Task Bonus - দিনে 5 টা</h3><p style="font-size:12px;opacity:0.6;margin-top:4px">Task complete করলে সাথে সাথে টাকা যোগ হবে</p><div id="taskList" style="margin-top:12px"></div></div>
</div>

<div id="p-wallet" class="page"><div class="card"><h3>💰 Wallet - ৳<span id="bal2">0</span></h3><p style="font-size:12px;opacity:0.6;margin-top:8px">Min Withdraw ৳500</p></div></div>
<div id="p-support" class="page"><div class="card"><h3>💬 Support</h3><p style="margin-top:8px">Telegram: @SHIBLI</p></div></div>
<div id="p-profile" class="page"><div class="card"><h3>👤 Profile</h3><p style="margin-top:8px">ID: <span id="uid"></span></p><p>Balance: ৳<span id="bal3">0</span></p></div></div>

<div class="btm">
<div class="on" id="b-home" onclick="nav('home')"><span>🏠</span>Home</div>
<div id="b-task" onclick="nav('task')"><span>📋</span>Task</div>
<div id="b-wallet" onclick="nav('wallet')"><span>💰</span>Wallet</div>
<div id="b-support" onclick="nav('support')"><span>💬</span>Support</div>
<div id="b-profile" onclick="nav('profile')"><span>👤</span>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let gAds=[],banners=[],idx=0,currentTasks=[],userData=null;
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');}
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());let s=r.settings;let u=r.user;userData=u;currentTasks=r.tasks;
 bal.innerText=u.balance;bal2.innerText=u.balance;bal3.innerText=u.balance;ads.innerText=u.ads_today;pop.innerText=u.popup_today;ads2.innerText=u.ads_today;pop2.innerText=u.popup_today;total.innerText=u.total;
 adsLim.innerText=s.company_limit;adsLim2.innerText=s.company_limit;popLim.innerText=s.popup_limit;popLim2.innerText=s.popup_limit;
 r1.innerText=s.ad_reward;r2.innerText=s.popup_reward;appName.innerText=s.app_name;adminName.innerText='Admin: '+s.admin_name;appLogo.innerText=s.app_logo;balTitle.innerText='💰 '+s.balance_title;offerTitle.innerText=s.offer_title;offerDesc.innerText=s.offer_desc;
 gAds=s.google_ads;banners=s.official_banners||[];prog.style.width=((u.ads_today+u.popup_today)/(s.company_limit+s.popup_limit)*100)+'%';
 uidEl=document.getElementById('uid');if(uidEl) uidEl.innerText=uid;
 let pb=document.getElementById('profBox');if(s.admin_profile_img && s.admin_profile_img.startsWith('data:image')){pb.innerHTML=`<img src="${s.admin_profile_img}">`;}else{pb.innerHTML='👤';}
 renderBanner(); renderTasks();
}
function renderBanner(){
 let box=document.getElementById('bannerBox');
 if(banners.length>0){box.innerHTML=`<div class="shine"></div><img src="${banners[idx % banners.length]}"><div class="bannerText">${gAds[idx % gAds.length]||''}</div>`;}
 else{box.innerHTML=`<div class="shine"></div><div style="height:100%;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:800;background:linear-gradient(90deg,#f59e0b,#ef4444)">${gAds[idx % gAds.length]||''}</div>`;}
}
function renderTasks(){
 let tl=document.getElementById('taskList');tl.innerHTML='';
 currentTasks.forEach(t=>{
  let done=userData.tasks_done.includes(t.id);
  tl.innerHTML+=`<div class="taskCard ${done?'taskDone':''}"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:24px">${t.icon}</div><div><div style="font-weight:700;font-size:13px">${t.title}</div><div style="font-size:11px;opacity:0.6">${t.desc||''} • ৳${t.reward}</div></div></div><button class="btn" style="width:auto;padding:10px 14px;margin:0;font-size:12px;background:${done?'#333':'#6d4cff'}" onclick="doTask(${t.id})">${done?'✅ Done':'৳'+t.reward}</button></div>`;
 });
}
async function doTask(tid){
 let t=currentTasks.find(x=>x.id==tid);
 if(t.link && t.link.startsWith('http')){window.open(t.link,'_blank');}
 // 2 sec por verify
 setTimeout(async()=>{
  if(confirm(t.title+' - Complete করেছেন? Verify করলে টাকা যোগ হবে')){
   let res=await fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:tid})}).then(x=>x.json());
   alert(res.msg); load();
  }
 },1500);
}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে...');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে...');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
setInterval(()=>{idx++;renderBanner();},3000);
load();
</script></body></html>
"""

ADMIN="""
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#0f0f0f;color:#fff;font-family:sans-serif;padding:14px}input,textarea{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}.card{background:#1e1e1e;padding:14px;border-radius:12px;margin:10px 0}.btn{padding:12px;width:100%;border:none;border-radius:8px;background:#6d4cff;color:#fff;font-weight:800;margin-top:6px;cursor:pointer}.prev{width:100%;height:120px;border-radius:10px;object-fit:cover;margin-top:6px;border:1px solid #333;display:none}.prev2{width:70px;height:70px;border-radius:50%;object-fit:cover;display:none}</style>
</head><body>
<h2>👑 Admin - Full Control</h2>

<div class="card" style="border:1.5px solid #f59e0b">
<h3>⭐ Official Banner (মিট মিট বড় বক্স)</h3>
<input type="file" id="bannerFile" accept="image/*"><img id="bannerPrev" class="prev">
<button class="btn" style="background:#f59e0b" onclick="uploadBanner()">📸 ব্যানার যোগ (5 টা পর্যন্ত)</button>
<button class="btn" style="background:#ef4444" onclick="clearBanner()">🗑️ সব মুছুন</button>
<div id="bannerCount" style="font-size:11px;margin-top:6px"></div>
</div>

<div class="card" style="border:1.5px solid #6d4cff">
<h3>👤 প্রোফাইল ছবি (52px বড়)</h3>
<input type="file" id="fileIn" accept="image/*"><img id="preview" class="prev2">
<button class="btn" style="background:#00c853" onclick="uploadImg()">📤 প্রোফাইল আপলোড</button>
</div>

<div class="card"><h3>📝 নাম ও লোগো</h3>App Name:<input id="app_name">Admin Name:<input id="admin_name">Logo:<input id="app_logo">Balance Title:<input id="balance_title"></div>
<div class="card"><h3>📢 Ad Text (ঘুরবে)</h3>Ad 1:<input id="g1">Ad 2:<input id="g2">Ad 3:<input id="g3"></div>

<div class="card" style="border:1.5px solid #00c853">
<h3>📋 Task Page - সব এডমিন থেকে চেঞ্জ (5 টা)</h3>
<div id="taskAdmin"></div>
<p style="font-size:11px;opacity:0.6">Link খালি রাখলে শুধু Verify হবে, লিংক দিলে ওই লিংকে যাবে</p>
</div>

<div class="card">Offer Title:<input id="offer_title">Offer Desc:<textarea id="offer_desc"></textarea></div>
<div class="card">Company Limit:<input id="company_limit" type="number">Reward:<input id="ad_reward" type="number">Popup Limit:<input id="popup_limit" type="number">Reward:<input id="popup_reward" type="number">Task Limit:<input id="task_limit" type="number"></div>

<button class="btn" style="background:#6d4cff;padding:16px;font-size:15px" onclick="save()">💾 Save All</button>
<div id="msg" style="text-align:center;margin-top:10px;color:#fde047;font-weight:800"></div>

<script>
let base64="",banner64="";
fileIn.addEventListener('change',e=>{let r=new FileReader();r.onload=ev=>{base64=ev.target.result;preview.src=base64;preview.style.display='block';};r.readAsDataURL(e.target.files[0]);});
bannerFile.addEventListener('change',e=>{let r=new FileReader();r.onload=ev=>{banner64=ev.target.result;bannerPrev.src=banner64;bannerPrev.style.display='block';};r.readAsDataURL(e.target.files[0]);});
async function uploadImg(){if(!base64){alert('ছবি সিলেক্ট করো');return;}let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({img:base64})}).then(x=>x.json());msg.innerText=res.msg;}
async function uploadBanner(){if(!banner64){alert('ব্যানার সিলেক্ট করো');return;}let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({banner:banner64})}).then(x=>x.json());msg.innerText=res.msg;load();banner64='';}
async function clearBanner(){if(!confirm('মুছবে?'))return;let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({clear_banner:1})}).then(x=>x.json());msg.innerText=res.msg;load();}

async function load(){
 let data=await fetch('/api/get?id=8807178385').then(x=>x.json());let s=data.settings;let tasks=data.tasks;
 app_name.value=s.app_name;admin_name.value=s.admin_name;app_logo.value=s.app_logo;balance_title.value=s.balance_title;
 g1.value=s.google_ads[0];g2.value=s.google_ads[1];g3.value=s.google_ads[2];offer_title.value=s.offer_title;offer_desc.value=s.offer_desc;
 company_limit.value=s.company_limit;ad_reward.value=s.ad_reward;popup_limit.value=s.popup_limit;popup_reward.value=s.popup_reward;task_limit.value=s.task_limit;
 bannerCount.innerText=`ব্যানার ${s.official_banners.length}/5`;
 if(s.admin_profile_img){preview.src=s.admin_profile_img;preview.style.display='block';base64=s.admin_profile_img;}
 let ta=document.getElementById('taskAdmin');ta.innerHTML='';
 tasks.forEach(t=>{
  ta.innerHTML+=`<div style="border:1px solid #333;padding:10px;border-radius:8px;margin:8px 0;background:#151515">
  <b>Task ${t.id}</b> Title:<input id="task_${t.id}_title" value="${t.title}"> Icon:<input id="task_${t.id}_icon" value="${t.icon}"> Reward:<input id="task_${t.id}_reward" type="number" value="${t.reward}"> Link:<input id="task_${t.id}_link" value="${t.link||''}"> Desc:<input id="task_${t.id}_desc" value="${t.desc||''}">
  </div>`;
 });
}
async function save(){
 let d={app_name:app_name.value,admin_name:admin_name.value,app_logo:app_logo.value,balance_title:balance_title.value,google_ad1:g1.value,google_ad2:g2.value,google_ad3:g3.value,offer_title:offer_title.value,offer_desc:offer_desc.value,company_limit:parseInt(company_limit.value),ad_reward:parseInt(ad_reward.value),popup_limit:parseInt(popup_limit.value),popup_reward:parseInt(popup_reward.value),task_limit:parseInt(task_limit.value)};
 document.querySelectorAll('[id^="task_"]').forEach(inp=>{d[inp.id]=inp.value;});
 let res=await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(x=>x.json());msg.innerText=res.msg;
}
load();
</script></body></html>
"""
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
