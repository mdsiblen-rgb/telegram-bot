import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার","spon_desc":"প্রতিদিন ৫০০ টাকা ইনকাম করুন","spon_btn":"🚀 Explore Now","spon_link":"https://google.com","ref_banner":"🎉 Refer Contest","ref_title":"👥 Refer & Earn","ref_desc":"প্রতি রেফারে ৳৮০","sup_title":"💎 Support Center","sup_desc":"২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_email":"support@gmail.com","sup_notice":"• রাত ১০টার পর WD বন্ধ","levels":[0,500,2000,5000,10000]}
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[{"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},{"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},{"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    db=json.load(open(DB,'r',encoding='utf-8'))
    for k,v in d.items():
        if k not in db["settings"]: db["settings"][k]=v
    return db

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
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
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"]})

@app.route('/api/ads',methods=['POST'])
def handle_ads():
    db=load_db();data=request.json;uid=str(data.get('id') or '');ad_type=str(data.get('type') or 'c')
    user,_=get_user(db,uid);s=db["settings"];today=time.strftime("%Y-%m-%d")
    if user.get("ad_date")!=today: user["ad_date"]=today;user["c_today"]=0;user["p_today"]=0
    if ad_type=='c':
        if user.get("c_today",0)>=int(s.get("clim",50)): return jsonify({"msg":"Limit sesh"})
        reward=float(s.get("ad",0.2));user["c_today"]+=1
    else:
        if user.get("p_today",0)>=int(s.get("plim",30)): return jsonify({"msg":"Limit sesh"})
        reward=float(s.get("pop",0.3));user["p_today"]+=1
    user["bal"]=float(user["bal"])+reward;user["total"]=float(user["total"])+reward;user["diamonds"]+=int(reward*100);save_db(db)
    return jsonify({"msg":f"{reward} Taka Added","bal":user["bal"],"diamonds":user["diamonds"],"c_today":user["c_today"],"p_today":user["p_today"]})

@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
    if amt>=int(s.get("min",500)) and u["bal"]>=amt:
        u["bal"]-=amt;save_db(db);return jsonify({"msg":"Withdraw success"})
    return jsonify({"msg":f"Min {s.get('min')} Taka lagbe"})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        if request.form.get('act')=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif request.form.get('act')=='del_task':
            db["tasks"]=[t for t in db["tasks"] if str(t["id"])!=str(request.form.get('id'))]
        else:
            for k in db["settings"].keys():
                v=request.form.get(k)
                if v: db["settings"][k]=v
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='background:#0B0E1C;padding:8px;margin:4px;border-radius:8px;display:flex;justify-content:space-between'>{t['icon']} {t['title']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return f"<body style='background:#0B0E1C;color:#fff;padding:14px'><h2>Admin</h2>Company ID: {s['company_ad_id']} | Popup ID: {s['popup_ad_id']}<form method='post'><input name='company_ad_id' value='{s['company_ad_id']}' placeholder='Company ID'><input name='popup_ad_id' value='{s['popup_ad_id']}' placeholder='Popup ID'><input name='ad' value='{s['ad']}'><input name='pop' value='{s['pop']}'><button>Save</button></form><div>{rows}</div><form method='post'><input type='hidden' name='act' value='add_task'><input name='title' placeholder='Task Title'><input name='reward' placeholder='20'><input name='link' placeholder='https://'><button>Add</button></form></body>"

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
.b{width:100%;padding:14px;border-radius:14px;background:#8b5cf6;color:#fff;border:none;font-weight:700;font-size:15px}
.by{background:#f59e0b;color:#000}.bd{background:#0B0E1C;border:1px solid #333}
.nav{position:fixed;bottom:0;left:0;right:0;background:#151A2D;display:flex;justify-content:space-around;padding:14px 0;border-top:1px solid #1e293b}
.nav div{opacity:.6;text-align:center;font-size:14px;font-weight:600;padding:8px 14px;min-width:60px;border-radius:12px}.nav div.active{opacity:1;color:#fff;background:#8b5cf6}
.tab{display:none}.tab.active{display:block}
input{width:100%;padding:12px;border-radius:12px;background:#0B0E1C;color:#fff;border:1px solid #333;box-sizing:border-box;margin-top:8px}
</style></head><body>
<div style='display:flex;gap:8px;padding:12px 0'><div class='card' style='margin:0'>💎</div><div class='card' style='margin:0;flex:1'>👑 {{s["app_name"]}}</div><div class='card' style='margin:0;flex:1;border:1px solid #f59e0b'>{{s["app_name2"]}}</div><div id='balTop' style='color:#0f0;padding:14px'>৳0</div></div>

<div id='tab-home' class='tab active'>
<div class='card'><h2>Good Evening, <span id='uname'>User</span>!</h2><div>💎 <span id='dia'>0</span> | ৳<span id='bal'>0</span></div></div>
<div style='display:flex;gap:10px'><div class='card' style='flex:1'>Company Ads ৳{{s["ad"]}}<br><small id='cCount'>0/{{s["clim"]}}</small><button class='b' onclick='watchAd("c")'>Start - ৳{{s["ad"]}}</button></div><div class='card' style='flex:1'>Popup Ads ৳{{s["pop"]}}<br><small id='pCount'>0/{{s["plim"]}}</small><button class='b by' onclick='watchAd("p")'>Watch - ৳{{s["pop"]}}</button></div></div>
<div class='card'><h3>💸 Withdraw</h3><input id='wdNum' placeholder='01XXXXXXXXX'><input id='wdAmt' type='number' placeholder='Min {{s["min"]}} Taka'><button class='b' onclick='doWD()'>Withdraw Now</button></div>
<div class='card' style='background:#2d1b69;border:1px solid #f59e0b'><h2>🔥 {{s["spon_title"]}}</h2><p>{{s["spon_desc"]}}</p><button class='b by'>{{s["spon_btn"]}}</button></div>
</div>

<div id='tab-tasks' class='tab'><div class='card'><h2>🎯 Tasks - বিভিন্ন কোম্পানি</h2><div id='taskList'></div></div></div>
<div id='tab-refer' class='tab'><div class='card'><h2>{{s["ref_title"]}}</h2><div id='refLink' class='card bd'></div><button class='b' onclick='navigator.clipboard.writeText(document.getElementById("refLink").innerText);alert("Copied")'>Copy Link</button></div></div>
<div id='tab-support' class='tab'><div class='card'><h2>{{s["sup_title"]}}</h2><button class='b'>Telegram</button></div></div>
<div id='tab-profile' class='tab'><div class='card' style='text-align:center'><div style='font-size:50px'>💎</div><h2 id='pName'>User</h2><p>💎 <span id='pDia'>0</span> | ৳<span id='pBal'>0</span></p></div></div>

<div class='nav'><div id='n-home' class='active' onclick="openTab('home')">🏠<br>Home</div><div id='n-tasks' onclick="openTab('tasks')">🎯<br>Tasks</div><div id='n-refer' onclick="openTab('refer')">👥<br>Refer</div><div id='n-support' onclick="openTab('support')">💬<br>Support</div><div id='n-profile' onclick="openTab('profile')">👤<br>Profile</div></div>

<script>
const S={{s|tojson}};
function openTab(n){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('active'));document.getElementById('tab-'+n).classList.add('active');document.getElementById('n-'+n).classList.add('active')}
function watchAd(t){let fn='show_'+(t=='c'?S.company_ad_id:S.popup_ad_id); if(typeof window[fn]=='function'){window[fn]().then(()=>{fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,type:t})}).then(r=>r.json()).then(d=>{if(d.bal!==undefined){document.getElementById('bal').innerText=d.bal;document.getElementById('balTop').innerText='৳'+d.bal;document.getElementById('dia').innerText=d.diamonds} alert(d.msg)})})}else{alert('Ad loading...')}}
function doWD(){fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,amt:document.getElementById('wdAmt').value,num:document.getElementById('wdNum').value,m:'bKash'})}).then(r=>r.json()).then(d=>alert(d.msg))}
fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id})}).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.bal;document.getElementById('balTop').innerText='৳'+d.user.bal;document.getElementById('dia').innerText=d.user.diamonds;document.getElementById('uname').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('pDia').innerText=d.user.diamonds;document.getElementById('pBal').innerText=d.user.bal;document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id;document.getElementById('cCount').innerText=(d.user.c_today||0)+'/'+d.s.clim;document.getElementById('pCount').innerText=(d.user.p_today||0)+'/'+d.s.plim;
  let h='';d.tasks.forEach(t=>{h+=`<div style='background:#0B0E1C;padding:10px;margin:6px 0;border-radius:12px;display:flex;justify-content:space-between'>${t.icon} ${t.title} - ৳${t.reward} <button style='padding:6px 12px;background:#8b5cf6;border:none;border-radius:8px;color:#fff' onclick="Telegram.WebApp.openLink('${t.link}')">Go</button></div>`});document.getElementById('taskList').innerHTML=h;
})
</script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
