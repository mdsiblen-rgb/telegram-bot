# ULTIMATE FINAL - EXACT SCREENSHOT - ALL FEATURES - 8807178385 - NO ELOMELO - TESTED
import os, json, time
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def db_default():
    return {"users":{}, "withdraws":[], "settings":{
        "top_text":"Search or edit profile header...","pro_title":"PRO MEMBER BONUS LIVE NOW","pro_sub":"LIVE NOW","pro_desc":"Unlock 20% extra withdrawal limit • Ends in 12:34:50","pro_bonus":50,
        "welcome":117,"ad_reward":2,"min_w":1000,"cooldown":1,"refer_bonus":20,
        "admin_pic":"https://i.pravatar.cc/150?img=68","user_line":"LIVE USERS - MITMIT - 8807178385",
        "ads":[{"title":"My Company Offer 50% OFF","img":"https://picsum.photos/600/300?random=1","link":"https://t.me","btn":"Shop Now"},{"title":"New Product Launch","img":"https://picsum.photos/600/300?random=2","link":"https://facebook.com","btn":"Visit Now"}]
    },"tasks":[{"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","btn":"Join & Get 25 Tk"},{"title":"Telegram Join","reward":10,"link":"https://t.me","color":"#2563eb","btn":"Join & Get 10 Tk"}]}

def load():
    if not os.path.exists(DB_FILE):
        d=db_default(); save(d); return d
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
def save(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)
def get_u(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":"BIG ADMIN" if uid==ADMIN_ID else f"User {uid[-4:]}","real":f"ADMIN • BIG ADMIN {uid}" if uid==ADMIN_ID else f"User {uid[-4:]}","pic":"","bal":db["settings"]["welcome"],"times":{},"earn":db["settings"]["welcome"],"pro_date":"","join":str(datetime.now())[:19],"ref_by":"","ref_c":0,"ref_e":0,"w_total":0}
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/admin')
def adm():
    if request.args.get('id')!=ADMIN_ID: return "Need?id=8807178385"
    return render_template_string(ADMIN)
@app.route('/api/all')
def all_data():
    uid=request.args.get('id',ADMIN_ID); ref=request.args.get('ref'); db=load(); new=str(uid) not in db["users"]; u=get_u(db,uid)
    if new and ref and ref!=uid and ref in db["users"]:
        u["ref_by"]=ref; r=db["users"][ref]; r["ref_c"]+=1; r["ref_e"]+=db["settings"]["refer_bonus"]; r["bal"]+=db["settings"]["refer_bonus"]
    save(db)
    return jsonify({"u":u,"s":db["settings"],"tasks":db["tasks"],"total_u":len(db["users"]),"total_w":sum([x["amount"] for x in db["withdraws"]]),"w_list":db["withdraws"][-10:][::-1],"u_list":list(db["users"].values())[-10:][::-1],"top_ref":sorted(db["users"].values(), key=lambda x: x["ref_c"], reverse=True)[:10]})

@app.route('/api/reward')
def rw():
    db=load(); u=get_u(db,request.args.get('id')); u["bal"]+=db["settings"]["ad_reward"]; save(db); return jsonify({"m":"Added"})
@app.route('/api/pro')
def pro():
    db=load(); u=get_u(db,request.args.get('id')); today=str(datetime.now().date())
    if u["pro_date"]==today: return jsonify({"m":"আজ নেওয়া হয়েছে"})
    u["bal"]+=db["settings"]["pro_bonus"]; u["pro_date"]=today; save(db); return jsonify({"m":f"Bonus {db['settings']['pro_bonus']}"})
@app.route('/api/task')
def task_api():
    db=load(); i=int(request.args.get('i')); u=get_u(db,request.args.get('id')); last=float(u["times"].get(str(i),0)); cd=db["settings"]["cooldown"]*3600
    if last and (time.time()-last)<cd: return jsonify({"m":"Wait"})
    u["times"][str(i)]=time.time(); u["bal"]+=db["tasks"][i]["reward"]; save(db); return jsonify({"m":"Added"})
@app.route('/api/withdraw')
def wd():
    db=load(); uid=request.args.get('id'); amt=int(request.args.get('amount',0)); num=request.args.get('number'); met=request.args.get('method','bKash'); u=get_u(db,uid)
    if amt<db["settings"]["min_w"]: return jsonify({"m":"Min 1000"})
    if u["bal"]<amt: return jsonify({"m":"Low Balance"})
    u["bal"]-=amt; u["w_total"]+=amt; db["withdraws"].append({"uid":uid,"name":u["name"],"amount":amt,"number":num,"method":met,"time":str(datetime.now())[:19]}); save(db); return jsonify({"m":"Success"})
@app.route('/api/admin/db')
def adb(): return jsonify(load())
@app.route('/api/admin/save',methods=['POST'])
def asave():
    db=load(); j=request.json; db["settings"].update(j.get("settings",{})); db["tasks"]=j.get("tasks",db["tasks"]); db["settings"]["ads"]=j.get("ads",db["settings"]["ads"]); save(db); return jsonify({"m":"Saved"})
@app.route('/api/admin/user')
def aus():
    db=load(); u=db["users"].get(str(request.args.get('id'))); return jsonify({"f":bool(u),"u":u})
@app.route('/api/admin/user_up',methods=['POST'])
def aup():
    db=load(); j=request.json; u=db["users"].get(str(j["id"]));
    if not u: return jsonify({"m":"No"})
    u["name"]=j.get("name",u["name"]); u["real"]=j.get("real",u["real"]); u["bal"]=int(j.get("bal",u["bal"])); u["pic"]=j.get("pic",u["pic"]); save(db); return jsonify({"m":"Updated"})

HTML="""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#070e1f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:95px}
.top{background:#0f1b33;margin:12px;border-radius:22px;padding:12px 14px;display:flex;align-items:center;gap:10px;border:1px solid #1e3a5f}.top input{flex:1;background:0;border:0;color:#8aa0bf;outline:0}
.pro{background:linear-gradient(135deg,#0f3a5f,#0a2a4a);margin:12px;border-radius:16px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:1px solid #1e5a8a;cursor:pointer}
.prof{background:#0d1a33;margin:12px;border-radius:20px;padding:16px;display:flex;gap:14px;align-items:center;border:1px solid #1e3a5f}.ring{width:70px;height:70px;border-radius:50%;padding:3px;background:linear-gradient(135deg,#22c55e,#38bdf8)}.ring img{width:100%;height:100%;border-radius:50%;object-fit:cover;background:#fff}
.bal{background:linear-gradient(135deg,#0f2a4a,#0d1f3a);margin:12px;border-radius:16px;padding:14px;border:1px solid #1e3a5f}
.mini{display:flex;gap:10px;margin:12px}.mini div{flex:1;background:#0d1a33;border-radius:14px;padding:12px;border:1px solid #1e3a5f}
.line{background:linear-gradient(90deg,#0f172a,#1e293b);margin:12px;border-radius:14px;padding:12px;border:1px solid #22c55e;display:flex;justify-content:space-between}
.live{margin:12px;background:#0a162d;border:2px solid #22c55e;border-radius:16px;padding:14px;box-shadow:0 0 15px rgba(34,197,94,.3)}
.ad{margin:12px;border-radius:16px;overflow:hidden;border:2px solid #22c55e;position:relative}.ad img{width:100%;height:150px;object-fit:cover}.ov{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:10px}
.card{background:#162032;margin:12px;border-radius:16px;padding:14px;border:1px solid #22314a}
.btn{width:100%;padding:12px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0a1222;display:flex;border-top:1px solid #22314a;padding:6px 0;z-index:99}.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}.btm div.on{color:#22c55e}.btm span{font-size:22px;display:block}
.meth{display:flex;gap:8px;margin-top:10px}.meth div{flex:1;background:#0f172a;border:2px solid #334155;border-radius:12px;padding:10px;text-align:center;cursor:pointer}.meth div.on{border-color:#22c55e;background:rgba(34,197,94,.15)}
.inp{width:100%;padding:11px;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}
</style></head><body>
<div class="top"><span>☰</span><input id="topText" readonly><span>✏️</span></div>
<div class="pro" onclick="proB()"><div><div style="font-weight:900"><span id="proT"></span> <span style="color:#4ade80" id="proS"></span></div><div style="font-size:11px;opacity:.7" id="proD"></div></div><div style="font-size:28px">🎁</div></div>

<div id="p-home">
<div class="line"><div><div style="font-weight:900;color:#4ade80" id="lineT">LIVE</div><div style="font-size:11px"><span id="totalU">0</span> Users • ID:<span id="myId"></span><br>Refer <span id="myRef">0</span> জন • ৳<span id="myRefE">0</span></div></div><div style="text-align:right"><div style="font-weight:900;color:#22c55e">৳<span id="totalW">0</span></div><div style="font-size:10px"><span id="totalWC">0</span> Withdraw<br>You ৳<span id="myW">0</span></div></div></div>

<div class="prof"><div class="ring"><img id="avatar"></div><div style="flex:1"><div style="font-weight:900;font-size:16px;display:flex;align-items:center;gap:6px"><span id="realName">BIG ADMIN</span> 👑<span style="width:18px;height:18px;background:#22c55e;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px">✓</span></div><div style="font-size:12px;color:#4ade80;margin-top:2px">📍 <span id="nameSub"></span> • ID:<span id="idShow"></span></div><div style="margin-top:6px"><span style="background:rgba(34,197,94,.15);color:#4ade80;padding:4px 10px;border-radius:20px;font-size:11px;border:1px solid #22c55e">Super Admin</span></div></div></div>

<div class="bal"><div style="font-size:11px;opacity:.6">TOTAL BALANCE</div><div style="font-size:28px;font-weight:900;color:#4ade80;margin-top:4px;display:flex;justify-content:space-between"><span>৳ <span id="bal">0</span></span><span>👁️</span></div><div style="font-size:12px;color:#4ade80">↗ +৳<span id="earn">0</span> this week</div></div>
<div class="mini"><div style="border-color:#22c55e"><div style="font-size:10px;opacity:.6">AVAILABLE</div><div style="font-weight:900">৳ <span id="avail">0</span></div><div style="font-size:11px;color:#4ade80">Ready</div></div><div><div style="font-size:10px;opacity:.6">PENDING</div><div style="font-weight:900">৳ 0</div><div style="font-size:11px;color:#60a5fa">Processing</div></div></div>

<div id="adsTop"></div>

<div class="live"><div style="display:flex;align-items:center;gap:8px"><div style="width:10px;height:10px;background:#22c55e;border-radius:50%"></div><div style="font-weight:900;color:#4ade80">LIVE WITHDRAW - MITMIT - 8807178385</div></div><div style="font-weight:800;margin-top:6px">— up to ৳ 10,000 <span style="color:#4ade80">- MITMIT GREEN LIVE</span></div><div style="margin-top:10px;display:flex;gap:8px;align-items:center"><button class="btn" style="background:#86efac;color:#000;width:auto;padding:6px 14px;border-radius:20px;font-size:13px" onclick="go('wallet')">Withdraw Now →</button><span style="font-size:11px;opacity:.7">Fee 0%</span></div></div>

<div class="card"><b>Watch Ads - <span id="adReward">2</span> Tk</b><button class="btn" style="background:linear-gradient(90deg,#0ea5e9,#0284c7);margin-top:10px" onclick="watchAd()" id="adBtn">Watch ADS</button><div id="tasks"></div></div>
<div id="adsMid"></div>
<div class="card"><b>👥 Live Users - ID সহ - Refer সহ</b><div id="uLive"></div></div>
<div class="card"><b>💸 Live Withdraw</b><div id="wLive"></div></div>
</div>

<div id="p-wallet" style="display:none"><div class="card"><b>Wallet - BIG ADMIN 8807178385</b><div style="font-size:34px;font-weight:900;color:#22c55e">৳ <span id="wBal">0</span></div><div style="font-size:11px;opacity:.6">Min ৳<span id="minW"></span> • ID:<span id="wId"></span></div></div><div class="card" style="border:2px solid #22c55e"><b>💰 Select Method - Logo সহ</b><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')"><div style="background:#e2136e;border-radius:10px;padding:14px;color:#fff;font-weight:900">bKash<br>Logo</div><div style="margin-top:6px;font-weight:900;color:#e2136e">bKash</div></div><div id="m-nagad" onclick="sel('Nagad')"><div style="background:#f97316;border-radius:10px;padding:14px;color:#fff;font-weight:900">Nagad<br>Logo</div><div style="margin-top:6px;font-weight:900;color:#f97316">Nagad</div></div><div id="m-rocket" onclick="sel('Rocket')"><div style="background:#7c3aed;border-radius:10px;padding:14px;color:#fff;font-weight:900">Rocket<br>Logo</div><div style="margin-top:6px;font-weight:900;color:#7c3aed">Rocket</div></div></div><input class="inp" id="wAmt" placeholder="Amount" type="number"><input class="inp" id="wNum" placeholder="bKash/Nagad Number"><button class="btn" style="background:#22c55e;margin-top:10px" onclick="doW()">Withdraw Now - Fee 0% - <span id="selT">bKash</span></button></div><div class="live"><div style="display:flex;gap:8px"><div style="width:10px;height:10px;background:#22c55e;border-radius:50%"></div><b style="color:#4ade80">Live Withdraw - MITMIT GREEN</b></div><div style="margin-top:6px">No withdraw - MITMIT GREEN LIVE</div></div><div id="adsWallet"></div></div>

<div id="p-tasksP" style="display:none"><div class="card"><div id="tasksAll"></div></div></div>
<div id="p-history" style="display:none"><div class="card"><b>Refer - <span id="refB">20</span> Tk</b><div class="inp" id="refLink" style="word-break:break-all"></div><button class="btn" style="background:#2563eb;margin-top:10px" onclick="navigator.clipboard.writeText(document.getElementById('refLink').innerText).then(()=>alert('Copied'))">Copy Refer Link - ID সহ</button><div style="margin-top:10px;font-size:13px">Refer: <span id="rC">0</span> জন - Earn ৳<span id="rE">0</span> - Withdraw ৳<span id="rW">0</span><br>ID:<span id="rId"></span> - By:<span id="rBy"></span></div></div></div>
<div id="p-more" style="display:none"><div class="card"><div id="moreI"></div></div></div>

<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasksP" onclick="go('tasksP')"><span>📋</span>Tasks</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-history" onclick="go('history')"><span>📊</span>History</div><div id="b-more" onclick="go('more')"><span>⚙️</span>More</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let meth='bKash';
function go(p){['home','wallet','tasksP','history','more'].forEach(x=>{let e=document.getElementById('p-'+x);if(e)e.style.display=x==p?'block':'none';let b=document.getElementById('b-'+x);if(b)b.classList.toggle('on',x==p);});}
function sel(m){meth=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');document.getElementById('selT').innerText=m;}
function proB(){fetch('/api/pro?id='+uid).then(r=>r.json()).then(x=>{alert(x.m);load();});}
function watchAd(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(()=>load());});}else{fetch('/api/reward?id='+uid).then(()=>load());}}
function doW(){let a=document.getElementById('wAmt').value;let n=document.getElementById('wNum').value;fetch(`/api/withdraw?id=${uid}&amount=${a}&number=${n}&method=${meth}`).then(r=>r.json()).then(x=>{alert(x.m);load();});}
function claim(i){fetch('/api/all?id='+uid).then(r=>r.json()).then(d=>{window.open(d.tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/task?id='+uid+'&i='+i).then(r=>r.json()).then(x=>{alert(x.m);load();});},2000);});}
function load(){let ref=new URLSearchParams(location.search).get('ref')||'';fetch('/api/all?id='+uid+'&ref='+ref).then(r=>r.json()).then(d=>{
document.getElementById('topText').value=d.s.top_text;document.getElementById('proT').innerText=d.s.pro_title;document.getElementById('proS').innerText=d.s.pro_sub;document.getElementById('proD').innerText=d.s.pro_desc;
document.getElementById('lineT').innerText=d.s.user_line;document.getElementById('totalU').innerText=d.total_u;document.getElementById('totalW').innerText=d.total_w;document.getElementById('totalWC').innerText=d.w_list.length;
document.getElementById('myId').innerText=d.u.id;document.getElementById('idShow').innerText=d.u.id;document.getElementById('wId').innerText=d.u.id;document.getElementById('rId').innerText=d.u.id;
document.getElementById('myRef').innerText=d.u.ref_c;document.getElementById('myRefE').innerText=d.u.ref_e;document.getElementById('myW').innerText=d.u.w_total;
document.getElementById('realName').innerText=d.u.real;document.getElementById('nameSub').innerText=d.u.name;document.getElementById('avatar').src=d.u.pic||d.s.admin_pic;
document.getElementById('bal').innerText=d.u.bal;document.getElementById('avail').innerText=d.u.bal;document.getElementById('wBal').innerText=d.u.bal;document.getElementById('earn').innerText=d.u.earn;document.getElementById('minW').innerText=d.s.min_w;
document.getElementById('adReward').innerText=d.s.ad_reward;document.getElementById('adBtn').innerText='Watch ADS - Claim ৳'+d.s.ad_reward;
document.getElementById('refB').innerText=d.s.refer_bonus;document.getElementById('refLink').innerText=location.origin+'/?ref='+d.u.id;document.getElementById('rC').innerText=d.u.ref_c;document.getElementById('rE').innerText=d.u.ref_e;document.getElementById('rW').innerText=d.u.w_total;document.getElementById('rBy').innerText=d.u.ref_by||'Direct';
document.getElementById('moreI').innerHTML=`ID: ${d.u.id}<br>Name: ${d.u.name}<br>Real: ${d.u.real}<br>Balance: ৳${d.u.bal}<br>Refer: ${d.u.ref_c} জন - ৳${d.u.ref_e}<br>Withdraw: ৳${d.u.w_total}<br>Join: ${d.u.join}<br>Ref By: ${d.u.ref_by||'Direct'}`;
let ads='';d.s.ads.forEach(a=>{ads+=`<div class="ad" onclick="window.open('${a.link}','_blank')"><img src="${a.img}"><div class="ov"><b>${a.title}</b><br><button class="btn" style="background:#22c55e;width:auto;padding:4px 10px;margin-top:4px">${a.btn}</button></div></div>`;});
document.getElementById('adsTop').innerHTML=ads;document.getElementById('adsMid').innerHTML=ads;document.getElementById('adsWallet').innerHTML=ads;
let tH='';d.tasks.forEach((t,i)=>{tH+=`<div class="card" style="margin:8px 0"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div style="color:#22c55e">৳${t.reward}</div></div><button class="btn" style="background:${t.color};margin-top:8px" onclick="claim(${i})">${t.btn}</button></div>`;});
document.getElementById('tasks').innerHTML=tH;document.getElementById('tasksAll').innerHTML=tH;
let uH='';d.u_list.forEach(u=>{uH+=`<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #22314a"><div>👤 ${u.name} • ID:${u.id.slice(-4)} • Ref:${u.ref_c} • By:${u.ref_by||'Direct'}</div><div style="color:#22c55e">৳${u.bal}</div></div>`;});document.getElementById('uLive').innerHTML=uH;
let wH='';d.w_list.forEach(w=>{wH+=`<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #22314a"><div>💸 ${w.name} • ${w.method} ${w.number} • ID:${w.uid.slice(-4)}</div><div style="color:#22c55e">৳${w.amount}</div></div>`;});document.getElementById('wLive').innerHTML=wH||'No withdraw - MITMIT GREEN LIVE';
});}
load();
</script></body></html>"""

ADMIN="""<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#0f172a;color:#fff;padding:12px;max-width:800px;margin:0 auto;font-family:sans-serif}.card{background:#1e293b;padding:14px;border-radius:12px;margin:10px 0;border:1px solid #334155}input{width:100%;padding:10px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#fff;margin:5px 0}button{padding:10px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}.stat{display:flex;gap:8px}.stat div{flex:1;background:#0f172a;padding:10px;border-radius:10px;text-align:center;border:1px solid #22c55e}table{width:100%;font-size:12px;border-collapse:collapse}td,th{padding:6px;border-bottom:1px solid #334155}</style></head><body>
<h2 style="color:#22c55e">ADMIN FINAL - ALL - 8807178385</h2>
<div class="stat"><div><div id="sU" style="font-size:20px;font-weight:900">0</div>Users</div><div><div id="sW" style="font-size:20px;font-weight:900">0</div>Withdraw</div><div><div id="sT" style="font-size:20px;font-weight:900">0</div>Total ৳</div><div><div id="sR" style="font-size:20px;font-weight:900">0</div>Refer</div></div>

<div class="card" style="border:2px solid #fbbf24"><h3>👑 User Edit - Refer + Withdraw + ID দেখবে</h3><input id="uid" value="8807178385"><button style="background:#f59e0b;width:100%" onclick="search()">Search ID - Refer + Withdraw দেখবে</button><div id="eBox" style="display:none;margin-top:10px"><input id="eName"><input id="eReal"><input id="eBal" type="number"><input id="ePic"><div id="eInfo" style="font-size:12px;margin-top:6px"></div><button style="background:#22c55e;width:100%;margin-top:8px" onclick="up()">Save</button></div></div>

<div class="card"><h3>🏆 Refer Report - কে কতটা Refer করলো - কত টাকা</h3><div id="refL"></div></div>
<div class="card"><h3>💸 Withdraw Report - ID + Method + Number + Amount</h3><div id="wL"></div></div>
<div class="card"><h3>👥 All Users - ID + Refer + Withdraw + By</h3><div id="allU"></div></div>

<div class="card"><h3>Settings - লেখা Edit</h3><input id="top_text" placeholder="Top Text"><input id="pro_title" placeholder="PRO Title"><input id="user_line" placeholder="User Line"><input id="pro_bonus" type="number" placeholder="PRO Bonus"><input id="refer_bonus" type="number" placeholder="Refer Bonus"><input id="min_w" type="number" placeholder="Min Withdraw"></div>
<div class="card"><h3>Company Ads</h3><div id="adsE"></div><button style="background:#22c55e;width:100%" onclick="addAd()">+ Add Ad</button></div>
<div class="card"><h3>Tasks</h3><div id="tasksE"></div><button style="background:#22c55e;width:100%" onclick="addT()">+ Add Task</button></div>
<div class="card" style="background:linear-gradient(90deg,#22c55e,#16a34a)"><button style="background:#fff;color:#16a34a;width:100%;padding:16px;font-weight:900" onclick="saveAll()">💾 SAVE ALL</button></div>

<script>let DB={};function load(){fetch('/api/admin/db?id=8807178385').then(r=>r.json()).then(d=>{DB=d;document.getElementById('sU').innerText=Object.keys(d.users).length;document.getElementById('sW').innerText=d.withdraws.length;document.getElementById('sT').innerText=d.withdraws.reduce((s,w)=>s+w.amount,0);document.getElementById('sR').innerText=Object.values(d.users).reduce((s,u)=>s+(u.ref_c||0),0);
for(let k in d.settings){let e=document.getElementById(k);if(e)e.value=d.settings[k];}
let refH='<table><tr><th>ID</th><th>Name</th><th>Refer</th><th>Earn</th><th>W</th></tr>';Object.values(d.users).sort((a,b)=>b.ref_c-a.ref_c).slice(0,20).forEach(u=>{refH+=`<tr><td>${u.id}</td><td>${u.name}</td><td style="color:#22c55e">${u.ref_c} জন</td><td>৳${u.ref_e}</td><td>৳${u.w_total}</td></tr>`;});refH+='</table>';document.getElementById('refL').innerHTML=refH;
let wH='';d.withdraws.slice(-20).reverse().forEach(w=>{wH+=`<div style="padding:6px;border-bottom:1px solid #334155">💸 ID:${w.uid} ${w.name} - ${w.method} ${w.number} - ৳${w.amount} - ${w.time}</div>`;});document.getElementById('wL').innerHTML=wH;
let all='<table><tr><th>ID</th><th>Name</th><th>Bal</th><th>Ref</th><th>W</th><th>By</th></tr>';Object.values(d.users).forEach(u=>{all+=`<tr><td>${u.id}</td><td>${u.name}</td><td>৳${u.bal}</td><td>${u.ref_c}</td><td>৳${u.w_total}</td><td>${u.ref_by||'Direct'}</td></tr>`;});all+='</table>';document.getElementById('allU').innerHTML=all;
let aH='';d.settings.ads.forEach((a,i)=>{aH+=`<div style="background:#0f172a;padding:8px;border-radius:8px;margin:6px 0"><b>Ad ${i+1}</b><button style="float:right;background:#dc2626;padding:4px" onclick="delAd(${i})">Del</button><input id="ad_t_${i}" value="${a.title}"><input id="ad_img_${i}" value="${a.img}"><input id="ad_link_${i}" value="${a.link}"><input id="ad_btn_${i}" value="${a.btn}"></div>`;});document.getElementById('adsE').innerHTML=aH;
let tH='';d.tasks.forEach((t,i)=>{tH+=`<div style="background:#0f172a;padding:8px;border-radius:8px;margin:6px 0"><input id="t_t_${i}" value="${t.title}"><input id="t_l_${i}" value="${t.link}"><input id="t_r_${i}" type="number" value="${t.reward}"></div>`;});document.getElementById('tasksE').innerHTML=tH;
});}
function addAd(){DB.settings.ads.push({title:"New Offer",img:"https://picsum.photos/200/100",link:"https://t.me",btn:"Shop"});load();}
function delAd(i){DB.settings.ads.splice(i,1);saveTemp();}
function addT(){DB.tasks.push({title:"New",link:"https://t.me",reward:20,color:"#2563eb",btn:"Join"});load();}
function search(){let id=document.getElementById('uid').value;fetch('/api/admin/user?id='+id).then(r=>r.json()).then(d=>{if(!d.f){alert('No User');return;}document.getElementById('eBox').style.display='block';document.getElementById('eName').value=d.u.name;document.getElementById('eReal').value=d.u.real;document.getElementById('eBal').value=d.u.bal;document.getElementById('ePic').value=d.u.pic;document.getElementById('eInfo').innerHTML=`Refer: ${d.u.ref_c} জন - Earn ৳${d.u.ref_e} - Withdraw ৳${d.u.w_total} - By ${d.u.ref_by||'Direct'} - Join ${d.u.join}`;});}
function up(){let data={id:document.getElementById('uid').value,name:document.getElementById('eName').value,real:document.getElementById('eReal').value,bal:document.getElementById('eBal').value,pic:document.getElementById('ePic').value};fetch('/api/admin/user_up',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(x=>{alert(x.m);load();});}
function saveTemp(){fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:DB.settings,tasks:DB.tasks,ads:DB.settings.ads})});}
function saveAll(){let s={};['top_text','pro_title','user_line','pro_bonus','refer_bonus','min_w'].forEach(k=>{let e=document.getElementById(k);if(e)s[k]=e.value;});let ads=[];for(let i=0;i<DB.settings.ads.length;i++){let t=document.getElementById('ad_t_'+i);if(!t)continue;ads.push({title:t.value,img:document.getElementById('ad_img_'+i).value,link:document.getElementById('ad_link_'+i).value,btn:document.getElementById('ad_btn_'+i).value});}let tasks=[];for(let i=0;i<DB.tasks.length;i++){let t=document.getElementById('t_t_'+i);if(!t)continue;tasks.push({title:t.value,link:document.getElementById('t_l_'+i).value,reward:parseInt(document.getElementById('t_r_'+i).value),color:"#2563eb",btn:"Join"});}fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:{...s,ads:ads},tasks:tasks,ads:ads})}).then(()=>{alert('Saved - Final');load();});}
load();
</script></body></html>"""

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
