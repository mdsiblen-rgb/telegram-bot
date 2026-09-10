import threading, sqlite3, os, time, datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

BOT_TOKEN = "8851083480:AAGiekbCF2sS6aLejQGT-3T1eSo_JAJs5rk"
ADMIN_ID = "8807178385"
CHANNEL_LINK = "https://t.me/ProtidinerKajBD"
WEBAPP_URL = "https://am-bot-1-v77g.onrender.com"
AD_LINK = "https://omg10.com/4/11760259"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
app = FastAPI()

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER DEFAULT 0, ref_by TEXT, name TEXT, last_daily TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, amount INTEGER, number TEXT, status TEXT DEFAULT 'pending')''')
    conn.commit(); conn.close()
init_db()

def main_keyboard(uid):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("🚀 Open App", web_app=WebAppInfo(url=f"{WEBAPP_URL}/?id={uid}")))
    markup.add("💰 Balance", "👥 My Referrals")
    markup.add("🎁 Daily Bonus", "🔗 Refer Link")
    markup.add("🌐 Community Task", "🛠️ Admin Panel")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    conn = sqlite3.connect('database.db'); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (user_id, balance, ref_by, name) VALUES (?,?,?,?)", (user_id, 10, ref_id, name))
        if ref_id and ref_id!= user_id:
            c.execute("UPDATE users SET balance=balance+25 WHERE user_id=?", (ref_id,))
            try: bot.send_message(ref_id, f"🎉 {name} আপনার লিংকে জয়েন করেছে! +25 TK")
            except: pass
        conn.commit()
    conn.close()
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("🚀 Open App", web_app={"url": f"{WEBAPP_URL}/?id={user_id}"}))
    mk.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id, f"🎉 স্বাগতম {name}!\nID: `{user_id}`\n💰 10 TK বোনাস পেয়েছেন!", reply_markup=mk)
    bot.send_message(message.chat.id, "নিচের মেনু থেকে বেছে নিন:", reply_markup=main_keyboard(user_id))

@bot.message_handler(func=lambda m: True)
def all_handler(message):
    uid = str(message.from_user.id)
    text = message.text.lower()
    conn = sqlite3.connect('database.db'); c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (uid,)); r=c.fetchone(); bal=r[0] if r else 0
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?", (uid,)); rc=c.fetchone()[0]
    conn.close()

    if "balance" in text:
        bot.send_message(message.chat.id, f"💰 আপনার ব্যালেন্স: {bal} TK", reply_markup=main_keyboard(uid))
    elif "my referral" in text:
        bot.send_message(message.chat.id, f"👥 আপনি রেফার করেছেন: {rc} জন\n💰 প্রতি রেফারে 25 TK\n\nআপনার লিংক:\n`https://t.me/ProtidinerKaj_BD_Bot?start={uid}`", reply_markup=main_keyboard(uid))
    elif "daily" in text:
        conn = sqlite3.connect('database.db'); c = conn.cursor()
        c.execute("SELECT last_daily FROM users WHERE user_id=?", (uid,)); row=c.fetchone()
        today = datetime.date.today().isoformat()
        if row and row[0]==today:
            bot.send_message(message.chat.id, "❌ আজকের বোনাস নিয়েছেন! কাল আবার পাবেন।", reply_markup=main_keyboard(uid))
        else:
            c.execute("UPDATE users SET balance=balance+5, last_daily=? WHERE user_id=?", (today, uid)); conn.commit()
            bot.send_message(message.chat.id, "🎁 Daily Bonus: 5 TK পেয়েছেন!", reply_markup=main_keyboard(uid))
        conn.close()
    elif "refer link" in text:
        bot.send_message(message.chat.id, f"🔗 আপনার রেফার লিংক:\n`https://t.me/ProtidinerKaj_BD_Bot?start={uid}`", reply_markup=main_keyboard(uid))
    elif "community" in text:
        mk=InlineKeyboardMarkup(); mk.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, f"আমাদের চ্যানেলে জয়েন করুন:\n{CHANNEL_LINK}", reply_markup=mk)
    elif "admin" in text:
        if uid==ADMIN_ID:
            bot.send_message(message.chat.id, f"👑 Admin Panel:\n{WEBAPP_URL}/admin/{ADMIN_ID}", reply_markup=main_keyboard(uid))
        else:
            bot.send_message(message.chat.id, "❌ আপনি Admin না", reply_markup=main_keyboard(uid))
    elif "open app" in text:
        mk = InlineKeyboardMarkup()
        mk.add(InlineKeyboardButton("🚀 Open App", web_app={"url": f"{WEBAPP_URL}/?id={uid}"}))
        bot.send_message(message.chat.id, "🚀 এখানে ক্লিক করুন:", reply_markup=mk)

def run_bot():
    while True:
        try: bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception as e: print(e); time.sleep(5)
threading.Thread(target=run_bot, daemon=True).start()

def get_home_html(uid):
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
body{{margin:0; font-family:sans-serif; background:#f0f2f5;}}
.container{{max-width:420px; margin:auto; padding:15px;}}
.header{{background:linear-gradient(135deg,#6a11cb,#2575fc); color:white; padding:20px; border-radius:20px; text-align:center;}}
.card{{background:white; padding:15px; border-radius:15px; margin-top:15px; box-shadow:0 2px 8px rgba(0,0,0,0.1);}}
.btn{{width:100%; padding:14px; border:none; border-radius:12px; font-weight:bold; cursor:pointer; display:block; text-align:center; text-decoration:none;}}
.btn-blue{{background:#007bff; color:white;}}.btn-green{{background:#28a745; color:white;}}.btn-orange{{background:#ff9800; color:white;}}
.ad-box{{background:#fff3cd; border:2px dashed #ff9800; padding:12px; border-radius:10px; text-align:center;}}
.timer{{font-size:26px; font-weight:bold; color:#d32f2f;}}
@keyframes pop{{0%{{transform:scale(0.5)}}100%{{transform:scale(1)}}}}
</style></head>
<body>
<div class="container">
<div class="header"><h2>Protidin Kaj BD</h2><p id="uid_show">ID: {uid}</p><h3 id="bal">Loading...</h3><p id="refCount"></p></div>
<div class="card"><div class="ad-box"><p>🔥 বিজ্ঞাপন দেখে 10 TK</p><p id="adTimer" class="timer">15s</p><button id="adBtn" class="btn btn-orange" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন</button></div></div>
<div class="card"><a href="{CHANNEL_LINK}" target="_blank" class="btn btn-blue">Join Channel</a><button class="btn btn-green" style="margin-top:10px;" onclick="completeTask()">✅ Task +10 TK</button></div>
<div class="card">
<h3>👥 রেফার সিস্টেম</h3><p>প্রতি রেফারে 25 TK</p>
<p id="refLink" style="background:#e8f0fe; padding:10px; border-radius:8px; word-break:break-all; font-size:12px; border:1px dashed #007bff;">https://t.me/ProtidinerKaj_BD_Bot?start={uid}</p>
<button class="btn btn-blue" onclick="copyRef()">📋 রেফার লিংক কপি করুন</button>
<button class="btn btn-green" style="margin-top:10px;" onclick="goEarn()">💰 My Earnings & Withdraw</button>
</div>
</div>

<div id="welcomeModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:9999; justify-content:center; align-items:center;">
  <div style="background:white; padding:25px; border-radius:20px; text-align:center; max-width:300px; margin:20px; animation: pop 0.3s;">
    <div style="font-size:60px;">🎉</div>
    <h2 style="color:#6a11cb; margin:10px 0;">স্বাগতম!</h2>
    <p>Protidin Kaj BD তে আপনাকে স্বাগতম!</p>
    <h3 style="color:green; background:#e8f5e9; padding:12px; border-radius:10px; margin:15px 0;">💰 10 TK বোনাস পেয়েছেন!</h3>
    <button onclick="document.getElementById('welcomeModal').style.display='none'; localStorage.setItem('welcomed_'+userId, '1')" style="background:#6a11cb; color:white; padding:12px 25px; border:none; border-radius:10px; font-weight:bold; width:100%; margin-top:10px;">🚀 শুরু করুন</button>
  </div>
</div>

<script>
let userId="{uid}";
function getTgId(){{ try{{ if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user) return Telegram.WebApp.initDataUnsafe.user.id.toString(); }}catch(e){{}} return null; }}
let tgId=getTgId();
if(tgId){{ userId=tgId; document.getElementById('uid_show').innerText='ID: '+userId; document.getElementById('refLink').innerText='https://t.me/ProtidinerKaj_BD_Bot?start='+userId; }}
if("{uid}"=="guest" && tgId){{ history.replaceState(null,'','/?id='+tgId); }}

fetch('/api/balance?user_id='+userId).then(r=>r.json()).then(d=>{{
  document.getElementById('bal').innerText='Balance: '+d.balance+' TK';
  document.getElementById('refCount').innerText='রেফার: '+d.ref_count+' জন';
  if(d.is_new &&!localStorage.getItem('welcomed_'+userId)){{
    setTimeout(()=>{{ document.getElementById('welcomeModal').style.display='flex'; }}, 600);
  }}
}});

function completeTask(){{ fetch('/api/task?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}}); }}
function goEarn(){{ location.href='/earnings/'+userId; }}
function copyRef(){{ let t=document.getElementById('refLink').innerText; navigator.clipboard.writeText(t); alert('✅ কপি হয়েছে!\\n'+t); }}
let timerStarted=false;
function watchAd(){{
  if(timerStarted) return; timerStarted=true;
  let adUrl="{AD_LINK}";
  try{{ Telegram.WebApp.openLink(adUrl); }}catch(e){{ window.open(adUrl,'_blank'); }}
  let sec=15, btn=document.getElementById('adBtn'), t=document.getElementById('adTimer'); btn.disabled=true;
  let iv=setInterval(()=>{{ sec--; t.innerText=sec+'s'; btn.innerText='⏳ '+sec+'s'; if(sec<=0){{ clearInterval(iv); fetch('/api/ad?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}}); }} }},1000);
}}
</script></body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    uid = request.query_params.get("id", "guest")
    return HTMLResponse(get_home_html(uid))

@app.get("/api/balance")
def get_balance(user_id: str):
    if user_id=="guest":
        return {"balance":0,"ref_count":0,"is_new":False}
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    r=c.fetchone()
    is_new=False
    if not r:
        c.execute("INSERT INTO users (user_id, balance, ref_by, name) VALUES (?,?,?,?)", (user_id, 10, None, f"User{user_id}"))
        conn.commit(); bal=10; is_new=True
    else: bal=r[0]
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?", (user_id,)); refc=c.fetchone()[0]
    conn.close()
    return {"balance":bal,"ref_count":refc,"is_new":is_new}

@app.get("/api/task")
def task(user_id: str):
    if user_id=="guest": return "❌ বট থেকে ঢুকুন @ProtidinerKaj_BD_Bot"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?", (user_id,)); conn.commit(); conn.close()
    return "✅ 10 TK Added"

@app.get("/api/ad")
def ad_reward(user_id: str):
    if user_id=="guest": return "❌ বট থেকে ঢুকুন"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?", (user_id,)); conn.commit(); conn.close()
    return "🎉 10 TK পেয়েছেন!"

@app.get("/earnings/{user_id}", response_class=HTMLResponse)
def earnings(user_id: str):
    return HTMLResponse(f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>body{{text-align:center; padding:20px; font-family:sans-serif; background:#f0f2f5;}}.card{{background:white; padding:20px; border-radius:15px; max-width:400px; margin:auto; box-shadow:0 2px 10px rgba(0,0,0,0.1);}}</style></head>
    <body>
    <div id="loading" class="card">⏳ Loading...</div>
    <div id="main" class="card" style="display:none;"><h2 id="balt">Balance: 0 TK</h2><p id="idt">ID: {user_id}</p><p id="reft"></p><hr><h3>Withdraw</h3>
    <form action="/api/withdraw" method="get"><input type="hidden" id="uid_input" name="user_id" value="{user_id}">
    <select name="method" required><option value="">Select</option><option value="Bkash">Bkash</option><option value="Nagad">Nagad</option></select><br><br>
    <input name="number" placeholder="Number" required><br><br><input name="amount" type="number" placeholder="Min 100" required><br><br><button style="padding:12px 20px; background:green; color:white; border:none; border-radius:8px;">Withdraw</button></form><br><a id="back" href="/?id={user_id}">⬅ Back</a></div>
    <div id="guest_msg" class="card" style="display:none;"><h2>⚠️ বট থেকে ঢুকুন!</h2><p>এই পেজটি শুধু Telegram বটের ভিতরে কাজ করবে</p><p>👉 @ProtidinerKaj_BD_Bot এ যান</p><p>👉 তারপর 🚀 Open App চাপুন</p><br><a href="{CHANNEL_LINK}">Join Channel</a></div>
    <script>
    let userId="{user_id}";
    function getTgId(){{ try{{ if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user) return Telegram.WebApp.initDataUnsafe.user.id.toString(); }}catch(e){{}} return null; }}
    let tgId=getTgId(); if(tgId) userId=tgId;
    if(userId=="guest"){{
        setTimeout(()=>{{
            let id2=getTgId();
            if(id2) location.href='/earnings/'+id2;
            else {{ document.getElementById('loading').style.display='none'; document.getElementById('guest_msg').style.display='block'; }}
        }},1500);
    }} else {{
        document.getElementById('uid_input').value=userId; document.getElementById('idt').innerText='ID: '+userId; document.getElementById('back').href='/?id='+userId;
        fetch('/api/balance?user_id='+userId).then(r=>r.json()).then(d=>{{
            document.getElementById('balt').innerText='Balance: '+d.balance+' TK';
            document.getElementById('reft').innerText='রেফার: '+d.ref_count+' জন';
            document.getElementById('loading').style.display='none';
            document.getElementById('main').style.display='block';
        }}).catch(()=>{{ document.getElementById('loading').style.display='none'; document.getElementById('main').style.display='block'; }});
    }}
    </script></body></html>""")

@app.get("/api/withdraw")
def withdraw(user_id: str, number: str, amount: int, method: str="Bkash"):
    if user_id=="guest": return HTMLResponse("❌ Guest - বট থেকে ঢুকুন <a href='/'>Back</a>")
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT balance, name FROM users WHERE user_id=?", (user_id,)); row=c.fetchone()
    bal=row[0] if row else 0; name=row[1] if row else "User"
    if amount>bal: return HTMLResponse(f"❌ ব্যালেন্স কম {bal} TK <a href='/earnings/{user_id}'>Back</a>")
    if amount<100: return HTMLResponse(f"❌ Min 100 TK <a href='/earnings/{user_id}'>Back</a>")
    c.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (amount, user_id))
    c.execute("INSERT INTO withdraws (user_id,amount,number,status) VALUES (?,?,?,?)", (user_id,amount,f"{method}-{number}",'pending'))
    conn.commit(); conn.close()
    try:
        mk=InlineKeyboardMarkup(); mk.add(InlineKeyboardButton("Admin Panel", url=f"{WEBAPP_URL}/admin/{ADMIN_ID}"))
        bot.send_message(ADMIN_ID, f"💸 *Withdraw*\\n👤 {name}\\n🆔 `{user_id}`\\n💳 {method} {number}\\n💰 {amount} TK", reply_markup=mk)
    except: pass
    return HTMLResponse(f"✅ {amount} TK Request Done!<br><a href='/earnings/{user_id}'>Back</a>")

@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_page(admin_id: str):
    if admin_id!=ADMIN_ID: return HTMLResponse("<h1>Not Admin</h1>", status_code=403)
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM users"); tu=c.fetchone()[0]
    c.execute("SELECT SUM(balance) FROM users"); tb=c.fetchone()[0] or 0
    c.execute("SELECT * FROM withdraws ORDER BY id DESC"); w=c.fetchall()
    c.execute("SELECT * FROM users ORDER BY rowid DESC LIMIT 50"); users=c.fetchall()
    conn.close()
    html=f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'></head><body><h2>Admin Panel</h2><p>Total User: {tu} | Total Taka: {tb}</p><h3>Pending Withdraw</h3>"
    for r in w:
        if r[4]=='pending': html+=f"<div style='border:1px solid #ddd; padding:10px; margin:5px;'>User:{r[1]} | {r[2]} TK | {r[3]} <a href='/api/approve?id={r[0]}&admin={ADMIN_ID}'><button>Approve</button></a></div>"
    html+="<h3>Last 50 Users</h3><table border='1' style='width:100%; font-size:12px;'><tr><th>ID</th><th>Bal</th><th>Ref By</th></tr>"
    for u in users:
        html+=f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2] or 'Direct'}</td></tr>"
    html+="</table></body></html>"
    return HTMLResponse(html)

@app.get("/api/approve")
def approve(id: int, admin: str):
    if admin!=ADMIN_ID: return "No"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE withdraws SET status='approved' WHERE id=?", (id,)); conn.commit(); conn.close()
    return HTMLResponse(f"Approved! <a href='/admin/{ADMIN_ID}'>Back</a>")

# কালো স্ক্রিন আর Not Found ঠিক করার জন্য - Redirect না, সরাসরি Home
@app.get("/{full_path:path}", response_class=HTMLResponse)
def catch_all(full_path: str, request: Request):
    uid = request.query_params.get("id", "guest")
    return HTMLResponse(get_home_html(uid))

if __name__ == "__main__":
    import uvicorn
    port=int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
