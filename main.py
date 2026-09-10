import threading, sqlite3, os, time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# --- CONFIG ---
BOT_TOKEN = "8851083480:AAGiekbCF2sS6aLejQGT-3T1eSo_JAJs5rk"
ADMIN_ID = "8807178385"
CHANNEL_USERNAME = "@ProtidinerKajBD"
CHANNEL_LINK = "https://t.me/ProtidinerKajBD"
WEBAPP_URL = "https://am-bot-1-v77g.onrender.com"
AD_LINK = "https://omg10.com/4/11760259"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
app = FastAPI()

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER DEFAULT 0, ref_by TEXT, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, amount INTEGER, number TEXT, status TEXT DEFAULT 'pending')''')
    conn.commit()
    conn.close()
init_db()

# --- BOT KEYBOARD ---
def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Balance", "👥 Refer Link")
    markup.add("🚀 Open App", "📢 Community Task")
    markup.add("👑 Admin Panel")
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
        c.execute("INSERT INTO users (user_id, balance, ref_by, name) VALUES (?,?,?,?)", (user_id, 10, ref_id, name))
        if ref_id and ref_id!= user_id:
            c.execute("UPDATE users SET balance=balance+25 WHERE user_id=?", (ref_id,))
            try:
                bot.send_message(ref_id, f"🎉 *{name}* আপনার লিংকে জয়েন করেছে! 25 TK বোনাস!")
            except:
                pass
        conn.commit()
    else:
        c.execute("UPDATE users SET name=? WHERE user_id=?", (name, user_id))
        conn.commit()
    conn.close()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Open App - ইনকাম শুরু করুন", web_app={"url": f"{WEBAPP_URL}/?id={user_id}"}))
    markup.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id, f"🎉 স্বাগতম {name}!\n\n🆔 ID: `{user_id}`\n💰 10 TK ওয়েলকাম বোনাস!\n\n👇 App ওপেন করে কাজ শুরু করুন:", reply_markup=markup)
    bot.send_message(message.chat.id, "👇 মেনু থেকে সিলেক্ট করুন:", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: True)
def all_handler(message):
    text = message.text.lower()
    uid = str(message.from_user.id)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (uid,))
    r = c.fetchone()
    bal = r[0] if r else 0
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?", (uid,))
    rc = c.fetchone()[0]
    conn.close()

    if "balance" in text:
        bot.reply_to(message, f"💰 আপনার ব্যালেন্স: *{bal} TK*")
    elif "refer" in text:
        bot.reply_to(message, f"👥 আপনি রেফার করেছেন: *{rc} জন*\n💰 প্রতি রেফারে 25 TK\n\nআপনার রেফার লিংক:\n`https://t.me/ProtidinerKaj_BD_Bot?start={uid}`\n\nWeb লিংক:\n`{WEBAPP_URL}/?id={uid}`")
    elif "open" in text:
        mk = InlineKeyboardMarkup()
        mk.add(InlineKeyboardButton("🚀 Open App", web_app={"url": f"{WEBAPP_URL}/?id={uid}"}))
        bot.send_message(message.chat.id, f"এখানে ক্লিক করুন: {WEBAPP_URL}/?id={uid}", reply_markup=mk)
    elif "community" in text or "task" in text or "channel" in text:
        mk = InlineKeyboardMarkup()
        mk.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, f"Step 1: প্রথমে চ্যানেলে জয়েন করুন\n{CHANNEL_LINK}\n\nতারপর App এ গিয়ে Task Complete করুন", reply_markup=mk)
    elif "admin" in text:
        if uid == ADMIN_ID:
            bot.reply_to(message, f"👑 Admin Panel:\n{WEBAPP_URL}/admin/{ADMIN_ID}")
        else:
            bot.reply_to(message, "❌ আপনি Admin না")

def run_bot():
    while True:
        try:
            print("Bot polling started...")
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Bot error: {e}, restarting in 5 sec...")
            time.sleep(5)

threading.Thread(target=run_bot, daemon=True).start()

# --- WEB APP ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_id = request.query_params.get("id", "guest")
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
body{{margin:0; font-family:sans-serif; background:#f0f2f5;}}
.container{{max-width:420px; margin:auto; padding:15px;}}
.header{{background:linear-gradient(135deg,#6a11cb,#2575fc); color:white; padding:20px; border-radius:20px; text-align:center;}}
.card{{background:white; padding:15px; border-radius:15px; margin-top:15px; box-shadow:0 2px 8px rgba(0,0,0,0.1);}}
.btn{{width:100%; padding:14px; border:none; border-radius:12px; font-weight:bold; font-size:16px; cursor:pointer; display:block; text-decoration:none; text-align:center;}}
.btn-blue{{background:#007bff; color:white;}}.btn-green{{background:#28a745; color:white;}}.btn-orange{{background:#ff9800; color:white;}}
.ad-box{{background:#fff3cd; border:2px dashed #ff9800; padding:12px; border-radius:10px; text-align:center;}}
.timer{{font-size:26px; font-weight:bold; color:#d32f2f;}}
</style></head>
<body>
<div class="container">
<div class="header"><h2>Protidin Kaj BD</h2><p id="uid_show">ID: {user_id}</p><h3 id="bal">Loading...</h3><p id="refCount"></p></div>
<div class="card"><h3>📢 Company Sponsored Ad</h3><div class="ad-box"><p>🔥 বিজ্ঞাপন দেখে 10 TK ইনকাম করুন!</p><p id="adTimer" class="timer">15s</p><button id="adBtn" class="btn btn-orange" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন</button></div></div>
<div class="card"><a href="{CHANNEL_LINK}" target="_blank" class="btn btn-blue">Step 1: Join Channel</a><button class="btn btn-green" style="margin-top:10px;" onclick="completeTask()">✅ Complete Task +10 TK</button></div>
<div class="card"><h3>👥 রেফার সিস্টেম</h3><p>প্রতি রেফারে 25 TK</p><button class="btn btn-blue" onclick="goEarn()">💰 My Earnings & Withdraw</button></div>
<div class="card" style="text-align:center;"><a href="/admin/{ADMIN_ID}">👑 Admin Panel</a></div>
</div>
<script>
let userId = "{user_id}";
function getTgId(){{ try{{ if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user){{ return Telegram.WebApp.initDataUnsafe.user.id.toString(); }} }}catch(e){{}} return null; }}
let tgId = getTgId();
if(tgId){{ userId = tgId; document.getElementById('uid_show').innerText = 'ID: ' + userId; }}
if("{user_id}"=="guest" && tgId){{ history.replaceState(null,'','/?id='+tgId); }}
fetch('/api/balance?user_id='+userId).then(r=>r.json()).then(d=>{{ document.getElementById('bal').innerText='Balance: '+d.balance+' TK'; document.getElementById('refCount').innerText='রেফার: '+d.ref_count+' জন'; }});
function completeTask(){{ fetch('/api/task?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}}); }}
function goEarn(){{ window.location.href='/earnings/'+userId; }}
let timerStarted=false;
function watchAd(){{
  if(timerStarted) return;
  let adUrl="{AD_LINK}";
  try{{ Telegram.WebApp.openLink(adUrl); }}catch(e){{ window.open(adUrl,'_blank'); }}
  timerStarted=true; let sec=15; let btn=document.getElementById('adBtn'); let t=document.getElementById('adTimer'); btn.disabled=true;
  let iv=setInterval(()=>{{ sec--; t.innerText=sec+'s'; btn.innerText='⏳ '+sec+'s অপেক্ষা করুন...'; if(sec<=0){{ clearInterval(iv); fetch('/api/ad?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}}); }} }},1000);
}}
</script></body></html>
"""

@app.get("/earnings/{user_id}", response_class=HTMLResponse)
def earnings(user_id: str):
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>body{{font-family:sans-serif; text-align:center; padding:20px; background:#f0f2f5;}}.card{{background:white; padding:20px; border-radius:15px; max-width:400px; margin:auto;}} select, input{{padding:12px; width:90%; margin:8px; border-radius:8px; border:1px solid #ccc;}} button{{padding:12px 25px; background:green; color:white; border:none; border-radius:10px; font-weight:bold;}}</style></head>
    <body>
    <div id="loading" class="card"><h3>⏳ লোড হচ্ছে...</h3><p>ID চেক করা হচ্ছে...</p></div>
    <div id="main" class="card" style="display:none;"><h2 id="balt">Balance: Loading</h2><p id="idt">ID: {user_id}</p><p id="reft"></p><hr><h3>Withdraw</h3>
    <form action="/api/withdraw" method="get"><input type="hidden" id="uid_input" name="user_id" value="{user_id}">
    <select name="method" required><option value="">পেমেন্ট সিলেক্ট করুন</option><option value="Bkash">Bkash</option><option value="Nagad">Nagad</option></select><br>
    <input name="number" placeholder="Bkash/Nagad Number" required><br>
    <input name="amount" type="number" placeholder="Min 100" min="100" required><br><br><button>Withdraw Request</button></form><br><a id="back" href="/?id={user_id}">⬅ Back Home</a></div>
    <script>
    let userId = "{user_id}";
    function getTgId(){{ try{{ if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user) return Telegram.WebApp.initDataUnsafe.user.id.toString(); }}catch(e){{}} return null; }}
    let tgId = getTgId();
    if(tgId){{ userId = tgId; }}
    if(userId=="guest"){{
        setTimeout(()=>{{ let id2 = getTgId(); if(id2){{ window.location.href='/earnings/'+id2; }} else {{ document.getElementById('loading').innerHTML = "<h2>⚠️ বট থেকে ঢুকুন!</h2><p>Telegram @ProtidinerKaj_BD_Bot থেকে <b>Open App</b> এ ক্লিক করুন</p>"; }} }}, 1200);
    }} else {{
        document.getElementById('uid_input').value = userId;
        document.getElementById('idt').innerText = 'ID: ' + userId;
        document.getElementById('back').href = '/?id=' + userId;
        fetch('/api/balance?user_id='+userId).then(r=>r.json()).then(d=>{{
            document.getElementById('balt').innerText='Balance: '+d.balance+' TK';
            document.getElementById('reft').innerText='রেফার: '+d.ref_count+' জন';
            document.getElementById('loading').style.display='none';
            document.getElementById('main').style.display='block';
        }});
    }}
    </script></body></html>
    """

@app.get("/api/balance")
def get_balance(user_id: str):
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?",(user_id,)); r=c.fetchone(); bal=r[0] if r else 0
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?",(user_id,)); refc=c.fetchone()[0]
    conn.close()
    return {"balance": bal, "ref_count": refc}

@app.get("/api/task")
def task(user_id: str):
    if user_id=="guest": return "⚠️ বট থেকে Open App দিয়ে ঢুকুন!"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?",(user_id,)); conn.commit(); conn.close()
    return "✅ Task Completed! 10 TK Added"

@app.get("/api/ad")
def ad_reward(user_id: str):
    if user_id=="guest": return "বট থেকে ঢুকুন"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?",(user_id,)); conn.commit(); conn.close()
    return "🎉 15s Done! 10 TK পেয়েছেন!"

@app.get("/api/withdraw")
def withdraw(user_id: str, number: str, amount: int, method: str = "Bkash"):
    if user_id=="guest": return HTMLResponse("❌ Guest দিয়ে Withdraw হবে না! বট থেকে ঢুকুন <a href='/'>Back</a>")
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT balance, name FROM users WHERE user_id=?",(user_id,)); row=c.fetchone()
    bal=row[0] if row else 0; name=row[1] if row and len(row)>1 and row[1] else "User"
    if amount>bal: return HTMLResponse(f"❌ ব্যালেন্স কম! আছে {bal} TK <a href='/earnings/{user_id}'>Back</a>")
    if amount<100: return HTMLResponse(f"❌ Min 100 TK <a href='/earnings/{user_id}'>Back</a>")
    c.execute("UPDATE users SET balance=balance-? WHERE user_id=?",(amount, user_id))
    c.execute("INSERT INTO withdraws (user_id,amount,number,status) VALUES (?,?,?,?)",(user_id,amount,f"{method}-{number}",'pending'))
    conn.commit(); conn.close()
    try:
        msg = f"💸 *New Withdraw Request!*\n\n👤 Name: {name}\n🆔 ID: `{user_id}`\n💳 Method: *{method}*\n🔢 Number: `{number}`\n💰 Amount: *{amount} TK*\n\n👉 Profile: tg://user?id={user_id}"
        mk=InlineKeyboardMarkup()
        mk.add(InlineKeyboardButton("✅ Approve - Admin Panel", url=f"{WEBAPP_URL}/admin/{ADMIN_ID}"))
        mk.add(InlineKeyboardButton(f"💬 {name} কে মেসেজ", url=f"tg://user?id={user_id}"))
        bot.send_message(ADMIN_ID, msg, reply_markup=mk)
    except Exception as e:
        print(e)
    return HTMLResponse(f"✅ {method} ({number}) এ {amount} TK Request পাঠানো হয়েছে!<br><br><a href='/earnings/{user_id}'>Back</a>")

@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_page(admin_id: str):
    if admin_id!=ADMIN_ID: return HTMLResponse("Not Admin", status_code=403)
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM users"); total_users=c.fetchone()[0]
    c.execute("SELECT SUM(balance) FROM users"); total_taka=c.fetchone()[0] or 0
    c.execute("SELECT * FROM users ORDER BY rowid DESC"); users=c.fetchall()
    c.execute("SELECT * FROM withdraws ORDER BY id DESC"); withdraws=c.fetchall()
    conn.close()
    html = f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{font-family:sans-serif; background:#f1f2f6; padding:10px;}}.box{{flex:1; background:white; padding:15px; border-radius:12px; text-align:center;}}.box h2{{margin:5px; color:#6a11cb;}} table{{width:100%; background:white; border-collapse:collapse; margin-top:15px; font-size:12px;}} th,td{{padding:8px; border-bottom:1px solid #eee;}} th{{background:#6a11cb; color:white;}}.card{{background:white; padding:12px; border-radius:10px; margin-top:10px;}}</style></head><body>
    <h2>👑 Admin Dashboard</h2><div style="display:flex; gap:10px;"><div class="box">ইউজার<h2>{total_users}</h2></div><div class="box">মোট টাকা<h2>{total_taka} TK</h2></div><div class="box">Withdraw<h2>{len(withdraws)}</h2></div></div><h3>💸 Pending Withdraw</h3>"""
    has=False
    for r in withdraws:
        if r[4]=='pending':
            has=True
            html+=f"<div class='card'>ID:{r[0]} | User:{r[1]}<br>{r[2]} TK - {r[3]}<br><a href='/api/approve?id={r[0]}&admin={ADMIN_ID}'><button style='background:green;color:white;padding:8px 15px;border:none;border-radius:8px;'>Approve</button></a> <a href='tg://user?id={r[1]}'><button>Message</button></a></div>"
    if not has: html+="<div class='card'>কোনো Pending নাই</div>"
    html+=f"<h3>👥 সকল ইউজার লিস্ট (ID সহ)</h3><table><tr><th>User ID</th><th>Name</th><th>Balance</th><th>Ref By</th><th>রেফার করেছে</th></tr>"
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    for u in users:
        uid=u[0]; bal=u[1]; ref_by=u[2] or "Direct"; name=u[3] if len(u)>3 else ""
        c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?",(uid,)); rc=c.fetchone()[0]
        html+=f"<tr><td><a href='tg://user?id={uid}'>{uid}</a></td><td>{name}</td><td>{bal}</td><td>{ref_by}</td><td>{rc} জন</td></tr>"
    conn.close()
    html+="</table></body></html>"
    return HTMLResponse(html)

@app.get("/api/approve")
def approve(id: int, admin: str):
    if admin!=ADMIN_ID: return "No"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE withdraws SET status='approved' WHERE id=?",(id,)); conn.commit(); conn.close()
    return HTMLResponse(f"Approved! <a href='/admin/{ADMIN_ID}'>Back</a>")

@app.get("/favicon.ico")
def favicon(): return HTMLResponse("", status_code=204)

@app.get("/{full_path:path}")
def catch_all(full_path: str, request: Request):
    if "admin" in full_path or "api" in full_path or "earnings" in full_path:
        return HTMLResponse("Not Found", status_code=404)
    uid = request.query_params.get("id", "guest")
    return RedirectResponse(f"/?id={uid}")

if __name__ == "__main__":
    import uvicorn
    port=int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
