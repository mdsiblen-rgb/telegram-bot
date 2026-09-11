import os, json, threading, datetime
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "pro_database.json"

app = Flask(__name__)

# === DATABASE ===
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "withdraws": [], "fb_requests": [], "settings": {"min_withdraw": 1000, "ad_reward": 1, "ref_bonus": 50, "fb_reward": 15, "fb_link": "https://www.facebook.com/share/1AXw16vWRj/", "channel": "https://t.me/ProtidinerKajBD"}}
    try:
        with open(DB_FILE, 'r') as f: return json.load(f)
    except: return {"users": {}, "withdraws": [], "fb_requests": [], "settings": {"min_withdraw": 1000, "ad_reward": 1, "ref_bonus": 50, "fb_reward": 15, "fb_link": "https://www.facebook.com/share/1AXw16vWRj/", "channel": "https://t.me/ProtidinerKajBD"}}
def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(d, f, indent=2)

db = load_db()

# === USER MINI APP ===
USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='3485122' data-sdk='show_11764581'></script>
<style>body{max-width:430px;margin:0 auto;background:#eef2ff;font-family:Arial;padding-bottom:80px}.top{background:#1e40af;color:#fff;padding:14px;display:flex;justify-content:space-between;font-weight:bold;position:sticky;top:0}.card{background:#fff;margin:12px;padding:16px;border-radius:18px;box-shadow:0 2px 10px rgba(0,0,0,.05)}button{width:100%;padding:14px;border:none;border-radius:12px;color:#fff;font-weight:bold;margin:6px 0}.ad{background:#1e40af}.fb{background:#1877F2}.bal{font-size:36px;color:#1e40af;font-weight:800;text-align:center}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#fff;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #ddd}.btm div{text-align:center;font-size:11px;color:#777}.btm.on{color:#1e40af;font-weight:bold}.tab{display:none}.tab.on{display:block}</style>
</head><body>
<div class="top"><span>প্রতিদিনের কাজ BD</span><span>৳<span id="bTop">0</span></span></div>
<div id="t-home" class="tab on"><div class="card"><div class="bal">৳<span id="bal">0</span></div><button style="background:#1e40af" onclick="go('earn')">💰 আয় করুন</button></div>
<div class="card"><b>Admin Message</b><br><small>ProtidinerKajBD</small><br><br><b>অফিশিয়াল চ্যানেল</b><br><small>ProtidinerKajBD</small><br><br><button style="background:#111" onclick="go('support')">কিভাবে কাজ করবেন? →</button></div></div>
<div id="t-earn" class="tab"><div class="card"><h3>🎬 Ads দেখে আয়</h3><p>প্রতি Ads: ৳<span id="adR">1</span></p><button class="ad" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button></div>
<div class="card"><h3>👍 Facebook Task - ৳<span id="fbR">15</span></h3><button class="fb" onclick="fbTask()">Follow করুন</button></div>
<div class="card"><h3>👥 Refer - ৳<span id="refR">50</span></h3><p id="refLink"></p><button style="background:#10b981" onclick="copyRef()">Copy Refer Link</button></div></div>
<div id="t-support" class="tab"><div class="card"><p>Admin Message<br>ProtidinerKajBD</p><p>অফিশিয়াল চ্যানেল<br>ProtidinerKajBD</p><button style="background:#111">কিভাবে কাজ করবেন?</button></div></div>
<div id="t-withdraw" class="tab"><div class="card"><div class="bal">৳<span class="bal2">0</span></div><input id="num" placeholder="bKash/Nagad Number"><input id="amt" type="number" placeholder="Amount"><button class="ad" onclick="withdraw()">উইথড্র করুন</button><p>Min: ৳<span id="minW">1000</span></p></div></div>
<div class="btm"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>
<script>
const tg=Telegram.WebApp; const p=new URLSearchParams(location.search); let uid=p.get('id')||tg.initDataUnsafe?.user?.id||"8807178385"; let ref=p.get('ref');
let refLinkEl=document.getElementById('refLink'); refLinkEl.innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;
function copyRef(){navigator.clipboard.writeText(refLinkEl.innerText); alert('Copied!');}
function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{document.getElementById('bal').innerText=d.user.balance.toFixed(0); document.getElementById('bTop').innerText=d.user.balance.toFixed(0); document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance.toFixed(0)); document.getElementById('adR').innerText=d.settings.ad_reward; document.getElementById('fbR').innerText=d.settings.fb_reward; document.getElementById('refR').innerText=d.settings.ref_bonus; document.getElementById('minW').innerText=d.settings.min_withdraw;});}
function watchAd(){show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(()=>{alert('✅ ৳ যোগ হয়েছে'); load();});}).catch(()=>{show_11764581('pop').then(()=>{fetch(`/api/reward?id=${uid}`).then(()=>{alert('✅ ৳ যোগ হয়েছে'); load();});}).catch(()=>alert('No ads, পরে চেষ্টা করুন'));});}
function fbTask(){fetch(`/api/fb_request?id=${uid}`,{method:'POST'}).then(()=>{window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank'); alert('Request গেছে, Admin Approve করলে টাকা পাবেন');});}
function withdraw(){let n=document.getElementById('num').value; let a=document.getElementById('amt').value; if(!n||!a) return alert('Number & Amount দিন'); fetch(`/api/withdraw?id=${uid}&number=${n}&amount=${a}`,{method:'POST'}).then(r=>r.json()).then(d=>{alert(d.msg); load();});}
function go(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on')); document.getElementById('t-'+t).classList.add('on'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); document.getElementById('b-'+t).classList.add('on');}
if(ref && ref!=uid){fetch(`/api/refer?new_id=${uid}&ref_id=${ref}`,{method:'POST'});}
load(); tg.ready(); tg.expand();
show_11764581({type:'inApp',inAppSettings:{frequency:2,capping:0.1,interval:30,timeout:5,everyPage:false}});
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Super Admin - Protidiner Kaj BD</title>
<style>body{font-family:Arial;background:#0f172a;color:#fff;margin:0;padding:10px}.nav{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.nav button{padding:10px 14px;border:none;border-radius:8px;background:#1e293b;color:#fff;cursor:pointer}.nav button.on{background:#1e40af} table{width:100%;background:#1e293b;border-collapse:collapse;margin-top:10px} th,td{padding:8px;border:1px solid #334155;font-size:13px;text-align:center} th{background:#1e40af} input,select{padding:6px;border-radius:6px;border:none}.g{background:#10b981;color:#fff;padding:6px 10px;border:none;border-radius:6px;cursor:pointer}.r{background:#ef4444;color:#fff;padding:6px 10px;border:none;border-radius:6px;cursor:pointer}.b{background:#3b82f6;color:#fff;padding:6px 10px;border:none;border-radius:6px;cursor:pointer}.card{background:#1e293b;padding:14px;border-radius:12px;margin:10px 0}.tab{display:none}.tab.on{display:block}</style>
</head><body>
<h2>👑 SUPER ADMIN PANEL - 8807178385</h2>
<p>Bot: @ProtidinerKaj_BD_Bot | Monetag: 3485122 / Zone 11764581 Active ✅ | FB: facebook.com/share/1AXw16vWRj/</p>
<div class="nav"><button onclick="show('dash')" id="n-dash" class="on">Dashboard</button><button onclick="show('users')" id="n-users">Users</button><button onclick="show('ref')" id="n-ref">Referrals</button><button onclick="show('fb')" id="n-fb">FB Tasks</button><button onclick="show('wd')" id="n-wd">Withdraws</button><button onclick="show('set')" id="n-set">Settings</button><button onclick="show('broad')" id="n-broad">Broadcast</button></div>

<div id="t-dash" class="tab on"><div class="card"><h3>📊 Dashboard</h3><p>Total Users: <span id="tu">0</span> | Total Balance: ৳<span id="tb">0</span> | Total Ads Watched: <span id="ta">0</span> | Total Refer: <span id="tr">0</span> | Pending WD: <span id="pw">0</span></p></div></div>

<div id="t-users" class="tab"><input id="search" placeholder="Search User ID" onkeyup="loadUsers()"><table><thead><tr><th>ID</th><th>Balance</th><th>Ads</th><th>Ref By</th><th>Ref Count</th><th>Action</th></tr></thead><tbody id="users"></tbody></table></div>

<div id="t-ref" class="tab"><table><thead><tr><th>User ID</th><th>Referred By</th><th>Refer List</th></tr></thead><tbody id="reft"></tbody></table></div>

<div id="t-fb" class="tab"><table><thead><tr><th>User ID</th><th>Action</th></tr></thead><tbody id="fbt"></tbody></table></div>

<div id="t-wd" class="tab"><table><thead><tr><th>User ID</th><th>Number</th><th>Amount</th><th>Date</th><th>Action</th></tr></thead><tbody id="wdt"></tbody></table></div>

<div id="t-set" class="tab"><div class="card"><p>Min Withdraw: <input id="s_min" type="number"> Ad Reward: <input id="s_ad" type="number"> Ref Bonus: <input id="s_ref" type="number"> FB Reward: <input id="s_fb" type="number"></p><p>FB Link: <input id="s_fbl" style="width:300px"> Channel: <input id="s_ch" style="width:300px"></p><button class="g" onclick="saveSet()">Save Settings</button></div></div>

<div id="t-broad" class="tab"><div class="card"><textarea id="bmsg" style="width:100%;height:80px" placeholder="Message to all users"></textarea><button class="b" onclick="broadcast()">Send Broadcast to All</button></div></div>

<script>
function show(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('on'));document.getElementById('n-'+t).classList.add('on'); if(t=='users') loadUsers(); if(t=='ref') loadRef(); if(t=='fb') loadFB(); if(t=='wd') loadWD(); if(t=='dash') loadDash(); if(t=='set') loadSet();}
function loadDash(){fetch('/api/admin_stats?admin=8807178385').then(r=>r.json()).then(d=>{document.getElementById('tu').innerText=d.total_users; document.getElementById('tb').innerText=d.total_balance; document.getElementById('ta').innerText=d.total_ads; document.getElementById('tr').innerText=d.total_ref; document.getElementById('pw').innerText=d.pending_wd;});}
function loadUsers(){let s=document.getElementById('search').value.toLowerCase(); fetch('/api/all_users').then(r=>r.json()).then(data=>{let h='';for(let id in data){if(s &&!id.includes(s)) continue; let u=data[id]; h+=`<tr><td>${id}</td><td>৳${u.balance}</td><td>${u.ads_watched||0}</td><td>${u.referred_by||'-'}</td><td>${(u.referrals||[]).length}</td><td><input id="b_${id}" value="${u.balance}" style="width:60px"><button class="b" onclick="upd('${id}')">Update</button> <button class="g" onclick="add('${id}',10)">+10</button><button class="r" onclick="add('${id}',-10)">-10</button> <button class="r" onclick="del('${id}')">Delete</button></td></tr>`;}document.getElementById('users').innerHTML=h;});}
function loadRef(){fetch('/api/all_users').then(r=>r.json()).then(data=>{let h='';for(let id in data){let u=data[id]; h+=`<tr><td>${id}</td><td>${u.referred_by||'-'}</td><td>${(u.referrals||[]).join(', ')||'-'}</td></tr>`;}document.getElementById('reft').innerHTML=h;});}
function loadFB(){fetch('/api/fb_list').then(r=>r.json()).then(l=>{let h='';l.forEach(id=>{h+=`<tr><td>${id}</td><td><button class="g" onclick="apFB('${id}')">Approve</button> <button class="r" onclick="rjFB('${id}')">Reject</button></td></tr>`});document.getElementById('fbt').innerHTML=h;});}
function loadWD(){fetch('/api/wd_list?admin=8807178385').then(r=>r.json()).then(l=>{let h='';l.forEach((w,i)=>{h+=`<tr><td>${w.user_id}</td><td>${w.number}</td><td>৳${w.amount}</td><td>${w.date}</td><td><button class="g" onclick="apWD(${i})">Approve</button> <button class="r" onclick="rjWD(${i})">Reject</button></td></tr>`});document.getElementById('wdt').innerHTML=h;});}
function loadSet(){fetch('/api/get_settings').then(r=>r.json()).then(s=>{document.getElementById('s_min').value=s.min_withdraw; document.getElementById('s_ad').value=s.ad_reward; document.getElementById('s_ref').value=s.ref_bonus; document.getElementById('s_fb').value=s.fb_reward; document.getElementById('s_fbl').value=s.fb_link; document.getElementById('s_ch').value=s.channel;});}
function upd(id){let v=document.getElementById('b_'+id).value; fetch(`/api/admin_update?id=${id}&balance=${v}&admin=8807178385`).then(()=>loadUsers());}
function add(id,a){fetch(`/api/admin_add?id=${id}&amount=${a}&admin=8807178385`).then(()=>loadUsers());}
function del(id){if(confirm('Delete?')) fetch(`/api/admin_delete?id=${id}&admin=8807178385`).then(()=>loadUsers());}
function apFB(id){fetch(`/api/fb_approve?id=${id}&admin=8807178385`).then(()=>{alert('Approved'); loadFB(); loadDash();});}
function rjFB(id){fetch(`/api/fb_reject?id=${id}&admin=8807178385`).then(()=>loadFB());}
function apWD(i){fetch(`/api/wd_approve?index=${i}&admin=8807178385`).then(()=>{alert('Approved'); loadWD();});}
function rjWD(i){fetch(`/api/wd_reject?index=${i}&admin=8807178385`).then(()=>loadWD());}
function saveSet(){let d={min_withdraw:document.getElementById('s_min').value, ad_reward:document.getElementById('s_ad').value, ref_bonus:document.getElementById('s_ref').value, fb_reward:document.getElementById('s_fb').value, fb_link:document.getElementById('s_fbl').value, channel:document.getElementById('s_ch').value, admin:'8807178385'}; fetch('/api/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>alert('Saved!'));}
function broadcast(){let m=document.getElementById('bmsg').value; if(!m) return; fetch(`/api/broadcast?admin=8807178385&msg=${encodeURIComponent(m)}`).then(r=>r.json()).then(d=>alert('Sent to '+d.sent+' users'));}
loadDash();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_panel():
    if str(request.args.get('id'))!=str(ADMIN_ID): return "Not Authorized - Only Super Admin 8807178385", 403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id')
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    return jsonify({"user":db["users"][uid],"settings":db["settings"]})

@app.route('/api/get_user')
def get_user():
    uid=request.args.get('id')
    return jsonify(db["users"].get(uid,{"balance":0}))

@app.route('/api/all_users')
def all_users(): return jsonify(db["users"])

@app.route('/api/reward')
def reward():
    uid=request.args.get('id')
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    db["users"][uid]["balance"]+=int(db["settings"]["ad_reward"])
    db["users"][uid]["ads_watched"]=db["users"][uid].get("ads_watched",0)+1
    save_db(db); return jsonify({"ok":True})

@app.route('/api/refer', methods=['POST'])
def refer():
    new_id=request.args.get('new_id'); ref_id=request.args.get('ref_id')
    if new_id not in db["users"]: db["users"][new_id]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    if db["users"][new_id].get("referred_by"): return jsonify({"ok":False})
    if ref_id not in db["users"]: db["users"][ref_id]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    if new_id==ref_id: return jsonify({"ok":False})
    db["users"][new_id]["referred_by"]=ref_id
    db["users"][ref_id]["referrals"].append(new_id)
    db["users"][ref_id]["balance"]+=int(db["settings"]["ref_bonus"])
    save_db(db); return jsonify({"ok":True})

@app.route('/api/fb_request', methods=['POST'])
def fb_req():
    uid=request.args.get('id')
    if uid not in db["fb_requests"]: db["fb_requests"].append(uid); save_db(db)
    return jsonify({"ok":True})
@app.route('/api/fb_list')
def fb_list(): return jsonify(db["fb_requests"])
@app.route('/api/fb_approve')
def fb_approve():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id')
    if uid in db["fb_requests"]: db["fb_requests"].remove(uid)
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    db["users"][uid]["balance"]+=int(db["settings"]["fb_reward"]); save_db(db); return jsonify({"ok":True})
@app.route('/api/fb_reject')
def fb_reject():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id')
    if uid in db["fb_requests"]: db["fb_requests"].remove(uid); save_db(db)
    return jsonify({"ok":True})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    uid=request.args.get('id'); number=request.args.get('number'); amount=int(request.args.get('amount',0))
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    if db["users"][uid]["balance"]<amount: return jsonify({"msg":"Balance কম আছে"})
    if amount<int(db["settings"]["min_withdraw"]): return jsonify({"msg":f"Min {db['settings']['min_withdraw']} লাগবে"})
    db["users"][uid]["balance"]-=amount
    db["withdraws"].append({"user_id":uid,"number":number,"amount":amount,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_db(db); return jsonify({"msg":"✅ Withdraw Request গেছে, Admin Approve করবে"})

@app.route('/api/wd_list')
def wd_list():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    return jsonify(db["withdraws"])
@app.route('/api/wd_approve')
def wd_approve():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    idx=int(request.args.get('index')); db["withdraws"].pop(idx); save_db(db); return jsonify({"ok":True})
@app.route('/api/wd_reject')
def wd_reject():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    idx=int(request.args.get('index')); w=db["withdraws"][idx]; db["users"][w["user_id"]]["balance"]+=w["amount"]; db["withdraws"].pop(idx); save_db(db); return jsonify({"ok":True})

@app.route('/api/admin_update')
def admin_update():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); bal=int(request.args.get('balance')); db["users"][uid]["balance"]=bal; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_add')
def admin_add():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); amt=int(request.args.get('amount')); db["users"][uid]["balance"]+=amt; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_delete')
def admin_delete():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); del db["users"][uid]; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_stats')
def admin_stats():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    total_users=len(db["users"]); total_bal=sum([u["balance"] for u in db["users"].values()]); total_ads=sum([u.get("ads_watched",0) for u in db["users"].values()]); total_ref=sum([len(u.get("referrals",[])) for u in db["users"].values()])
    return jsonify({"total_users":total_users,"total_balance":total_bal,"total_ads":total_ads,"total_ref":total_ref,"pending_wd":len(db["withdraws"])})
@app.route('/api/get_settings')
def get_settings(): return jsonify(db["settings"])
@app.route('/api/save_settings', methods=['POST'])
def save_settings():
    data=request.json
    if str(data.get('admin'))!=str(ADMIN_ID): return "No",403
    db["settings"]["min_withdraw"]=int(data["min_withdraw"]); db["settings"]["ad_reward"]=int(data["ad_reward"]); db["settings"]["ref_bonus"]=int(data["ref_bonus"]); db["settings"]["fb_reward"]=int(data["fb_reward"]); db["settings"]["fb_link"]=data["fb_link"]; db["settings"]["channel"]=data["channel"]; save_db(db); return jsonify({"ok":True})
@app.route('/api/broadcast')
def broadcast():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    msg=request.args.get('msg'); return jsonify({"sent":len(db["users"]), "msg":msg})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id); args=context.args
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    if args and args[0]!=uid:
        ref_id=args[0]
        if not db["users"][uid].get("referred_by") and ref_id in db["users"] and ref_id!=uid:
            db["users"][uid]["referred_by"]=ref_id; db["users"][ref_id]["referrals"].append(uid); db["users"][ref_id]["balance"]+=int(db["settings"]["ref_bonus"])
    save_db(db)
    kb=[[InlineKeyboardButton("💰 Open Earning App", web_app={"url": f"https://am-bot-1-v77g.onrender.com/?id={uid}"})]]
    if str(uid)==str(ADMIN_ID): kb.append([InlineKeyboardButton("👑 Super Admin Panel", url=f"https://am-bot-1-v77g.onrender.com/admin?id={uid}")])
    await update.message.reply_text(f"Welcome to Protidiner Kaj BD Official ✅\n\nYour ID: {uid}\nBalance: ৳{db['users'][uid]['balance']}\nRefer Bonus: ৳{db['settings']['ref_bonus']}\n\nRefer Link: https://t.me/ProtidinerKaj_BD_Bot?start={uid}", reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    application=Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

def run_flask(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__=='__main__':
    threading.Thread(target=run_bot).start()
    run_flask()
