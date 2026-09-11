import os, json, threading, time, datetime, requests
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db.json"
SELF_URL = "https://telegram-bot-1-v77g.onrender.com"
app = Flask(__name__)

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [],
            "slider": [
                {"img":"https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800","title":"To Do - প্রতিদিনের কাজ"},
                {"img":"https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800","title":"Doing - কাজ চলছে"},
                {"img":"https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800","title":"Done - সম্পন্ন"}
            ],
            "settings":{"app_name":"প্রতিদিনের কাজ BD","ad_zone":"11764581","ad_reward":1,"ad_daily_limit":100,"min_withdraw":1000,"welcome_bonus":60,"daily_bonus":10,"ad_timer":30},
            "tasks":[
                {"title":"YouTube ভিডিও দেখুন","reward":25,"link":"https://youtube.com/@ProtidinerKajBD","color":"#065f46","btn":"শুরু করুন","type":"youtube"},
                {"title":"Telegram Join","reward":10,"link":"https://t.me/ProtidinerKajBD","color":"#1e40af","btn":"Join","type":"telegram"},
                {"title":"Facebook Follow","reward":15,"link":"https://www.facebook.com/share/1AXw16vWRj/","color":"#1976d2","btn":"Follow","type":"facebook"}
            ]
        }
    with open(DB_FILE,'r') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE,'w') as f: json.dump(d,f,indent=2)

# ===== USER APP - তোমার ছবির মতো =====
USER_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600;700&display=swap" rel="stylesheet">
<style>
*{font-family:'Hind Siliguri',sans-serif;margin:0;padding:0;box-sizing:border-box}
body{max-width:430px;margin:0 auto;background:#eef2ff;padding-bottom:90px}
.top{background:#1e3a8a;color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.top-left{display:flex;align-items:center;gap:10px;font-weight:700}
.top-left img{width:38px;height:38px;border-radius:50%;background:#fff;border:2px solid #fff}
.card{background:#fff;margin:12px;border-radius:20px;padding:16px;box-shadow:0 4px 16px rgba(0,0,0,.05)}
.bal-big{font-size:54px;font-weight:900;text-align:center;color:#1e3a8a;line-height:1}
.btn-blue{width:100%;background:#1e3a8a;color:#fff;padding:14px;border:none;border-radius:14px;font-weight:700;font-size:16px;margin-top:12px}
.btn-green{background:#065f46}.btn-yellow{background:#f59e0b;color:#fff;padding:12px 20px;border:none;border-radius:12px;font-weight:700}
.slider{margin:12px;border-radius:22px;overflow:hidden;height:185px;position:relative;background:#000}
.slide{position:absolute;inset:0;opacity:0;transition:.8s}.slide.active{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover}
.dots{text-align:center;margin-top:6px}.dot{width:8px;height:8px;background:#cbd5e1;border-radius:50%;display:inline-block;margin:0 3px}.dot.active{background:#1e3a8a;width:20px}
.task-row{display:flex;justify-content:space-between;align-items:center;margin-top:10px}
.meth{display:inline-block;padding:10px 18px;border-radius:10px;color:#fff;font-weight:700;margin:4px}
.bKash{background:#e4006b}.Nagad{background:#f59e0b}.Rocket{background:#0ea5e9}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#fff;display:flex;padding:8px 0;border-top:1px solid #e2e8f0;z-index:100}
.btm div{flex:1;text-align:center;color:#94a3b8;font-size:11px;line-height:1.2}.btm div.on{color:#1e3a8a;font-weight:700}
input{width:100%;padding:13px;border:1px solid #e2e8f0;border-radius:12px;margin-top:10px}
</style></head><body>

<div class="top">
<div class="top-left"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"><span>প্রতিদিনের কাজ BD</span></div>
<div style="font-weight:900">৳<span id="topBal">60</span></div>
</div>

<!-- HOME -->
<div id="t-home">
<div class="slider" id="sliderBox">
<div class="slide active"><img src="https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800"></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=800"></div>
<div class="slide"><img src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800"></div>
</div>
<div class="dots" id="dotsBox"><span class="dot active"></span><span class="dot"></span><span class="dot"></span></div>

<div class="card">
<div class="bal-big">৳<span id="bal">60</span></div>
<button class="btn-blue" onclick="go('earn')">💰 আয় করুন</button>
</div>

<div class="card">
<div style="display:flex;justify-content:space-between;align-items:center">
<div><div style="font-size:18px">🎁 Daily Check-in</div><div style="color:#64748b;font-size:13px">প্রতিদিন বোনাস ৳10</div></div>
<button class="btn-yellow" onclick="dailyCheck()">আজকের বোনাস নিন</button>
</div>
</div>

<div class="card">
<div style="font-weight:700">Admin Message - ProtidinerKajBD</div>
<div style="font-weight:900;margin:5px 0;font-size:17px">অফিশিয়াল চ্যানেল - ProtidinerKajBD</div>
<div style="font-size:13px;color:#334155">Ads দেখুন, Task করুন, Refer করুন, Withdraw করুন</div>
</div>
</div>

<!-- EARN -->
<div id="t-earn" style="display:none">
<div class="card">
<div style="font-size:14px">প্রতি Ads ৳1 | Timer 30s</div>
<div class="bal-big" style="margin:10px 0">৳1</div>
<button class="btn-blue" id="adBtn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button>
<div style="font-size:12px;margin-top:8px;color:#64748b">Limit: 100 | Watched: <span id="watched">0</span></div>
</div>
<div id="tasksBox"></div>
</div>

<!-- WITHDRAW -->
<div id="t-withdraw" style="display:none">
<div class="card" style="text-align:center">
<div style="font-weight:700">💳 উইথড্র - ফিটফাট ✅</div>
<div class="bal-big" style="margin:10px 0">৳<span id="wdBal">1</span></div>
<input id="wNum" placeholder="bKash/Nagad Number">
<input id="wAmt" type="number" placeholder="Amount - Min 1000">
<button class="btn-blue" onclick="doWithdraw()">উইথড্র রিকোয়েস্ট করুন</button>
</div>
<div class="card">
<div style="font-weight:700">💳 পেমেন্ট মেথড</div>
<div style="margin-top:10px"><span class="meth bKash">bKash</span><span class="meth Nagad">Nagad</span><span class="meth Rocket">Rocket</span></div>
<div style="font-size:12px;margin-top:10px">⏰ পেমেন্ট টাইম: প্রতিদিন রাত 8PM - 10PM<br>📋 নিয়ম: 1. ভুল Number দিবেন না 2. Min ৳1000</div>
</div>
<div class="card">
<div style="font-weight:700">📜 আমার Withdraw History</div>
<div style="font-size:13px;color:#64748b;margin-top:8px">কোনো History নেই, প্রথম Withdraw করুন</div>
</div>
</div>

<!-- SUPPORT -->
<div id="t-support" style="display:none">
<div class="card"><button class="btn-blue" onclick="window.open('https://t.me/ProtidinerKajBD')">📢 Channel</button>
<button class="btn-blue" style="background:#FF0000;margin-top:10px" onclick="window.open('https://youtube.com/@ProtidinerKajBD')">▶️ YouTube</button>
<button class="btn-blue" style="background:#1877F2;margin-top:10px" onclick="window.open('https://www.facebook.com/share/1AXw16vWRj/')">📘 Facebook</button></div>
</div>

<div class="btm">
<div id="b-home" class="on" onclick="go('home')">🏠<br>হোম</div>
<div id="b-earn" onclick="go('earn')">📦<br>আয়</div>
<div id="b-support" onclick="go('support')">🎧<br>সাপোর্ট</div>
<div id="b-withdraw" onclick="go('withdraw')">💳<br>উইথড্র</div>
</div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
let cur=0;setInterval(()=>{let s=document.querySelectorAll('.slide');let d=document.querySelectorAll('.dot');s[cur].classList.remove('active');d[cur].classList.remove('active');cur=(cur+1)%s.length;s[cur].classList.add('active');d[cur].classList.add('active');},3000);
function go(t){['home','earn','withdraw','support'].forEach(x=>{document.getElementById('t-'+x).style.display=x==t?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==t);});}
function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{document.getElementById('topBal').innerText=d.user.balance;document.getElementById('bal').innerText=d.user.balance;document.getElementById('wdBal').innerText=d.user.balance;document.getElementById('watched').innerText=d.user.ads_watched||0;let box=document.getElementById('tasksBox');box.innerHTML='';d.tasks.forEach(t=>{box.innerHTML+=`<div class="card"><div style="font-size:15px">${t.title} ৳${t.reward} [${t.type}]</div><button class="btn-blue" style="background:${t.color};margin-top:10px" onclick="window.open('${t.link}','_blank')">${t.btn}</button></div>`});});}
function watchAd(){let b=document.getElementById('adBtn');if(typeof show_11764581!=='undefined'){b.innerText='Loading...';show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(x=>{alert(x.msg);b.innerText='▶ বিজ্ঞাপন দেখুন';load();})});}else{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(x=>{alert(x.msg);load();})}}
function doWithdraw(){let n=document.getElementById('wNum').value;let a=document.getElementById('wAmt').value;fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}`).then(r=>r.json()).then(x=>alert(x.msg))}
function dailyCheck(){fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
load();
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/health')
def health(): return "ok",200

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385'); d=load_db()
    if uid not in d['users']:
        d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'last_daily':''}
        save_db(d)
    return jsonify({"user":d['users'][uid],"settings":d['settings'],"slider":d['slider'],"tasks":d['tasks']})

@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); d=load_db()
    if d['users'][uid]['ads_watched']>=d['settings']['ad_daily_limit']: return jsonify({"msg":"Limit Done"})
    d['users'][uid]['balance']+=d['settings']['ad_reward']; d['users'][uid]['ads_watched']+=1; save_db(d)
    return jsonify({"msg":f"✅ ৳{d['settings']['ad_reward']} যোগ হয়েছে"})

@app.route('/api/daily')
def daily():
    uid=request.args.get('id'); d=load_db(); today=str(datetime.date.today())
    if d['users'][uid].get('last_daily')==today: return jsonify({"msg":"আজ নিয়েছো"})
    d['users'][uid]['balance']+=d['settings']['daily_bonus']; d['users'][uid]['last_daily']=today; save_db(d)
    return jsonify({"msg":"✅ ৳10 বোনাস!"})

@app.route('/api/withdraw')
def wd():
    uid=request.args.get('id'); amt=int(request.args.get('amt') or 0); d=load_db()
    if d['users'][uid]['balance']<amt: return jsonify({"msg":"Balance কম"})
    d['users'][uid]['balance']-=amt; d['withdraws'].append({"uid":uid,"amt":amt}); save_db(d)
    return jsonify({"msg":"✅ Request গেছে, Admin 8PM এ দিবে"})

# BOT
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id); d=load_db()
    if uid not in d['users']: d['users'][uid]={'balance':60,'ads_watched':0,'last_daily':''}; save_db(d)
    kb=[[InlineKeyboardButton("🚀 Open App", web_app={"url":f"{SELF_URL}/?id={uid}"})]]
    await update.message.reply_text(f"Welcome {update.effective_user.first_name} ✅", reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    app_bot=Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.run_polling()

if __name__=='__main__':
    threading.Thread(target=run_bot,daemon=True).start()
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
