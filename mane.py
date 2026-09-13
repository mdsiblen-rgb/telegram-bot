import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def load_db():
    if not os.path.exists(DB):
        d={"users":{},"withdraws":[],"settings":{"bonus":1120,"min_with":500,"bkash_logo":"","nagad_logo":"","bkash_name":"bKash","nagad_name":"Nagad","tele_link":"https://t.me/","wa_link":"https://wa.me/8801","yt_link":"https://youtube.com/","zone":"11764581"}}
        with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d
    with open(DB,'r',encoding='utf-8') as f: return json.load(f)
def save_db(d):
    with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","balance":1120,"ads_today":0,"total":0,"profile_img":"","join_date":today,"last":today,"phone":uid}
    u=db["users"][uid]
    if u.get("last")!=today: u["ads_today"]=0; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/admin')
def admin_page():
    if request.args.get('id')!='8807178385': return "Admin?id=8807178385"
    return render_template_string(ADMIN)
@app.route('/api/get')
def api_get():
    db=load_db(); u=get_user(db,request.args.get('id','0')); save_db(db)
    return jsonify({"user":u,"settings":db["settings"]})
@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id')); u["balance"]+=2; u["ads_today"]+=1; save_db(db)
    return jsonify({"msg":"৳2 যোগ"})
@app.route('/api/admin/save',methods=['POST'])
def save():
    db=load_db(); j=request.json
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ Save - Halka MitMit OK"})
@app.route('/api/profile/update',methods=['POST'])
def prof():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); u["profile_img"]=j.get('img',''); save_db(db); return jsonify({"msg":"✅ Profile Save"})

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#0a0a14;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}
.top{padding:12px;background:#0f0f1e;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.card{margin:12px;border-radius:16px;padding:14px;background:#15152a;border:1px solid #23233a}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;margin-top:8px;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;padding:8px 0;border-radius:20px 20px 0 0;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
#lockOverlay{position:fixed;inset:0;z-index:999;background:#0a0a14f2;display:flex;justify-content:center;align-items:center;padding:20px}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #2a2a4a;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.payCard.active{border-color:#e2136e}.payLogo{width:56px;height:56px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;color:#000;font-weight:900}.payLogo img{width:100%;height:100%;object-fit:contain}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}
.page{display:none}.page.active{display:block}
/* HALKA MIT MIT - শুধু হালকা আলো, কোনো লাফালাফি নাই */
.halka-mitmit{animation:halkaGlow 2.5s ease-in-out infinite; border:1.5px solid #6d4cff40!important}
@keyframes halkaGlow{
  0%{box-shadow:0 0 6px #6d4cff30}
  50%{box-shadow:0 0 14px #6d4cff60, 0 0 20px #06b6d430}
  100%{box-shadow:0 0 6px #6d4cff30}
}
.halka-mitmit2{animation:halkaGlow2 2.5s ease-in-out infinite 1.2s; border:1.5px solid #f59e0b40!important}
@keyframes halkaGlow2{
  0%{box-shadow:0 0 6px #f59e0b30}
  50%{box-shadow:0 0 14px #f59e0b50, 0 0 20px #ef444430}
  100%{box-shadow:0 0 6px #f59e0b30}
}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:28px">👑</div><div><b>Protidiner Kaj BD ✓</b><div style="font-size:11px;color:#aaa">SHIBLI NOMAN</div></div></div><div id="topAv" style="width:44px;height:44px;border-radius:50%;border:2px solid #6d4cff;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden"><img id="topAvImg" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="topAvTxt">👤</span></div></div>

<div id="lockOverlay"><div style="background:#fff;color:#000;padding:20px;border-radius:20px;width:100%;max-width:320px;text-align:center"><div style="font-size:36px">🔒</div><h3 style="color:#6d4cff">লকিং সিস্টেম</h3><p style="font-size:11px;font-weight:700;margin-top:4px">নাম্বার দিয়ে লক করুন - ইউজার নিজে লক করতে পারবে</p><input id="phoneInput" type="tel" placeholder="01XXXXXXXXX" maxlength="11" style="background:#f5f3ff;color:#000"><button class="btn" style="background:#6d4cff" onclick="sendOTP()">📲 OTP পাঠান (1234)</button><div id="otpSection" style="display:none"><input id="otpInput" placeholder="1234" maxlength="4" style="background:#f5f3ff;color:#000"><button class="btn" style="background:#10b981" onclick="verifyOTP()">✅ লক করুন</button></div></div></div>

<div id="p-home" class="page active">
<div class="card halka-mitmit2" style="background:linear-gradient(90deg,#f59e0b,#ef4444);text-align:center;border:none;height:130px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px">🎉 Daily Bonus Available Today</div>
<div class="card halka-mitmit" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4);text-align:center;border:none"><div>💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:40px;font-weight:900" id="balMain">৳1120</div><div id="c1" style="font-size:12px;background:#0003;padding:6px 12px;border-radius:20px;display:inline-block;margin-top:6px">Ads 0/30</div></div>
<div class="card"><button class="btn" style="background:#7c3aed" onclick="watchAd()">📺 COMPANY ADS (৳2)</button><button class="btn" style="background:#10b981" onclick="watchAd()">💰 POPUP ADS (৳3)</button><button class="btn" style="background:#1e293b" onclick="goPage('tasks')">📋 TASK BONUS</button></div>
</div>

<div id="p-tasks" class="page"><div class="card"><h3>📋 Task Bonus</h3><div style="background:linear-gradient(135deg,#6d4cff,#4f46e5);padding:14px;border-radius:14px;margin-top:10px"><b>🎁 Refer & Earn ৳50</b><div id="refLink" style="font-size:10px;background:#0003;padding:8px;border-radius:8px;margin-top:6px;word-break:break-all"></div><button class="btn" style="background:#fff;color:#6d4cff" onclick="copyRef()">📋 কপি</button></div></div></div>

<div id="p-wallet" class="page"><div class="card halka-mitmit" style="background:linear-gradient(135deg,#1e293b,#334155);text-align:center;border:none"><div>ব্যালেন্স</div><div style="font-size:44px;font-weight:900" id="walletBal">৳1120</div><div style="font-size:12px">Min ৳500</div></div><div class="card"><h3>💸 Withdraw Method - লোগো এডমিন থেকে</h3><div id="bkashOpt" class="payCard active" onclick="selectMethod('bKash')"><div class="payLogo"><img id="bkashImg" src="" style="display:none"><span id="bkashTxt">bK</span></div><div style="flex:1"><b id="bkashName">bKash</b><div style="font-size:11px;color:#aaa">Personal • Instant</div></div><div style="color:#10b981">✓</div></div><div id="nagadOpt" class="payCard" onclick="selectMethod('Nagad')"><div class="payLogo"><img id="nagadImg" src="" style="display:none"><span id="nagadTxt">Na</span></div><div style="flex:1"><b id="nagadName">Nagad</b><div style="font-size:11px;color:#aaa">Personal • Fast</div></div></div><input id="accNum" placeholder="01XXXXXXXXX"><input id="amount" type="number" placeholder="500"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f59e0b)" onclick="alert('Withdraw Request')">🚀 Withdraw করুন</button></div></div>

<div id="p-support" class="page"><div class="card halka-mitmit" style="background:linear-gradient(135deg,#6d4cff,#4f46e5);text-align:center;border:none"><div style="background:#0003;padding:10px;border-radius:12px;font-size:13px">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:20px;font-weight:900;margin-top:10px">আমরা আছি আপনার পাশে</div></div><div class="card"><h3>🚀 দ্রুত যোগাযোগ</h3><div class="payCard" onclick="openLink('tele_link')"><div style="width:48px;height:48px;background:#0ea5e9;border-radius:12px;display:flex;align-items:center;justify-content:center">✈️</div><div style="flex:1"><b>Telegram Support</b></div><div>➡️</div></div><div class="payCard" onclick="openLink('wa_link')"><div style="width:48px;height:48px;background:#22c55e;border-radius:12px;display:flex;align-items:center;justify-content:center">💬</div><div style="flex:1"><b>WhatsApp Support</b></div><div>➡️</div></div><div class="payCard" onclick="openLink('yt_link')"><div style="width:48px;height:48px;background:#f59e0b;border-radius:12px;display:flex;align-items:center;justify-content:center">▶️</div><div style="flex:1"><b>🎥 Tutorial Video - YouTube - Admin Link</b></div><div>➡️</div></div></div></div>

<div id="p-profile" class="page"><div class="card" style="text-align:center"><div style="width:80px;height:80px;border-radius:50%;background:#1e293b;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:36px;overflow:hidden" id="profAv"><img id="profAvImg" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="profAvTxt">👤</span></div><h3 id="profName" style="margin-top:8px">User</h3><p id="profPhone" style="font-size:12px;color:#aaa">01XXXXXXXXX</p><button class="btn" style="background:#ef4444;margin-top:10px" onclick="logoutLock()">🚪 লগআউট / অন্য নাম্বার দিয়ে লক</button><input id="profileImgInput" placeholder="https://... প্রোফাইল ছবির লিংক" style="margin-top:12px"><button class="btn" style="background:#6d4cff" onclick="updateProfileImg()">💾 প্রোফাইল ছবি সেভ</button></div></div>

<div class="btm"><div id="nav-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div><div id="nav-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div><div id="nav-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div><div id="nav-support" onclick="goPage('support')"><span>💬</span>Support</div><div id="nav-profile" onclick="goPage('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=localStorage.getItem('locked_phone')||''; let settings={};
function initApp(){ if(!uid){document.getElementById('lockOverlay').style.display='flex';return;} document.getElementById('lockOverlay').style.display='none'; fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ settings=d.settings; let u=d.user; document.getElementById('balMain').innerText='৳'+u.balance; document.getElementById('walletBal').innerText='৳'+u.balance; document.getElementById('c1').innerText='Ads '+u.ads_today+'/30'; document.getElementById('profName').innerText=u.name; document.getElementById('profPhone').innerText=u.phone; document.getElementById('refLink').innerText=location.origin+'/?ref='+uid;
if(settings.bkash_logo && settings.bkash_logo.startsWith('http')){ document.getElementById('bkashImg').src=settings.bkash_logo; document.getElementById('bkashImg').style.display='block'; document.getElementById('bkashTxt').style.display='none'; }
if(settings.nagad_logo && settings.nagad_logo.startsWith('http')){ document.getElementById('nagadImg').src=settings.nagad_logo; document.getElementById('nagadImg').style.display='block'; document.getElementById('nagadTxt').style.display='none'; }
if(u.profile_img && u.profile_img.startsWith('http')){ document.getElementById('topAvImg').src=u.profile_img; document.getElementById('topAvImg').style.display='block'; document.getElementById('topAvTxt').style.display='none'; document.getElementById('profAvImg').src=u.profile_img; document.getElementById('profAvImg').style.display='block'; document.getElementById('profAvTxt').style.display='none'; }
});}
function sendOTP(){ let p=document.getElementById('phoneInput').value; if(p.length!=11){alert('11 digit দিন');return;} document.getElementById('otpSection').style.display='block';}
function verifyOTP(){ let o=document.getElementById('otpInput').value; let p=document.getElementById('phoneInput').value; if(o!='1234'){alert('OTP 1234');return;} localStorage.setItem('locked_phone',p); uid=p; document.getElementById('lockOverlay').style.display='none'; initApp();}
function goPage(p){ document.querySelectorAll('.page').forEach(e=>e.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on')); document.getElementById('nav-'+p).classList.add('on');}
function watchAd(){ fetch('/api/reward?id='+uid).then(r=>r.json()).then(d=>{alert(d.msg); initApp();}); if(typeof show_11764581==='function') show_11764581();}
function selectMethod(m){ document.getElementById('bkashOpt').classList.toggle('active',m==='bKash'); document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad');}
function openLink(k){ let l=settings[k]; if(l) window.open(l,'_blank'); }
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('কপি');}
function logoutLock(){ if(confirm('লগআউট?')){ localStorage.removeItem('locked_phone'); location.reload(); }}
function updateProfileImg(){ let img=document.getElementById('profileImgInput').value; if(!img.startsWith('http')){alert('https:// লিংক দিন');return;} fetch('/api/profile/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,img:img})}).then(r=>r.json()).then(d=>{alert(d.msg); initApp();});}
initApp();
</script></body></html>
"""

ADMIN="""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin - Halka MitMit</title><style>*{box-sizing:border-box;font-family:system-ui}body{background:#070710;color:#fff;max-width:600px;margin:0 auto;padding:16px}.card{background:#15152a;border:1px solid #222;border-radius:14px;padding:14px;margin:10px 0}input{width:100%;padding:10px;border-radius:8px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}.btn{padding:12px;width:100%;border:none;border-radius:8px;font-weight:800;background:#6d4cff;color:#fff;cursor:pointer;margin-top:10px}</style></head><body>
<h2>👑 Admin - Halka MitMit + Logo + Locking</h2>
<div class="card" style="border:2px solid #e2136e"><h3>💳 bKash / Nagad Logo - এডমিন থেকে চেঞ্জ</h3>
bKash Logo URL: <input id="bkash_logo" placeholder="https://.../bkash.png"><br>
Nagad Logo URL: <input id="nagad_logo" placeholder="https://.../nagad.png"><br>
<p style="font-size:11px;color:#aaa">লিংক বসালেই Wallet এ লোগো চেঞ্জ হবে</p>
</div>
<div class="card"><h3>🎥 YouTube + Telegram + WhatsApp Link - Admin</h3>
Telegram Link: <input id="tele_link"><br>WhatsApp Link: <input id="wa_link"><br>YouTube Video Link: <input id="yt_link"><br></div>
<div class="card" style="border:2px solid #6d4cff"><h3>✨ MitMit Setting - হালকা করা আছে</h3><p style="font-size:12px;color:#aaa">এখন scale নাই, শুধু হালকা আলো জ্বলবে নিভবে 2.5 সেকেন্ডে একবার। লাফাবে না।</p></div>
<button class="btn" onclick="save()">💾 Save - Halka MitMit</button><div id="msg" style="color:#10b981;margin-top:10px"></div>
<script>
function load(){ fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{ for(let k in d.settings){ let el=document.getElementById(k); if(el) el.value=d.settings[k]; } }); }
function save(){ let data={}; document.querySelectorAll('input').forEach(e=>{ if(e.id) data[e.id]=e.value; }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ document.getElementById('msg').innerText=d.msg; alert(d.msg); }); }
load();
</script></body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
