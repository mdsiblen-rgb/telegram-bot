import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    tasks20 = [
        {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "Join & Get 25 Tk"},
        {"title": "Telegram Join", "reward": 10, "link": "https://t.me", "color": "#1e40af", "btn": "Join & Get 10 Tk"},
        {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "Follow & Get 15 Tk"},
        {"title": "Website Visit", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "Visit & Get 20 Tk"},
        {"title": "Group Join", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "Join & Get 20 Tk"},
        {"title": "Post Like", "reward": 20, "link": "https://facebook.com", "color": "#be123c", "btn": "Like & Get 20 Tk"},
        {"title": "YouTube Like", "reward": 10, "link": "https://youtube.com", "color": "#dc2626", "btn": "Like 10 Tk"},
        {"title": "Insta Follow", "reward": 15, "link": "https://instagram.com", "color": "#e11d48", "btn": "Follow 15 Tk"},
        {"title": "Twitter Follow", "reward": 15, "link": "https://x.com", "color": "#111", "btn": "Follow 15 Tk"},
        {"title": "App Download", "reward": 30, "link": "https://google.com", "color": "#16a34a", "btn": "Download 30 Tk"},
        {"title": "Video Watch", "reward": 10, "link": "https://youtube.com", "color": "#f59e0b", "btn": "Watch 10 Tk"},
        {"title": "Refer Share", "reward": 10, "link": "https://t.me", "color": "#0ea5e9", "btn": "Share 10 Tk"},
        {"title": "Daily Check", "reward": 5, "link": "https://google.com", "color": "#7c3aed", "btn": "Check 5 Tk"},
        {"title": "Survey Complete", "reward": 50, "link": "https://google.com", "color": "#059669", "btn": "Complete 50 Tk"},
        {"title": "Game Play", "reward": 20, "link": "https://google.com", "color": "#7c2d12", "btn": "Play 20 Tk"},
        {"title": "Quiz Answer", "reward": 15, "link": "https://google.com", "color": "#0f766e", "btn": "Answer 15 Tk"},
        {"title": "Link Click", "reward": 5, "link": "https://google.com", "color": "#4f46e5", "btn": "Click 5 Tk"},
        {"title": "Comment Task", "reward": 10, "link": "https://facebook.com", "color": "#be123c", "btn": "Comment 10 Tk"},
        {"title": "Share Post", "reward": 10, "link": "https://facebook.com", "color": "#1e40af", "btn": "Share 10 Tk"},
        {"title": "Review Task", "reward": 25, "link": "https://google.com", "color": "#15803d", "btn": "Review 25 Tk"},
    ]
    default = {"users": {}, "s": {"admin_name": "Protidiner Kaj BD","admin_pic": "https://i.pravatar.cc/150?img=32","ads_limit": 100,"ads_reward": 2,"notice_title": "Official Notice","notice_sub": "Watch Ads Daily - Earn Upto ৳500","slider": ["https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600","https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"],"tasks": tasks20}}
    if not os.path.exists(DB_FILE): return default
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except: return default

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False)
def get_user(db,uid):
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0,"tasks":{}}
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(PAGE)
@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID: return "Admin?id=8807178385"
    return render_template_string(ADMIN)
@app.route('/api/bal')
def bal():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); save_db(db); return jsonify({"bal":u["bal"],"ads":u["ads"],"tasks":u["tasks"],"s":db["s"]})
@app.route('/api/add')
def add():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); u["bal"]+=db["s"]["ads_reward"]; u["ads"]+=1; save_db(db); return jsonify({"ok":True})
@app.route('/api/claim')
def claim():
    uid=request.args.get('id',ADMIN_ID); tid=request.args.get('tid','0'); db=load_db(); u=get_user(db,uid)
    if tid in u["tasks"]: return jsonify({"msg":"DONE"})
    u["tasks"][tid]="1"; u["bal"]+=db["s"]["tasks"][int(tid)]["reward"]; save_db(db); return jsonify({"ok":True})
@app.route('/api/save',methods=['POST'])
def save():
    db=load_db(); d=request.json
    for k in d: db["s"][k]=d[k]
    save_db(db); return jsonify({"ok":True})

PAGE="""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#081028;color:#fff;max-width:430px;margin:auto;padding-bottom:85px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#162a5e);border-radius:0 0 26px 26px;padding:18px 18px 22px 18px;position:relative}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:23px;font-weight:800;display:flex;align-items:center;gap:8px}
.hdr-pic{width:58px;height:58px;border-radius:50%;border:3px solid #2ef36c;object-fit:cover}
.bal{font-size:56px;font-weight:900;color:#2ef36c;margin-top:10px;line-height:1}
.bal-sub{opacity:0.8;font-size:14px;margin-top:4px}
.notice{background:linear-gradient(90deg,#1e3a8a,#0f4c5c);margin:12px;border-radius:18px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.live-btn{background:#2ef36c;color:#000;font-weight:900;padding:12px 22px;border-radius:28px;display:flex;gap:8px;align-items:center;box-shadow:0 0 12px #2ef36c}
.live-dot{width:16px;height:16px;border:3px solid #004d00;border-radius:50%;background:transparent;animation:blink 0.7s infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:20px;height:200px;position:relative;overflow:hidden;background:#000;border:1px solid #1e2d4f}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer;font-size:14px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0 6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.tasks-grid{display:grid;grid-template-columns:1fr;gap:0}
</style></head><body>

<div id="p-home">
<div class="hdr"><div class="hdr-top"><div class="hdr-name"><span>👑</span><span id="hn">Protidiner Kaj BD</span><span style="background:#22c55e;color:#fff;border-radius:4px;padding:2px 4px;font-size:18px">✅</span></div><img id="hp" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div><div class="bal-sub">Ads: <span class="adsV">0</span>/100</div></div>
<div class="notice"><div><div style="font-weight:900;font-size:16px">Official Notice</div><div style="font-size:13px;opacity:0.9">Watch Ads Daily - Earn Upto ৳500</div></div><div class="live-btn"><span class="live-dot"></span>LIVE</div></div>
<div class="slider" id="sl"></div>
<div id="homeTasks"></div>
</div>

<div id="p-tasks" style="display:none">
<div class="hdr"><div class="hdr-top"><div class="hdr-name"><span>👑</span><span id="hn2">Protidiner Kaj BD</span><span style="background:#22c55e;color:#fff;border-radius:4px;padding:2px 4px;font-size:18px">✅</span></div><img id="hp2" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div><div class="bal-sub">Ads: <span class="adsV">0</span>/100</div></div>
<div class="notice"><div><div style="font-weight:900;font-size:16px">Official Notice</div><div style="font-size:13px;opacity:0.9">Watch Ads Daily - Earn Upto ৳500</div></div><div class="live-btn"><span class="live-dot"></span>LIVE</div></div>
<div class="slider" id="sl2"></div>
<div id="tasksPage"></div>
</div>

<div id="p-refer" style="display:none"><div class="hdr">Refer</div></div>
<div id="p-wallet" style="display:none"><div class="hdr">Wallet</div></div>
<div id="p-profile" style="display:none"><div class="hdr">Profile</div></div>

<div class="btm">
<div id="b-home" onclick="go('home')"><span>🏠</span>Home</div>
<div class="on" id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div>
<div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div>
<div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div>
<div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{let pe=document.getElementById('p-'+x);if(pe)pe.style.display=x==p?'block':'none';let be=document.getElementById('b-'+x);if(be)be.classList.toggle('on',x==p);});}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(()=>load());});}else{fetch('/api/add?id='+uid).then(()=>load());}}
function doTask(i,l){window.open(l,'_blank');setTimeout(()=>{fetch('/api/claim?id='+uid+'&tid='+i).then(()=>load());},1000);}
let sI=0;setInterval(()=>{let a=document.querySelectorAll('#sl img');let b=document.querySelectorAll('#sl2 img');if(!a.length)return;a.forEach(e=>e.classList.remove('on'));b.forEach(e=>e.classList.remove('on'));sI=(sI+1)%a.length;a[sI].classList.add('on');if(b[sI])b[sI].classList.add('on');},3000);
function load(){
fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{
document.querySelectorAll('.balV').forEach(e=>e.innerText=d.bal);
document.querySelectorAll('.adsV').forEach(e=>e.innerText=d.ads);
document.getElementById('hn').innerText=d.s.admin_name;
document.getElementById('hn2').innerText=d.s.admin_name;
document.getElementById('hp').src=d.s.admin_pic;
document.getElementById('hp2').src=d.s.admin_pic;
let sl=document.getElementById('sl');let sl2=document.getElementById('sl2');sl.innerHTML='';sl2.innerHTML='';
d.s.slider.forEach((s,i)=>{sl.innerHTML+=`<img class="${i==0?'on':''}" src="${s}">`;sl2.innerHTML+=`<img class="${i==0?'on':''}" src="${s}">`;});
let html=`<div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">ADS দেখুন - ৳${d.s.ads_reward} বোনাস</button></div>`;
d.s.tasks.forEach((t,i)=>{let done=d.tasks[i]!==undefined;html+=`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><div>⭐ ${t.title}</div><div style="font-weight:900">৳${t.reward}</div></div><button class="btn" style="background:${done?'#555':t.color};margin-top:12px" onclick="doTask(${i},'${t.link}')">${done?'DONE ✅':t.btn}</button></div>`;});
document.getElementById('homeTasks').innerHTML=html;
document.getElementById('tasksPage').innerHTML=html;
});}
load();
go('tasks');
</script></body></html>
"""
ADMIN="""<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#081028;color:#fff;font-family:sans-serif;padding:10px;max-width:500px;margin:auto;padding-bottom:120px}.card{background:#132042;border-radius:14px;padding:12px;margin:10px 0;border:1px solid #1e2d4f}.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:8px;padding:11px;width:100%;color:#fff;margin:5px 0}</style></head><body>
<h2 style="text-align:center;color:#2ef36c">ADMIN - সব Change করতে পারবা</h2>
<div class="card">Name<input class="input" id="admin_name">Pic Link<input class="input" id="admin_pic"></div>
<div class="card"><div id="t"></div></div>
<button style="position:fixed;bottom:10px;left:50%;transform:translateX(-50%);width:95%;max-width:480px;padding:16px;background:#22c55e;border:0;border-radius:14px;font-weight:900;color:#fff" onclick="saveAll()">SAVE ALL - Live হবে</button>
<script>
let cur=[];
function load(){fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{document.getElementById('admin_name').value=d.s.admin_name;document.getElementById('admin_pic').value=d.s.admin_pic;cur=d.s.tasks;let h='';cur.forEach((t,i)=>{h+=`<div style="border:1px solid #2a3a5f;padding:8px;margin:5px 0;border-radius:8px">Task ${i+1}<input class="input" id="tt_${i}" value="${t.title}"><input class="input" id="tl_${i}" value="${t.link}"><input class="input" id="tr_${i}" value="${t.reward}"></div>`;});document.getElementById('t').innerHTML=h;});}
function saveAll(){let tasks=[];for(let i=0;i<cur.length;i++){tasks.push({title:document.getElementById('tt_'+i).value,link:document.getElementById('tl_'+i).value,reward:parseInt(document.getElementById('tr_'+i).value)||20,color:cur[i].color,btn:cur[i].btn});}let data={admin_name:document.getElementById('admin_name').value,admin_pic:document.getElementById('admin_pic').value,tasks:tasks};fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>alert('Saved'));}load();
</script></body></html>
"""
if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
