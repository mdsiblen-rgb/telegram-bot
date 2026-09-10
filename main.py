import threading, sqlite3, os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import telebot

BOT_TOKEN = "8851083480:AAGiekbCF2sS6aLejQGT-3T1eSo_JAJs5rk"
ADMIN_ID = "8807178385"
CHANNEL_USERNAME = "@ProtidinerKajBD"
CHANNEL_LINK = "https://t.me/ProtidinerKajBD"

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

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    user_id = str(message.from_user.id)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (user_id, balance, ref_by) VALUES (?,?,?)", (user_id, 0, ref_id))
        if ref_id and ref_id!= user_id:
            c.execute("UPDATE users SET balance = balance + 25 WHERE user_id=?", (ref_id,))
            try: bot.send_message(ref_id, "🎉 নতুন রেফার! ২৫ টাকা পেয়েছেন।")
            except: pass
        conn.commit()
    conn.close()
    bot.reply_to(message, f"স্বাগতম! 👋\n\nID: {user_id}\nলিঙ্ক: https://am-bot-1-v77g.onrender.com/?id={user_id}\n\n1. Join: {CHANNEL_LINK}\n2. Website এ Task Complete করুন।")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_id = request.query_params.get("id", "guest")
    is_admin = "Admin" if user_id == ADMIN_ID else "User"
    return f"""
    <html><body style="font-family:sans-serif; text-align:center; padding:20px;">
    <h2>Welcome {is_admin} - {user_id}</h2>
    <p>Step 1: Join <a href='{CHANNEL_LINK}' target='_blank'>{CHANNEL_LINK}</a></p>
    <button onclick="fetch('/api/task?user_id={user_id}').then(r=>r.text()).then(a=>alert(a))" style="padding:15px; background:green; color:white; border:none; border-radius:10px;">Complete Task +10 TK</button>
    <br><br>
    <p><a href='/earnings/{user_id}'>My Earnings</a> | <a href='/admin/{ADMIN_ID}'>Admin</a></p>
    <p>Ref Link: https://am-bot-1-v77g.onrender.com/?id={user_id}</p>
    </body></html>
    """

@app.get("/api/task")
def task(user_id: str):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, int(user_id))
        if member.status in ['left', 'kicked']:
            return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK}"
    except:
        return f"আগে চ্যানেলে জয়েন করুন: {CHANNEL_LINK}"
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
    return f"<h2>Balance: {bal} TK</h2><form action='/api/withdraw' method='get'><input type='hidden' name='user_id' value='{user_id}'><input name='number' placeholder='Bkash/Nagad' required><input name='amount' type='number' placeholder='Amount' required><button>Withdraw</button></form><br><a href='/?id={user_id}'>Back</a>"

@app.get("/api/withdraw")
def withdraw(user_id: str, number: str, amount: int):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO withdraws (user_id, amount, number) VALUES (?,?,?)", (user_id, amount, number))
    conn.commit()
    conn.close()
    try: bot.send_message(ADMIN_ID, f"New Withdraw: {user_id} - {amount} TK - {number}")
    except: pass
    return HTMLResponse(f"Withdraw Sent! <a href='/earnings/{user_id}'>Back</a>")

@app.get("/admin/{admin_id}", response_class=HTMLResponse)
def admin_page(admin_id: str):
    if admin_id!= ADMIN_ID:
        return HTMLResponse("Not allowed", status_code=403)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM withdraws WHERE status='pending'")
    rows = c.fetchall()
    conn.close()
    html = "<h1>Admin - Withdraws</h1>"
    for r in rows:
        html += f"<p>ID:{r[0]} User:{r[1]} Amt:{r[2]} Num:{r[3]} <a href='/api/approve?id={r[0]}&admin={ADMIN_ID}'><button>Approve</button></a></p>"
    if not rows:
        html += "<p>No pending</p>"
    return HTMLResponse(html)

@app.get("/api/approve")
def approve(id: int, admin: str):
    if admin!= ADMIN_ID:
        return "Not admin"
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE withdraws SET status='approved' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return HTMLResponse(f"Approved! <a href='/admin/{ADMIN_ID}'>Back</a>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
