# CLEAN PROFESSIONAL - NO TOKEN SHOW IN USER APP - ONLY ADMIN SEES - 8807178385
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"
ZONE = "11764581"

def load_db():
    if not os.path.exists(DB_FILE):
        d={"users":{"8807178385":{"id":"8807178385","bal":60,"ads":0}},"w":[]}
        with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d)
        return d
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except:
        return {"users":{"8807178385":{"id":"8807178385","bal":60,"ads":0}},"w":[]}

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)

@app.route('/')
def home(): return render_template_string(USER_PAGE)

@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID:
        return f"<center><h3>Admin Only</h3><p>Use /admin?id={ADMIN_ID}</p></center>"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/bal')
def api_bal():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0}
    return jsonify({"bal":db["users"][uid]["bal"],"ads":db["users"][uid]["ads"],"id":uid,"total_users":len(db["users"]),"w":db["w"][-15:][::-1]})

@app.route('/api/add')
def api_add():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0}
    db["users"][uid]["bal"]+=int(request.args.get('amt',2))
    db["users"][uid]["ads"]+=1
    save_db(db)
    return jsonify({"ok":True})

@app.route('/api/wd')
def api_wd():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    amt=int(request.args.get('amt',0))
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0}
    if db["users"][uid]["bal"]<amt: return jsonify({"msg":"Balance কম - Min 1000"})
    db["users"][uid]["bal"]-=amt
    db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"met":request.args.get('met','bKash'),"time":str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg":"Withdraw Success - 24 ঘন্টায় পেমেন্ট"})

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
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #2a3a5f;background:#0b142d;color:#fff;margin-top:10px;outline:none}
.meth{display:flex;gap:8px;margin-top:12px}
.meth div{flex:1;background:#0b142d;border:2px solid #2a3a5f;border-radius:12px;padding:12px;text-align:center;cursor:pointer;font-weight:700}
.meth div.on{border-color:#ff2d7a;background:#1a1430}
</style></head><body>
<div id="p-home">
<div class="hdr"><div style="font-size:16px;font-weight:700">প্রতিদিনের কাজ BD</div><div class="bal">৳ <span id="bh">60</span></div><div style="font-size:13px;opacity:0.7;margin-top:4px">Ads: <span id="adH">0</span>/100</div></div>
<div class="notice"><div style="flex:1"><div style="font-weight:900;font-size:16px">অফিসিয়াল নোটিস</div><div style="font-size:12px;opacity:0.85;margin-top:3px">প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম করুন</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:10px 18px;border-radius:30px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"><img class="on" src="https://picsum.photos/600/300?random=21"><img src="https://picsum.photos/600/300?random=22"><img src="https://picsum.photos/600/300?random=23"><img src="https://picsum.photos/600/300?random=24"><img src="https://picsum.photos/600/300?random=25"><img src="https://picsum.photos/600/300?random=26"></div>
<div class="card"><div style="font-weight:800">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">ADS দেখুন - ৳2 বোনাস</button></div>
<div id="tasksHome"></div>
</div>

<div id="p-tasks" style="display:none">
<div class="hdr"><div style="font-weight:700">প্রতিদিনের কাজ BD</div><div class="bal">৳ <span id="bt">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span id="adT">0</span>/100</div></div>
<div id="tasksAll"></div>
</div>

<div id="p-refer" style="display:none">
<div class="hdr"><div style="font-weight:700">রেফার করুন</div><div class="bal">৳ <span id="br">60</span></div></div>
<div class="card"><div style="font-weight:900">Refer & Earn ৳20</div><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyR()">Copy Link</button></div>
<div class="card"><div style="font-weight:800">📖 কিভাবে রেফার কাজ করে?</div><div style="font-size:13px;opacity:0.8;margin-top:6px;line-height:1.6">১. লিংক Copy করুন<br>২. বন্ধুকে পাঠান<br>৩. প্রতি রেফারে ৳20 বোনাস পাবেন</div></div>
</div>

<div id="p-wallet" style="display:none">
<div class="hdr"><div style="font-weight:700">আমার ওয়ালেট</div><div class="bal">৳ <span id="bw">60</span></div><div style="opacity:0.7;font-size:13px">সর্বনিম্ন উত্তোলন ৳1000</div></div>
<div class="card"><div style="font-weight:900">আমার ব্যালেন্স</div><div style="font-size:38px;font-weight:900;color:#2ef36c">৳ <span id="bw2">60</span></div><div style="opacity:0.6">সর্বনিম্ন ৳1000 হলে তুলতে পারবেন</div></div>
<div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')">bKash</div><div id="m-nagad" onclick="sel('Nagad')">Nagad</div></div><input class="inp" id="wNum" placeholder="Number - 01XXXXXXXXX"><button class="btn" style="background:#2563eb;margin-top:12px" onclick="wd()">Withdraw করুন</button></div>
<div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c;display:flex;gap:6px;align-items:center"><span class="dot"></span>Live Withdraw - সবাই কত তুলছে</div><div style="font-size:11px;opacity:0.6;margin-top:4px">কেউ Withdraw করলেই এখানে দেখাবে</div><div id="liveList" style="margin-top:10px;font-size:13px">এখনো কেউ Withdraw করেনি</div></div>
<div class="card" style="border:1px solid #0ea5e9"><div style="font-weight:900">Withdraw নিয়ম</div><div style="white-space:pre-line;font-size:12px;margin-top:8px;opacity:0.8;line-height:1.6">১. সর্বনিম্ন ৳1000 হলে Withdraw
২. bKash / Nagad Number সঠিক দিন
৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন
৪. ভুল Number দিলে দায় আপনার
৫. একাধিক Account করলে Ban হবে</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">বোনাস Ads দেখুন</button></div>
</div>

<div id="p-profile" style="display:none">
<div class="hdr"><div style="font-weight:700">আমার প্রোফাইল</div><div class="bal">৳ <span id="bp">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span id="adP">0</span>/100</div></div>
<div class="card"><div style="font-weight:900;font-size:16px">আমার প্রোফাইল</div><div style="opacity:0.7;margin-top:4px">ID: <span id="pid">8807178385</span> - Balance ৳<span id="bp2">60</span></div><div style="margin-top:10px;background:#0b142d;border-radius:10px;padding:10px;font-size:13px;line-height:1.6">আপনার প্রোফাইল ভেরিফাইড - সব কাজ ঠিকঠাক চলছে - প্রতিদিন কাজ করুন, ইনকাম করুন</div></div>
<div class="card"><div style="font-weight:900">🎯 আমার কাজের হিসাব</div><div style="margin-top:10px;display:flex;gap:10px"><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#2ef36c" id="adP2">0</div><div style="font-size:11px;opacity:0.6">Ads দেখা</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#0ea5e9" id="bp3">60</div><div style="font-size:11px;opacity:0.6">ব্যালেন্স</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#f59e0b">Active</div><div style="font-size:11px;opacity:0.6">Status</div></div></div></div>
<div class="card" style="border:1px solid #0ea5e9"><div style="font-weight:900">সাপোর্ট সেন্টার</div><div style="font-size:13px;opacity:0.85;margin-top:8px;line-height:1.6">Telegram: @ProtidinerKajBD<br>২৪ ঘণ্টা Support - কোন সমস্যা হলে মেসেজ দিন - আমরা আছি আপনার পাশে</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="window.open('https://t.me','_blank')">Telegram Support - Join</button></div>
<div class="card" style="background:linear-gradient(135deg,#132042,#1e3a5a)"><div style="font-weight:900">✅ ভেরিফাইড একাউন্ট</div><div style="font-size:12px;opacity:0.7;margin-top:6px">আপনার একাউন্ট ভেরিফাইড - সব কিছু ঠিকঠাক আছে - Company Verified ✅</div></div>
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
{title:'YouTube Subscribe',reward:25,link:'https://youtube.com',color:'#dc2626',btn:'Join & Get 25 Tk'},
{title:'Telegram Join',reward:10,link:'https://t.me',color:'#1e40af',btn:'Join & Get 10 Tk'},
{title:'Facebook Follow',reward:15,link:'https://facebook.com',color:'#0ea5e9',btn:'Follow & Get 15 Tk'},
{title:'Website Visit',reward:20,link:'https://google.com',color:'#7c3aed',btn:'Visit & Get 20 Tk'},
{title:'Group Join',reward:20,link:'https://t.me',color:'#0f766e',btn:'Join & Get 20 Tk'},
{title:'Post Like',reward:20,link:'https://facebook.com',color:'#be123c',btn:'Like & Get 20 Tk'}
];
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});window.scrollTo(0,0);}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Link Copied ✅'));}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid+'&amt=2').then(()=>load());});}else{fetch('/api/add?id='+uid+'&amt=2').then(()=>{alert('Ads ৳2 Added ✅');load();});}}
function claim(i){window.open(tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/add?id='+uid+'&amt='+tasks[i].reward).then(()=>{alert('৳'+tasks[i].reward+' Added ✅');load();});},1200);}
function wd(){let amt=document.getElementById('wAmt').value;let num=document.getElementById('wNum').value;if(!amt||!num){alert('Amount & Number লাগবে');return;}fetch('/api/wd?id='+uid+'&amt='+amt+'&num='+num+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
let slIdx=0;setInterval(()=>{let imgs=document.querySelectorAll('#sl img');imgs.forEach(im=>im.classList.remove('on'));slIdx=(slIdx+1)%imgs.length;imgs[slIdx].classList.add('on');},2000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{['bh','bt','br','bw','bw2','bp','bp2','bp3'].forEach(id=>{let el=document.getElementById(id);if(el)el.innerText=d.bal;});['adH','adT','adP','adP2'].forEach(id=>{let el=document.getElementById(id);if(el)el.innerText=d.ads;});document.getElementById('pid').innerText=d.id.slice(0,4)+'****'+d.id.slice(-3);document.getElementById('refLink').value=location.origin+'/?ref='+d.id;let live='';if(d.w.length==0)live='এখনো কেউ Withdraw করেনি';else d.w.forEach(w=>{live+='<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">💸 ID:'+w.id.slice(-4)+' - ৳'+w.amt+' - '+w.met+' - '+w.time+'</div>';});document.getElementById('liveList').innerHTML=live;});}
function renderTasks(){let h='';tasks.forEach((t,i)=>{h+='<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ '+t.title+'</div><div>৳'+t.reward+'</div></div><button class="btn" style="background:'+t.color+';margin-top:10px" onclick="claim('+i+')">'+t.btn+'</button></div>';});document.getElementById('tasksHome').innerHTML=h;document.getElementById('tasksAll').innerHTML=h;}
renderTasks();load();
</script></body></html>
'''

ADMIN_PAGE = '''
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a1020;color:#fff;font-family:sans-serif;padding:14px;max-width:500px;margin:0 auto;padding-bottom:100px}
.card{background:#151f35;border:1px solid #1e2d4f;border-radius:16px;padding:14px;margin:12px 0}
</style></head><body>
<h2 style="color:#22c55e;text-align:center">✅ ADMIN PANEL - CLEAN VERSION<br>Token: 11764581 - ID: 8807178385</h2>
<div class="card"><div id="info" style="font-weight:800;line-height:1.6"></div></div>
<div class="card"><div style="font-weight:900">💸 Live Withdraw - Admin Only</div><div id="wList"></div></div>
<script>
function load(){fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{
document.getElementById('info').innerHTML='Company Connected ✅<br>Token: 11764581 - Zone: 11764581<br>Admin ID: 8807178385<br>Users: '+d.total_users+'<br>Balance: ৳'+d.bal;
let h='';if(d.w.length==0)h='No Withdraw Yet';else d.w.forEach(w=>{h+='<div style="padding:6px;border-bottom:1px solid #222">৳'+w.amt+' - '+w.met+' '+w.num+' - '+w.time+'</div>';});
document.getElementById('wList').innerHTML=h;
});}
load();setInterval(load,4000);
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
