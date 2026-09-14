# -*- coding: utf-8 -*-
# FINAL BEAUTIFUL - 5 Button + Profile Photo + Support + Withdraw Beautiful + Shine + Glass
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def load_db():
    defaults={"app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","app_logo":"👑","zone":"11764581","direct_link":"https://omg10.com/4/11760259","bonus":50,"ad_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"task_limit":5,"min_with":500,"refer_reward":50,"refer_condition_ads":10,"bg_color":"#070710","card_color":"#17172a","top_color":"#0e0e20","btn_color":"#6d4cff","btn2_color":"#f59e0b","text_color":"#ffffff","offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!","balance_title":"আপনার বর্তমান ব্যালেন্স","tg_channel":"https://t.me/","support_link":"https://t.me/","whatsapp":"01XXXXXXXXX","notice":"🎉 Daily Bonus Available • Official Ad • Trusted"}
    if not os.path.exists(DB):
        data={"users":{},"withdraws":[],"settings":defaults,"tasks":[{"id":1,"title":"Join Telegram Channel","reward":10,"link":"https://t.me/"},{"id":2,"title":"Subscribe YouTube","reward":15,"link":"https://youtube.com/"},{"id":3,"title":"Follow Facebook","reward":10,"link":"https://facebook.com/"}]}
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
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","profile_img":"","balance":db["settings"]["bonus"],"total":0,"company_today":0,"popup_today":0,"tasks_done":[],"join_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"last_date":str(datetime.now().date()),"referred_by":ref,"refer_list":[],"refer_status":"pending","ads_watched":0}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refer_list"].append({"id":uid,"name":db["users"][uid]["name"],"time":db["users"][uid]["join_time"]})
    return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def api_init():
    db=load_db(); j=request.json; uid=str(j.get('id')); ref=j.get('ref')
    if ref==uid: ref=None
    u=get_user(db,uid,ref); today=str(datetime.now().date())
    if u.get("last_date")!=today: u["company_today"]=0; u["popup_today"]=0; u["last_date"]=today
    save_db(db); return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":[w for w in db["withdraws"] if w["uid"]==uid]})

@app.route('/api/ads/complete',methods=['POST'])
def ads_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); typ=j.get('type','company'); u=get_user(db,uid); s=db["settings"]
    if typ=='company':
        if u["company_today"]>=s["company_limit"]: return jsonify({"msg":f"লিমিট {s['company_limit']} শেষ"})
        u["company_today"]+=1; u["balance"]+=s["ad_reward"]; msg=f"✅ ৳{s['ad_reward']} যোগ"
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"লিমিট {s['popup_limit']} শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]; msg=f"✅ ৳{s['popup_reward']} যোগ"
    u["ads_watched"]+=1; ref=u.get("referred_by")
    if ref and ref in db["users"] and u["ads_watched"]>=s["refer_condition_ads"] and u["refer_status"]=="pending": db["users"][ref]["balance"]+=s["refer_reward"]; u["refer_status"]="completed"
    save_db(db); return jsonify({"msg":msg})

@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db(); j=request.json; uid=str(j.get('id')); tid=int(j.get('task_id')); u=get_user(db,uid)
    if tid in u["tasks_done"]: return jsonify({"msg":"Done"})
    task=next((t for t in db["tasks"] if t["id"]==tid),None); u["tasks_done"].append(tid); u["balance"]+=task["reward"]; save_db(db); return jsonify({"msg":f"✅ ৳{task['reward']} যোগ"})

@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid); s=db["settings"]
    amt=int(j.get('amount',0)); num=j.get('number',''); method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']} টাকা"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt; db["withdraws"].append({"uid":uid,"name":u["name"],"amount":amt,"number":num,"method":method,"status":"Pending","time":datetime.now().strftime("%Y-%m-%d %H:%M")}); save_db(db); return jsonify({"msg":f"✅ ৳{amt} Request সফল"})

@app.route('/api/user/update',methods=['POST'])
def user_update():
    db=load_db(); j=request.json; uid=str(j.get('id')); u=get_user(db,uid)
    if 'name' in j: u["name"]=str(j['name'])[:25]
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save_db(db); return jsonify({"msg":"✅ প্রোফাইল সুন্দরভাবে সেভ হয়েছে"})

@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db(); j=request.json
    for k in j: db["settings"][k]=j[k]
    save_db(db); return jsonify({"msg":"✅ Saved"})
@app.route('/api/admin/users')
def admin_users(): return jsonify(load_db()["users"])
@app.route('/api/admin/withdraws')
def admin_withdraws(): return jsonify(load_db()["withdraws"])

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>{{app_name}}</title>
<script src='//libtl.com/sdk.js' data-zone='{{zone}}' data-sdk='show_{{zone}}'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:{{bg_color}};color:{{text_color}};max-width:430px;margin:0 auto;padding-bottom:230px!important}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:{{top_color}};position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{margin:12px;border-radius:22px;padding:18px;background:linear-gradient(145deg, rgba(23,23,42,0.95), rgba(14,14,32,0.95));backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.12);box-shadow:0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);position:relative;overflow:hidden}
.card:before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent)}
.btn{width:100%;padding:15px;border:none;border-radius:14px;font-weight:800;color:#fff;margin-top:10px;cursor:pointer;background:{{btn_color}};box-shadow:0 6px 20px rgba(109,76,255,0.35);transition:0.2s}
.btn:active{transform:scale(0.97)}
.btn2{background:linear-gradient(90deg,{{btn2_color}},#ef4444)!important;box-shadow:0 6px 20px rgba(245,158,11,0.35)!important}
.profile{width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,#1e293b,#334155);display:flex;align-items:center;justify-content:center;border:2px solid {{btn_color}};overflow:hidden;font-size:28px;box-shadow:0 0 25px rgba(109,76,255,0.5)}
.bannerBox{margin:12px;border-radius:24px;overflow:hidden;height:170px;background:linear-gradient(90deg,{{btn2_color}},#ef4444);position:relative;border:2px solid rgba(255,255,255,0.15);box-shadow:0 10px 30px rgba(245,158,11,0.3)}
.shine{position:absolute;top:0;left:-100%;width:70%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.4),transparent);transform:skewX(-20deg);animation:shineMove 3s infinite;z-index:2}
@keyframes shineMove{0%{left:-100%}100%{left:200%}}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.97);backdrop-filter:blur(15px);display:flex;padding:10px 0 16px;border-radius:26px 26px 0 0;border-top:1px solid rgba(255,255,255,0.1);box-shadow:0 -5px 25px rgba(0,0,0,0.5);z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:10px;font-weight:800;cursor:pointer;transition:0.2s}.btm div.on{color:#fff;transform:translateY(-2px)}.btm div span{font-size:22px;display:block;margin-bottom:2px}
.page{display:none}.page.active{display:block}
.taskCard{display:flex;justify-content:space-between;align-items:center;padding:14px;border:1px solid rgba(255,255,255,0.08);border-radius:14px;margin-top:12px;background:rgba(17,17,40,0.8);box-shadow:0 4px 15px rgba(0,0,0,0.2)}
.marquee{background:rgba(14,14,32,0.9);padding:10px;overflow:hidden;white-space:nowrap;margin:12px;border-radius:12px;border:1px solid rgba(255,255,255,0.08)}
input,select{width:100%;padding:13px;border-radius:12px;border:1px solid rgba(255,255,255,0.1);background:rgba(10,10,26,0.9);color:#fff;margin-top:8px;box-shadow:inset 0 2px 5px rgba(0,0,0,0.3)}
</style></head><body>
<div class="top"><div style="display:flex;gap:12px;align-items:center"><div class="profile" id="pImg">👑</div><div><b id="uName">Loading...</b><br><small id="uId" style="opacity:.6"></small></div></div><div id="bal" style="font-weight:900;color:#22c55e;font-size:18px">৳0</div></div>
<div class="marquee"><span>{{notice}}</span></div>
<div class="bannerBox"><div class="shine"></div><div style="padding:20px;position:relative;z-index:3"><h3 style="font-size:18px">{{offer_title}}</h3><p style="margin-top:8px;opacity:.9;font-size:13px">{{offer_desc}}</p></div></div>

<div id="p-home" class="page active">
<div class="card"><h4 style="opacity:.9">💰 {{balance_title}}</h4><h1 id="bal2" style="margin-top:10px;color:#22c55e;font-size:36px">৳0</h1><p style="opacity:.6;font-size:12px;margin-top:6px">Company: <span id="cLim">0/30</span> | Popup: <span id="pLim">0/20</span></p></div>
<div class="card"><h4>📢 Official Ads</h4><button class="btn" onclick="handleCompanyAd()">▶ Company Ads - ৳<span id="adR">2</span></button><button class="btn btn2" onclick="handlePopupAd()">🎁 Popup Ads - ৳<span id="popR">3</span></button></div>
</div>

<div id="p-tasks" class="page"><div class="card"><h4>✅ Daily Tasks</h4><div id="taskList"></div></div></div>

<div id="p-refer" class="page">
<div class="card"><h4>👥 রেফার করুন</h4><p style="font-size:12px;opacity:.7;margin:8px 0">বন্ধু {{refer_condition_ads}} টা Ads দেখলে ৳{{refer_reward}} পাবেন</p><input id="refLink" readonly><button class="btn" onclick="copyRef()">🔗 লিংক কপি করুন</button><p style="margin-top:12px;font-size:13px">আপনার রেফার: <b id="myRefCount">0</b> জন</p><div id="refList" style="margin-top:10px"></div></div>
</div>

<div id="p-support" class="page">
<div class="card"><h4>📞 সাপোর্ট সিস্টেম</h4><p style="font-size:12px;opacity:.7;margin:10px 0">যেকোনো সমস্যায় যোগাযোগ করুন</p>
<button class="btn" onclick="window.open('{{tg_channel}}','_blank')">📢 Telegram Channel</button>
<button class="btn" style="background:#25D366" onclick="window.open('https://wa.me/{{whatsapp}}','_blank')">💬 WhatsApp Support</button>
<button class="btn" style="background:#0088cc" onclick="window.open('{{support_link}}','_blank')">✈️ Telegram Support</button>
<div style="margin-top:14px;padding:12px;background:rgba(10,10,26,0.8);border-radius:12px;border:1px solid rgba(255,255,255,0.05)"><b>Admin: {{admin_name}}</b><br><small style="opacity:.7">24/7 Support Available</small></div>
</div>
</div>

<div id="p-profile" class="page">
<div class="card"><h4>👤 প্রোফাইল</h4><input id="editName" placeholder="আপনার নাম"><input type="file" id="imgFile" accept="image/*"><button class="btn" onclick="saveProfile()">💾 সেভ করুন</button></div>
<div class="card"><h4>💸 টাকা তুলুন</h4><select id="wMethod"><option>bKash</option><option>Nagad</option></select><input id="wNumber" placeholder="01XXXXXXXXX"><input id="wAmount" type="number" placeholder="Amount"><button class="btn" onclick="doWithdraw()">Withdraw</button></div>
<div class="card"><h4>📜 Withdraw History</h4><div id="wHistory"></div></div>
</div>

<div class="btm">
<div onclick="showPage('home')" id="b-home" class="on"><span>🏠</span>Home</div>
<div onclick="showPage('tasks')" id="b-tasks"><span>✅</span>Tasks</div>
<div onclick="showPage('refer')" id="b-refer"><span>👥</span>Refer</div>
<div onclick="showPage('support')" id="b-support"><span>📞</span>Support</div>
<div onclick="showPage('profile')" id="b-profile"><span>👤</span>Profile</div>
</div>

<script>
let userId=localStorage.getItem("myAppUserId"); if(!userId){ userId="user_"+Date.now()+"_"+Math.floor(Math.random()*9999); localStorage.setItem("myAppUserId",userId); }
let savedRef=localStorage.getItem("myRef") || new URLSearchParams(window.location.search).get("ref"); if(savedRef) localStorage.setItem("myRef",savedRef);
let directLink="{{direct_link}}";
function init(){ fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,ref:savedRef})}).then(r=>r.json()).then(d=>{
document.getElementById('uName').innerText=d.user.name; document.getElementById('uId').innerText=d.user.id; document.getElementById('bal').innerText="৳"+d.user.balance; document.getElementById('bal2').innerText="৳"+d.user.balance;
document.getElementById('cLim').innerText=d.user.company_today+"/"+d.settings.company_limit; document.getElementById('pLim').innerText=d.user.popup_today+"/"+d.settings.popup_limit;
document.getElementById('adR').innerText=d.settings.ad_reward; document.getElementById('popR').innerText=d.settings.popup_reward;
document.getElementById('refLink').value=window.location.origin+"/?ref="+d.user.id; document.getElementById('myRefCount').innerText=d.user.refer_list.length; document.getElementById('editName').value=d.user.name;
if(d.user.profile_img){ document.getElementById('pImg').innerHTML="<img src='"+d.user.profile_img+"' style='width:100%;height:100%;object-fit:cover'>"; }
let tl=""; d.tasks.forEach(t=>{ let done=d.user.tasks_done.includes(t.id); tl+=`<div class="taskCard"><div><b>${t.title}</b><br><small style="color:#22c55e">৳${t.reward}</small></div><button class="btn" style="width:auto;padding:10px 18px;margin:0" onclick="doTask(${t.id},'${t.link}')" ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`; }); document.getElementById('taskList').innerHTML=tl;
let rl=""; d.user.refer_list.forEach(r=>{ rl+=`<div style="padding:8px;border-bottom:1px solid rgba(255,255,255,0.05);font-size:12px">👤 ${r.name} - ${r.time}</div>`; }); document.getElementById('refList').innerHTML=rl||"<small style='opacity:.5'>কেউ নাই</small>";
let wh=""; d.withdraws.forEach(w=>{ wh+=`<div style="padding:8px;border-bottom:1px solid rgba(255,255,255,0.05);font-size:12px">💸 ${w.method} ৳${w.amount} - ${w.status}</div>`; }); document.getElementById('wHistory').innerHTML=wh||"<small style='opacity:.5'>No history</small>";
});}
function handleCompanyAd(){ window.open(directLink,"_blank"); if(typeof show_{{zone}}==='function'){ show_{{zone}}().then(()=>{ completeAd('company'); }); } else { completeAd('company'); } }
function handlePopupAd(){ window.open(directLink,"_blank"); completeAd('popup'); }
function completeAd(type){ fetch('/api/ads/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,type:type})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function doTask(id,link){ window.open(link,"_blank"); fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,task_id:id})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function saveProfile(){ let n=document.getElementById('editName').value; let file=document.getElementById('imgFile').files[0]; if(file){ let rd=new FileReader(); rd.onload=e=>{ fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,name:n,profile_img:e.target.result})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }; rd.readAsDataURL(file);} else { fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,name:n})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); } }
function doWithdraw(){ let m=document.getElementById('wMethod').value, num=document.getElementById('wNumber').value, amt=document.getElementById('wAmount').value; fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:userId,method:m,number:num,amount:amt})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); }); }
function showPage(p){ document.querySelectorAll('.page').forEach(x=>x.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); document.getElementById('b-'+p).classList.add('on'); }
function copyRef(){ let i=document.getElementById('refLink'); i.select(); document.execCommand('copy'); alert('✅ লিংক কপি হয়েছে'); }
init();
</script></body></html>
    """, **s)

@app.route('/admin')
def admin():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin</title>
<style>*{box-sizing:border-box;font-family:system-ui}body{max-width:600px;margin:0 auto;padding:12px;background:#070710;color:#fff}.card{padding:14px;border:1px solid #222;border-radius:12px;margin-top:12px;background:#111128}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0a0a1a;color:#fff;margin-top:6px}.btn{width:100%;padding:12px;border:none;border-radius:10px;font-weight:800;color:#fff;background:#6d4cff;margin-top:10px}</style></head><body>
<h2>👑 Admin Beautiful + 5 Button</h2>
<div class="card"><h4>💰 টাকা</h4><input id="bonus"><input id="ad_reward"><input id="popup_reward"><input id="refer_reward"><input id="refer_condition_ads"><input id="company_limit"><input id="popup_limit"><input id="min_with"></div>
<div class="card"><h4>🎨 রং</h4><input type="color" id="bg_color" style="width:60px"><input type="color" id="card_color" style="width:60px"><input type="color" id="top_color" style="width:60px"><input type="color" id="btn_color" style="width:60px"><input type="color" id="btn2_color" style="width:60px"><input type="color" id="text_color" style="width:60px"></div>
<div class="card"><h4>📝 লেখা + Support</h4><input id="offer_title"><input id="offer_desc"><input id="balance_title"><input id="notice"><input id="direct_link"><input id="zone"><input id="tg_channel"><input id="support_link"><input id="whatsapp"><input id="app_name"><button class="btn" onclick="save()">💾 Save Beautiful</button></div>
<div class="card"><div id="users"></div></div>
<script>
function load(){ fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:'admin'})}).then(r=>r.json()).then(d=>{ for(let k in d.settings){ let el=document.getElementById(k); if(el) el.value=d.settings[k]; } });}
function save(){ let data={}; document.querySelectorAll('input').forEach(i=>{ if(i.value) data[i.id]= i.type=='color'? i.value : (isNaN(i.value)||i.value.includes('#')||i.value.includes('http')? i.value : parseInt(i.value)); }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ alert(d.msg); location.reload(); }); }
load();
</script></body></html>
    """)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
