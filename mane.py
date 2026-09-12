# PART 1/3 - FINAL FIXED BIG FILE - START HERE
import os
import json
import threading
import time
import datetime
import requests
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db.json"
SELF_URL = "https://telegram-bot-1-v77g.onrender.com"

app = Flask(name)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},
            "withdraws": [],
            "banned": [],
            "slider": [
                {"img":"https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800","link":"https://t.me/ProtidinerKajBD"},
                {"img":"https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800","link":"https://t.me/ProtidinerKajBD"},
                {"img":"https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800","link":"https://youtube.com/@ProtidinerKajBD"}
            ],
            "settings":{
                "app_name":"প্রতিদিনের কাজ BD",
                "ad_zone":"11764581",
                "ad_reward":1,
                "ad_limit":100,
                "min_withdraw":1000,
                "welcome_bonus":60,
                "daily_bonus":10,
                "ref_bonus":20,
                "payment_time":"প্রতিদিন রাত 8PM - 10PM",
                "payment_rules":"ভুল Number দিবেন না",
                "admin_msg_title":"অফিশিয়াল চ্যানেল",
                "admin_msg_desc":"Ads দেখুন Task করুন",
                "my_ad_title":"🔥 স্পেশাল অফার",
                "my_ad_desc":"এডমিন থেকে চেঞ্জ হবে",
                "support_title":"🎧 সাপোর্ট সেন্টার",
                "support_desc":"সমস্যা হলে যোগাযোগ করুন - এডমিন এটা লিখবে",
                "support_extra":"সঠিক তথ্য দিন"
            },
            "tasks":[
                {"title":"YouTube ভিডিও দেখুন","reward":25,"link":"https://youtube.com/@ProtidinerKajBD","btn":"শুরু করুন","color":"#065f46"},
                {"title":"Telegram Channel Join","reward":10,"link":"https://t.me/ProtidinerKajBD","btn":"Join","color":"#1e40af"},
                {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","btn":"Follow","color":"#1877F2"},
                {"title":"Company Task 1","reward":20,"link":"https://t.me/ProtidinerKajBD","btn":"Visit","color":"#7c3aed"},
                {"title":"Company Task 2","reward":20,"link":"https://t.me/ProtidinerKajBD","btn":"Visit","color":"#0f766e"},
                {"title":"Company Task 3","reward":20,"link":"https://t.me/ProtidinerKajBD","btn":"Visit","color":"#be123c"}
            ]
        }
    with open(DB_FILE,'r',encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f:
        json.dump(d,f,indent=2,ensure_ascii=False)

def is_admin(id):
    try:
        return int(id)==ADMIN_ID
    except:
        return False

def keep_alive():
    while True:
        try:
            time.sleep(240)
            requests.get(f"{SELF_URL}/health",timeout=5)
        except:
            pass

threading.Thread(target=keep_alive,daemon=True).start()

USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>App</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@500;700&display=swap" rel="stylesheet">
<style>
*{font-family:'Hind Siliguri';box-sizing:border-box;margin:0;padding:0}
body{max-width:430px;margin:0 auto;background:#eef2ff;padding-bottom:150px}
.top{background:#1e40af;color:#fff;padding:14px;display:flex;justify-content:space-between;position:sticky;top:0;z-index:9}
.card{background:#fff;margin:12px;border-radius:20px;padding:16px;box-shadow:0 4px 18px rgba(0,0,0,.06)}
.bal{font-size:50px;font-weight:900;text-align:center;color:#1e40af}
.btn{width:100%;background:#1e40af;color:#fff;padding:14px;border:none;border-radius:14px;font-weight:700}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#fff;display:flex;border-top:1px solid #ddd;padding:16px 0 20px;z-index:99}
.btm div{flex:1;text-align:center;color:#94a3b8;font-size:15px;font-weight:700}
.btm div.on{color:#1e40af;background:#e8edff;border-radius:16px;transform:scale(1.2)}
.prof{background:linear-gradient(135deg,#0f766e,#115e59);color:#fff;margin:12px;border-radius:22px;padding:18px;display:flex;gap:14px}
.gcard{background:#0f766e;color:#fff;margin:10px 12px;border-radius:16px;padding:14px;display:flex;justify-content:space-between}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px}
.scard{background:#fff;border-radius:16px;padding:14px}
</style></head><body>
<div class="top"><b id="appN">BD</b><b>৳<span id="tb">0</span></b></div>

<div id="t-home"><div class="card"><div class="bal">৳<span id="b">0</span></div><button class="btn" onclick="go('earn')">💰 আয় করুন</button></div><div class="card"><b id="myT"></b><div id="myD"></div></div><div class="card"><b id="adT"></b><div id="adD"></div></div></div>

<div id="t-earn" style="display:none">
<div class="card"><button class="btn" onclick="watchAd()">▶ বিজ্ঞাপন - ৳<span id="ar">1</span></button><div>Watched: <span id="w">0</span></div></div>
<div id="tasks"></div>
<div class="card" style="background:#1e40af;color:#fff"><b>🔗 রেফার লিংক - ৳<span id="rb">20</span></b><div id="rl" style="background:#fff;color:#000;padding:10px;border-radius:10px;margin-top:8px;word-break:break-all;font-size:12px"></div><button class="btn" style="background:#f59e0b;margin-top:8px" onclick="copyR()">📋 কপি</button><div>মোট রেফার: <span id="rc">0</span></div></div>
</div>

<div id="t-support" style="display:none"><div class="card"><h3 id="sT" style="text-align:center"></h3><div id="sD" style="text-align:center;margin:10px 0"></div><div id="sE" style="background:#fff7ed;padding:12px;border-radius:12px"></div></div></div>

<div id="t-withdraw" style="display:none"><div class="card"><input id="wn" placeholder="Number" style="width:100%;padding:12px;border-radius:12px;border:1px solid #ddd"><input id="wa" type="number" placeholder="Amount" style="width:100%;padding:12px;border-radius:12px;border:1px solid #ddd;margin-top:8px"><button class="btn" style="margin-top:10px" onclick="wd()">Withdraw</button></div></div>

<div id="t-profile" style="display:none">
<div class="prof"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:64px;height:64px;border-radius:50%;background:#fff"><div style="flex:1"><div id="pn" style="font-weight:900;font-size:18px"></div><div>ID:

<span id="pid"></span></div><div style="display:flex;gap:6px;margin-top:8px"><input id="en" placeholder="নতুন নাম" style="padding:8px;border-radius:10px;border:none;flex:1;color:#000"><button onclick="cn()" style="background:#f59e0b;border:none;padding:8px 12px;border-radius:10px;color:#fff;font-weight:700">Edit</button></div></div></div>
<div class="gcard"><span>💼 বর্তমান ব্যালেন্স</span><b>৳<span id="pb">0</span></b></div>
<div class="gcard"><span>✅ মোট সফল উইথড্র</span><b>৳<span id="ptw">0</span></b></div>
<div class="grid"><div class="scard"><small>আজকের আয়</small><b id="pt">৳0</b></div><div class="scard"><small>গতকালের আয়</small><b id="py">৳0</b></div><div class="scard"><small>মোট Ads</small><b id="pa">0</b></div><div class="scard"><small>মোট রেফার</small><b id="pr">0 জন</b></div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><span>🪪 ইউজার আইডি</span><b id="uid2"></b></div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><span>📊 মোট আয়</span><b id="ptot">৳0</b></div></div>
</div>

<div class="btm"><div id="b-home" class="on" onclick="go('home')">🏠<br>হোম</div><div id="b-earn" onclick="go('earn')">📦<br>আয়</div><div id="b-support" onclick="go('support')">🎧<br>সাপোর্ট</div><div id="b-withdraw" onclick="go('withdraw')">💳<br>উইথড্র</div><div id="b-profile" onclick="go('profile')">👤<br>প্রোফাইল</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')'8807178385';
function go(t){['home','earn','support','withdraw','profile'].forEach(x=>{document.getElementById('t-'+x).style.display=x==t?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==t)})}
function load(){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{document.getElementById('tb').innerText=d.user.balance;document.getElementById('b').innerText=d.user.balance;document.getElementById('pb').innerText=d.user.balance;document.getElementById('pid').innerText=uid;document.getElementById('uid2').innerText=uid;document.getElementById('pn').innerText=d.user.name;document.getElementById('w').innerText=d.user.ads_watched0;document.getElementById('pa').innerText=(d.user.ads_watched0)+' টি';document.getElementById('pt').innerText='৳'+(d.user.today_earn0);document.getElementById('py').innerText='৳'+(d.user.yesterday_earn0);document.getElementById('ptw').innerText=d.user.total_withdraw0;document.getElementById('pr').innerText=(d.user.refer_count0)+' জন';document.getElementById('rc').innerText=d.user.refer_count0;document.getElementById('ptot').innerText='৳'+(d.user.total_earn||0);document.getElementById('appN').innerText=d.settings.app_name;document.getElementById('myT').innerText=d.settings.my_ad_title;document.getElementById('myD').innerText=d.settings.my_ad_desc;document.getElementById('adT').innerText=d.settings.admin_msg_title;document.getElementById('adD').innerText=d.settings.admin_msg_desc;document.getElementById('sT').innerText=d.settings.support_title;document.getElementById('sD').innerText=d.settings.support_desc;document.getElementById('sE').innerText=d.settings.support_extra;document.getElementById('ar').innerText=d.settings.ad_reward;document.getElementById('rb').innerText=d.settings.ref_bonus;document.getElementById('rl').innerText='https://t.me/ProtidinerKajBD_bot?start='+uid;let bx=document.getElementById('tasks');bx.innerHTML='';d.tasks.forEach(t=>{bx.innerHTML+='<div class=card><div style=display:flex;justify-content:space-between><span>'+t.title+'</span><b>৳'+t.reward+'</b></div><button class=btn style=background:'+t.color+';margin-top:8px onclick=window.open('+t.link+')>'+t.btn+'</button></div>'})})}
function watchAd(){if(typeof show_11764581!=='function'){fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()});return}show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})})}
function wd(){fetch('/api/withdraw?id='+uid+'&num='+document.getElementById('wn').value+'&amt='+document.getElementById('wa').value).then(r=>r.json()).then(x=>alert(x.msg))}

function cn(){fetch('/api/update_name?id='+uid+'&name='+encodeURIComponent(document.getElementById('en').value)).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
function copyR(){navigator.clipboard.writeText(document.getElementById('rl').innerText).then(()=>alert('কপি'))}
load();
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin</title><style>body{max-width:500px;margin:0 auto;background:#eef6f3;padding:10px}.c{background:#fff;border-radius:16px;padding:14px;margin:10px}.i{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px;margin-top:4px}.b{width:100%;background:#0f766e;color:#fff;padding:14px;border-radius:12px;border:none;font-weight:900}</style></head><body>
<div style="background:#0f766e;color:#fff;padding:16px;border-radius:16px"><b>Admin Panel FINAL - Support Edit</b></div>
<div class="c"><b>🎧 সাপোর্ট এডিট</b><input id="st" class="i" placeholder="Support Title"><textarea id="sd" class="i" placeholder="Support Desc"></textarea><input id="se" class="i" placeholder="Extra"></div>
<div class="c"><b>📢 Home</b><input id="mt" class="i"><input id="md" class="i"><input id="at" class="i"><input id="ad" class="i"></div>
<div class="c"><b>🔗 6 Link</b><input id="l0" class="i"><input id="l1" class="i"><input id="l2" class="i"><input id="l3" class="i"><input id="l4" class="i"><input id="l5" class="i"></div>
<div class="c"><b>Setting</b><input id="an" class="i"><input id="ar" class="i"><input id="rb" class="i"></div>
<button class="b" onclick="save()">SAVE ALL</button>
<script>
let aid=new URLSearchParams(location.search).get('id');
function load(){fetch('/api/get_full?id='+aid).then(r=>r.json()).then(d=>{document.getElementById('st').value=d.settings.support_title;document.getElementById('sd').value=d.settings.support_desc;document.getElementById('se').value=d.settings.support_extra;document.getElementById('mt').value=d.settings.my_ad_title;document.getElementById('md').value=d.settings.my_ad_desc;document.getElementById('at').value=d.settings.admin_msg_title;document.getElementById('ad').value=d.settings.admin_msg_desc;for(let i=0;i<6;i++)document.getElementById('l'+i).value=d.tasks[i].link;document.getElementById('an').value=d.settings.app_name;document.getElementById('ar').value=d.settings.ad_reward;document.getElementById('rb').value=d.settings.ref_bonus})}
function save(){fetch('/api/admin/save_all?id='+aid,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({st:document.getElementById('st').value,sd:document.getElementById('sd').value,se:document.getElementById('se').value,mt:document.getElementById('mt').value,md:document.getElementById('md').value,at:document.getElementById('at').value,ad:document.getElementById('ad').value,l0:document.getElementById('l0').value,l1:document.getElementById('l1').value,l2:document.getElementById('l2').value,l3:document.getElementById('l3').value,l4:document.getElementById('l4').value,l5:document.getElementById('l5').value,an:document.getElementById('an').value,ar:document.getElementById('ar').value,rb:document.getElementById('rb').value})}).then(()=>alert('Saved'))}
load();
</script></body></html>
"""
@app.route('/')
def home():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin_page():
    if not is_admin(request.args.get('id')):
        return "Unauthorized", 403
    return render_template_string(ADMIN_HTML)

@app.route('/health')
def health():
    return "ok", 200

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id','8807178385')
    d = load_db()
    if uid not in d['users']:
        d['users'][uid] = {
            "balance": d['settings']['welcome_bonus'],
            "ads_watched": 0,
            "name": f"User {uid[-4:]}",
            "total_earn": d['settings']['welcome_bonus'],
            "today_earn": 0,
            "yesterday_earn": 0,
            "total_withdraw": 0,
            "refer_count": 0
        }
        save_db(d)
    return jsonify({
        "user": d['users'][uid],
        "settings": d['settings'],
        "tasks": d['tasks'],
        "slider": d['slider']
    })

@app.route('/api/reward')
def reward():
    uid = request.args.get('id')
    d = load_db()
    d['users'][uid]['balance'] += d['settings']['ad_reward']
    d['users'][uid]['ads_watched'] += 1
    d['users'][uid]['today_earn'] += d['settings']['ad_reward']
    d['users'][uid]['total_earn'] += d['settings']['ad_reward']
    save_db(d)
    return jsonify({"msg": f"৳{d['settings']['ad_reward']} যোগ হয়েছে"})

@app.route('/api/withdraw')
def wd_api():
    uid = request.args.get('id')
    amt = int(request.args.get('amt') or 0)
    d = load_db()
    if d['users'][uid]['balance'] < amt:
        return jsonify({"msg": "Balance কম আছে"})
    d['users'][uid]['balance'] -= amt
    d['withdraws'].append({"uid": uid, "amt": amt, "num": request.args.get('num'), "time": str(datetime.datetime.now())})
    save_db(d)
    return jsonify({"msg": "Withdraw Request চলে গেছে"})

@app.route('/api/update_name')
def up_name():
    uid = request.args.get('id')
    d = load_db()
    new_name = request.args.get('name','').strip()[:30]
    if new_name:
        d['users'][uid]['name'] = new_name
        save_db(d)
    return jsonify({"msg": "নাম চেঞ্জ হয়ে গেছে ✅"})

@app.route('/api/admin/save_all', methods=['POST'])
def save_all():
    if not is_admin(request.args.get('id')):
        return jsonify({"error": 1})
    j = request.json
    d = load_db()
    d['settings']['support_title'] = j['st']
    d['settings']['support_desc'] = j['sd']
    d['settings']['support_extra'] = j['se']
    d['settings']['my_ad_title'] = j['mt']
    d['settings']['my_ad_desc'] = j['md']
    d['settings']['admin_msg_title'] = j['at']
    d['settings']['admin_msg_desc'] = j['ad']
    d['settings']['app_name'] = j['an']
    d['settings']['ad_reward'] = int(j['ar'] or 1)
    d['settings']['ref_bonus'] = int(j['rb'] or 20)
    for i in range(6):
        d['tasks'][i]['link'] = j[f'l{i}']
    save_db(d)
    return jsonify({"ok": 1})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    d = load_db()
    ref = context.args[0] if context.args else None
    if uid not in d['users']:
        d['users'][uid] = {
            "balance": d['settings']['welcome_bonus'],
            "ads_watched": 0,
            "name": update.effective_user.first_name or f"User {uid[-4:]}",
            "total_earn": d['settings']['welcome_bonus'],
            "today_earn": 0,
            "yesterday_earn": 0,
            "total_withdraw": 0,
            "refer_count": 0
        }
        if ref and ref!= uid and ref in d['users']:
            d['users'][ref]['balance'] += d['settings']['ref_bonus']
            d['users'][ref]['refer_count'] = d['users'][ref].get('refer_count',0) + 1
        save_db(d)
    kb = [[InlineKeyboardButton("🚀 Open App", web_app={"url": f"{SELF_URL}/?id={uid}"})]]
    await update.message.reply_text(
        f"Welcome {update.effective_user.first_name} 🎉\nBalance: ৳{d['users'][uid]['balance']}",
        reply_markup=InlineKeyboardMarkup(kb)
    )

def run_bot():
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))


@app.route('/')
def home():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin_page():
    if not is_admin(request.args.get('id')):
        return "Unauthorized", 403
    return render_template_string(ADMIN_HTML)

@app.route('/health')
def health():
    return "ok", 200

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id','8807178385')
    d = load_db()
    if uid not in d['users']:
        d['users'][uid] = {
            "balance": d['settings']['welcome_bonus'],
            "ads_watched": 0,
            "name": f"User {uid[-4:]}",
            "total_earn": d['settings']['welcome_bonus'],
            "today_earn": 0,
            "yesterday_earn": 0,
            "total_withdraw": 0,
            "refer_count": 0
        }
        save_db(d)
    return jsonify({
        "user": d['users'][uid],
        "settings": d['settings'],
        "tasks": d['tasks'],
        "slider": d['slider']
    })

@app.route('/api/reward')
def reward():
    uid = request.args.get('id')
    d = load_db()
    d['users'][uid]['balance'] += d['settings']['ad_reward']
    d['users'][uid]['ads_watched'] += 1
    d['users'][uid]['today_earn'] += d['settings']['ad_reward']
    d['users'][uid]['total_earn'] += d['settings']['ad_reward']
    save_db(d)
    return jsonify({"msg": f"৳{d['settings']['ad_reward']} যোগ হয়েছে"})

@app.route('/api/withdraw')
def wd_api():
    uid = request.args.get('id')
    amt = int(request.args.get('amt') or 0)
    d = load_db()
    if d['users'][uid]['balance'] < amt:
        return jsonify({"msg": "Balance কম আছে"})
    d['users'][uid]['balance'] -= amt
    d['withdraws'].append({"uid": uid, "amt": amt, "num": request.args.get('num'), "time": str(datetime.datetime.now())})
    save_db(d)
    return jsonify({"msg": "Withdraw Request চলে গেছে"})

@app.route('/api/update_name')
def up_name():
    uid = request.args.get('id')
    d = load_db()
    new_name = request.args.get('name','').strip()[:30]
    if new_name:
        d['users'][uid]['name'] = new_name
        save_db(d)
    return jsonify({"msg": "নাম চেঞ্জ হয়ে গেছে ✅"})

@app.route('/api/admin/save_all', methods=['POST'])
def save_all():
    if not is_admin(request.args.get('id')):
        return jsonify({"error": 1})
    j = request.json
    d = load_db()
    d['settings']['support_title'] = j['st']
    d['settings']['support_desc'] = j['sd']
    d['settings']['support_extra'] = j['se']
    d['settings']['my_ad_title'] = j['mt']
    d['settings']['my_ad_desc'] = j['md']
    d['settings']['admin_msg_title'] = j['at']
    d['settings']['admin_msg_desc'] = j['ad']
    d['settings']['app_name'] = j['an']
    d['settings']['ad_reward'] = int(j['ar'] or 1)
    d['settings']['ref_bonus'] = int(j['rb'] or 20)
    for i in range(6):
        d['tasks'][i]['link'] = j[f'l{i}']
    save_db(d)
    return jsonify({"ok": 1})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    d = load_db()
    ref = context.args[0] if context.args else None
    if uid not in d['users']:
        d['users'][uid] = {
            "balance": d['settings']['welcome_bonus'],
            "ads_watched": 0,
            "name": update.effective_user.first_name or f"User {uid[-4:]}",
            "total_earn": d['settings']['welcome_bonus'],
            "today_earn": 0,
            "yesterday_earn": 0,
            "total_withdraw": 0,
            "refer_count": 0
        }
        if ref and ref!= uid and ref in d['users']:
            d['users'][ref]['balance'] += d['settings']['ref_bonus']
            d['users'][ref]['refer_count'] = d['users'][ref].get('refer_count',0) + 1
        save_db(d)
    kb = [[InlineKeyboardButton("🚀 Open App", web_app={"url": f"{SELF_URL}/?id={uid}"})]]
    await update.message.reply_text(
        f"Welcome {update.effective_user.first_name} 🎉\nBalance: ৳{d['users'][uid]['balance']}",
        reply_markup=InlineKeyboardMarkup(kb)
    )

def run_bot():
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))

app_bot.run_polling()

if name == 'main':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))















