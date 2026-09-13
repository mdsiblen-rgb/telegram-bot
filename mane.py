# FINAL VORPUR - 5 PAGE - NO BLANK - ADMIN 8807178385 - TOKEN 11764581
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

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
def home():
    return render_template_string(PAGE)

@app.route('/admin')
def adm():
    if request.args.get('id')!=ADMIN_ID:
        return f"Need?id={ADMIN_ID} - Your Admin ID {ADMIN_ID} Active"
    return f"Admin Panel OK - ID {ADMIN_ID} - Token 11764581 - Company Connected - Users {len(load_db()['users'])} - Withdraws {len(load_db()['w'])}"

@app.route('/api/bal')
def api_bal():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0}
    return jsonify(db["users"][uid])

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
    if db["users"][uid]["bal"]<amt: return jsonify({"msg":"Balance কম"})
    db["users"][uid]["bal"]-=amt
    db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"met":request.args.get('met','bKash'),"time":str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg":"Withdraw Success"})

PAGE = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#08122e;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0e1a3f);border-radius:0 0 26px 26px;padding:18px}
.bal{font-size:48px;font-weight:900;color:#2ef36c}
.notice{background:linear-gradient(90deg,#1a3a8a,#0f6b6b);margin:12px;border-radius:16px;padding:14px;display:flex;justify-content:space-between;border:2px solid #2ef36c}
.dot{width:12px;height:12px;background:#2ef36c;border-radius:50%;animation:blk 0.8s infinite;box-shadow:0 0 8px #2ef36c}
@keyframes blk{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:16px;height:170px;position:relative;overflow:hidden;background:#000;border:1px solid #234}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.7s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:16px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:13px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:12px;border-radius:10px;border:1px solid #2a3a5f;background:#0f172a;color:#fff;margin-top:8px}
.meth{display:flex;gap:8px;margin-top:10px}
.meth div{flex:1;background:#0f172a;border:2px solid #2a3a5f;border-radius:12px;padding:10px;text-align:center;cursor:pointer}
.meth div.on{border-color:#ec4899}
</style></head><body>

<div id="p-home">
<div class="hdr"><div style="font-size:14px">প্রতিদিনের কাজ BD - 11764581 - 8807178385</div><div class="bal">৳ <span id="bh">60</span></div><div style="font-size:13px;opacity:0.7">Ads: <span id="adH">0</span>/100 - 11764581</div></div>
<div class="notice"><div><div style="font-weight:900">অফিসিয়াল নোটিস - 11764581</div><div style="font-size:12px;opacity:0.8">প্রতিদিন Ads দেখুন - ৳500 ইনকাম - Token 11764581</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:8px 14px;border-radius:20px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"><img class="on" src="https://picsum.photos/600/300?random=1"><img src="https://picsum.photos/600/300?random=2"><img src="https://picsum.photos/600/300?random=3"><img src="https://picsum.photos/600/300?random=4"><img src="https://picsum.photos/600/300?random=5"><img src="https://picsum.photos/600/300?random=6"></div>
<div class="card"><div style="font-weight:800">🎬 স্পেশাল অফার - Mini Boy Ads - 11764581</div><button class="btn" style="background:#0ea5e9;margin-top:10px" onclick="ads()">ADS দেখুন - Token 11764581 - ৳2</button><div style="font-size:11px;opacity:0.5;margin-top:6px">Zone: 11764581 - Token 11764581 - Admin 8807178385</div></div>
<div id="tasksHome"></div>
</div>

<div id="p-tasks" style="display:none">
<div class="hdr"><div style="font-size:14px">প্রতিদিনের কাজ BD - 11764581</div><div class="bal">৳ <span id="bt">60</span></div><div style="font-size:13px;opacity:0.7">Ads: <span id="adT">0</span>/100</div></div>
<div id="tasksAll"></div>
</div>

<div id="p-refer" style="display:none">
<div class="hdr"><div style="font-size:14px">প্রতিদিনের কাজ BD - Refer</div><div class="bal">৳ <span id="br">60</span></div></div>
<div class="card"><div style="font-weight:900">Refer & Earn ৳20 - 11764581</div><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:10px" onclick="copyR()">Copy Link</button></div>
<div class="card"><div style="font-weight:800">📖 কিভাবে রেফার কাজ করে?</div><div style="font-size:13px;opacity:0.8;margin-top:6px">১. লিংক Copy করুন - ২. বন্ধুকে পাঠান - ৩. প্রতি রেফারে ৳20 পাবেন - Token 11764581 - Admin 8807178385</div></div>
</div>

<div id="p-wallet" style="display:none">
<div class="hdr"><div style="font-size:14px">Wallet - 8807178385</div><div class="bal">৳ <span id="bw">60</span></div><div style="font-size:13px;opacity:0.7">Min: ৳1000 - Token 11764581</div></div>
<div class="card"><div style="font-weight:900">Wallet - 8807178385</div><div style="font-size:36px;font-weight:900;color:#2ef36c">৳ <span id="bw2">60</span></div><div style="opacity:0.6">Min: ৳1000 - Token 11764581</div></div>
<div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')"><b>bKash - 11764581</b></div><div id="m-nagad" onclick="sel('Nagad')"><b>Nagad - 11764581</b></div></div><input class="inp" id="wNum" placeholder="Number - 01XXXXXXXXX"><button class="btn" style="background:#2563eb;margin-top:10px" onclick="wd()">Withdraw - 11764581</button></div>
<div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c;display:flex;gap:6px"><span class="dot"></span>Live Withdraw - সবাই কত তুলছে - Auto</div><div style="font-size:11px;opacity:0.6;margin-top:4px">কেউ Withdraw করলেই এখানে Auto ভাসবে - Token 11764581</div><div id="liveList" style="margin-top:10px;font-size:13px">এখনো কেউ Withdraw করেনি - Token 11764581</div></div>
<div class="card" style="border:2px solid #0ea5e9"><div style="font-weight:900">Withdraw নিয়ম - Admin থেকে Change - 11764581</div><div style="white-space:pre-line;font-size:12px;margin-top:8px;opacity:0.8">১. Minimum ৳1000 হলে Withdraw
২. bKash / Nagad Number সঠিক দিন
৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট
৪. ভুল Number দিলে দায় আপনার
৫. একাধিক Account Ban
Admin 8807178385 - Token 11764581</div><div style="background:#0f172a;border:1px dashed #334155;border-radius:10px;padding:8px;margin-top:8px;font-size:11px">সতর্কতা: একাধিক Account Ban - Fake Refer Balance 0 - Admin 8807178385</div><button class="btn" style="background:#0ea5e9;margin-top:10px" onclick="ads()">Mini Boy Ad দেখুন - 11764581</button></div>
</div>

<div id="p-profile" style="display:none">
<div class="hdr"><div style="font-size:14px">Profile - 8807178385 - 11764581</div><div class="bal">৳ <span id="bp">60</span></div><div style="font-size:13px;opacity:0.7">Ads: <span id="adP">0</span>/100</div></div>
<div class="card"><div style="font-weight:900">Profile - 8807178385 - 11764581</div><div style="opacity:0.7">ID: <span id="pid">8807178385</span> - Balance ৳<span id="bp2">60</span></div></div>
<div class="card"><div style="font-weight:900">সাপোর্ট সেন্টার - 8807178385</div><div style="font-size:13px;opacity:0.8;margin-top:6px">Telegram: @ProtidinerKajBD - Admin ID 8807178385 - Token 11764581 - ২৪ ঘণ্টা Support</div></div>
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
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Link Copied'));}
function ads(){
if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid+'&amt=2').then(()=>loadBal());});}
else{fetch('/api/add?id='+uid+'&amt=2').then(()=>{alert('Ads ৳2 Added');loadBal();});}
}
function claim(i){window.open(tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/add?id='+uid+'&amt='+tasks[i].reward).then(()=>{alert('৳'+tasks[i].reward+' Added');loadBal();});},1200);}
function wd(){
let amt=document.getElementById('wAmt').value;
let num=document.getElementById('wNum').value;
if(!amt||!num){alert('Amount & Number লাগবে');return;}
fetch('/api/wd?id='+uid+'&amt='+amt+'&num='+num+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);loadBal();});
}
function loadBal(){
fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{
['bh','bt','br','bw','bw2','bp','bp2'].forEach(id=>{let el=document.getElementById(id);if(el)el.innerText=d.bal;});
['adH','adT','adP'].forEach(id=>{let el=document.getElementById(id);if(el)el.innerText=d.ads;});
document.getElementById('pid').innerText=d.id;
document.getElementById('refLink').value=location.origin+'/?ref='+d.id;
});
}
let slIdx=0;
setInterval(()=>{
let imgs=document.querySelectorAll('#sl img');
imgs.forEach(im=>im.classList.remove('on'));
slIdx=(slIdx+1)%imgs.length;
imgs[slIdx].classList.add('on');
},2000);
function renderTasks(){
let h='';
tasks.forEach((t,i)=>{
h+='<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ '+t.title+'</div><div>৳'+t.reward+'</div></div><button class="btn" style="background:'+t.color+';margin-top:8px" onclick="claim('+i+')">'+t.btn+'</button></div>';
});
document.getElementById('tasksHome').innerHTML=h;
document.getElementById('tasksAll').innerHTML=h;
}
renderTasks();
loadBal();
document.getElementById('refLink').value=location.origin+'/?ref='+uid;
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
