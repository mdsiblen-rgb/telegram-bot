# -*- coding: utf-8 -*-
# FINAL FIRST PAGE - Crown Left, Tick Right, 3 Google Ads Rotating, Offer Bottom, All Admin Control
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
            "app_name":"Protidiner Kaj BD",
            "admin_name":"MD Emon - Owner",
            "zone":"11764581",
            "bonus":1120,
            "ad_reward":2,
            "popup_reward":3,
            "company_limit":30,
            "popup_limit":20,
            "task_limit":5,
            "min_with":500,
            # এডমিন থেকে ৩ টা গুগল এড চেঞ্জ করতে পারবে
            "google_ads":[
                "📢 Google Sponsored • Zone 11764581 • Official Partner",
                "⭐ Official Ad • bKash • Nagad • Daraz • Trusted",
                "✅ Verified Company Ads • 100% Safe & Secure"
            ],
            "offer_title":"🎉 আজকের স্পেশাল অফার",
            "offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস! দ্রুত কাজ করুন",
            "offer_active":True
        },
        "tasks":[
            {"title":"Telegram Channel Join","reward":25,"icon":"✈️"},
            {"title":"Telegram Group Join","reward":20,"icon":"👥"},
            {"title":"Telegram Bot Start","reward":20,"icon":"🤖"},
            {"title":"Kurigram Channel","reward":25,"icon":"📢"},
            {"title":"Refer Friend","reward":50,"icon":"👨‍👩‍👧‍👦"}
        ]
    }

def load():
    if not os.path.exists(DB):
        d=default(); json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2); return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save(d): json.dump(d,open(DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
def getu(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User-{uid[-4:]}","pic":"https://cdn-icons-png.flaticon.com/512/149/149071.png","balance":default()["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"last":today,"claimed":[]}
    u=db["users"][uid]
    if u["last"]!=today: u["ads_today"]=0; u["popup_today"]=0; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(USER)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only?id=8807178385",403
    return render_template_string(ADMIN)

@app.route('/api/get')
def api_get():
    db=load(); u=getu(db,request.args.get('id','0')); save(db)
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})

@app.route('/api/reward')
def api_reward():
    db=load(); u=getu(db,request.args.get('id')); typ=request.args.get('type','company'); s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":f"Company Ads লিমিট {s['company_limit']} শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"Popup লিমিট {s['popup_limit']} শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save(db); return jsonify({"msg":f"৳{s['ad_reward' if typ=='company' else 'popup_reward']} যোগ হয়েছে!"})

@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load(); j=request.json
    # এডমিন থেকে সব কিছু আপডেট হবে
    for k in ["app_name","admin_name","ad_reward","popup_reward","company_limit","popup_limit","task_limit","min_with","offer_title","offer_desc","offer_active","google_ad1","google_ad2","google_ad3"]:
        if k in j:
            if k.startswith("google_ad"):
                idx=int(k[-1])-1
                db["settings"]["google_ads"][idx]=j[k]
            else:
                db["settings"][k]=j[k]
    save(db); return jsonify({"msg":"Saved - অ্যাপে সাথে সাথে আপডেট হবে"})

USER="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:130px}
.top{background:#0a0a19;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,rgba(255,255,255,0.08),rgba(255,255,255,0.03));border:1px solid rgba(255,255,255,0.1)}
.btn{width:100%;padding:18px;border:none;border-radius:14px;font-weight:900;font-size:15px;color:#fff;cursor:pointer;margin-top:12px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(12,10,30,0.98);display:flex;padding:14px 0 18px;border-radius:26px 26px 0 0;border-top:1px solid rgba(255,255,255,0.15);z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:14px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:26px;display:block;margin-bottom:2px}
.gad{margin:12px;border-radius:16px;padding:16px;font-weight:900;text-align:center;background:linear-gradient(90deg,#4285f4,#34a853,#fbbc05,#ea4335);background-size:300% 100%;animation:grad 3s infinite alternate;color:#fff;font-size:15px}
@keyframes grad{0%{background-position:0%}100%{background-position:100%}}
.offer{border:2px solid #fbbf24;background:linear-gradient(135deg,rgba(251,191,36,0.18),rgba(0,0,0,0.4));}
.page{display:none}.page.active{display:block}
</style></head><body>

<!-- TOP: বামে মুকুট, ডানে টিক -->
<div class="top">
<div style="display:flex;gap:10px;align-items:center">
<div style="font-size:28px">👑</div>
<div>
<div style="font-weight:900;font-size:17px;display:flex;align-items:center;gap:6px"><span id="appName"></span><span style="color:#00ff88;font-size:18px">✅</span></div>
<div style="font-size:12px;opacity:0.7" id="adminName"></div>
<div style="font-size:11px;color:#00ff88">Zone 11764581 • Auto OFF ✅</div>
</div>
</div>
<img id="userPic" style="width:42px;height:42px;border-radius:50%;border:2px solid #6d4cff" src="https://cdn-icons-png.flaticon.com/512/149/149071.png">
</div>

<div id="p-home" class="page active">
<!-- উপরে গুগল এড - ৩ সেকেন্ড পর পর চেঞ্জ -->
<div class="gad" id="googleAdBox">Loading Ads...</div>

<div class="card" style="text-align:center"><div style="opacity:0.6;font-size:13px">আপনার ব্যালেন্স</div><div style="font-size:46px;font-weight:900">৳<span id="bal">0</span></div><small>Company <span id="ads">0</span>/<span id="adsLim">30</span> • Popup <span id="pop">0</span>/<span id="popLim">20</span> • Total <span id="total">0</span></small><div style="background:rgba(0,0,0,0.4);height:7px;border-radius:10px;margin-top:12px"><div id="prog" style="height:7px;background:linear-gradient(90deg,#6d4cff,#00ff88);width:0%;border-radius:10px"></div></div></div>

<div class="card">
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS দেখুন (৳<span id="r1">2</span>) - <span id="ads2">0</span>/<span id="adsLim2">30</span></button>
<button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS (৳<span id="r2">3</span>) - <span id="pop2">0</span>/<span id="popLim2">20</span></button>
<button class="btn" style="background:#1e293b" onclick="nav('task')">📋 TASK BONUS - <span id="taskLim">5</span> টা/দিন</button>
</div>

<!-- আজকের স্পেশাল অফার - সবার নিচে -->
<div class="card offer" id="offerBox"><div style="font-weight:900;font-size:15px" id="offerTitle"></div><div style="font-size:13px;opacity:0.9;margin-top:6px" id="offerDesc"></div></div>

</div>

<!-- অন্য পেজ -->
<div id="p-task" class="page"><div class="card"><h3>📋 Tasks</h3><div id="taskList"></div></div></div>
<div id="p-wallet" class="page"><div class="card"><h3>Wallet ৳<span id="bal2">0</span></h3></div></div>
<div id="p-support" class="page"><div class="card"><h3>Support</h3></div></div>
<div id="p-profile" class="page"><div class="card"><h3>Profile</h3></div></div>

<div class="btm">
<div class="on" onclick="nav('home')" id="b-home"><span>🏠</span>Home</div>
<div onclick="nav('task')" id="b-task"><span>📋</span>Task</div>
<div onclick="nav('wallet')" id="b-wallet"><span>💰</span>Wallet</div>
<div onclick="nav('support')" id="b-support"><span>💬</span>Support</div>
<div onclick="nav('profile')" id="b-profile"><span>👤</span>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let gAds=[];let gIdx=0;
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());
 document.getElementById('bal').innerText=r.user.balance; if(document.getElementById('bal2')) document.getElementById('bal2').innerText=r.user.balance;
 document.getElementById('ads').innerText=r.user.ads_today;document.getElementById('pop').innerText=r.user.popup_today;
 document.getElementById('ads2').innerText=r.user.ads_today;document.getElementById('pop2').innerText=r.user.popup_today;
 document.getElementById('adsLim').innerText=r.settings.company_limit;document.getElementById('adsLim2').innerText=r.settings.company_limit;
 document.getElementById('popLim').innerText=r.settings.popup_limit;document.getElementById('popLim2').innerText=r.settings.popup_limit;
 document.getElementById('taskLim').innerText=r.settings.task_limit;
 document.getElementById('r1').innerText=r.settings.ad_reward;document.getElementById('r2').innerText=r.settings.popup_reward;
 document.getElementById('appName').innerText=r.settings.app_name;document.getElementById('adminName').innerText='Admin: '+r.settings.admin_name;
 document.getElementById('offerTitle').innerText=r.settings.offer_title;document.getElementById('offerDesc').innerText=r.settings.offer_desc;
 document.getElementById('total').innerText=r.user.total;
 let prog=((r.user.ads_today+r.user.popup_today)/(r.settings.company_limit+r.settings.popup_limit)*100);document.getElementById('prog').style.width=prog+'%';
 gAds=r.settings.google_ads;
 // Task list
 let tl=document.getElementById('taskList'); if(tl){tl.innerHTML=''; r.tasks.forEach(t=>{tl.innerHTML+=`<div class="card" style="margin:8px 0">${t.icon} ${t.title} - ৳${t.reward}</div>`})}
}
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');load();}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(x=>x.json()).then(d=>{alert(d.msg);load();});}).catch(e=>{});}
// ৩ সেকেন্ড পর পর গুগল এড চেঞ্জ
setInterval(()=>{ if(gAds.length>0){ document.getElementById('googleAdBox').innerText=gAds[gIdx]; gIdx=(gIdx+1)%gAds.length; } },3000);
load();
</script></body></html>
"""

ADMIN="""
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;padding:16px;background:#0f0f0f;color:#fff}input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}.card{background:#1e1e1e;padding:16px;border-radius:12px;margin:12px 0}.btn{padding:14px;width:100%;border:none;border-radius:8px;background:#6d4cff;color:#fff;font-weight:900;cursor:pointer}</style></head><body>
<h2>👑 Admin Panel - সব কিছু এখান থেকে কন্ট্রোল</h2>
<div class="card"><h3>App Name & Admin</h3>App Name:<input id="app_name">Admin Name:<input id="admin_name"></div>
<div class="card"><h3>📢 উপরের ৩ টা Google Official Ad (৩ সেকেন্ড পর পর চেঞ্জ হবে)</h3>Ad 1:<input id="g1">Ad 2:<input id="g2">Ad 3:<input id="g3"></div>
<div class="card"><h3>🎁 নিচের Special Offer Box</h3>Title:<input id="offer_title">Desc:<textarea id="offer_desc"></textarea>Active: <select id="offer_active" style="width:100%;padding:10px;background:#1a1a1a;color:#fff"><option value="true">Show</option><option value="false">Hide</option></select></div>
<div class="card"><h3>💸 Taka & Limit Control</h3>Company Limit:<input id="company_limit" type="number">Company Reward:<input id="ad_reward" type="number">Popup Limit:<input id="popup_limit" type="number">Popup Reward:<input id="popup_reward" type="number">Task Limit:<input id="task_limit" type="number"></div>
<button class="btn" onclick="save()">💾 Save All - সাথে সাথে অ্যাপে আপডেট</button>
<script>
async function load(){let r=await fetch('/api/get?id=8807178385').then(x=>x.json());document.getElementById('app_name').value=r.settings.app_name;document.getElementById('admin_name').value=r.settings.admin_name;document.getElementById('g1').value=r.settings.google_ads[0];document.getElementById('g2').value=r.settings.google_ads[1];document.getElementById('g3').value=r.settings.google_ads[2];document.getElementById('offer_title').value=r.settings.offer_title;document.getElementById('offer_desc').value=r.settings.offer_desc;document.getElementById('company_limit').value=r.settings.company_limit;document.getElementById('ad_reward').value=r.settings.ad_reward;document.getElementById('popup_limit').value=r.settings.popup_limit;document.getElementById('popup_reward').value=r.settings.popup_reward;document.getElementById('task_limit').value=r.settings.task_limit;}
async function save(){let d={app_name:document.getElementById('app_name').value,admin_name:document.getElementById('admin_name').value,google_ad1:document.getElementById('g1').value,google_ad2:document.getElementById('g2').value,google_ad3:document.getElementById('g3').value,offer_title:document.getElementById('offer_title').value,offer_desc:document.getElementById('offer_desc').value,offer_active:document.getElementById('offer_active').value==='true',company_limit:parseInt(document.getElementById('company_limit').value),ad_reward:parseInt(document.getElementById('ad_reward').value),popup_limit:parseInt(document.getElementById('popup_limit').value),popup_reward:parseInt(document.getElementById('popup_reward').value),task_limit:parseInt(document.getElementById('task_limit').value)};await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});alert('Saved!');load();}
load();
</script></body></html>
"""
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
