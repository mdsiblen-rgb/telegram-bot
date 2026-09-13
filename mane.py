# FINAL APP - 8-9 DIN ER KOSTO - ADMIN HEADER + USER EDITABLE PROFILE - CLEAN
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    if not os.path.exists(DB_FILE):
        d={"users":{"8807178385":{"id":"8807178385","bal":60,"ads":0,"uname":"Admin Anis","upic":"https://i.pravatar.cc/150?img=12"}},"w":[],"s":{"admin_name":"প্রতিদিনের কাজ BD","admin_pic":"https://i.pravatar.cc/150?img=32"}}
        with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,ensure_ascii=False)
        return d
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except:
        return {"users":{"8807178385":{"id":"8807178385","bal":60,"ads":0,"uname":"Admin Anis","upic":"https://i.pravatar.cc/150?img=12"}},"w":[],"s":{"admin_name":"প্রতিদিনের কাজ BD","admin_pic":"https://i.pravatar.cc/150?img=32"}}

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)

@app.route('/')
def home(): return render_template_string(USER_PAGE)

@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID: return f"<h3>Admin Only /admin?id={ADMIN_ID}</h3>"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/bal')
def api_bal():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0,"uname":f"User {uid[-4:]}","upic":"https://i.pravatar.cc/150?img=8"}
    save_db(db)
    u=db["users"][uid]
    return jsonify({"bal":u["bal"],"ads":u["ads"],"id":uid,"uname":u.get("uname",f"User {uid[-4:]}"),"upic":u.get("upic",""),"w":db["w"][-15:][::-1],"s":db.get("s",{}),"total_users":len(db["users"])})

@app.route('/api/add')
def api_add():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0,"uname":f"User {uid[-4:]}","upic":"https://i.pravatar.cc/150?img=8"}
    db["users"][uid]["bal"]+=int(request.args.get('amt',2))
    db["users"][uid]["ads"]+=1
    save_db(db)
    return jsonify({"ok":True})

@app.route('/api/wd')
def api_wd():
    uid=request.args.get('id',ADMIN_ID)
    db=load_db()
    amt=int(request.args.get('amt',0))
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    if db["users"][uid]["bal"]<amt: return jsonify({"msg":"Min 1000 লাগবে"})
    db["users"][uid]["bal"]-=amt
    db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"met":request.args.get('met','bKash'),"time":str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg":"Withdraw Success"})

@app.route('/api/save',methods=['POST'])
def api_save():
    db=load_db()
    db["s"].update(request.json)
    save_db(db)
    return jsonify({"msg":"Saved"})

@app.route('/api/update_profile',methods=['POST'])
def api_upd():
    j=request.json
    uid=j.get('id',ADMIN_ID)
    db=load_db()
    if uid not in db["users"]: db["users"][uid]={"id":uid,"bal":60,"ads":0}
    if j.get('uname'): db["users"][uid]["uname"]=j.get('uname')
    if j.get('upic'): db["users"][uid]["upic"]=j.get('upic')
    save_db(db)
    return jsonify({"msg":"Profile Updated"})

USER_PAGE = '''
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#08112e;color:#fff;max-width:430px;margin:0 auto;padding-bottom:95px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:17px;font-weight:800}
.hdr-pic{width:52px;height:52px;border-radius:50%;border:3px solid #2ef36c;object-fit:cover}
.bal{font-size:50px;font-weight:900;color:#2ef36c;margin-top:6px}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.dot{width:10px;height:10px;background:#2ef36c;border-radius:50%;animation:blk 0.8s infinite}
@keyframes blk{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:18px;height:175px;position:relative;overflow:hidden}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:13px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:12px;border-radius:12px;border:1px solid #2a3a5f;background:#0b142d;color:#fff;margin-top:10px}
.meth{display:flex;gap:8px;margin-top:10px}
.meth div{flex:1;background:#0b142d;border:2px solid #2a3a5f;border-radius:12px;padding:11px;text-align:center;cursor:pointer}
.meth div.on{border-color:#ff2d7a;background:#1a1430}
.upic{width:90px;height:90px;border-radius:50%;border:4px solid #2ef36c;object-fit:cover}
</style></head><body>
<div id="p-home">
<div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName">👑 প্রতিদিনের কাজ BD ✅</div><img id="hdrPic" class="hdr-pic" src="https://i.pravatar.cc/150?img=32"></div><div class="bal">৳ <span id="bh">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span id="adH">0</span>/100</div></div>
<div class="notice"><div><div style="font-weight:900">অফিসিয়াল নোটিস</div><div style="font-size:12px;opacity:0.8">প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:10px 18px;border-radius:30px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"><img class="on" src="https://picsum.photos/600/300?random=21"><img src="https://picsum.photos/600/300?random=22"><img src="https://picsum.photos/600/300?random=23"></div>
<div class="card"><div style="font-weight:800">🎬 স্পেশাল অফার</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="ads()">ADS দেখুন - ৳2 বোনাস</button></div>
<div id="tasksHome"></div>
</div>
<div id="p-tasks" style="display:none"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName2">👑 প্রতিদিনের কাজ BD ✅</div><img id="hdrPic2" class="hdr-pic" src=""></div><div class="bal">৳ <span id="bt">60</span></div></div><div id="tasksAll"></div></div>
<div id="p-refer" style="display:none"><div class="hdr"><div>রেফার</div><div class="bal">৳ <span id="br">60</span></div></div><div class="card"><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyR()">Copy Link</button></div></div>
<div id="p-wallet" style="display:none"><div class="hdr"><div>ওয়ালেট</div><div class="bal">৳ <span id="bw">60</span></div></div><div class="card"><div style="font-size:36px;font-weight:900;color:#2ef36c">৳ <span id="bw2">60</span></div></div><div class="card"><input class="inp" id="wAmt" placeholder="Amount Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')">bKash</div><div id="m-nagad" onclick="sel('Nagad')">Nagad</div></div><input class="inp" id="wNum" placeholder="Number"><button class="btn" style="background:#2563eb;margin-top:12px" onclick="wd()">Withdraw</button></div><div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c">💸 Live Withdraw</div><div id="liveList"></div></div></div>

<div id="p-profile" style="display:none">
<div class="hdr" style="text-align:center"><img id="userPic" class="upic" src="https://i.pravatar.cc/150?img=8"><div style="font-weight:900;font-size:19px;margin-top:10px" id="userName">User</div><div style="opacity:0.7;font-size:12px;margin-top:4px">ID: <span id="pid"></span> - Verified ✅</div><div class="bal" style="text-align:center">৳ <span id="bp">60</span></div><div style="opacity:0.7;text-align:center">Ads: <span id="adP">0</span>/100</div></div>
<div class="card" style="border:2px solid #22c55e"><div style="font-weight:900">✏️ আমার প্রোফাইল পরিবর্তন করুন</div><div style="font-size:12px;opacity:0.6;margin-top:4px">আপনার নাম ও ছবি পরিবর্তন করতে পারবেন - সবাই আপনার নাম দেখবে</div><input class="inp" id="editName" placeholder="আপনার নাম লিখুন"><input class="inp" id="editPic" placeholder="ছবির Link দিন - imgbb.com থেকে"><button class="btn" style="background:#22c55e;color:#000;margin-top:12px" onclick="saveProfile()">💾 Save Profile</button></div>
<div class="card"><div style="display:flex;gap:10px"><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#2ef36c" id="adP2">0</div><div style="font-size:11px;opacity:0.6">Ads</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#0ea5e9" id="bp3">60</div><div style="font-size:11px;opacity:0.6">Balance</div></div><div style="flex:1;background:#0b142d;border-radius:12px;padding:12px;text-align:center"><div style="font-size:20px;font-weight:900;color:#22c55e">Active</div><div style="font-size:11px;opacity:0.6">Status</div></div></div></div>
</div>

<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let method='bKash';
let tasks=[{title:'YouTube Subscribe',reward:25,link:'https://youtube.com',color:'#dc2626',btn:'Join & Get 25 Tk'},{title:'Telegram Join',reward:10,link:'https://t.me',color:'#1e40af',btn:'Join & Get 10 Tk'},{title:'Facebook Follow',reward:15,link:'https://facebook.com',color:'#0ea5e9',btn:'Follow & Get 15 Tk'},{title:'Website Visit',reward:20,link:'https://google.com',color:'#7c3aed',btn:'Visit & Get 20 Tk'}];
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Copied'));}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid+'&amt=2').then(()=>load());});}else{fetch('/api/add?id='+uid+'&amt=2').then(()=>{alert('৳2 Added');load();});}}
function claim(i){window.open(tasks[i].link,'_blank');setTimeout(()=>{fetch('/api/add?id='+uid+'&amt='+tasks[i].reward).then(()=>{alert('৳'+tasks[i].reward);load();});},1200);}
function wd(){let a=document.getElementById('wAmt').value,n=document.getElementById('wNum').value;if(!a||!n){alert('Amount & Number');return;}fetch('/api/wd?id='+uid+'&amt='+a+'&num='+n+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function saveProfile(){let name=document.getElementById('editName').value,pic=document.getElementById('editPic').value;if(!name&&!pic){alert('নাম বা ছবির Link দিন');return;}fetch('/api/update_profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,uname:name,upic:pic})}).then(r=>r.json()).then(x=>{alert('✅ Profile Updated');load();});}
let sI=0;setInterval(()=>{let im=document.querySelectorAll('#sl img');im.forEach(i=>i.classList.remove('on'));sI=(sI+1)%im.length;im[sI].classList.add('on');},2500);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{
['bh','bt','br','bw','bw2','bp','bp3'].forEach(id=>{let e=document.getElementById(id);if(e)e.innerText=d.bal;});
['adH','adT','adP','adP2'].forEach(id=>{let e=document.getElementById(id);if(e)e.innerText=d.ads;});
document.getElementById('pid').innerText=d.id.slice(0,4)+'****'+d.id.slice(-2);
document.getElementById('refLink').value=location.origin+'/?ref='+d.id;
let live='';if(d.w.length==0)live='এখনো কেউ Withdraw করেনি';else d.w.forEach(w=>{live+='<div style="padding:6px 0;border-bottom:1px solid #1e2d4f">💸 ID:'+w.id.slice(-4)+' - ৳'+w.amt+' - '+w.met+'</div>';});
document.getElementById('liveList').innerHTML=live;
let an=d.s.admin_name||'প্রতিদিনের কাজ BD';let ap=d.s.admin_pic||'https://i.pravatar.cc/150?img=32';
let dec='👑 '+an+' ✅';
document.getElementById('hdrName').innerText=dec;
let h2=document.getElementById('hdrName2');if(h2)h2.innerText=dec;
document.getElementById('hdrPic').src=ap;
let hp2=document.getElementById('hdrPic2');if(hp2)hp2.src=ap;
document.getElementById('userName').innerText=d.uname;
document.getElementById('userPic').src=d.upic||'https://i.pravatar.cc/150?img=8';
document.getElementById('editName').placeholder=d.uname;
});}
function renderTasks(){let h='';tasks.forEach((t,i)=>{h+='<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ '+t.title+'</div><div>৳'+t.reward+'</div></div><button class="btn" style="background:'+t.color+';margin-top:10px" onclick="claim('+i+')">'+t.btn+'</button></div>';});document.getElementById('tasksHome').innerHTML=h;document.getElementById('tasksAll').innerHTML=h;}
renderTasks();load();
</script></body></html>
'''

ADMIN_PAGE = '''
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a1020;color:#fff;font-family:sans-serif;padding:14px;max-width:500px;margin:0 auto;padding-bottom:120px}
.card{background:#151f35;border:1px solid #1e2d4f;border-radius:16px;padding:14px;margin:12px 0}
.label{color:#38bdf8;font-size:12px;margin:12px 0 6px 0}
.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:10px;padding:12px;width:100%;color:#fff}
.btn-save{width:100%;max-width:480px;position:fixed;bottom:12px;left:50%;transform:translateX(-50%);padding:16px;background:linear-gradient(90deg,#22c55e,#16a34a);border:0;border-radius:14px;font-weight:900;color:#fff;z-index:99}
.preview{width:70px;height:70px;border-radius:50%;border:3px solid #22c55e;object-fit:cover}
</style></head><body>
<h2 style="color:#22c55e;text-align:center">✅ FINAL ADMIN PANEL</h2>
<div class="card" style="border:2px solid #22c55e">
<div style="font-weight:900">👑 Header Control - তোমার ছবি + নাম</div>
<div class="label">Header নাম - (👑 + ✅ Auto)</div>
<input class="input" id="admin_name"><div style="margin-top:4px">Preview: <b id="prevName" style="color:#2ef36c">👑 নাম ✅</b></div>
<div class="label">Header ছবির Link</div>
<input class="input" id="admin_pic"><div style="margin-top:8px;display:flex;gap:10px;align-items:center"><img id="prevPic" class="preview" src=""><div style="font-size:12px;opacity:0.7">Home এর ডান কোনায় দেখাবে</div></div>
</div>
<div class="card"><div id="info"></div></div>
<div class="card"><div style="font-weight:900">👥 Users - তাদের নিজের নাম/ছবি</div><div id="usersList" style="font-size:12px"></div></div>
<div class="card"><div style="font-weight:900">💸 Withdraw</div><div id="wList"></div></div>
<div style="height:80px"></div>
<button class="btn-save" onclick="saveAll()">💾 SAVE HEADER</button>
<script>
function load(){
fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{
document.getElementById('info').innerHTML='Users: '+d.total_users+'<br>Token Hidden: 11764581 - ID: 8807178385';
if(d.s.admin_name){document.getElementById('admin_name').value=d.s.admin_name;document.getElementById('prevName').innerText='👑 '+d.s.admin_name+' ✅';}
if(d.s.admin_pic){document.getElementById('admin_pic').value=d.s.admin_pic;document.getElementById('prevPic').src=d.s.admin_pic;}
let w='';if(d.w.length==0)w='No Withdraw';else d.w.forEach(x=>{w+='<div style="padding:5px;border-bottom:1px solid #222">৳'+x.amt+' - '+x.met+' '+x.num+'</div>';});
document.getElementById('wList').innerHTML=w;
fetch('/api/bal?id=8807178385').then(()=>{}); // placeholder
// users list from db - we need extra call, but quick hack: show from local? For now just total
document.getElementById('usersList').innerHTML='Total Users: '+d.total_users+' - User রা নিজের Profile Edit করতে পারবে Profile Page থেকে';
});
}
document.getElementById('admin_name').addEventListener('input',e=>{document.getElementById('prevName').innerText='👑 '+e.target.value+' ✅';});
document.getElementById('admin_pic').addEventListener('input',e=>{if(e.target.value.startsWith('http'))document.getElementById('prevPic').src=e.target.value;});
function saveAll(){let data={admin_name:document.getElementById('admin_name').value,admin_pic:document.getElementById('admin_pic').value};fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(()=>{alert('Saved - Header Live ✅');load();});}
load();
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
