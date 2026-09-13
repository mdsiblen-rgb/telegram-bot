import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    default = {
        "users": {}, "w": [],
        "s": {
            "admin_name": "Protidiner Kaj BD",
            "admin_pic": "https://i.pravatar.cc/150?img=32",
            "profile_box": "✅ Official Telegram - @ProtidinerKajBD",
            "ads_limit": 100, "ads_reward": 2, "refer_bonus": 20,
            "notice_title": "Official Notice",
            "notice_sub": "Watch Ads Daily - Earn Upto ৳500",
            "slider": [
                "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600",
                "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600",
                "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"
            ],
            "tasks": [
                {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "Join & Get 25 Tk"},
                {"title": "Telegram Join", "reward": 10, "link": "https://t.me", "color": "#1e40af", "btn": "Join & Get 10 Tk"},
                {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "Follow & Get 15 Tk"},
                {"title": "Website Visit", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "Visit & Get 20 Tk"},
                {"title": "Group Join", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "Join & Get 20 Tk"},
                {"title": "Post Like", "reward": 20, "link": "https://facebook.com", "color": "#be123c", "btn": "Like & Get 20 Tk"}
            ]
        }
    }
    if not os.path.exists(DB_FILE):
        return default
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def get_user(db,uid):
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"bal":60,"ads":0,"uname":f"User {uid[-4:]}","upic":"","tasks":{}}
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(USER_PAGE)

@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID: return "Admin Only?id=8807178385"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/bal')
def bal():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); save_db(db)
    return jsonify({"bal":u["bal"],"ads":u["ads"],"id":uid,"uname":u["uname"],"upic":u["upic"],"tasks":u["tasks"],"w":db["w"][-10:][::-1],"s":db["s"]})

@app.route('/api/add')
def add():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid)
    if u["ads"]>=db["s"]["ads_limit"]: return jsonify({"ok":False})
    u["bal"]+=db["s"]["ads_reward"]; u["ads"]+=1; save_db(db); return jsonify({"ok":True})

@app.route('/api/claim')
def claim():
    uid=request.args.get('id',ADMIN_ID); tid=request.args.get('tid','0'); db=load_db(); u=get_user(db,uid)
    if tid in u["tasks"]: return jsonify({"ok":False,"msg":"DONE ✅"})
    u["tasks"][tid]=str(datetime.now()); u["bal"]+=db["s"]["tasks"][int(tid)]["reward"]; save_db(db)
    return jsonify({"ok":True,"msg":f"৳{db['s']['tasks'][int(tid)]['reward']} Added"})

@app.route('/api/wd')
def wd():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); amt=int(request.args.get('amt',0))
    if u["bal"]<amt or amt<1000: return jsonify({"msg":"Min 1000 Tk"})
    u["bal"]-=amt; db["w"].append({"id":uid,"amt":amt,"time":str(datetime.now())[:16]}); save_db(db); return jsonify({"msg":"Withdraw Success"})

@app.route('/api/save',methods=['POST'])
def save():
    db=load_db(); data=request.json
    if "tasks" in data: db["s"]["tasks"]=data["tasks"]
    for k in ["admin_name","admin_pic","profile_box","ads_limit","ads_reward","refer_bonus","notice_title","notice_sub","slider"]:
        if k in data: db["s"][k]=data[k]
    save_db(db); return jsonify({"msg":"Saved"})

USER_PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#081028;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px 18px 16px 18px}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:22px;font-weight:900;letter-spacing:0.5px;display:flex;align-items:center;gap:6px}
.hdr-pic{width:52px;height:52px;border-radius:50%;border:3px solid #2ef36c;object-fit:cover;box-shadow:0 0 12px #2ef36c66}
.bal{font-size:54px;font-weight:900;color:#2ef36c;margin-top:6px;line-height:1}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.live-btn{background:#2ef36c;color:#000;font-weight:900;padding:10px 22px;border-radius:30px;display:flex;gap:8px;align-items:center;font-size:14px;box-shadow:0 0 15px #2ef36c99}
.dot{width:12px;height:12px;background:#00ff00;border-radius:50%;animation:blink 0.7s infinite;box-shadow:0 0 8px #00ff00}
@keyframes blink{0%{opacity:1;transform:scale(1)}50%{opacity:0.2;transform:scale(0.6)}100%{opacity:1;transform:scale(1)}}
.slider{margin:12px;border-radius:18px;height:185px;position:relative;overflow:hidden;background:#000;border:1px solid #1e2d4f}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer;font-size:14px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0 6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
</style></head><body>
<!-- HOME PAGE - একদম তোমার Screenshot এর মত -->
<div id="p-home">
<div class="hdr"><div class="hdr-top"><div class="hdr-name"><span>👑</span><span id="hn">Protidiner Kaj BD</span><span>✅</span></div><img id="hp" class="hdr-pic" src="https://i.pravatar.cc/150?img=32"></div><div class="bal">৳ <span class="balV">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span class="adsV">0</span>/100</div></div>
<div class="notice"><div><div id="nt" style="font-weight:900;font-size:16px">Official Notice</div><div id="ns" style="font-size:12px;opacity:0.85;margin-top:2px">Watch Ads Daily - Earn Upto ৳500</div></div><div class="live-btn"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"></div>
<div id="homeTasks"></div>
</div>

<!-- TASKS PAGE - HOME এর সাথে 100% SAME -->
<div id="p-tasks" style="display:none">
<div class="hdr"><div class="hdr-top"><div class="hdr-name"><span>👑</span><span id="hn2">Protidiner Kaj BD</span><span>✅</span></div><img id="hp2" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span class="adsV">0</span>/100</div></div>
<div class="notice"><div><div style="font-weight:900">Official Notice</div><div style="font-size:12px;opacity:0.85">Watch Ads Daily - Earn Upto ৳500</div></div><div class="live-btn"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl2"></div>
<div id="tasksPage"></div>
</div>

<div id="p-refer" style="display:none"><div class="hdr"><div>Refer - ৳ <span class="balV">60</span></div></div><div class="card"><div id="pb" style="font-size:13px;opacity:0.8"></div></div></div>
<div id="p-wallet" style="display:none"><div class="hdr"><div>Wallet - ৳ <span class="balV">60</span></div></div><div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c">🟢 Live Withdraw</div><div id="live" style="margin-top:8px"></div></div></div>
<div id="p-profile" style="display:none"><div class="hdr" style="text-align:center"><div class="hdr-name" style="justify-content:center"><span>👑</span><span class="hn3">Protidiner Kaj BD</span><span>✅</span></div><div class="bal" style="justify-content:center">৳ <span class="balV">60</span></div></div></div>

<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(()=>load());});}else{fetch('/api/add?id='+uid).then(()=>load());}}
function doTask(i,l){window.open(l,'_blank');setTimeout(()=>{fetch('/api/claim?id='+uid+'&tid='+i).then(r=>r.json()).then(j=>{alert(j.msg);load();});},1500);}
let sI=0;setInterval(()=>{document.querySelectorAll('.slider img').forEach((im,idx)=>{im.classList.remove('on');});let imgs=document.querySelectorAll('#sl img');if(imgs.length){sI=(sI+1)%imgs.length;imgs.forEach((im,ii)=>{if(ii==sI)im.classList.add('on');});let imgs2=document.querySelectorAll('#sl2 img');imgs2.forEach((im,ii)=>{if(ii==sI)im.classList.add('on');});}},3000);
function buildTasks(d){let h=`<div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">ADS দেখুন - ৳${d.s.ads_reward} বোনাস</button></div>`;d.s.tasks.forEach((t,i)=>{let done=d.tasks[i]!==undefined;h+=`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><div>⭐ ${t.title}</div><div style="font-weight:900">৳${t.reward}</div></div><button class="btn" style="background:${done?'#555':t.color};margin-top:12px" onclick="doTask(${i},'${t.link}')">${done?'DONE ✅':t.btn}</button></div>`;});return h;}
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{
document.querySelectorAll('.balV').forEach(e=>e.innerText=d.bal);document.querySelectorAll('.adsV').forEach(e=>e.innerText=d.ads);
document.getElementById('hn').innerText=d.s.admin_name;document.getElementById('hn2').innerText=d.s.admin_name;
document.querySelectorAll('.hn3').forEach(e=>e.innerText=d.s.admin_name);
document.getElementById('hp').src=d.s.admin_pic;document.getElementById('hp2').src=d.s.admin_pic;
document.getElementById('nt').innerText=d.s.notice_title;document.getElementById('ns').innerText=d.s.notice_sub;
document.getElementById('pb').innerText=d.s.profile_box||'';
let sl=document.getElementById('sl');let sl2=document.getElementById('sl2');sl.innerHTML='';sl2.innerHTML='';
d.s.slider.forEach((src,i)=>{sl.innerHTML+=`<img class="${i==0?'on':''}" src="${src}">`;sl2.innerHTML+=`<img class="${i==0?'on':''}" src="${src}">`;});
let tasksHTML=buildTasks(d);
document.getElementById('homeTasks').innerHTML=tasksHTML;
document.getElementById('tasksPage').innerHTML=tasksHTML;
let lv=d.w.length==0?'<div style="opacity:0.6;font-size:13px">এখনো কেউ Withdraw করেনি</div>':'';d.w.forEach(w=>{lv+=`<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">💸 ID:${w.id.slice(-4)} - ৳${w.amt} - ${w.time}</div>`;});document.getElementById('live').innerHTML=lv;
});}load();
</script></body></html>
"""

ADMIN_PAGE = """
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#081028;color:#fff;font-family:sans-serif;padding:10px;max-width:500px;margin:auto;padding-bottom:120px}
.card{background:#132042;border:1px solid #1e2d4f;border-radius:14px;padding:12px;margin:10px 0}
.label{color:#38bdf8;font-size:11px;margin:8px 0 3px 0;font-weight:700}
.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:8px;padding:11px;width:100%;color:#fff;margin-bottom:5px}
.btn-save{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);width:95%;max-width:480px;padding:16px;background:linear-gradient(90deg,#22c55e,#16a34a);border:0;border-radius:14px;font-weight:900;color:#fff;font-size:16px}
.tab{display:flex;gap:5px;overflow:auto;margin:10px 0}
.tab div{padding:10px 14px;background:#132042;border-radius:8px;white-space:nowrap;cursor:pointer;border:1px solid #1e2d4f;font-size:13px}
.tab div.on{background:#22c55e;color:#000;font-weight:900}
</style></head><body>
<h2 style="text-align:center;color:#22c55e">👑 SUPER ADMIN - A-Z Control</h2>
<div class="tab"><div class="on" id="t1" onclick="tab(1)">Header & Profile</div><div id="t2" onclick="tab(2)">Tasks Link Edit</div><div id="t3" onclick="tab(3)">Slider & Notice</div></div>

<div id="p1">
<div class="card"><div style="font-weight:900">👑 Header - ডান কোনার ছবি + নাম</div>
<div class="label">নাম - English - বড় করে - (Example: Protidiner Kaj BD) - সামনে 👑 পিছনে ✅ Auto আসবে</div><input class="input" id="admin_name">
<div class="label">ডান কোনার ছবি Link - এইখানে তোমার ছবির Link বসাও</div><input class="input" id="admin_pic" placeholder="https://...jpg">
<div class="label">Profile Box Text</div><textarea class="input" id="profile_box" rows="2"></textarea>
</div>
<div class="card"><div style="font-weight:900">💰 Money Control</div><div class="label">Ads Reward ৳</div><input class="input" id="ads_reward" type="number"><div class="label">Ads Limit</div><input class="input" id="ads_limit" type="number"><div class="label">Refer Bonus ৳</div><input class="input" id="refer_bonus" type="number"></div>
</div>

<div id="p2" style="display:none"><div class="card"><div style="font-weight:900">✅ Tasks - Link System - এখানে সব Link বসাবা</div><div id="tasksEdit"></div></div></div>

<div id="p3" style="display:none">
<div class="card"><div style="font-weight:900">📢 Notice + LIVE বাতি</div><div class="label">Notice Title</div><input class="input" id="notice_title"><div class="label">Notice Sub</div><input class="input" id="notice_sub"></div>
<div class="card"><div style="font-weight:900">🖼️ Slider 3 টা ছবি Link</div><div class="label">Slider Image 1</div><input class="input" id="sl1"><div class="label">Slider Image 2</div><input class="input" id="sl2"><div class="label">Slider Image 3</div><input class="input" id="sl3"></div>
</div>

<button class="btn-save" onclick="saveAll()">💾 SAVE ALL - সাথে সাথে Live</button>
<script>
let curTasks=[];
function tab(n){[1,2,3].forEach(i=>{document.getElementById('p'+i).style.display=i==n?'block':'none';document.getElementById('t'+i).classList.toggle('on',i==n);});}
function load(){
fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{
document.getElementById('admin_name').value=d.s.admin_name;document.getElementById('admin_pic').value=d.s.admin_pic;
document.getElementById('notice_title').value=d.s.notice_title;document.getElementById('notice_sub').value=d.s.notice_sub;
document.getElementById('profile_box').value=d.s.profile_box||'';
document.getElementById('ads_reward').value=d.s.ads_reward;document.getElementById('ads_limit').value=d.s.ads_limit;document.getElementById('refer_bonus').value=d.s.refer_bonus||20;
document.getElementById('sl1').value=d.s.slider[0]||'';document.getElementById('sl2').value=d.s.slider[1]||'';document.getElementById('sl3').value=d.s.slider[2]||'';
curTasks=d.s.tasks;let h='';
curTasks.forEach((t,i)=>{
h+=`<div style="border:1px solid #2a3a5f;border-radius:10px;padding:10px;margin:8px 0;background:#0a1229">
<b>Task ${i+1} - ${t.title}</b>
<div class="label">Title</div><input class="input" id="tt_${i}" value="${t.title}">
<div class="label">Reward ৳</div><input class="input" id="tr_${i}" type="number" value="${t.reward}">
<div class="label">Link - তোমার YouTube / Telegram / FB Link এখানে</div><input class="input" id="tl_${i}" value="${t.link}">
<div class="label">Button Text</div><input class="input" id="tb_${i}" value="${t.btn}">
</div>`;
});
document.getElementById('tasksEdit').innerHTML=h;
});
}
function saveAll(){
let tasks=[];
for(let i=0;i<6;i++){let el=document.getElementById('tt_'+i);if(!el)continue;tasks.push({title:document.getElementById('tt_'+i).value,reward:parseInt(document.getElementById('tr_'+i).value)||20,link:document.getElementById('tl_'+i).value,color:curTasks[i].color,btn:document.getElementById('tb_'+i).value});}
let data={
admin_name:document.getElementById('admin_name').value,
admin_pic:document.getElementById('admin_pic').value,
notice_title:document.getElementById('notice_title').value,
notice_sub:document.getElementById('notice_sub').value,
profile_box:document.getElementById('profile_box').value,
ads_reward:parseInt(document.getElementById('ads_reward').value)||2,
ads_limit:parseInt(document.getElementById('ads_limit').value)||100,
refer_bonus:parseInt(document.getElementById('refer_bonus').value)||20,
slider:[document.getElementById('sl1').value,document.getElementById('sl2').value,document.getElementById('sl3').value],
tasks:tasks
};
fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>{alert('✅ Saved - এখন App Refresh করো - সব Live');load();});
}
load();
</script></body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
