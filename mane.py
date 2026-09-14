import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"Premium Diamond","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,"daily":20,"zone":"11764581","link":"https://omg10.com/4/11760259","admin":"SHIBLI","notice":"5-30 Min Payment"}
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[{"id":1,"title":"Join Channel","reward":20,"link":"https://t.me/"},{"id":2,"title":"Subscribe","reward":25,"link":"https://youtube.com/"}]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    db=json.load(open(DB,'r',encoding='utf-8'));
    for k,v in d.items():
        if k not in db["settings"]: db["settings"][k]=v
    return db

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"ads":0}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refl"].append(uid)
    return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;uid=str(j.get('id'));ref=j.get('ref')
    if ref==uid: ref=None
    u=get_user(db,uid,ref)
    if u["last"]!=str(datetime.now().date()): u["c"]=0;u["p"]=0;u["last"]=str(datetime.now().date())
    save_db(db); return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":[x for x in db["wds"] if x["uid"]==uid]})

@app.route('/api/ads',methods=['POST'])
def ads():
    db=load_db();j=request.json;uid=str(j.get('id'));t=j.get('type');u=get_user(db,uid);s=db["settings"]
    if t=='c':
        if u["c"]>=s["clim"]: return jsonify({"msg":"আজকের লিমিট শেষ"})
        u["c"]+=1; u["bal"]+=s["ad"]; u["total"]+=s["ad"]
    else:
        if u["p"]>=s["plim"]: return jsonify({"msg":"লিমিট শেষ"})
        u["p"]+=1; u["bal"]+=s["pop"]; u["total"]+=s["pop"]
    u["ads"]+=1; save_db(db); return jsonify({"msg":f"৳{s['ad'] if t=='c' else s['pop']} যোগ হয়েছে"})

@app.route('/api/task',methods=['POST'])
def task():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));tid=int(j.get('tid'))
    if tid in u["done"]: return jsonify({"msg":"Done"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None); u["done"].append(tid); u["bal"]+=t["reward"]; u["total"]+=t["reward"]; save_db(db); return jsonify({"msg":f"৳{t['reward']} যোগ"})

@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
    if amt<s["min"]: return jsonify({"msg":f"Min {s['min']}"})
    if u["bal"]<amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt; db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")}); save_db(db); return jsonify({"msg":"Withdraw সফল"})

@app.route('/api/update',methods=['POST'])
def up():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')))
    if 'name' in j: u["name"]=j['name'][:20]
    if 'img' in j and j['img']: u["img"]=j['img']
    save_db(db); return jsonify({"msg":"Profile Saved"})

@app.route('/')
def home():
    s=load_db()["settings"]
    html="""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:Inter,system-ui}body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.glass{background:linear-gradient(135deg,#151A2D 0%,#1A2040 100%);border:1px solid rgba(139,92,246,.2);border-radius:20px;padding:16px;margin:12px;box-shadow:0 10px 40px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.05)}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b}
.btn{width:100%;padding:13px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(135deg,#8b5cf6,#7c3aed);margin-top:8px}
.btn2{background:linear-gradient(135deg,#f59e0b,#f97316)!important}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(21,26,45,.96);backdrop-filter:blur(20px);display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;border-top:1px solid rgba(139,92,246,.2);z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer}.btm div.on{color:#a78bfa}.btm div span{font-size:20px;display:block}
.page{display:none}.page.active{display:block}
input{width:100%;padding:12px;border-radius:12px;border:1px solid #1e293b;background:#0B0E1C;color:#fff;margin-top:8px;outline:none}
.meth{flex:1;padding:11px;border-radius:12px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C;font-weight:700}.meth.on{border-color:#8b5cf6;background:rgba(139,92,246,.2);color:#a78bfa}
.card2{flex:1;background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:16px;padding:16px;border:1px solid rgba(139,92,246,.15);position:relative;overflow:hidden}
.spon{background:linear-gradient(90deg,#0f172a,#1e293b);border:1px dashed #f59e0b;border-radius:14px;padding:12px;margin:12px;display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<div class='top'><div style='display:flex;gap:10px;align-items:center'><div id='pImg' style='width:44px;height:44px;border-radius:12px;background:#1e293b;display:flex;align-items:center;justify-content:center;border:2px solid #8b5cf6;overflow:hidden'>💎</div><div><b id='uName'>Loading</b><br><small id='uId' style='opacity:.5;font-size:11px'></small></div></div><b id='bal' style='color:#22c55e'>৳0</b></div>

<div id='p-home' class='page active'>
<div class='glass' style='background:radial-gradient(120% 120% at 0% 0%, rgba(139,92,246,.25) 0%, transparent 60%), linear-gradient(135deg,#151A2D,#1A2040);'>
<div style='display:flex;justify-content:space-between;align-items:center'><div style='display:flex;gap:12px;align-items:center'><div style='width:58px;height:58px;border-radius:50%;background:radial-gradient(circle,#8b5cf6,#1e1b4b);display:flex;align-items:center;justify-content:center;font-size:28px;box-shadow:0 0 20px rgba(139,92,246,.5)'>💎</div><div><small style='color:#a78bfa'>Diamond Member • Level 3</small><br><b id='pName2'>User</b></div></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2><small style='background:#16a34a30;color:#4ade80;padding:2px 8px;border-radius:10px;font-size:10px' id='today'>+৳0 today</small></div></div>
<div style='display:flex;gap:20px;margin-top:12px;font-size:12px;opacity:.7'><span>Total Earned: <b id='total' style='color:#fff'>৳0</b></span><span>Pending: <b id='pending'>৳0</b></span></div>
</div>

<div style='padding:0 12px;display:flex;justify-content:space-between;align-items:center'><h4>Earn More</h4><small style='color:#8b5cf6'>View All ></small></div>
<div style='display:flex;gap:10px;margin:10px 12px'>
<div class='card2'><div style='width:40px;height:40px;background:#8b5cf6;border-radius:10px;display:flex;align-items:center;justify-content:center'>📢</div><b style='display:block;margin:8px 0'>Company Ads</b><small style='opacity:.6'>Watch ads & earn</small><button class='btn' style='padding:9px;font-size:12px' onclick='doAd(\"c\")'>Start Earning</button><small style='display:block;text-align:center;margin-top:6px;color:#8b5cf6'>৳3 / ad</small></div>
<div class='card2' style='border-color:rgba(245,158,11,.3)'><div style='width:40px;height:40px;background:#f59e0b;border-radius:10px;display:flex;align-items:center;justify-content:center'>▶️</div><b style='display:block;margin:8px 0'>Popup Ads</b><small style='opacity:.6'>Quick popup</small><button class='btn btn2' style='padding:9px;font-size:12px' onclick='doAd(\"p\")'>Watch & Earn</button><small style='display:block;text-align:center;margin-top:6px;color:#f59e0b'>৳5 / ad</small></div>
</div>

<div class='glass'><h4>💸 Withdraw Earnings <span style='float:right;font-size:11px;background:#16a34a30;color:#4ade80;padding:3px 8px;border-radius:10px'>Secure • Instant</span></h4><div style='display:flex;gap:8px;margin:12px 0'><div class='meth on' id='mBk' onclick='setM(\"bKash\")'>bKash</div><div class='meth' id='mNa' onclick='setM(\"Nagad\")'>Nagad</div></div><small>Withdraw Amount</small><input id='wAmt' type='number' placeholder='৳500.00'><small style='opacity:.5'>Min ৳100 | Max ৳5000</small><button class='btn' onclick='doWd()' style='background:linear-gradient(135deg,#6366f1,#8b5cf6)'>Withdraw Now ↓</button><small style='display:block;text-align:center;margin-top:8px;opacity:.5'>Funds arrive within 5-30 minutes • 2% fee</small></div>

<div class='spon'><div><small style='background:#f59e0b;color:#000;padding:2px 6px;border-radius:6px;font-size:9px;font-weight:800'>SPONSORED</small><br><b style='font-size:14px'>Daraz 11.11 Sale Live!</b><br><small style='opacity:.6;font-size:11px'>Shop now and earn 5% cashback</small></div><button class='btn' style='width:auto;padding:8px 16px;margin:0;font-size:12px'>Explore</button></div>
<div style='margin:0 12px;opacity:.6;font-size:11px;text-align:center'>Company Ads Banner এখানে চলবে - Zone 11764581</div>
</div>

<div id='p-tasks' class='page'><div class='glass'><h4>✅ Tasks</h4><div id='tList'></div></div></div>
<div id='p-refer' class='page'><div class='glass'><h4>👥 Refer & Earn ৳80</h4><input id='rLink' readonly><button class='btn' onclick='copyR()'>Copy Link</button><div id='rList' style='margin-top:10px'></div></div></div>
<div id='p-support' class='page'><div class='glass'><h4>💎 Support</h4><button class='btn' onclick='window.open(\"https://t.me/\")'>Telegram</button><button class='btn btn2' onclick='window.open(\"https://wa.me/\")'>WhatsApp</button></div></div>
<div id='p-profile' class='page'>
<div class='glass' style='text-align:center'><div id='pImg2' style='width:76px;height:76px;margin:0 auto;background:#1e293b;border-radius:20px;display:flex;align-items:center;justify-content:center;border:2px solid #8b5cf6;font-size:32px;overflow:hidden'>💎</div><h3 id='pName' style='margin-top:8px'>User</h3><small id='pJoin' style='opacity:.6'></small><input id='eName' placeholder='নতুন নাম'><input type='file' id='fImg' accept='image/*'><button class='btn' onclick='saveP()'>💾 Save Profile</button></div>
<div class='glass'><h4>Withdraw History</h4><div id='wH'></div><input id='wNum' placeholder='01XXXXXXXXX' style='margin-top:12px'></div>
</div>

<div class='btm'>
<div onclick='show(\"home\")' id='b-home' class='on'><span>🏠</span>Home</div>
<div onclick='show(\"tasks\")' id='b-tasks'><span>🎯</span>Tasks</div>
<div onclick='show(\"refer\")' id='b-refer'><span>👥</span>Refer</div>
<div onclick='show(\"support\")' id='b-support'><span>💎</span>Support</div>
<div onclick='show(\"profile\")' id='b-profile'><span>👤</span>Profile</div>
</div>

<script>
let uid=localStorage.getItem('uid'); if(!uid){uid='u_'+Date.now();localStorage.setItem('uid',uid)}
let ref=localStorage.getItem('ref')||new URLSearchParams(location.search).get('ref'); if(ref)localStorage.setItem('ref',ref)
let curM='bKash'
function setM(m){curM=m;document.querySelectorAll('.meth').forEach(x=>x.classList.remove('on'));document.getElementById(m=='bKash'?'mBk':'mNa').classList.add('on')}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,ref:ref})}).then(r=>r.json()).then(d=>{
document.getElementById('uName').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('pName2').innerText=d.user.name;document.getElementById('uId').innerText=d.user.id;document.getElementById('pJoin').innerText='Join: '+d.user.join;document.getElementById('bal').innerText='৳'+d.user.bal;document.getElementById('bal2').innerText='৳'+d.user.bal;document.getElementById('total').innerText='৳'+d.user.total;document.getElementById('today').innerText='+৳'+d.user.c*3+' today';document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src=\"'+d.user.img+'\" style=\"width:100%;height:100%;object-fit:cover\">';document.getElementById('pImg2').innerHTML='<img src=\"'+d.user.img+'\" style=\"width:100%;height:100%;object-fit:cover\">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div style='display:flex;justify-content:space-between;align-items:center;padding:12px;background:#0B0E1C;border-radius:12px;margin-top:8px'><div><b>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},\"${t.link}\")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
let rl='';d.user.refl.forEach(r=>{rl+=`<div style='padding:6px;font-size:12px;border-bottom:1px solid #1e293b'>👤 ${r}</div>`});document.getElementById('rList').innerHTML=rl||'No refer yet';
let wh='';d.wds.forEach(w=>{wh+=`<div style='padding:8px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #1e293b'><span>${w.m} ৳${w.amt}</span><span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:10px'>${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh||'No history';
})}
function doAd(t){window.open('{{link}}','_blank');fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function saveP(){let n=document.getElementById('eName').value;let f=document.getElementById('fImg').files[0];if(f){let rd=new FileReader();rd.onload=e=>{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:e.target.result})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})};rd.readAsDataURL(f)}else{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}}
function doWd(){let num=document.getElementById('wNum').value,amt=document.getElementById('wAmt').value;fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,m:curM,num:num,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
function copyR(){let i=document.getElementById('rLink');i.select();document.execCommand('copy');alert('Copied')}
load()
</script></body></html>
    """
    return render_template_string(html,link=s["link"])
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
