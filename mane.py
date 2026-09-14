import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def load_db():
    if not os.path.exists(DB):
        d={"users":{},"withdraws":[],"settings":{
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN",
            "company_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"balance_target":2000,"min_withdraw":500,
            "tele_link":"https://t.me/","whatsapp":"01XXXXXXXXXX","email":"support@protidinerkajbd.com","yt_tutorial":"https://youtube.com/"
        }}
        open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
        return d
    return json.load(open(DB,'r',encoding='utf-8'))

def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))

def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":"User 8385","balance":1120,"company":0,"popup":0,"total":0,"tasks":[],"img":"","join":"2026-09-13","work":0}
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(HTML)

# --- ADMIN PANEL FIX - এটা না থাকলে Not Found আসে ---
@app.route('/admin')
def admin_panel():
    if request.args.get('id')!= '8807178385':
        return "<h2>❌ Access Denied - Use /admin?id=8807178385</h2>", 403
    return render_template_string(ADMIN_HTML)

@app.route('/api/admin/get')
def admin_get():
    return jsonify(load_db())

@app.route('/api/admin/save', methods=['POST'])
def admin_save():
    db=load_db()
    data=request.json
    if 'settings' in data:
        db["settings"].update(data['settings'])
    save_db(db)
    return jsonify({"msg":"✅ Save হয়েছে"})

@app.route('/api/get')
def api_get():
    db=load_db()
    u=get_user(db,request.args.get('id','8807178385'))
    save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"withdraws":[w for w in db["withdraws"] if w["uid"]==u["id"]]})

@app.route('/api/reward')
def reward():
    db=load_db(); u=get_user(db,request.args.get('id')); t=request.args.get('type'); s=db["settings"]
    if t=='company':
        if u["company"]>=int(s["company_limit"]): return jsonify({"msg":"Limit শেষ"})
        u["company"]+=1; u["balance"]+=int(s["company_reward"])
    else:
        if u["popup"]>=int(s["popup_limit"]): return jsonify({"msg":"Limit শেষ"})
        u["popup"]+=1; u["balance"]+=int(s["popup_reward"])
    u["total"]=u["company"]+u["popup"]; u["work"]=u["total"]
    save_db(db)
    return jsonify({"ok":1})

@app.route('/api/task/done',methods=['POST'])
def task_done():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); tid=j.get('tid'); amt=int(j.get('amt',0))
    if tid not in u["tasks"]:
        u["tasks"].append(tid); u["balance"]+=amt
    save_db(db)
    return jsonify({"msg":f"✅ ৳{amt} Bonus"})

@app.route('/api/withdraw',methods=['POST'])
def withdraw():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); amt=int(j.get('amt',0))
    if amt<int(db["settings"]["min_withdraw"]): return jsonify({"msg":f"Min ৳{db['settings']['min_withdraw']}"})
    if u["balance"]<amt: return jsonify({"msg":"❌ ব্যালেন্স কম"})
    u["balance"]-=amt
    db["withdraws"].append({"uid":u["id"],"amt":amt,"num":j.get('num'),"method":j.get('method'),"time":str(datetime.now())[:16],"status":"Pending"})
    save_db(db)
    return jsonify({"msg":"✅ Withdraw পাঠানো হয়েছে"})

@app.route('/api/profile/save',methods=['POST'])
def profile_save():
    db=load_db(); j=request.json; u=get_user(db,j.get('id'))
    if j.get('name'): u["name"]=j.get('name')
    if j.get('img'): u["img"]=j.get('img')
    save_db(db)
    return jsonify({"msg":"✅ Profile Save"})

ADMIN_HTML="""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin Panel</title>
<style>body{background:#070710;color:#fff;max-width:600px;margin:0 auto;padding:12px;font-family:system-ui}.card{background:#15152a;border-radius:16px;padding:14px;margin:12px 0}input{width:100%;padding:10px;border-radius:10px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:5px}label{font-size:11px;color:#aaa;margin-top:8px;display:block}.btn{width:100%;padding:14px;background:#6d4cff;border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:12px;cursor:pointer}</style>
</head><body><h2 style="text-align:center">👑 SUPER ADMIN - Protidiner Kaj BD</h2>
<div class="card"><h3>⚙️ Settings</h3><div id="box"></div></div>
<script>
function load(){
 fetch('/api/admin/get').then(r=>r.json()).then(d=>{
  let s=d.settings; let h='';
  for(let k in s){ h+=`<label>${k}</label><input id="${k}" value="${s[k]}">`; }
  h+=`<button class=btn onclick=saveAll()>💾 SAVE ALL</button>`;
  document.getElementById('box').innerHTML=h;
 });
}
function saveAll(){
 let s={}; document.querySelectorAll('input').forEach(e=>s[e.id]=e.value);
 fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:s})})
.then(r=>r.json()).then(d=>alert(d.msg));
}
load();
</script></body></html>"""

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}body{background:#000;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.header{background:#0a0a18;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bottomNav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#121225;display:flex;justify-content:space-around;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #1e1e3a;z-index:99}
.navItem{text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.navItem.active{color:#fff}.navItem span{font-size:24px;display:block}
.page{display:none}.page.active{display:block}
.balanceCard{background:linear-gradient(135deg,#1e3a8a,#2563eb,#06b6d4);border-radius:24px;padding:20px 16px;text-align:center;margin:12px}
.pill{background:#00000035;padding:7px 14px;border-radius:20px;font-size:13px;border:1px solid #ffffff15}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:800;color:#fff;margin:6px 0;cursor:pointer}
.boxDark{background:#131326;border-radius:24px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.rowCard{display:flex;align-items:center;justify-content:space-between;background:#1a1a30;border:1px solid #25253d;border-radius:16px;padding:14px;margin:10px 0}
.walletBal{background:#1e293b;border-radius:24px;padding:32px;text-align:center;margin:12px;border:1px solid #2d3a4f}
.wMethod{background:#131326;border-radius:24px;padding:16px;margin:12px;border:1px solid #1e1e3a}
.mCard{display:flex;align-items:center;gap:14px;background:#1e1e36;border:2px solid #2a2a4a;border-radius:18px;padding:16px;margin:12px 0;cursor:pointer}
.mCard.active{border-color:#e2136e;background:#261a3a}
.mIcon{width:62px;height:62px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:28px;color:#fff}
.inputF{width:100%;background:#0e0e20;border:1px solid #25253d;border-radius:14px;padding:18px;color:#9ca3af;margin:12px 0;font-size:15px;outline:none}
.wBtn{width:100%;background:linear-gradient(90deg,#e2136e,#ff7a00);border:none;border-radius:14px;padding:18px;font-weight:900;color:#fff;font-size:17px;margin-top:8px;cursor:pointer}
</style></head><body>
<div class="header"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:900">Protidiner Kaj BD <span style="background:#22c55e;padding:2px 6px;border-radius:50%;font-size:10px">✓</span></div><div style="font-size:11px;color:#9ca3af">Admin: SHIBLI NOMAN</div></div></div><div style="width:42px;height:42px;border-radius:50%;background:#1e1e3a;border:2px solid #6d4cff;display:flex;align-items:center;justify-content:center" onclick="goP('profile')">👤</div></div>
<div id="p-home" class="page active"><div style="background:linear-gradient(90deg,#ff9a00,#ff3d00);border-radius:24px;height:145px;margin:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px">🎉 Daily Bonus Available Today</div><div class="balanceCard"><div>💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:56px;font-weight:900" id="balHome">৳1120</div><div style="display:flex;gap:8px;justify-content:center"><span class="pill" id="bC">Company 0/30</span><span class="pill" id="bP">Popup 0/20</span><span class="pill" id="bT">Total 0</span></div></div><div class="boxDark"><button class="btn" style="background:#6d28d9" onclick="doR('company')">📺 COMPANY ADS (৳<span id="cr">2</span>) - <span id="btnC">0/30</span></button><button class="btn" style="background:#16a34a" onclick="doR('popup')">💰 POPUP ADS (৳<span id="pr">3</span>) - <span id="btnP">0/20</span></button><button class="btn" style="background:#232336" onclick="goP('tasks')">📋 TASK BONUS - 5 টা/দিন</button></div></div>
<div id="p-tasks" class="page"><div class="boxDark"><div style="font-size:20px;font-weight:900">📋 Task Bonus - দিনে 5 টা</div><div class="rowCard"><div>✈️ Telegram Channel Join</div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('tele',25)">৳25</button></div><div class="rowCard"><div>▶️ YouTube Subscribe</div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('yt',30)">৳30</button></div><div class="rowCard"><div>👍 Facebook Page Like</div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('fb',20)">৳20</button></div></div></div>
<div id="p-wallet" class="page"><div class="walletBal"><div style="color:#8b95a5">ব্যালেন্স</div><div style="font-size:72px;font-weight:900" id="wBal">৳1120</div><div style="color:#7a8594">Min ৳500</div></div><div class="wMethod"><div style="font-size:20px;font-weight:900;margin-bottom:12px">💸 Withdraw Method</div><div class="mCard active" id="bkCard" onclick="selPay('bKash')"><div class="mIcon" style="background:#e2136e">৳</div><div style="flex:1"><div style="font-weight:700">bKash</div><div style="font-size:13px;color:#9ca3af">Personal • Instant Payment</div></div><div style="color:#22c55e;font-size:20px" id="bkCheck">✓</div></div><div class="mCard" id="ngCard" onclick="selPay('Nagad')"><div class="mIcon" style="background:#ff7a00">৳</div><div style="flex:1"><div style="font-weight:700">Nagad</div><div style="font-size:13px;color:#9ca3af">Personal • Fast Withdraw</div></div><div style="color:#22c55e;font-size:20px;display:none" id="ngCheck">✓</div></div><input id="accNum" class="inputF" placeholder="01XXXXXXXXXX"><input id="wdAmt" class="inputF" type="number" placeholder="500"><button class="wBtn" onclick="doWd()">🚀 Withdraw করুন</button></div></div>
<div id="p-support" class="page"><div style="background:linear-gradient(135deg,#6d4cff,#4f46e5);border-radius:24px;padding:18px;margin:12px;text-align:center"><div style="font-size:22px;font-weight:900">আমরা আছি আপনার পাশে</div><div style="font-size:13px;opacity:.9;margin-top:6px">২৪ ঘণ্টা সাপোর্ট • 100% Trusted</div></div><div class="boxDark"><div class="rowCard" onclick="window.open(teleLink,'_blank')"><div><b>Telegram Support</b><div style="font-size:12px;color:#9ca3af">2 মিনিটে রিপ্লাই</div></div><div>➡️</div></div><div class="rowCard" onclick="openWa()"><div><b>WhatsApp Support</b><div style="font-size:12px;color:#9ca3af" id="waNum">01XXXXXXXXXX</div></div><div>➡️</div></div><div class="rowCard" onclick="openEmail()"><div><b>Email Support</b><div style="font-size:12px;color:#9ca3af" id="emTxt">support@protidinerkajbd.com</div></div><div>➡️</div></div></div></div>
<div id="p-profile" class="page"><div style="background:#131326;border-radius:24px;padding:20px;margin:12px;border:1px solid #1e1e3a;text-align:center"><div style="width:120px;height:120px;border-radius:50%;border:4px solid #6d4cff;margin:0 auto;background:#0a0a18;display:flex;align-items:center;justify-content:center;font-size:60px;overflow:hidden;position:relative" id="avatarBox">👤</div><div style="margin-top:14px;font-size:20px;font-weight:800" id="pNameTop">User 8385</div><div style="font-size:13px;color:#9ca3af" id="pIdTop">ID: 8807178385</div><div style="background:#6d4cff;color:#fff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:700;display:inline-block;margin-top:8px">🏅 Bronze Member</div></div></div>
<div class="bottomNav"><div class="navItem active" id="n-home" onclick="goP('home')"><span>🏠</span>Home</div><div class="navItem" id="n-tasks" onclick="goP('tasks')"><span>📋</span>Task</div><div class="navItem" id="n-wallet" onclick="goP('wallet')"><span>💰</span>Wallet</div><div class="navItem" id="n-support" onclick="goP('support')"><span>💬</span>Support</div><div class="navItem" id="n-profile" onclick="goP('profile')"><span>👤</span>Profile</div></div>
<script>
let uid='8807178385', method='bKash', teleLink='https://t.me/', wa='01XXXXXXXXXX', email='support@protidinerkajbd.com', ytTut='https://youtube.com/';
function goP(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.navItem').forEach(e=>e.classList.remove('active'));document.getElementById('n-'+p).classList.add('active');}
function init(){ fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ let u=d.user; let s=d.settings; document.getElementById('balHome').innerText='৳'+u.balance; document.getElementById('wBal').innerText='৳'+u.balance; document.getElementById('bC').innerText='Company '+u.company+'/'+s.company_limit; document.getElementById('bP').innerText='Popup '+u.popup+'/'+s.popup_limit; document.getElementById('bT').innerText='Total '+u.total; document.getElementById('btnC').innerText=u.company+'/'+s.company_limit; document.getElementById('btnP').innerText=u.popup+'/'+s.popup_limit; document.getElementById('cr').innerText=s.company_reward; document.getElementById('pr').innerText=s.popup_reward; teleLink=s.tele_link; wa=s.whatsapp; email=s.email; });}
function doR(t){ if(typeof show_11764581==='function') show_11764581(); fetch('/api/reward?id='+uid+'&type='+t).then(()=>init());}
function doTask(id,amt){ if(id=='tele') window.open(teleLink,'_blank'); fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function selPay(m){ method=m; document.getElementById('bkCard').classList.toggle('active',m=='bKash'); document.getElementById('ngCard').classList.toggle('active',m=='Nagad'); document.getElementById('bkCheck').style.display=m=='bKash'?'block':'none'; document.getElementById('ngCheck').style.display=m=='Nagad'?'block':'none';}
function doWd(){ let num=document.getElementById('accNum').value; let amt=document.getElementById('wdAmt').value; if(!num||!amt){alert('নাম্বার ও টাকা দিন');return;} fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:method})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function openWa(){ window.open('https://wa.me/'+wa,'_blank'); }
function openEmail(){ window.location.href='mailto:'+email; }
init();
</script></body></html>"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
