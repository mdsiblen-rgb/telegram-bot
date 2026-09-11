import os, json, threading
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
FB_LINK = "https://www.facebook.com/share/1AXw16vWRj/"
DB_FILE = "database.json"
MINI_APP_URL = "https://am-bot-1-v77g.onrender.com"

app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE): return {"users": {}, "fb_requests": []}
    try:
        with open(DB_FILE, 'r') as f: return json.load(f)
    except: return {"users": {}, "fb_requests": []}
def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=2)
db = load_db()

USER_HTML = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - Official</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='3485122' data-sdk='show_11764581'></script>
<style>body{margin:0;font-family:Arial;background:#eef2ff;text-align:center;padding-bottom:20px}.top{background:#1e40af;color:#fff;padding:15px;font-weight:bold}.card{background:#fff;margin:12px;padding:20px;border-radius:18px;box-shadow:0 2px 10px rgba(0,0,0,.05)}button{width:100%;padding:15px;border:none;border-radius:12px;color:#fff;font-weight:bold;margin:8px 0;font-size:16px}.ad{background:#1e40af}.fb{background:#1877F2}.bal{font-size:28px;color:#1e40af;font-weight:800}</style>
</head><body>
<div class="top">প্রতিদিনের কাজ BD - Official</div>
<p class="bal">৳<span id="bal">0.00</span></p>
<div class="card">
<button class="ad" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন - ৳1</button>
<button class="fb" onclick="taskFB()">👍 Facebook Follow - ৳15</button>
<p style="font-size:12px;color:#666;margin-top:10px">Admin ID: 8807178385 | Monetag 3485122 Active ✅</p>
<p style="font-size:12px">ID: <span id="uid"></span></p>
</div>
<script>
const tg=Telegram.WebApp; const p=new URLSearchParams(location.search); const uid=p.get('id')||tg.initDataUnsafe?.user?.id||"8807178385";
document.getElementById('uid').innerText=uid;
fetch(`/api/get_user?id=${uid}`).then(r=>r.json()).then(d=>{document.getElementById('bal').innerText=(d.balance||0).toFixed(2);});
function watchAd(){ show_11764581().then(()=>{fetch(`/api/reward?id=${uid}&amount=1`).then(()=>{alert('✅ ৳1 যোগ হয়েছে!'); location.reload();});}).catch(()=>{show_11764581('pop').then(()=>{fetch(`/api/reward?id=${uid}&amount=1`).then(()=>{alert('✅ ৳1 যোগ হয়েছে!'); location.reload();});}).catch(()=>alert('Ads not ready, 30s পর চেষ্টা করুন'));});}
function taskFB(){ window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank'); fetch(`/api/fb_request?id=${uid}`,{method:'POST'}).then(()=>alert('Admin এর কাছে Request গেছে, Approve করলে ৳15 পাবেন!')); }
show_11764581({type:'inApp',inAppSettings:{frequency:2,capping:0.1,interval:30,timeout:5,everyPage:false}});
tg.ready(); tg.expand();
</script>
</body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Super Admin</title>
<style>body{font-family:Arial;background:#0f172a;color:#fff;padding:10px} table{width:100%;background:#1e293b;border-collapse:collapse;margin-top:10px} th,td{padding:10px;border:1px solid #334155;text-align:center} th{background:#1e40af} input{padding:5px;width:70px;border-radius:5px;border:none} button{padding:6px 12px;border:none;border-radius:6px;cursor:pointer;font-weight:bold}.g{background:#10b981;color:#fff}.r{background:#ef4444;color:#fff}.b{background:#3b82f6;color:#fff}</style>
</head><body>
<h2>👑 SUPER ADMIN - 8807178385</h2><p>Bot: @ProtidinerKaj_BD_Bot | Monetag: 3485122 / Zone 11764581 ✅</p><p>FB: https://www.facebook.com/share/1AXw16vWRj/</p>
<h3>All Users (<span id="count">0</span>)</h3><table><tr><th>User ID</th><th>Balance</th><th>Change Balance</th><th>Action</th></tr><tbody id="users"></tbody></table>
<h3>Facebook Task Requests</h3><table><tr><th>User ID</th><th>Action</th></tr><tbody id="fb"></tbody></table>
<script>
function load(){fetch('/api/all_users').then(r=>r.json()).then(data=>{let h='';let c=0;for(let id in data){c++;h+=`<tr><td>${id}</td><td>৳${data[id].balance}</td><td><input id="b_${id}" value="${data[id].balance}"><button class="b" onclick="upd('${id}')">Update</button></td><td><button class="g" onclick="add('${id}',10)">+10</button> <button class="g" onclick="add('${id}',100)">+100</button> <button class="r" onclick="add('${id}',-10)">-10</button></td></tr>`;}document.getElementById('users').innerHTML=h;document.getElementById('count').innerText=c;});fetch('/api/fb_list').then(r=>r.json()).then(l=>{let h='';l.forEach(id=>{h+=`<tr><td>${id}</td><td><button class="g" onclick="ap('${id}')">Approve +15</button> <button class="r" onclick="rj('${id}')">Reject</button></td></tr>`});document.getElementById('fb').innerHTML=h;});}
function upd(id){let v=document.getElementById('b_'+id).value;fetch(`/api/admin_update?id=${id}&balance=${v}&admin=8807178385`).then(()=>load());}
function add(id,a){fetch(`/api/admin_add?id=${id}&amount=${a}&admin=8807178385`).then(()=>load());}
function ap(id){fetch(`/api/fb_approve?id=${id}&admin=8807178385`).then(()=>{alert('Approved');load();});}
function rj(id){fetch(`/api/fb_reject?id=${id}&admin=8807178385`).then(()=>load());}
load();setInterval(load,4000);
</script>
</body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_panel():
    if str(request.args.get('id'))!=str(ADMIN_ID): return "Not Authorized - Only 8807178385", 403
    return render_template_string(ADMIN_HTML)
@app.route('/api/get_user')
def get_user(): return jsonify(db["users"].get(request.args.get('id'), {"balance":0}))
@app.route('/api/all_users')
def all_users(): return jsonify(db["users"])
@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); amt=int(request.args.get('amount',1))
    if uid not in db["users"]: db["users"][uid]={"balance":0}
    db["users"][uid]["balance"]+=amt; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_update')
def admin_update():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); bal=int(request.args.get('balance'))
    if uid not in db["users"]: db["users"][uid]={"balance":0}
    db["users"][uid]["balance"]=bal; save_db(db); return jsonify({"ok":True})
@app.route('/api/admin_add')
def admin_add():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id'); amt=int(request.args.get('amount'))
    if uid not in db["users"]: db["users"][uid]={"balance":0}
    db["users"][uid]["balance"]+=amt; save_db(db); return jsonify({"ok":True})
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
    if uid not in db["users"]: db["users"][uid]={"balance":0}
    db["users"][uid]["balance"]+=15; save_db(db); return jsonify({"ok":True})
@app.route('/api/fb_reject')
def fb_reject():
    if str(request.args.get('admin'))!=str(ADMIN_ID): return "No",403
    uid=request.args.get('id')
    if uid in db["fb_requests"]: db["fb_requests"].remove(uid); save_db(db)
    return jsonify({"ok":True})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id)
    if uid not in db["users"]: db["users"][uid]={"balance":0}; save_db(db)
    kb=[[InlineKeyboardButton("💰 Open Earning App", web_app={"url": f"{MINI_APP_URL}/?id={uid}"})],[InlineKeyboardButton("👑 Admin Panel", url=f"{MINI_APP_URL}/admin?id={uid}")]]
    await update.message.reply_text(f"Welcome to Protidiner Kaj BD Official ✅\nYour ID: {uid}\nBalance: ৳{db['users'][uid]['balance']}\n\nEarn by Watching Ads!", reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    application=Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

def run_flask(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__=='__main__':
    threading.Thread(target=run_bot).start()
    run_flask()
