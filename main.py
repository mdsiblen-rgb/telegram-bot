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

def main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Balance", "👥 My Referrals")
    markup.add("🔗 Refer Link", "🎁 Daily Bonus")
    markup.add("🛠 Admin Panel", "🌐 Community Task")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    data = c.fetchone()

    if not data:
        welcome_bonus = 10
        c.execute("INSERT INTO users (user_id, balance, ref_by) VALUES (?,?,?)", (user_id, welcome_bonus, ref_id))
        if ref_id and ref_id!= user_id:
            c.execute("UPDATE users SET balance = balance + 25 WHERE user_id=?", (ref_id,))
            try:
                bot.send_message(ref_id, f"🎉 অভিনন্দন! {user_name} আপনার লিঙ্কে জয়েন করেছে! আপনি ২৫ টাকা বোনাস পেয়েছেন! 🔥")
            except:
                pass
        conn.commit()
        if ref_id:
            welcome_text = f"🎉 স্বাগতম {user_name}! 👋\n\n🔥 আপনি ১০ টাকা ওয়েলকাম বোনাস পেয়েছেন!\n\n💰 বন্ধুর লিঙ্কে ঢোকার জন্য!\n\n🚀 এখন কাজ শুরু করুন:\n1. চ্যানেলে জয়েন করুন\n2. Open App এ ক্লিক করে আরো ১০ টাকা নিন!\n\n🔗 আপনার রেফার লিঙ্ক:\n{WEBAPP_URL}/?id={user_id}"
        else:
            welcome_text = f"👋 স্বাগতম {user_name}!\n\n🎁 আপনি ১০ টাকা ওয়েলকাম বোনাস পেয়েছেন!\n\n🚀 কাজ শুরু করুন!"
    else:
        welcome_text = f"স্বাগতম {user_name}! 👋\n\nID: {user_id}\nলিঙ্ক: {WEBAPP_URL}/?id={user_id}"

    conn.close()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 Open App - 10 TK নিন", web_app={"url": f"{WEBAPP_URL}/?id={user_id}"}))
    markup.add(InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    bot.send_message(message.chat.id, "মেনু থেকে সিলেক্ট করুন:", reply_markup=main_keyboard(user_id))

@bot.message_handler(func=lambda m: True)
def all_text(message):
    user_id = str(message.from_user.id)
    text = message.text
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    bal = row[0] if row else 0
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?", (user_id,))
    refs = c.fetchone()[0]
    conn.close()
    if "Balance" in text:
        bot.reply_to(message, f"💰 আপনার ব্যালেন্স: {bal} TK", reply_markup=main_keyboard(user_id))
    elif "Referrals" in text:
        bot.reply_to(message, f"👥 মোট রেফার: {refs} জন", reply_markup=main_keyboard(user_id))
    elif "Refer Link" in text:
        bot.reply_to(message, f"🔗 আপনার লিঙ্ক:\n{WEBAPP_URL}/?id={user_id}\n\nবট লিঙ্ক:\nhttps://t.me/ProtidinerKaj_BD_Bot?start={user_id}", reply_markup=main_keyboard(user_id))
    elif "Daily Bonus" in text:
        bot.reply_to(message, "🎁 Daily Bonus নিতে অ্যাপ ওপেন করুন।", reply_markup=main_keyboard(user_id))
    elif "Admin Panel" in text:
        if user_id == ADMIN_ID:
            bot.reply_to(message, f"🛠 Admin: {WEBAPP_URL}/admin/{ADMIN_ID}")
        else:
            bot.reply_to(message, "আপনি Admin না।")
    elif "Community" in text:
        bot.reply_to(message, f"🌐 আমাদের চ্যানেল: {CHANNEL_LINK}")

def run_bot():
    bot.infinity_polling()
threading.Thread(target=run_bot, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_id = request.query_params.get("id", "guest")
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{font-family:sans-serif; text-align:center; background:#f5f5f5; padding:20px;}}
   .card{{background:white; padding:20px; border-radius:15px; box-shadow:0 2px 10px #ccc; max-width:400px; margin:auto;}}
    button{{width:100%; padding:15px; margin:10px 0; border:none; border-radius:10px; font-size:16px;}}
   .green{{background:#28a745; color:white;}}.blue{{background:#007bff; color:white;}}
    </style></head>
    <body><div class="card">
    <h2>Protidin Kaj BD</h2><p>Welcome {user_id}</p>
    <a href="{CHANNEL_LINK}" target="_blank"><button class="blue">Step 1: Join Channel</button></a>
    <button class="green" onclick="fetch('/api/task?user_id={user_id}').then(r=>r.text()).then(a=>alert(a))">Complete Task +10 TK</button>
    <br><br><a href='/earnings/{user_id}'>My Earnings</a> | <a href='/admin/{ADMIN_ID}'>Admin</a>
    <p style="font-size:12px; word-break:break-all;">Ref: {WEBAPP_URL}/?id={user_id}</p>
    </div></body></html>
    """

@app.get("/api/task")
def task(user_id: str):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, int(user_id))
        if member.status in ['left', 'kicked']:
            return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK}"
    except:
        return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK}"
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + 10 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return "Task Completed! 10 TK Added"

@app.get("/earnings/{user_id}", response_class=HTMLResponse)
def earnings(user_id: str):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    bal = row[0] if row else 0
    conn.close()
    return f"<h2>Balance: {bal} TK</h2><form action='/api/withdraw' method='get'><input type='hidden' name='user_id' value='{user_id}'><input name='number' placeholder='Bkash/Nagad' required><input name='amount' type='number' required><button>Withdraw</button></form>"

@app.get("/api/withdraw")
def withdraw(user_id: str, number: str, amount: int):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO withdraws (user_id, amount, number) VALUES (?,?,?)", (user_id, amount, number))
    conn.commit()
    conn.close()
    try: bot.send_message(ADMIN_ID, f"New Withdraw: {user_id} - {amount} - {number}")
    except: pass
    return HTMLResponse(f"Sent! <a href='/earnings/{user_id}'>Back</a>")

@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_page(admin_id: str):
    if admin_id!= ADMIN_ID: return HTMLResponse("Not allowed", status_code=403)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM withdraws WHERE status='pending'")
    rows = c.fetchall()
    conn.close()
    html = "<h1>Admin Panel</h1>"
    for r in rows:
        html += f"<p>{r[0]} User:{r[1]} {r[2]} TK {r[3]} <a href='/api/approve?id={r[0]}&admin={ADMIN_ID}'>Approve</a></p>"
    if not rows: html += "<p>No pending</p>"
    return HTMLResponse(html)

@app.get("/api/approve")
def approve(id: int, admin: str):
    if admin!= ADMIN_ID: return "No"
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE withdraws SET status='approved' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return HTMLResponse(f"Approved <a href='/admin/{ADMIN_ID}'>Back</a>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
