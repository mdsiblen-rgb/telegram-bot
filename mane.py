import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    default = {"users": {}, "w": [], "s": {"admin_name": "Protidiner Kaj BD","admin_pic": "https://i.pravatar.cc/150?img=32","inbox_text": "📢 Official Channel Join করুন - প্রতিদিন Update","ads_limit": 100,"ads_reward": 2,"notice_title": "Official Notice","notice_sub": "Watch Ads Daily - Earn Upto ৳500","slider": ["https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600","https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"],"official_links": [{"title": "Official Telegram","link": "https://t.me","color": "#0ea5e9"},{"title": "Official YouTube","link": "https://youtube.com","color": "#dc2626"},{"title": "Official Facebook","link": "https://facebook.com","color": "#1e40af"}],"tasks": [{"title": "YouTube Subscribe","reward": 25,"link": "https://youtube.com","color": "#dc2626","btn": "Join & Get 25 Tk"},{"title": "Telegram Join","reward": 10,"link": "https://t.me","color": "#1e40af","btn": "Join & Get 10 Tk"},{"title": "Facebook Follow","reward": 15,"link": "https://facebook.com","color": "#0ea5e9","btn": "Follow & Get 15 Tk"},{"title": "Website Visit","reward": 20,"link": "https://google.com","color": "#7c3aed","btn": "Visit & Get 20 Tk"},{"title": "Group Join","reward": 20,"link": "https://t.me","color": "#0f766e","btn": "Join & Get 20 Tk"},{"title": "Post Like","reward": 20,"link": "https://facebook.com","color": "#be123c","btn": "Like & Get 20 Tk"}]}}
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
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); save_db(db)
    return jsonify({"bal":u["bal"],"ads":u["ads"],"id":uid,"tasks":u["tasks"],"s":db["s"]})
@app.route('/api/add')
def add():
    uid=request.args.get('id',ADMIN_ID); db=load_db(); u=get_user(db,uid); u["bal"]+=db["s"]["ads_reward"]; u["ads"]+=1; save_db(db); return jsonify({"ok":True})
@app.route('/api/claim')
def claim():
    uid=request.args.get('id',ADMIN_ID); tid=request.args.get('tid','0'); db=load_db(); u=get_user(db,uid)
    if tid in u["tasks"]: return jsonify({"msg":"DONE"})
    u["tasks"][tid]="1"; u["bal"]+=db["s"]["tasks"][int(tid)]["reward"]; save_db(db); return jsonify({"msg":"Added"})
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
body{background:#081028;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:22px;font-weight:900;display:flex;gap:8px;align-items:center}
.tick-box{background:#bbf7d0;color:#065f46;font-weight:900;font-size:20px;width:32px;height:28px;display:flex;justify-content:center;align-items:center;border-radius:6px;border:2px solid #22c55e}
.hdr-pic{width:54px;height:54px;border-radius:50%;border:3px solid #2ef36c}
.bal{font-size:54px;font-weight:900;color:#2ef36c}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.live-btn{background:#bbf7d0;color:#065f46;font-weight:900;padding:10px 22px;border-radius:30px;display:flex;gap:10px;align-items:center;border:2px solid #22c55e;box-shadow:0 0 15px #bbf7d0}
.live-dot{width:14px;height:14px;background:#065f46;border:2px solid #fff;border-radius:50%;animation:blinkLive 0.6s infinite;box-shadow:0 0 8px #065f46}
@keyframes blinkLive{0%{opacity:1;transform:scale(1)}50%{opacity:0.15;transform:scale(0.6)}100%{opacity:1;transform:scale(1.3)}}
.slider{margin:12px;border-radius:18px;height:185px;position:relative;overflow:hidden}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:800;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inbox{background:linear-gradient(90deg,#0f172a,#132042);border:2px dashed #2ef36c;margin:12px;border-radius:14px;padding:14px}
</style></head><body>
<div id="p-home"><div class="hdr"><div class="hdr-top"><div class="hdr-name"><span>👑</span><span id="hn">Protidiner Kaj BD</span><span class="tick-box">✔</span></div><img id="hp" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div></div>
<div class="notice"><div><div style="font-weight:900">Official Notice</div><div style="font-size:12px">Watch Ads Daily - Upto ৳500</div></div><div class="live-btn"><span class="live-dot"></span>LIVE</div></div>
<div class="slider" id="sl"></div><div class="inbox" id="inbox"></div><div id="official"></div><div id="homeTasks"></div></div>
<div id="p-tasks" style="display:none"><div class="hdr"><div class="hdr-top"><div class="hdr-name"><span>👑</span><span id="hn2">Protidiner Kaj BD</span><span class="tick-box">✔</span></div><img id="hp2" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div></div>
<div class="notice"><div><div style="font-weight:900">Official Notice</div><div style="font-size:12px">Watch Ads Daily</div></div><div class="live-btn"><span class="live-dot"></span>LIVE</div></div>
<div class="slider" id="sl2"></div><div class="inbox" id="inbox2"></div><div id="official2"></div><div id="tasksPage"></div></div>
<div id="p-refer" style="display:none"><div class="hdr">Refer</div></div><div id="p-wallet" style="display:none"><div class="hdr">Wallet - ৳ <span class="balV">60</span></div></div><div id="p-profile" style="display:none"><div class="hdr">Profile - ৳ <span class="balV">60</span></div></div>
<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(()=>load());});}else{fetch('/api/add?id='+uid).then(()=>load());}}
function doTask(i,l){window.open(l,'_blank');setTimeout(()=>{fetch('/api/claim?id='+uid+'&tid='+i).then(()=>load());},1000);}
let sI=0;setInterval(()=>{let a=document.querySelectorAll('#sl img');let b=document.querySelectorAll('#sl2 img');if(!a.length)return;a.forEach(e=>e.classList.remove('on'));b.forEach(e=>e.classList.remove('on'));sI=(sI+1)%a.length;a[sI].classList.add('on');b[sI].classList.add('on');},3000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{
document.querySelectorAll('.balV').forEach(e=>e.innerText=d.bal);
document.getElementById('hn').innerText=d.s.admin_name;document.getElementById('hn2').innerText=d.s.admin_name;
document.getElementById('hp').src=d.s.admin_pic;document.getElementById('hp2').src=d.s.admin_pic;
document.getElementById('inbox').innerText=d.s.inbox_text;document.getElementById('inbox2').innerText=d.s.inbox_text;
let sl=document.getElementById('sl');let sl2=document.getElementById('sl2');sl.innerHTML='';sl2.innerHTML='';
d.s.slider.forEach((s,i)=>{sl.innerHTML+=`<img class="${i==0?'on':''}" src="${s}">`;sl2.innerHTML+=`<img class="${i==0?'on':''}" src="${s}">`;});
let off='';d.s.official_links.forEach(o=>{off+=`<div class="card" style="border-left:5px solid ${o.color}"><div style="display:flex;justify-content:space-between"><div>🔗 ${o.title}</div><button class="btn" style="width:auto;padding:8px 14px;background:${o.color}" onclick="window.open('${o.link}','_blank')">Join</button></div></div>`;});
document.getElementById('official').innerHTML=off;document.getElementById('official2').innerHTML=off;
let h=`<div class="card"><div style="font-weight:900">🎬 বোনাস Ads - ৳${d.s.ads_reward}</div><button class="btn" style="background:#0ea5e9;margin-top:10px" onclick="ads()">ADS দেখুন</button></div>`;
d.s.tasks.forEach((t,i)=>{let done=d.tasks[i]!==undefined;h+=`<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div>৳${t.reward}</div></div><button class="btn" style="background:${done?'#555':t.color};margin-top:10px" onclick="doTask(${i},'${t.link}')">${done?'DONE ✅':t.btn}</button></div>`;});
document.getElementById('homeTasks').innerHTML=h;document.getElementById('tasksPage').innerHTML=h;
});}load();
</script></body></html>
"""
ADMIN="""<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#081028;color:#fff;font-family:sans-serif;padding:10px;max-width:500px;margin:auto;padding-bottom:120px}.card{background:#132042;border:1px solid #1e2d4f;border-radius:14px;padding:12px;margin:10px 0}.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:8px;padding:11px;width:100%;color:#fff;margin:5px 0}.btn-save{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);width:95%;max-width:480px;padding:16px;background:#22c55e;border:0;border-radius:14px;font-weight:900;color:#fff}</style></head><body>
<h2 style="text-align:center;color:#22c55e">ADMIN A-Z</h2>
<div class="card">Header<input class="input" id="admin_name">Pic<input class="input" id="admin_pic"></div>
<div class="card">Inbox Box - লিখতে পারবা<textarea class="input" id="inbox_text" rows="3"></textarea></div>
<div class="card">Official Link 1 Title<input class="input" id="ot0">Link<input class="input" id="ol0">Link 2 Title<input class="input" id="ot1">Link<input class="input" id="ol1">Link 3 Title<input class="input" id="ot2">Link<input class="input" id="ol2"></div>
<div class="card">Tasks 6 টা Link - <div id="t"></div></div>
<button class="btn-save" onclick="saveAll()">SAVE ALL</button>
<script>
let cur=[];let off=[];
function load(){fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{document.getElementById('admin_name').value=d.s.admin_name;document.getElementById('admin_pic').value=d.s.admin_pic;document.getElementById('inbox_text').value=d.s.inbox_text;document.getElementById('ot0').value=d.s.official_links[0].title;document.getElementById('ol0').value=d.s.official_links[0].link;document.getElementById('ot1').value=d.s.official_links[1].title;document.getElementById('ol1').value=d.s.official_links[1].link;document.getElementById('ot2').value=d.s.official_links[2].title;document.getElementById('ol2').value=d.s.official_links[2].link;cur=d.s.tasks;let h='';cur.forEach((t,i)=>{h+=`Task ${i+1}<input class="input" id="tt_${i}" value="${t.title}"><input class="input" id="tl_${i}" value="${t.link}"><input class="input" id="tr_${i}" value="${t.reward}">`;});document.getElementById('t').innerHTML=h;});}
function saveAll(){let tasks=[];for(let i=0;i<6;i++){tasks.push({title:document.getElementById('tt_'+i).value,link:document.getElementById('tl_'+i).value,reward:parseInt(document.getElementById('tr_'+i).value)||20,color:cur[i].color,btn:cur[i].btn});}let data={admin_name:document.getElementById('admin_name').value,admin_pic:document.getElementById('admin_pic').value,inbox_text:document.getElementById('inbox_text').value,official_links:[{title:document.getElementById('ot0').value,link:document.getElementById('ol0').value,color:'#0ea5e9'},{title:document.getElementById('ot1').value,link:document.getElementById('ol1').value,color:'#dc2626'},{title:document.getElementById('ot2').value,link:document.getElementById('ol2').value,color:'#1e40af'}],tasks:tasks};fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>alert('Saved'));}load();
</script></body></html>
"""
if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
