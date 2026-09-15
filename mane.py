import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'
def load_db():
    d={"app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন এবং বোনাস নিন।","spon_btn":"🚀 Explore Now - Click Here","spon_link":"https://google.com","ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• বন্ধুর প্রতি Ads থেকে ১৫% কমিশন\n• Min Withdraw ৳৩০০\n• Instant Payment","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০ বোনাস!","sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_email":"support@gmail.com","sup_notice":"⚠️ গুরুত্বপূর্ণ নোটিশ:\n• রাত ১০টার পর Withdraw বন্ধ\n• সকাল ৯টায় চালু\n• ভুয়া রেফার ব্যান\n• VPN ব্যবহার করবেন না","sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে bKash/Nagad এ পাবেন।","sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই ৳৮০ সাথে সাথে।","sup_faq3_q":"📢 Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN ব্যবহার করবেন না, ১০ সেকেন্ড দেখুন।","sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান\n3. VPN নিষেধ\n4. দিনে ৫০টা Company, ৩০টা Popup","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]}
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
    uid=str(uid);is_new=False
    if uid not in db["users"]:
        is_new=True
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c_today":0,"p_today":0,"ad_date":"","diamonds":db["settings"]["bonus"]*100,"join":datetime.now().strftime("%Y-%m-%d"),"refl":[]}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["refl"].append(uid);db["users"][ref]["bal"]+=db["settings"]["ref"]
    return db["users"][uid],is_new
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
        if user.get("c_today",0)>=int(s.get("clim",50)): return jsonify({"msg":"Ajker limit sesh"})
        reward=float(s.get("ad",0.2));user["c_today"]+=1
    else:
        if user.get("p_today",0)>=int(s.get("plim",30)): return jsonify({"msg":"Ajker limit sesh"})
        reward=float(s.get("pop",0.3));user["p_today"]+=1
    user["bal"]+=reward;user["total"]+=reward;user["diamonds"]+=int(reward*100);save_db(db)
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
        for k in db["settings"].keys():
            if request.form.get(k): db["settings"][k]=request.form.get(k)
        save_db(db)
    s=db["settings"]
    return f"<body style='background:#0B0E1C;color:#fff;padding:20px'><h3>Admin - ID Safe</h3><form method='post'>AD <input name='ad' value='{s['ad']}'><br>POP <input name='pop' value='{s['pop']}'><br>Company ID <input name='company_ad_id' value='{s['company_ad_id']}'><br>Popup ID <input name='popup_ad_id' value='{s['popup_ad_id']}'><br>Direct <input name='direct_link' value='{s['direct_link']}'><br><button>Save</button></form></body>"
@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='https://telegram.org/js/telegram-web-app.js'></script>
<script src='//libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
<style>
body{margin:0;background:#0A0D1E;color:#fff;font-family:system-ui;padding:0 12px 90px}
.card{background:#151A2D;border:1px solid #1e293b;border-radius:20px;padding:14px;margin:12px 0}
.b{width:100%;padding:13px;border-radius:12px;background:#8b5cf6;color:#fff;border:none;font-weight:700}
.by{background:#f59e0b;color:#000}.bd{background:#0B0E1C;border:1px solid #333}
.nav{position:fixed;bottom:0;left:0;right:0;background:#151A2D;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1e293b}
.nav div{opacity:.6;text-align:center;font-size:11px}.nav div.active{opacity:1;color:#8b5cf6}
.tab{display:none}.tab.active{display:block}
input{width:100%;padding:12px;border-radius:12px;background:#0B0E1C;color:#fff;border:1px solid #333;box-sizing:border-box;margin-top:8px}
</style></head><body>
<div style='display:flex;gap:8px;padding:12px 0'><div class='card' style='margin:0'>💎</div><div class='card' style='margin:0;flex:1'>👑 {{s["app_name"]}}</div><div class='card' style='margin:0;flex:1;border:1px solid #f59e0b'>{{s["app_name2"]}}</div><div id='balTop' style='color:#0f0;padding:14px'>৳0</div></div>

<div id='tab-home' class='tab active'>
<div class='card'><div style='display:flex;justify-content:space-between'><span style='color:#8b5cf6'>Diamond Member • Level <span id='lvl'>1</span></span><span>Total Balance</span></div><h2>Good Evening, <span id='uname'>User</span>!</h2><div style='display:flex;justify-content:space-between'><span>💎 <span id='dia'>0</span> Diamond</span><span style='color:#0f0;font-size:22px'>৳<span id='bal'>0</span></span></div></div>
<div style='display:flex;gap:10px'><div class='card' style='flex:1'>Company Ads ৳{{s["ad"]}}<br><small id='cCount'>0/{{s["clim"]}}</small><button class='b' onclick='watchAd("c")'>Start - ৳{{s["ad"]}}</button></div><div class='card' style='flex:1'>Popup Ads ৳{{s["pop"]}}<br><small id='pCount'>0/{{s["plim"]}}</small><button class='b by' onclick='watchAd("p")'>Watch - ৳{{s["pop"]}}</button></div></div>
<div class='card'><h3>💸 Withdraw</h3><div style='display:flex;gap:8px'><button class='b bd'>bKash</button><button class='b bd'>Nagad</button></div><input id='wdNum' placeholder='01XXXXXXXXX'><input id='wdAmt' type='number' placeholder='Min {{s["min"]}} Taka'><button class='b' onclick='doWD()'>Withdraw Now</button></div>
<div class='card' style='background:#2d1b69;border:1px solid #f59e0b'><span style='background:#f59e0b;color:#000;padding:4px 10px;border-radius:20px'>SPONSORED • BIGGEST AD</span><h2>🔥 {{s["spon_title"]}}</h2><p>{{s["spon_desc"]}}</p><button class='b by' onclick='Telegram.WebApp.openLink(S.spon_link)'>{{s["spon_btn"]}}</button></div>
</div>

<div id='tab-tasks' class='tab'><div class='card'><h2>🎯 Tasks</h2><div id='taskList'></div></div></div>
<div id='tab-refer' class='tab'><div class='card' style='background:#f59e0b;color:#000'>{{s["ref_banner"]}}</div><div class='card'><h2>👥 {{s["ref_title"]}}</h2><p>{{s["ref_desc"]}}</p><div id='refLink' class='card bd' style='word-break:break-all'></div><button class='b' onclick='navigator.clipboard.writeText(document.getElementById("refLink").innerText);alert("Copied")'>Copy Refer Link</button></div><div class='card'><p style='white-space:pre-line'>{{s["ref_rules"]}}</p></div></div>
<div id='tab-support' class='tab'><div class='card'><h2>💎 {{s["sup_title"]}}</h2><p>{{s["sup_desc"]}}</p><div style='display:flex;gap:8px'><button class='b' onclick='Telegram.WebApp.openLink(S.sup_tg)'>Telegram</button><button class='b by' onclick='Telegram.WebApp.openLink(S.sup_wa)'>WhatsApp</button></div><div class='card bd'>Email: {{s["sup_email"]}}</div></div><div class='card' style='border:1px solid #f59e0b'><h3>Notice Board</h3><p style='white-space:pre-line'>{{s["sup_notice"]}}</p></div><div class='card'><p style='white-space:pre-line'>{{s["sup_rules"]}}</p></div></div>
<div id='tab-profile' class='tab'><div class='card' style='text-align:center'><div style='font-size:40px'>💎</div><h2 id='pName'>User</h2><p>💎 <span id='pDia'>0</span> Diamond | ৳<span id='pBal'>0</span></p></div><div class='card'><h3>📊 Statistics</h3><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'><div class='card bd' style='text-align:center'>৳<span id='sEarn'>0</span><br>Total Earned</div><div class='card bd' style='text-align:center'>৳<span id='sBal'>0</span><br>Balance</div><div class='card bd' style='text-align:center'><span id='sAds'>0</span><br>Ads</div><div class='card bd' style='text-align:center'><span id='sRef'>0</span><br>Refer</div></div></div><div class='card'><h3>📈 Level Progress</h3><div style='display:flex;justify-content:space-between'><span>Level <span id='lpLvl'>1</span></span><span>Next ৳<span id='lpNext'>500</span></span></div><div style='background:#0B0E1C;height:10px;border-radius:10px'><div id='lpBar' style='height:10px;background:#8b5cf6;width:10%'></div></div></div></div>

<div class='nav'><div id='n-home' class='active' onclick="openTab('home')">🏠<br>Home</div><div id='n-tasks' onclick="openTab('tasks')">🎯<br>Tasks</div><div id='n-refer' onclick="openTab('refer')">👥<br>Refer</div><div id='n-support' onclick="openTab('support')">💬<br>Support</div><div id='n-profile' onclick="openTab('profile')">👤<br>Profile</div></div>
<script>
const S={{s|tojson}};
function openTab(n){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('active'));document.getElementById('tab-'+n).classList.add('active');document.getElementById('n-'+n).classList.add('active')}
function watchAd(t){let z=t=='c'?`show_{{s["company_ad_id"]}}`:`show_{{s["popup_ad_id"]}}`; if(typeof window[z]=='function'){window[z]().then(()=>{fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,type:t})}).then(r=>r.json()).then(d=>{if(d.bal!==undefined){document.getElementById('bal').innerText=d.bal;document.getElementById('balTop').innerText='৳'+d.bal;document.getElementById('dia').innerText=d.diamonds} alert(d.msg)})})}else{alert('Ad not ready')}}
function doWD(){fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,amt:document.getElementById('wdAmt').value,num:document.getElementById('wdNum').value,m:'bKash'})}).then(r=>r.json()).then(d=>alert(d.msg))}
fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id})}).then(r=>r.json()).then(d=>{document.getElementById('bal').innerText=d.user.bal;document.getElementById('balTop').innerText='৳'+d.user.bal;document.getElementById('sBal').innerText=d.user.bal;document.getElementById('pBal').innerText=d.user.bal;document.getElementById('sEarn').innerText=d.user.total;document.getElementById('dia').innerText=d.user.diamonds;document.getElementById('pDia').innerText=d.user.diamonds;document.getElementById('uname').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('lvl').innerText=d.level;document.getElementById('lpLvl').innerText=d.level;document.getElementById('lpNext').innerText=d.next;document.getElementById('lpBar').style.width=d.prog+'%';document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id; let h='';d.tasks.forEach(t=>{h+=`<div style='background:#0B0E1C;padding:10px;margin:6px 0;border-radius:12px;display:flex;justify-content:space-between'>${t.icon} ${t.title} - ৳${t.reward} <button style='padding:6px 12px;background:#8b5cf6;border:none;border-radius:8px;color:#fff' onclick="Telegram.WebApp.openLink('${t.link}')">Go</button></div>`});document.getElementById('taskList').innerHTML=h;})
</script></body></html>
    """, s=s)
if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
