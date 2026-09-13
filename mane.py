# FINAL RESTORED - SCREENSHOT SAME DESIGN - NO CUT - ONLY BUG FIX
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime, timedelta
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    if not os.path.exists(DB_FILE):
        d={"users":{},"w":[],"s":{"admin_name":"প্রতিদিনের কাজ BD","admin_pic":"https://i.pravatar.cc/150?img=32","profile_box":"✅ Official Telegram Channel এ Join করুন - @ProtidinerKajBD","ads_limit":100}}
        with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,ensure_ascii=False)
        return d
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)

def get_user(db, uid):
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"bal":60,"ads":0,"uname":f"User {uid[-4:]}","upic":"","tasks":{},"last_ads_reset":str(datetime.now().date())}
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
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); save_db(db)
    return jsonify({"bal":u["bal"],"ads":u["ads"],"id":uid,"uname":u.get("uname"),"upic":u.get("upic"),"tasks":u.get("tasks",{}),"w":db["w"][-15:][::-1],"s":db.get("s",{}),"total_users":len(db["users"])})

@app.route('/api/add')
def api_add():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid)
    limit=db.get("s",{}).get("ads_limit",100)
    if u["ads"]>=limit: return jsonify({"ok":False,"msg":f"আজকের {limit} টা Ads শেষ"})
    u["bal"]+=2; u["ads"]+=1; save_db(db); return jsonify({"ok":True,"bal":u["bal"]})

@app.route('/api/claim_task')
def api_claim_task():
    uid=request.args.get('id',ADMIN_ID); tid=request.args.get('tid','0'); db=load_db(); u=get_user(db,uid)
    rewards=[25,10,15,20,20,20]; reward=rewards[int(tid)] if int(tid)<len(rewards) else 20
    last=u.get("tasks",{}).get(tid)
    if last:
        diff=datetime.now()-datetime.fromisoformat(last)
        if diff < timedelta(hours=24): return jsonify({"ok":False,"msg":f"২৪ ঘন্টা পর আবার - {int(24-diff.total_seconds()/3600)} ঘন্টা বাকি"})
    if "tasks" not in u: u["tasks"]={}
    u["tasks"][tid]=datetime.now().isoformat(); u["bal"]+=reward; save_db(db)
    return jsonify({"ok":True,"bal":u["bal"],"msg":f"৳{reward} Added ✅"})

@app.route('/api/wd')
def api_wd():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); amt=int(request.args.get('amt',0))
    if u["bal"]<amt or amt<1000: return jsonify({"msg":"Min ৳1000"})
    u["bal"]-=amt; db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"met":request.args.get('met','bKash'),"time":str(datetime.now())[:16]}); save_db(db); return jsonify({"msg":"Withdraw Success - ২৪ ঘন্টায় পেমেন্ট"})

@app.route('/api/save',methods=['POST'])
def api_save(): db=load_db(); db["s"].update(request.json); save_db(db); return jsonify({"msg":"Saved"})
@app.route('/api/update_profile',methods=['POST'])
def api_upd(): j=request.json; uid=j.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid);
    if j.get('uname'): u["uname"]=j.get('uname")
    if j.get('upic'): u["upic"]=j.get('upic"); save_db(db); return jsonify({"msg":"Updated"})

USER_PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#081028;color:#fff;max-width:430px;margin:0 auto;padding-bottom:95px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px 18px 22px 18px}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:19px;font-weight:800;display:flex;align-items:center;gap:6px}
.hdr-pic{width:46px;height:46px;border-radius:50%;border:2px solid #2ef36c;object-fit:cover}
.bal{font-size:52px;font-weight:900;color:#2ef36c;margin-top:8px}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.dot{width:10px;height:10px;background:#2ef36c;border-radius:50%;animation:blk 0.8s infinite}
@keyframes blk{0%{opacity:1}50%{opacity:0.3}100%{opacity:1}}
.slider{margin:12px;border-radius:18px;height:185px;position:relative;overflow:hidden;background:#000;border:1px solid #1e2d4f}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0 6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #2a3a5f;background:#0b142d;color:#fff;margin-top:10px;outline:none}
.meth{display:flex;gap:8px;margin-top:12px}
.meth div{flex:1;background:#0b142d;border:2px solid #2a3a5f;border-radius:12px;padding:12px;text-align:center;cursor:pointer;font-weight:700}
.meth div.on{border-color:#ff2d7a;background:#1a1430}
</style></head><body>
<div id="p-home"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName">👑 প্রতিদিনের কাজ BD ✅</div><img id="hdrPic" class="hdr-pic" src="https://i.pravatar.cc/150?img=32"></div><div class="bal">৳ <span class="balV">60</span></div><div style="font-size:13px;opacity:0.7;margin-top:4px">Ads: <span class="adsV">0</span>/<span class="limitV">100</span></div></div><div class="notice"><div><div style="font-weight:900;font-size:16px">অফিসিয়াল নোটিস</div><div style="font-size:12px;opacity:0.85;margin-top:3px">প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম করুন</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:10px 18px;border-radius:30px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div><div class="slider" id="sl"><img class="on" src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600"><img src="https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600"><img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"></div><div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="watchAds()">ADS দেখুন - ৳2 বোনাস</button></div><div id="tasksHome"></div></div>
<div id="p-tasks" style="display:none"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName2">👑 প্রতিদিনের কাজ BD ✅</div><img id="hdrPic2" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div><div style="font-size:13px;opacity:0.7;margin-top:4px">Ads: <span class="adsV">0</span>/<span class="limitV">100</span></div></div><div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="watchAds()">ADS দেখুন - ৳2 বোনাস</button></div><div id="tasksAll"></div></div>
<div id="p-refer" style="display:none"><div class="hdr"><div style="font-weight:700;font-size:19px">রেফার করুন</div><div class="bal">৳ <span class="balV">60</span></div></div><div class="card"><div style="font-weight:900">Refer & Earn ৳20</div><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyR()">Copy Link</button></div><div class="card"><div style="font-weight:900">📖 কিভাবে রেফার কাজ করে?</div><div style="font-size:13px;opacity:0.8;margin-top:6px;line-height:1.6">১. লিংক Copy করুন<br>২. বন্ধুকে পাঠান<br>৩. প্রতি রেফারে ৳20 বোনাস পাবেন</div></div></div>
<div id="p-wallet" style="display:none"><div class="hdr"><div style="font-weight:700;font-size:19px">আমার ওয়ালেট</div><div class="bal">৳ <span class="balV">60</span></div><div style="opacity:0.7;font-size:13px;margin-top:4px">সর্বনিম্ন উত্তোলন ৳1000</div></div><div class="card"><div style="font-weight:900">আমার ব্যালেন্স</div><div style="font-size:38px;font-weight:900;color:#2ef36c">৳ <span class="balV">60</span></div><div style="opacity:0.6;font-size:13px">সর্বনিম্ন ৳1000 হলে তুলতে পারবেন</div></div><div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')">bKash</div><div id="m-nagad" onclick="sel('Nagad')">Nagad</div></div><input class="inp" id="wNum" placeholder="Number - 01XXXXXXXXX"><button class="btn" style="background:#2563eb;margin-top:12px" onclick="wd()">Withdraw করুন</button></div><div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c;display:flex;gap:6px;align-items:center">🟢 Live Withdraw - সবাই কত তুলছে</div><div style="font-size:11px;opacity:0.6;margin-top:4px">কেউ Withdraw করলেই এখানে দেখাবে</div><div id="liveList" style="margin-top:10px;font-size:13px">এখনো কেউ Withdraw করেনি</div></div><div class="card" style="border:1px solid #0ea5e9"><div style="font-weight:900">Withdraw নিয়ম</div><div style="white-space:pre-line;font-size:12px;margin-top:8px;opacity:0.8;line-height:1.6">১. সর্বনিম্ন ৳1000 হলে Withdraw
২. bKash / Nagad Number সঠিক দিন
৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন
৪. ভুল Number দিলে দায় আপনার
৫. একাধিক Account করলে Ban হবে</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="watchAds()">বোনাস Ads দেখুন</button></div></div>
<div id="p-profile" style="display:none"><div class="hdr" style="text-align:center"><img id="userPic" style="width:90px;height:90px;border-radius:50%;border:4px solid #2ef36c;object-fit:cover" src="https://i.pravatar.cc/150?img=8"><div style="font-weight:900;font-size:18px;margin-top:10px" id="userName">User</div><div style="opacity:0.7;font-size:13px;margin-top:4px">ID: <span id="pid">----</span> - Verified ✅</div><div class="bal" style="text-align:center">৳ <span class="balV">60</span></div><div style="opacity:0.7">Ads: <span class="adsV">0</span>/<span class="limitV">100</span></div></div><div class="card" style="border:2px solid #22c55e"><div style="font-weight:900">✏️ আমার প্রোফাইল পরিবর্তন করুন</div><div style="font-size:12px;opacity:0.6;margin-top:4px">নাম ও ছবি পরিবর্তন করতে পারবেন</div><input class="inp" id="editName" placeholder="আপনার নাম লিখুন"><input class="inp" id="editPic" placeholder="ছবির Link - imgbb.com থেকে"><button class="btn" style="background:#22c55e;color:#000;margin-top:12px" onclick="saveProfile()">💾 Save Profile</button></div><div class="card"><div style="font-weight:900">🎯 আমার কাজের হিসাব</div><div style="margin-top:10px;display:flex;gap:10px"><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#2ef36c" class="adsV">0</div><div style="font-size:11px;opacity:0.6">Ads দেখা</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#0ea5e9" class="balV">60</div><div style="font-size:11px;opacity:0.6">ব্যালেন্স</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#f59e0b">Active</div><div style="font-size:11px;opacity:0.6">Status</div></div></div></div><div class="card" style="border:2px solid #f59e0b;background:linear-gradient(135deg,#1f1a0f,#132042)"><div style="font-weight:900;color:#fbbf24">📢 Admin Notice</div><div id="adminBoxText" style="font-size:13px;margin-top:8px;line-height:1.6;opacity:0.9">Loading...</div></div></div>
<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385'; let method='bKash';
let tasks=[{title:'YouTube Subscribe',reward:25,link:'https://youtube.com',color:'#dc2626',btn:'Join & Get 25 Tk'},{title:'Telegram Join',reward:10,link:'https://t.me',color:'#1e40af',btn:'Join & Get 10 Tk'},{title:'Facebook Follow',reward:15,link:'https://facebook.com',color:'#0ea5e9',btn:'Follow & Get 15 Tk'},{title:'Website Visit',reward:20,link:'https://google.com',color:'#7c3aed',btn:'Visit & Get 20 Tk'},{title:'Group Join',reward:20,link:'https://t.me',color:'#0f766e',btn:'Join & Get 20 Tk'},{title:'Post Like',reward:20,link:'https://facebook.com',color:'#be123c',btn:'Like & Get 20 Tk'}];
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Link Copied ✅'));}
function watchAds(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(r=>r.json()).then(j=>{if(!j.ok){alert(j.msg);return;}alert('৳2 Added ✅ - সাথে সাথে যোগ হইছে');load();});});}else{fetch('/api/add?id='+uid).then(r=>r.json()).then(j=>{if(!j.ok){alert(j.msg);return;}alert('৳2 Added ✅');load();});}}
function doTask(i){window.open(tasks[i].link,'_blank'); setTimeout(()=>{if(confirm('আপনি কি '+tasks[i].title+' Complete করেছেন? Join/Follow করেছেন? OK দিলে টাকা যোগ হবে')){fetch('/api/claim_task?id='+uid+'&tid='+i).then(r=>r.json()).then(j=>{alert(j.msg);load();});}},3000);}
function wd(){let amt=document.getElementById('wAmt').value;let num=document.getElementById('wNum').value;if(!amt||!num){alert('Amount & Number লাগবে');return;}fetch('/api/wd?id='+uid+'&amt='+amt+'&num='+num+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function saveProfile(){let n=document.getElementById('editName').value,p=document.getElementById('editPic').value;if(!n&&!p){alert('নাম বা ছবির Link দিন');return;}fetch('/api/update_profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,uname:n,upic:p})}).then(()=>{alert('✅ Profile Updated');load();});}
let slIdx=0;setInterval(()=>{let imgs=document.querySelectorAll('#sl img');imgs.forEach(im=>im.classList.remove('on'));slIdx=(slIdx+1)%imgs.length;imgs[slIdx].classList.add('on');},3000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{document.querySelectorAll('.balV').forEach(e=>e.innerText=d.bal);document.querySelectorAll('.adsV').forEach(e=>e.innerText=d.ads);document.querySelectorAll('.limitV').forEach(e=>e.innerText=d.s.ads_limit||100);document.getElementById('pid').innerText=d.id.slice(0,4)+'****'+d.id.slice(-2);document.getElementById('refLink').value=location.origin+'/?ref='+d.id;let live='';if(d.w.length==0)live='এখনো কেউ Withdraw করেনি';else d.w.forEach(w=>{live+='<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">💸 ID:'+w.id.slice(-4)+' - ৳'+w.amt+' - '+w.met+' - '+w.time+'</div>';});document.getElementById('liveList').innerHTML=live;let an=d.s.admin_name||'প্রতিদিনের কাজ BD';let ap=d.s.admin_pic||'https://i.pravatar.cc/150?img=32';let dec='👑 '+an+' ✅';document.getElementById('hdrName').innerText=dec;document.getElementById('hdrName2').innerText=dec;document.getElementById('hdrPic').src=ap;document.getElementById('hdrPic2').src=ap;document.getElementById('userName').innerText=d.uname||('User '+d.id.slice(-4));document.getElementById('userPic').src=d.upic||'https://i.pravatar.cc/150?img=8';document.getElementById('adminBoxText').innerText=d.s.profile_box||'Loading...';renderTasks(d.tasks||{});});}
function renderTasks(doneTasks){let h='';tasks.forEach((t,i)=>{let isDone=doneTasks[i]!==undefined;let btnText=isDone?'DONE ✅ - 24h পরে আবার':t.btn;let btnColor=isDone?'#475569':t.color;let dis=isDone?'disabled':'';h+='<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ '+t.title+'</div><div>৳'+t.reward+'</div></div><button class="btn" style="background:'+btnColor+';margin-top:10px" '+dis+' onclick="doTask('+i+')">'+btnText+'</button></div>';});document.getElementById('tasksHome').innerHTML=h;document.getElementById('tasksAll').innerHTML=h;}
renderTasks({});load();
</script></body></html>
'''

ADMIN_PAGE = '''
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a1020;color:#fff;font-family:sans-serif;padding:14px;max-width:500px;margin:0 auto;padding-bottom:120px}
.card{background:#151f35;border:1px solid #1e2d4f;border-radius:16px;padding:14px;margin:12px 0}
.label{color:#38bdf8;font-size:12px;margin:10px 0 6px 0}
.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:10px;padding:12px;width:100%;color:#fff}
.btn-save{width:100%;max-width:480px;position:fixed;bottom:12px;left:50%;transform:translateX(-50%);padding:16px;background:linear-gradient(90deg,#22c55e,#16a34a);border:0;border-radius:14px;font-weight:900;color:#fff;z-index:99}
.preview{width:60px;height:60px;border-radius:50%;border:3px solid #22c55e;object-fit:cover}
</style></head><body>
<h2 style="color:#22c55e;text-align:center">✅ FINAL ADMIN PANEL</h2>
<div class="card" style="border:2px solid #22c55e">
<div style="font-weight:900">👑 Header Control - তোমার ছবি + নাম</div>
<div class="label">Header নাম - 👑 + ✅ Auto লাগবে</div>
<input class="input" id="admin_name">
<div style="font-size:13px;margin-top:6px">Preview: <b id="prevName" style="color:#2ef36c">👑 নাম ✅</b></div>
<div class="label">Header ছবির Link - ডান কোনায় দেখাবে</div>
<input class="input" id="admin_pic" placeholder="https://...">
<div style="display:flex;gap:10px;align-items:center;margin-top:8px"><img id="prevPic" class="preview" src=""><span style="font-size:12px;opacity:0.6">imgbb.com থেকে Link নাও</span></div>
</div>
<div class="card" style="border:2px solid #0ea5e9">
<div style="font-weight:900">🎬 Ads Limit Control</div>
<div class="label">দিনে কয়টা Ads - তুমি কমাতে/বাড়াতে পারবে</div>
<input class="input" id="ads_limit" type="number">
</div>
<div class="card" style="border:2px solid #f59e0b">
<div style="font-weight:900;color:#fbbf24">📢 Profile এর নিচের Box Control</div>
<div class="label">Box এর লেখা - Profile এর খালি জায়গায় দেখাবে</div>
<textarea class="input" id="profile_box" rows="4"></textarea>
</div>
<div class="card"><div id="info"></div></div>
<div class="card"><div style="font-weight:900">💸 Live Withdraw</div><div id="wList"></div></div>
<div style="height:80px"></div>
<button class="btn-save" onclick="saveAll()">💾 SAVE ALL - Live করো</button>
<script>
function load(){fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{
document.getElementById('info').innerHTML='Total Users: '+d.total_users+'<br>Token: 11764581 Hidden ✅<br>Ads Limit: '+(d.s.ads_limit||100);
if(d.s.admin_name){document.getElementById('admin_name').value=d.s.admin_name;document.getElementById('prevName').innerText='👑 '+d.s.admin_name+' ✅';}
if(d.s.admin_pic){document.getElementById('admin_pic').value=d.s.admin_pic;document.getElementById('prevPic').src=d.s.admin_pic;}
if(d.s.profile_box) document.getElementById('profile_box').value=d.s.profile_box;
if(d.s.ads_limit) document.getElementById('ads_limit').value=d.s.ads_limit;
let h='';if(d.w.length==0)h='No Withdraw';else d.w.forEach(w=>{h+='<div style="padding:5px;border-bottom:1px solid #222">৳'+w.amt+' - '+w.met+' '+w.num+'</div>';});
document.getElementById('wList').innerHTML=h;
});}
document.getElementById('admin_name').addEventListener('input',e=>{document.getElementById('prevName').innerText='👑 '+e.target.value+' ✅';});
document.getElementById('admin_pic').addEventListener('input',e=>{if(e.target.value.startsWith('http'))document.getElementById('prevPic').src=e.target.value;});
function saveAll(){let data={admin_name:document.getElementById('admin_name').value,admin_pic:document.getElementById('admin_pic').value,profile_box:document.getElementById('profile_box').value,ads_limit:parseInt(document.getElementById('ads_limit').value)||100};fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>{alert('Saved ✅');load();});}
load();
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
