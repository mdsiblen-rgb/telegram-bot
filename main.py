import os, json, threading, datetime, time, requests
from flask import Flask, request, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFoG66q4seW7HB1WLXgrMCxuqHbfmnYWJQ"
ADMIN_ID = 8807178385
DB_FILE = "db.json"
SELF_URL = "https://telegram-bot-1-v77g.onrender.com"
app = Flask(__name__)

# --- DB ---
def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {}, "withdraws": [], "banned": [], "refer_logs": [],
            "slider": [
                {"img": "https://img.freepik.com/free-vector/flat-design-earn-money-banner_23-2149439772.jpg", "link": "https://t.me/ProtidinerKajBD", "title": "🔥 প্রতিদিনের কাজ BD"},
                {"img": "https://img.freepik.com/free-vector/gradient-refer-friend-banner_23-2149373488.jpg", "link": "https://t.me/ProtidinerKajBD", "title": "💰 Refer করে ৳50 বোনাস"},
            ],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD", "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "banner_color": "#1e40af", "bg_color": "#eef2ff", "card_bg": "#ffffff",
                "balance_c1": "#1e3a8a", "balance_c2": "#3b82f6", "ad_btn": "#1e40af", "wd_btn": "#1e40af", "checkin_btn": "#f59e0b",
                "ad_zone": "11764581", "ad_reward": 1, "ad_daily_limit": 100,
                "ref_bonus": 50, "min_withdraw": 1000, "welcome_bonus": 30, "daily_bonus": 10,
                "home_notice": "🔥 আজ রাত 8টায় Giveaway! - Admin"
            },
            "tasks": [
                {"id": 1, "title": "YouTube ভিডিও দেখুন - 1 মিনিট", "reward": 25, "link": "https://youtube.com/@ProtidinerKajBD", "color": "#065f46", "btn": "শুরু করুন"},
                {"id": 2, "title": "Telegram Channel Join করুন", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join করুন"},
                {"id": 3, "title": "Facebook Page Follow করুন", "reward": 15, "link": "https://www.facebook.com/share/1AXw16vWRj/", "color": "#1877F2", "btn": "Follow করুন"}
            ]
        }
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w') as f: json.dump(f, d, indent=2)

# --- YOUR FULL HTML - bKash/Nagad Only - Same as before ---
USER_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>BD</title><script src="https://telegram.org/js/telegram-web-app.js"></script><script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script><style>body{max-width:430px;margin:0 auto;font-family:Arial;padding-bottom:90px}.top{color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;background:#1e40af;position:sticky;top:0}.bal-card{margin:12px;color:#fff;padding:18px;border-radius:20px;text-align:center;background:linear-gradient(135deg,#1e3a8a,#3b82f6)}.bal-big{font-size:48px;font-weight:900}.card{margin:12px;padding:14px;border-radius:18px;box-shadow:0 4px 12px rgba(0,0,0,.06);background:#fff}.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:bold;cursor:pointer;color:#fff;background:#1e40af;margin-top:8px}.tab{display:none}.tab.on{display:block}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;display:flex;justify-content:space-around;background:#fff;padding:10px 0;border-top:1px solid #ddd}.btm div{flex:1;text-align:center;font-size:12px;color:#888;cursor:pointer}.btm div.on{color:#1e40af;font-weight:bold}.slider{position:relative;width:calc(100% - 24px);margin:12px;height:165px;overflow:hidden;border-radius:18px}.slide{position:absolute;inset:0;opacity:0;transition:opacity.8s}.slide.active{opacity:1}.slide img{width:100%;height:100%;object-fit:cover}.slide-title{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.7));color:#fff;padding:25px 12px 10px;font-weight:bold}.dots{text-align:center}.dot{height:7px;width:7px;background:#bbb;border-radius:50%;display:inline-block;margin:0 3px}.dot.active{background:#1e40af}input{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;margin-top:8px;box-sizing:border-box}.meth{flex:1;background:#fff;border-radius:14px;padding:12px 6px;text-align:center;cursor:pointer;border:2px solid #ddd;position:relative}.meth.sel{border-width:3px!important}.meth.sel:after{content:'✓';position:absolute;top:4px;right:6px;background:#1e40af;color:#fff;width:18px;height:18px;border-radius:50%;font-size:12px;line-height:18px}.task-item{display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid #eee;border-radius:12px;margin:8px 0}.wd-info{background:#f8fafc;padding:10px;border-radius:10px;margin:10px 0;font-size:12px;text-align:center}</style></head><body><div class="top"><div style="display:flex;gap:8px;align-items:center"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:36px;height:36px;border-radius:50%;background:#fff"><span>প্রতিদিনের কাজ BD</span></div><span>৳<span id="bTop">0</span></span></div><div id="t-home" class="tab on"><div class="slider" id="sliderBox"></div><div class="dots" id="dotsBox"></div><div class="bal-card"><p>আপনার ব্যালেন্স</p><div class="bal-big">৳<span id="bal">0</span></div><div style="display:flex;gap:10px;margin-top:12px"><div style="flex:1;background:rgba(255,255,255,.2);padding:10px;border-radius:12px">আজ <b><span id="adWatched">0</span>/100</b></div><div style="flex:1;background:rgba(255,255,255,.2);padding:10px;border-radius:12px">Refer ৳<span id="refBonus">50</span></div></div><button class="btn" style="background:#fff;color:#1e40af;margin-top:14px" onclick="go('earn')">💰 এখনই আয় করুন</button></div><div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><div><b>🎁 Daily Check-in</b><br><small>৳<span id="dailyR">10</span></small></div><button class="btn" style="width:auto;padding:10px 18px;background:#f59e0b" onclick="dailyCheck()">বোনাস নিন</button></div></div><div class="card" id="homeNoticeBox" style="display:none;background:linear-gradient(135deg,#fef3c7,#fde68a);border:2px dashed #f59e0b"><h4 style="margin:0">📢 নোটিশ</h4><p id="homeNoticeText"></p></div></div><div id="t-earn" class="tab"><div class="card"><h3>📺 কোম্পানি বিজ্ঞাপন Zone 11764581</h3><div style="font-size:40px;text-align:center;font-weight:900;color:#1e40af">৳<span id="adR2">1</span></div><button class="btn" id="adBtn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button><p style="font-size:11px;color:green">✅ Telegram App থেকে Open করলে 100% Ad</p><p style="font-size:11px">Watched: <span id="adWatched2">0</span> / <span id="adLimit">100</span></p></div><div class="card"><h3>📋 অন্যান্য কাজ</h3><div id="tasksContainer"></div></div><div class="card"><p id="refLink" style="font-size:11px;background:#f1f5f9;padding:10px;border-radius:8px;word-break:break-all"></p><button class="btn" style="background:#10b981" onclick="navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('Copied')">Copy Link</button></div></div><div id="t-support" class="tab"><div class="card"><h3>🎧 সাপোর্ট</h3><button class="btn" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">📢 চ্যানেল</button><button class="btn" style="background:#FF0000" onclick="window.open('https://youtube.com/@ProtidinerKajBD','_blank')">▶️ YouTube</button><button class="btn" style="background:#1877F2" onclick="window.open('https://www.facebook.com/share/1AXw16vWRj/','_blank')">📘 Facebook</button></div></div><div id="t-withdraw" class="tab"><div class="card"><h3>💳 উইথড্র - বিকাশ নগদ ONLY</h3><div style="font-size:36px;text-align:center;font-weight:900">৳<span class="bal2">0</span></div><div class="wd-info">Min 1000 - আর <b id="needAmt">0</b> লাগবে</div></div><div class="card"><h4>💳 মেথড</h4><div style="display:flex;gap:12px"><div onclick="selectMethod('bKash')" id="m-bKash" class="meth sel" style="border-color:#e11d48"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bd/BKash_Logo.png" style="height:34px;display:block;margin:0 auto"><div style="font-weight:bold;color:#e11d48;margin-top:8px">bKash</div></div><div onclick="selectMethod('Nagad')" id="m-Nagad" class="meth" style="border-color:#f59e0b"><img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Nagad_Logo.png" style="height:34px;display:block;margin:0 auto"><div style="font-weight:bold;color:#e11d48;margin-top:8px">Nagad</div></div></div><input type="hidden" id="selectedMethod" value="bKash"><input id="wNum" placeholder="bKash Number"><input id="wAmt" type="number" placeholder="Min 1000"><button class="btn" onclick="doWithdraw()">উইথড্র করুন</button></div></div><div class="btm"><div onclick="go('home')" id="b-home" class="on">🏠<br>হোম</div><div onclick="go('earn')" id="b-earn">📦<br>আয়</div><div onclick="go('support')" id="b-support">🎧<br>সাপোর্ট</div><div onclick="go('withdraw')" id="b-withdraw">💳<br>উইথড্র</div></div><script>const tg=Telegram.WebApp;let qp=new URLSearchParams(location.search);let uid=qp.get('id')||tg.initDataUnsafe?.user?.id||"8807178385";let curSlide=0,slideInt,curMeth='bKash';function go(t){document.querySelectorAll('.tab').forEach(e=>e.classList.remove('on'));document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));document.getElementById('b-'+t).classList.add('on');}function selectMethod(m){curMeth=m;document.getElementById('selectedMethod').value=m;document.querySelectorAll('.meth').forEach(e=>e.classList.remove('sel'));document.getElementById('m-'+m).classList.add('sel');}function initSlider(imgs){let box=document.getElementById('sliderBox');let dots=document.getElementById('dotsBox');if(!imgs||!imgs.length)return;box.innerHTML='';dots.innerHTML='';imgs.forEach((it,i)=>{let d=document.createElement('div');d.className='slide'+(i==0?' active':'');d.innerHTML=`<img src="${it.img}"><div class="slide-title">${it.title||''}</div>`;d.onclick=()=>window.open(it.link,'_blank');box.appendChild(d);let dot=document.createElement('span');dot.className='dot'+(i==0?' active':'');dots.appendChild(dot);});if(slideInt)clearInterval(slideInt);slideInt=setInterval(()=>{let s=document.querySelectorAll('.slide');let ds=document.querySelectorAll('.dot');s[curSlide].classList.remove('active');ds[curSlide].classList.remove('active');curSlide=(curSlide+1)%s.length;s[curSlide].classList.add('active');ds[curSlide].classList.add('active');},3500);}function load(){fetch(`/api/get_full?id=${uid}`).then(r=>r.json()).then(d=>{document.getElementById('bal').innerText=d.user.balance;document.getElementById('bTop').innerText=d.user.balance;document.querySelectorAll('.bal2').forEach(e=>e.innerText=d.user.balance);document.getElementById('adWatched').innerText=d.user.ads_watched||0;document.getElementById('adWatched2').innerText=d.user.ads_watched||0;let s=d.settings;document.getElementById('adR2').innerText=s.ad_reward;document.getElementById('adLimit').innerText=s.ad_daily_limit;document.getElementById('refBonus').innerText=s.ref_bonus;document.getElementById('dailyR').innerText=s.daily_bonus;document.getElementById('refLink').innerText=`https://t.me/ProtidinerKaj_BD_Bot?start=${uid}`;if(s.home_notice){document.getElementById('homeNoticeBox').style.display='block';document.getElementById('homeNoticeText').innerText=s.home_notice;}let need=Math.max(0,s.min_withdraw-d.user.balance);document.getElementById('needAmt').innerText=need;initSlider(d.slider);let tc=document.getElementById('tasksContainer');tc.innerHTML='';d.tasks.forEach(t=>{tc.innerHTML+=`<div class="task-item"><div><b>${t.title}</b><br><small>৳${t.reward}</small></div><button class="btn" style="width:auto;background:${t.color};padding:8px 14px" onclick="window.open('${t.link}','_blank')">${t.btn}</button></div>`;});});}function watchAd(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{alert('✅ ৳'+d.reward);load();});});}else{fetch(`/api/reward?id=${uid}`).then(r=>r.json()).then(d=>{alert('Test ৳'+d.reward);load();});}}function doWithdraw(){let n=document.getElementById('wNum').value;let a=document.getElementById('wAmt').value;if(!n||!a)return alert('দাও');fetch(`/api/withdraw?id=${uid}&num=${n}&amt=${a}&method=${curMeth}`).then(r=>r.json()).then(d=>alert(d.msg));}function dailyCheck(){fetch(`/api/daily?id=${uid}`).then(r=>r.json()).then(d=>{alert(d.msg);load();});}load();</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(USER_HTML)
@app.route('/health')
def health(): return "ok", 200
@app.route('/ping')
def ping(): return "pong", 200

@app.route('/api/get_full')
def get_full():
    uid=request.args.get('id','8807178385'); d=load_db()
    if uid not in d['users']:
        d['users'][uid]={'balance':d['settings']['welcome_bonus'],'ads_watched':0,'ref_count':0,'last_daily':''}
        save_db(d)
    return jsonify({"user":d['users'][uid],"settings":d['settings'],"slider":d['slider'],"tasks":d['tasks'],"banned":False})
@app.route('/api/reward')
def reward():
    uid=request.args.get('id'); d=load_db(); d['users'][uid]['balance']+=d['settings']['ad_reward']; d['users'][uid]['ads_watched']+=1; save_db(d)
    return jsonify({"reward":d['settings']['ad_reward']})
@app.route('/api/daily')
def daily():
    uid=request.args.get('id'); d=load_db(); today=str(datetime.date.today())
    if d['users'][uid].get('last_daily')==today: return jsonify({"msg":"আজ নিয়েছো"})
    d['users'][uid]['balance']+=d['settings']['daily_bonus']; d['users'][uid]['last_daily']=today; save_db(d)
    return jsonify({"msg":f"✅ ৳{d['settings']['daily_bonus']}!"})
@app.route('/api/withdraw')
def wd():
    uid=request.args.get('id'); num=request.args.get('num'); amt=int(request.args.get('amt') or 0); method=request.args.get('method','bKash'); d=load_db()
    if d['users'][uid]['balance']<amt: return jsonify({"msg":"Balance কম"})
    if amt<d['settings']['min_withdraw']: return jsonify({"msg":f"Min {d['settings']['min_withdraw']}"})
    d['users'][uid]['balance']-=amt; d['withdraws'].append({"uid":uid,"num":num,"amt":amt,"method":method,"date":str(datetime.datetime.now())}); save_db(d)
    return jsonify({"msg":f"✅ {method} ৳{amt} OK!"})

# --- TELEGRAM WEBHOOK ---
application = Application.builder().token(BOT_TOKEN).build()
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.effective_user.id)
    kb=[[InlineKeyboardButton("🚀 Open App - Zone 11764581", web_app={"url": f"{SELF_URL}/?id={uid}"})]]
    await update.message.reply_text(f"Welcome {update.effective_user.first_name} ✅\n🎁 Bonus Ready!", reply_markup=InlineKeyboardMarkup(kb))
application.add_handler(CommandHandler("start", start_cmd))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        # run async handler in loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
    except Exception as e:
        print(f"Webhook error {e}")
    return "ok"

def set_webhook():
    time.sleep(5)
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={SELF_URL}/webhook"
        r = requests.get(url, timeout=10)
        print(f"Set webhook: {r.text}")
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        requests.get(url, timeout=10)
    except Exception as e:
        print(f"Webhook set failed {e}")

if __name__ == '__main__':
    threading.Thread(target=set_webhook, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
