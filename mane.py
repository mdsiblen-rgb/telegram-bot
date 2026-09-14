# -*- coding: utf-8 -*-
# FINAL FULL 5 PAGES - HOME/TASKS/REFER/WITHDRAW/PROFILE - ZONE 3490663
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'
def default_data():
    return {"users":{}, "withdraws":[], "settings":{"app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","app_logo":"👑","admin_profile_img":"","zone":"3490663","bonus":1120,"ad_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"task_limit":5,"min_with":500,"official_banners":[],"google_ads":["🎉 Daily Bonus Available","⭐ Official Ad • bKash • Nagad","📢 100% Safe & Trusted"],"offer_title":"🎉 আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!","balance_title":"আপনার বর্তমান ব্যালেন্স","tg_channel":"https://t.me/","support_link":"https://t.me/","whatsapp":"01XXXXXXXXX","tutorial_video":"https://youtube.com/"},"tasks":[{"id":1,"title":"Telegram Channel Join","reward":25,"icon":"✈️","link":"https://t.me/","desc":"চ্যানেলে জয়েন করুন"},{"id":2,"title":"YouTube Subscribe","reward":30,"icon":"▶️","link":"https://youtube.com/","desc":"সাবস্ক্রাইব + লাইক"},{"id":3,"title":"Facebook Page Like","reward":20,"icon":"👍","link":"https://facebook.com/","desc":"পেজে লাইক দিন"},{"id":4,"title":"Refer Friend","reward":50,"icon":"👨‍👩‍👧‍👦","link":"","desc":"১ জন রেফার = ৳50"},{"id":5,"title":"Daily Check-in","reward":15,"icon":"✅","link":"","desc":"প্রতিদিন একবার"}]}
def load_db():
    if not os.path.exists(DB):
        d=default_data()
        open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2));return d
    try: return json.load(open(DB,'r',encoding='utf-8'))
    except: d=default_data(); open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2));return d
def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid);today=str(datetime.now().date())
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":"","profile_img":"","balance":db["settings"]["bonus"],"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":today}
    u=db["users"][uid]
    if u.get("last")!=today: u["ads_today"]=0;u["popup_today"]=0;u["tasks_done"]=[];u["last"]=today
    return u
@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin only",403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get')
def api_get():
    db=load_db();u=get_user(db,request.args.get('id','0'));save_db(db)
    wds=[w for w in db.get("withdraws",[]) if w["uid"]==str(request.args.get('id','0'))]
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"],"withdraws":wds})
@app.route('/api/reward')
def api_reward():
    db=load_db();u=get_user(db,request.args.get('id'));typ=request.args.get('type','company');s=db["settings"]
    if typ=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":f"Limit {s['company_limit']} শেষ"})
        u["ads_today"]+=1;u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":f"Limit {s['popup_limit']} শেষ"})
        u["popup_today"]+=1;u["balance"]+=s["popup_reward"]
    u["total"]+=1;save_db(db);return jsonify({"msg":"৳ যোগ হয়েছে"})
@app.route('/api/task/complete',methods=['POST'])
def task_complete():
    db=load_db();j=request.json;uid=str(j.get('id'));tid=int(j.get('task_id'));u=get_user(db,uid)
    if tid in u["tasks_done"]: return jsonify({"msg":"আজকে করা হয়েছে"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    if not t: return jsonify({"msg":"Task নেই"})
    u["tasks_done"].append(tid);u["balance"]+=t["reward"];u["total"]+=1;save_db(db);return jsonify({"msg":f"✅ {t['title']} ৳{t['reward']}"})
@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db();j=request.json;uid=str(j.get('id'));u=get_user(db,uid);s=db["settings"];amt=int(j.get('amount',0));num=j.get('number','');method=j.get('method','bKash')
    if amt < s["min_with"]: return jsonify({"msg":f"মিনিমাম {s['min_with']}"})
    if u["balance"] < amt: return jsonify({"msg":"ব্যালেন্স কম"})
    if len(num)<11: return jsonify({"msg":"সঠিক নাম্বার দিন"})
    u["balance"]-=amt;db["withdraws"].append({"uid":uid,"amount":amt,"number":num,"method":method,"status":"Pending","time":str(datetime.now())[:16]});save_db(db);return jsonify({"msg":f"✅ {method} ৳{amt} Request সফল"})
@app.route('/api/user/update',methods=['POST'])
def user_update():
    db=load_db();j=request.json;uid=str(j.get('id'));u=get_user(db,uid)
    if 'name' in j: u["name"]=str(j['name'])[:25]
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save_db(db);return jsonify({"msg":"✅ প্রোফাইল সেভ"})
@app.route('/api/admin/save',methods=['POST'])
def api_save():
    db=load_db();j=request.json
    for k in j:
        if k.startswith("google_ad"):
            try: idx=int(k[-1])-1;db["settings"]["google_ads"][idx]=j[k]
            except: pass
        elif k.startswith("task_"):
            try:
                parts=k.split('_');tid=int(parts[1]);field='_'.join(parts[2:])
                for t in db["tasks"]:
                    if t["id"]==tid:
                        if field=='reward': t[field]=int(j[k])
                        else: t[field]=j[k]
            except: pass
        else: db["settings"][k]=j[k]
    save_db(db);return jsonify({"msg":"✅ Saved"})
@app.route('/api/admin/upload',methods=['POST'])
def upload():
    db=load_db();j=request.json
    if 'banner' in j:
        if len(db["settings"]["official_banners"])>=5: db["settings"]["official_banners"].pop(0)
        db["settings"]["official_banners"].append(j['banner']);save_db(db);return jsonify({"msg":f"✅ ব্যানার {len(db['settings']['official_banners'])}/5"})
    if 'clear_banner' in j: db["settings"]["official_banners"]=[];save_db(db);return jsonify({"msg":"🗑️ মুছা হয়েছে"})
    return jsonify({"msg":"Error"})
USER_HTML="""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="//libtl.com/sdk.js" data-zone="3490663" data-sdk="show_3490663"></script><style>*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:125px}.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,#17172a,#0e0e20);border:1px solid #222;position:relative;overflow:hidden}.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;font-size:14px;color:#fff;margin-top:8px;cursor:pointer;background:linear-gradient(90deg,#6d4cff,#e2136e)}.profile{width:52px;height:52px;border-radius:50%;background:#1e293b;display:flex;align-items:center;justify-content:center;border:2px solid #6d4cff;overflow:hidden;font-size:26px}.profile img{width:100%;height:100%;object-fit:cover}.profileBig{width:100px;height:100px;border-radius:50%;background:#1e293b;display:flex;align-items:center;justify-content:center;border:3px solid #6d4cff;margin:0 auto;overflow:hidden;font-size:44px;position:relative}.profileBig img{width:100%;height:100%;object-fit:cover}.camIcon{position:absolute;bottom:2px;right:2px;background:#6d4cff;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;border:2px solid #0e0e20}.bannerBox{margin:12px;border-radius:22px;overflow:hidden;height:150px;background:linear-gradient(90deg,#f59e0b,#ef4444);position:relative;border:2px solid rgba(255,255,255,0.15)}.shine{position:absolute;top:0;left:-100%;width:65%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35),transparent);transform:skewX(-20deg);animation:shineMove 2.8s infinite;z-index:2}@keyframes shineMove{0%{left:-100%}100%{left:200%}}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:8px 0 12px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}.btm div{flex:1;text-align:center;color:#6b7280;font-size:10px;font-weight:800;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:20px;display:block}.page{display:none}.page.active{display:block}.taskCard{display:flex;justify-content:space-between;align-items:center;background:#15152a;border:1px solid #2a2a4a;border-radius:14px;padding:12px;margin:10px 0}.payCard{display:flex;align-items:center;gap:12px;background:#15152a;border:2px solid #2a2a4a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}.payCard.active{border-color:#e2136e;background:#1e1e3a}.payLogo{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#fff;font-size:22px}.faq{background:#15152a;border:1px solid #2a2a4a;border-radius:12px;padding:12px;margin:8px 0}.statBox{background:#15152a;border:1px solid #2a2a4a;border-radius:14px;padding:12px;text-align:center;flex:1}input{width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#111;color:#fff;margin-top:8px}</style></head><body><div class="top"><div style="font-weight:900">👑 <span id="appName">Protidiner Kaj BD</span></div><div class="profile" onclick="nav('profile',document.querySelectorAll('.btm div')[4])"><span id="topP">👤</span></div></div><div id="p_home" class="page active"><div class="bannerBox"><div class="shine"></div><div style="padding:18px;position:relative;z-index:3"><h2 id="offerTitle">🎉 আজকের স্পেশাল অফার</h2><p id="offerDesc" style="margin-top:6px">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</p></div></div><div class="card"><h3 id="balTitle">আপনার বর্তমান ব্যালেন্স</h3><h1 style="font-size:34px;margin:8px 0">৳<span id="bal">0</span></h1><div style="display:flex;gap:8px"><div class="statBox"><small>Company</small><br><b><span id="adC">0</span>/30</b></div><div class="statBox"><small>Popup</small><br><b><span id="popC">0</span>/20</b></div><div class="statBox"><small>Total</small><br><b><span id="tot">0</span></b></div></div><button class="btn" onclick="showAd('company')">📺 Company Ad দেখুন (৳2)</button><button class="btn" style="background:linear-gradient(90deg,#f59e0b,#ef4444)" onclick="showAd('popup')">🎁 Popup Ad (৳3)</button></div><div class="card" id="gAds"></div></div><div id="p_tasks" class="page"><div class="card"><h3>📋 Tasks - 5 টি</h3><div id="taskList"></div></div><div class="card"><h3>❓ FAQ</h3><div class="faq"><b>কিভাবে ইনকাম করব?</b><br>Ads + Task + Refer</div><div class="faq"><b>Withdraw কখন?</b><br>24 ঘন্টার মধ্যে</div></div></div><div id="p_refer" class="page"><div class="card" style="text-align:center"><h3>👨‍👩‍👧‍👦 Refer & Earn</h3><p style="margin:10px 0">প্রতি রেফারে ৳50</p><div class="payCard"><div class="payLogo" style="background:#6d4cff">🔗</div><div style="text-align:left;flex:1"><small>আপনার Refer Link</small><br><b id="refLink" style="font-size:11px;word-break:break-all">https://t.me/YourBot?start=123</b></div></div><button class="btn" onclick="copyRef()">📋 Link Copy করুন</button></div></div><div id="p_with" class="page"><div class="card"><h3>💸 Withdraw</h3><div style="display:flex;gap:8px;margin:10px 0"><div class="payCard active" style="flex:1" id="bk" onclick="setM('bKash',this)"><div class="payLogo" style="background:#e2136e">B</div><b>bKash</b></div><div class="payCard" style="flex:1" id="ng" onclick="setM('Nagad',this)"><div class="payLogo" style="background:#f59e0b">N</div><b>Nagad</b></div></div><input id="wNum" placeholder="Number 01XXXXXXXXX"><input id="wAmt" type="number" placeholder="Amount Min 500"><button class="btn" onclick="doW()">Withdraw করুন</button><div id="wList" style="margin-top:12px"></div></div></div><div id="p_profile" class="page"><div class="card" style="text-align:center"><div class="profileBig" onclick="document.getElementById('fileIn').click()"><span id="bigP">👤</span><div class="camIcon">📷</div></div><input type="file" id="fileIn" accept="image/*" style="display:none" onchange="upImg(this)"><input id="nameIn" placeholder="আপনার নাম"><button class="btn" onclick="saveP()">✅ প্রোফাইল সেভ</button><div style="text-align:left;margin-top:12px"><div class="payCard"><div class="payLogo" style="background:#6d4cff">ID</div><div><small>User ID</small><br><b id="uid"></b></div></div><div class="payCard"><div class="payLogo" style="background:#e2136e">📅</div><div><small>Join</small><br><b id="join"></b></div></div></div><a id="tut" target="_blank" style="color:#6d4cff;display:block;margin-top:10px">📺 Tutorial Video</a></div></div><div class="btm"><div class="on" onclick="nav('home',this)"><span>🏠</span>Home</div><div onclick="nav('tasks',this)"><span>📋</span>Tasks</div><div onclick="nav('refer',this)"><span>👨‍👩‍👧‍👦</span>Refer</div><div onclick="nav('with',this)"><span>💸</span>Withdraw</div><div onclick="nav('profile',this)"><span>👤</span>Profile</div></div><script>let uid=new URLSearchParams(location.search).get('id')||'12345';let curM='bKash';function nav(p,el){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p_'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));el.classList.add('on');}
function setM(m,el){curM=m;document.querySelectorAll('#p_with.payCard').forEach(x=>x.classList.remove('active'));el.classList.add('active');}
function load(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{let s=d.settings,u=d.user;document.getElementById('bal').innerText=u.balance;document.getElementById('adC').innerText=u.ads_today;document.getElementById('popC').innerText=u.popup_today;document.getElementById('tot').innerText=u.total;document.getElementById('uid').innerText=u.id;document.getElementById('join').innerText=u.join_date;document.getElementById('appName').innerText=s.app_name;document.getElementById('balTitle').innerText=s.balance_title;document.getElementById('offerTitle').innerText=s.offer_title;document.getElementById('offerDesc').innerText=s.offer_desc;document.getElementById('tut').href=s.tutorial_video;document.getElementById('gAds').innerHTML=s.google_ads.map(a=>'• '+a).join('<br>');document.getElementById('refLink').innerText='https://t.me/YourBot?start='+u.id;if(u.profile_img){document.getElementById('bigP').innerHTML='<img src="'+u.profile_img+'">';document.getElementById('topP').innerHTML='<img src="'+u.profile_img+'">';}if(u.name)document.getElementById('nameIn').value=u.name;let tl='';d.tasks.forEach(t=>{tl+=`<div class="taskCard"><div><b>${t.icon} ${t.title}</b><br><small>${t.desc}</small></div><button class="btn" style="width:auto;padding:8px 14px" onclick="doT(${t.id},'${t.link}')">${t.reward}৳</button></div>`});document.getElementById('taskList').innerHTML=tl;let wl='';d.withdraws.slice(-5).reverse().forEach(w=>{wl+=`<div class="faq">${w.method} ৳${w.amount} - ${w.status}<br><small>${w.time} - ${w.number}</small></div>`});document.getElementById('wList').innerHTML=wl;});}
function showAd(t){if(typeof show_3490663==='function'){if(t==='popup'){show_3490663({type:'popup'}).then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(()=>load());});}else{show_3490663().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(()=>load());});}}else{alert('Ad লোড হচ্ছে...');}}
function doT(id,link){if(link)window.open(link,'_blank');fetch('/api/task/complete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,task_id:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load();});}
function upImg(inp){let f=inp.files[0];if(!f)return;let r=new FileReader();r.onload=function(e){document.getElementById('bigP').innerHTML='<img src="'+e.target.result+'">';document.getElementById('topP').innerHTML='<img src="'+e.target.result+'">';window._tmp=e.target.result;};r.readAsDataURL(f);}
function saveP(){let b={id:uid,name:document.getElementById('nameIn').value};if(window._tmp)b.profile_img=window._tmp;fetch('/api/user/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(r=>r.json()).then(d=>{alert(d.msg);load();});}
function doW(){fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,number:document.getElementById('wNum').value,amount:document.getElementById('wAmt').value,method:curM})}).then(r=>r.json()).then(d=>{alert(d.msg);load();});}
function copyRef(){let t=document.getElementById('refLink').innerText;navigator.clipboard.writeText(t);alert('✅ Copy হয়েছে: '+t);}
load();</script></body></html>
"""
ADMIN_HTML="""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#111;color:#fff;font-family:system-ui;padding:12px}input{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#222;color:#fff}.btn{padding:12px;border:none;border-radius:10px;background:#6d4cff;color:#fff;font-weight:800;width:100%;margin-top:10px}</style></head><body><h2>👑 Admin - 3490663 - Full 5 Pages</h2><div id="form"></div><button class="btn" onclick="save()">Save</button><script>let sid='8807178385';fetch('/api/get?id='+sid).then(r=>r.json()).then(d=>{let s=d.settings;let h='';h+=`<input id="app_name" value="${s.app_name}"><input id="offer_title" value="${s.offer_title}"><input id="offer_desc" value="${s.offer_desc}"><input id="balance_title" value="${s.balance_title}"><input id="tutorial_video" value="${s.tutorial_video}"><input id="bonus" value="${s.bonus}"><input id="ad_reward" value="${s.ad_reward}"><input id="popup_reward" value="${s.popup_reward}">`;d.tasks.forEach(t=>{h+=`<hr><b>Task ${t.id}</b><input id="task_${t.id}_title" value="${t.title}"><input id="task_${t.id}_reward" value="${t.reward}"><input id="task_${t.id}_link" value="${t.link}">`});document.getElementById('form').innerHTML=h;});function save(){let o={};document.querySelectorAll('input').forEach(i=>{o[i.id]=i.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)}).then(r=>r.json()).then(d=>alert(d.msg));}</script></body></html>
"""
if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
