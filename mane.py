import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime, timedelta
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    default = {
        "users":{},
        "w":[],
        "s":{
            "admin_name":"প্রতিদিনের কাজ BD",
            "admin_pic":"https://i.pravatar.cc/150?img=32",
            "profile_box":"✅ Official Telegram Channel এ Join করুন - @ProtidinerKajBD",
            "ads_limit":100,
            "ads_reward":2,
            "refer_bonus":20,
            "notice_title":"অফিসিয়াল নোটিস",
            "notice_sub":"প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম করুন",
            "slider":["https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600","https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"],
            "tasks":[
                {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","btn":"Join & Get 25 Tk"},
                {"title":"Telegram Join","reward":10,"link":"https://t.me","color":"#1e40af","btn":"Join & Get 10 Tk"},
                {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9","btn":"Follow & Get 15 Tk"},
                {"title":"Website Visit","reward":20,"link":"https://google.com","color":"#7c3aed","btn":"Visit & Get 20 Tk"},
                {"title":"Group Join","reward":20,"link":"https://t.me","color":"#0f766e","btn":"Join & Get 20 Tk"},
                {"title":"Post Like","reward":20,"link":"https://facebook.com","color":"#be123c","btn":"Like & Get 20 Tk"}
            ]
        }
    }
    if not os.path.exists(DB_FILE): return default
    try:
        if os.path.getsize(DB_FILE)==0: return default
        with open(DB_FILE,'r',encoding='utf-8') as f:
            c=f.read().strip()
            if not c: return default
            j=json.loads(c)
            # ensure keys
            for k in default["s"]:
                if k not in j["s"]: j["s"][k]=default["s"][k]
            return j
    except:
        try: os.remove(DB_FILE)
        except: pass
        return default

def save_db(d):
    tmp=DB_FILE+".tmp"
    with open(tmp,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)
    os.replace(tmp,DB_FILE)

def get_user(db,uid):
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"bal":60,"ads":0,"uname":f"User {uid[-4:]}","upic":"","tasks":{},"banned":False,"last_ads_reset":str(datetime.now().date())}
    u=db["users"][uid]
    if u.get("last_ads_reset")!=str(datetime.now().date()):
        u["ads"]=0; u["last_ads_reset"]=str(datetime.now().date())
    return u

@app.route('/')
def home(): return render_template_string(USER_PAGE)
@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID: return "Admin Only"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/bal')
def api_bal():
    uid=request.args.get('id',ADMIN_ID); db=load_db()
    if uid in db["users"] and db["users"][uid].get("banned"): return jsonify({"banned":True,"msg":"You are Banned"})
    u=get_user(db,uid); save_db(db)
    return jsonify({"bal":u["bal"],"ads":u["ads"],"id":uid,"uname":u.get("uname"),"upic":u.get("upic"),"tasks":u.get("tasks",{}),"w":db["w"][-20:][::-1],"s":db["s"],"total_users":len(db["users"]),"total_withdraw":sum([x["amt"] for x in db["w"]])})

@app.route('/api/add')
def api_add():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid)
    if u.get("banned"): return jsonify({"ok":False,"msg":"Banned"})
    limit=db["s"].get("ads_limit",100); reward=db["s"].get("ads_reward",2)
    if u["ads"]>=limit: return jsonify({"ok":False,"msg":f"আজকের {limit} টা Ads শেষ"})
    u["bal"]+=reward; u["ads"]+=1; save_db(db); return jsonify({"ok":True,"bal":u["bal"]})

@app.route('/api/claim_task')
def api_claim_task():
    uid=request.args.get('id',ADMIN_ID); tid=request.args.get('tid','0'); db=load_db(); u=get_user(db,uid)
    tasks=db["s"]["tasks"]; reward=tasks[int(tid)]["reward"] if int(tid)<len(tasks) else 20
    last=u.get("tasks",{}).get(tid)
    if last:
        diff=datetime.now()-datetime.fromisoformat(last)
        if diff < timedelta(hours=24): return jsonify({"ok":False,"msg":f"২৪ ঘন্টা পর - {int(24-diff.total_seconds()/3600)} ঘন্টা বাকি"})
    if "tasks" not in u: u["tasks"]={}
    u["tasks"][tid]=datetime.now().isoformat(); u["bal"]+=reward; save_db(db)
    return jsonify({"ok":True,"bal":u["bal"],"msg":f"৳{reward} Added ✅"})

@app.route('/api/wd')
def api_wd():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); amt=int(request.args.get('amt',0))
    if u["bal"]<amt or amt<1000: return jsonify({"msg":"Min ৳1000"})
    u["bal"]-=amt; db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"met":request.args.get('met','bKash'),"time":str(datetime.now())[:16],"status":"pending"})
    save_db(db); return jsonify({"msg":"Withdraw Request Success - Pending"})

# ADMIN APIS
@app.route('/api/admin/users')
def admin_users(): db=load_db(); return jsonify(list(db["users"].values())[-200:][::-1])

@app.route('/api/admin/edit_bal')
def edit_bal():
    uid=request.args.get('uid'); amt=int(request.args.get('amt',0)); db=load_db()
    if uid in db["users"]: db["users"][uid]["bal"]+=amt; save_db(db); return jsonify({"msg":f"Balance {amt} Added"})
    return jsonify({"msg":"User Not Found"})

@app.route('/api/admin/ban')
def ban_user():
    uid=request.args.get('uid'); db=load_db()
    if uid in db["users"]: db["users"][uid]["banned"]=not db["users"][uid].get("banned",False); save_db(db); return jsonify({"msg":"Toggled"})
    return jsonify({"msg":"Not Found"})

@app.route('/api/admin/wd_action')
def wd_action():
    idx=int(request.args.get('idx',-1)); act=request.args.get('act','approve'); db=load_db()
    if 0<=idx<len(db["w"]): db["w"][idx]["status"]=act; save_db(db); return jsonify({"msg":act})
    return jsonify({"msg":"Not Found"})

@app.route('/api/save',methods=['POST'])
def api_save(): db=load_db(); data=request.json
    # tasks update special
    if "tasks" in data: db["s"]["tasks"]=data["tasks"]
    else: db["s"].update(data)
    save_db(db); return jsonify({"msg":"Saved"})

@app.route('/api/update_profile',methods=['POST'])
def api_upd():
    j=request.json; uid=j.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid)
    if j.get('uname'): u["uname"]=j.get('uname')
    if j.get('upic'): u["upic"]=j.get('upic')
    save_db(db); return jsonify({"msg":"Updated"})

USER_PAGE = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#081028;color:#fff;max-width:430px;margin:0 auto;padding-bottom:95px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:18px;font-weight:800}
.hdr-pic{width:46px;height:46px;border-radius:50%;border:3px solid #2ef36c;object-fit:cover}
.bal{font-size:52px;font-weight:900;color:#2ef36c;margin-top:8px}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.dot{width:10px;height:10px;background:#2ef36c;border-radius:50%;animation:blk 0.8s infinite}
@keyframes blk{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:18px;height:185px;position:relative;overflow:hidden}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0 6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #2a3a5f;background:#0b142d;color:#fff;margin-top:10px}
.meth{display:flex;gap:8px;margin-top:12px}
.meth div{flex:1;background:#0b142d;border:2px solid #2a3a5f;border-radius:12px;padding:12px;text-align:center;cursor:pointer}
.meth div.on{border-color:#ff2d7a;background:#1a1430}
</style></head><body>
<div id="p-home"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName">👑</div><img id="hdrPic" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span class="adsV">0</span>/<span class="limitV">100</span></div></div><div class="notice"><div><div style="font-weight:900" id="noticeT">অফিসিয়াল নোটিস</div><div style="font-size:12px;opacity:0.8" id="noticeS">প্রতিদিন Ads দেখুন</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:10px 18px;border-radius:30px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div><div class="slider" id="sl"></div><div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" id="adsBtn" onclick="watchAds()">ADS দেখুন</button></div><div id="tasksHome"></div></div>
<div id="p-tasks" style="display:none"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName2">👑</div><img id="hdrPic2" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div></div><div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার</div><button class="btn" style="background:#0ea5e9;margin-top:12px" id="adsBtn2" onclick="watchAds()">ADS দেখুন</button></div><div id="tasksAll"></div></div>
<div id="p-refer" style="display:none"><div class="hdr"><div>রেফার করুন</div><div class="bal">৳ <span class="balV">60</span></div></div><div class="card"><div style="font-weight:900">Refer & Earn <span id="refBonusV">৳20</span></div><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyR()">Copy Link</button></div></div>
<div id="p-wallet" style="display:none"><div class="hdr"><div>আমার ওয়ালেট</div><div class="bal">৳ <span class="balV">60</span></div></div><div class="card"><div style="font-size:38px;font-weight:900;color:#2ef36c">৳ <span class="balV">60</span></div></div><div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')">bKash</div><div id="m-nagad" onclick="sel('Nagad')">Nagad</div></div><input class="inp" id="wNum" placeholder="Number"><button class="btn" style="background:#2563eb;margin-top:12px" onclick="wd()">Withdraw করুন</button></div><div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c">🟢 Live Withdraw</div><div id="liveList"></div></div></div>
<div id="p-profile" style="display:none"><div class="hdr" style="text-align:center"><img id="userPic" style="width:90px;height:90px;border-radius:50%;border:4px solid #2ef36c;object-fit:cover" src=""><div style="font-weight:900;font-size:18px;margin-top:10px" id="userName">User</div><div style="opacity:0.7;font-size:13px">ID: <span id="pid">----</span> - Verified ✅</div><div class="bal" style="text-align:center">৳ <span class="balV">60</span></div></div><div class="card" style="border:2px solid #22c55e"><div style="font-weight:900">✏️ প্রোফাইল পরিবর্তন</div><input class="inp" id="editName" placeholder="আপনার নাম"><input class="inp" id="editPic" placeholder="ছবির Link"><button class="btn" style="background:#22c55e;color:#000;margin-top:12px" onclick="saveProfile()">💾 Save Profile</button></div><div class="card" style="border:2px solid #f59e0b"><div style="font-weight:900;color:#fbbf24">📢 Admin Notice</div><div id="adminBoxText"></div></div></div>
<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385'; let method='bKash'; let tasks=[];
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Copied'));}
function watchAds(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(r=>r.json()).then(j=>{if(!j.ok){alert(j.msg);return;}load();});});}else{fetch('/api/add?id='+uid).then(r=>r.json()).then(j=>{if(!j.ok){alert(j.msg);return;}load();});}}
function doTask(i){window.open(tasks[i].link,'_blank'); setTimeout(()=>{if(confirm('Join/Follow Complete করেছেন?')){fetch('/api/claim_task?id='+uid+'&tid='+i).then(r=>r.json()).then(j=>{alert(j.msg);load();});}},3000);}
function wd(){let a=document.getElementById('wAmt').value,n=document.getElementById('wNum').value;if(!a||!n){alert('Amount & Number');return;}fetch('/api/wd?id='+uid+'&amt='+a+'&num='+n+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function saveProfile(){let nm=document.getElementById('editName').value,pic=document.getElementById('editPic').value;fetch('/api/update_profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,uname:nm,upic:pic})}).then(()=>{alert('Updated ✅');load();});}
let slIdx=0;setInterval(()=>{let imgs=document.querySelectorAll('#sl img');if(imgs.length==0)return;imgs.forEach(im=>im.classList.remove('on'));slIdx=(slIdx+1)%imgs.length;imgs[slIdx].classList.add('on');},3000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{if(d.banned){document.body.innerHTML='<center><h2 style=margin-top:100px;color:red>⛔ You Are Banned</h2></center>';return;}document.querySelectorAll('.balV').forEach(e=>e.innerText=d.bal);document.querySelectorAll('.adsV').forEach(e=>e.innerText=d.ads);document.querySelectorAll('.limitV').forEach(e=>e.innerText=d.s.ads_limit||100);document.getElementById('pid').innerText=d.id.slice(0,4)+'****'+d.id.slice(-2);document.getElementById('refLink').value=location.origin+'/?ref='+d.id;document.getElementById('userName').innerText=d.uname||'User';document.getElementById('userPic').src=d.upic||'https://i.pravatar.cc/150?img=8';document.getElementById('adminBoxText').innerText=d.s.profile_box||'';document.getElementById('noticeT').innerText=d.s.notice_title||'অফিসিয়াল নোটিস';document.getElementById('noticeS').innerText=d.s.notice_sub||'';document.getElementById('refBonusV').innerText='৳'+(d.s.refer_bonus||20);document.getElementById('adsBtn').innerText='ADS দেখুন - ৳'+(d.s.ads_reward||2)+' বোনাস';document.getElementById('adsBtn2').innerText='ADS দেখুন - ৳'+(d.s.ads_reward||2)+' বোনাস';let an=d.s.admin_name||'প্রতিদিনের কাজ BD';let ap=d.s.admin_pic||'https://i.pravatar.cc/150?img=32';let dec='👑 '+an+' ✅';document.getElementById('hdrName').innerText=dec;document.getElementById('hdrName2').innerText=dec;document.getElementById('hdrPic').src=ap;document.getElementById('hdrPic2').src=ap;let sl=document.getElementById('sl');sl.innerHTML='';(d.s.slider||[]).forEach((src,i)=>{sl.innerHTML+=`<img class="${i==0?'on':''}" src="${src}">`;});let live='';if(d.w.length==0)live='এখনো কেউ Withdraw করেনি';else d.w.forEach(w=>{live+=`<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">💸 ${w.id.slice(-4)} - ৳${w.amt} - ${w.status}</div>`;});document.getElementById('liveList').innerHTML=live;tasks=d.s.tasks||[];renderTasks(d.tasks||{});});}
function renderTasks(doneTasks){let h='';tasks.forEach((t,i)=>{let isDone=doneTasks[i]!==undefined;let btnText=isDone?'DONE ✅ - 24h পরে আবার':t.btn;let btnColor=isDone?'#475569':t.color;let dis=isDone?'disabled':'';h+=`<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div>৳${t.reward}</div></div><button class="btn" style="background:${btnColor};margin-top:10px" ${dis} onclick="doTask(${i})">${btnText}</button></div>`;});document.getElementById('tasksHome').innerHTML=h;document.getElementById('tasksAll').innerHTML=h;}
load();
</script></body></html>
"""
ADMIN_PAGE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{background:#081028;color:#fff;font-family:sans-serif;padding:10px;max-width:500px;margin:0 auto;padding-bottom:100px}
.card{background:#132042;border:1px solid #1e2d4f;border-radius:16px;padding:14px;margin:10px 0}
.label{color:#38bdf8;font-size:12px;margin:8px 0 4px 0}
.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:10px;padding:12px;width:100%;color:#fff;margin-bottom:6px}
.btn{padding:10px 14px;border:0;border-radius:10px;font-weight:800;color:#fff;cursor:pointer;margin:2px}
.btn-save{width:100%;max-width:480px;position:fixed;bottom:10px;left:50%;transform:translateX(-50%);padding:16px;background:linear-gradient(90deg,#22c55e,#16a34a);border:0;border-radius:14px;font-weight:900;color:#fff;z-index:99}
.tab{display:flex;gap:6px;overflow:auto;margin:10px 0}
.tab div{padding:10px 14px;background:#132042;border-radius:10px;cursor:pointer;white-space:nowrap;border:1px solid #1e2d4f}
.tab div.on{background:#22c55e;color:#000;font-weight:900}
</style></head><body>
<h2 style="text-align:center;color:#22c55e">👑 SUPER ADMIN A-Z</h2>
<div class="tab"><div class="on" id="t-dash" onclick="tab('dash')">Dashboard</div><div id="t-users" onclick="tab('users')">Users</div><div id="t-wd" onclick="tab('wd')">Withdraw</div><div id="t-tasks" onclick="tab('tasks')">Tasks</div><div id="t-set" onclick="tab('set')">Settings</div></div>

<div id="p-dash">
<div class="card" style="border:2px solid #22c55e"><div style="font-weight:900">📊 Dashboard</div><div id="dashInfo"></div></div>
<div class="card"><div style="font-weight:900">👑 Header Control</div><div class="label">Header নাম</div><input class="input" id="admin_name"><div class="label">Header ছবি Link</div><input class="input" id="admin_pic"></div>
<div class="card"><div style="font-weight:900">📢 Notice + Profile Box</div><div class="label">Notice Title</div><input class="input" id="notice_title"><div class="label">Notice Sub</div><input class="input" id="notice_sub"><div class="label">Profile Bottom Box</div><textarea class="input" id="profile_box" rows="3"></textarea></div>
</div>

<div id="p-users" style="display:none">
<div class="card"><div style="font-weight:900">👥 Users Control</div><input class="input" id="searchUid" placeholder="User ID দিয়ে Search - 880717..."><button class="btn" style="background:#0ea5e9" onclick="searchUser()">Search</button><div id="userList" style="max-height:500px;overflow:auto;margin-top:10px"></div></div>
</div>

<div id="p-wd" style="display:none">
<div class="card"><div style="font-weight:900">💸 Withdraw Control - Approve / Reject</div><div id="wdList"></div></div>
</div>

<div id="p-tasks" style="display:none">
<div class="card" style="border:2px solid #f59e0b"><div style="font-weight:900">✅ Tasks Control - 6 টা Task</div><div id="tasksEdit"></div></div>
</div>

<div id="p-set" style="display:none">
<div class="card" style="border:2px solid #0ea5e9"><div style="font-weight:900">⚙️ Money & Slider Control</div>
<div class="label">Ads Reward - প্রতি Ads এ কত টাকা (৳2)</div><input class="input" id="ads_reward" type="number">
<div class="label">Ads Daily Limit - দিনে কয়টা</div><input class="input" id="ads_limit" type="number">
<div class="label">Refer Bonus - প্রতি Refer এ কত</div><input class="input" id="refer_bonus" type="number">
<div class="label">Slider Image 1 Link</div><input class="input" id="sl1">
<div class="label">Slider Image 2 Link</div><input class="input" id="sl2">
<div class="label">Slider Image 3 Link</div><input class="input" id="sl3">
</div>
</div>

<div style="height:80px"></div>
<button class="btn-save" onclick="saveAll()">💾 SAVE ALL SETTINGS</button>
<script>
let allUsers=[]; let currentSettings={};
function tab(t){['dash','users','wd','tasks','set'].forEach(x=>{document.getElementById('p-'+x).style.display=x==t?'block':'none';document.getElementById('t-'+x).classList.toggle('on',x==t);});}
function load(){fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{currentSettings=d.s;document.getElementById('dashInfo').innerHTML=`Total Users: <b style=color:#2ef36c>${d.total_users}</b><br>Total Withdraw: <b style=color:#fbbf24>৳${d.total_withdraw}</b><br>Token: 11764581 Hidden ✅<br>Live: <span style=color:#2ef36c>● মিটমিট করছে</span>`;document.getElementById('admin_name').value=d.s.admin_name||'';document.getElementById('admin_pic').value=d.s.admin_pic||'';document.getElementById('profile_box').value=d.s.profile_box||'';document.getElementById('notice_title').value=d.s.notice_title||'';document.getElementById('notice_sub').value=d.s.notice_sub||'';document.getElementById('ads_reward').value=d.s.ads_reward||2;document.getElementById('ads_limit').value=d.s.ads_limit||100;document.getElementById('refer_bonus').value=d.s.refer_bonus||20;if(d.s.slider){document.getElementById('sl1').value=d.s.slider[0]||'';document.getElementById('sl2').value=d.s.slider[1]||'';document.getElementById('sl3').value=d.s.slider[2]||'';}let h='';(d.s.tasks||[]).forEach((t,i)=>{h+=`<div style=border:1px solid #2a3a5f;border-radius:10px;padding:10px;margin:8px 0><div class=label>Task ${i+1} Title</div><input class=input id=t_title_${i} value="${t.title}"><div class=label>Reward ৳</div><input class=input id=t_reward_${i} type=number value="${t.reward}"><div class=label>Link</div><input class=input id=t_link_${i} value="${t.link}"><div class=label>Button Text</div><input class=input id=t_btn_${i} value="${t.btn}"></div>`;});document.getElementById('tasksEdit').innerHTML=h;let wl='';d.w.forEach((w,idx)=>{wl+=`<div style=padding:8px;border-bottom:1px solid #222;display:flex;justify-content:space-between;align-items:center><div>ID:${w.id}<br>৳${w.amt} - ${w.met} - ${w.num}<br><small>${w.time} - ${w.status}</small></div><div><button class=btn style=background:#22c55e onclick=wdAct(${idx},'approved')>✓</button><button class=btn style=background:#ef4444 onclick=wdAct(${idx},'rejected')>✕</button></div></div>`;});document.getElementById('wdList').innerHTML=wl||'No Withdraw';});fetch('/api/admin/users').then(r=>r.json()).then(u=>{allUsers=u;renderUsers(u);});}
function renderUsers(list){let h='';list.slice(0,100).forEach(u=>{h+=`<div style=padding:8px;border-bottom:1px solid #1e2d4f><b>${u.uname}</b> - ${u.id} - ৳${u.bal} - Ads:${u.ads} ${u.banned?'<span style=color:red>[BANNED]</span>':''}<br><button class=btn style=background:#22c55e onclick=editBal('${u.id}',100)>+100</button><button class=btn style=background:#ef4444 onclick=editBal('${u.id}',-50)>-50</button><button class=btn style=background:#f59e0b onclick=banUser('${u.id}')>${u.banned?'Unban':'Ban'}</button></div>`;});document.getElementById('userList').innerHTML=h;}
function searchUser(){let q=document.getElementById('searchUid').value;if(!q){renderUsers(allUsers);return;}let f=allUsers.filter(u=>u.id.includes(q));renderUsers(f);}
function editBal(uid,amt){fetch(`/api/admin/edit_bal?uid=${uid}&amt=${amt}`).then(r=>r.json()).then(j=>{alert(j.msg);load();});}
function banUser(uid){fetch(`/api/admin/ban?uid=${uid}`).then(r=>r.json()).then(j=>{alert('Done');load();});}
function wdAct(idx,act){fetch(`/api/admin/wd_action?idx=${idx}&act=${act}`).then(r=>r.json()).then(j=>{alert(act);load();});}
function saveAll(){
 let tasks=[];
 for(let i=0;i<6;i++){let ti=document.getElementById(`t_title_${i}`);if(!ti)continue;tasks.push({title:document.getElementById(`t_title_${i}`).value,reward:parseInt(document.getElementById(`t_reward_${i}`).value)||20,link:document.getElementById(`t_link_${i}`).value,color:currentSettings.tasks[i].color,btn:document.getElementById(`t_btn_${i}`).value});}
 let data={
  admin_name:document.getElementById('admin_name').value,
  admin_pic:document.getElementById('admin_pic').value,
  profile_box:document.getElementById('profile_box').value,
  notice_title:document.getElementById('notice_title').value,
  notice_sub:document.getElementById('notice_sub').value,
  ads_reward:parseInt(document.getElementById('ads_reward').value)||2,
  ads_limit:parseInt(document.getElementById('ads_limit').value)||100,
  refer_bonus:parseInt(document.getElementById('refer_bonus').value)||20,
  slider:[document.getElementById('sl1').value,document.getElementById('sl2').value,document.getElementById('sl3').value],
  tasks:tasks
 };
 fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>{alert('✅ All Saved - Live হয়ে গেছে');load();});
}
load();
</script></body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
