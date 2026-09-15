import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন!","spon_btn":"🚀 Explore Now","spon_link":"https://google.com","ref_title":"👥 Refer & Earn","ref_desc":"প্রতি রেফারে ৳৮০","ref_rules":"• বন্ধু জয়েন করলে ৳৮০","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০","sup_title":"💎 Support Center","sup_desc":"২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_email":"support@gmail.com","sup_notice":"• রাত ১০টার পর WD বন্ধ\n• ভুয়া রেফার ব্যান","sup_faq1_q":"Withdraw কতক্ষণে?","sup_faq1_a":"৫-৩০ মিনিটে","sup_faq2_q":"Refer টাকা কখন?","sup_faq2_a":"সাথে সাথে","sup_faq3_q":"Ads আসে না কেন?","sup_faq3_a":"VPN বন্ধ করুন","sup_rules":"1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]}
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[{"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},{"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},{"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}]}
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
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c_today":0,"p_today":0,"ad_date":"","diamonds":db["settings"]["bonus"]*100,"join":datetime.now().strftime("%Y-%m-%d"),"refl":[]}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["refl"].append(uid);db["users"][ref]["bal"]+=db["settings"]["ref"]
    return db["users"][uid],False

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')),j.get('ref'));save_db(db)
    lvl=get_level(u["total"], db["settings"]["levels"]);nxt=db["settings"]["levels"][lvl] if lvl < len(db["settings"]["levels"]) else db["settings"]["levels"][-1]
    prog=int((u["total"]/nxt*100)) if nxt>0 else 0
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"level":lvl,"next":nxt,"prog":prog})

@app.route('/api/ads',methods=['POST'])
def handle_ads():
    db=load_db();data=request.json;uid=str(data.get('id') or '');ad_type=str(data.get('type') or 'c')
    user,_=get_user(db,uid);s=db["settings"];today=time.strftime("%Y-%m-%d")
    if user.get("ad_date")!=today: user["ad_date"]=today;user["c_today"]=0;user["p_today"]=0
    if ad_type=='c':
        if user.get("c_today",0)>=int(s.get("clim",50)): return jsonify({"msg":"Ajker Company limit sesh"})
        reward=float(s.get("ad",0.2));user["c_today"]+=1
    else:
        if user.get("p_today",0)>=int(s.get("plim",30)): return jsonify({"msg":"Ajker Popup limit sesh"})
        reward=float(s.get("pop",0.3));user["p_today"]+=1
    user["bal"]=float(user["bal"])+reward;user["total"]=float(user["total"])+reward;user["diamonds"]=int(user["diamonds"])+int(reward*100);save_db(db)
    return jsonify({"msg":f"{reward} Taka Added","bal":user["bal"],"diamonds":user["diamonds"],"c_today":user["c_today"],"p_today":user["p_today"]})

@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
    if amt>=int(s.get("min",500)) and u["bal"]>=amt:
        u["bal"]-=amt;db["wds"].append({"uid":u["id"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending"});save_db(db);return jsonify({"msg":"Withdraw success"})
    return jsonify({"msg":f"Min {s.get('min')} Taka lagbe"})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        act=request.form.get('act')
        if act=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif act=='del_task':
            db["tasks"]=[t for t in db["tasks"] if str(t["id"])!=str(request.form.get('id'))]
        elif act=='save_all':
            for k in list(db["settings"].keys()):
                v=request.form.get(k)
                if v not in (None,''): db["settings"][k]=v
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='display:flex;justify-content:space-between;background:#0B0E1C;padding:8px;margin:4px;border-radius:8px'>{t['icon']} {t['title']} ৳{t['reward']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return render_template_string(f"<style>body{{background:#0B0E1C;color:#fff;padding:14px;max-width:800px;margin:auto}}.card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px}} input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333;margin-top:6px}} button{{background:#8b5cf6;color:#fff;padding:8px 14px;border:none;border-radius:8px}}</style><div class='card'><h2>Admin - সব কন্ট্রোল</h2>Company: {s['company_ad_id']} | Popup: {s['popup_ad_id']}</div><form method='post' class='card'><input type='hidden' name='act' value='save_all'>App Name <input name='app_name' value=\"{s['app_name']}\"> AD <input name='ad' value=\"{s['ad']}\"> POP <input name='pop' value=\"{s['pop']}\"> Company ID <input name='company_ad_id' value=\"{s['company_ad_id']}\"> Popup ID <input name='popup_ad_id' value=\"{s['popup_ad_id']}\"> Direct <input name='direct_link' value=\"{s['direct_link']}\"><br><br><button style='width:100%;padding:12px'>SAVE ALL</button></form><div class='card'><h3>Tasks - বিভিন্ন কোম্পানি Add করুন (YouTube, FB, Website)</h3>{rows}<form method='post'><input type='hidden' name='act' value='add_task'>Title <input name='title' placeholder='YouTube Subscribe'> Reward <input name='reward' placeholder='25'> Link <input name='link' placeholder='https://...'> Icon <input name='icon' value='🔗'><button>Add Task</button></form></div>")

@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='https://telegram.org/js/telegram-web-app.js'></script>
<script src='https://libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
<script src='https://libtl.com/sdk.js' data-zone='{{ s["popup_ad_id"] }}' data-sdk='show_{{ s["popup_ad_id"] }}'></script>
<style>
body{margin:0;background:#0A0D1E;color:#fff;font-family:system-ui;padding:0 12px 100px}
.card{background:#151A2D;border:1px solid #1e293b;border-radius:20px;padding:14px;margin:12px 0}
.b{width:100%;padding:14px;border-radius:14px;background:{{s["primary"]}};color:#fff;border:none;font-weight:700;font-size:15px}
.by{background:{{s["secondary"]}};color:#000}.bd{background:#0B0E1C;border:1px solid #333}
.nav{position:fixed;bottom:0;left:0;right:0;background:#151A2D;display:flex;justify-content:space-around;padding:14px 0;border-top:1px solid #1e293b;z-index:999}
.nav div{opacity:.7;text-align:center;font-size:13px;font-weight:600;padding:8px 12px;border-radius:12px;min-width:58px;cursor:pointer}.nav div.active{opacity:1;color:#fff;background:{{s["primary"]}}}
.tab{display:none}.tab.active{display:block}
input{width:100%;padding:12px;border-radius:12px;background:#0B0E1C;color:#fff;border:1px solid #333;box-sizing:border-box;margin-top:8px}
.task-item{background:#0B0E1C;padding:12px;margin:8px 0;border-radius:14px;display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<div style='display:flex;gap:8px;padding:12px 0;align-items:center'><div class='card' style='margin:0;padding:10px 16px'>💎</div><div class='card' style='margin:0;flex:1'>👑 {{s["app_name"]}}</div><div class='card' style='margin:0;flex:1;border:1px solid #f59e0b'>{{s["app_name2"]}}</div><div id='balTop' style='color:#00ff88;font-weight:700'>৳0</div></div>

<div id='tab-home' class='tab active'>
<div class='card'><div style='display:flex;justify-content:space-between'><span style='color:#8b5cf6'>Diamond Member • Level <span id='lvl'>1</span></span><span>Total Balance</span></div><h2>Good Evening, <span id='uname'>User</span>!</h2><div style='display:flex;justify-content:space-between'><span>💎 <span id='dia'>0</span> Diamond</span><span style='color:#0f0;font-size:22px'>৳<span id='bal'>0</span></span></div></div>
<div style='display:flex;gap:10px'><div class='card' style='flex:1'>Company Ads ৳{{s["ad"]}}<br><small id='cCount'>0/{{s["clim"]}}</small><button class='b' onclick='watchAd("c")'>Start - ৳{{s["ad"]}}</button></div><div class='card' style='flex:1'>Popup Ads ৳{{s["pop"]}}<br><small id='pCount'>0/{{s["plim"]}}</small><button class='b by' onclick='watchAd("p")'>Watch - ৳{{s["pop"]}}</button></div></div>
<div class='card'><h3 style='margin:0 0 10px'>🏢 Company Tasks - বিভিন্ন কোম্পানি</h3><div id='homeTaskList'></div><small style='color:#888'>Admin Panel থেকে Add করলে এখানে বিভিন্ন কোম্পানি আসবে</small></div>
<div class='card'><h3>💸 Withdraw</h3><div style='display:flex;gap:8px'><button class='b bd'>bKash</button><button class='b bd'>Nagad</button></div><input id='wdNum' placeholder='01XXXXXXXXX'><input id='wdAmt' type='number' placeholder='Min {{s["min"]}} Taka'><button class='b' onclick='doWD()'>Withdraw Now</button></div>
<div class='card' style='background:#2d1b69;border:1px solid #f59e0b'><span style='background:#f59e0b;color:#000;padding:4px 12px;border-radius:20px;font-size:12px'>SPONSORED BIGGEST AD</span><h2>🔥 {{s["spon_title"]}}</h2><p>{{s["spon_desc"]}}</p><button class='b by' onclick='Telegram.WebApp.openLink(S.spon_link)'>{{s["spon_btn"]}}</button></div>
</div>

<div id='tab-tasks' class='tab'><div class='card'><h2>🎯 Tasks & Company Links</h2><div id='taskList'></div></div></div>
<div id='tab-refer' class='tab'><div class='card' style='background:#f59e0b;color:#000;text-align:center'>{{s["ref_banner"]}}</div><div class='card'><h2>{{s["ref_title"]}}</h2><div id='refLink' class='card bd' style='word-break:break-all'></div><button class='b' onclick='navigator.clipboard.writeText(document.getElementById("refLink").innerText);alert("Copied")'>Copy</button></div></div>
<div id='tab-support' class='tab'><div class='card'><h2>{{s["sup_title"]}}</h2><div style='display:flex;gap:8px'><button class='b' onclick='Telegram.WebApp.openLink(S.sup_tg)'>Telegram</button><button class='b by' onclick='Telegram.WebApp.openLink(S.sup_wa)'>WhatsApp</button></div></div></div>
<div id='tab-profile' class='tab'><div class='card' style='text-align:center'><div style='font-size:50px'>💎</div><h2 id='pName'>User</h2><p>💎 <span id='pDia'>0</span> | ৳<span id='pBal'>0</span></p><p>Level <span id='pLvl'>1</span> | Join <span id='pJoin'></span></p></div><div class='card'><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'><div class='card bd' style='text-align:center;margin:0'>৳<span id='sEarn'>0</span><br>Total</div><div class='card bd' style='text-align:center;margin:0'>৳<span id='sBal'>0</span><br>Bal</div></div></div></div>

<div class='nav'><div id='n-home' class='active' onclick="openTab('home')">🏠<br>Home</div><div id='n-tasks' onclick="openTab('tasks')">🎯<br>Tasks</div><div id='n-refer' onclick="openTab('refer')">👥<br>Refer</div><div id='n-support' onclick="openTab('support')">💬<br>Support</div><div id='n-profile' onclick="openTab('profile')">👤<br>Profile</div></div>

<script>
const S={{s|tojson}};
function openTab(n){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('active'));document.getElementById('tab-'+n).classList.add('active');document.getElementById('n-'+n).classList.add('active')}
function watchAd(t){let fn='show_'+(t=='c'?S.company_ad_id:S.popup_ad_id); if(typeof window[fn]=='function'){window[fn]().then(()=>{fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,type:t})}).then(r=>r.json()).then(d=>{document.getElementById('bal').innerText=d.bal;document.getElementById('balTop').innerText='৳'+d.bal; alert(d.msg)})})}else{alert('Ad loading... Zone:'+(t=='c'?S.company_ad_id:S.popup_ad_id))}}
function doWD(){fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,amt:document.getElementById('wdAmt').value,num:document.getElementById('wdNum').value,m:'bKash'})}).then(r=>r.json()).then(d=>alert(d.msg))}
fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id})}).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.bal;document.getElementById('balTop').innerText='৳'+d.user.bal;document.getElementById('sBal').innerText=d.user.bal;document.getElementById('pBal').innerText=d.user.bal;document.getElementById('sEarn').innerText=d.user.total;document.getElementById('dia').innerText=d.user.diamonds;document.getElementById('pDia').innerText=d.user.diamonds;document.getElementById('uname').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('lvl').innerText=d.level;document.getElementById('pLvl').innerText=d.level;document.getElementById('pJoin').innerText=d.user.join;document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id;document.getElementById('cCount').innerText=(d.user.c_today||0)+'/'+S.clim+' today';document.getElementById('pCount').innerText=(d.user.p_today||0)+'/'+S.plim+' today';
  let h='';d.tasks.forEach(t=>{h+=`<div class='task-item'><div>${t.icon} ${t.title}<br><small style='color:#0f0'>৳${t.reward}</small></div><button style='width:auto;padding:8px 16px;background:#8b5cf6;border:none;border-radius:10px;color:#fff' onclick="Telegram.WebApp.openLink('${t.link}')">Go</button></div>`});document.getElementById('taskList').innerHTML=h;document.getElementById('homeTaskList').innerHTML=h;
})
</script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
