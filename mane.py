# FINAL - 5 PAGE EXACT SCREENSHOT - LIVE BLINK + SLIDER 2s + FULL ADMIN CONTROL - 8807178385
import os, json, time
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"
TOKEN = "11764581"

def default_db():
    return {
        "users": {"8807178385":{"id":"8807178385","name":"User 8807178385","bal":60,"ads":0,"ref_c":0,"w_total":0,"join":str(datetime.now())[:19]}},
        "withdraws": [],
        "settings": {
            "app_title": f"প্রতিদিনের কাজ BD - {TOKEN} - {ADMIN_ID}",
            "bal_text": "60",
            "ads_count": f"Ads: 0/100 - {TOKEN}",
            "notice_title": f"অফিসিয়াল নোটিস - {TOKEN}",
            "notice_desc": f"প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন - Token {TOKEN} - Admin {ADMIN_ID}",
            "slider": [
                {"img":"https://i.ibb.co.com/nsT0W7r6/gaming1.jpg","link":"https://t.me"},
                {"img":"https://i.ibb.co.com/0y0L0p0/rocket.png","link":"https://youtube.com"},
                {"img":"https://picsum.photos/600/300?random=1","link":"https://facebook.com"},
                {"img":"https://picsum.photos/600/300?random=2","link":"https://t.me"},
                {"img":"https://picsum.photos/600/300?random=3","link":"https://google.com"},
                {"img":"https://picsum.photos/600/300?random=4","link":"https://t.me"}
            ],
            "mini_title": "স্পেশাল অফার - Mini Boy Ads",
            "mini_btn": f"ADS দেখুন - Token {TOKEN}",
            "zone_text": f"Zone: {TOKEN} - Token {TOKEN} - Admin {ADMIN_ID}",
            "wallet_title": f"Wallet - {ADMIN_ID}",
            "wallet_bal": "60",
            "wallet_min": f"Min: ৳1000 - Token {TOKEN}",
            "bkash_text": f"bKash - {TOKEN}",
            "nagad_text": f"Nagad - {TOKEN}",
            "withdraw_btn": f"Withdraw - {TOKEN}",
            "live_title": "Live Withdraw - সবাই কত তুলছে - Auto",
            "live_desc": f"কেউ Withdraw করলেই এখানে Auto ভাসবে - Token {TOKEN} - Admin {ADMIN_ID}",
            "live_empty": f"এখনো কেউ Withdraw করেনি - Token {TOKEN}",
            "rules_title": f"Withdraw নিয়ম - Admin থেকে Change করতে পারবেন - {TOKEN}",
            "rules_text": f"১. Minimum ৳1000 হলে Withdraw দিতে পারবেন\n২. bKash / Nagad Number সঠিক ভাবে দিন\n৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন\n৪. ভুল Number দিলে টাকা পাবেন না, দায় আপনার\n৫. একাধিক Account করলে Ban হবেন\n\nএই লেখাটি Admin Panel থেকে যেকোনো সময় Change করতে পারবেন - Token {TOKEN} - Admin ID {ADMIN_ID}",
            "warning": f"সতর্কতা: একাধিক Account করলে Ban হবেন। Fake Refer করলে Balance 0 করে দেওয়া হবে। ভুল Number এ টাকা গেলে Admin দায়ী নয়। - Admin {ADMIN_ID} - Token {TOKEN}",
            "mini_ad_btn2": f"Mini Boy Ad দেখুন - {TOKEN}",
            "refer_title": f"Refer & Earn ৳20 - {TOKEN}",
            "refer_desc": f"কিভাবে রেফার কাজ করে? - {TOKEN}\nআপনার লিংক শেয়ার করুন - প্রতি রেফারে ৳20 পাবেন - বন্ধু 60 টাকা বোনাস পাবে - Admin {ADMIN_ID}",
            "profile_title": f"Profile - {ADMIN_ID} - {TOKEN}",
            "profile_sub": f"ID: {ADMIN_ID} - Balance ৳60",
            "support_title": f"সাপোর্ট সেন্টার - {ADMIN_ID}",
            "support_desc": f"যেকোনো সমস্যায় যোগাযোগ করুন - Telegram: @ProtidinerKajBD - Admin ID {ADMIN_ID} - Token {TOKEN}"
        },
        "tasks": [
            {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","btn":f"Join & Get 25 Tk - {TOKEN}"},
            {"title":"Telegram Join","reward":10,"link":"https://t.me","color":"#1e40af","btn":f"Join & Get 10 Tk - {TOKEN}"},
            {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9","btn":f"Follow & Get 15 Tk - {TOKEN}"},
            {"title":"Website Visit","reward":20,"link":"https://google.com","color":"#7c3aed","btn":f"Visit & Get 20 Tk - {TOKEN}"},
            {"title":"Group Join","reward":20,"link":"https://t.me","color":"#0f766e","btn":f"Join & Get 20 Tk - {TOKEN}"},
            {"title":"Post Like","reward":20,"link":"https://facebook.com","color":"#be123c","btn":f"Like & Get 20 Tk - {TOKEN}"},
            {"title":"Post Share","reward":20,"link":"https://facebook.com","color":"#166534","btn":f"Share & Get 20 Tk - {TOKEN}"},
            {"title":"Comment","reward":20,"link":"https://facebook.com","color":"#2563eb","btn":f"Comment & Get 20 Tk - {TOKEN}"},
            {"title":"Refer 3 Friend","reward":20,"link":"https://t.me","color":"#d97706","btn":f"Refer & Get 20 Tk - {TOKEN}"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d=default_db(); save_db(d); return d
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)
def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":60,"ads":0,"ref_c":0,"w_total":0,"join":str(datetime.now())[:19]}
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID: return f"Need?id={ADMIN_ID}"
    return render_template_string(ADMIN_HTML)

@app.route('/api/all')
def api_all():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid)
    return jsonify({"u":u,"s":db["settings"],"tasks":db["tasks"],"withdraws":db["withdraws"][-10:][::-1],"total_u":len(db["users"])})

@app.route('/api/ads')
def api_ads():
    db=load_db(); u=get_user(db,request.args.get('id')); u["bal"]+=2; u["ads"]+=1; save_db(db)
    return jsonify({"msg":"Ads দেখা হয়েছে - ৳2"})

@app.route('/api/task')
def api_task():
    db=load_db(); idx=int(request.args.get('idx')); uid=request.args.get('id'); u=get_user(db,uid)
    u["bal"]+=db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg":f"৳{db['tasks'][idx]['reward']} Added"})

@app.route('/api/withdraw')
def api_wd():
    db=load_db(); uid=request.args.get('id'); amt=int(request.args.get('amount',0)); num=request.args.get('number'); met=request.args.get('method','bKash')
    u=get_user(db,uid)
    if amt<1000: return jsonify({"msg":"Min 1000"})
    if u["bal"]<amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt; u["w_total"]+=amt
    db["withdraws"].append({"uid":uid,"name":u["name"],"amount":amt,"number":num,"method":met,"time":str(datetime.now())[:19]})
    save_db(db)
    return jsonify({"msg":"Withdraw Success - Admin দেখবে"})

@app.route('/api/admin/db')
def adb(): return jsonify(load_db())
@app.route('/api/admin/save',methods=['POST'])
def asave():
    db=load_db(); j=request.json
    db["settings"].update(j.get("settings",{}))
    if "tasks" in j: db["tasks"]=j["tasks"]
    if "slider" in j: db["settings"]["slider"]=j["slider"]
    save_db(db)
    return jsonify({"msg":"Saved"})

HTML = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}
body{background:#0a1229;color:#fff;max-width:430px;margin:0 auto;padding-bottom:80px}
.header{background:linear-gradient(135deg,#1e3a8a,#0f172a);border-radius:0 0 24px 24px;padding:16px;position:relative}
.bal{font-size:54px;font-weight:900;color:#22c55e;line-height:1}
.notice{background:linear-gradient(135deg,#1e3a8a,#0f766e);margin:12px;border-radius:18px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:1px solid #22c55e;position:relative}
.live-dot{width:16px;height:16px;background:#22c55e;border-radius:50%;animation:blink 1s infinite;box-shadow:0 0 12px #22c55e}
@keyframes blink{0%{opacity:1;transform:scale(1)}50%{opacity:0.3;transform:scale(1.2)}100%{opacity:1;transform:scale(1)}}
.live-green{width:12px;height:12px;background:#22c55e;border-radius:50%;display:inline-block;animation:blink 0.8s infinite}
.slider{margin:12px;border-radius:18px;overflow:hidden;height:170px;position:relative;border:1px solid #1e3a5f;background:#000}
.slider img{width:100%;height:100%;object-fit:cover;position:absolute;left:0;top:0;opacity:0;transition:opacity 0.8s}
.slider img.active{opacity:1}
.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px;z-index:2}
.dots span{width:8px;height:8px;background:rgba(255,255,255,0.4);border-radius:50%;transition:all 0.3s}
.dots span.active{width:28px;background:#0ea5e9;border-radius:10px}
.card{background:#121e36;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.task{background:#121e36;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f;display:flex;flex-direction:column;gap:10px}
.btn{width:100%;padding:14px;border:0;border-radius:14px;font-weight:800;color:#fff;cursor:pointer;font-size:15px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:11px;cursor:pointer;padding:6px}
.btm div.on{color:#22c55e}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:12px;border-radius:12px;border:1px solid #2a3a5f;background:#0f172a;color:#fff;margin-top:8px}
.meth{display:flex;gap:10px;margin-top:10px}
.meth div{flex:1;background:#0f172a;border:2px solid #2a3a5f;border-radius:14px;padding:14px;text-align:center;cursor:pointer}
.meth div.on{border-color:#ec4899}
</style></head><body>

<div id="p-home">
<div class="header"><div style="display:flex;justify-content:space-between;align-items:start"><div><div style="font-size:15px;line-height:1.3" id="appTitle"></div><div class="bal" style="margin-top:6px">৳ <span id="balH">60</span></div><div style="margin-top:6px;opacity:0.8;font-size:14px" id="adsCount"></div></div><img src="https://i.pravatar.cc/150?img=12" style="width:56px;height:56px;border-radius:50%;border:2px solid #fff"></div></div>

<div class="notice"><div style="flex:1"><div style="font-weight:900;font-size:16px" id="noticeTitle"></div><div style="font-size:13px;opacity:0.9;margin-top:4px" id="noticeDesc"></div></div><div style="background:#22c55e;color:#000;font-weight:900;padding:12px 18px;border-radius:50%;display:flex;align-items:center;gap:8px"><span class="live-dot"></span>LIVE</div></div>

<div class="slider" id="sliderBox"><div id="sliderImgs"></div><div class="dots" id="dots"></div></div>

<div class="card"><div style="display:flex;gap:8px;align-items:center;font-weight:800"><span>🎬</span><span style="color:#f97316">🔥</span><span id="miniTitle"></span></div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="watchAds()" id="miniBtn"></button><div style="font-size:12px;opacity:0.6;margin-top:8px" id="zoneText"></div></div>

<div id="tasksHome"></div>
</div>

<div id="p-tasks" style="display:none">
<div class="header"><div id="appTitle2" style="font-size:15px"></div><div class="bal" style="margin-top:6px">৳ <span id="balT">60</span></div><div style="margin-top:6px" id="adsCount2"></div></div>
<div id="tasksAll"></div>
</div>

<div id="p-refer" style="display:none">
<div class="header"><div id="appTitle3" style="font-size:15px"></div><div class="bal">৳ <span id="balR">60</span></div><div style="margin-top:6px" id="adsCount3"></div></div>
<div class="card"><div style="font-weight:900" id="referTitle"></div><input class="inp" id="referLink" readonly style="margin-top:10px"><button class="btn" style="background:#2563eb;margin-top:10px" onclick="copyRefer()">Copy Link</button></div>
<div class="card"><div style="font-weight:900" id="referDescTitle"></div><div style="margin-top:8px;white-space:pre-line;font-size:13px;opacity:0.8" id="referDesc"></div></div>
</div>

<div id="p-wallet" style="display:none">
<div class="header"><div id="appTitle4" style="font-size:15px"></div><div class="bal">৳ <span id="balW">60</span></div><div style="margin-top:6px" id="adsCount4"></div></div>
<div class="card"><div style="font-weight:900" id="walletTitle"></div><div style="font-size:42px;font-weight:900;color:#22c55e">৳ <span id="walletBal">60</span></div><div style="opacity:0.7" id="walletMin"></div></div>
<div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')"><div style="font-size:12px">📷</div><div style="font-weight:800;margin-top:4px" id="bkashText"></div></div><div id="m-nagad" onclick="sel('Nagad')"><div style="font-size:12px;color:#f97316">💳 নগদ</div><div style="font-weight:800;margin-top:4px" id="nagadText"></div></div></div><input class="inp" id="wNum" placeholder="Number - 01XXXXXXXXX"><button class="btn" style="background:#2563eb;margin-top:10px" onclick="doWithdraw()" id="withdrawBtn"></button></div>
<div class="card" style="border:2px solid #22c55e"><div style="font-weight:900;color:#22c55e;display:flex;gap:8px;align-items:center"><span class="live-green"></span><span>💸</span><span id="liveTitle"></span></div><div style="font-size:12px;opacity:0.7;margin-top:6px" id="liveDesc"></div><div style="margin-top:10px;font-weight:600" id="liveEmpty"></div><div id="liveList"></div></div>
<div class="card" style="border:2px solid #0ea5e9"><div style="font-weight:900" id="rulesTitle"></div><div style="white-space:pre-line;font-size:13px;margin-top:10px;opacity:0.8" id="rulesText"></div><div style="background:#0f172a;border:1px dashed #334155;border-radius:12px;padding:10px;margin-top:10px;font-size:12px" id="warningText"></div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="watchAds()" id="miniAdBtn2"></button></div>
</div>

<div id="p-profile" style="display:none">
<div class="header"><div id="appTitle5" style="font-size:15px"></div><div class="bal">৳ <span id="balP">60</span></div><div style="margin-top:6px" id="adsCount5"></div></div>
<div class="card"><div style="font-weight:900" id="profileTitle"></div><div style="opacity:0.7;margin-top:4px" id="profileSub"></div></div>
<div class="card"><div style="font-weight:900" id="supportTitle"></div><div style="margin-top:8px;font-size:13px;opacity:0.8;white-space:pre-line" id="supportDesc"></div></div>
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
let slideIndex=0;
let sliderData=[];
function go(p){
['home','tasks','refer','wallet','profile'].forEach(x=>{
let e=document.getElementById('p-'+x);
if(e)e.style.display=x==p?'block':'none';
let b=document.getElementById('b-'+x);
if(b)b.classList.toggle('on',x==p);
});
}
function sel(m){
method=m;
document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));
document.getElementById('m-'+m.toLowerCase()).classList.add('on');
}
function copyRefer(){
navigator.clipboard.writeText(document.getElementById('referLink').value).then(()=>alert('Link Copied - Working'));
}
function watchAds(){
if(typeof show_11764581!=='undefined'){
show_11764581().then(()=>{
fetch('/api/ads?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});
});
}else{
fetch('/api/ads?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});
}
}
function claimTask(i){
fetch('/api/all?id='+uid).then(r=>r.json()).then(d=>{
window.open(d.tasks[i].link,'_blank');
setTimeout(()=>{
fetch('/api/task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});
},1500);
});
}
function doWithdraw(){
let amt=document.getElementById('wAmt').value;
let num=document.getElementById('wNum').value;
if(!amt||!num){alert('Amount & Number Required');return;}
fetch('/api/withdraw?id='+uid+'&amount='+amt+'&number='+num+'&method='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});
}
function startSlider(){
if(sliderData.length==0)return;
let box=document.getElementById('sliderImgs');
let dots=document.getElementById('dots');
box.innerHTML='';
dots.innerHTML='';
sliderData.forEach((s,i)=>{
let img=document.createElement('img');
img.src=s.img;
img.className=i==0?'active':'';
img.onclick=()=>window.open(s.link,'_blank');
box.appendChild(img);
let dot=document.createElement('span');
dot.className=i==0?'active':'';
dot.onclick=()=>{slideIndex=i;showSlide();};
dots.appendChild(dot);
});
setInterval(()=>{
slideIndex=(slideIndex+1)%sliderData.length;
showSlide();
},2000);
}
function showSlide(){
let imgs=document.querySelectorAll('#sliderImgs img');
let dotSpans=document.querySelectorAll('#dots span');
imgs.forEach((im,i)=>{im.classList.toggle('active',i==slideIndex);});
dotSpans.forEach((d,i)=>{d.classList.toggle('active',i==slideIndex);});
}
function load(){
fetch('/api/all?id='+uid).then(r=>r.json()).then(d=>{
let s=d.s;
let u=d.u;
sliderData=s.slider;
document.getElementById('appTitle').innerText=s.app_title;
document.getElementById('appTitle2').innerText=s.app_title;
document.getElementById('appTitle3').innerText=s.app_title;
document.getElementById('appTitle4').innerText=s.app_title;
document.getElementById('appTitle5').innerText=s.app_title;
document.getElementById('balH').innerText=u.bal;
document.getElementById('balT').innerText=u.bal;
document.getElementById('balR').innerText=u.bal;
document.getElementById('balW').innerText=u.bal;
document.getElementById('balP').innerText=u.bal;
document.getElementById('walletBal').innerText=u.bal;
document.getElementById('adsCount').innerText='Ads: '+u.ads+'/100 - 11764581';
document.getElementById('adsCount2').innerText='Ads: '+u.ads+'/100 - 11764581';
document.getElementById('adsCount3').innerText='Ads: '+u.ads+'/100 - 11764581';
document.getElementById('adsCount4').innerText='Ads: '+u.ads+'/100 - 11764581';
document.getElementById('adsCount5').innerText='Ads: '+u.ads+'/100 - 11764581';
document.getElementById('noticeTitle').innerText=s.notice_title;
document.getElementById('noticeDesc').innerText=s.notice_desc;
document.getElementById('miniTitle').innerText=s.mini_title;
document.getElementById('miniBtn').innerText=s.mini_btn;
document.getElementById('zoneText').innerText=s.zone_text;
document.getElementById('walletTitle').innerText=s.wallet_title;
document.getElementById('walletMin').innerText=s.wallet_min;
document.getElementById('bkashText').innerText=s.bkash_text;
document.getElementById('nagadText').innerText=s.nagad_text;
document.getElementById('withdrawBtn').innerText=s.withdraw_btn;
document.getElementById('liveTitle').innerText=s.live_title;
document.getElementById('liveDesc').innerText=s.live_desc;
document.getElementById('liveEmpty').innerText=d.withdraws.length==0?s.live_empty:'';
document.getElementById('rulesTitle').innerText=s.rules_title;
document.getElementById('rulesText').innerText=s.rules_text;
document.getElementById('warningText').innerText=s.warning;
document.getElementById('miniAdBtn2').innerText=s.mini_ad_btn2;
document.getElementById('referTitle').innerText=s.refer_title;
document.getElementById('referDescTitle').innerText='📖 কিভাবে রেফার কাজ করে? - 11764581';
document.getElementById('referDesc').innerText=s.refer_desc;
document.getElementById('profileTitle').innerText=s.profile_title;
document.getElementById('profileSub').innerText='ID: '+u.id+' - Balance ৳'+u.bal;
document.getElementById('supportTitle').innerText=s.support_title;
document.getElementById('supportDesc').innerText=s.support_desc;
document.getElementById('referLink').value='https://t.me/YourBot?start='+u.id;

let tHtml='';
d.tasks.forEach((t,i)=>{
tHtml+='<div class="task"><div style="display:flex;justify-content:space-between"><div>⭐ '+t.title+'</div><div>৳'+t.reward+'</div></div><button class="btn" style="background:'+t.color+'" onclick="claimTask('+i+')">'+t.btn+'</button></div>';
});
document.getElementById('tasksHome').innerHTML=tHtml;
document.getElementById('tasksAll').innerHTML=tHtml;

let liveHtml='';
d.withdraws.forEach(w=>{
liveHtml+='<div style="padding:8px 0;border-bottom:1px solid #1e2d4f">💸 '+w.name+' - ID:'+w.uid.slice(-4)+' - '+w.method+' '+w.number+' - ৳'+w.amount+' - '+w.time+'</div>';
});
document.getElementById('liveList').innerHTML=liveHtml;

if(document.getElementById('sliderImgs').children.length==0){startSlider();}
});
}
load();
setInterval(load,5000);
</script></body></html>
'''

ADMIN_HTML = '''
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{background:#0f172a;color:#fff;padding:12px;max-width:900px;margin:0 auto;font-family:sans-serif}
.card{background:#1e293b;padding:14px;border-radius:12px;margin:12px 0;border:1px solid #334155}
input,textarea{width:100%;padding:10px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#fff;margin:6px 0}
textarea{min-height:80px}
button{padding:10px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}
label{font-size:11px;color:#38bdf8;margin-top:8px;display:block}
</style></head><body>
<h2 style="color:#22c55e">ADMIN FULL CONTROL - 8807178385 - Token 11764581</h2>
<p style="opacity:0.7">এখানে যা লিখবে App এ Live হবে - সবুজ বাতি মিটমিট, Slider, সব লেখা, সব লিংক</p>

<div class="card"><h3>📝 সব লেখা Control</h3>
<label>App Title (উপরে)</label><input id="app_title">
<label>Notice Title</label><input id="notice_title">
<label>Notice Desc</label><textarea id="notice_desc"></textarea>
<label>Mini Title - Special Offer</label><input id="mini_title">
<label>Mini Button Text</label><input id="mini_btn">
<label>Zone Text</label><input id="zone_text">
<label>Wallet Title</label><input id="wallet_title">
<label>Wallet Min Text</label><input id="wallet_min">
<label>bKash Text</label><input id="bkash_text">
<label>Nagad Text</label><input id="nagad_text">
<label>Withdraw Button</label><input id="withdraw_btn">
<label>Live Title</label><input id="live_title">
<label>Live Desc</label><input id="live_desc">
<label>Live Empty Text</label><input id="live_empty">
<label>Rules Title</label><input id="rules_title">
<label>Rules Text (Withdraw নিয়ম)</label><textarea id="rules_text" style="min-height:140px"></textarea>
<label>Warning Text</label><textarea id="warning"></textarea>
<label>Mini Ad Button 2</label><input id="mini_ad_btn2">
<label>Refer Title</label><input id="refer_title">
<label>Refer Desc</label><textarea id="refer_desc"></textarea>
<label>Profile Title</label><input id="profile_title">
<label>Support Title</label><input id="support_title">
<label>Support Desc</label><textarea id="support_desc"></textarea>
</div>

<div class="card"><h3>🖼️ উপরে Slider - 6 টা ছবি - 2 সেকেন্ড পর পর - Auto</h3>
<div id="sliderEdit"></div>
<button style="background:#22c55e;width:100%;margin-top:10px" onclick="addSlide()">+ Add Slider Image</button>
</div>

<div class="card"><h3>📋 Tasks - সব লিংক + টাকা + বাটন Text Control</h3>
<div id="tasksEdit"></div>
<button style="background:#22c55e;width:100%" onclick="addTask()">+ Add Task</button>
</div>

<div class="card"><h3>💸 Live Withdraw List - কে কত তুলছে</h3>
<div id="withdrawList"></div>
</div>

<div class="card" style="background:linear-gradient(90deg,#22c55e,#16a34a)"><button style="background:#fff;color:#16a34a;width:100%;padding:16px;font-weight:900;font-size:18px" onclick="saveAll()">💾 SAVE ALL - LIVE করো</button></div>

<script>
let DB={};
function load(){
fetch('/api/admin/db?id=8807178385').then(r=>r.json()).then(d=>{
DB=d;
for(let k in d.settings){
if(k=='slider')continue;
let el=document.getElementById(k);
if(el)el.value=d.settings[k];
}
let sHtml='';
d.settings.slider.forEach((s,i)=>{
sHtml+='<div style="background:#0f172a;padding:10px;border-radius:10px;margin:8px 0"><b>Image '+(i+1)+' - 2s পর পর আসবে</b><button style="float:right;background:#dc2626;padding:4px 8px" onclick="delSlide('+i+')">Delete</button><label>Image URL</label><input id="slide_img_'+i+'" value="'+s.img+'"><label>Link (Click করলে যাবে)</label><input id="slide_link_'+i+'" value="'+s.link+'"><img src="'+s.img+'" style="width:100%;height:100px;object-fit:cover;border-radius:8px;margin-top:6px"></div>';
});
document.getElementById('sliderEdit').innerHTML=sHtml;

let tHtml='';
d.tasks.forEach((t,i)=>{
tHtml+='<div style="background:#0f172a;padding:10px;border-radius:10px;margin:8px 0"><b>Task '+(i+1)+'</b><button style="float:right;background:#dc2626;padding:4px 8px" onclick="delTask('+i+')">Delete</button><label>Title</label><input id="t_title_'+i+'" value="'+t.title+'"><label>Reward ৳</label><input id="t_reward_'+i+'" type="number" value="'+t.reward+'"><label>Link</label><input id="t_link_'+i+'" value="'+t.link+'"><label>Button Color</label><input id="t_color_'+i+'" value="'+t.color+'"><label>Button Text</label><input id="t_btn_'+i+'" value="'+t.btn+'"></div>';
});
document.getElementById('tasksEdit').innerHTML=tHtml;

let wHtml='';
d.withdraws.slice(-20).reverse().forEach(w=>{
wHtml+='<div style="padding:6px;border-bottom:1px solid #334155">ID:'+w.uid+' - '+w.method+' '+w.number+' - ৳'+w.amount+' - '+w.time+'</div>';
});
document.getElementById('withdrawList').innerHTML=wHtml||'No Withdraw Yet';
});
}
function addSlide(){DB.settings.slider.push({img:"https://picsum.photos/600/300?random="+Date.now(),link:"https://t.me"});saveTemp();load();}
function delSlide(i){DB.settings.slider.splice(i,1);saveTemp();load();}
function addTask(){DB.tasks.push({title:"New Task",reward:20,link:"https://t.me",color:"#2563eb",btn:"Join & Get 20 Tk - 11764581"});load();}
function delTask(i){DB.tasks.splice(i,1);saveTemp();load();}
function saveTemp(){
let slider=[];
for(let i=0;i<DB.settings.slider.length;i++){
let img=document.getElementById('slide_img_'+i);
if(!img)continue;
slider.push({img:img.value,link:document.getElementById('slide_link_'+i).value});
}
let tasks=[];
for(let i=0;i<DB.tasks.length;i++){
let ti=document.getElementById('t_title_'+i);
if(!ti)continue;
tasks.push({title:ti.value,reward:parseInt(document.getElementById('t_reward_'+i).value)||20,link:document.getElementById('t_link_'+i).value,color:document.getElementById('t_color_'+i).value,btn:document.getElementById('t_btn_'+i).value});
}
fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:DB.settings,tasks:tasks,slider:slider})});
}
function saveAll(){
let settings={};
let keys=["app_title","notice_title","notice_desc","mini_title","mini_btn","zone_text","wallet_title","wallet_min","bkash_text","nagad_text","withdraw_btn","live_title","live_desc","live_empty","rules_title","rules_text","warning","mini_ad_btn2","refer_title","refer_desc","profile_title","support_title","support_desc"];
keys.forEach(k=>{
let el=document.getElementById(k);
if(el)settings[k]=el.value;
});
let slider=[];
for(let i=0;i<DB.settings.slider.length;i++){
let img=document.getElementById('slide_img_'+i);
if(!img)continue;
slider.push({img:img.value,link:document.getElementById('slide_link_'+i).value});
}
let tasks=[];
for(let i=0;i<DB.tasks.length;i++){
let ti=document.getElementById('t_title_'+i);
if(!ti)continue;
tasks.push({title:ti.value,reward:parseInt(document.getElementById('t_reward_'+i).value)||20,link:document.getElementById('t_link_'+i).value,color:document.getElementById('t_color_'+i).value,btn:document.getElementById('t_btn_'+i).value});
}
fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:settings,tasks:tasks,slider:slider})}).then(r=>r.json()).then(x=>{alert('✅ Saved - App এ Live - সবুজ বাতি মিটমিট করছে - Slider 2s পর পর');load();});
}
load();
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
