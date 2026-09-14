# -*- coding: utf-8 -*-
# PREMIUM PRO FINAL - New Design + Everything A to Z + 5 Button + Photo + Money + Admin Full
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def load_db():
    defaults={
        "app_name":"Premium Earning Pro","admin_name":"SHIBLI NOMAN","app_logo":"💎",
        "zone":"11764581","direct_link":"https://omg10.com/4/11760259",
        "bonus":100,"ad_reward":3,"popup_reward":5,"company_limit":50,"popup_limit":30,"min_with":300,"refer_reward":80,"refer_condition_ads":15,"daily_bonus":20,
        "bg_color":"#0f172a","card_color":"#1e293b","top_color":"#1e293b","btn_color":"#8b5cf6","btn2_color":"#f59e0b","text_color":"#f8fafc",
        "offer_title":"💎 Premium Special Offer","offer_desc":"আজ 50 টা Ads দেখলে ৳150 Bonus - Limited!","balance_title":"💰 Premium Balance",
        "tg_channel":"https://t.me/","support_link":"https://t.me/","whatsapp":"01XXXXXXXXX","notice":"💎 Premium App • Fast Payment • Trusted • Daily Bonus"
    }
    if not os.path.exists(DB):
        data={"users":{},"withdraws":[],"settings":defaults,"tasks":[{"id":1,"title":"💎 Join Premium Channel","reward":20,"link":"https://t.me/"},{"id":2,"title":"🔔 Subscribe & Like","reward":25,"link":"https://youtube.com/"},{"id":3,"title":"👍 Follow Facebook Page","reward":15,"link":"https://facebook.com/"},{"id":4,"title":"📸 Follow Instagram","reward":15,"link":"https://instagram.com/"}]}
        with open(DB,'w',encoding='utf-8') as f: json.dump(data,f,indent=2,ensure_ascii=False)
        return data
    with open(DB,'r',encoding='utf-8') as f:
        db=json.load(f)
        for k,v in defaults.items():
            if k not in db["settings"]: db["settings"][k]=v
        return db

def save_db(db):
    with open(DB,'w',encoding='utf-8') as f: json.dump(db,f,indent=2,ensure_ascii=False)

def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","profile_img":"","balance":db["settings"]["bonus"],"total_earn":db["settings"]["bonus"],"company_today":0,"popup_today":0,"tasks_done":[],"join_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"last_date":str(datetime.now().date()),"referred_by":ref,"refer_list":[],"refer_status":"pending","ads_watched":0,"level":"Bronze","daily_claimed":str(datetime.now().date())}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refer_list"].append({"id":uid,"name":db["users"][uid]["name"],"time":db["users"][uid]["join_time"]})
    return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def api_init():
    db=load_db(); j=request.json; uid=str(j.get('id')); ref=j.get('ref')
    if ref==uid: ref=None
    u=get_user(db,uid,ref); today=str(datetime.now().date())
    if u.get("last_date")!=today: u["company_today"]=0; u["popup_today"]=0; u["last_date"]=today
    # level system
    if u["total_earn"]>1000: u["level"]="Gold"
    elif u["total_earn"]>500: u["level"]="Silver"
    save_db(db); return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":[w for w in db["withdraws"] if w["uid"]==uid]})

@app.route('/api/ads/complete',methods=['POST'])
def ads_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); typ=j.get('type','company'); u=get_user(db,uid); s=db["settings"]
    if typ=='company':
        if u["company_today"]>=s["company_limit"]: return jsonify({"msg":f"আজকের লিমিট {s['company_limit']} শেষ"})
        u["company_today"]+=1; u["balance"]+=s["ad_reward"]; u["total_earn"]+=s["ad_reward"]; msg=f"✅ ৳{s['ad_reward']} যোগ হয়েছে"
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"লিমিট {s['popup_limit']} শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]; u["total_earn"]+=s["popup_reward"]; msg=f"✅ ৳{s['popup_reward']} যোগ"
    u["ads_watched"]+=1; ref=u.get("referred_by")
    if ref and ref in db["users"] and u["ads_watched"]>=s["refer_condition_ads"] and u["refer_status"]=="pending": db["users"][ref]["balance"]+=s["refer_reward"]; db["users"][ref]["total_earn"]+=s["refer_reward"]; u["refer_status"]="completed"
    save_db(db); return jsonify({"msg":msg})

@app.route('/api/daily',methods=['POST'])
def daily():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); today=str(datetime.now().date())
    if u.get("daily_claimed")==today: return jsonify({"msg":"আজ Bonus নিয়েছেন"})
    u["daily_claimed"]=today; u["balance"]+=db["settings"]["daily_bonus"]; u["total_earn"]+=db["settings"]["daily_bonus"]; save_db(db); return jsonify({"msg":f"✅ Daily ৳{db['settings']['daily_bonus']} Bonus!"})

@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid)
    if tid in u["tasks_done"]: return jsonify({"msg":"Already Done"})
    task=next((t for t in db["tasks"] if t["id"]==tid),None); u["tasks_done"].append(tid); u["balance"]+=task["reward"]; u["total_earn"]+=task["reward"]; save_db(db); return jsonify({"msg":f"✅ ৳{task['reward']} যোগ"})

@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt; db["withdraws"].append({"uid":uid,"name":u["name"],"amount":amt,"number":num,"method":method,"status":"Pending","time":datetime.now().strftime("%Y-%m-%d %H:%M")}); save_db(db); return jsonify({"msg":f"✅ ৳{amt} Withdraw Request সফল"})

@app.route('/api/user/update',methods=['POST'])
def user_update():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid)
    if 'name' in j: u["name"]=str(j['name'])[:25]
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save_db(db); return jsonify({"msg":"✅ Premium Profile Saved"})

@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db(); j=request.json
    for k in j: db["settings"][k]=j[k]
    save_db(db); return jsonify({"msg":"✅ Premium Saved"})

@app.route('/api/admin/users')
def admin_users(): return jsonify(load_db()["users"])
@app.route('/api/admin/withdraws')
def admin_withdraws(): return jsonify(load_db()["withdraws"])
@app.route('/api/admin/task/add',methods=['POST'])
def task_add():
    db=load_db(); j=request.json; nid=max([t["id"] for t in db["tasks"]]+[0])+1; db["tasks"].append({"id":nid,"title":j["title"],"reward":int(j["reward"]),"link":j["link"]}); save_db(db); return jsonify({"msg":"Task Added"})
@app.route('/api/admin/task/del',methods=['POST'])
def task_del():
    db=load_db(); j=request.json; db["tasks"]=[t for t in db["tasks"] if t["id"]!=int(j["id"])]; save_db(db); return jsonify({"msg":"Deleted"})

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>{{app_name}}</title>
<script src='//libtl.com/sdk.js' data-zone='{{zone}}' data-sdk='show_{{zone}}'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:Inter,system-ui}
body{background:radial-gradient(1200px 600px at 20% -10%, rgba(139,92,246,0.25), transparent), radial-gradient(1000px 500px at 80% 0%, rgba(245,158,11,0.18), transparent), {{bg_color}};color:{{text_color}};max-width:440px;margin:0 auto;padding-bottom:240px;min-height:100vh}
.top{padding:16px 18px;display:flex;justify-content:space-between;align-items:center;background:rgba(30,41,59,0.85);backdrop-filter:blur(16px);position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08);box-shadow:0 4px 20px rgba(0,0,0,0.3)}
.card{margin:14px;border-radius:24px;padding:20px;background:linear-gradient(180deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);box-shadow:0 10px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08);position:relative;overflow:hidden}
.card:before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(139,92,246,0.5),transparent)}
.btn{width:100%;padding:16px;border:none;border-radius:16px;font-weight:800;color:#fff;margin-top:10px;cursor:pointer;background:linear-gradient(135deg,{{btn_color}},#7c3aed);box-shadow:0 8px 25px rgba(139,92,246,0.4);transition:0.2s;font-size:14px}
.btn:active{transform:scale(0.97)}
.btn2{background:linear-gradient(135deg,{{btn2_color}},#f97316)!important;box-shadow:0 8px 25px rgba(245,158,11,0.4)!important}
.profile{width:56px;height:56px;border-radius:18px;background:linear-gradient(135deg,#334155,#1e293b);display:flex;align-items:center;justify-content:center;border:2px solid rgba(139,92,246,0.5);overflow:hidden;font-size:28px;box-shadow:0 0 30px rgba(139,92,246,0.4)}
.bannerBox{margin:14px;border-radius:26px;overflow:hidden;height:180px;background:linear-gradient(135deg,#8b5cf6 0%,#7c3aed 50%,#f59e0b 100%);position:relative;border:1px solid rgba(255,255,255,0.15);box-shadow:0 15px 40px rgba(139,92,246,0.35)}
.shine{position:absolute;top:0;left:-100%;width:70%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.45),transparent);transform:skewX(-20deg);animation:shineMove 3s infinite;z-index:2}
@keyframes shineMove{0%{left:-100%}100%{left:200%}}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:440px;background:rgba(15,23,42,0.92);backdrop-filter:blur(20px);display:flex;padding:12px 0 18px;border-radius:28px 28px 0 0;border-top:1px solid rgba(255,255,255,0.1);box-shadow:0 -8px 30px rgba(0,0,0,0.5);z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer;transition:0.3s}.btm div.on{color:#fff;transform:translateY(-3px)}.btm div.on span{filter:drop-shadow(0 0 8px rgba(139,92,246,0.8))}.btm div span{font-size:24px;display:block;margin-bottom:3px}
.page{display:none}.page.active{display:block}
.taskCard{display:flex;justify-content:space-between;align-items:center;padding:16px;border:1px solid rgba(255,255,255,0.07);border-radius:16px;margin-top:12px;background:rgba(15,23,42,0.6);transition:0.2s}
.taskCard:hover{border-color:rgba(139,92,246,0.3);transform:translateY(-1px)}
.premiumBadge{background:linear-gradient(135deg,#8b5cf6,#f59e0b);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:800;color:#fff;display:inline-block}
</style></head><body>
<div class="top"><div style="display:flex;gap:12px;align-items:center"><div class="profile" id="pImg">💎</div><div><b id="uName" style="font-size:15px">Loading...</b><br><small id="uId" style="opacity:.5;font-size:10px"></small><span class="premiumBadge" id="uLevel" style="margin-top:4px">Bronze</span></div></div><div style="text-align:right"><div id="bal" style="font-weight:900;color:#22c55e;font-size:18px">৳0</div><small style="opacity:.6;font-size:10px">Total: <span id="totalEarn">0</span></small></div></div>

<div class="bannerBox"><div class="shine"></div><div style="padding:22px;position:relative;z-index:3"><div style="background:rgba(255,255,255,0.2);display:inline-block;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:800">PREMIUM OFFER</div><h3 style="font-size:20px;margin-top:10px;line-height:1.2">{{offer_title}}</h3><p style="margin-top:8px;opacity:.9;font-size:13px">{{offer_desc}}</p></div></div>

<div id="p-home" class="page active">
<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><h4 style="opacity:.8">💰 {{balance_title}}</h4><button onclick="claimDaily()" style="background:linear-gradient(135deg,#f59e0b,#f97316);border:none;padding:6px 12px;border-radius:20px;color:#fff;font-weight:800;font-size:11px;cursor:pointer">🎁 Daily ৳{{daily_bonus}}</button></div><h1 id="bal2" style="margin-top:12px;color:#22c55e;font-size:38px;letter-spacing:-1px">৳0</h1><div style="display:flex;gap:10px;margin-top:12px"><div style="flex:1;background:rgba(0,0,0,0.3);padding:10px;border-radius:12px;text-align:center"><small style="opacity:.6">Company</small><br><b id="cLim">0/50</b></div><div style="flex:1;background:rgba(0,0,0,0.3);padding:10px;border-radius:12px;text-align:center"><small style="opacity:.6">Popup</small><br><b id="pLim">0/30</b></div></div></div>
<div class="card"><h4 style="margin-bottom:12px">🚀 Premium Earning</h4><button class="btn" onclick="handleCompanyAd()">▶ Premium Ads - ৳<span id="adR">3</span> <small style="opacity:.8">• {{direct_link[:20]}}...</small></button><button class="btn btn2" onclick="handlePopupAd()">🎁 Bonus Ads - ৳<span id="popR">5</span> <small style="opacity:.8">• High Reward</small></button><p style="font-size:11px;opacity:.5;margin-top:10px;text-align:center">2 টা Monetag লিংক থেকে ইনকাম হবে</p></div>
</div>

<div id="p-tasks" class="page"><div class="card"><h4>✅ Premium Tasks</h4><p style="font-size:11px;opacity:.6;margin:6px 0">Complete & Earn Instant</p><div id="taskList"></div></div></div>

<div id="p-refer" class="page">
<div class="card"><h4>👥 Premium Refer</h4><p style="font-size:12px;opacity:.7;margin:8px 0">বন্ধু {{refer_condition_ads}} টা Ads দেখলে ৳{{refer_reward}} Instant</p><div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:14px;margin:10px 0"><input id="refLink" readonly style="background:transparent;border:none;color:#fff;width:100%;font-size:12px"><button class="btn" onclick="copyRef()">🔗 Copy Premium Link</button></div><div style="display:flex;gap:10px;margin-top:12px"><div style="flex:1;background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(124,58,237,0.2));padding:12px;border-radius:14px;text-align:center;border:1px solid rgba(139,92,246,0.2)"><b id="myRefCount" style="font-size:20px">0</b><br><small>Refer</small></div><div style="flex:1;background:rgba(0,0,0,0.2);padding:12px;border-radius:14px;text-align:center"><b id="refStatus" style="font-size:14px">pending</b><br><small>Status</small></div></div><div id="refList" style="margin-top:14px"></div></div>
</div>

<div id="p-support" class="page">
<div class="card"><h4>💎 Premium Support</h4><p style="font-size:12px;opacity:.7;margin:10px 0">24/7 Premium Support - Instant Reply</p>
<button class="btn" onclick="window.open('{{tg_channel}}','_blank')">📢 Premium Channel</button>
<button class="btn" style="background:linear-gradient(135deg,#25D366,#128C7E)" onclick="window.open('https://wa.me/{{whatsapp}}','_blank')">💬 WhatsApp Premium</button>
<button class="btn" style="background:linear-gradient(135deg,#0088cc,#006699)" onclick="window.open('{{support_link}}','_blank')">✈️ Telegram Support</button>
<div style="margin-top:16px;padding:14px;background:linear-gradient(135deg,rgba(139,92,246,0.15),rgba(245,158,11,0.1));border-radius:16px;border:1px solid rgba(139,92,246,0.2)"><div style="display:flex;gap:10px;align-items:center"><div style="width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#f59e0b);display:flex;align-items:center;justify-content:center;font-size:20px">👑</div><div><b>{{admin_name}}</b><br><small style="opacity:.7">Premium Admin • Online</small></div></div></div>
</div>
</div>

<div id="p-profile" class="page">
<div class="card"><div style="display:flex;gap:14px;align-items:center"><div class="profile" id="pImg2" style="width:70px;height:70px;font-size:32px;border-radius:20px">💎</div><div><h3 id="pName">User</h3><small id="pLevel" style="opacity:.7">Bronze Level</small><br><small id="pJoin" style="opacity:.5">Join: --</small></div></div><input id="editName" placeholder="আপনার Premium নাম" style="margin-top:14px"><input type="file" id="imgFile" accept="image/*"><button class="btn" onclick="saveProfile()">💎 Save Premium Profile</button></div>
<div class="card"><h4>💸 Premium Withdraw</h4><select id="wMethod"><option>bKash</option><option>Nagad</option></select><input id="wNumber" placeholder="01XXXXXXXXX"><input id="wAmount" type="number" placeholder="Amount (Min {{min_with}})"><button class="btn" onclick="doWithdraw()">💎 Premium Withdraw</button><p style="font-size:11px;opacity:.5;margin-top:8px;text-align:center">Min {{min_with}} Taka • Fast Payment</p></div>
<div class="card"><h4>📜 Premium History</h4><div id="wHistory"></div></div>
</div>

<div class="btm">
<div onclick="showPage('home')" id="b-home" class="on"><span>🏠</span>Home</div>
<div onclick="showPage('tasks')" id="b-tasks"><span>🎯</span>Tasks</div>
<div onclick="showPage('refer')" id="b-refer"><span>👥</span>Refer</div>
<div onclick="showPage('support')" id="b-support"><span>💎</span>Support</div>
<div onclick="showPage('profile')" id="b-profile"><span>👤</span>Profile</div>
</div>

<script>
let userId=localStorage.getItem("premiumUserId"); if(!userId){ userId="user_"+Date.now()+"_"+Math.floor(Math.random()*9999); localStorage.setItem("premiumUserId",userId); }
let savedRef=localStorage.getItem("myRef") || new URLSearchParams(window.location.search).get("ref"); if(savedRef) localStorage.setItem("myRef",savedRef);
let directLink="{{direct_link}}";
function init(){ fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,ref:savedRef})}).then(r=>r.json()).then(d=>{
document.getElementById('uName').innerText=d.user.name; document.getElementById('pName').innerText=d.user.name; document.getElementById('uId').innerText=d.user.id; document.getElementById('bal').innerText="৳"+d.user.balance; document.getElementById('bal2').innerText="৳"+d.user.balance; document.getElementById('totalEarn').innerText="৳"+d.user.total_earn; document.getElementById('uLevel').innerText=d.user.level; document.getElementById('pLevel').innerText=d.user.level+" Level"; document.getElementById('pJoin').innerText="Join: "+d.user.join_time;
document.getElementById('cLim').innerText=d.user.company_today+"/"+d.settings.company_limit; document.getElementById('pLim').innerText=d.user.popup_today+"/"+d.settings.popup_limit;
document.getElementById('adR').innerText=d.settings.ad_reward; document.getElementById('popR').innerText=d.settings.popup_reward;
document.getElementById('refLink').value=window.location.origin+"/?ref="+d.user.id; document.getElementById('myRefCount').innerText=d.user.refer_list.length; document.getElementById('refStatus').innerText=d.user.refer_status; document.getElementById('editName').value=d.user.name;
if(d.user.profile_img){ document.getElementById('pImg').innerHTML="<img src='"+d.user.profile_img+"' style='width:100%;height:100%;object-fit:cover;border-radius:18px'>"; document.getElementById('pImg2').innerHTML="<img src='"+d.user.profile_img+"' style='width:100%;height:100%;object-fit:cover;border-radius:20px'>"; }
let tl=""; d.tasks.forEach(t=>{ let done=d.user.tasks_done.includes(t.id); tl+=`<div class="taskCard"><div><b style="font-size:14px">${t.title}</b><br><small style="color:#22c55e;font-weight:700">৳${t.reward}</small></div><button class="btn" style="width:auto;padding:10px 20px;margin:0;font-size:12px" onclick="doTask(${t.id},'${t.link}')" ${done?'disabled':''}>${done?'✓ Done':'Go →'}</button></div>`; }); document.getElementById('taskList').innerHTML=tl;
let rl=""; d.user.refer_list.forEach(r=>{ rl+=`<div style="padding:10px;border-bottom:1px solid rgba(255,255,255,0.05);font-size:12px;display:flex;justify-content:space-between"><span>👤 ${r.name}</span><small style="opacity:.5">${r.time}</small></div>`; }); document.getElementById('refList').innerHTML=rl||"<small style='opacity:.5'>No referrals yet</small>";
let wh=""; d.withdraws.forEach(w=>{ wh+=`<div style="padding:10px;border-bottom:1px solid rgba(255,255,255,0.05);font-size:12px;display:flex;justify-content:space-between"><span>💸 ${w.method} ৳${w.amount}</span><span style="background:${w.status=='Pending'?'#f59e0b':'#22c55e'};padding:2px 8px;border-radius:20px;font-size:10px">${w.status}</span></div>`; }); document.getElementById('wHistory').innerHTML=wh||"<small style='opacity:.5'>No history</small>";
});}
function handleCompanyAd(){ window.open(directLink,"_blank"); if(typeof show_{{zone}}==='function'){ show_{{zone}}().then(()=>{ completeAd('company'); }); } else { completeAd('company'); } }
function handlePopupAd(){ window.open(directLink,"_blank"); completeAd('popup'); }
function completeAd(type){ fetch('/api/ads/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,type:type})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function claimDaily(){ fetch('/api/daily',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function doTask(id,link){ window.open(link,"_blank"); fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function saveProfile(){ let n=document.getElementById('editName').value; let file=document.getElementById('imgFile').files[0]; if(file){ let rd=new FileReader(); rd.onload=e=>{ fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,name:n,profile_img:e.target.result})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }; rd.readAsDataURL(file);} else { fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,name:n})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); } }
function doWithdraw(){ let m=document.getElementById('wMethod').value, num=document.getElementById('wNumber').value, amt=document.getElementById('wAmount').value; fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,method:m,number:num,amount:amt})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function showPage(p){ document.querySelectorAll('.page').forEach(x=>x.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); document.getElementById('b-'+p).classList.add('on'); }
function copyRef(){ let i=document.getElementById('refLink'); i.select(); document.execCommand('copy'); alert('✅ Premium Link Copied'); }
init();
</script></body></html>
    """, **s)

@app.route('/admin')
def admin():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Premium Admin A-Z</title>
<style>*{box-sizing:border-box;font-family:system-ui}body{max-width:650px;margin:0 auto;padding:12px;background:#0f172a;color:#fff}.card{padding:16px;border:1px solid rgba(255,255,255,0.1);border-radius:16px;margin-top:12px;background:rgba(30,41,59,0.8)}input{width:100%;padding:11px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background:rgba(15,23,42,0.9);color:#fff;margin-top:6px}.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(135deg,#8b5cf6,#7c3aed);margin-top:12px;cursor:pointer}</style></head><body>
<h2>💎 Premium Admin - Everything A-Z</h2>
<div class="card"><h4>💰 টাকার সব বাটন</h4><input id="bonus" placeholder="Join Bonus"><input id="ad_reward" placeholder="Company Reward"><input id="popup_reward" placeholder="Popup Reward"><input id="daily_bonus" placeholder="Daily Bonus"><input id="refer_reward" placeholder="Refer Reward"><input id="refer_condition_ads" placeholder="Refer Condition Ads"><input id="company_limit" placeholder="Company Limit"><input id="popup_limit" placeholder="Popup Limit"><input id="min_with" placeholder="Min Withdraw"></div>
<div class="card"><h4>🎨 Premium কালার - যেকোনো রং</h4><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div><input type="color" id="bg_color"><small>Background</small></div><div><input type="color" id="card_color"><small>Card</small></div><div><input type="color" id="top_color"><small>Top</small></div><div><input type="color" id="btn_color"><small>Btn1</small></div><div><input type="color" id="btn2_color"><small>Btn2</small></div><div><input type="color" id="text_color"><small>Text</small></div></div></div>
<div class="card"><h4>📝 লেখা + লিংক + সাপোর্ট Everything</h4><input id="app_name" placeholder="App Name"><input id="offer_title" placeholder="Offer Title"><input id="offer_desc" placeholder="Offer Desc"><input id="balance_title" placeholder="Balance Title"><input id="notice" placeholder="Notice"><input id="direct_link" placeholder="Direct Link 11760259"><input id="zone" placeholder="Zone 11764581"><input id="tg_channel" placeholder="TG Channel"><input id="support_link" placeholder="Support TG"><input id="whatsapp" placeholder="WhatsApp"><button class="btn" onclick="save()">💎 Save Everything</button></div>
<div class="card"><h4>➕ Task Add</h4><input id="newTitle" placeholder="Task Title"><input id="newReward" type="number" placeholder="Reward"><input id="newLink" placeholder="Link"><button class="btn" style="background:#22c55e" onclick="addTask()">Add Task</button><div id="taskAdmin"></div></div>
<div class="card"><h4>👥 Users A-Z</h4><div id="users"></div></div>
<div class="card"><h4>💸 Withdraws</h4><div id="wds"></div></div>
<script>
function load(){ fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:'admin'})}).then(r=>r.json()).then(d=>{ for(let k in d.settings){ let el=document.getElementById(k); if(el) el.value=d.settings[k]; } let th=""; d.tasks.forEach(t=>{ th+=`<div style="padding:8px;border-bottom:1px solid #333;display:flex;justify-content:space-between"><span>${t.title} - ৳${t.reward}</span><button onclick="delTask(${t.id})" style="background:#ef4444;border:none;color:#fff;padding:4px 8px;border-radius:6px">Del</button></div>`; }); document.getElementById('taskAdmin').innerHTML=th; }); fetch('/api/admin/users').then(r=>r.json()).then(u=>{ let h=""; for(let id in u){ let x=u[id]; h+=`<div style="border-bottom:1px solid #333;padding:10px 0"><b>${x.name}</b> (${x.id})<br>৳${x.balance} | Total ৳${x.total_earn} | Level ${x.level} | Ads ${x.ads_watched}<br>Ref ${x.refer_list.length} | ${x.join_time} | <small>${x.referred_by||'Direct'}</small></div>`; } document.getElementById('users').innerHTML=h; }); fetch('/api/admin/withdraws').then(r=>r.json()).then(w=>{ let h=""; w.forEach(x=>{ h+=`<div style="border-bottom:1px solid #333;padding:8px 0">${x.name} - ৳${x.amount} - ${x.method} - ${x.number} - ${x.status} - ${x.time}</div>`}); document.getElementById('wds').innerHTML=h; });}
function save(){ let data={}; document.querySelectorAll('input').forEach(i=>{ if(i.id && i.id.startsWith('new')) return; if(i.value) data[i.id]= i.type=='color'? i.value : (isNaN(i.value)||i.value.includes('#')||i.value.includes('http')? i.value : parseInt(i.value)); }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ alert(d.msg); }); }
function addTask(){ let t=document.getElementById('newTitle').value, r=document.getElementById('newReward').value, l=document.getElementById('newLink').value; fetch('/api/admin/task/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:t,reward:r,link:l})}).then(r=>r.json()).then(d=>{ alert(d.msg); load(); }); }
function delTask(id){ fetch('/api/admin/task/del',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id})}).then(r=>r.json()).then(d=>{ load(); }); }
load();
</script></body></html>
    """)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
