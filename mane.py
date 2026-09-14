import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={
        "app_name":"SHIBLI👑 NOMAN✅","app_logo":"","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,
        "spon_title":"🔥 আজকের সেরা অফার - বড় বিজ্ঞাপন!",
        "spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন এবং আপনার বোনাস নিন। সীমিত সময়ের জন্য এই অফার - মিস করবেন না!",
        "spon_btn":"Explore Now →","spon_link":"https://google.com",
        "ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% লাইফটাইম কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• বন্ধুর প্রতি Ads থেকে ১৫%\n• Min Withdraw ৳৩০০\n• Instant Payment","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০ বোনাস!",
        "sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com",
        "sup_notice":"⚠️ গুরুত্বপূর্ণ নোটিশ: রাত ১০টার পর Withdraw বন্ধ। সকাল ৯টায় চালু হবে।","sup_faq1_q":"Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটে পাবেন।","sup_faq2_q":"Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই সাথে সাথে।","sup_faq3_q":"Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN ব্যবহার করবেন না।","sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান\n3. VPN নিষেধ\n4. দিনে ৫০টা Company Ads",
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
                if request.form.get(k): db["settings"][k]=request.form.get(k)
            if request.form.get('app_logo'): db["settings"]["app_logo"]=request.form.get('app_logo')
        save_db(db)
    rows="".join([f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']}</td><td>৳{t['reward']}</td><td><form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button style='background:red;color:#fff;border:none;padding:4px 8px;border-radius:6px'>Del</button></form></td></tr>" for t in db["tasks"]])
    s=db["settings"]
    return render_template_string(f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui;max-width:600px;margin:auto}}.card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px;border:1px solid #1e293b}} input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}</style></head><body><h3>Admin</h3><div class='card'><form method='post'><input type='hidden' name='act' value='save_first'><label>App Name</label><input name='app_name' value='{s["app_name"]}'><input type='file' id='logoFile' accept='image/*'><input type='hidden' name='app_logo' id='logoHidden'><label>Spon Title (Big)</label><input name='spon_title' value='{s["spon_title"]}'><textarea name='spon_desc' rows='3'>{s["spon_desc"]}</textarea><input name='spon_btn' value='{s["spon_btn"]}'><input name='spon_link' value='{s["spon_link"]}'><h4>Refer Page</h4><input name='ref_title' value='{s["ref_title"]}'><input name='ref_desc' value='{s["ref_desc"]}'><textarea name='ref_rules' rows='3'>{s["ref_rules"]}</textarea><input name='ref_banner' value='{s["ref_banner"]}'><h4>Support Page</h4><input name='sup_tg' value='{s["sup_tg"]}'><input name='sup_wa' value='{s["sup_wa"]}'><textarea name='sup_notice' rows='3'>{s["sup_notice"]}</textarea><textarea name='sup_rules' rows='3'>{s["sup_rules"]}</textarea><button style='background:#8b5cf6;color:#fff;width:100%;padding:10px;border:none;border-radius:8px;margin-top:10px'>Save All</button></form></div><div class='card'><table style='width:100%'><tr><th>ID</th><th>Title</th><th>Del</th></tr>{rows}</table><form method='post'><input type='hidden' name='act' value='add_task'><input name='title' placeholder='Title' required><input name='link' placeholder='Link' required><input name='reward' type='number' value='20'><input name='icon' value='📢'><button style='background:#8b5cf6;color:#fff;width:100%;padding:8px;border:none;border-radius:8px;margin-top:6px'>Add Task</button></form></div><a href='/' style='color:#8b5cf6'>← App</a><script>document.getElementById('logoFile')?.addEventListener('change',function(e){{let r=new FileReader(); r.onload=function(ev){{document.getElementById('logoHidden').value=ev.target.result;}}; r.readAsDataURL(e.target.files[0]);}});</script></body></html>")

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
.spon-big{background:linear-gradient(135deg,#1A1033 0%, #2D1B4E 50%, #1A1429 100%);border:1.5px solid #f59e0b;border-radius:22px;padding:20px;margin:12px;position:relative;box-shadow:0 0 40px rgba(245,158,11,.2);min-height:130px}
.sup-card{display:flex;align-items:center;gap:12px;padding:14px;background:#0F1429;border:1px solid #1e293b;border-radius:14px;margin-top:10px}
</style></head><body>
<div style='padding:12px 16px;display:flex;justify-content:space-between;align-items:center;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b'>
<div style='display:flex;align-items:center;gap:10px'><div id='appLogo' style='width:38px;height:38px;border-radius:12px;background:#1e293b;display:flex;align-items:center;justify-content:center;border:1.5px solid #8b5cf6;overflow:hidden'>💎</div><b id='appName'>Premium App</b></div><b id='bal' style='color:#22c55e'>৳0</b></div>

<div id='p-home' class='page active'>
<div class='glass'><div style='display:flex;justify-content:space-between'><div><small id='levelTxt' style='color:#a78bfa'>Level 1</small><br><b>Good Evening, <span id='uName'>User</span>!</b></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2></div></div><div style='margin-top:8px;font-size:11px;opacity:.6'>Total: <b id='total' style='color:#fff'>৳0</b></div></div>
<div style='display:flex;gap:10px;margin:0 12px'><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><b style='font-size:13px'>Company Ads</b><button class='btn' style='padding:8px;font-size:12px' onclick='doAd("c")'>Start Earning</button></div><div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><b style='font-size:13px'>Popup Ads</b><button class='btn btn2' style='padding:8px;font-size:12px' onclick='doAd("p")'>Watch & Earn</button></div></div>
<div class='glass'><h4>💸 Withdraw</h4><div style='display:flex;gap:8px;margin:10px 0'><div class='meth on' id='mBk' onclick='setM("bKash")'>bKash</div><div class='meth' id='mNa' onclick='setM("Nagad")'>Nagad</div></div><input id='wNum' placeholder='01XXXXXXXXX'><input id='wAmt' type='number' placeholder='Amount Min 300'><button class='btn' style='background:linear-gradient(135deg,#6366f1,#8b5cf6)' onclick='doWd()'>Withdraw Now</button><div id='wH' style='margin-top:10px'></div></div>

<div class='spon-big'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'><small style='background:#f59e0b;color:#000;padding:5px 12px;border-radius:8px;font-size:11px;font-weight:900'>🔥 SPONSORED • BIG AD</small></div>
<b id='sponTitle' style='font-size:19px;display:block;line-height:1.3'>🔥 আজকের সেরা অফার!</b>
<p id='sponDesc' style='font-size:14px;opacity:.85;margin:10px 0 16px;line-height:1.6'>বর্ণনা</p>
<button id='sponBtn' style='width:100%;background:linear-gradient(135deg,#f59e0b,#f97316);color:#fff;border:none;padding:14px;border-radius:12px;font-weight:900;font-size:14px'>Explore Now →</button>
</div>
</div>

<div id='p-tasks' class='page'><div class='glass'><h4>🎯 Tasks & Company Links</h4><div id='tList'></div></div></div>

<div id='p-refer' class='page'>
<div style='margin:12px;background:linear-gradient(135deg,#f59e0b,#f97316);border-radius:16px;padding:14px;text-align:center;color:#000;font-weight:800;font-size:13px' id='refBanner'>🎉 Refer Contest</div>
<div class='glass'>
<h3 id='refTitle'>👥 Refer & Earn Unlimited</h3>
<p id='refDesc' style='font-size:13px;opacity:.7;margin:8px 0'>প্রতি রেফারে ৳৮০ + ১৫% কমিশন!</p>
<div style='display:flex;gap:8px;margin:12px 0'>
<div style='flex:1;background:#0B0E1C;padding:12px;border-radius:12px;text-align:center;border:1px solid #1e293b'><b style='font-size:18px;color:#8b5cf6' id='rCount'>0</b><br><small>Total Refer</small></div>
<div style='flex:1;background:#0B0E1C;padding:12px;border-radius:12px;text-align:center;border:1px solid #1e293b'><b style='font-size:18px;color:#22c55e' id='rEarn'>৳0</b><br><small>Earned</small></div>
<div style='flex:1;background:#0B0E1C;padding:12px;border-radius:12px;text-align:center;border:1px solid #1e293b'><b style='font-size:18px;color:#f59e0b'>15%</b><br><small>Commission</small></div>
</div>
<input id='rLink' readonly style='font-size:12px'><button class='btn' onclick='copyR()'>🔗 Copy Refer Link</button>
<button class='btn' style='background:#0B0E1C;border:1px solid #1e293b' onclick='copyR()'>📤 Share Now</button>
</div>
<div class='glass'>
<h4>📋 How Refer Works</h4>
<pre id='refRules' style='white-space:pre-wrap;font-family:system-ui;font-size:13px;opacity:.8;margin-top:8px;line-height:1.6'>Rules</pre>
</div>
<div class='glass'>
<h4>👥 My Refer List</h4>
<div id='rList' style='margin-top:8px'></div>
</div>
<div class='glass' style='background:linear-gradient(135deg,#1e293b,#0f172a);border:1px dashed #8b5cf6'>
<h4>🏆 Top Referrers (This Week)</h4>
<div style='margin-top:8px;font-size:12px'><div style='display:flex;justify-content:space-between;padding:6px'><span>🥇 SHIBLI - 152 Refer</span><span style='color:#22c55e'>৳12160</span></div><div style='display:flex;justify-content:space-between;padding:6px'><span>🥈 Noman - 98 Refer</span><span style='color:#22c55e'>৳7840</span></div></div>
</div>
</div>

<div id='p-support' class='page'>
<div class='glass'><h3 id='supTitle'>💎 Support Center</h3><p id='supDesc' style='font-size:12px;opacity:.7;margin:6px 0'></p></div>
<div class='glass'><h4>📞 Contact Us</h4>
<div class='sup-card' onclick='window.open(document.getElementById("supTgLink").value,"_blank")'><div style='width:40px;height:40px;background:#229ED9;border-radius:10px;display:flex;align-items:center;justify-content:center'>✈️</div><div><b>Telegram</b><br><small style='opacity:.6'>Join channel</small></div><span style='margin-left:auto'>→</span></div>
<div class='sup-card' onclick='window.open(document.getElementById("supWaLink").value,"_blank")'><div style='width:40px;height:40px;background:#25D366;border-radius:10px;display:flex;align-items:center;justify-content:center'>💬</div><div><b>WhatsApp</b><br><small style='opacity:.6'>Direct chat</small></div><span style='margin-left:auto'>→</span></div>
</div>
<div class='glass' style='border:1px solid #f59e0b;background:linear-gradient(135deg,#1A1400,#2A1F00)'><h4>📢 Notice Board</h4><p id='supNotice' style='font-size:13px;line-height:1.6;margin-top:8px;white-space:pre-wrap'></p></div>
<div class='glass'><h4>📜 Rules</h4><pre id='supRules' style='white-space:pre-wrap;font-family:system-ui;font-size:12px;opacity:.8;line-height:1.6;margin-top:8px'></pre></div>
<input type='hidden' id='supTgLink'><input type='hidden' id='supWaLink'>
</div>

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
document.getElementById('refTitle').innerText=d.s.ref_title;document.getElementById('refDesc').innerText=d.s.ref_desc;document.getElementById('refRules').innerText=d.s.ref_rules;document.getElementById('refBanner').innerText=d.s.ref_banner;
document.getElementById('supTitle').innerText=d.s.sup_title;document.getElementById('supDesc').innerText=d.s.sup_desc;document.getElementById('supNotice').innerText=d.s.sup_notice;document.getElementById('supRules').innerText=d.s.sup_rules;
document.getElementById('supTgLink').value=d.s.sup_tg;document.getElementById('supWaLink').value=d.s.sup_wa;
if(d.s.app_logo){document.getElementById('appLogo').innerHTML='<img src="'+d.s.app_logo+'" style="width:100%;height:100%;object-fit:cover">'}
document.getElementById('levelTxt').innerText='Diamond Member • Level '+d.level;
document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div class='task-card'><div style='display:flex;gap:10px;align-items:center'><div style='font-size:20px'>${t.icon}</div><div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;
document.getElementById('rCount').innerText=d.user.refl.length;document.getElementById('rEarn').innerText='৳'+(d.user.refl.length*d.s.ref);
let wh='';d.wds.forEach(w=>{wh+=`<div style='padding:6px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #1e293b'><span>${w.m} ৳${w.amt}</span><span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:8px'>${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh;
document.getElementById('rList').innerHTML=d.user.refl.map(r=>`<div style='padding:8px;font-size:12px;border-bottom:1px solid #1e293b;display:flex;justify-content:space-between'><span>👤 ${r}</span><span style='color:#22c55e'>+৳${d.s.ref}</span></div>`).join('')||'<small style="opacity:.5">No refer yet - Share your link!</small>';
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
