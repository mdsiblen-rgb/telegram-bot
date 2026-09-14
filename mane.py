import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'
def load_db():
    if not os.path.exists(DB):
        d={"users":{},"withdraws":[],"settings":{
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN",
            "company_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,
            "balance_target":2000,"min_withdraw":500,
            "tele_link":"https://t.me/","whatsapp":"01XXXXXXXXXX","email":"support@protidinerkajbd.com","yt_tutorial":"https://youtube.com/"
        }}
        open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2));return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":"User 8385","balance":1120,"company":0,"popup":0,"total":0,"tasks":[],"img":"","join":"2026-09-13","work":0}
    return db["users"][uid]
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Use /admin?id=8807178385",403
    return "Admin OK - /api/get?id=8807178385"
@app.route('/api/get')
def api_get():
    db=load_db(); u=get_user(db,request.args.get('id','8807178385'))
    save_db(db)
    return jsonify({"user":u,"settings":db["settings"]})
@app.route('/api/reward')
def reward():
    db=load_db(); u=get_user(db,request.args.get('id')); t=request.args.get('type'); s=db["settings"]
    if t=='company':
        if u["company"]>=int(s["company_limit"]): return jsonify({"msg":"Limit শেষ"})
        u["company"]+=1; u["balance"]+=int(s["company_reward"])
    else:
        if u["popup"]>=int(s["popup_limit"]): return jsonify({"msg":"Limit শেষ"})
        u["popup"]+=1; u["balance"]+=int(s["popup_reward"])
    u["total"]=u["company"]+u["popup"]; u["work"]=u["total"]; save_db(db); return jsonify({"ok":1})
@app.route('/api/task/done',methods=['POST'])
def task_done():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); tid=j.get('tid'); amt=int(j.get('amt',0))
    if tid not in u["tasks"]: u["tasks"].append(tid); u["balance"]+=amt
    save_db(db); return jsonify({"msg":f"✅ ৳{amt} Bonus"})
@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); amt=int(j.get('amt',0))
    if amt<int(db["settings"]["min_withdraw"]): return jsonify({"msg":f"Min ৳{db['settings']['min_withdraw']}"})
    if u["balance"]<amt: return jsonify({"msg":"❌ ব্যালেন্স কম"})
    u["balance"]-=amt; db["withdraws"].append({"uid":u["id"],"amt":amt,"num":j.get('num'),"method":j.get('method'),"time":str(datetime.now())[:16]}); save_db(db); return jsonify({"msg":"✅ Withdraw পাঠানো হয়েছে"})
@app.route('/api/profile/save',methods=['POST'])
def profile_save():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); u["name"]=j.get('name',u["name"]);
    if j.get('img'): u["img"]=j.get('img')
    save_db(db); return jsonify({"msg":"✅ Profile Save"})

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}body{background:#000;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.header{background:#0a0a18;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bottomNav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;justify-content:space-around;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #1e1e3a;z-index:99}
.navItem{text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.navItem.active{color:#fff}.navItem span{font-size:24px;display:block}
.page{display:none}.page.active{display:block}

/* HOME */
.balanceCard{background:linear-gradient(135deg,#1e3a8a,#06b6d4);border-radius:24px;padding:18px;text-align:center;margin:12px}
.pill{background:#00000035;padding:7px 14px;border-radius:20px;font-size:13px;border:1px solid #ffffff15}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:800;color:#fff;margin:6px 0;cursor:pointer}

/* WALLET - EXACT LIKE YOUR NEW SCREENSHOT - FIXED */
.walletBalanceExact{background:#1e293b;border-radius:24px;padding:28px;text-align:center;margin:12px;border:1px solid #2d3a4f}
.walletWithdrawExact{background:#131326;border-radius:24px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.methodCardExact{display:flex;align-items:center;gap:14px;background:#1e1e36;border:2px solid #2a2a4a;border-radius:18px;padding:16px;margin:12px 0;cursor:pointer;position:relative}
.methodCardExact.active{border-color:#e2136e;background:#261a3a}
.methodIconExact{width:60px;height:60px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:26px;color:#fff;flex-shrink:0}
.inputExact{width:100%;background:#0e0e20;border:1px solid #25253d;border-radius:14px;padding:18px 16px;color:#9ca3af;margin:12px 0;font-size:15px;outline:none}
.withdrawBtnExact{width:100%;background:linear-gradient(90deg,#e2136e,#ff7a00);border:none;border-radius:14px;padding:18px;font-weight:900;color:#fff;font-size:17px;margin-top:12px;cursor:pointer;box-shadow:0 4px 15px #e2136e40}
</style></head><body>

<div class="header"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:900">Protidiner Kaj BD <span style="background:#22c55e;padding:2px 6px;border-radius:50%;font-size:10px">✓</span></div><div style="font-size:11px;color:#9ca3af">Admin: SHIBLI NOMAN</div></div></div><div style="width:42px;height:42px;border-radius:50%;background:#1e1e3a;border:2px solid #6d4cff;display:flex;align-items:center;justify-content:center" onclick="goP('profile')">👤</div></div>

<div id="p-home" class="page">
<div style="background:linear-gradient(90deg,#ff9a00,#ff5500);border-radius:24px;height:145px;margin:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px">🎉 Daily Bonus Available Today</div>
<div class="balanceCard"><div>💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:54px;font-weight:900" id="balHome">৳1120</div><div style="display:flex;gap:8px;justify-content:center;margin-top:10px"><span class="pill" id="bC">Company 0/30</span><span class="pill" id="bP">Popup 0/20</span><span class="pill" id="bT">Total 0</span></div></div>
<div style="background:#0f0f1f;border-radius:24px;padding:12px;margin:0 12px 12px 12px;border:1px solid #1e1e2e"><button class="btn" style="background:#6d28d9" onclick="doR('company')">📺 COMPANY ADS (৳<span id="cr">2</span>) - <span id="btnC">0/30</span></button><button class="btn" style="background:#16a34a" onclick="doR('popup')">💰 POPUP ADS (৳<span id="pr">3</span>) - <span id="btnP">0/20</span></button><button class="btn" style="background:#232336" onclick="goP('tasks')">📋 TASK BONUS - 5 টা/দিন</button></div>
</div>

<div id="p-tasks" class="page">
<div style="background:#0f0f1f;border-radius:24px;padding:12px;margin:12px;border:1px solid #1e1e2e"><div style="font-size:20px;font-weight:900;padding:8px">📋 Task Bonus - দিনে 5 টা</div>
<div style="display:flex;align-items:center;justify-content:space-between;background:#17172a;border:1px solid #22223a;border-radius:16px;padding:12px 14px;margin:10px 0"><div>✈️ Telegram Channel Join</div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('tele',25)">৳25</button></div>
<div style="display:flex;align-items:center;justify-content:space-between;background:#17172a;border:1px solid #22223a;border-radius:16px;padding:12px 14px;margin:10px 0"><div>▶️ YouTube Subscribe</div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('yt',30)">৳30</button></div>
<div style="display:flex;align-items:center;justify-content:space-between;background:#17172a;border:1px solid #22223a;border-radius:16px;padding:12px 14px;margin:10px 0"><div>👍 Facebook Page Like</div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('fb',20)">৳20</button></div>
</div>
</div>

<!-- WALLET PAGE - FIXED EXACTLY LIKE YOUR IMAGE -->
<div id="p-wallet" class="page active">
<div class="walletBalanceExact">
<div style="color:#8b95a5;font-size:16px">ব্যালেন্স</div>
<div style="font-size:68px;font-weight:900;margin:8px 0;letter-spacing:-2px" id="wBal">৳1120</div>
<div style="color:#7a8594;font-size:15px">Min ৳500</div>
</div>

<div class="walletWithdrawExact">
<div style="font-size:20px;font-weight:900;margin-bottom:16px;display:flex;align-items:center;gap:8px">💸 Withdraw Method</div>

<div class="methodCardExact active" id="bkCard" onclick="selPay('bKash')">
<div class="methodIconExact" style="background:#e2136e">৳</div>
<div style="flex:1"><div style="font-size:17px;font-weight:700">bKash</div><div style="font-size:13px;color:#9ca3af;margin-top:2px">Personal • Instant Payment</div></div>
<div style="color:#22c55e;font-size:20px;font-weight:900" id="bkCheck">✓</div>
</div>

<div class="methodCardExact" id="ngCard" onclick="selPay('Nagad')" style="border-color:#ff1f6e30">
<div class="methodIconExact" style="background:#ff7a00">৳</div>
<div style="flex:1"><div style="font-size:17px;font-weight:700">Nagad</div><div style="font-size:13px;color:#9ca3af;margin-top:2px">Personal • Fast Withdraw</div></div>
<div style="color:#22c55e;font-size:20px;font-weight:900;display:none" id="ngCheck">✓</div>
</div>

<input id="accNum" class="inputExact" placeholder="01XXXXXXXXXX">
<input id="wdAmt" class="inputExact" type="number" placeholder="500">
<button class="withdrawBtnExact" onclick="doWd()">🚀 Withdraw করুন</button>
</div>

<div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px">
<div style="font-weight:800">✅ Withdraw নিয়ম</div><div style="font-size:12px;margin-top:6px;line-height:1.7">• সর্বনিম্ন ৳500<br>• 24 ঘণ্টার মধ্যে পেমেন্ট<br>• ভুল নাম্বারে গেলে দায়ী নন</div>
</div>
</div>

<div id="p-support" class="page">
<div style="background:linear-gradient(135deg,#6d4cff,#4f46e5);border-radius:24px;padding:18px;margin:12px;text-align:center"><div style="background:#00000025;border-radius:16px;padding:12px;margin-bottom:14px">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:50px">💬</div><div style="font-size:22px;font-weight:900">আমরা আছি আপনার পাশে</div><div style="font-size:13px;opacity:.9;margin-top:6px">২৪ ঘণ্টা সাপোর্ট • 100% Trusted</div></div>
<div style="background:#131326;border-radius:20px;padding:14px;margin:12px;border:1px solid #1e1e3a"><div style="font-size:18px;font-weight:900;margin-bottom:12px">🚀 দ্রুত যোগাযোগ করুন</div>
<div style="display:flex;align-items:center;gap:12px;background:#1a1a30;border:1.5px solid #25253d;border-radius:16px;padding:14px;margin:10px 0" onclick="window.open(teleLink,'_blank')"><div style="width:52px;height:52px;background:#0ea5e9;border-radius:14px;display:flex;align-items:center;justify-content:center">✈️</div><div><b>Telegram Support</b><div style="font-size:12px;color:#9ca3af">2 মিনিটে রিপ্লাই</div></div></div>
<div style="display:flex;align-items:center;gap:12px;background:#1a1a30;border:1.5px solid #25253d;border-radius:16px;padding:14px;margin:10px 0" onclick="window.open('https://wa.me/'+wa,'_blank')"><div style="width:52px;height:52px;background:#22c55e;border-radius:14px;display:flex;align-items:center;justify-content:center">💬</div><div><b>WhatsApp Support</b><div style="font-size:12px;color:#9ca3af">01XXXXXXXXXX</div></div></div>
<div style="display:flex;align-items:center;gap:12px;background:#1a1a30;border:1.5px solid #25253d;border-radius:16px;padding:14px;margin:10px 0" onclick="window.location.href='mailto:'+email"><div style="width:52px;height:52px;background:#ff8c00;border-radius:14px;display:flex;align-items:center;justify-content:center">📧</div><div><b>Email Support</b><div style="font-size:12px;color:#9ca3af">support@protidinerkajbd.com</div></div></div>
</div>
</div>

<div id="p-profile" class="page">
<div style="background:#131326;border-radius:24px;padding:20px;margin:12px;border:1px solid #1e1e3a;text-align:center"><div style="width:120px;height:120px;border-radius:50%;border:4px solid #6d4cff;margin:0 auto;background:#0a0a18;display:flex;align-items:center;justify-content:center;font-size:60px" id="avatarBox">👤</div><div style="margin-top:14px;font-size:20px;font-weight:800">User 8385</div><div style="font-size:13px;color:#9ca3af">ID: 8807178385</div><div style="background:#6d4cff;color:#fff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:700;display:inline-block;margin-top:8px">🏅 Bronze Member</div><input id="nameInput" style="width:100%;background:#0e0e20;border:1px solid #25253d;border-radius:14px;padding:14px;color:#fff;margin:10px 0;text-align:center" placeholder="আপনার নাম লিখুন"><button style="width:100%;background:#6d4cff;border:none;border-radius:14px;padding:16px;font-weight:800;color:#fff;cursor:pointer;margin:8px 0" onclick="document.getElementById('filePick').click()">📷 গ্যালারি থেকে ছবি নিন</button><button style="width:100%;background:#16a34a;border:none;border-radius:14px;padding:16px;font-weight:800;color:#fff;cursor:pointer" onclick="saveProfile()">💾 Save Profile</button></div>
</div>

<div class="bottomNav">
<div class="navItem" id="n-home" onclick="goP('home')"><span>🏠</span>Home</div>
<div class="navItem" id="n-tasks" onclick="goP('tasks')"><span>📋</span>Task</div>
<div class="navItem active" id="n-wallet" onclick="goP('wallet')"><span>💰</span>Wallet</div>
<div class="navItem" id="n-support" onclick="goP('support')"><span>💬</span>Support</div>
<div class="navItem" id="n-profile" onclick="goP('profile')"><span>👤</span>Profile</div>
</div>

<input type="file" id="filePick" accept="image/*" style="display:none" onchange="handleFile(this)">
<script>
let uid='8807178385', method='bKash', teleLink='https://t.me/', wa='01XXXXXXXXXX', email='support@protidinerkajbd.com', tempImg='';
function goP(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.navItem').forEach(e=>e.classList.remove('active'));document.getElementById('n-'+p).classList.add('active');}
function init(){
 fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{
  let u=d.user; let s=d.settings;
  document.getElementById('balHome').innerText='৳'+u.balance; document.getElementById('wBal').innerText='৳'+u.balance;
  document.getElementById('bC').innerText='Company '+u.company+'/'+s.company_limit; document.getElementById('bP').innerText='Popup '+u.popup+'/'+s.popup_limit; document.getElementById('bT').innerText='Total '+u.total;
  document.getElementById('btnC').innerText=u.company+'/'+s.company_limit; document.getElementById('btnP').innerText=u.popup+'/'+s.popup_limit;
  document.getElementById('cr').innerText=s.company_reward; document.getElementById('pr').innerText=s.popup_reward;
  teleLink=s.tele_link;
 });
}
function doR(t){ if(typeof show_11764581==='function') show_11764581(); fetch('/api/reward?id='+uid+'&type='+t).then(()=>init());}
function doTask(id,amt){ if(id=='tele') window.open(teleLink,'_blank'); fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function selPay(m){
 method=m;
 document.getElementById('bkCard').classList.toggle('active',m=='bKash');
 document.getElementById('ngCard').classList.toggle('active',m=='Nagad');
 document.getElementById('bkCheck').style.display=m=='bKash'?'block':'none';
 document.getElementById('ngCheck').style.display=m=='Nagad'?'block':'none';
 document.getElementById('ngCard').style.borderColor=m=='Nagad'?'#e2136e':'#2a2a4a';
}
function doWd(){ let num=document.getElementById('accNum').value; let amt=document.getElementById('wdAmt').value; if(!num||!amt){alert('নাম্বার ও টাকা দিন');return;} fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:method})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function handleFile(inp){ let f=inp.files[0]; if(!f) return; let r=new FileReader(); r.onload=function(e){ tempImg=e.target.result; document.getElementById('avatarBox').innerHTML=`<img src="${tempImg}" style="width:100%;height:100%;object-fit:cover;border-radius:50%">`; }; r.readAsDataURL(f); }
function saveProfile(){ let name=document.getElementById('nameInput').value; fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:name||'User 8385',img:tempImg})}).then(r=>r.json()).then(d=>alert(d.msg)); }
init();
</script></body></html>"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
