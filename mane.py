import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস!","ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন এবং বোনাস নিন। বড় বিজ্ঞাপন বক্সে আপনার অফার লিখুন!","spon_btn":"🚀 Explore Now - Click Here","spon_link":"https://google.com","ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• বন্ধুর প্রতি Ads থেকে ১৫% কমিশন\n• Min Withdraw ৳৩০০\n• Instant Payment","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০ বোনাস!","sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com","sup_notice":"⚠️ গুরুত্বপূর্ণ নোটিশ:\n• রাত ১০টার পর Withdraw বন্ধ\n• সকাল ৯টায় চালু\n• ভুয়া রেফার ব্যান\n• VPN ব্যবহার করবেন না","sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে bKash/Nagad এ পাবেন।","sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই ৳৮০ সাথে সাথে।","sup_faq3_q":"📢 Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN ব্যবহার করবেন না, ১০ সেকেন্ড দেখুন।","sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান\n3. VPN নিষেধ\n4. দিনে ৫০টা Company, ৩০টা Popup","pro_title":"👤 My Profile","pro_notice":"💎 Diamond Member - Level বাড়ান, বেশি ইনকাম করুন!","pro_ver":"Version 3.1 - Monetag 2 Ads Active","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]}
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
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c_today":0,"p_today":0,"ad_date":"","diamonds":db["settings"]["bonus"]*100,"join":datetime.now().strftime("%Y-%m-%d"),"refl":[],"img":""}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["refl"].append(uid);db["users"][ref]["bal"]+=db["settings"]["ref"];db["users"][ref]["total"]+=db["settings"]["ref"]
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
        u["bal"]-=amt;db["wds"].append({"uid":u["id"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")});save_db(db);return jsonify({"msg":"Withdraw Pending"})
    return jsonify({"msg":f"Min {s.get('min')} Taka lagbe"})

@app.route('/api/update',methods=['POST'])
def up():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')))
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
            db["tasks"]=[t for t in db["tasks"] if str(t["id"])!=str(request.form.get('id'))]
        elif act=='save_all':
            for k in list(db["settings"].keys()):
                v=request.form.get(k)
                if v not in (None,''):
                    db["settings"][k]=v
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='display:flex;justify-content:space-between;background:#0B0E1C;padding:8px;margin:4px;border-radius:8px'>{t['id']}. {t['icon']} {t['title']} ৳{t['reward']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return render_template_string(f"""
    <style>body{{background:#0B0E1C;color:#fff;padding:14px;max-width:800px;margin:auto;font-family:system-ui}}.card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px;border:1px solid #1e293b}}input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333;margin-top:6px}}button{{background:#8b5cf6;color:#fff;padding:8px 14px;border:none;border-radius:8px}}</style>
    <div class='card'><h2>✅ Admin - সব কন্ট্রোল + ID Safe + Company Ad Fix</h2>Company: {s.get('company_ad_id')} | Popup: {s.get('popup_ad_id')} | Direct: {s.get('direct_link')}</div>
    <form method='post' class='card'><input type='hidden' name='act' value='save_all'>
    <h3>🎨 App & Color</h3>App Name <input name='app_name' value="{s['app_name']}"> App Name2 <input name='app_name2' value="{s['app_name2']}"> Primary <input name='primary' value="{s['primary']}"> Secondary <input name='secondary' value="{s['secondary']}">
    <h3>💰 Money - Admin থেকে সব</h3>Bonus <input name='bonus' value="{s['bonus']}"> AD Company <input name='ad' value="{s['ad']}"> POP Popup <input name='pop' value="{s['pop']}"> Company Limit <input name='clim' value="{s['clim']}"> Popup Limit <input name='plim' value="{s['plim']}"> Min WD <input name='min' value="{s['min']}"> Ref <input name='ref' value="{s['ref']}">
    <h3>📦 Ads ID - ID ব্যান হবে না</h3>Company ID <input name='company_ad_id' value="{s['company_ad_id']}"> Popup ID <input name='popup_ad_id' value="{s['popup_ad_id']}"> Direct Link <input name='direct_link' value="{s['direct_link']}">
    <h3>🔥 Sponsor Big Box</h3>Title <input name='spon_title' value="{s['spon_title']}"> Desc <textarea name='spon_desc'>{s['spon_desc']}</textarea> Btn <input name='spon_btn' value="{s['spon_btn']}"> Link <input name='spon_link' value="{s['spon_link']}">
    <h3>👥 Refer & Support</h3>Ref Title <input name='ref_title' value="{s['ref_title']}"> Ref Banner <input name='ref_banner' value="{s['ref_banner']}"> Sup TG <input name='sup_tg' value="{s['sup_tg']}"> Sup WA <input name='sup_wa' value="{s['sup_wa']}"> Email <input name='sup_email' value="{s['sup_email']}"> Notice <textarea name='sup_notice'>{s['sup_notice']}</textarea>
    <br><br><button type='submit' style='width:100%;padding:12px'>💾 SAVE ALL</button></form>
    <div class='card'><h3>Tasks - Delete 100% কাজ করবে</h3>{rows}<form method='post'><input type='hidden' name='act' value='add_task'>Title <input name='title'> Reward <input name='reward'> Link <input name='link'> Icon <input name='icon' value='🔗'><button>Add</button></form></div>
    """)

@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='https://telegram.org/js/telegram-web-app.js'></script>
<script src='https://libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
<script src='https://libtl.com/sdk.js' data-zone='{{ s["popup_ad_id"] }}' data-sdk='show_{{ s["popup_ad_id"] }}'></script>
<style>
body{margin:0;background:#0A0D1E;color:#fff;font-family:system-ui;padding:0 12px 90px}
.card{background:#151A2D;border:1px solid #1e293b;border-radius:20px;padding:14px;margin:12px 0}
.b{width:100%;padding:13px;border-radius:12px;background:{{s["primary"]}};color:#fff;border:none;font-weight:700;cursor:pointer}
.by{background:{{s["secondary"]}};color:#000}.bd{background:#0B0E1C;border:1px solid #333}
.nav{position:fixed;bottom:0;left:0;right:0;background:#151A2D;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1e293b;z-index:999}
.nav div{opacity:.6;text-align:center;font-size:11px;cursor:pointer}.nav div.active{opacity:1;color:{{s["primary"]}}}
.tab{display:none}.tab.active{display:block}
input{width:100%;padding:12px;border-radius:12px;background:#0B0E1C;color:#fff;border:1px solid #333;box-sizing:border-box;margin-top:8px}
</style></head><body>

<div style='display:flex;gap:8px;padding:12px 0;align-items:center'><div class='card' style='margin:0;padding:10px 16px'>💎</div><div class='card' style='margin:0;flex:1'>👑 {{s["app_name"]}}</div><div class='card' style='margin:0;flex:1;border:1px solid #f59e0b'>{{s["app_name2"]}}</div><div id='balTop' style='color:#00ff88;font-weight:700'>৳0</div></div>

<div id='tab-home' class='tab active'>
<div class='card'><div style='display:flex;justify-content:space-between'><span style='color:#8b5cf6'>Diamond Member • Level <span id='lvl'>1</span></span><span>Total Balance</span></div><h2 style='margin:6px 0'>Good Evening, <span id='uname'>User</span>!</h2><div style='display:flex;justify-content:space-between'><span>💎 <span id='dia'>0</span> Diamond | 100=৳1</span><span style='color:#0f0;font-size:22px'>৳<span id='bal'>0</span></span></div><div style='text-align:right;color:#f59e0b;font-size:12px'><span id='adsCount'>0/80</span> Ads</div><div style='background:#0B0E1C;height:8px;border-radius:10px;margin-top:8px'><div id='prog' style='height:8px;background:#8b5cf6;width:10%;border-radius:10px'></div></div></div>

<div style='display:flex;gap:10px'><div class='card' style='flex:1'><div style='display:flex;justify-content:space-between;font-size:13px'>Company Ads <span style='color:#f59e0b'>৳{{s["ad"]}}</span></div><small id='cCount'>0/{{s["clim"]}} today</small><button class='b' onclick='watchAd("c")'>Start - ৳{{s["ad"]}}</button></div><div class='card' style='flex:1'><div style='display:flex;justify-content:space-between;font-size:13px'>Popup Ads <span style='color:#f59e0b'>৳{{s["pop"]}}</span></div><small id='pCount'>0/{{s["plim"]}} today</small><button class='b by' onclick='watchAd("p")'>Watch - ৳{{s["pop"]}}</button></div></div>

<div class='card'><h3 style='margin:0 0 8px'>💸 Withdraw</h3><div style='display:flex;gap:8px'><button class='b bd' id='bkBtn'>bKash</button><button class='b bd' id='ngBtn'>Nagad</button></div><input id='wdNum' placeholder='01XXXXXXXXX'><input id='wdAmt' type='number' placeholder='Min {{s["min"]}} Taka'><button class='b' onclick='doWD()'>Withdraw Now</button><p style='color:#666;font-size:12px'>No history</p></div>

<div class='card' style='background:linear-gradient(135deg,#2d1b69,#1a0f3d);border:1px solid #f59e0b'><span style='background:#f59e0b;color:#000;padding:4px 12px;border-radius:20px;font-size:12px'>🔥 SPONSORED • BIGGEST AD</span><h2>🔥 {{s["spon_title"]}}</h2><p style='white-space:pre-line'>{{s["spon_desc"]}}</p><button class='b by' onclick='Telegram.WebApp.openLink(S.spon_link)'>{{s["spon_btn"]}}</button><button class='b bd' style='margin-top:8px' onclick='Telegram.WebApp.openLink(S.direct_link)'>Direct Link</button></div>
</div>

<div id='tab-tasks' class='tab'><div class='card'><h2 style='margin:0'>🎯 Tasks & Company Links</h2><p style='color:#888'>প্রতি Task এ ৳20-25 + Diamond</p><div id='taskList'></div></div></div>

<div id='tab-refer' class='tab'><div class='card' style='background:linear-gradient(90deg,#f59e0b,#ff8c00);color:#000;text-align:center;font-weight:700'>{{s["ref_banner"]}}</div><div class='card'><h2 style='margin:0'>{{s["ref_title"]}}</h2><p style='color:#888'>{{s["ref_desc"]}}</p><div style='display:flex;gap:8px'><div class='card bd' style='flex:1;text-align:center'><div style='color:#8b5cf6;font-size:20px' id='rTotal'>0</div>Total Refer</div><div class='card bd' style='flex:1;text-align:center'><div style='color:#0f0;font-size:20px' id='rEarn'>৳0</div>Earned</div><div class='card bd' style='flex:1;text-align:center'><div style='color:#f59e0b;font-size:20px'>15%</div>Commission</div></div><div id='refLink' class='card bd' style='word-break:break-all;font-size:11px'></div><button class='b' onclick='navigator.clipboard.writeText(document.getElementById("refLink").innerText);alert("Copied")'>🔗 Copy Refer Link</button></div><div class='card'><h3>📋 How Refer Works</h3><p style='white-space:pre-line'>{{s["ref_rules"]}}</p></div><div class='card'><h3>👥 My Refer List</h3><p id='refList' style='color:#888'>No refer yet</p></div></div>

<div id='tab-support' class='tab'><div class='card'><h2 style='margin:0'>{{s["sup_title"]}}</h2><p style='color:#888'>{{s["sup_desc"]}}</p><div style='display:flex;gap:8px;margin-top:10px'><button class='b' onclick='Telegram.WebApp.openLink(S.sup_tg)'>✈️ Telegram</button><button class='b by' onclick='Telegram.WebApp.openLink(S.sup_wa)'>💬 WhatsApp</button></div><div class='card bd' style='margin-top:10px'>📧 {{s["sup_email"]}}</div></div><div class='card' style='border:1px solid #f59e0b;background:#1a1500'><h3 style='margin:0'>📢 Notice Board</h3><p style='white-space:pre-line'>{{s["sup_notice"]}}</p></div><div class='card'><h3>❓ FAQ</h3><details class='card bd'><summary>{{s["sup_faq1_q"]}}</summary><p>{{s["sup_faq1_a"]}}</p></details><details class='card bd'><summary>{{s["sup_faq2_q"]}}</summary><p>{{s["sup_faq2_a"]}}</p></details><details class='card bd'><summary>{{s["sup_faq3_q"]}}</summary><p>{{s["sup_faq3_a"]}}</p></details></div><div class='card'><h3>📜 Rules</h3><p style='white-space:pre-line'>{{s["sup_rules"]}}</p></div></div>

<div id='tab-profile' class='tab'>
<div class='card' style='text-align:center'><div style='width:80px;height:80px;background:#0B0E1C;border:2px solid #8b5cf6;border-radius:20px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:40px' id='pImg'>💎</div><div style='background:#f59e0b;color:#000;display:inline-block;padding:2px 12px;border-radius:20px;font-size:12px;margin-top:10px'>Level <span id='pLvl'>1</span></div><h2 style='margin:8px 0' id='pName'>User 4250</h2><small>Join: <span id='pJoin'>2026-09-15</span></small><br><small>💎 <span id='pDia'>0</span> Diamond | ৳<span id='pBal'>0</span> Taka</small><p style='color:#888;font-size:12px'>{{s["pro_ver"]}}</p></div>
<div class='card'><h3 style='margin:0 0 10px'>📊 Statistics</h3><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'><div class='card bd' style='text-align:center;margin:0'><div style='color:#0f0;font-size:18px'>৳<span id='sEarn'>0</span></div><small>Total Earned</small></div><div class='card bd' style='text-align:center;margin:0'><div style='color:#8b5cf6;font-size:18px'>৳<span id='sBal'>0</span></div><small>Balance</small></div><div class='card bd' style='text-align:center;margin:0'><div style='color:#f59e0b;font-size:18px' id='sAds'>0</div><small>Ads</small></div><div class='card bd' style='text-align:center;margin:0'><div style='color:#ff5a9a;font-size:18px' id='sRef'>0</div><small>Refer</small></div></div></div>
<div class='card'><h3 style='margin:0'>📈 Level Progress</h3><div style='display:flex;justify-content:space-between;margin-top:8px'><span>Level <span id='lpLvl'>1</span></span><span>Next: ৳<span id='lpNext'>500</span></span></div><div style='background:#0B0E1C;height:10px;border-radius:10px;margin:8px 0'><div id='lpBar' style='height:10px;background:#8b5cf6;width:10%;border-radius:10px'></div></div><small>{{s["pro_notice"]}}</small></div>
<div class='card'><h3 style='margin:0 0 10px'>⚙️ Account</h3><div class='card bd' style='margin:0 0 8px'>User ID<br><b id='accId'>0</b></div><div class='card bd' style='margin:0 0 8px'><span id='accName'>User</span></div><input type='text' id='newName' placeholder='New Name'><input type='file' id='fileIn'><button class='b' onclick='saveProfile()'>💾 Save Profile</button></div>
<div class='card'><h3>💸 Withdraw History</h3><p style='color:#888'>No withdraw yet</p></div>
</div>

<div class='nav'><div id='n-home' class='active' onclick="openTab('home')">🏠<br>Home</div><div id='n-tasks' onclick="openTab('tasks')">🎯<br>Tasks</div><div id='n-refer' onclick="openTab('refer')">👥<br>Refer</div><div id='n-support' onclick="openTab('support')">💬<br>Support</div><div id='n-profile' onclick="openTab('profile')">👤<br>Profile</div></div>

<script>
const S={{s|tojson}}; let curM='bKash';
function openTab(n){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('active'));document.getElementById('tab-'+n).classList.add('active');document.getElementById('n-'+n).classList.add('active')}
document.getElementById('bkBtn').onclick=function(){curM='bKash'; this.style.borderColor='#8b5cf6'; document.getElementById('ngBtn').style.borderColor='#333'};
document.getElementById('ngBtn').onclick=function(){curM='Nagad'; this.style.borderColor='#8b5cf6'; document.getElementById('bkBtn').style.borderColor='#333'};
function watchAd(t){
  let zoneId=t=='c'?S.company_ad_id:S.popup_ad_id;
  let fn='show_'+zoneId;
  if(typeof window[fn]==='function'){
    window[fn]().then(()=>{
      fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,type:t})}).then(r=>r.json()).then(d=>{
        if(d.bal!==undefined){document.getElementById('bal').innerText=d.bal;document.getElementById('balTop').innerText='৳'+d.bal;document.getElementById('sBal').innerText=d.bal;document.getElementById('pBal').innerText=d.bal;document.getElementById('dia').innerText=d.diamonds;document.getElementById('pDia').innerText=d.diamonds;}
        document.getElementById('cCount').innerText=(d.c_today||0)+'/'+S.clim+' today';document.getElementById('pCount').innerText=(d.p_today||0)+'/'+S.plim+' today';
        document.getElementById('adsCount').innerText=(d.c_today+d.p_today)+'/80';document.getElementById('sAds').innerText=(d.c_today+d.p_today);
        alert(d.msg)
      })
    }).catch(()=>alert('Ad closed'));
  } else {alert('Company Ad loading... 5 sec por try koro. Zone: '+zoneId)}
}
function doWD(){fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,amt:document.getElementById('wdAmt').value,num:document.getElementById('wdNum').value,m:curM})}).then(r=>r.json()).then(d=>alert(d.msg))}
function saveProfile(){
  let name=document.getElementById('newName').value;
  fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,name:name})}).then(r=>r.json()).then(d=>{alert(d.msg); location.reload()})
}
fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id})}).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.bal;document.getElementById('balTop').innerText='৳'+d.user.bal;document.getElementById('sBal').innerText=d.user.bal;document.getElementById('pBal').innerText=d.user.bal;document.getElementById('sEarn').innerText=d.user.total;document.getElementById('dia').innerText=d.user.diamonds;document.getElementById('pDia').innerText=d.user.diamonds;
  document.getElementById('uname').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('accName').innerText=d.user.name;document.getElementById('accId').innerText=d.user.id;document.getElementById('lvl').innerText=d.level;document.getElementById('pLvl').innerText=d.level;document.getElementById('lpLvl').innerText=d.level;document.getElementById('lpNext').innerText=d.next;document.getElementById('lpBar').style.width=d.prog+'%';document.getElementById('prog').style.width=d.prog+'%';
  document.getElementById('pJoin').innerText=d.user.join;document.getElementById('sAds').innerText=(d.user.c_today||0)+(d.user.p_today||0);document.getElementById('sRef').innerText=d.user.refl.length;document.getElementById('rTotal').innerText=d.user.refl.length;document.getElementById('adsCount').innerText=(d.user.c_today+d.user.p_today)+'/80';
  document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id;document.getElementById('cCount').innerText=(d.user.c_today||0)+'/'+S.clim+' today';document.getElementById('pCount').innerText=(d.user.p_today||0)+'/'+S.plim+' today';
  let h='';d.tasks.forEach(t=>{h+=`<div style='display:flex;justify-content:space-between;align-items:center;background:#0B0E1C;padding:12px;margin:8px 0;border-radius:14px'><div>${t.icon} ${t.title}<br><small style='color:#0f0'>৳${t.reward} + 💎${t.reward*100}</small></div><button style='width:auto;padding:8px 16px;background:#8b5cf6;border:none;border-radius:10px;color:#fff' onclick="Telegram.WebApp.openLink('${t.link}')">Go</button></div>`});document.getElementById('taskList').innerHTML=h;
  if(d.user.refl.length>0){document.getElementById('refList').innerText=d.user.refl.join(', ')}
})
</script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
