import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={
        "app_name":"SHIBLI👑 NOMAN✅","app_logo":"","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,
        "spon_title":"🔥 আজকের সেরা অফার - বড় বিজ্ঞাপন!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন!","spon_btn":"Explore Now →","spon_link":"https://google.com",
        "ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• ১৫% কমিশন","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০!",
        "sup_title":"💎 Support Center","sup_desc":"২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com","sup_notice":"⚠️ রাত ১০টার পর Withdraw বন্ধ।","sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান",
        "sup_faq1_q":"Withdraw কতক্ষণে?","sup_faq1_a":"৫-৩০ মিনিটে","sup_faq2_q":"Refer টাকা?","sup_faq2_a":"সাথে সাথে","sup_faq3_q":"Ads টাকা আসে না?","sup_faq3_a":"VPN ব্যবহার করবেন না",
        # 5th Page - Profile NEW
        "pro_title":"👤 My Profile",
        "pro_notice":"💎 Diamond Member - আপনি Level 3 এ আছেন। বেশি বেশি Ads দেখুন আর Level বাড়ান!",
        "pro_ver":"Version 2.5 - Premium",
        "levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]
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
    for i,th in enumerate(levels):
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
    nxt=db["settings"]["levels"][lvl] if lvl < len(db["settings"]["levels"]) else db["settings"]["levels"][-1]
    prog=int((u["total"]/nxt*100)) if nxt>0 else 0
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds,"level":lvl,"next":nxt,"prog":prog})

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
    u["ads"]+=1;save_db(db);return jsonify({"msg":"Added"})
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
            for k in db["settings"]:
                if request.form.get(k) is not None and request.form.get(k)!='': db["settings"][k]=request.form.get(k)
            if request.form.get('app_logo'): db["settings"]["app_logo"]=request.form.get('app_logo')
        save_db(db)
    rows="".join([f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']}</td><td>Del</td></tr>" for t in db["tasks"]])
    s=db["settings"]
    return render_template_string(f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui;max-width:600px;margin:auto}}.card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px;border:1px solid #1e293b}} input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}</style></head><body><h3>Admin - All Pages</h3><div class='card'><form method='post'><input type='hidden' name='act' value='save_first'><input name='app_name' value='{s["app_name"]}'><input type='file' id='logoFile' accept='image/*'><input type='hidden' name='app_logo' id='logoHidden'><textarea name='spon_desc' rows='2'>{s["spon_desc"]}</textarea><input name='ref_banner' value='{s["ref_banner"]}'><input name='sup_notice' value='{s["sup_notice"]}'><h4>5th Page Profile</h4><input name='pro_title' value='{s["pro_title"]}'><textarea name='pro_notice' rows='2'>{s["pro_notice"]}</textarea><input name='pro_ver' value='{s["pro_ver"]}'><button style='background:#8b5cf6;color:#fff;width:100%;padding:10px;border:none;border-radius:8px;margin-top:10px'>Save All</button></form></div><a href='/' style='color:#8b5cf6'>← App</a><script>document.getElementById('logoFile')?.addEventListener('change',function(e){{let r=new FileReader(); r.onload=function(ev){{document.getElementById('logoHidden').value=ev.target.result;}}; r.readAsDataURL(e.target.files[0]);}});</script></body></html>")

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
.spon-big{background:linear-gradient(135deg,#1A1033,#2D1B4E);border:1.5px solid #f59e0b;border-radius:22px;padding:20px;margin:12px}
.stat-box{flex:1;background:#0B0E1C;padding:12px;border-radius:12px;text-align:center;border:1px solid #1e293b}
</style></head><body>
<div style='padding:12px 16px;display:flex;justify-content:space-between;align-items:center;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b'>
<div style='display:flex;align-items:center;gap:10px'><div id='appLogo' style='width:38px;height:38px;border-radius:12px;background:#1e293b;display:flex;align-items:center;justify-content:center;border:1.5px solid #8b5cf6;overflow:hidden'>💎</div><b id='appName'>Premium App</b></div><b id='bal' style='color:#22c55e'>৳0</b></div>

<div id='p-home' class='page active'>
<div class='glass'><div style='display:flex;justify-content:space-between'><div><small id='levelTxt' style='color:#a78bfa'>Level 1</small><br><b>Good Evening, <span id='uName'>User</span>!</b></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2></div></div></div>
<div style='display:flex;gap:10px;margin:0 12px'><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><b style='font-size:13px'>Company Ads</b><button class='btn' style='padding:8px;font-size:12px' onclick='doAd("c")'>Start</button></div><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><b style='font-size:13px'>Popup Ads</b><button class='btn btn2' style='padding:8px;font-size:12px' onclick='doAd("p")'>Watch</button></div></div>
<div class='glass'><h4>💸 Withdraw</h4><div style='display:flex;gap:8px;margin:10px 0'><div class='meth on' id='mBk' onclick='setM("bKash")'>bKash</div><div class='meth' id='mNa' onclick='setM("Nagad")'>Nagad</div></div><input id='wNum' placeholder='01XXXXXXXXX'><input id='wAmt' type='number' placeholder='Min 300'><button class='btn' onclick='doWd()'>Withdraw Now</button><div id='wH' style='margin-top:10px'></div></div>
<div class='spon-big'><b id='sponTitle' style='font-size:18px;display:block'>Offer</b><p id='sponDesc' style='font-size:13px;opacity:.8;margin:8px 0'>Desc</p><button id='sponBtn' style='width:100%;background:#f59e0b;color:#000;border:none;padding:12px;border-radius:10px;font-weight:900'>Explore</button></div>
</div>

<div id='p-tasks' class='page'><div class='glass'><h4>🎯 Tasks</h4><div id='tList'></div></div></div>
<div id='p-refer' class='page'><div style='margin:12px;background:linear-gradient(135deg,#f59e0b,#f97316);border-radius:16px;padding:14px;text-align:center;color:#000;font-weight:800' id='refBanner'>Banner</div><div class='glass'><h3 id='refTitle'>Refer</h3><p id='refDesc' style='font-size:12px;opacity:.7'></p><input id='rLink' readonly><button class='btn' onclick='copyR()'>Copy Link</button><div id='rList' style='margin-top:8px'></div></div></div>
<div id='p-support' class='page'><div class='glass'><h3 id='supTitle'>Support</h3><p id='supDesc' style='font-size:12px;opacity:.7'></p><div style='padding:10px;background:#0F1429;border-radius:10px;margin-top:8px'><p id='supNotice' style='font-size:12px;white-space:pre-wrap'></p></div></div></div>

<div id='p-profile' class='page'>
<div class='glass' style='text-align:center;position:relative;overflow:hidden'>
<div style='position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(135deg,#8b5cf6,#6366f1);opacity:.3'></div>
<div style='position:relative'>
<div id='pImg' style='width:80px;height:80px;margin:0 auto;background:#1e293b;border-radius:22px;display:flex;align-items:center;justify-content:center;border:3px solid #8b5cf6;font-size:32px;overflow:hidden;box-shadow:0 0 20px rgba(139,92,246,.4)'>💎</div>
<div style='background:linear-gradient(135deg,#f59e0b,#f97316);display:inline-block;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:900;color:#000;margin-top:8px' id='pLevelBadge'>Level 1</div>
<h2 id='pName' style='margin-top:8px'>User 4250</h2>
<small id='pJoin' style='opacity:.6'>Join: 2025-01-01</small>
</div>
</div>

<div class='glass'>
<h4>📊 Statistics - Box System</h4>
<div style='display:flex;gap:8px;margin-top:10px'>
<div class='stat-box'><b style='font-size:18px;color:#22c55e' id='pTotal'>৳0</b><br><small>Total Earned</small></div>
<div class='stat-box'><b style='font-size:18px;color:#8b5cf6' id='pBal'>৳0</b><br><small>Balance</small></div>
</div>
<div style='display:flex;gap:8px;margin-top:8px'>
<div class='stat-box'><b style='font-size:18px;color:#f59e0b' id='pAds'>0</b><br><small>Ads Watched</small></div>
<div class='stat-box'><b style='font-size:18px;color:#ec4899' id='pRef'>0</b><br><small>Referrals</small></div>
</div>
</div>

<div class='glass'>
<h4>📈 Level Progress</h4>
<div style='display:flex;justify-content:space-between;font-size:12px;margin:8px 0'><span id='pLevelNow'>Level 1</span><span id='pLevelNext'>Next: ৳500</span></div>
<div style='width:100%;height:10px;background:#0B0E1C;border-radius:20px;overflow:hidden'><div id='pProgBar' style='height:100%;background:linear-gradient(90deg,#8b5cf6,#22c55e);width:0%;border-radius:20px;transition:1s'></div></div>
<small id='pProgTxt' style='opacity:.6;font-size:11px;margin-top:6px;display:block'>0% completed</small>
<div style='margin-top:8px;background:#0B0E1C;padding:10px;border-radius:10px;font-size:11px' id='proNotice'>💎 Diamond Member - Level বাড়ান!</div>
</div>

<div class='glass'>
<h4>⚙️ Account Info - Box</h4>
<div style='background:#0B0E1C;padding:12px;border-radius:12px;margin-top:8px;display:flex;justify-content:space-between;align-items:center'><div><small style='opacity:.6'>User ID</small><br><b id='pUid' style='font-size:12px'>u_123</b></div><button style='background:#8b5cf6;color:#fff;border:none;padding:6px 12px;border-radius:8px;font-size:11px' onclick='navigator.clipboard.writeText(document.getElementById("pUid").innerText);alert("Copied")'>Copy</button></div>
<div style='background:#0B0E1C;padding:12px;border-radius:12px;margin-top:8px'><small style='opacity:.6'>Name Edit</small><input id='eName' placeholder='নতুন নাম' style='margin-top:6px'><input type='file' id='fImg' accept='image/*' style='margin-top:6px'><button class='btn' onclick='saveP()'>💾 Save Profile</button></div>
</div>

<div class='glass'>
<h4>💸 Withdraw History - Profile Box</h4>
<div id='pWhist' style='margin-top:8px'>No history</div>
</div>

<div class='glass' style='background:#0B0E1C;border:1px dashed #1e293b'>
<div style='display:flex;justify-content:space-between;align-items:center'><div><b style='font-size:13px' id='proVer'>Version 2.5</b><br><small style='opacity:.6'>Premium App</small></div><button style='background:#ef444420;color:#ef4444;border:1px solid #ef4444;padding:8px 14px;border-radius:8px;font-size:11px' onclick='localStorage.clear();location.reload()'>Logout</button></div>
</div>

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
let curM='bKash', sponLink='#'
function setM(m){curM=m;document.querySelectorAll('.meth').forEach(x=>x.classList.remove('on'));document.getElementById(m=='bKash'?'mBk':'mNa').classList.add('on')}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,ref:ref})}).then(r=>r.json()).then(d=>{
document.getElementById('bal').innerText='৳'+d.user.bal;document.getElementById('bal2').innerText='৳'+d.user.bal;document.getElementById('uName').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('pJoin').innerText='Join: '+d.user.join;document.getElementById('pUid').innerText=d.user.id;
document.getElementById('pTotal').innerText='৳'+d.user.total;document.getElementById('pBal').innerText='৳'+d.user.bal;document.getElementById('pAds').innerText=d.user.ads||0;document.getElementById('pRef').innerText=d.user.refl.length;
document.getElementById('pLevelBadge').innerText='Level '+d.level;document.getElementById('pLevelNow').innerText='Level '+d.level;document.getElementById('pLevelNext').innerText='Next: ৳'+d.next;document.getElementById('pProgBar').style.width=d.prog+'%';document.getElementById('pProgTxt').innerText=d.prog+'% completed - ৳'+(d.next-d.user.total)+' more for next level';
document.getElementById('appName').innerText=d.s.app_name;document.getElementById('sponTitle').innerText=d.s.spon_title;document.getElementById('sponDesc').innerText=d.s.spon_desc;document.getElementById('sponBtn').innerText=d.s.spon_btn; sponLink=d.s.spon_link;
document.getElementById('refTitle').innerText=d.s.ref_title;document.getElementById('refDesc').innerText=d.s.ref_desc;document.getElementById('refBanner').innerText=d.s.ref_banner;
document.getElementById('supTitle').innerText=d.s.sup_title;document.getElementById('supDesc').innerText=d.s.sup_desc;document.getElementById('supNotice').innerText=d.s.sup_notice;
document.getElementById('proNotice').innerText=d.s.pro_notice;document.getElementById('proVer').innerText=d.s.pro_ver;
if(d.s.app_logo){document.getElementById('appLogo').innerHTML='<img src="'+d.s.app_logo+'" style="width:100%;height:100%;object-fit:cover">'}
document.getElementById('levelTxt').innerText='Diamond Member • Level '+d.level;
document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div class='task-card'><div style='display:flex;gap:10px;align-items:center'><div style='font-size:20px'>${t.icon}</div><div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;
let wh='';d.wds.forEach(w=>{wh+=`<div style='padding:6px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #1e293b'><span>${w.m} ৳${w.amt}</span><span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:8px'>${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh||'<small style="opacity:.5">No history</small>';document.getElementById('pWhist').innerHTML=wh||'<small style="opacity:.5">No withdraw yet</small>';
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
