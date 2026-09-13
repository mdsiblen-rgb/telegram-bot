# -*- coding: utf-8 -*-
# FINAL VERSION - Clean Header + Clear Balance Color Fill + All Admin Control
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def default():
    return {
        "users":{},
        "settings":{
            "app_name":"Protidiner Kaj BD",
            "admin_name":"MD Emon - Owner",
            "app_logo":"👑",
            "admin_profile":"👤",
            "zone":"11764581",
            "bonus":1120,
            "ad_reward":2,
            "popup_reward":3,
            "company_limit":30,
            "popup_limit":20,
            "task_limit":5,
            "min_with":500,
            "google_ads":[
                "⭐ Official Ad • bKash • Nagad • Daraz • Trusted",
                "📢 Company Sponsored • 100% Safe",
                "🎉 Daily Bonus Available Today"
            ],
            "offer_title":"🎉 আজকের স্পেশাল অফার",
            "offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস! দ্রুত কাজ করুন",
            "balance_title":"আপনার বর্তমান ব্যালেন্স"
        },
        "tasks":[
            {"title":"Telegram Channel","reward":25,"icon":"✈️"},
            {"title":"Telegram Group","reward":20,"icon":"👥"},
            {"title":"Telegram Bot","reward":20,"icon":"🤖"},
            {"title":"Kurigram Channel","reward":25,"icon":"📢"},
            {"title":"Refer Friend","reward":50,"icon":"👨‍👩‍👧‍👦"}
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
        db["users"][uid]={"id":uid,"balance":default()["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"last":today}
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
        if u["ads_today"]>=s["company_limit"]: return jsonify({"ok":False,"msg":f"Company Limit {s['company_limit']} শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"ok":False,"msg":f"Popup Limit {s['popup_limit']} শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save(db)
    return jsonify({"ok":True,"msg":f"৳{s['ad_reward' if typ=='company' else 'popup_reward']} যোগ হয়েছে ✅"})

@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load(); j=request.json
    for k in j:
        if k.startswith("google_ad"):
            try:
                idx=int(k[-1])-1
                if 0<=idx<3: db["settings"]["google_ads"][idx]=j[k]
            except: pass
        else:
            db["settings"][k]=j[k]
    save(db); return jsonify({"msg":"✅ Saved - সাথে সাথে অ্যাপে আপডেট"})

USER="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:125px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;border-bottom:1px solid rgba(255,255,255,0.08);position:sticky;top:0;z-index:99}
.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,#17172a,#0e0e20);border:1px solid #222}
.btn{width:100%;padding:18px;border:none;border-radius:16px;font-weight:900;font-size:15px;color:#fff;margin-top:12px;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:12px 0 16px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:12px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:24px;display:block;margin-bottom:2px}
.page{display:none}.page.active{display:block}
</style></head><body>

<div class="top">
<div style="display:flex;align-items:center;gap:10px">
<div style="font-size:28px" id="appLogo">👑</div>
<div>
<div style="font-weight:900;font-size:17px;display:flex;align-items:center;gap:6px"><span id="appName">Protidiner Kaj BD</span><span style="background:#22c55e;color:#fff;font-size:11px;padding:2px 6px;border-radius:6px">✓</span></div>
<div style="font-size:11px;opacity:0.6" id="adminName">Admin: MD Emon</div>
</div>
</div>
<div style="width:38px;height:38px;border-radius:50%;background:#1f1f3a;display:flex;align-items:center;justify-content:center" id="adminProfile">👤</div>
</div>

<div id="p-home" class="page active">
<div style="margin:12px;border-radius:14px;padding:14px;text-align:center;font-weight:800;background:linear-gradient(90deg,#f59e0b,#ef4444);color:#fff;font-size:14px" id="gAd">Loading...</div>

<!-- ক্লিয়ার ব্যালেন্স - ভরাট কালার -->
<div class="card" style="text-align:center;background:linear-gradient(135deg,#1e3a8a,#3b82f6,#06b6d4,#10b981,#f59e0b);padding:30px 18px;border:2px solid rgba(255,255,255,0.25);box-shadow:0 10px 40px rgba(59,130,246,0.4)">
<div style="font-size:11px;letter-spacing:2px;color:#e0f2fe;font-weight:700" id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div>
<div style="font-size:60px;font-weight:900;margin:10px 0;color:#fff;text-shadow:0 2px 20px rgba(0,0,0,0.6)">৳<span id="bal">0</span></div>
<div style="display:flex;justify-content:center;gap:6px;flex-wrap:wrap">
<span style="background:rgba(0,0,0,0.35);padding:6px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,0.2)">Company <b id="ads" style="color:#fde047">0</b>/<span id="adsLim">30</span></span>
<span style="background:rgba(0,0,0,0.35);padding:6px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,0.2)">Popup <b id="pop" style="color:#86efac">0</b>/<span id="popLim">20</span></span>
<span style="background:rgba(0,0,0,0.35);padding:6px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,0.2)">Total <b id="total">0</b></span>
</div>
<div style="background:rgba(0,0,0,0.4);height:10px;border-radius:20px;margin-top:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.2)"><div id="prog" style="height:100%;background:linear-gradient(90deg,#fde047,#fbbf24);width:0%;border-radius:20px;transition:width 1s ease"></div></div>
</div>

<div class="card">
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS দেখুন (৳<span id="r1">2</span>) - <span id="ads2">0</span>/<span id="adsLim2">30</span></button>
<button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS (৳<span id="r2">3</span>) - <span id="pop2">0</span>/<span id="popLim2">20</span></button>
<button class="btn" style="background:#1e293b" onclick="nav('task')">📋 TASK BONUS - 5 টা/দিন</button>
</div>

<div class="card" style="border:2px solid #fbbf24;background:linear-gradient(135deg,rgba(251,191,36,0.15),#0e0e20)"><div style="font-weight:900" id="offerTitle"></div><div style="font-size:13px;margin-top:6px;opacity:0.9" id="offerDesc"></div></div>
</div>

<div id="p-task" class="page"><div class="card"><h3>📋 Task Bonus</h3><div id="taskList"></div></div></div>
<div id="p-wallet" class="page"><div class="card"><h3>💰 Wallet - ৳<span id="bal2">0</span></h3></div></div>
<div id="p-support" class="page"><div class="card"><h3>💬 Support</h3><p>Telegram: @Emon</p></div></div>
<div id="p-profile" class="page"><div class="card"><h3>👤 Profile</h3><p>ID: <span id="uid"></span></p></div></div>

<div class="btm">
<div class="on" onclick="nav('home')" id="b-home"><span>🏠</span>Home</div>
<div onclick="nav('task')" id="b-task"><span>📋</span>Task</div>
<div onclick="nav('wallet')" id="b-wallet"><span>💰</span>Wallet</div>
<div onclick="nav('support')" id="b-support"><span>💬</span>Support</div>
<div onclick="nav('profile')" id="b-profile"><span>👤</span>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let gAds=[],gIdx=0;
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());let s=r.settings;let u=r.user;
 document.getElementById('bal').innerText=u.balance;document.getElementById('bal2').innerText=u.balance;
 document.getElementById('ads').innerText=u.ads_today;document.getElementById('pop').innerText=u.total-u.ads_today;document.getElementById('pop').innerText=u.popup_today;document.getElementById('ads2').innerText=u.ads_today;document.getElementById('pop2').innerText=u.popup_today;
 document.getElementById('adsLim').innerText=s.company_limit;document.getElementById('adsLim2').innerText=s.company_limit;document.getElementById('popLim').innerText=s.popup_limit;document.getElementById('popLim2').innerText=s.popup_limit;
 document.getElementById('r1').innerText=s.ad_reward;document.getElementById('r2').innerText=s.popup_reward;
 document.getElementById('appName').innerText=s.app_name;document.getElementById('adminName').innerText='Admin: '+s.admin_name;
 document.getElementById('appLogo').innerText=s.app_logo;document.getElementById('adminProfile').innerText=s.admin_profile;
 document.getElementById('balTitle').innerText='💰 '+s.balance_title;document.getElementById('offerTitle').innerText=s.offer_title;document.getElementById('offerDesc').innerText=s.offer_desc;
 document.getElementById('uid').innerText=uid;document.getElementById('total').innerText=u.total;
 gAds=s.google_ads;let prog=((u.ads_today+u.popup_today)/(s.company_limit+s.popup_limit)*100);document.getElementById('prog').style.width=prog+'%';
 let tl=document.getElementById('taskList');tl.innerHTML='';r.tasks.forEach(t=>{tl.innerHTML+=`<div class="card" style="margin:8px 0;display:flex;justify-content:space-between"><span>${t.icon} ${t.title}</span><b>৳${t.reward}</b></div>`});
}
function nav(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে, 2 সেকেন্ড পর আবার চাপো');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(x=>x.json()).then(d=>{alert(d.msg);load();});}).catch(()=>{});}
setInterval(()=>{if(gAds.length>0){document.getElementById('gAd').innerText=gAds[gIdx];gIdx=(gIdx+1)%gAds.length;}},3000);
load();
</script></body></html>
"""

ADMIN="""
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#0f0f0f;color:#fff;font-family:sans-serif;padding:16px}input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}.card{background:#1e1e1e;padding:16px;border-radius:12px;margin:12px 0}.btn{padding:16px;width:100%;border:none;border-radius:10px;background:#6d4cff;color:#fff;font-weight:900;font-size:16px}</style>
</head><body>
<h2>👑 Admin - সব কিছু চেঞ্জ</h2>
<div class="card">App Name:<input id="app_name">Admin Name:<input id="admin_name">Logo:<input id="app_logo">Profile:<input id="admin_profile">Balance Title:<input id="balance_title"></div>
<div class="card">Google Ad 1:<input id="g1">Ad 2:<input id="g2">Ad 3:<input id="g3"></div>
<div class="card">Offer Title:<input id="offer_title">Offer Desc:<textarea id="offer_desc"></textarea></div>
<div class="card">Company Limit:<input id="company_limit" type="number">Company Reward:<input id="ad_reward" type="number">Popup Limit:<input id="popup_limit" type="number">Popup Reward:<input id="popup_reward" type="number"></div>
<button class="btn" onclick="save()">💾 Save All</button><div id="msg" style="text-align:center;margin-top:10px"></div>
<script>
async function load(){let r=await fetch('/api/get?id=8807178385').then(x=>x.json());let s=r.settings;app_name.value=s.app_name;admin_name.value=s.admin_name;app_logo.value=s.app_logo;admin_profile.value=s.admin_profile;balance_title.value=s.balance_title;g1.value=s.google_ads[0];g2.value=s.google_ads[1];g3.value=s.google_ads[2];offer_title.value=s.offer_title;offer_desc.value=s.offer_desc;company_limit.value=s.company_limit;ad_reward.value=s.ad_reward;popup_limit.value=s.popup_limit;popup_reward.value=s.popup_reward;}
async function save(){let d={app_name:app_name.value,admin_name:admin_name.value,app_logo:app_logo.value,admin_profile:admin_profile.value,balance_title:balance_title.value,google_ad1:g1.value,google_ad2:g2.value,google_ad3:g3.value,offer_title:offer_title.value,offer_desc:offer_desc.value,company_limit:parseInt(company_limit.value),ad_reward:parseInt(ad_reward.value),popup_limit:parseInt(popup_limit.value),popup_reward:parseInt(popup_reward.value)};let res=await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(x=>x.json());msg.innerText=res.msg;}
load();
</script></body></html>
"""
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
