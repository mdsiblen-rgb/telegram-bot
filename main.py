import threading, sqlite3, os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

BOT_TOKEN = "8851083480:AAGiekbCF2sS6aLejQGT-3T1eSo_JAJs5rk"
ADMIN_ID = "8807178385"
CHANNEL_USERNAME = "@ProtidinerKajBD"
CHANNEL_LINK = "https://t.me/ProtidinerKajBD"
WEBAPP_URL = "https://am-bot-1-v77g.onrender.com"
AD_LINK = "https://omg10.com/4/11760259"

bot = telebot.TeleBot(BOT_TOKEN)
app = FastAPI()

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER DEFAULT 0, ref_by TEXT, name TEXT)''')
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
        c.execute("INSERT INTO users (user_id, balance, ref_by, name) VALUES (?,?,?,?)", (user_id, 10, ref_id, name))
        if ref_id and ref_id!=user_id:
            c.execute("UPDATE users SET balance=balance+25 WHERE user_id=?", (ref_id,))
            try: bot.send_message(ref_id, f"🎉 {name} আপনার লিংকে জয়েন করেছে! 25 TK বোনাস পেয়েছেন!")
            except: pass
        conn.commit()
    else:
        c.execute("UPDATE users SET name=? WHERE user_id=?",(name, user_id))
        conn.commit()
    conn.close()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Open App - টাকা ইনকাম করুন", web_app={"url": f"{WEBAPP_URL}/?id={user_id}"}))
    markup.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id, f"🎉 স্বাগতম {name}!\n\nID: {user_id}\n10 TK বোনাস পেয়েছেন!\n\nলিংক: {WEBAPP_URL}/?id={user_id}\n\n1. Join: {CHANNEL_LINK}\n2. Website এ Task Complete করুন।", reply_markup=markup)
    bot.send_message(message.chat.id, "মেনু:", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text and ("Balance" in m.text or "My Referrals" in m.text or "Referrals" in m.text))
def text_handler(message):
    user_id = str(message.from_user.id)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?",(user_id,))
    bal_row = c.fetchone()
    bal = bal_row[0] if bal_row else 0
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?",(user_id,))
    refs = c.fetchone()[0]
    conn.close()
    if "Balance" in message.text:
        bot.reply_to(message, f"💰 আপনার ব্যালেন্স: {bal} TK")
    else:
        bot.reply_to(message, f"👥 আপনি রেফার করেছেন: {refs} জন\n💰 প্রতি রেফারে 25 TK\n\nআপনার লিংক:\nhttps://t.me/ProtidinerKaj_BD_Bot?start={user_id}")

def run_bot(): bot.infinity_polling()
threading.Thread(target=run_bot, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_id = request.query_params.get("id", "guest")
    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>body{{margin:0; font-family:sans-serif; background:#f0f2f5;}}.container{{max-width:420px; margin:auto; padding:15px;}}.header{{background:linear-gradient(135deg,#6a11cb,#2575fc); color:white; padding:20px; border-radius:20px; text-align:center;}}.card{{background:white; padding:15px; border-radius:15px; margin-top:15px; box-shadow:0 2px 8px rgba(0,0,0,0.1);}}.btn{{width:100%; padding:14px; border:none; border-radius:12px; font-weight:bold; font-size:16px; cursor:pointer;}}.btn-blue{{background:#007bff; color:white;}}.btn-green{{background:#28a745; color:white;}}.btn-orange{{background:#ff9800; color:white;}}.ad-box{{background:#fff3cd; border:2px dashed #ff9800; padding:12px; border-radius:10px; text-align:center;}}.timer{{font-size:26px; font-weight:bold; color:#d32f2f;}}</style>
</head><body><div class="container">
<div class="header"><h2>Protidin Kaj BD</h2><p>ID: {user_id}</p><h3 id="bal">Loading...</h3><p id="refCount"></p></div>
<div class="card"><h3>📢 Company Ad</h3><div class="ad-box"><p>🔥 বিজ্ঞাপন দেখে 10 TK ইনকাম!</p><p id="adTimer" class="timer">15s</p><button id="adBtn" class="btn btn-orange" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন</button></div></div>
<div class="card"><button class="btn btn-blue" onclick="openChannel()">Step 1: Join Channel</button><button class="btn btn-green" style="margin-top:10px;" onclick="completeTask()">✅ Complete Task +10 TK</button></div>
<div class="card"><h3>👥 রেফার</h3><p>প্রতি রেফারে 25 TK</p><button class="btn btn-blue" onclick="location.href='/earnings/{user_id}'">💰 My Earnings & Withdraw</button></div>
</div>
<script>
let userId = "{user_id}";
fetch('/api/balance?user_id='+userId).then(r=>r.json()).then(d=>{{
  document.getElementById('bal').innerText='Balance: '+d.balance+' TK';
  document.getElementById('refCount').innerText='রেফার: '+d.ref_count+' জন';
}});
function openChannel(){{ let url="{CHANNEL_LINK}"; try{{ if(Telegram && Telegram.WebApp) Telegram.WebApp.openLink(url); else window.open(url,'_blank'); }}catch(e){{window.open(url,'_blank');}} }}
function completeTask(){{ fetch('/api/task?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}}); }}
let timerStarted=false;
function watchAd(){{ if(timerStarted) return; let adUrl="{AD_LINK}"; try{{ if(window.Telegram && Telegram.WebApp) Telegram.WebApp.openLink(adUrl); else window.open(adUrl,'_blank'); }}catch(e){{window.open(adUrl,'_blank');}} timerStarted=true; let sec=15; let btn=document.getElementById('adBtn'); let t=document.getElementById('adTimer'); btn.disabled=true; let iv=setInterval(()=>{{sec--; t.innerText=sec+'s'; btn.innerText='⏳ '+sec+'s'; if(sec<=0){{clearInterval(iv); fetch('/api/ad?user_id='+userId).then(r=>r.text()).then(a=>{{alert(a); location.reload();}});}}}},1000); }}
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
    if user_id=="guest": return "বট থেকে Open App দিয়ে ঢুকুন"
    try:
        m=bot.get_chat_member(CHANNEL_USERNAME, int(user_id))
        if m.status in ['left','kicked']: return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK}"
    except: return f"চ্যানেলে জয়েন করুন ও বটকে Admin করুন"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?",(user_id,)); conn.commit(); conn.close()
    return "✅ 10 TK Added"

@app.get("/api/ad")
def ad_reward(user_id: str):
    if user_id=="guest": return "বট থেকে ঢুকুন"
    conn=sqlite3.connect('database.db'); c=conn.cursor(); c.execute("UPDATE users SET balance=balance+10 WHERE user_id=?",(user_id,)); conn.commit(); conn.close()
    return "🎉 15s Done! 10 TK পেয়েছেন!"

@app.get("/earnings/{user_id}", response_class=HTMLResponse)
def earnings(user_id: str):
    if user_id=="guest":
        return HTMLResponse("<h2 style='text-align:center;margin-top:50px;'>⚠️ বট থেকে ঢুকুন!<br>Telegram @ProtidinerKaj_BD_Bot থেকে Open App এ ক্লিক করুন</h2>")
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?",(user_id,)); r=c.fetchone(); bal=r[0] if r else 0
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?",(user_id,)); refc=c.fetchone()[0]
    conn.close()
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{font-family:sans-serif; text-align:center; padding:20px; background:#f0f2f5;}}.card{{background:white; padding:20px; border-radius:15px; max-width:400px; margin:auto;}} select, input{{padding:12px; width:90%; margin:8px; border-radius:8px; border:1px solid #ccc;}} button{{padding:12px 25px; background:green; color:white; border:none; border-radius:10px;}}</style></head>
    <body><div class="card"><h2>💰 {bal} TK</h2><p>ID: {user_id}</p><p>রেফার: {refc} জন</p><hr><h3>Withdraw</h3>
    <form action="/api/withdraw" method="get"><input type="hidden" name="user_id" value="{user_id}">
    <select name="method" required><option value="">পেমেন্ট সিলেক্ট করুন</option><option value="Bkash">Bkash</option><option value="Nagad">Nagad</option></select><br>
    <input name="number" placeholder="Bkash/Nagad Number" required><br>
    <input name="amount" type="number" placeholder="Min 100" min="100" max="{bal}" required><br><br><button>Withdraw</button></form><br><a href="/?id={user_id}">Back</a></div></body></html>
    """

@app.get("/api/withdraw")
def withdraw(user_id: str, number: str, amount: int, method: str):
    if user_id=="guest":
        return HTMLResponse("❌ Guest ID দিয়ে Withdraw হবে না! বট থেকে Open App দিয়ে ঢুকুন <a href='/'>Back</a>")
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT balance, name FROM users WHERE user_id=?",(user_id,)); row=c.fetchone()
    bal=row[0] if row else 0
    name=row[1] if row and row[1] else "User"
    if amount>bal: return HTMLResponse(f"❌ ব্যালেন্স কম! আছে {bal} TK <a href='/earnings/{user_id}'>Back</a>")
    if amount<100: return HTMLResponse(f"❌ Min 100 TK <a href='/earnings/{user_id}'>Back</a>")
    c.execute("UPDATE users SET balance=balance-? WHERE user_id=?",(amount, user_id))
    c.execute("INSERT INTO withdraws (user_id,amount,number,status) VALUES (?,?,?,?)",(user_id,amount,f"{method}-{number}",'pending'))
    conn.commit(); conn.close()

    # তোমার বটে প্রফেশনাল নোটিফিকেশন যাবে
    try:
        msg = f"💸 *New Withdraw Request!*\n\n👤 Name: {name}\n🆔 User ID: `{user_id}`\n💳 Method: *{method}*\n🔢 Number: `{number}`\n💰 Amount: *{amount} TK*\n\n👉 User Profile: [Click](tg://user?id={user_id})"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Approve করতে Admin Panel", url=f"{WEBAPP_URL}/admin/{ADMIN_ID}"))
        markup.add(InlineKeyboardButton(f"👤 {name} কে মেসেজ দিন", url=f"tg://user?id={user_id}"))
        bot.send_message(ADMIN_ID, msg, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(e)
    return HTMLResponse(f"✅ {method} ({number}) এ {amount} TK Request পাঠানো হয়েছে! Admin Approve করবে।<br><br><a href='/earnings/{user_id}'>Back</a>")

@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_page(admin_id: str):
    if admin_id!=ADMIN_ID: return HTMLResponse("Not Admin", status_code=403)
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM users"); total_users=c.fetchone()[0]
    c.execute("SELECT SUM(balance) FROM users"); total_taka=c.fetchone()[0] or 0
    c.execute("SELECT * FROM users ORDER BY rowid DESC"); users=c.fetchall()
    c.execute("SELECT * FROM withdraws ORDER BY id DESC"); withdraws=c.fetchall()
    conn.close()
    html = f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{font-family:sans-serif; background:#f1f2f6; padding:10px;}}.box{{flex:1; background:white; padding:15px; border-radius:12px; text-align:center;}} table{{width:100%; background:white; border-collapse:collapse; margin-top:15px;}} th,td{{padding:8px; border-bottom:1px solid #eee; font-size:12px;}} th{{background:#6a11cb; color:white;}}.card{{background:white; padding:12px; border-radius:10px; margin-top:10px;}}</style></head><body>
    <h2>👑 Admin Dashboard</h2><div style="display:flex; gap:10px;"><div class="box">ইউজার<br><h2>{total_users}</h2></div><div class="box">মোট টাকা<br><h2>{total_taka} TK</h2></div><div class="box">Withdraw<br><h2>{len(withdraws)}</h2></div></div>
    <h3>💸 Pending Withdraw</h3>"""
    has=False
    for r in withdraws:
        if r[4]=='pending':
            has=True
            html+=f"<div class='card'>ID:{r[0]} | User:{r[1]}<br>{r[2]} TK - {r[3]}<br><a href='/api/approve?id={r[0]}&admin={ADMIN_ID}'><button style='background:green;color:white;padding:8px 15px;border:none;border-radius:8px;'>Approve</button></a> <a href='tg://user?id={r[1]}'><button>Message User</button></a></div>"
    if not has: html+="<div class='card'>No Pending</div>"
    html+=f"""<h3>👥 ইউজার লিস্ট</h3><table><tr><th>ID</th><th>Name</th><th>Balance</th><th>Ref By</th><th>রেফার</th></tr>"""
    conn=sqlite3.connect('database.db'); c=conn.cursor()
    for u in users:
        uid=u[0]; bal=u[1]; ref_by=u[2] or "Direct"; name=u[3] if len(u)>3 else ""
        c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?",(uid,)); refc=c.fetchone()[0]
        html+=f"<tr><td><a href='tg://user?id={uid}'>{uid}</a></td><td>{name}</td><td>{bal}</td><td>{ref_by}</td><td>{refc}</td></tr>"
    conn.close()
    html+="</table></body></html>"
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
