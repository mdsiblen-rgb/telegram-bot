# -*- coding: utf-8 -*-
# FINAL 600+ LINES - MINI BOY - 11764581 - 8807178385
# Banner 3 Pic Slider + Wallet Bottom Admin Editable + No Auto Ad
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'

def default_db():
    return {
        "users": {}, "withdraws": [],
        "settings": {
            "app_name": "প্রতিদিনের কাজ BD - 11764581",
            "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "bkash_logo": "https://download.logo.wine/logo/BKash/bKash-Logo.wine.png",
            "nagad_logo": "https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png",
            "welcome_bonus": 60, "ad_reward": 2, "ad_limit": 30, "min_withdraw": 1000, "ref_bonus": 20,
            "official_title": "আফিশিয়াল নোটিস - 11764581",
            "official_desc": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন - Token 11764581",
            "official_live": "LIVE",
            "home_ad_top_title": "🎬 স্পেশাল অফার - Mini Boy Ads",
            "home_ad_btn": "▶️ ADS দেখুন - Token 11764581",
            "home_ad_zone": "11764581",
            "tasks_header": "📋 আজকের ৯ টি টাস্ক - 11764581",
            "support_title": "💬 সাপোর্ট সেন্টার - 8807178385",
            "support_desc": "Telegram: @ProtidinerKajBD - Admin 8807178385",
            "support_tg": "https://t.me/ProtidinerKajBD",
            "banner1": "https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2": "https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3": "https://img.freepik.com/free-vector/earning-money-online-concept-landing-page_52683-25203.jpg",
            "wallet_bottom_title": "💳 Withdraw নিয়ম - Admin থেকে Change",
            "wallet_bottom_desc": "১. Minimum ৳1000 হলে Withdraw\n২. bKash/Nagad সঠিক দিন\n৩. ২৪ ঘণ্টায় পেমেন্ট\n৪. ভুল Number দিলে দায় আপনার\n৫. একাধিক Account Ban",
        },
        "tasks": [
            {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "👉 Claim - 25"},
            {"title": "Telegram Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "👉 Claim - 10"},
            {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "👉 Claim - 15"},
            {"title": "Website Visit", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "👉 Claim - 20"},
            {"title": "Group Join", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "👉 Claim - 20"},
            {"title": "Post Like", "reward": 20, "link": "https://t.me", "color": "#be123c", "btn": "👉 Claim - 20"},
            {"title": "Post Share", "reward": 20, "link": "https://t.me", "color": "#065f46", "btn": "👉 Claim - 20"},
            {"title": "Comment", "reward": 20, "link": "https://t.me", "color": "#2563eb", "btn": "👉 Claim - 20"},
            {"title": "Refer 3 Friend", "reward": 20, "link": "https://t.me", "color": "#d97706", "btn": "👉 Claim - 20"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d=default_db(); save_db(d); return d
    with open(DB_FILE,'r',encoding='utf-8') as f: d=json.load(f)
    dd=default_db()
    for k,v in dd["settings"].items():
        if k not in d["settings"]: d["settings"][k]=v
    return d

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False)

def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"balance":db["settings"]["welcome_bonus"],"ads_watched":0,"ads_today":0,"last_date":today,"claimed":[],"ref_count":0,"total_earn":db["settings"]["welcome_bonus"]}
    u=db["users"][uid]
    if u.get("last_date")!=today: u["ads_today"]=0; u["last_date"]=today
    return u

@app.route('/health')
def health(): return "OK - 11764581",200

@app.route('/')
def index(): return render_template_string(USER_HTML)

@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "Need?id=8807178385",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385')
    db=load_db(); u=get_user(db,uid); save_db(db)
    top=sorted(db["users"].values(),key=lambda x:x.get('ref_count',0),reverse=True)[:5]
    recent=db["withdraws"][-20:][::-1]
    my=[w for w in db["withdraws"] if str(w["uid"])==str(uid)]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":my,"top_users":top,"recent_withdraws":recent})

@app.route('/api/reward')
def reward():
    db=load_db(); u=get_user(db,request.args.get('id'))
    if u["ads_today"]>=db["settings"]["ad_limit"]: return jsonify({"msg":"আজকের লিমিট শেষ!"})
    u["balance"]+=db["settings"]["ad_reward"]; u["total_earn"]+=db["settings"]["ad_reward"]; u["ads_watched"]+=1; u["ads_today"]+=1; save_db(db)
    return jsonify({"msg":f"৳{db['settings']['ad_reward']} পেয়েছেন!"})

@app.route('/api/claim_task')
def claim_task():
    db=load_db(); idx=int(request.args.get('idx')); uid=request.args.get('id'); u=get_user(db,uid)
    if idx in u["claimed"]: return jsonify({"msg":"Already Done"})
    u["claimed"].append(idx); u["balance"]+=db["tasks"][idx]["reward"]; u["total_earn"]+=db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg":"Task Complete!"})

@app.route('/api/withdraw')
def withdraw():
    db=load_db(); uid=request.args.get('id'); amt=int(request.args.get('amount',0)); num=request.args.get('number'); method=request.args.get('method','bKash')
    u=get_user(db,uid)
    if amt<db["settings"]["min_withdraw"]: return jsonify({"msg":f"Min {db['settings']['min_withdraw']}"})
    if u["balance"]<amt: return jsonify({"msg":"Balance কম"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"time":str(datetime.now())[:19],"status":"Pending"})
    save_db(db); return jsonify({"msg":"Withdraw Success!"})

@app.route('/api/admin/full')
def a_full(): return jsonify(load_db())

@app.route('/api/admin/save_settings', methods=['POST'])
def a_save():
    db=load_db(); j=request.json
    for k,v in j.items():
        if k in db["settings"]: db["settings"][k]=v
        if k=="tasks": db["tasks"]=v
    save_db(db); return jsonify({"msg":"Saved! 8807178385"})

USER_HTML = """
<!DOCTYPE html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}
body{background:#0a1222;color:#fff;max-width:430px;margin:0 auto;padding-bottom:140px}
.top{background:linear-gradient(135deg,#1e3a8a,#0f172a);padding:14px;border-radius:0 0 24px 24px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bal{color:#22c55e;font-size:42px;font-weight:900}
.card{background:#162032;margin:12px;border-radius:18px;padding:14px;border:1px solid #23344a}
.btn{width:100%;padding:13px;border:none;border-radius:12px;font-weight:700;cursor:pointer;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#121d32;display:flex;border-top:1px solid #23344a;padding:8px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#94a3b8;font-size:12px;cursor:pointer}.btm div.on{color:#38bdf8}
.inp{width:100%;padding:12px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}
.slider{position:relative;margin:12px;border-radius:18px;overflow:hidden;height:165px;border:1px solid #22314a;background:#000}
.slides{display:flex;transition:transform 0.6s ease;width:300%}.slide{min-width:100%;height:165px}.slide img{width:100%;height:165px;object-fit:cover}
.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px}.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.4)}.dot.on{background:#38bdf8;width:20px;border-radius:10px}
.live-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;animation:blink 1s infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0}100%{opacity:1}}
</style>
</head><body>
<div class="top">
<div><div id="appName" style="font-weight:900;font-size:18px"></div><div class="bal" id="bal">৳ 0</div><div id="adsInfo" style="font-size:12px;opacity:0.8"></div></div>
<div style="text-align:right"><div style="background:#22c55e;color:#000;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:900"><span class="live-dot"></span> <span id="liveTxt">LIVE</span></div><img id="logo" src="" style="width:40px;height:40px;border-radius:50%;margin-top:6px;border:2px solid #22c55e"></div>
</div>

<div class="card" style="display:flex;justify-content:space-between;align-items:center;border-color:#22c55e"><div><b id="offTitle"></b><br><small id="offDesc" style="opacity:0.7"></small></div><div style="background:#22c55e;color:#000;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:900">● LIVE</div></div>

<div class="slider" id="slider"><div class="slides" id="slides"><div class="slide"><img id="b1"></div><div class="slide"><img id="b2"></div><div class="slide"><img id="b3"></div></div><div class="dots"><div class="dot on" id="d0"></div><div class="dot" id="d1"></div><div class="dot" id="d2"></div></div></div>

<div class="card" style="border:2px dashed #38bdf8;text-align:center"><small style="color:#38bdf8">Company Ads - Token 11764581</small><div style="margin:8px 0;font-weight:700" id="adTopTitle"></div><button class="btn" style="background:#22c55e;color:#000" onclick="watchAd()">▶️ ADS দেখুন - ৳2 বোনাস</button><small id="zoneTxt" style="opacity:0.6;display:block;margin-top:6px"></small></div>

<div id="home_tasks"></div>

<div class="card"><b id="supTitle"></b><br><small id="supDesc"></small><br><button class="btn" style="background:#0ea5e9;margin-top:10px" onclick="openTG()">Telegram Support</button></div>

<div id="pages">
<div id="p_tasks" style="display:none"><div class="card"><b id="taskHeader"></b></div><div id="tasksList"></div></div>
<div id="p_refer" style="display:none"><div class="card"><h3>👥 Refer Box</h3><p id="refDesc"></p><div style="background:#0f172a;padding:12px;border-radius:10px;margin-top:8px;word-break:break-all" id="refLink"></div><button class="btn" style="background:#22c55e;color:#000;margin-top:10px" onclick="copyRef()">Copy</button></div></div>
<div id="p_wallet" style="display:none">
<div class="card"><h3>💰 Wallet</h3><div style="font-size:32px;color:#22c55e;font-weight:900" id="wBal">৳0</div><div id="myW"></div></div>
<div class="card"><h3>Withdraw</h3><select id="wMethod" class="inp"><option>bKash</option><option>Nagad</option></select><input id="wNum" class="inp" placeholder="Number"><input id="wAmt" class="inp" type="number" placeholder="Amount"><button class="btn" style="background:#22c55e;color:#000;margin-top:10px" onclick="doWithdraw()">Withdraw</button></div>
<div class="card" style="border-color:#f59e0b"><b id="wBotTitle"></b><br><small id="wBotDesc" style="white-space:pre-line"></small></div>
<div class="card"><b>Recent Withdraw</b><div id="recentW"></div></div>
</div>
<div id="p_profile" style="display:none"><div class="card" style="text-align:center"><img id="pLogo" src="" style="width:80px;height:80px;border-radius:50%;border:3px solid #22c55e"><h3 id="pApp"></h3><p>Total Earn: <span id="pEarn"></span></p></div></div>
</div>

<div class="btm"><div class="on" onclick="nav('home',this)">🏠<br>Home</div><div onclick="nav('tasks',this)">✅<br>Tasks</div><div onclick="nav('refer',this)">👥<br>Refer</div><div onclick="nav('wallet',this)">💰<br>Wallet</div><div onclick="nav('profile',this)">👤<br>Profile</div></div>

<script>
let DB=null, UID=localStorage.getItem('uid')||'8807178385_'+Math.floor(Math.random()*9999); localStorage.setItem('uid',UID);
let sdkLoaded=false;
function loadSDK(cb){
 if(sdkLoaded){cb();return;}
 let s=document.createElement('script'); s.src='//libtl.com/sdk.js'; s.dataset.zone='11764581'; s.dataset.sdk='show_11764581';
 s.onload=()=>{sdkLoaded=true;cb();}; document.body.appendChild(s);
}
async function loadAll(){
 let r=await fetch('/api/get_full?id='+UID); DB=await r.json();
 document.getElementById('appName').innerText=DB.settings.app_name;
 document.getElementById('bal').innerText='৳ '+DB.user.balance;
 document.getElementById('adsInfo').innerText='Ads: '+DB.user.ads_today+'/'+DB.settings.ad_limit;
 document.getElementById('wBal').innerText='৳ '+DB.user.balance;
 document.getElementById('offTitle').innerText=DB.settings.official_title;
 document.getElementById('offDesc').innerText=DB.settings.official_desc;
 document.getElementById('liveTxt').innerText=DB.settings.official_live;
 document.getElementById('adTopTitle').innerText=DB.settings.home_ad_top_title;
 document.getElementById('zoneTxt').innerText=DB.settings.home_ad_zone_text;
 document.getElementById('supTitle').innerText=DB.settings.support_title;
 document.getElementById('supDesc').innerText=DB.settings.support_desc;
 document.getElementById('taskHeader').innerText=DB.settings.tasks_header;
 document.getElementById('refDesc').innerText=DB.settings.ref_bottom_desc;
 document.getElementById('wBotTitle').innerText=DB.settings.wallet_bottom_title;
 document.getElementById('wBotDesc').innerText=DB.settings.wallet_bottom_desc;
 document.getElementById('logo').src=DB.settings.company_logo;
 document.getElementById('pLogo').src=DB.settings.company_logo;
 document.getElementById('pApp').innerText=DB.settings.app_name;
 document.getElementById('pEarn').innerText=DB.user.total_earn;
 document.getElementById('b1').src=DB.settings.banner1; document.getElementById('b2').src=DB.settings.banner2; document.getElementById('b3').src=DB.settings.banner3;
 document.getElementById('refLink').innerText=location.origin+'?ref='+UID;
 let ht=''; DB.tasks.forEach((t,i)=>{
   let done=DB.user.claimed.includes(i);
   ht+=`<div class="card" style="display:flex;justify-content:space-between;align-items:center;border-left:4px solid ${t.color}"><div><b>${t.title}</b><br><small style=color:${t.color}>৳${t.reward}</small></div><button class="btn" style="width:auto;background:${done?'#334155':t.color}" ${done?'disabled':''} onclick="claimTask(${i})">${done?'Done':t.btn}</button></div>`;
 }); document.getElementById('tasksList').innerHTML=ht; document.getElementById('home_tasks').innerHTML=ht;
 let mw=''; DB.withdraws.forEach(w=>{mw+=`<div style="background:#0f172a;padding:8px;border-radius:8px;margin-top:6px;font-size:12px">${w.method} - ৳${w.amount} - ${w.status}</div>`}); document.getElementById('myW').innerHTML=mw;
 let rw=''; DB.recent_withdraws.forEach(w=>{rw+=`<div style="font-size:12px;opacity:0.8;margin-top:4px">৳${w.amount} - ${w.method} - ${w.time}</div>`}); document.getElementById('recentW').innerHTML=rw;
}
function nav(p,el){
 document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on')); el.classList.add('on');
 document.getElementById('p_tasks').style.display=p=='tasks'?'block':'none';
 document.getElementById('p_refer').style.display=p=='refer'?'block':'none';
 document.getElementById('p_wallet').style.display=p=='wallet'?'block':'none';
 document.getElementById('p_profile').style.display=p=='profile'?'block':'none';
 if(p=='home') location.reload();
}
function watchAd(){
 loadSDK(()=>{ show_11764581().then(()=>{ fetch('/api/reward?id='+UID).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();}) }) });
}
function claimTask(i){
 let t=DB.tasks[i]; window.open(t.link,'_blank');
 fetch('/api/claim_task?id='+UID+'&idx='+i).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();});
}
function doWithdraw(){
 let amt=document.getElementById('wAmt').value, num=document.getElementById('wNum').value, method=document.getElementById('wMethod').value;
 fetch(`/api/withdraw?id=${UID}&amount=${amt}&number=${num}&method=${method}`).then(r=>r.json()).then(j=>{alert(j.msg); loadAll();});
}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied!');}
function openTG(){window.open(DB.settings.support_tg,'_blank');}
// slider auto
let cur=0; setInterval(()=>{cur=(cur+1)%3; document.getElementById('slides').style.transform=`translateX(-${cur*100}%)`; document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('on',i==cur));},3000);
loadAll();
</script>
</body></html>
"""

ADMIN_HTML="""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#f1f5f9;padding:12px;font-family:sans-serif}input,textarea{width:100%;padding:12px;margin-top:6px;border-radius:10px;border:1px solid #cbd5e1}button{width:100%;padding:14px;background:#22c55e;border:none;border-radius:12px;font-weight:900;margin-top:12px}</style>
</head><body>
<h2>Admin Panel - 8807178385 - 11764581</h2>
<div id="form"></div>
<button onclick="save()">💾 SAVE ALL</button>
<script>
let DB=null;
async function load(){let r=await fetch('/api/admin/full'); DB=await r.json(); let s=DB.settings; let h='';
h+=`App Name<br><input id="app_name" value="${s.app_name}"><br>`;
h+=`Company Logo<br><input id="company_logo" value="${s.company_logo}"><br>`;
h+=`Banner1<br><input id="banner1" value="${s.banner1}"><br>`;
h+=`Banner2<br><input id="banner2" value="${s.banner2}"><br>`;
h+=`Banner3<br><input id="banner3" value="${s.banner3}"><br>`;
h+=`Official Title<br><input id="official_title" value="${s.official_title}"><br>`;
h+=`Official Desc<br><textarea id="official_desc">${s.official_desc}</textarea><br>`;
h+=`Home Ad Top Title<br><input id="home_ad_top_title" value="${s.home_ad_top_title}"><br>`;
h+=`Ad Reward<br><input id="ad_reward" type="number" value="${s.ad_reward}"><br>`;
h+=`Ad Limit Daily (30)<br><input id="ad_limit" type="number" value="${s.ad_limit}"><br>`;
h+=`Min Withdraw<br><input id="min_withdraw" type="number" value="${s.min_withdraw}"><br>`;
h+=`Wallet Bottom Title (Admin Editable)<br><input id="wallet_bottom_title" value="${s.wallet_bottom_title}"><br>`;
h+=`Wallet Bottom Desc (Admin Editable - নিচের ফাঁকা জায়গা ঠিক হবে)<br><textarea id="wallet_bottom_desc" rows="6">${s.wallet_bottom_desc}</textarea><br>`;
h+=`Support TG<br><input id="support_tg" value="${s.support_tg}"><br>`;
DB.tasks.forEach((t,i)=>{h+=`<div style="background:#fff;padding:8px;margin-top:8px;border-radius:10px"><b>Task ${i+1}</b><br>Title<input id="t_title_${i}" value="${t.title}"><br>Reward<input id="t_reward_${i}" type="number" value="${t.reward}"><br>Link<input id="t_link_${i}" value="${t.link}"><br>Color<input id="t_color_${i}" value="${t.color}"></div>`});
document.getElementById('form').innerHTML=h;
}
async function save(){
 let s={};
 ["app_name","company_logo","banner1","banner2","banner3","official_title","official_desc","home_ad_top_title","ad_reward","ad_limit","min_withdraw","wallet_bottom_title","wallet_bottom_desc","support_tg"].forEach(k=>{let el=document.getElementById(k); if(el) s[k]=el.valueAsNumber!==undefined && el.type=='number'? parseInt(el.value) : el.value});
 let tasks=[]; DB.tasks.forEach((t,i)=>{tasks.push({title:document.getElementById('t_title_'+i).value, reward:parseInt(document.getElementById('t_reward_'+i).value), link:document.getElementById('t_link_'+i).value, color:document.getElementById('t_color_'+i).value, btn:`👉 Claim - ${document.getElementById('t_reward_'+i).value}`})});
 s.tasks=tasks;
 let r=await fetch('/api/admin/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(s)}); let j=await r.json(); alert(j.msg);
}
load();
</script>
</body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
