import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'
def load_db():
 d={"app_name":"Premium Pro","admin":"SHIBLI NOMAN","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,"refc":15,"daily":20,"zone":"11764581","link":"YOUR_DIRECT_LINK_11760259","bg":"#0B0E1C","card":"#151A2D","top":"#151A2D","btn":"#8b5cf6","btn2":"#f59e0b","text":"#f8fafc","offer_t":"💎 Premium Offer","offer_d":"50 Ads দেখলে ৳150 Bonus","bal_t":"Premium Balance","notice":"💎 Fast Payment • Trusted"}
 if not os.path.exists(DB):
  data={"users":{},"wds":[],"settings":d,"tasks":[{"id":1,"title":"💎 Join Channel","reward":20,"link":"https://t.me/"},{"id":2,"title":"🔔 Subscribe","reward":25,"link":"https://youtube.com/"}]}
  open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
 db=json.load(open(DB,'r',encoding='utf-8'))
 for k,v in d.items():
  if k not in db["settings"]:db["settings"][k]=v
 return db
def save_db(db):open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
def get_user(db,uid,ref=None):
 uid=str(uid)
 if uid not in db["users"]:
  db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"ads":0}
  if ref and ref in db["users"] and ref!=uid:db["users"][ref]["refl"].append(uid)
 return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def init_api():
 db=load_db();j=request.json;uid=str(j.get('id'));ref=j.get('ref')
 if ref==uid:ref=None
 u=get_user(db,uid,ref)
 if u["last"]!=str(datetime.now().date()):u["c"]=0;u["p"]=0;u["last"]=str(datetime.now().date())
 save_db(db);return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":[x for x in db["wds"] if x["uid"]==uid]})

@app.route('/api/ads',methods=['POST'])
def ads():
 db=load_db();j=request.json;uid=str(j.get('id'));t=j.get('type');u=get_user(db,uid);s=db["settings"]
 if t=='c':
  if u["c"]>=s["clim"]:return jsonify({"msg":"Limit শেষ"})
  u["c"]+=1;u["bal"]+=s["ad"];u["total"]+=s["ad"]
 else:
  if u["p"]>=s["plim"]:return jsonify({"msg":"Limit শেষ"})
  u["p"]+=1;u["bal"]+=s["pop"];u["total"]+=s["pop"]
 u["ads"]+=1;save_db(db);return jsonify({"msg":f"৳{s['ad'] if t=='c' else s['pop']} যোগ"})

@app.route('/api/task',methods=['POST'])
def task():
 db=load_db();j=request.json;u=get_user(db,str(j.get('id')));tid=int(j.get('tid'))
 if tid in u["done"]:return jsonify({"msg":"Done"})
 t=next((x for x in db["tasks"] if x["id"]==tid),None);u["done"].append(tid);u["bal"]+=t["reward"];u["total"]+=t["reward"];save_db(db);return jsonify({"msg":f"৳{t['reward']} যোগ"})

@app.route('/api/wd',methods=['POST'])
def wd():
 db=load_db();j=request.json;u=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
 if amt<s["min"]:return jsonify({"msg":f"Min {s['min']}"})
 if u["bal"]<amt:return jsonify({"msg":"Balance কম"})
 u["bal"]-=amt;db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")});save_db(db);return jsonify({"msg":"Withdraw সফল"})

@app.route('/api/update',methods=['POST'])
def up():
 db=load_db();j=request.json;u=get_user(db,str(j.get('id')))
 if 'name' in j:u["name"]=j['name'][:20]
 if 'img' in j and j['img']:u["img"]=j['img']
 save_db(db);return jsonify({"msg":"Saved"})

@app.route('/')
def home():
 s=load_db()["settings"]
 return render_template_string("""
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{app_name}}</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:{{bg}};color:{{text}};max-width:430px;margin:auto;padding-bottom:220px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:{{top}};position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b}
.card{margin:12px;border-radius:20px;padding:18px;background:{{card}};border:1px solid #1e293b;box-shadow:0 8px 30px rgba(0,0,0,.3);position:relative;overflow:hidden}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;margin-top:10px;background:linear-gradient(135deg,{{btn}},#7c3aed)}
.btn2{background:linear-gradient(135deg,{{btn2}},#f97316)!important}
.profile{width:52px;height:52px;border-radius:16px;background:#1e293b;display:flex;align-items:center;justify-content:center;border:2px solid {{btn}};overflow:hidden;font-size:26px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(21,26,45,.95);backdrop-filter:blur(15px);display:flex;padding:10px 0 14px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
input{width:100%;padding:13px;border-radius:12px;border:1px solid #1e293b;background:#0B0E1C;color:#fff;margin-top:8px;outline:none}
.meth{flex:1;padding:12px;border-radius:12px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C}.meth.on{border-color:{{btn}};background:rgba(139,92,246,.15)}
.task{display:flex;justify-content:space-between;align-items:center;padding:14px;border:1px solid #1e293b;border-radius:14px;margin-top:10px;background:#0F1429}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div class="profile" id="pImg">💎</div><div><b id="uName">Loading</b><br><small id="uId" style="opacity:.5"></small></div></div><div><b id="bal" style="color:#22c55e">৳0</b></div></div>

<div id="p-home" class="page active">
<div class="card"><h4>💰 {{bal_t}}</h4><h1 id="bal2" style="color:#22c55e;margin-top:8px">৳0</h1><div style="display:flex;gap:8px;margin-top:10px"><div style="flex:1;background:#0B0E1C;padding:10px;border-radius:12px;text-align:center"><small>Company</small><br><b id="cL">0/50</b></div><div style="flex:1;background:#0B0E1C;padding:10px;border-radius:12px;text-align:center"><small>Popup</small><br><b id="pL">0/30</b></div></div></div>
<div class="card"><h4>🚀 Premium Ads</h4><p style="font-size:11px;opacity:.5;margin:6px 0">2 টা লিংক থেকে ইনকাম (81+59)</p><button class="btn" onclick="doAd('c')">▶ Company Ads - ৳<span id="ar">3</span></button><button class="btn btn2" onclick="doAd('p')">🎁 Popup Ads - ৳<span id="pr">5</span></button></div>
</div>

<div id="p-tasks" class="page"><div class="card"><h4>✅ Tasks</h4><div id="tList"></div></div></div>

<div id="p-refer" class="page"><div class="card"><h4>👥 Refer</h4><input id="rLink" readonly><button class="btn" onclick="copyR()">Copy Link</button><div id="rList" style="margin-top:10px"></div></div></div>

<div id="p-support" class="page"><div class="card"><h4>💎 Support</h4><button class="btn" onclick="window.open('https://t.me/','_blank')">Telegram</button><button class="btn btn2" onclick="window.open('https://wa.me/','_blank')">WhatsApp</button></div></div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center"><div class="profile" id="pImg2" style="width:80px;height:80px;margin:0 auto;border-radius:20px;font-size:36px">💎</div><h3 id="pName" style="margin-top:10px">User</h3><small id="pJoin" style="opacity:.6"></small><input id="eName" placeholder="নতুন নাম লিখুন"><input type="file" id="fImg" accept="image/*"><button class="btn" onclick="saveP()">💾 Save Profile</button></div>

<div class="card"><h4>💸 Beautiful Withdraw</h4><div style="display:flex;gap:8px;margin:10px 0"><div class="meth on" id="mBk" onclick="setM('bKash')">bKash</div><div class="meth" id="mNa" onclick="setM('Nagad')">Nagad</div></div><input id="wNum" placeholder="01XXXXXXXXX"><input id="wAmt" type="number" placeholder="Amount"><button class="btn" onclick="doWd()">Withdraw</button><div id="wH" style="margin-top:12px"></div></div>
</div>

<div class="btm">
<div onclick="show('home')" id="b-home" class="on"><span>🏠</span>Home</div>
<div onclick="show('tasks')" id="b-tasks"><span>🎯</span>Tasks</div>
<div onclick="show('refer')" id="b-refer"><span>👥</span>Refer</div>
<div onclick="show('support')" id="b-support"><span>💎</span>Support</div>
<div onclick="show('profile')" id="b-profile"><span>👤</span>Profile</div>
</div>

<script>
let uid=localStorage.getItem("uid"); if(!uid){uid="u_"+Date.now();localStorage.setItem("uid",uid)}
let ref=localStorage.getItem("ref")||new URLSearchParams(location.search).get("ref"); if(ref)localStorage.setItem("ref",ref)
let curM='bKash'
function setM(m){curM=m;document.querySelectorAll('.meth').forEach(x=>x.classList.remove('on'));document.getElementById(m=='bKash'?'mBk':'mNa').classList.add('on')}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,ref:ref})}).then(r=>r.json()).then(d=>{
document.getElementById('uName').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('uId').innerText=d.user.id;document.getElementById('pJoin').innerText='Join: '+d.user.join;document.getElementById('bal').innerText='৳'+d.user.bal;document.getElementById('bal2').innerText='৳'+d.user.bal;document.getElementById('cL').innerText=d.user.c+'/'+d.s.clim;document.getElementById('pL').innerText=d.user.p+'/'+d.s.plim;document.getElementById('ar').innerText=d.s.ad;document.getElementById('pr').innerText=d.s.pop;document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover;border-radius:14px">';document.getElementById('pImg2').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover;border-radius:18px">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div class="task"><div><b>${t.title}</b><br><small style="color:#22c55e">৳${t.reward}</small></div><button class="btn" style="width:auto;padding:8px 14px;margin:0" onclick="doT(${t.id},'${t.link}')" ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
let rl='';d.user.refl.forEach(r=>{rl+=`<div style="padding:8px;border-bottom:1px solid #1e293b;font-size:12px">👤 ${r}</div>`});document.getElementById('rList').innerHTML=rl||'No ref';
let wh='';d.wds.forEach(w=>{wh+=`<div style="padding:8px;border-bottom:1px solid #1e293b;font-size:12px;display:flex;justify-content:space-between"><span>${w.m} ৳${w.amt}</span><span style="background:#f59e0b;padding:2px 8px;border-radius:10px;font-size:10px">${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh||'No history';
})}
function doAd(t){window.open('https://example.com','_blank');fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function saveP(){let n=document.getElementById('eName').value;let f=document.getElementById('fImg').files[0];if(f){let rd=new FileReader();rd.onload=e=>{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:e.target.result})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})};rd.readAsDataURL(f)}else{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}}
function doWd(){let num=document.getElementById('wNum').value,amt=document.getElementById('wAmt').value;fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,m:curM,num:num,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
function copyR(){let i=document.getElementById('rLink');i.select();document.execCommand('copy');alert('Copied')}
load()
</script></body></html>
""", **s)

@app.route('/admin')
def admin():return "Admin - add /api/admin/save route if needed"
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
