# পুরা ফাইল - তোমার অরিজিনালটাই, শুধু 3টা বাগ ফিক্স
# 1. inputt -> input
# 2. importt_link -> direct_link
# 3. pop bug fix -> s['pop'] and s['ad']
# 4. Withdraw bug fix -> Min 500 input fixed
# 5. ID Safe -> openLink

import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={ "app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস পেয়েছেন! এখন ইনকাম শুরু করুন!","ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন এবং বোনাস নিন। বড় বিজ্ঞাপন বক্সে আপনার অফার লিখুন!","spon_btn":"🚀 Explore Now - Click Here","spon_link":"https://google.com","ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• বন্ধুর প্রতি Ads থেকে ১৫% কমিশন\n• Min Withdraw ৳৩০০\n• Instant Payment","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০ বোনাস!","sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com","sup_notice":"⚠️ গুরুত্বপূর্ণ নোটিশ:\n• রাত ১০টার পর Withdraw বন্ধ\n• সকাল ৯টায় চালু\n• ভুয়া রেফার ব্যান\n• VPN ব্যবহার করবেন না","sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে bKash/Nagad এ পাবেন।","sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই ৳৮০ সাথে সাথে।","sup_faq3_q":"📢 Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN ব্যবহার করবেন না, ১০ সেকেন্ড দেখুন।","sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান\n3. VPN নিষেধ\n4. দিনে ৫০টা Company, ৩০টা Popup","pro_title":"👤 My Profile","pro_notice":"💎 Diamond Member - Level বাড়ান, বেশি ইনকাম করুন!","pro_ver":"Version 3.1 - Monetag 2 Ads Active","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000] }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[ {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"}, {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"}, {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"} ]}
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
    uid=str(uid);is_new=False
    if uid not in db["users"]:
        is_new=True
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"ads":0,"diamonds":db["settings"]["bonus"]*db["settings"]["diamond_rate"],"task_timer":{},"ad_date":"","c_today":0,"p_today":0}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["refl"].append(uid);db["users"][ref]["bal"]+=db["settings"]["ref"];db["users"][ref]["total"]+=db["settings"]["ref"]
    return db["users"][uid], is_new

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u,is_new=get_user(db,str(j.get('id')),j.get('ref'));save_db(db)
    wds=[x for x in db["wds"] if x["uid"]==u["id"]];lvl=get_level(u["total"], db["settings"]["levels"])
    nxt=db["settings"]["levels"][lvl] if lvl < len(db["settings"]["levels"]) else db["settings"]["levels"][-1]
    prog=int((u["total"]/nxt*100)) if nxt>0 else 0
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds,"level":lvl,"next":nxt,"prog":prog,"is_new":is_new})

@app.route('/api/ads', methods=['POST'])
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
    user["bal"]=float(user.get("bal",0))+reward;user["total"]=float(user.get("total",0))+reward;user["diamonds"]=int(user.get("diamonds",0))+int(reward*100);save_db(db)
    return jsonify({"msg": f"{reward} Taka Added","bal":user["bal"],"diamonds":user["diamonds"],"c_today":user["c_today"],"p_today":user["p_today"]})

@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
    if amt>=int(s.get("min",500)) and u["bal"]>=amt:
        u["bal"]-=amt;db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")});save_db(db);return jsonify({"msg":"Withdraw সফল"})
    return jsonify({"msg":f"Min {s.get('min')} Tk lagbe"})

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
                if request.form.get(k) not in (None,''):
                    db["settings"][k]=request.form.get(k)
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='display:flex;justify-content:space-between;background:#0B0E1C;padding:8px;margin:4px;border-radius:8px'>{t['id']}. {t['icon']} {t['title']} ৳{t['reward']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return render_template_string(f"<style>body{{background:#0B0E1C;color:#fff;padding:16px;max-width:700px;margin:auto}}.card{{background:#151A2D;padding:16px;border-radius:14px;margin-bottom:12px}} input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333;margin-top:6px}} button{{background:#8b5cf6;color:#fff;padding:10px;border:none;border-radius:8px}}</style><div class='card'><h3>✅ Admin Fixed - All Controllable + ID Safe</h3>Company: {s.get('company_ad_id')} | Popup: {s.get('popup_ad_id')} | Direct: {s.get('direct_link')}</div><form method='post' class='card'><input type='hidden' name='act' value='save_all'>App Name <input name='app_name' value='{s['app_name']}'> Bonus <input name='bonus' value='{s['bonus']}'> AD <input name='ad' value='{s['ad']}'> POP <input name='pop' value='{s['pop']}'> Company ID <input name='company_ad_id' value='{s['company_ad_id']}'> Popup ID <input name='popup_ad_id' value='{s['popup_ad_id']}'> Direct <input name='direct_link' value='{s['direct_link']}'> Sponsor Title <input name='spon_title' value='{s['spon_title']}'><textarea name='spon_desc'>{s['spon_desc']}</textarea><input name='spon_btn' value='{s['spon_btn']}'><input name='spon_link' value='{s['spon_link']}'><button>SAVE ALL</button></form><div class='card'>{rows}</div>")

@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='https://telegram.org/js/telegram-web-app.js'></script>
<script src='//libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
<style>
:root{--p:{{s["primary"]}};--s:{{s["secondary"]}}}
body{margin:0;background:#0A0D1E;color:#fff;font-family:system-ui;padding:0 12px 90px}
.card{background:#151A2D;border:1px solid #1e293b;border-radius:20px;padding:14px;margin:12px 0}
.b{width:100%;padding:13px;border-radius:12px;background:var(--p);color:#fff;border:none;font-weight:700}
.by{background:var(--s);color:#000}.bd{background:#0B0E1C;color:#fff;border:1px solid #333}
.nav{position:fixed;bottom:0;left:0;right:0;background:#151A2D;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #1e293b;z-index:99}
input{width:100%;padding:12px;border-radius:12px;background:#0B0E1C;color:#fff;border:1px solid #333;box-sizing:border-box}
</style></head><body>
<div style='display:flex;gap:8px;padding:12px 0'><div class='card' style='flex:1;margin:0;text-align:center'>💎</div><div class='card' style='flex:3;margin:0'>👑 {{s["app_name"]}}</div><div class='card' style='flex:2;margin:0'>{{s["app_name2"]}}</div><div style='padding:14px;color:#00ff88' id='balTop'>৳0</div></div>

<div class='card'>
<div style='display:flex;justify-content:space-between'><span style='color:#8b5cf6'>Diamond Member • Level <span id='lvl'>1</span></span><span>Total Balance</span></div>
<h2 style='margin:4px 0'>Good Evening, <span id='uname'>User</span>!</h2>
<div style='display:flex;justify-content:space-between'><span>💎 <span id='dia'>0</span> Diamond | 100=৳1</span><span style='color:#00ff88;font-size:20px'>৳<span id='bal'>0</span></span></div>
<div style='text-align:right;color:#f59e0b;font-size:12px'><span id='adsCount'>0/80</span> Ads</div>
</div>

<div style='display:flex;gap:12px'>
<div class='card' style='flex:1'><div style='display:flex;justify-content:space-between'>Company Ads <span style='color:#f59e0b'>৳{{s["ad"]}}</span></div><small id='cCount'>0/{{s["clim"]}} today</small><button class='b' onclick='watchAd("c")'>Start - ৳{{s["ad"]}}</button></div>
<div class='card' style='flex:1'><div style='display:flex;justify-content:space-between'>Popup Ads <span style='color:#f59e0b'>৳{{s["pop"]}}</span></div><small id='pCount'>0/{{s["plim"]}} today</small><button class='b by' onclick='watchAd("p")'>Watch - ৳{{s["pop"]}}</button></div>
</div>

<div class='card'><h3>💸 Withdraw</h3><div style='display:flex;gap:8px'><button class='b bd' id='bk'>bKash</button><button class='b bd' id='ng'>Nagad</button></div><input id='num' placeholder='01XXXXXXXXX' style='margin-top:10px'><input id='amt' type='number' placeholder='Min {{s["min"]}} Taka' style='margin-top:8px'><button class='b' onclick='doWD()' style='margin-top:8px'>Withdraw Now</button><p style='color:#888'>No history</p></div>

<div class='card' style='background:linear-gradient(135deg,#2d1b69,#1a0f3d);border:1px solid #f59e0b'><div style='display:flex;justify-content:space-between'><span style='background:#f59e0b;color:#000;padding:4px 10px;border-radius:20px;font-size:12px'>🔥 SPONSORED • BIGGEST AD</span><small>Monetag Active</small></div><h2>🔥 {{s["spon_title"]}}</h2><p>{{s["spon_desc"]}}</p><button class='b by' onclick='openSponsor()'>{{s["spon_btn"]}}</button></div>

<div id='pages'>
<div id='pHome'></div>
<div id='pTasks' style='display:none'><div class='card'><h3>🎯 Tasks & Company Links</h3><p>প্রতি Task এ ৳20-25 + Diamond</p><div id='taskList'></div></div></div>
<div id='pRefer' style='display:none'></div>
<div id='pSupport' style='display:none'></div>
</div>

<div class='nav'><div onclick="showTab('home')">🏠<br>Home</div><div onclick="showTab('tasks')">🎯<br>Tasks</div><div onclick="showTab('refer')">👥<br>Refer</div><div onclick="showTab('support')">💬<br>Support</div><div onclick="showTab('profile')">👤<br>Profile</div></div>

<script>
const S={{s|tojson}}; let curM='bKash';
document.getElementById('bk').onclick=()=>{curM='bKash'}; document.getElementById('ng').onclick=()=>{curM='Nagad'};
function openSponsor(){Telegram.WebApp.openLink(S.spon_link)}
function openDirect(){Telegram.WebApp.openLink(S.direct_link)}
function showTab(t){
  document.getElementById('pTasks').style.display=t=='tasks'?'block':'none';
  // Home is default, others you can add
}
function watchAd(type){
  let zone=type=='c'?`show_${S.company_ad_id}`:`show_${S.popup_ad_id}`;
  if(typeof window[zone]==='function'){
    window[zone]().then(()=>{
      fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,type:type})}).then(r=>r.json()).then(d=>{
        if(d.bal!==undefined){document.getElementById('bal').innerText=d.bal; document.getElementById('balTop').innerText='৳'+d.bal; document.getElementById('dia').innerText=d.diamonds;}
        document.getElementById('cCount').innerText=(d.c_today||0)+'/'+S.clim+' today';
        document.getElementById('pCount').innerText=(d.p_today||0)+'/'+S.plim+' today';
        alert(d.msg)
      })
    })
  } else {alert('Ad loading...')}
}
function doWD(){
  fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,amt:document.getElementById('amt').value,num:document.getElementById('num').value,m:curM})}).then(r=>r.json()).then(d=>alert(d.msg))
}
fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id})}).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.bal; document.getElementById('balTop').innerText='৳'+d.user.bal; document.getElementById('dia').innerText=d.user.diamonds; document.getElementById('uname').innerText=d.user.name; document.getElementById('lvl').innerText=d.level;
  let h=''; d.tasks.forEach(t=>{h+=`<div style='display:flex;justify-content:space-between;background:#0B0E1C;padding:10px;margin:6px 0;border-radius:12px'><div>${t.icon} ${t.title}<br><small style='color:#0f0'>৳${t.reward} + 💎${t.reward*100}</small></div><button style='width:auto;padding:6px 14px;background:#8b5cf6;border:none;border-radius:8px;color:#fff' onclick="Telegram.WebApp.openLink('${t.link}')">Go</button></div>`}); document.getElementById('taskList').innerHTML=h;
  document.getElementById('cCount').innerText=(d.user.c_today||0)+'/'+S.clim+' today'; document.getElementById('pCount').innerText=(d.user.p_today||0)+'/'+S.plim+' today'; document.getElementById('adsCount').innerText=(d.user.c_today+d.user.p_today)+'/80';
})
</script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
