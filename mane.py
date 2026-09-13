# CLEAN FINAL - BIG ADMIN 8807178385 - TESTED - NO ELOMELO
import os, json, time
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
BIG_ADMIN = "8807178385"

def default_db():
    return {
        "users": {},
        "withdraws": [],
        "settings": {
            "top_text": "Search or edit profile header...",
            "pro_title": "PRO MEMBER BONUS LIVE NOW",
            "pro_sub": "LIVE NOW",
            "pro_desc": "Unlock 20% extra - MITMIT GREEN",
            "pro_bonus": 50,
            "welcome": 60,
            "ad_reward": 2,
            "min_withdraw": 1000,
            "cooldown": 1,
            "refer_bonus": 20,
            "admin_pic": "https://i.pravatar.cc/150?img=68",
            "admin_name": "BIG ADMIN 8807178385",
            "user_line": "LIVE USERS - MITMIT - 8807178385",
            "ads": [
                {"title": "My Company Offer 50% OFF", "img": "https://picsum.photos/600/300?1", "link": "https://t.me", "btn": "Shop Now"},
                {"title": "New Product Launch", "img": "https://picsum.photos/600/300?2", "link": "https://facebook.com", "btn": "Visit Now"}
            ]
        },
        "tasks": [
            {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "Join & Get 25 Tk"},
            {"title": "Telegram Join", "reward": 10, "link": "https://t.me", "color": "#2563eb", "btn": "Join & Get 10 Tk"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d = default_db(); save_db(d); return d
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(f, d, indent=2, ensure_ascii=False)

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid, "name": "BIG ADMIN" if uid==BIG_ADMIN else f"User {uid[-4:]}",
            "real": db["settings"]["admin_name"], "pic": "", "balance": db["settings"]["welcome"],
            "times": {}, "earn": db["settings"]["welcome"], "pro_date": "", "join": str(datetime.now())[:19],
            "ref_by": "", "ref_count": 0, "ref_earn": 0, "withdraw_total": 0
        }
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(USER_PAGE)

@app.route('/admin')
def admin():
    if request.args.get('id')!= BIG_ADMIN: return f"Admin only?id={BIG_ADMIN}"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/data')
def data():
    uid = request.args.get('id', BIG_ADMIN); ref = request.args.get('ref')
    db = load_db(); new = str(uid) not in db["users"]; u = get_user(db, uid)
    if new and ref and ref!=uid and ref in db["users"]:
        u["ref_by"] = ref; r = db["users"][ref]; r["ref_count"]+=1; r["ref_earn"]+=db["settings"]["refer_bonus"]; r["balance"]+=db["settings"]["refer_bonus"]
    save_db(db)
    return jsonify({
        "user": u, "settings": db["settings"], "tasks": db["tasks"],
        "total_users": len(db["users"]), "total_withdraw": sum([x["amount"] for x in db["withdraws"]]),
        "withdraws": db["withdraws"][-10:][::-1], "users_list": list(db["users"].values())[-10:][::-1],
        "top_ref": sorted(db["users"].values(), key=lambda x: x["ref_count"], reverse=True)[:10]
    })

@app.route('/api/reward')
def reward():
    db=load_db(); u=get_user(db, request.args.get('id')); u["balance"]+=db["settings"]["ad_reward"]; save_db(db); return jsonify({"ok": True})

@app.route('/api/pro')
def pro():
    db=load_db(); u=get_user(db, request.args.get('id')); today=str(datetime.now().date())
    if u["pro_date"]==today: return jsonify({"msg": "আজ নেওয়া হয়েছে"})
    u["balance"]+=db["settings"]["pro_bonus"]; u["pro_date"]=today; save_db(db); return jsonify({"msg": f"🎁 {db['settings']['pro_bonus']} Tk Added"})

@app.route('/api/task')
def task():
    db=load_db(); i=int(request.args.get('i')); uid=request.args.get('id'); u=get_user(db, uid)
    last=float(u["times"].get(str(i),0)); cd=db["settings"]["cooldown"]*3600
    if last and (time.time()-last)<cd: return jsonify({"msg": "Wait"})
    u["times"][str(i)]=time.time(); u["balance"]+=db["tasks"][i]["reward"]; save_db(db); return jsonify({"msg": "Added"})

@app.route('/api/withdraw')
def withdraw():
    db=load_db(); uid=request.args.get('id'); amt=int(request.args.get('amount',0)); num=request.args.get('number'); method=request.args.get('method','bKash')
    u=get_user(db, uid)
    if amt<db["settings"]["min_withdraw"]: return jsonify({"msg": "Min 1000"})
    if u["balance"]<amt: return jsonify({"msg": "Low Balance"})
    u["balance"]-=amt; u["withdraw_total"]+=amt; db["withdraws"].append({"uid":uid,"name":u["name"],"amount":amt,"number":num,"method":method,"time":str(datetime.now())[:19]}); save_db(db); return jsonify({"msg": "Withdraw Success"})

@app.route('/api/admin/all')
def admin_all(): return jsonify(load_db())

@app.route('/api/admin/save', methods=['POST'])
def admin_save():
    db=load_db(); j=request.json
    db["settings"].update(j.get("settings",{})); db["tasks"]=j.get("tasks",db["tasks"]); db["settings"]["ads"]=j.get("ads",db["settings"]["ads"]); save_db(db); return jsonify({"msg":"Saved"})

@app.route('/api/admin/user_search')
def user_search():
    db=load_db(); u=db["users"].get(str(request.args.get('id'))); return jsonify({"found": bool(u), "user": u})

@app.route('/api/admin/user_update', methods=['POST'])
def user_update():
    db=load_db(); j=request.json; u=db["users"].get(str(j["id"]))
    if not u: return jsonify({"msg":"No User"})
    u["name"]=j.get("name",u["name"]); u["real"]=j.get("real",u["real"]); u["balance"]=int(j.get("balance",u["balance"])); u["pic"]=j.get("pic",u["pic"]); save_db(db); return jsonify({"msg":"Updated"})

USER_PAGE = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#070e1f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}
.top{background:#0f1b33;margin:12px;border-radius:20px;padding:12px;display:flex;gap:10px;border:1px solid #1e3a5f}.top input{flex:1;background:0;border:0;color:#fff;outline:0}
.pro{background:linear-gradient(135deg,#0f3a5f,#0a2a4a);margin:12px;border-radius:16px;padding:14px;display:flex;justify-content:space-between;border:1px solid #1e5a8a}
.line{background:#0f172a;margin:12px;border-radius:12px;padding:12px;border:1px solid #22c55e;display:flex;justify-content:space-between}
.card{background:#162032;margin:12px;border-radius:16px;padding:14px;border:1px solid #22314a}
.btn{width:100%;padding:12px;border:0;border-radius:12px;font-weight:800;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0a1222;display:flex;border-top:1px solid #22314a;padding:6px 0}.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}.btm div.on{color:#22c55e}.btm span{font-size:22px;display:block}
.ad{margin:12px;border-radius:16px;overflow:hidden;border:2px solid #22c55e;position:relative}.ad img{width:100%;height:150px;object-fit:cover}.ad.ov{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,black);padding:10px}
.meth{display:flex;gap:8px;margin-top:10px}.meth div{flex:1;background:#0f172a;border:2px solid #334155;border-radius:12px;padding:10px;text-align:center;cursor:pointer}.meth div.on{border-color:#22c55e}
.inp{width:100%;padding:11px;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}
</style></head><body>
<div class="top"><span onclick="go('more')">☰</span><input id="topText" readonly><span>✏️</span></div>
<div class="pro" onclick="proBonus()"><div><b id="proTitle"></b> <span style="color:#4ade80" id="proSub"></span><div style="font-size:11px;opacity:.7" id="proDesc"></div></div><div>🎁</div></div>

<div id="home">
<div class="line"><div><b style="color:#4ade80" id="lineText"></b><div style="font-size:11px"><span id="tUsers">0</span> Users • ID: <span id="myId"></span><br>Refer: <span id="myRef">0</span> জন • ৳<span id="myRefEarn">0</span></div></div><div style="text-align:right"><b style="color:#22c55e">৳<span id="tWithdraw">0</span></b><div style="font-size:10px"><span id="tWCount">0</span> Withdraw<br>You: ৳<span id="myW">0</span></div></div></div>
<div class="card"><div style="font-size:11px;opacity:.6">TOTAL BALANCE</div><div style="font-size:26px;font-weight:900;color:#4ade80">৳ <span id="bal">0</span></div></div>
<div id="adsTop"></div>
<div class="card" style="border-color:#22c55e"><div style="display:flex;gap:8px;align-items:center"><div style="width:8px;height:8px;background:#22c55e;border-radius:50%"></div><b style="color:#4ade80">LIVE WITHDRAW - MITMIT GREEN</b></div><div style="margin-top:6px">up to ৳10,000 - ID 8807178385</div><button class="btn" style="background:#86efac;color:#000;width:auto;margin-top:8px;padding:6px 14px;border-radius:20px" onclick="go('wallet')">Withdraw Now →</button></div>
<div class="card"><button class="btn" style="background:#0ea5e9" onclick="watchAd()" id="adBtn">Watch ADS</button><div id="tasks"></div></div>
<div class="card"><b>👥 Live Users</b><div id="usersLive"></div></div>
<div class="card"><b>💸 Live Withdraw</b><div id="withdrawLive"></div></div>
</div>

<div id="wallet" style="display:none">
<div class="card"><b>Wallet - ID <span id="wId"></span></b><div style="font-size:30px;font-weight:900;color:#22c55e">৳ <span id="wBal">0</span></div><div style="font-size:11px">Min ৳<span id="minW"></span></div></div>
<div class="card" style="border-color:#22c55e"><b>Select Method</b><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')"><div style="background:#e2136e;border-radius:8px;padding:12px;color:#fff;font-weight:900">bKash</div><div style="margin-top:6px">bKash</div></div><div id="m-nagad" onclick="sel('Nagad')"><div style="background:#f97316;border-radius:8px;padding:12px;color:#fff;font-weight:900">Nagad</div><div style="margin-top:6px">Nagad</div></div><div id="m-rocket" onclick="sel('Rocket')"><div style="background:#7c3aed;border-radius:8px;padding:12px;color:#fff;font-weight:900">Rocket</div><div style="margin-top:6px">Rocket</div></div></div>
<input class="inp" id="wAmt" placeholder="Amount" type="number"><input class="inp" id="wNum" placeholder="Number"><button class="btn" style="background:#22c55e;margin-top:10px" onclick="doW()">Withdraw - <span id="selT">bKash</span></button></div>
<div id="adsWallet"></div>
</div>

<div id="tasksP" style="display:none"><div class="card"><div id="tasksAll"></div></div></div>
<div id="history" style="display:none"><div class="card"><b>Refer - <span id="refBonus"></span> Tk</b><div class="inp" id="refLink" style="word-break:break-all"></div><button class="btn" style="background:#2563eb;margin-top:10px" onclick="navigator.clipboard.writeText(document.getElementById('refLink').innerText).then(()=>alert('Copied'))">Copy Link</button><div style="margin-top:10px;font-size:13px">Refer: <span id="rCount">0</span> জন - Earn: ৳<span id="rEarn">0</span> - Withdraw: ৳<span id="rW">0</span><br>ID: <span id="rId"></span> - By: <span id="rBy"></span></div></div></div>
<div id="more" style="display:none"><div class="card"><div id="moreInfo"></div></div></div>

<div class="btm"><div class="on" id="b-home" onclick="go('home')"> <span>🏠</span>Home</div><div id="b-tasksP" onclick="go('tasksP')"><span>📋</span>Tasks</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-history" onclick="go('history')"><span>📊</span>History</div><div id="b-more" onclick="go('more')"><span>⚙️</span>More</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let method='bKash';
function go(p){['home','wallet','tasksP','history','more'].forEach(x=>{let e=document.getElementById(x);if(e)e.style.display=x==p?'block':'none';let b=document.getElementById('b-'+x);if(b)b.classList.toggle('on',x==p);});}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');document.getElementById('selT').innerText=m;}
function proBonus(){fetch('/api/pro?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function watchAd(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(()=>load());});}else{fetch('/api/reward?id='+uid).then(()=>load());}}
function doW(){let a=document.getElementById('wAmt').value;let n=document.getElementById('wNum').value;fetch(`/api/withdraw?id=${uid}&amount=${a}&number=${n}&method=${method}`).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function claim(i){let db={};fetch('/api/data?id='+uid).then(r=>r.json()).then(d=>{window.open(d.tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/task?id='+uid+'&i='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});},2000);});}
function load(){let ref=new URLSearchParams(location.search).get('ref')||'';fetch('/api/data?id='+uid+'&ref='+ref).then(r=>r.json()).then(d=>{
document.getElementById('topText').value=d.settings.top_text;document.getElementById('proTitle').innerText=d.settings.pro_title;document.getElementById('proSub').innerText=d.settings.pro_sub;document.getElementById('proDesc').innerText=d.settings.pro_desc;document.getElementById('lineText').innerText=d.settings.user_line;
document.getElementById('tUsers').innerText=d.total_users;document.getElementById('tWithdraw').innerText=d.total_withdraw;document.getElementById('tWCount').innerText=d.withdraws.length;
document.getElementById('myId').innerText=d.user.id;document.getElementById('wId').innerText=d.user.id;document.getElementById('rId').innerText=d.user.id;document.getElementById('myRef').innerText=d.user.ref_count;document.getElementById('myRefEarn').innerText=d.user.ref_earn;document.getElementById('myW').innerText=d.user.withdraw_total;
document.getElementById('bal').innerText=d.user.balance;document.getElementById('wBal').innerText=d.user.balance;document.getElementById('minW').innerText=d.settings.min_withdraw;document.getElementById('adBtn').innerText='Watch ADS - ৳'+d.settings.ad_reward;
document.getElementById('refBonus').innerText=d.settings.refer_bonus;document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id;document.getElementById('rCount').innerText=d.user.ref_count;document.getElementById('rEarn').innerText=d.user.ref_earn;document.getElementById('rW').innerText=d.user.withdraw_total;document.getElementById('rBy').innerText=d.user.ref_by||'Direct';
document.getElementById('moreInfo').innerHTML=`ID: ${d.user.id}<br>Name: ${d.user.name}<br>Balance: ৳${d.user.balance}<br>Refer: ${d.user.ref_count} জন<br>Withdraw: ৳${d.user.withdraw_total}<br>Join: ${d.user.join}`;
let ads='';d.settings.ads.forEach(a=>{ads+=`<div class="ad" onclick="window.open('${a.link}','_blank')"><img src="${a.img}"><div class="ov"><b>${a.title}</b><br><button class="btn" style="background:#22c55e;width:auto;padding:4px 10px;margin-top:4px">${a.btn}</button></div></div>`;});
document.getElementById('adsTop').innerHTML=ads;document.getElementById('adsWallet').innerHTML=ads;
let tHtml='';d.tasks.forEach((t,i)=>{tHtml+=`<div class="card" style="margin:8px 0"><div style="display:flex;justify-content:space-between"><div>${t.title}</div><div style="color:#22c55e">৳${t.reward}</div></div><button class="btn" style="background:${t.color};margin-top:8px" onclick="claim(${i})">${t.btn}</button></div>`;});
document.getElementById('tasks').innerHTML=tHtml;document.getElementById('tasksAll').innerHTML=tHtml;
let uHtml='';d.users_list.forEach(u=>{uHtml+=`<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #22314a"><div>${u.name} • ID:${u.id.slice(-4)} • Ref:${u.ref_count}</div><div>৳${u.balance}</div></div>`;});document.getElementById('usersLive').innerHTML=uHtml;
let wHtml='';d.withdraws.forEach(w=>{wHtml+=`<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #22314a"><div>${w.name} • ${w.method} ${w.number}</div><div style="color:#22c55e">৳${w.amount}</div></div>`;});document.getElementById('withdrawLive').innerHTML=wHtml;
});}
load();
</script></body></html>"""

ADMIN_PAGE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#0f172a;color:#fff;padding:12px;max-width:800px;margin:0 auto;font-family:sans-serif}.card{background:#1e293b;padding:14px;border-radius:12px;margin:10px 0;border:1px solid #334155}input{width:100%;padding:10px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#fff;margin:5px 0}button{padding:10px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}label{font-size:11px;color:#38bdf8}.stat{display:flex;gap:8px}.stat div{flex:1;background:#0f172a;padding:10px;border-radius:10px;text-align:center;border:1px solid #22c55e}table{width:100%;font-size:12px;border-collapse:collapse}td,th{padding:6px;border-bottom:1px solid #334155}</style></head><body>
<h2 style="color:#22c55e">ADMIN CLEAN - 8807178385</h2>
<div class="stat"><div><div id="sUsers" style="font-size:20px;font-weight:900">0</div>Total Users</div><div><div id="sW" style="font-size:20px;font-weight:900">0</div>Withdraw</div><div><div id="sT" style="font-size:20px;font-weight:900">0</div>Total ৳</div><div><div id="sR" style="font-size:20px;font-weight:900">0</div>Refer</div></div>

<div class="card" style="border:2px solid #fbbf24"><h3>👑 User Edit - ID দিয়ে - Refer + Withdraw দেখবে</h3><input id="uid" value="8807178385" placeholder="ID লেখো"><button style="background:#f59e0b;width:100%" onclick="search()">Search - ID দিয়ে</button><div id="editBox" style="display:none;margin-top:10px"><input id="eName" placeholder="Name"><input id="eReal" placeholder="Real Name"><input id="eBal" type="number" placeholder="Balance"><input id="ePic" placeholder="Pic URL"><div id="eInfo" style="font-size:12px;margin-top:6px"></div><button style="background:#22c55e;width:100%;margin-top:8px" onclick="update()">Save Profile</button></div></div>

<div class="card"><h3>🏆 Refer - কে কতটা Refer করলো</h3><div id="refList"></div></div>
<div class="card"><h3>💸 Withdraw - কে কত টাকা</h3><div id="wList"></div></div>
<div class="card"><h3>👥 All Users - ID + Refer + Withdraw</h3><div id="allUsers"></div></div>

<div class="card"><h3>Settings - সব লেখা</h3><label>Top Text</label><input id="top_text"><label>PRO Title</label><input id="pro_title"><label>User Line</label><input id="user_line"><label>PRO Bonus</label><input id="pro_bonus" type="number"><label>Refer Bonus</label><input id="refer_bonus" type="number"><label>Min Withdraw</label><input id="min_withdraw" type="number"></div>

<div class="card"><h3>Company Ads - অনেক গুলো</h3><div id="adsEdit"></div><button style="background:#22c55e;width:100%" onclick="addAd()">+ Add Ad</button></div>

<div class="card"><h3>Tasks</h3><div id="tasksEdit"></div><button style="background:#22c55e;width:100%" onclick="addTask()">+ Add Task</button></div>

<div class="card" style="background:linear-gradient(90deg,#22c55e,#16a34a)"><button style="background:#fff;color:#16a34a;width:100%;padding:16px;font-weight:900" onclick="save()">💾 SAVE ALL - FINAL</button></div>

<script>let DB={};function load(){fetch('/api/admin/all?id=8807178385').then(r=>r.json()).then(d=>{DB=d;document.getElementById('sUsers').innerText=Object.keys(d.users).length;document.getElementById('sW').innerText=d.withdraws.length;document.getElementById('sT').innerText=d.withdraws.reduce((s,w)=>s+w.amount,0);document.getElementById('sR').innerText=Object.values(d.users).reduce((s,u)=>s+(u.ref_count||0),0);
for(let k in d.settings){let e=document.getElementById(k);if(e)e.value=d.settings[k];}
let refHtml='<table><tr><th>ID</th><th>Name</th><th>Refer</th><th>Earn</th><th>W</th></tr>';Object.values(d.users).sort((a,b)=>b.ref_count-a.ref_count).slice(0,20).forEach(u=>{refHtml+=`<tr><td>${u.id}</td><td>${u.name}</td><td style="color:#22c55e">${u.ref_count} জন</td><td>৳${u.ref_earn}</td><td>৳${u.withdraw_total}</td></tr>`;});refHtml+='</table>';document.getElementById('refList').innerHTML=refHtml;
let wHtml='';d.withdraws.slice(-15).reverse().forEach(w=>{wHtml+=`<div style="padding:6px;border-bottom:1px solid #334155">ID:${w.uid} ${w.name} - ${w.method} ${w.number} - ৳${w.amount} - ${w.time}</div>`;});document.getElementById('wList').innerHTML=wHtml;
let all='<table><tr><th>ID</th><th>Name</th><th>Bal</th><th>Ref</th><th>W</th><th>By</th></tr>';Object.values(d.users).forEach(u=>{all+=`<tr><td>${u.id}</td><td>${u.name}</td><td>৳${u.balance}</td><td>${u.ref_count}</td><td>৳${u.withdraw_total}</td><td>${u.ref_by||'Direct'}</td></tr>`;});all+='</table>';document.getElementById('allUsers').innerHTML=all;
let aHtml='';d.settings.ads.forEach((a,i)=>{aHtml+=`<div style="background:#0f172a;padding:8px;border-radius:8px;margin:6px 0"><b>Ad ${i+1}</b> <button style="float:right;background:#dc2626;padding:4px" onclick="delAd(${i})">Del</button><input id="ad_t_${i}" value="${a.title}"><input id="ad_img_${i}" value="${a.img}"><input id="ad_link_${i}" value="${a.link}"><input id="ad_btn_${i}" value="${a.btn}"></div>`;});document.getElementById('adsEdit').innerHTML=aHtml;
let tHtml='';d.tasks.forEach((t,i)=>{tHtml+=`<div style="background:#0f172a;padding:8px;border-radius:8px;margin:6px 0"><input id="t_title_${i}" value="${t.title}"><input id="t_link_${i}" value="${t.link}"><input id="t_reward_${i}" type="number" value="${t.reward}"></div>`;});document.getElementById('tasksEdit').innerHTML=tHtml;
});}
function addAd(){DB.settings.ads.push({title:"New Offer",img:"https://picsum.photos/200/100",link:"https://t.me",btn:"Shop Now"});load();}
function delAd(i){DB.settings.ads.splice(i,1);saveTemp();}
function addTask(){DB.tasks.push({title:"New",link:"https://t.me",reward:20,color:"#2563eb",btn:"Join"});load();}
function search(){let id=document.getElementById('uid').value;fetch('/api/admin/user_search?id='+id).then(r=>r.json()).then(d=>{if(!d.found){alert('No User');return;}document.getElementById('editBox').style.display='block';document.getElementById('eName').value=d.user.name;document.getElementById('eReal').value=d.user.real;document.getElementById('eBal').value=d.user.balance;document.getElementById('ePic').value=d.user.pic;document.getElementById('eInfo').innerHTML=`Refer: ${d.user.ref_count} জন - Earn: ৳${d.user.ref_earn} - Withdraw: ৳${d.user.withdraw_total} - By: ${d.user.ref_by||'Direct'}`;});}
function update(){let data={id:document.getElementById('uid').value,name:document.getElementById('eName').value,real:document.getElementById('eReal').value,balance:document.getElementById('eBal').value,pic:document.getElementById('ePic').value};fetch('/api/admin/user_update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function saveTemp(){fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:DB.settings,tasks:DB.tasks,ads:DB.settings.ads})});}
function save(){let s={};['top_text','pro_title','user_line','pro_bonus','refer_bonus','min_withdraw'].forEach(k=>{let e=document.getElementById(k);if(e)s[k]=e.value;});let ads=[];for(let i=0;i<DB.settings.ads.length;i++){let t=document.getElementById('ad_t_'+i);if(!t)continue;ads.push({title:t.value,img:document.getElementById('ad_img_'+i).value,link:document.getElementById('ad_link_'+i).value,btn:document.getElementById('ad_btn_'+i).value});}let tasks=[];for(let i=0;i<DB.tasks.length;i++){let t=document.getElementById('t_title_'+i);if(!t)continue;tasks.push({title:t.value,link:document.getElementById('t_link_'+i).value,reward:parseInt(document.getElementById('t_reward_'+i).value),color:"#2563eb",btn:"Join"});}fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:{...s,ads:ads},tasks:tasks,ads:ads})}).then(r=>r.json()).then(()=>{alert('Saved - Clean Final');load();});}
load();
</script></body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
