import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"Premium Diamond","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,"refc":15}
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[
            {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
            {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},
            {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}
        ]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    return json.load(open(DB,'r',encoding='utf-8'))

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"ads":0}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refl"].append(uid)
    return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')),j.get('ref'));save_db(db)
    wds=[x for x in db["wds"] if x["uid"]==u["id"]]
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds})

@app.route('/api/task',methods=['POST'])
def task_done():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));tid=int(j.get('tid'))
    if tid not in u["done"]:
        t=next((x for x in db["tasks"] if x["id"]==tid),None);u["done"].append(tid);u["bal"]+=t["reward"];u["total"]+=t["reward"];save_db(db)
        return jsonify({"msg":f"৳{t['reward']} যোগ"})
    return jsonify({"msg":"Done"})

@app.route('/api/ads',methods=['POST'])
def ads():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));s=db["settings"]
    if j.get('type')=='c':
        if u["c"]>=s["clim"]: return jsonify({"msg":"Limit শেষ"})
        u["c"]+=1;u["bal"]+=s["ad"];u["total"]+=s["ad"]
    else:
        if u["p"]>=s["plim"]: return jsonify({"msg":"Limit শেষ"})
        u["p"]+=1;u["bal"]+=s["pop"];u["total"]+=s["pop"]
    u["ads"]+=1;save_db(db);return jsonify({"msg":"Balance Added"})

@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
    if amt<s["min"]: return jsonify({"msg":f"Min {s['min']} লাগবে"})
    if u["bal"]<amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt;db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")});save_db(db);return jsonify({"msg":"Withdraw সফল"})

@app.route('/api/update',methods=['POST'])
def up():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')))
    if 'name' in j: u["name"]=j['name'][:20]
    if 'img' in j and j['img']: u["img"]=j['img']
    save_db(db);return jsonify({"msg":"Saved"})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        if request.form.get('act')=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif request.form.get('act')=='del_task':
            db["tasks"]=[t for t in db["tasks"] if t["id"]!=int(request.form.get('id'))]
        save_db(db)
    rows="".join([f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']}</td><td>৳{t['reward']}</td><td><form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button style='background:red;color:#fff;border:none;padding:4px 8px;border-radius:6px'>Del</button></form></td></tr>" for t in db["tasks"]])
    return render_template_string(f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui}}.card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px;border:1px solid #1e293b}} input{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}</style></head><body><h3>Admin - Tasks</h3><div class='card'><form method='post'><input type='hidden' name='act' value='add_task'><input name='title' placeholder='Title' required><input name='link' placeholder='Link' required><input name='reward' type='number' value='20'><input name='icon' value='📢'><button style='background:#8b5cf6;color:#fff;width:100%;padding:10px;border:none;border-radius:8px;margin-top:8px'>Add</button></form></div><div class='card'><table style='width:100%'><tr><th>ID</th><th>Title</th><th>Reward</th><th>Action</th></tr>{rows}</table></div><a href='/' style='color:#8b5cf6'>← App</a></body></html>")

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.glass{background:linear-gradient(135deg,#151A2D,#1A2040);border:1px solid rgba(139,92,246,.2);border-radius:20px;padding:16px;margin:12px}
.btn{width:100%;padding:12px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(135deg,#8b5cf6,#7c3aed);margin-top:8px;cursor:pointer}
.btn2{background:linear-gradient(135deg,#f59e0b,#f97316)!important}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(21,26,45,.98);backdrop-filter:blur(15px);display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer}.btm div.on{color:#a78bfa}.btm div span{font-size:20px;display:block}
.page{display:none}.page.active{display:block}
.task-card{display:flex;justify-content:space-between;align-items:center;padding:14px;background:#0F1429;border:1px solid #1e293b;border-radius:14px;margin-top:10px}
input{width:100%;padding:12px;border-radius:12px;border:1px solid #1e293b;background:#0B0E1C;color:#fff;margin-top:8px;outline:none}
.meth{flex:1;padding:10px;border-radius:10px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C;font-weight:700}.meth.on{border-color:#8b5cf6;background:rgba(139,92,246,.2);color:#a78bfa}
</style></head><body>
<div style='padding:14px 16px;display:flex;justify-content:space-between;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b'><b>💎 Premium App</b><b id='bal' style='color:#22c55e'>৳0</b></div>

<div id='p-home' class='page active'>
<div class='glass'><div style='display:flex;justify-content:space-between'><div><small style='color:#a78bfa'>Diamond Member • Level 3</small><br><b>Good Evening, <span id='uName'>User</span>!</b></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2></div></div></div>
<div style='display:flex;gap:10px;margin:0 12px'><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><div style='width:36px;height:36px;background:#8b5cf6;border-radius:8px;display:flex;align-items:center;justify-content:center'>📢</div><b style='display:block;margin:6px 0;font-size:13px'>Company Ads</b><button class='btn' style='padding:8px;font-size:12px' onclick='doAd("c")'>Start Earning</button></div><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><div style='width:36px;height:36px;background:#f59e0b;border-radius:8px;display:flex;align-items:center;justify-content:center'>▶️</div><b style='display:block;margin:6px 0;font-size:13px'>Popup Ads</b><button class='btn btn2' style='padding:8px;font-size:12px' onclick='doAd("p")'>Watch & Earn</button></div></div>
<div class='glass'><h4>💸 Withdraw <span style='float:right;font-size:10px;background:#16a34a30;color:#4ade80;padding:3px 8px;border-radius:8px'>Secure</span></h4><div style='display:flex;gap:8px;margin:10px 0'><div class='meth on' id='mBk' onclick='setM("bKash")'>bKash</div><div class='meth' id='mNa' onclick='setM("Nagad")'>Nagad</div></div><input id='wNum' placeholder='01XXXXXXXXX'><input id='wAmt' type='number' placeholder='Amount Min 300'><button class='btn' style='background:linear-gradient(135deg,#6366f1,#8b5cf6)' onclick='doWd()'>Withdraw Now</button><div id='wH' style='margin-top:10px'></div></div>
<div style='margin:12px;background:#0F1429;border:1px dashed #f59e0b;border-radius:12px;padding:12px;display:flex;justify-content:space-between;align-items:center'><div><small style='background:#f59e0b;color:#000;padding:2px 6px;border-radius:4px;font-size:9px'>SPONSORED</small><br><b style='font-size:13px'>Company Ads Box</b></div><button style='background:#8b5cf6;color:#fff;border:none;padding:6px 12px;border-radius:8px'>Explore</button></div>
</div>

<div id='p-tasks' class='page'>
<div class='glass'><h4>🎯 Tasks & Company Links</h4><div id='tList'></div></div>
</div>

<div id='p-refer' class='page'>
<div class='glass'><h4>👥 Refer & Earn</h4><p style='font-size:12px;opacity:.6;margin:8px 0'>প্রতি রেফারে ৳80 বোনাস + 15% কমিশন</p><input id='rLink' readonly><button class='btn' onclick='copyR()'>Copy Refer Link</button><div style='display:flex;gap:8px;margin-top:12px'><div style='flex:1;background:#0B0E1C;padding:10px;border-radius:10px;text-align:center'><small>Total Refer</small><br><b id='rCount'>0</b></div><div style='flex:1;background:#0B0E1C;padding:10px;border-radius:10px;text-align:center'><small>Earned</small><br><b style='color:#22c55e' id='rEarn'>৳0</b></div></div><div id='rList' style='margin-top:10px'></div></div>
</div>

<div id='p-support' class='page'>
<div class='glass'><h4>💎 Support Center</h4><p style='font-size:12px;opacity:.6;margin:8px 0'>যেকোনো সমস্যায় আমাদের সাথে যোগাযোগ করুন</p><button class='btn' onclick='window.open("https://t.me/","_blank")'>📢 Telegram Channel</button><button class='btn btn2' onclick='window.open("https://wa.me/","_blank")'>💬 WhatsApp Support</button><div style='margin-top:12px;background:#0B0E1C;padding:12px;border-radius:12px'><b style='font-size:13px'>FAQ</b><br><small style='opacity:.7'>• Withdraw 5-30 মিনিটে পেমেন্ট<br>• Daily 50 টা Company Ads<br>• Min Withdraw ৳300</small></div></div>
</div>

<div id='p-profile' class='page'>
<div class='glass' style='text-align:center'><div id='pImg' style='width:70px;height:70px;margin:0 auto;background:#1e293b;border-radius:18px;display:flex;align-items:center;justify-content:center;border:2px solid #8b5cf6;font-size:30px;overflow:hidden'>💎</div><h3 id='pName' style='margin-top:8px'>User</h3><small id='pJoin' style='opacity:.6'></small><input id='eName' placeholder='নতুন নাম লিখুন'><input type='file' id='fImg' accept='image/*'><button class='btn' onclick='saveP()'>💾 Save Profile</button></div>
<div class='glass'><h4>📊 Statistics</h4><div style='display:flex;gap:8px;margin-top:8px'><div style='flex:1;background:#0B0E1C;padding:10px;border-radius:10px;text-align:center'><small>Total Earned</small><br><b id='total' style='color:#22c55e'>৳0</b></div><div style='flex:1;background:#0B0E1C;padding:10px;border-radius:10px;text-align:center'><small>Ads Watched</small><br><b id='ads'>0</b></div></div></div>
</div>

<div class='btm'>
<div onclick="show('home')" id='b-home' class='on'><span>🏠</span>Home</div>
<div onclick="show('tasks')" id='b-tasks'><span>🎯</span>Tasks</div>
<div onclick="show('refer')" id='b-refer'><span>👥</span>Refer</div>
<div onclick="show('support')" id='b-support'><span>💬</span>Support</div>
<div onclick="show('profile')" id='b-profile'><span>👤</span>Profile</div>
</div>

<script>
let uid=localStorage.getItem('uid'); if(!uid){uid='u_'+Date.now();localStorage.setItem('uid',uid)}
let ref=localStorage.getItem('ref')||new URLSearchParams(location.search).get('ref'); if(ref)localStorage.setItem('ref',ref)
let curM='bKash'
function setM(m){curM=m;document.querySelectorAll('.meth').forEach(x=>x.classList.remove('on'));document.getElementById(m=='bKash'?'mBk':'mNa').classList.add('on')}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,ref:ref})}).then(r=>r.json()).then(d=>{
document.getElementById('bal').innerText='৳'+d.user.bal;document.getElementById('bal2').innerText='৳'+d.user.bal;document.getElementById('uName').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('pJoin').innerText='Join: '+d.user.join;document.getElementById('total').innerText='৳'+d.user.total;document.getElementById('ads').innerText=d.user.ads||0;document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;document.getElementById('rCount').innerText=d.user.refl.length;document.getElementById('rEarn').innerText='৳'+(d.user.refl.length*d.s.ref);
document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div class='task-card'><div style='display:flex;gap:10px;align-items:center'><div style='font-size:20px'>${t.icon}</div><div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
let rl='';d.user.refl.forEach(r=>{rl+=`<div style='padding:6px;font-size:12px;border-bottom:1px solid #1e293b'>👤 ${r} - ৳${d.s.ref}</div>`});document.getElementById('rList').innerHTML=rl||'<small style="opacity:.5">No refer yet</small>';
let wh='';d.wds.forEach(w=>{wh+=`<div style='padding:6px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #1e293b'><span>${w.m} ৳${w.amt}</span><span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:8px'>${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh||'<small style="opacity:.5">No history</small>';
})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doAd(t){fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doWd(){let num=document.getElementById('wNum').value,amt=document.getElementById('wAmt').value;fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,m:curM,num:num,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function saveP(){let n=document.getElementById('eName').value;let f=document.getElementById('fImg').files[0];if(f){let rd=new FileReader();rd.onload=e=>{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:e.target.result})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})};rd.readAsDataURL(f)}else{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
function copyR(){let i=document.getElementById('rLink');i.select();document.execCommand('copy');alert('Copied')}
load()
</script></body></html>
    """)

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
