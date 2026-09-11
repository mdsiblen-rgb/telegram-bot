import os, json, threading, datetime
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "pro_database.json"

app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "withdraws": [], "fb_requests": [], "settings": {"min_withdraw": 1000, "ad_reward": 1, "ref_bonus": 50, "fb_reward": 15, "fb_link": "https://www.facebook.com/share/1AXw16vWRj/", "channel": "https://t.me/ProtidinerKajBD", "youtube": "https://youtube.com/@ProtidinerKajBD"}}
    try:
        with open(DB_FILE, 'r') as f: return json.load(f)
    except: return {"users": {}, "withdraws": [], "fb_requests": [], "settings": {"min_withdraw": 1000, "ad_reward": 1, "ref_bonus": 50, "fb_reward": 15, "fb_link": "https://www.facebook.com/share/1AXw16vWRj/", "channel": "https://t.me/ProtidinerKajBD", "youtube": "https://youtube.com/@ProtidinerKajBD"}}
def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(d, f, indent=2)
db = load_db()

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='3485122' data-sdk='show_11764581'></script>
<style>body{max-width:430px;margin:0 auto;background:#eef2ff;font-family:Arial;padding-bottom:80px}.top{background:#1e40af;color:#fff;padding:14px;display:flex;justify-content:space-between;font-weight:bold;position:sticky;top:0}.card{background:#fff;margin:12px;padding:16px;border-radius:18px;box-shadow:0 2px 10px rgba(0,0,0,.05)}button{width:100%;padding:14px;border:none;border-radius:12px;color:#fff;font-weight:bold;margin:6px 0}.ad{background:#1e40af}.fb{background:#1877F2}.bal{font-size:36px;color:#1e40af;font-weight:800;text-align:center}.tab{display:none}.tab.on{display:block}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#fff;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #ddd}.btm div{text-align:center;font-size:11px;color:#777;cursor:pointer}.btm div.on{color:#1e40af;font-weight:bold}</style>
</head><body>
<div class="top"><span>প্রতিদিনের কাজ BD</span><span>৳<span id="bTop">0</span></span></div>
<div id="t-home" class="tab on"><div class="card"><div class="bal">৳<span id="bal">0</span></div><button style="background:#1e40af" onclick="go('earn')">💰 আয় করুন</button></div><div class="card"><b>Admin Message</b><br>ProtidinerKajBD<br><br><b>অফিশিয়াল চ্যানেল</b><br>ProtidinerKajBD</div></div>
<div id="t-earn" class="tab"><div class="card"><h3>প্রতি Ads এ ৳<span id="adR">1</span></h3><div class="bal">৳1</div><button class="ad" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button></div>
<div class="card"><b>YouTube ভিডিও ৳25</b><button style="background:#065f46" onclick="window.open('https://youtube.com/@ProtidinerKajBD','_blank')">শুরু করুন</button></div>
<div class="card"><b>Join Telegram ৳10</b><button class="ad" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">Join</button></div>
<div class="card"><b>👥 Refer ৳<span id="refR">50</span></b><p id="refLink" style="font-size:12px;word-break:break-all"></p><button style="background:#10b981" onclick="copyRef()">Copy Link</button></div></div>
<div id="t-support" class="tab"><div class="card"><p onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">Admin Message - ProtidinerKajBD →</p><hr><p onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">অফিশিয়াল চ্যানেল - ProtidinerKajBD →</p><hr><button style="background:#dc2626">কিভাবে কাজ করবেন? →</button></div></div>
<div id="t-withdraw" class="tab"><div class="card"><div class="bal">৳<span class="bal2">0</span></div><input id="num" placeholder="bKash/Nagad Number" style="width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:10px"><input id="amt" type="number" placeholder="Amount" style="width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:10px"><button class="ad" onclick="withdraw()">উইথড্র</button><p>Min: ৳<span id="minW">1000</span></p></div></div>
<div class="btm"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div>
<script>
const tg=Telegram.WebApp; const p=new URLSearchParams(location.search); let uid=p.get('id')||tg.initDataUnsafe?.user?.id||"8807178385"; let ref=p.get('ref');
document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied!');}
function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{let b=d.user.balance; document.getElementById('bal').innerText=b.toFixed(0); document.getElementById('bTop').innerText=b.toFixed(0); document.querySelectorAll('.bal2').forEach(e=>e.innerText=b.toFixed(0)); document.getElementById('adR').innerText=d.settings.ad_reward; document.getElementById('refR').innerText=d.settings.ref_bonus; document.getElementById('minW').innerText=d.settings.min_withdraw;});}
function watchAd(){show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(()=>{alert('✅ ৳ যোগ হয়েছে'); load();});}).catch(()=>{show_11764581('pop').then(()=>{fetch(`/api/reward?id=${uid}`).then(()=>{alert('✅ ৳ যোগ হয়েছে'); load();});}).catch(()=>alert('Ads not ready'));});}
function withdraw(){let n=document.getElementById('num').value; let a=document.getElementById('amt').value; if(!n||!a) return alert('Number & Amount দিন'); fetch(`/api/withdraw?id=${uid}&number=${n}&amount=${a}`,{method:'POST'}).then(r=>r.json()).then(d=>{alert(d.msg); load();});}
function go(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on')); document.getElementById('t-'+t).classList.add('on'); document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on')); document.getElementById('b-'+t).classList.add('on');}
if(ref && ref!=uid){fetch(`/api/refer?new_id=${uid}&ref_id=${ref}`,{method:'POST'});}
load(); tg.ready(); tg.expand();
show_11764581({type:'inApp',inAppSettings:{frequency:2,capping:0.1,interval:30,timeout:5,everyPage:false}});
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Super Admin</title>
<style>body{font-family:Arial;background:#0f172a;color:#fff;margin:0;padding:10px}.nav{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.nav button{padding:10px 14px;border:none;border-radius:8px;background:#1e293b;color:#fff;cursor:pointer}.nav button.on{background:#1e40af} table{width:100%;background:#1e293b;border-collapse:collapse;margin-top:10px} th,td{padding:8px;border:1px solid #334155;font-size:13px;text-align:center} th{background:#1e40af} input{padding:6px;border-radius:6px;border:none}.g{background:#10b981;color:#fff;padding:6px 10px;border:none;border-radius:6px}.r{background:#ef4444;color:#fff;padding:6px 10px;border:none;border-radius:6px}.b{background:#3b82f6;color:#fff;padding:6px 10px;border:none;border-radius:6px}.card{background:#1e293b;padding:14px;border-radius:12px;margin:10px 0}.tab{display:none}.tab.on{display:block}</style>
</head><body>
<h2>👑 SUPER ADMIN - 8807178385</h2><p>Bot: @ProtidinerKaj_BD_Bot | Monetag Zone 11764581 Active ✅</p>
<div class="nav"><button onclick="show('dash')" id="n-dash" class="on">Dashboard</button><button onclick="show('users')" id="n-users">Users</button><button onclick="show('ref')" id="n-ref">Referral</button><button onclick="show('wd')" id="n-wd">Withdraw</button><button onclick="show('set')" id="n-set">Settings</button></div>
<div id="t-dash" class="tab on"><div class="card"><p>Total Users: <b id="tu">0</b> | Total Balance: ৳<b id="tb">0</b> | Total Ads: <b id="ta">0</b> | Refer: <b id="tr">0</b> | Pending WD: <b id="pw">0</b></p></div></div>
<div id="t-users" class="tab"><input id="search" placeholder="Search ID" onkeyup="loadUsers()"><table><thead><tr><th>ID</th><th>Bal</th><th>Ads</th><th>Ref By</th><th>Refs</th><th>Action</th></tr></thead><tbody id="users"></tbody></table></div>
<div id="t-ref" class="tab"><table><thead><tr><th>User</th><th>Referred By</th><th>Refer List</th></tr></thead><tbody id="reft"></tbody></table></div>
<div id="t-wd" class="tab"><table><thead><tr><th>User</th><th>Number</th><th>Amt</th><th>Date</th><th>Action</th></tr></thead><tbody id="wdt"></tbody></table></div>
<div id="t-set" class="tab"><div class="card"><p>Min Withdraw: <input id="s_min" type="number"> Ad Reward: <input id="s_ad" type="number"> Ref Bonus: <input id="s_ref" type="number"> FB Reward: <input id="s_fb" type="number"></p><p>FB Link: <input id="s_fbl" style="width:300px"> Channel: <input id="s_ch" style="width:300px"></p><button class="g" onclick="saveSet()">Save All</button></div></div>
<script>
function show(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('on'));document.getElementById('n-'+t).classList.add('on'); if(t=='users') loadUsers(); if(t=='ref') loadRef(); if(t=='wd') loadWD(); if(t=='dash') loadDash(); if(t=='set') loadSet();}
function loadDash(){fetch('/api/admin_stats?admin=8807178385').then(r=>r.json()).then(d=>{document.getElementById('tu').innerText=d.total_users; document.getElementById('tb').innerText=d.total_balance; document.getElementById('ta').innerText=d.total_ads; document.getElementById('tr').innerText=d.total_ref; document.getElementById('pw').innerText=d.pending_wd;});}
function loadUsers(){let s=document.getElementById('search').value.toLowerCase(); fetch('/api/all_users').then(r=>r.json()).then(data=>{let h='';for(let id in data){if(s &&!id.includes(s)) continue; let u=data[id]; h+=`<tr><td>${id}</td><td>৳${u.balance}</td><td>${u.ads_watched||0}</td><td>${u.referred_by||'-'}</td><td>${(u.referrals||[]).length}</td><td><input id="b_${id}" value="${u.balance}" style="width:50px"><button class="b" onclick="upd('${id}')">Upd</button> <button class="g" onclick="add('${id}',10)">+10</button><button class="r" onclick="add('${id}',-10)">-10</button></td></tr>`;}document.getElementById('users').innerHTML=h;});}
function loadRef(){fetch('/api/all_users').then(r=>r.json()).then(data=>{let h='';for(let id in data){let u=data[id]; h+=`<tr><td>${id}</td><td>${u.referred_by||'-'}</td><td>${(u.referrals||[]).join(', ')||'-'}</td></tr>`;}document.getElementById('reft').innerHTML=h;});}
function loadWD(){fetch('/api/wd_list?admin=8807178385').then(r=>r.json()).then(l=>{let h='';l.forEach((w,i)=>{h+=`<tr><td>${w.user_id}</td><td>${w.number}</td><td>৳${w.amount}</td><td>${w.date}</td><td><button class="g" onclick="apWD(${i})">Approve</button> <button class="r" onclick="rjWD(${i})">Reject</button></td></tr>`});document.getElementById('wdt').innerHTML=h;});}
function loadSet(){fetch('/api/get_settings').then(r=>r.json()).then(s=>{document.getElementById('s_min').value=s.min_withdraw; document.getElementById('s_ad').value=s.ad_reward; document.getElementById('s_ref').value=s.ref_bonus; document.getElementById('s_fb').value=s.fb_reward; document.getElementById('s_fbl').value=s.fb_link; document.getElementById('s_ch').value=s.channel;});}
function upd(id){let v=document.getElementById('b_'+id).value; fetch(`/api/admin_update?id=${id}&balance=${v}&admin=8807178385`).then(()=>loadUsers());}
function add(id,a){fetch(`/api/admin_add?id=${id}&amount=${a}&admin=8807178385`).then(()=>loadUsers());}
function apWD(i){fetch(`/api/wd_approve?index=${i}&admin=8807178385`).then(()=>loadWD());}
function rjWD(i){fetch(`/api/wd_reject?index=${i}&admin=8807178385`).then(()=>loadWD());}
function saveSet(){let d={min_withdraw:document.getElementById('s_min').value, ad_reward:document.getElementById('s_ad').value, ref_bonus:document.getElementById('s_ref').value, fb_reward:document.getElementById('s_fb').value, fb_link:document.getElementById('s_fbl').value, channel:document.getElementById('s_ch').value, admin:'8807178385'}; fetch('/api/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>alert('Saved!'));}
loadDash();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_panel():
    if str(request.args.get('id'))!=str(ADMIN_ID): return "Not Authorized", 403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id')
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    return jsonify({"user":db["users"][uid],"settings":db["settings"]})
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
@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    uid=request.args.get('id'); number=request.args.get('number'); amount=int(request.args.get('amount',0))
    if db["users"][uid]["balance"]<amount: return jsonify({"msg":"Balance কম"})
    if amount<int(db["settings"]["min_withdraw"]): return jsonify({"msg":f"Min {db['settings']['min_withdraw']} লাগবে"})
    db["users"][uid]["balance"]-=amount
    import datetime; db["withdraws"].append({"user_id":uid,"number":number,"amount":amount,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_db(db); return jsonify({"msg":"✅ Request গেছে"})
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
@app.route('/api/fb_request', methods=['POST'])
def fb_req():
    uid=request.args.get('id')
    if uid not in db.get("fb_requests",[]):
        if "fb_requests" not in db: db["fb_requests"]=[]
        db["fb_requests"].append(uid); save_db(db)
    return jsonify({"ok":True})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id)
    if uid not in db["users"]: db["users"][uid]={"balance":0,"ads_watched":0,"referrals":[],"referred_by":None}
    if context.args and context.args[0]!=uid:
        ref_id=context.args[0]
        if not db["users"][uid].get("referred_by") and ref_id in db["users"]:
            db["users"][uid]["referred_by"]=ref_id; db["users"][ref_id]["referrals"].append(uid); db["users"][ref_id]["balance"]+=int(db["settings"]["ref_bonus"])
    save_db(db)
    kb=[[InlineKeyboardButton("💰 Open Earning App", web_app={"url": f"https://am-bot-1-v77g.onrender.com/?id={uid}"})]]
    if str(uid)==str(ADMIN_ID): kb.append([InlineKeyboardButton("👑 Super Admin Panel", url=f"https://am-bot-1-v77g.onrender.com/admin?id={uid}")])
    await update.message.reply_text(f"Welcome ✅\nID: {uid}\nBalance: ৳{db['users'][uid]['balance']}\nRefer: https://t.me/ProtidinerKaj_BD_Bot?start={uid}", reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    try:
        application=Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.run_polling()
    except Exception as e:
        print(f"Bot error: {e}")

# For Render
def start_bot_thread():
    threading.Thread(target=run_bot, daemon=True).start()

start_bot_thread()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
