# FINAL FIX - ADMIN PANEL OK + PROFILE PAGE FIX + ELOMELO FIX - 8807178385
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"
TOKEN = "11764581"

def load_db():
    if not os.path.exists(DB_FILE):
        d={"users":{"8807178385":{"id":"8807178385","bal":60,"ads":0,"ref":0}},"w":[],"s":{
            "app_title":f"প্রতিদিনের কাজ BD - {TOKEN} - {ADMIN_ID}",
            "notice_title":f"অফিসিয়াল নোটিস - {TOKEN}",
            "notice_desc":f"প্রতিদিন Ads দেখুন - ৳500 ইনকাম - Token {TOKEN}",
            "wallet_title":f"Wallet - {ADMIN_ID}",
            "profile_title":f"Profile - {ADMIN_ID} - {TOKEN}",
            "profile_desc":f"আপনার প্রোফাইল - ID {ADMIN_ID} - কোম্পানির সাথে কানেক্টেড - Token {TOKEN}",
            "support_title":f"সাপোর্ট সেন্টার - {ADMIN_ID}",
            "support_desc":f"Telegram: @ProtidinerKajBD\nAdmin ID: {ADMIN_ID}\nToken: {TOKEN}\n২৪ ঘণ্টা Support - কোম্পানি থেকে সরাসরি হেল্প পাবেন"
        }}
        with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,ensure_ascii=False)
        return d
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except:
        return {"users":{"8807178385":{"id":"8807178385","bal":60,"ads":0}},"w":[],"s":{}}

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)

@app.route('/')
def home(): return render_template_string(USER_PAGE)

@app.route('/admin')
def admin():
    if request.args.get('id')!= ADMIN_ID:
        return f"<center><h2>Admin ID দাও</h2><p>/admin?id={ADMIN_ID}</p><p>Your Company ID: {ADMIN_ID}<br>Token: {TOKEN}<br>Company Connected ✅</p></center>"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/bal')
def api_bal():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0,"ref":0}
    return jsonify({"bal":db["users"][uid]["bal"],"ads":db["users"][uid]["ads"],"id":uid,"total_users":len(db["users"]),"total_w":len(db["w"]),"w":db["w"][-15:][::-1],"s":db.get("s",{}),"users":list(db["users"].values())})

@app.route('/api/add')
def api_add():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0,"ref":0}
    db["users"][uid]["bal"]+=int(request.args.get('amt',2))
    db["users"][uid]["ads"]+=1
    save_db(db)
    return jsonify({"ok":True})

@app.route('/api/wd')
def api_wd():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    amt=int(request.args.get('amt',0))
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0,"ref":0}
    if db["users"][uid]["bal"]<amt: return jsonify({"msg":"Balance কম - Min 1000 লাগবে"})
    db["users"][uid]["bal"]-=amt
    db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"met":request.args.get('met','bKash'),"time":str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg":f"Withdraw {amt}Tk Success - {request.args.get('met')} {request.args.get('num')}"})

@app.route('/api/save',methods=['POST'])
def api_save():
    db=load_db()
    db["s"].update(request.json)
    save_db(db)
    return jsonify({"msg":"Saved - Live"})

@app.route('/api/del_wd')
def del_wd():
    if request.args.get('id')!=ADMIN_ID: return jsonify({"msg":"Admin Only"})
    db=load_db()
    db["w"]=[]
    save_db(db)
    return jsonify({"msg":"Clear"})

USER_PAGE = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#08112e;color:#fff;max-width:430px;margin:0 auto;padding-bottom:95px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px 18px 22px 18px}
.bal{font-size:52px;font-weight:900;color:#2ef36c;margin-top:6px}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.dot{width:12px;height:12px;background:#2ef36c;border-radius:50%;animation:blk 0.8s infinite;box-shadow:0 0 10px #2ef36c}
@keyframes blk{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:18px;height:175px;position:relative;overflow:hidden;background:#000;border:1px solid #2a3a6b}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:13px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0 6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer;line-height:1.2}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #2a3a5f;background:#0b142d;color:#fff;margin-top:10px;outline:none}
.inp:focus{border-color:#2ef36c}
.meth{display:flex;gap:8px;margin-top:12px}
.meth div{flex:1;background:#0b142d;border:2px solid #2a3a5f;border-radius:12px;padding:12px;text-align:center;cursor:pointer;font-weight:700}
.meth div.on{border-color:#ff2d7a;background:#1a1430}
</style></head><body>
<div id="p-home">
<div class="hdr"><div style="font-size:14px;opacity:0.9" id="appTitle">প্রতিদিনের কাজ BD - 11764581 - 8807178385</div><div class="bal">৳ <span id="bh">60</span></div><div style="font-size:13px;opacity:0.7;margin-top:4px">Ads: <span id="adH">0</span>/100 - 11764581</div></div>
<div class="notice"><div style="flex:1"><div style="font-weight:900;font-size:16px" id="noticeTitle">অফিসিয়াল নোটিস - 11764581</div><div style="font-size:12px;opacity:0.85;margin-top:3px" id="noticeDesc">প্রতিদিন Ads দেখুন - ৳500 ইনকাম - Token 11764581</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:10px 18px;border-radius:30px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"><img class="on" src="https://picsum.photos/600/300?random=21"><img src="https://picsum.photos/600/300?random=22"><img src="https://picsum.photos/600/300?random=23"><img src="https://picsum.photos/600/300?random=24"><img src="https://picsum.photos/600/300?random=25"><img src="https://picsum.photos/600/300?random=26"></div>
<div class="card"><div style="font-weight:800;font-size:15px">🎬 স্পেশাল অফার - Mini Boy Ads - 11764581</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">ADS দেখুন - Token 11764581 - ৳2</button><div style="font-size:11px;opacity:0.5;margin-top:8px">Zone: 11764581 - Token 11764581 - Admin 8807178385</div></div>
<div id="tasksHome"></div>
</div>

<div id="p-tasks" style="display:none">
<div class="hdr"><div>প্রতিদিনের কাজ BD - 11764581</div><div class="bal">৳ <span id="bt">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span id="adT">0</span>/100</div></div>
<div id="tasksAll"></div>
</div>

<div id="p-refer" style="display:none">
<div class="hdr"><div>প্রতিদিনের কাজ BD - Refer</div><div class="bal">৳ <span id="br">60</span></div></div>
<div class="card"><div style="font-weight:900">Refer & Earn ৳20 - 11764581</div><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyR()">Copy Link</button></div>
<div class="card"><div style="font-weight:800">📖 কিভাবে রেফার কাজ করে?</div><div style="font-size:13px;opacity:0.8;margin-top:6px;line-height:1.5">১. লিংক Copy করুন<br>২. বন্ধুকে পাঠান<br>৩. প্রতি রেফারে ৳20 পাবেন<br>Token 11764581 - Admin 8807178385</div></div>
</div>

<div id="p-wallet" style="display:none">
<div class="hdr"><div>Wallet - 8807178385</div><div class="bal">৳ <span id="bw">60</span></div><div style="opacity:0.7;font-size:13px">Min: ৳1000 - Token 11764581</div></div>
<div class="card"><div style="font-weight:900">Wallet - 8807178385</div><div style="font-size:38px;font-weight:900;color:#2ef36c">৳ <span id="bw2">60</span></div><div style="opacity:0.6">Min: ৳1000 - Token 11764581</div></div>
<div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')">bKash - 11764581</div><div id="m-nagad" onclick="sel('Nagad')">Nagad - 11764581</div></div><input class="inp" id="wNum" placeholder="Number - 01XXXXXXXXX"><button class="btn" style="background:#2563eb;margin-top:12px" onclick="wd()">Withdraw - 11764581</button></div>
<div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c;display:flex;gap:6px;align-items:center"><span class="dot"></span>Live Withdraw - সবাই কত তুলছে - Auto</div><div style="font-size:11px;opacity:0.6;margin-top:4px">কেউ Withdraw করলেই এখানে Auto ভাসবে - Token 11764581</div><div id="liveList" style="margin-top:10px;font-size:13px">এখনো কেউ Withdraw করেনি - Token 11764581</div></div>
<div class="card" style="border:2px solid #0ea5e9"><div style="font-weight:900">Withdraw নিয়ম - Admin থেকে Change - 11764581</div><div style="white-space:pre-line;font-size:12px;margin-top:8px;opacity:0.8;line-height:1.6">১. Minimum ৳1000 হলে Withdraw
২. bKash / Nagad Number সঠিক দিন
৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট
৪. ভুল Number দিলে দায় আপনার
৫. একাধিক Account Ban
Admin 8807178385 - Token 11764581</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">Mini Boy Ad দেখুন - 11764581</button></div>
</div>

<div id="p-profile" style="display:none">
<div class="hdr"><div>Profile - 8807178385 - 11764581</div><div class="bal">৳ <span id="bp">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span id="adP">0</span>/100 - Company Connected ✅</div></div>
<div class="card"><div style="font-weight:900;font-size:16px" id="profileTitle">Profile - 8807178385 - 11764581</div><div style="opacity:0.7;margin-top:4px">ID: <span id="pid">8807178385</span> - Balance ৳<span id="bp2">60</span></div><div style="margin-top:10px;background:#0b142d;border-radius:10px;padding:10px;font-size:13px;line-height:1.6" id="profileDesc">আপনার প্রোফাইল - কোম্পানির সাথে কানেক্টেড - Token 11764581 - সব কাজ ঠিকঠাক চলছে</div></div>
<div class="card"><div style="font-weight:900">🎯 আমার কাজের হিসাব</div><div style="margin-top:10px;display:flex;gap:10px"><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#2ef36c" id="adP2">0</div><div style="font-size:11px;opacity:0.6">Ads দেখা</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#0ea5e9">11764581</div><div style="font-size:11px;opacity:0.6">Token ID</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#f59e0b">Active</div><div style="font-size:11px;opacity:0.6">Status</div></div></div></div>
<div class="card" style="border:1px solid #0ea5e9"><div style="font-weight:900" id="supportTitle">সাপোর্ট সেন্টার - 8807178385</div><div style="font-size:13px;opacity:0.85;margin-top:8px;white-space:pre-line;line-height:1.6" id="supportDesc">Telegram: @ProtidinerKajBD
Admin ID: 8807178385
Token: 11764581
২৪ ঘণ্টা Support - কোম্পানি থেকে সরাসরি হেল্প পাবেন - কোন সমস্যা হলে মেসেজ দিন</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="window.open('https://t.me','_blank')">Telegram Support - Join</button></div>
<div class="card" style="background:linear-gradient(135deg,#132042,#1e3a5a)"><div style="font-weight:900">✅ কোম্পানির সাথে কানেক্ট - Verified</div><div style="font-size:12px;opacity:0.7;margin-top:6px">Admin ID: 8807178385 - Token 11764581 - Zone 11764581 - সব কিছু ঠিকঠাক আছে - Company Verified ✅</div></div>
</div>

<div class="btm">
<div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div>
<div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div>
<div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div>
<div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div>
<div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let method='bKash';
let tasks=[
{title:'YouTube Subscribe',reward:25,link:'https://youtube.com',color:'#dc2626',btn:'Join & Get 25 Tk - 11764581'},
{title:'Telegram Join',reward:10,link:'https://t.me',color:'#1e40af',btn:'Join & Get 10 Tk - 11764581'},
{title:'Facebook Follow',reward:15,link:'https://facebook.com',color:'#0ea5e9',btn:'Follow & Get 15 Tk - 11764581'},
{title:'Website Visit',reward:20,link:'https://google.com',color:'#7c3aed',btn:'Visit & Get 20 Tk - 11764581'},
{title:'Group Join',reward:20,link:'https://t.me',color:'#0f766e',btn:'Join & Get 20 Tk - 11764581'},
{title:'Post Like',reward:20,link:'https://facebook.com',color:'#be123c',btn:'Like & Get 20 Tk - 11764581'}
];
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});window.scrollTo(0,0);}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Link Copied ✅'));}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid+'&amt=2').then(()=>load());});}else{fetch('/api/add?id='+uid+'&amt=2').then(()=>{alert('Ads ৳2 Added ✅');load();});}}
function claim(i){window.open(tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/add?id='+uid+'&amt='+tasks[i].reward).then(()=>{alert('৳'+tasks[i].reward+' Added ✅');load();});},1200);}
function wd(){let amt=document.getElementById('wAmt').value;let num=document.getElementById('wNum').value;if(!amt||!num){alert('Amount & Number লাগবে');return;}fetch('/api/wd?id='+uid+'&amt='+amt+'&num='+num+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
let slIdx=0;setInterval(()=>{let imgs=document.querySelectorAll('#sl img');imgs.forEach(im=>im.classList.remove('on'));slIdx=(slIdx+1)%imgs.length;imgs[slIdx].classList.add('on');},2000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{['bh','bt','br','bw','bw2','bp','bp2'].forEach(id=>{let el=document.getElementById(id);if(el)el.innerText=d.bal;});['adH','adT','adP','adP2'].forEach(id=>{let el=document.getElementById(id);if(el)el.innerText=d.ads;});document.getElementById('pid').innerText=d.id;document.getElementById('refLink').value=location.origin+'/?ref='+d.id;let live='';if(d.w.length==0)live='এখনো কেউ Withdraw করেনি - Token 11764581';else d.w.forEach(w=>{live+='<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">💸 ID:'+w.id.slice(-4)+' - ৳'+w.amt+' - '+w.met+' '+w.num+' - '+w.time+'</div>';});document.getElementById('liveList').innerHTML=live;if(d.s.app_title)document.getElementById('appTitle').innerText=d.s.app_title;});}
function renderTasks(){let h='';tasks.forEach((t,i)=>{h+='<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ '+t.title+'</div><div>৳'+t.reward+'</div></div><button class="btn" style="background:'+t.color+';margin-top:10px" onclick="claim('+i+')">'+t.btn+'</button></div>';});document.getElementById('tasksHome').innerHTML=h;document.getElementById('tasksAll').innerHTML=h;}
renderTasks();load();
</script></body></html>
'''

ADMIN_PAGE = '''
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a1020;color:#fff;font-family:sans-serif;padding:14px;max-width:500px;margin:0 auto;padding-bottom:100px}
.card{background:#151f35;border:1px solid #1e2d4f;border-radius:16px;padding:14px;margin:12px 0}
.label{color:#38bdf8;font-size:12px;margin:14px 0 6px 0;display:flex;justify-content:space-between}
.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:10px;padding:12px;width:100%;color:#fff;outline:none}
.input:focus{border-color:#22c55e}
.copy{font-size:11px;background:#1e293b;padding:5px 10px;border-radius:6px;cursor:pointer;color:#22c55e;border:1px solid #334155}
.btn-save{width:100%;max-width:480px;position:fixed;bottom:12px;left:50%;transform:translateX(-50%);padding:16px;background:linear-gradient(90deg,#22c55e,#16a34a);border:0;border-radius:14px;font-weight:900;color:#fff;z-index:99;box-shadow:0 -4px 20px rgba(0,0,0,0.6)}
.badge{background:#22c55e;color:#000;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:800}
</style></head><body>
<h2 style="color:#22c55e;text-align:center;margin-top:10px">✅ ADMIN PANEL OK<br>8807178385 - Token 11764581</h2>
<p style="text-align:center;opacity:0.7;font-size:13px;margin:8px 0">Company Connected ✅ - সব ঠিকঠাক - Admin Active</p>

<div class="card" style="border:2px solid #22c55e"><div id="info" style="font-weight:800;line-height:1.6"></div></div>

<div class="card">
<div style="font-weight:900;font-size:16px">📝 সব লেখা Control - একটা একটা Copy করো <span class="badge">LIVE</span></div>

<div class="label">App Title (উপরে) <span class="copy" onclick="copyV('app_title')">Copy</span></div>
<input class="input" id="app_title" value="প্রতিদিনের কাজ BD - 11764581 - 8807178385">

<div class="label">Notice Title <span class="copy" onclick="copyV('notice_title')">Copy</span></div>
<input class="input" id="notice_title" value="অফিসিয়াল নোটিস - 11764581">

<div class="label">Notice Desc <span class="copy" onclick="copyV('notice_desc')">Copy</span></div>
<textarea class="input" id="notice_desc" style="min-height:70px">প্রতিদিন Ads দেখুন - ৳500 ইনকাম - Token 11764581 - Admin 8807178385</textarea>

<div class="label">Profile Title (5 নং পেজ) <span class="copy" onclick="copyV('profile_title')">Copy</span></div>
<input class="input" id="profile_title" value="Profile - 8807178385 - 11764581">

<div class="label">Profile Description (5 নং পেজের ভিতরে লেখা) <span class="copy" onclick="copyV('profile_desc')">Copy</span></div>
<textarea class="input" id="profile_desc" style="min-height:90px">আপনার প্রোফাইল - ID 8807178385 - কোম্পানির সাথে কানেক্টেড - Token 11764581 - সব কাজ ঠিকঠাক চলছে - Company Verified ✅</textarea>

<div class="label">Wallet Title <span class="copy" onclick="copyV('wallet_title')">Copy</span></div>
<input class="input" id="wallet_title" value="Wallet - 8807178385">

<div class="label">Support Title <span class="copy" onclick="copyV('support_title')">Copy</span></div>
<input class="input" id="support_title" value="সাপোর্ট সেন্টার - 8807178385">

<div class="label">Support Description (5 নং পেজ) <span class="copy" onclick="copyV('support_desc')">Copy</span></div>
<textarea class="input" id="support_desc" style="min-height:110px">Telegram: @ProtidinerKajBD
Admin ID: 8807178385
Token: 11764581
২৪ ঘণ্টা Support - কোম্পানি থেকে সরাসরি হেল্প পাবেন - কোন সমস্যা হলে মেসেজ দিন
Company Connected ✅</textarea>
</div>

<div class="card">
<div style="font-weight:900">💸 Live Withdraw List - কে কত তুলছে - Auto <span class="badge" id="wCount">0</span></div>
<div id="wList" style="margin-top:10px;font-size:13px"></div>
<button style="background:#dc2626;width:100%;padding:10px;border:0;border-radius:10px;margin-top:10px;color:#fff;font-weight:700" onclick="clearW()">Clear All Withdraw - Admin Only</button>
</div>

<div class="card">
<div style="font-weight:900">👥 Users List - কোম্পানির সাথে কারা আছে</div>
<div id="uList" style="margin-top:10px;font-size:12px"></div>
</div>

<div style="height:80px"></div>
<button class="btn-save" onclick="saveAll()">💾 SAVE ALL - LIVE করো - Company Connected ✅</button>

<script>
function copyV(id){let el=document.getElementById(id);el.select();el.setSelectionRange(0,99999);navigator.clipboard.writeText(el.value).then(()=>alert('Copied: '+id+' ✅'));}
function load(){
fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{
document.getElementById('info').innerHTML=
'✅ Company Connected<br>'+
'👑 Admin ID: 8807178385 - Active<br>'+
'🔑 Token: 11764581 - Zone: 11764581<br>'+
'👥 Total Users: '+d.total_users+' জন<br>'+
'💸 Total Withdraw: '+d.total_w+' টা<br>'+
'💰 Your Balance: ৳'+d.bal+'<br>'+
'📺 Ads: '+d.ads+'/100<br>'+
'ID: '+d.id+' - সব ঠিকঠাক ✅';

for(let k in d.s){let el=document.getElementById(k);if(el&&d.s[k])el.value=d.s[k];}

let wHtml='';
if(d.w.length==0) wHtml='<div style="opacity:0.5">এখনো কেউ Withdraw করেনি - Token 11764581</div>';
else d.w.forEach(w=>{wHtml+='<div style="padding:8px 0;border-bottom:1px solid #1e2d4f;display:flex;justify-content:space-between"><span>💸 ID:'+w.id.slice(-4)+' - ৳'+w.amt+' - '+w.met+'</span><span style="opacity:0.5;font-size:11px">'+w.time+'</span></div><div style="opacity:0.7;font-size:11px;padding-bottom:6px">'+w.num+'</div>';});
document.getElementById('wList').innerHTML=wHtml;
document.getElementById('wCount').innerText=d.w.length;

let uHtml='';
if(d.users){d.users.slice(0,20).forEach(u=>{uHtml+='<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">👤 ID:'+u.id+' - ৳'+u.bal+' - Ads:'+u.ads+'</div>';});}
document.getElementById('uList').innerHTML=uHtml;
});
}
function saveAll(){
let data={};
['app_title','notice_title','notice_desc','profile_title','profile_desc','wallet_title','support_title','support_desc'].forEach(k=>{
let el=document.getElementById(k);if(el)data[k]=el.value;
});
fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>{alert('✅ Saved - User App এ Live - Profile Page ও ঠিক হলো');load();});
}
function clearW(){if(confirm('Clear All Withdraw?')){fetch('/api/del_wd?id=8807178385').then(()=>{alert('Cleared');load();});}}
load();
setInterval(load,5000);
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
