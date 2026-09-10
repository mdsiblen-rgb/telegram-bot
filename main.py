import threading, sqlite3, os, time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

BOT_TOKEN = "8851083480:AAGiekbCF2sS6aLejQGT-3T1eSo_JAJs5rk"
ADMIN_ID = "8807178385"
CHANNEL_USERNAME = "@ProtidinerKajBD"
CHANNEL_LINK = "https://t.me/ProtidinerKajBD"
WEBAPP_URL = "https://am-bot-1-v77g.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)
app = FastAPI()

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER DEFAULT 0, ref_by TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, amount INTEGER, number TEXT, status TEXT DEFAULT 'pending')''')
    conn.commit()
    conn.close()
init_db()

def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Balance", "👥 Refer")
    markup.add("🚀 Open App", "📢 Channel")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (user_id, balance, ref_by) VALUES (?,?,?)", (user_id, 10, ref_id))
        if ref_id and ref_id!=user_id:
            c.execute("UPDATE users SET balance=balance+25 WHERE user_id=?", (ref_id,))
            try: bot.send_message(ref_id, f"🎉 {name} আপনার লিংকে জয়েন করেছে! 25 TK পেয়েছেন!")
            except: pass
        conn.commit()
        msg = f"🎉 স্বাগতম {name}!\n\nআপনি 10 TK ওয়েলকাম বোনাস পেয়েছেন!\n\nরেফার লিংক: {WEBAPP_URL}/?id={user_id}"
    else:
        msg = f"স্বাগতম {name}!\n\nআপনার লিংক: {WEBAPP_URL}/?id={user_id}"
    conn.close()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Open App - টাকা ইনকাম করুন", web_app={"url": f"{WEBAPP_URL}/?id={user_id}"}))
    markup.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id, msg, reply_markup=markup)
    bot.send_message(message.chat.id, "মেনু:", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: True)
def text_handler(message):
    user_id = str(message.from_user.id)
    if "Balance" in message.text:
        conn = sqlite3.connect('database.db'); c=conn.cursor(); c.execute("SELECT balance FROM users WHERE user_id=?",(user_id,)); bal=c.fetchone(); conn.close()
        bot.reply_to(message, f"💰 Balance: {bal[0] if bal else 0} TK")
    elif "Refer" in message.text:
        conn = sqlite3.connect('database.db'); c=conn.cursor(); c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?",(user_id,)); refs=c.fetchone()[0]; conn.close()
        bot.reply_to(message, f"👥 আপনার রেফার: {refs} জন\n\nলিংক: https://t.me/ProtidinerKaj_BD_Bot?start={user_id}\nওয়েব লিংক: {WEBAPP_URL}/?id={user_id}")
    elif "Open App" in message.text:
        bot.reply_to(message, f"এখানে ক্লিক করুন: {WEBAPP_URL}/?id={user_id}")
    elif "Channel" in message.text:
        bot.reply_to(message, f"Join করুন: {CHANNEL_LINK}")

def run_bot(): bot.infinity_polling()
threading.Thread(target=run_bot, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_id = request.query_params.get("id", "guest")
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{margin:0; font-family:sans-serif; background:#f0f2f5;}}
.container{{max-width:420px; margin:auto; padding:15px;}}
.header{{background:linear-gradient(135deg,#6a11cb,#2575fc); color:white; padding:20px; border-radius:20px; text-align:center;}}
.card{{background:white; padding:15px; border-radius:15px; margin-top:15px; box-shadow:0 2px 8px rgba(0,0,0,0.1);}}
.btn{{width:100%; padding:14px; border:none; border-radius:12px; font-weight:bold; font-size:16px; cursor:pointer;}}
.btn-blue{{background:#007bff; color:white;}}.btn-green{{background:#28a745; color:white;}}.btn-orange{{background:#ff9800; color:white;}}
.ad-box{{background:#fff3cd; border:1px dashed #ff9800; padding:12px; border-radius:10px; text-align:center;}}
.timer{{font-size:24px; font-weight:bold; color:#d32f2f;}}
</style></head>
<body>
<div class="container">
<div class="header"><h2>Protidin Kaj BD</h2><p>Welcome {user_id}</p><h3 id="bal">Loading...</h3></div>

<div class="card">
<h3>📢 Company Ads</h3>
<p>আমাদের স্পন্সর কোম্পানির বিজ্ঞাপন দেখুন</p>
<div class="ad-box">
<p>🔥 Daraz 11.11 Sale - 70% Discount!</p>
<p id="adTimer" class="timer">15s</p>
<button id="adBtn" class="btn btn-orange" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন (10 TK)</button>
</div>
</div>

<div class="card">
<button class="btn btn-blue" onclick="window.open('{CHANNEL_LINK}','_blank')">Step 1: Join Channel</button>
<button class="btn btn-green" style="margin-top:10px;" onclick="completeTask()">✅ Complete Task +10 TK</button>
</div>

<div class="card">
<h3>👥 রেফার সিস্টেম</h3>
<p>প্রতি রেফারে 25 TK</p>
<p style="background:#eee; padding:10px; border-radius:8px; word-break:break-all; font-size:12px;">{WEBAPP_URL}/?id={user_id}</p>
<p>বট লিংক: t.me/ProtidinerKaj_BD_Bot?start={user_id}</p>
<button class="btn btn-blue" onclick="location.href='/earnings/{user_id}'">💰 My Earnings & Withdraw</button>
</div>

<div class="card" style="text-align:center;">
<a href="/admin/{ADMIN_ID}">Admin Panel</a>
</div>
</div>

<script>
let userId = "{user_id}";
fetch('/api/balance?user_id='+userId).then(r=>r.json()).then(d=>{{document.getElementById('bal').innerText='Balance: '+d.balance+' TK';}});

function completeTask(){{
  fetch('/api/task?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}});
}}

let timerStarted=false;
function watchAd(){{
  if(timerStarted) return;
  timerStarted=true;
  let sec=15;
  let btn=document.getElementById('adBtn');
  let t=document.getElementById('adTimer');
  btn.disabled=true;
  let interval=setInterval(()=>{{
    sec--; t.innerText=sec+'s';
    if(sec<=0){{
      clearInterval(interval);
      fetch('/api/ad?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}});
    }}
  }},1000);
}}
</script>
</body></html>
"""

@app.get("/api/balance")
def get_balance(user_id: str):
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("SELECT balance FROM users WHERE user_id=?",(user_id,)); r=c.fetchone(); conn.close()
    return {"balance": r[0] if r else 0}

@app.get("/api/task")
def task(user_id: str):
    if user_id=="guest": return "বট থেকে Open App এ ক্লিক করে ঢুকুন!"
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, int(user_id))
        if member.status in ['left','kicked']: return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK}"
    except: return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK} - বটকে চ্যানেলে Admin করুন"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?",(user_id,)); conn.commit(); conn.close()
    return "✅ Task Completed! 10 TK Added"

@app.get("/api/ad")
def ad_reward(user_id: str):
    if user_id=="guest": return "ID লাগবে"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?",(user_id,)); conn.commit(); conn.close()
    return "🎉 বিজ্ঞাপন দেখা শেষ! 10 TK পেয়েছেন!"

@app.get("/earnings/{user_id}", response_class=HTMLResponse)
def earnings(user_id: str):
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("SELECT balance FROM users WHERE user_id=?",(user_id,)); r=c.fetchone(); bal=r[0] if r else 0; conn.close()
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{font-family:sans-serif; text-align:center; padding:20px;}} input{{padding:10px; margin:5px; width:80%;}} button{{padding:12px 20px; background:green; color:white; border:none; border-radius:10px;}}</style></head>
    <body><h2>💰 Balance: {bal} TK</h2><p>User: {user_id}</p>
    <form action="/api/withdraw" method="get"><input type="hidden" name="user_id" value="{user_id}"><input name="number" placeholder="Bkash/Nagad Number" required><br><input name="amount" type="number" placeholder="Amount Min 100" required><br><br><button>Withdraw Request</button></form><br><a href="/?id={user_id}">⬅ Back Home</a></body></html>
    """

@app.get("/api/withdraw")
def withdraw(user_id: str, number: str, amount: int):
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("INSERT INTO withdraws (user_id,amount,number) VALUES (?,?,?)",(user_id,amount,number)); conn.commit(); conn.close()
    try: bot.send_message(ADMIN_ID, f"💸 New Withdraw\nUser:{user_id}\nAmount:{amount}\nNumber:{number}")
    except: pass
    return HTMLResponse(f"Withdraw Request Sent! <a href='/earnings/{user_id}'>Back</a>")

@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_page(admin_id: str):
    if admin_id!=ADMIN_ID: return HTMLResponse("Not Admin", status_code=403)
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("SELECT * FROM withdraws WHERE status='pending'"); rows=c.fetchall(); conn.close()
    html="<h2>Admin Panel - Pending</h2>"
    for r in rows: html+=f"<p>ID:{r[0]} User:{r[1]} {r[2]}TK {r[3]} <a href='/api/approve?id={r[0]}&admin={ADMIN_ID}'><button>Approve</button></a></p>"
    if not rows: html+="<p>No pending</p>"
    return HTMLResponse(html)

@app.get("/api/approve")
def approve(id: int, admin: str):
    if admin!=ADMIN_ID: return "No"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE withdraws SET status='approved' WHERE id=?",(id,)); conn.commit(); conn.close()
    return HTMLResponse(f"Approved! <a href='/admin/{ADMIN_ID}'>Back</a>")

if __name__ == "__main__":
    import uvicorn
    port=int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
