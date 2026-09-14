import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={
        "app_name":"Premium App",
        "app_logo":"", # Admin ছবি
        "bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,
        "spon_title":"Company Ads Box",
        "spon_desc":"Best earning offer - Click to explore now!",
        "spon_btn":"Explore",
        "spon_link":"https://google.com",
        "levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000] # Level 1-10
    }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[
            {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
            {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},
            {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}
        ]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    db=json.load(open(DB,'r',encoding='utf-8'))
    for k,v in d.items():
        if k not in db["settings"]: db["settings"][k]=v
    return db

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))

def get_level(total, levels):
    lvl=1
    for i, th in enumerate(levels):
        if total>=th: lvl=i+1
    return lvl

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
    lvl=get_level(u["total"], db["settings"]["levels"])
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds,"level":lvl})

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
    if amt<s["min"]: return jsonify({"msg":f"Min {s['min']}"})
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
        act=request.form.get('act')
        if act=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif act=='del_task':
            db["tasks"]=[t for t in db["tasks"] if t["id"]!=int(request.form.get('id'))]
        elif act=='save_first':
            db["settings"]["app_name"]=request.form.get('app_name',db["settings"]["app_name"])
            db["settings"]["spon_title"]=request.form.get('spon_title')
            db["settings"]["spon_desc"]=request.form.get('spon_desc')
            db["settings"]["spon_btn"]=request.form.get('spon_btn')
            db["settings"]["spon_link"]=request.form.get('spon_link')
            logo=request.form.get('app_logo')
            if logo: db["settings"]["app_logo"]=logo
        save_db(db)
    rows="".join([f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']}</td><td>৳{t['reward']}</td><td><form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button style='background:red;color:#fff;border:none;padding:4px 8px;border-radius:6px'>Del</button></form></td></tr>" for t in db["tasks"]])
    return render_template_string(f"""
    <html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>
    body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui;max-width:600px;margin:auto}}
   .card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px;border:1px solid #1e293b}}
    input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}
    </style></head><body>
    <h3>⚙️ Admin - First Page Control</h3>
    <div class='card'>
        <h4>1. App Name & Logo (উপরের কোনায় ছবি)</h4>
        <form method='post'>
            <input type='hidden' name='act' value='save_first'>
            <label>App Name</label><input name='app_name' value='{db["settings"]["app_name"]}'>
            <label>App Logo (Base64) - গ্যালারি থেকে নিতে নিচের ফাইল ইনপুট ব্যবহার করুন</label>
            <input type='file' id='logoFile' accept='image/*'>
            <input type='hidden' name='app_logo' id='logoHidden'>
            <img id='logoPrev' src='{db["settings"]["app_logo"]}' style='width:60px;height:60px;margin-top:8px;border-radius:12px;display:{'block' if db["settings"]["app_logo"] else 'none'}'>
            <label style='margin-top:12px;display:block'>Sponsored Box - Title</label><input name='spon_title' value='{db["settings"]["spon_title"]}'>
            <label>Description (বড় বক্সে যা লিখবেন)</label><textarea name='spon_desc' rows='3'>{db["settings"]["spon_desc"]}</textarea>
            <label>Button Text</label><input name='spon_btn' value='{db["settings"]["spon_btn"]}'>
            <label>Button Link</label><input name='spon_link' value='{db["settings"]["spon_link"]}'>
            <button style='background:#8b5cf6;color:#fff;width:100%;padding:10px;border:none;border-radius:8px;margin-top:10px'>Save First Page</button>
        </form>
    </div>
    <div class='card'><h4>2nd Page - Tasks</h4>
        <form method='post'><input type='hidden' name='act' value='add_task'><input name='title' placeholder='Title' required><input name='link' placeholder='Link' required><input name='reward' type='number' value='20'><input name='icon' value='📢'><button style='background:#8b5cf6;color:#fff;width:100%;padding:8px;border:none;border-radius:8px;margin-top:6px'>Add Task</button></form>
        <table style='width:100%;margin-top:10px'><tr><th>ID</th><th>Title</th><th>Reward</th><th>Action</th></tr>{rows}</table>
    </div>
    <a href='/' style='color:#8b5cf6'>← App</a>
    <script>
        document.getElementById('logoFile').addEventListener('change',function(e){{
            let r=new FileReader(); r.onload=function(ev){{document.getElementById('logoHidden').value=ev.target.result; document.getElementById('logoPrev').src=ev.target.result; document.getElementById('logoPrev').style.display='block';}}; r.readAsDataURL(e.target.files[0]);
        }});
    </script>
    </body></html>
    """)

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
.spon-big{background:linear-gradient(135deg,#0F1429,#1A1F3D);border:1px dashed #f59e0b;border-radius:16px;padding:16px;margin:12px}
</style></head><body>
<div style='padding:12px 16px;display:flex;justify-content:space-between;align-items:center;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b'>
<div style='display:flex;align-items:center;gap:10px'>
<div id='appLogo' style='width:36px;height:36px;border-radius:10px;background:#1e293b;display:flex;align-items:center;justify-content:center;border:1px solid #8b5cf6;overflow:hidden'>💎</div>
<b id='appName'>Premium App</b>
</div>
<b id='bal' style='color:#22c55e'>৳0</b>
</div>

<div id='p-home' class='page active'>
<div class='glass'><div style='display:flex;justify-content:space-between'><div><small id='levelTxt' style='color:#a78bfa'>Diamond Member • Level 3</small><br><b>Good Evening, <span id='uName'>User</span>!</b></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2></div></div><div style='margin-top:8px;font-size:11px;opacity:.6'><span>Total Earned: <b id='total' style='color:#fff'>৳0</b></span> • <span>Level Progress: <b id='nextLvl'>0%</b></span></div></div>
<div style='display:flex;gap:10px;margin:0 12px'><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><div style='width:36px;height:36px;background:#8b5cf6;border-radius:8px;display:flex;align-items:center;justify-content:center'>📢</div><b style='display:block;margin:6px 0;font-size:13px'>Company Ads</b><button class='btn' style='padding:8px;font-size:12px' onclick='doAd("c")'>Start Earning</button></div><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><div style='width:36px;height:36px;background:#f59e0b;border-radius:8px;display:flex;align-items:center;justify-content:center'>▶️</div><b style='display:block;margin:6px 0;font-size:13px'>Popup Ads</b><button class='btn btn2' style='padding:8px;font-size:12px' onclick='doAd("p")'>Watch & Earn</button></div></div>
<div class='glass'><h4>💸 Withdraw <span style='float:right;font-size:10px;background:#16a34a30;color:#4ade80;padding:3px 8px;border-radius:8px'>Secure</span></h4><div style='display:flex;gap:8px;margin:10px 0'><div class='meth on' id='mBk' onclick='setM("bKash")'>bKash</div><div class='meth' id='mNa' onclick='setM("Nagad")'>Nagad</div></div><input id='wNum' placeholder='01XXXXXXXXX'><input id='wAmt' type='number' placeholder='Amount Min 300'><button class='btn' style='background:linear-gradient(135deg,#6366f1,#8b5cf6)' onclick='doWd()'>Withdraw Now</button><div id='wH' style='margin-top:10px'></div></div>

<div class='spon-big'>
<div style='display:flex;justify-content:space-between;align-items:flex-start'>
<div style='flex:1'><small style='background:#f59e0b;color:#000;padding:3px 8px;border-radius:6px;font-size:10px;font-weight:800'>SPONSORED</small><br><b id='sponTitle' style='font-size:16px;display:block;margin:6px 0'>Company Ads Box</b><small id='sponDesc' style='opacity:.7;font-size:12px;line-height:1.4'>Best earning offer - Click to explore now!</small></div>
<button id='sponBtn' style='background:#8b5cf6;color:#fff;border:none;padding:10px 18px;border-radius:10px;font-weight:700;margin-left:10px'>Explore</button>
</div>
</div>

</div>

<div id='p-tasks' class='page'><div class='glass'><h4>🎯 Tasks & Company Links</h4><div id='tList'></div></div></div>
<div id='p-refer' class='page'><div class='glass'><h4>👥 Refer & Earn</h4><input id='rLink' readonly><button class='btn' onclick='copyR()'>Copy Link</button><div id='rList' style='margin-top:10px'></div></div></div>
<div id='p-support' class='page'><div class='glass'><h4>💎 Support</h4><button class='btn' onclick='window.open("https://t.me/","_blank")'>Telegram</button><button class='btn btn2' onclick='window.open("https://wa.me/","_blank")'>WhatsApp</button></div></div>
<div id='p-profile' class='page'><div class='glass' style='text-align:center'><div id='pImg' style='width:70px;height:70px;margin:0 auto;background:#1e293b;border-radius:18px;display:flex;align-items:center;justify-content:center;border:2px solid #8b5cf6;font-size:30px;overflow:hidden'>💎</div><h3 id='pName' style='margin-top:8px'>User</h3><input id='eName' placeholder='নতুন নাম'><input type='file' id='fImg' accept='image/*'><button class='btn' onclick='saveP()'>Save</button></div></div>

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
let curM='bKash', sponLink='#'
function setM(m){curM=m;document.querySelectorAll('.meth').forEach(x=>x.classList.remove('on'));document.getElementById(m=='bKash'?'mBk':'mNa').classList.add('on')}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,ref:ref})}).then(r=>r.json()).then(d=>{
document.getElementById('bal').innerText='৳'+d.user.bal;document.getElementById('bal2').innerText='৳'+d.user.bal;document.getElementById('uName').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('total').innerText='৳'+d.user.total;
document.getElementById('appName').innerText=d.s.app_name;
document.getElementById('sponTitle').innerText=d.s.spon_title;document.getElementById('sponDesc').innerText=d.s.spon_desc;document.getElementById('sponBtn').innerText=d.s.spon_btn; sponLink=d.s.spon_link;
if(d.s.app_logo){document.getElementById('appLogo').innerHTML='<img src="'+d.s.app_logo+'" style="width:100%;height:100%;object-fit:cover">'}
document.getElementById('levelTxt').innerText='Diamond Member • Level '+d.level;
document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div class='task-card'><div style='display:flex;gap:10px;align-items:center'><div style='font-size:20px'>${t.icon}</div><div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;
let wh='';d.wds.forEach(w=>{wh+=`<div style='padding:6px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #1e293b'><span>${w.m} ৳${w.amt}</span><span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:8px'>${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh;
document.getElementById('rList').innerHTML=d.user.refl.map(r=>`<div style='padding:6px;font-size:12px'>👤 ${r}</div>`).join('')||'No refer';
})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doAd(t){fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doWd(){let num=document.getElementById('wNum').value,amt=document.getElementById('wAmt').value;fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,m:curM,num:num,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function saveP(){let n=document.getElementById('eName').value;let f=document.getElementById('fImg').files[0];if(f){let rd=new FileReader();rd.onload=e=>{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:e.target.result})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})};rd.readAsDataURL(f)}else{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
function copyR(){let i=document.getElementById('rLink');i.select();document.execCommand('copy');alert('Copied')}
document.getElementById('sponBtn').onclick=()=>{if(sponLink) window.open(sponLink,'_blank')}
load()
</script></body></html>
    """)

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
