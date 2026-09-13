# -*- coding: utf-8 -*-
# FINAL A-Z - 11764581 - 8807178385 - 5 Button Working + Company Banner
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE='database.json'

def default_db():
    return {"users":{},"withdraws":[],
        "settings":{
            "app_name":"প্রতিদিনের কাজ BD",
            "logo":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "welcome_bonus":60,"ad_reward":2,"ad_limit":30,"min_withdraw":1000,
            "official_title":"অফিসিয়াল নোটিস","official_desc":"প্রতিদিন Ads দেখুন - Token 11764581",
            "banner1":"https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2":"https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3":"https://img.freepik.com/free-vector/earning-money-online-concept-landing-page_52683-25203.jpg",
            "support_tg":"https://t.me/ProtidinerKajBD",
            "wallet_title":"💳 Withdraw নিয়ম","wallet_desc":"১. Min ৳1000\n২. ২৪ ঘন্টায় পেমেন্ট\n৩. ভুল নাম্বারে দায় আপনার",
            "company_banner_title":"📢 Sponsored by Company"
        },
        "tasks":[
            {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626"},
            {"title":"Telegram Join","reward":10,"link":"https://t.me/ProtidinerKajBD","color":"#1e40af"},
            {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9"},
            {"title":"Website Visit","reward":20,"link":"https://google.com","color":"#7c3aed"},
            {"title":"Group Join","reward":20,"link":"https://t.me","color":"#0f766e"},
            {"title":"Post Like","reward":20,"link":"https://t.me","color":"#be123c"},
            {"title":"Post Share","reward":20,"link":"https://t.me","color":"#065f46"},
            {"title":"Comment","reward":20,"link":"https://t.me","color":"#2563eb"},
            {"title":"Refer 3 Friend","reward":20,"link":"https://t.me","color":"#d97706"}
        ]}

def load_db():
    if not os.path.exists(DB_FILE):
        d=default_db(); save_db(d); return d
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"balance":db["settings"]["welcome_bonus"],"ads_today":0,"last_date":today,"claimed":[],"total_earn":db["settings"]["welcome_bonus"]}
    u=db["users"][uid]
    if u.get("last_date")!=today: u["ads_today"]=0; u["last_date"]=today
    return u

@app.route('/')
def index(): return render_template_string(HTML)
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "Need?id=8807178385"
    return render_template_string(ADMIN_HTML)
@app.route('/api/get')
def api_get():
    db=load_db(); u=get_user(db,request.args.get('id','8807178385')); save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})
@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id'))
    if u["ads_today"]>=db["settings"]["ad_limit"]: return jsonify({"msg":"আজকের লিমিট শেষ"})
    u["balance"]+=db["settings"]["ad_reward"]; u["total_earn"]+=db["settings"]["ad_reward"]; u["ads_today"]+=1; save_db(db)
    return jsonify({"msg":f"৳{db['settings']['ad_reward']} পেয়েছেন"})
@app.route('/api/claim')
def api_claim():
    db=load_db(); idx=int(request.args.get('idx')); u=get_user(db,request.args.get('id'))
    if idx in u["claimed"]: return jsonify({"msg":"Already Done"})
    u["claimed"].append(idx); u["balance"]+=db["tasks"][idx]["reward"]; u["total_earn"]+=db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg":"Task Complete"})
@app.route('/api/admin/full')
def admin_full(): return jsonify(load_db())
@app.route('/api/admin/save',methods=['POST'])
def admin_save():
    db=load_db(); j=request.json
    for k,v in j.items():
        if k in db["settings"]: db["settings"][k]=v
        if k=="tasks": db["tasks"]=v
    save_db(db); return jsonify({"msg":"Saved"})

HTML="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}
body{background:#0a1222;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.top{background:linear-gradient(135deg,#1e3a8a,#0f172a);padding:14px;border-radius:0 0 24px 24px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bal{color:#22c55e;font-size:38px;font-weight:900}
.card{background:#162032;margin:12px;border-radius:18px;padding:14px;border:1px solid #23344a}
.bigbtn{width:100%;padding:18px;border:none;border-radius:14px;font-weight:900;font-size:17px;color:#fff;cursor:pointer;margin-top:10px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#121d32;display:flex;border-top:2px solid #22c55e;padding:6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#94a3b8;font-size:11px;padding:8px;cursor:pointer}.btm div.on{color:#38bdf8;background:#1e293b;border-radius:12px}
.slider{margin:12px;border-radius:18px;overflow:hidden;height:160px;position:relative;border:1px solid #23344a}.slides{display:flex;width:300%;transition:0.6s}.slide{min-width:100%;height:160px}.slide img{width:100%;height:160px;object-fit:cover}
.page{display:none}.page.active{display:block}
.live-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;animation:blink 1s infinite}@keyframes blink{0%{opacity:1}50%{opacity:0}100%{opacity:1}}
</style></head><body>
<div class="top"><div><div id="appName" style="font-weight:900"></div><div class="bal" id="bal">৳0</div><div id="adsInfo" style="font-size:12px"></div></div><div style="text-align:right"><div style="background:#22c55e;color:#000;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:900"><span class="live-dot"></span> LIVE</div><img id="logo" style="width:42px;height:42px;border-radius:50%;border:2px solid #22c55e;margin-top:6px"></div></div>

<div id="page-home" class="page active">
<div class="card" style="border-color:#22c55e;display:flex;justify-content:space-between"><div><b id="offTitle"></b><br><small id="offDesc"></small></div><div style="color:#22c55e">● LIVE</div></div>
<div class="slider"><div class="slides" id="slides"><div class="slide"><img id="b1"></div><div class="slide"><img id="b2"></div><div class="slide"><img id="b3"></div></div></div>
<div class="card" style="border:2px dashed #38bdf8;text-align:center;background:#0d1f4a"><small style="color:#38bdf8" id="compTitle">Sponsored</small><div id="companyAdBox" style="margin:10px 0;background:#000;border-radius:12px;padding:8px"><img src="https://img.freepik.com/free-vector/gradient-sale-landing-page-template_52683-24288.jpg" style="width:100%;height:90px;object-fit:cover;border-radius:10px"><div style="font-size:12px;margin-top:6px">কোম্পানির ব্যানার - 45 সেকেন্ড পর পর আপডেট হবে</div></div><button class="bigbtn" style="background:#22c55e;color:#000" onclick="watchAd()">▶️ ADS দেখুন - বড় বাটন</button></div>
<div id="homeTasks"></div>
</div>

<div id="page-tasks" class="page"><div class="card"><b>📋 আজকের টাস্ক</b></div><div id="tasksList"></div></div>
<div id="page-refer" class="page"><div class="card"><h3>👥 Refer</h3><div id="refLink" style="background:#0f172a;padding:12px;border-radius:10px;margin-top:8px;word-break:break-all"></div><button class="bigbtn" style="background:#22c55e;color:#000" onclick="copyRef()">📋 Copy Link</button></div></div>
<div id="page-wallet" class="page"><div class="card"><h3>💰 Wallet</h3><div id="wBal" style="font-size:36px;color:#22c55e;font-weight:900"></div><button class="bigbtn" style="background:#22c55e;color:#000">💸 Withdraw</button></div><div class="card"><b id="wTitle"></b><br><small id="wDesc" style="white-space:pre-line"></small></div></div>
<div id="page-profile" class="page"><div class="card" style="text-align:center"><img id="pLogo" style="width:90px;height:90px;border-radius:50%;border:3px solid #22c55e"><h3 id="pApp"></h3><p id="pEarn"></p></div></div>

<div class="btm">
<div class="on" onclick="goPage('home',this)">🏠<br>Home</div>
<div onclick="goPage('tasks',this)">✅<br>Tasks</div>
<div onclick="goPage('refer',this)">👥<br>Refer</div>
<div onclick="goPage('wallet',this)">💰<br>Wallet</div>
<div onclick="goPage('profile',this)">👤<br>Profile</div>
</div>

<script>
let DB=null, UID=localStorage.getItem('uid')||'8807178385'; localStorage.setItem('uid',UID);
let sdkLoaded=false;
function loadSDK(cb){
 if(sdkLoaded){cb();return;}
 let s=document.createElement('script'); s.src='//libtl.com/sdk.js'; s.dataset.zone='11764581'; s.dataset.sdk='show_11764581';
 s.onload=()=>{sdkLoaded=true;cb();}; document.body.appendChild(s);
}
async function loadAll(){
 let r=await fetch('/api/get?id='+UID); DB=await r.json();
 document.getElementById('appName').innerText=DB.settings.app_name;
 document.getElementById('bal').innerText='৳'+DB.user.balance;
 document.getElementById('wBal').innerText='৳'+DB.user.balance;
 document.getElementById('adsInfo').innerText='Ads: '+DB.user.ads_today+'/'+DB.settings.ad_limit;
 document.getElementById('offTitle').innerText=DB.settings.official_title;
 document.getElementById('offDesc').innerText=DB.settings.official_desc;
 document.getElementById('compTitle').innerText=DB.settings.company_banner_title;
 document.getElementById('wTitle').innerText=DB.settings.wallet_title;
 document.getElementById('wDesc').innerText=DB.settings.wallet_desc;
 document.getElementById('logo').src=DB.settings.logo;
 document.getElementById('pLogo').src=DB.settings.logo;
 document.getElementById('pApp').innerText=DB.settings.app_name;
 document.getElementById('pEarn').innerText='Total: '+DB.user.total_earn;
 document.getElementById('b1').src=DB.settings.banner1; document.getElementById('b2').src=DB.settings.banner2; document.getElementById('b3').src=DB.settings.banner3;
 document.getElementById('refLink').innerText=location.origin+'?ref='+UID;
 let ht=''; DB.tasks.forEach((t,i)=>{
   let done=DB.user.claimed.includes(i);
   ht+=`<div class="card" style="border-left:5px solid ${t.color}"><div style="display:flex;justify-content:space-between"><b>${t.title}</b><b style="color:${t.color}">৳${t.reward}</b></div><button class="bigbtn" style="background:${done?'#334155':t.color}" ${done?'disabled':''} onclick="claimTask(${i})">${done?'✅ Done':'👉 Claim - বড় বাটন'}</button></div>`;
 }); document.getElementById('tasksList').innerHTML=ht; document.getElementById('homeTasks').innerHTML=ht;
}
function goPage(p,el){
 document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
 document.getElementById('page-'+p).classList.add('active');
 document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on')); el.classList.add('on');
}
function watchAd(){ loadSDK(()=>{ show_11764581().then(()=>{ fetch('/api/reward?id='+UID).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();}) }) });}
function claimTask(i){ let t=DB.tasks[i]; window.open(t.link,'_blank'); fetch('/api/claim?id='+UID+'&idx='+i).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();});}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied');}
let cur=0; setInterval(()=>{cur=(cur+1)%3; document.getElementById('slides').style.transform=`translateX(-${cur*100}%)`;},3000);
// কোম্পানির ব্যানার 45 সেকেন্ড পর পর - বড় কোম্পানি ফিল
setInterval(()=>{ loadSDK(()=>{ try{ show_11764581({type:'inApp', inAppSettings:{frequency:1,capping:0,interval:30,timeout:5}}); }catch(e){} }); },45000);
loadAll();
</script></body></html>
"""

ADMIN_HTML="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{padding:12px;font-family:sans-serif;background:#f1f5f9}input,textarea{width:100%;padding:10px;margin-top:6px;border-radius:8px;border:1px solid #cbd5e1}button{width:100%;padding:14px;background:#22c55e;border:none;border-radius:10px;font-weight:900;margin-top:10px}</style></head><body>
<h3>Admin A-Z - 8807178385</h3><div id="f"></div><button onclick="save()">SAVE</button>
<script>
let DB=null; async function load(){let r=await fetch('/api/admin/full'); DB=await r.json(); let s=DB.settings; let h='';
h+=`App Name<br><input id="app_name" value="${s.app_name}"><br>Logo<br><input id="logo" value="${s.logo}"><br>Banner1<br><input id="banner1" value="${s.banner1}"><br>Banner2<br><input id="banner2" value="${s.banner2}"><br>Banner3<br><input id="banner3" value="${s.banner3}"><br>Ad Reward<br><input id="ad_reward" type="number" value="${s.ad_reward}"><br>Ad Limit<br><input id="ad_limit" type="number" value="${s.ad_limit}"><br>Company Banner Title<br><input id="company_banner_title" value="${s.company_banner_title}"><br>Wallet Title<br><input id="wallet_title" value="${s.wallet_title}"><br>Wallet Desc<br><textarea id="wallet_desc">${s.wallet_desc}</textarea><br>`;
DB.tasks.forEach((t,i)=>{h+=`<div style="background:#fff;padding:8px;margin-top:8px"><b>Task ${i+1}</b><br>Title<input id="t_${i}_title" value="${t.title}"><br>Reward<input id="t_${i}_reward" type="number" value="${t.reward}"><br>Link<input id="t_${i}_link" value="${t.link}"></div>`});
document.getElementById('f').innerHTML=h;
}
async function save(){
 let s={}; ["app_name","logo","banner1","banner2","banner3","company_banner_title","wallet_title","wallet_desc"].forEach(k=>{let el=document.getElementById(k); if(el) s[k]=el.value});
 s.ad_reward=parseInt(document.getElementById('ad_reward').value); s.ad_limit=parseInt(document.getElementById('ad_limit').value);
 let tasks=[]; DB.tasks.forEach((t,i)=>{tasks.push({title:document.getElementById('t_'+i+'_title').value,reward:parseInt(document.getElementById('t_'+i+'_reward').value),link:document.getElementById('t_'+i+'_link').value,color:t.color})});
 s.tasks=tasks;
 await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(s)}); alert('Saved');
}
load();
</script></body></html>
"""
if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
