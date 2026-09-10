import os, sqlite3, threading, datetime
from flask import Flask, request, render_template_string, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEB_URL = "https://telegram-bot-1-v77g.onrender.com"
AD_LINK = "https://omg10.com/4/11760259"
ADMIN_ID = "8807178385" # তোমার ID বসানো আছে

def init_db():
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT, name TEXT, balance INTEGER, referred_by TEXT, refer_count INTEGER, total_task INTEGER, join_date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, method TEXT, number TEXT, amount INTEGER, status TEXT, date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, date TEXT)")
    con.commit(); con.close()
init_db()
app = Flask(__name__)

HOME_HTML = """<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Protidin Kaj</title>
<style>body{margin:0;font-family:sans-serif;background:#f0f2f5}.header{background:linear-gradient(135deg,#00b09b,#96c93d);color:white;padding:25px;text-align:center;border-radius:0 0 25px 25px}.card{background:white;margin:12px;padding:16px;border-radius:16px;box-shadow:0 4px 10px rgba(0,0,0,.07)}.balance{font-size:34px;font-weight:900;text-align:center;color:#00a854}.btn{width:100%;padding:14px;border:none;border-radius:12px;font-size:16px;font-weight:bold;margin-top:10px;cursor:pointer}.btn-g{background:#00b14f;color:white}.btn-o{background:#ff8c00;color:white}.btn-b{background:#0084ff;color:white}.welcome{background:#d4edda;color:#155724;padding:12px;border-radius:10px;text-align:center;font-weight:bold}</style>
<script>function doTask(uid){ window.open('""" + AD_LINK + """', '_blank'); setTimeout(function(){ fetch('/complete_task?id='+uid).then(()=>location.reload()); }, 2000); }</script>
</head><body>
<div class="header"><h2>🏢 Protidin Kaj BD</h2><p>প্রতিদিন কাজ, প্রতিদিন ইনকাম</p></div>
{% if new_user %}<div class="card"><div class="welcome">🎉 স্বাগতম! ৫০ টাকা বোনাস পেয়েছেন!</div></div>{% endif %}
<div class="card"><div style="text-align:center;color:gray;font-size:12px">ID: {{user_id}} | {{name}}</div><div style="text-align:center;color:gray;font-size:13px">ব্যালেন্স</div><div class="balance">৳ {{balance}}</div><button class="btn btn-g" onclick="doTask('{{user_id}}')">💲 টাস্ক করুন - ১০ টাকা</button></div>
<div class="card"><h3>👥 রেফার - ২৫ টাকা</h3><div style="background:#eef1ff;padding:10px;border-radius:10px;text-align:center;font-weight:bold;word-break:break-all;font-size:13px">{{ref_link}}</div><button class="btn btn-b" onclick="navigator.clipboard.writeText('{{ref_link}}');alert('কপি হয়েছে!')">লিংক কপি</button><p>রেফার: <b>{{refer_count}} জন</b> | টাস্ক: <b>{{total_task}} টি</b></p></div>
<div class="card"><h3>💸 বিকাশ/নগদে তুলুন</h3><form method="POST" action="/withdraw"><input type="hidden" name="user_id" value="{{user_id}}"><select name="method" required style="width:100%;padding:12px;border-radius:10px"><option value="">সিলেক্ট করুন</option><option value="bKash">bKash</option><option value="Nagad">Nagad</option></select><input type="text" name="number" placeholder="আপনার নাম্বার" required style="width:100%;padding:12px;margin-top:8px;border-radius:10px;border:1px solid #ddd"><input type="number" name="amount" placeholder="৫০০ মিনিমাম" min="500" required style="width:100%;padding:12px;margin-top:8px;border-radius:10px;border:1px solid #ddd"><button class="btn btn-o" type="submit">উইথড্র দিন</button></form></div>
<div class="card" style="text-align:center"><a href="/admin?admin_id={{user_id}}">🔐 Admin</a> | <a href="/earnings?admin_id={{user_id}}">💰 My Earnings</a></div>
</body></html>"""

ADMIN_HTML = """<h1>👑 Admin - সব ইউজার</h1><p><a href="/">Home</a> | <a href="/earnings?admin_id={{admin_id}}">💰 Income</a></p><p>মোট ইউজার: {{total_users}}</p><table border=1 cellpadding=8><tr><th>ID</th><th>Username</th><th>Name</th><th>Balance</th><th>Ref By</th><th>Ref Count</th><th>Task</th><th>Join</th></tr>{% for u in users %}<tr><td>{{u[0]}}</td><td>{{u[1]}}</td><td>{{u[2]}}</td><td style="color:green;font-weight:bold">{{u[3]}}</td><td>{{u[4]}}</td><td>{{u[5]}}</td><td>{{u[6]}}</td><td>{{u[7]}}</td></tr>{% endfor %}</table><h2>Withdraw</h2><table border=1 cellpadding=8><tr><th>User</th><th>Method</th><th>Number</th><th>Amount</th><th>Status</th><th>Date</th></tr>{% for w in withdraws %}<tr><td>{{w[1]}}</td><td>{{w[2]}}</td><td>{{w[3]}}</td><td>{{w[4]}}</td><td>{{w[5]}}</td><td>{{w[6]}}</td></tr>{% endfor %}</table>"""

EARNINGS_HTML = """<h1>💰 আমার ইনকাম</h1><p><a href="/">Home</a> | <a href="/admin?admin_id={{admin_id}}">Users</a></p><div style="border:2px solid green;padding:20px;border-radius:15px;background:#e8f5e9"><p>মোট ক্লিক: <b>{{total_clicks}} বার</b></p><h3>আনুমানিক: ${{est_usd}} ≈ ৳ {{est_bdt}} টাকা</h3><p>আসল টাকা Monetag এ দেখো</p></div>"""

@app.route('/')
def home():
    user_id = request.args.get('id', '0'); username = request.args.get('username', 'NoUsername'); name = request.args.get('name', 'User'); ref = request.args.get('ref')
    if user_id == '0': user_id = 'guest_' + os.urandom(3).hex()
    con = sqlite3.connect("database.db", check_same_thread=False); cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,)); user = cur.fetchone()
    new_user=False
    if not user:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (user_id, username, name, 50, ref, 0, 0, now))
        new_user=True
        if ref and ref!= user_id: cur.execute("UPDATE users SET balance=balance+25, refer_count=refer_count+1 WHERE user_id=?", (ref,))
        con.commit()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,)); u = cur.fetchone(); con.close()
    ref_link = f"https://t.me/ProtidinerKaj_BD_Bot?start={user_id}"
    return render_template_string(HOME_HTML, user_id=u[0], name=u[2], balance=u[3], refer_count=u[5], total_task=u[6], ref_link=ref_link, new_user=new_user)

@app.route('/complete_task')
def complete_task():
    uid = request.args.get('id'); now_full = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    con = sqlite3.connect("database.db", check_same_thread=False); cur = con.cursor()
    cur.execute("UPDATE users SET balance=balance+10, total_task=total_task+1 WHERE user_id=?", (uid,))
    cur.execute("INSERT INTO tasks (user_id, date) VALUES (?,?)", (uid, now_full)); con.commit(); con.close(); return "ok"

@app.route('/withdraw', methods=['POST'])
def withdraw():
    user_id, method, number, amount = request.form['user_id'], request.form['method'], request.form['number'], int(request.form['amount'])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    con = sqlite3.connect("database.db", check_same_thread=False); cur = con.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)); row = cur.fetchone()
    if row and row[0] >= amount:
        cur.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (amount, user_id))
        cur.execute("INSERT INTO withdraws (user_id, method, number, amount, status, date) VALUES (?,?,?,?,?,?)", (user_id, method, number, amount, 'Pending', now)); con.commit()
    con.close(); return redirect(f"/?id={user_id}")

@app.route('/admin')
def admin_panel():
    admin_id = request.args.get('admin_id')
    if admin_id!= ADMIN_ID: return f"Not allowed. Your ID {admin_id} is not admin. Admin ID is {ADMIN_ID}"
    con = sqlite3.connect("database.db", check_same_thread=False); cur = con.cursor()
    cur.execute("SELECT * FROM users ORDER BY id DESC"); users = cur.fetchall()
    cur.execute("SELECT * FROM withdraws ORDER BY id DESC"); w = cur.fetchall(); con.close()
    return render_template_string(ADMIN_HTML, users=users, withdraws=w, total_users=len(users), admin_id=admin_id)

@app.route('/earnings')
def earnings():
    admin_id = request.args.get('admin_id')
    if admin_id!= ADMIN_ID: return "Not allowed"
    con = sqlite3.connect("database.db", check_same_thread=False); cur = con.cursor()
    cur.execute("SELECT * FROM tasks"); tasks = cur.fetchall(); con.close()
    total = len(tasks); est_usd = round(total * 0.02, 2); est_bdt = round(est_usd * 122, 2)
    return render_template_string(EARNINGS_HTML, total_clicks=total, est_usd=est_usd, est_bdt=est_bdt, admin_id=admin_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id); username = update.effective_user.username or "NoUsername"; name = update.effective_user.first_name or "User"
    con = sqlite3.connect("database.db", check_same_thread=False); cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    if not cur.fetchone():
        ref = context.args[0] if context.args else None
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (uid, username, name, 50, ref, 0, 0, now))
        if ref and ref!= uid: cur.execute("UPDATE users SET balance=balance+25, refer_count=refer_count+1 WHERE user_id=?", (ref,))
        con.commit()
    con.close()
    kb = [[InlineKeyboardButton("💰 অ্যাপ ওপেন করুন", web_app=WebAppInfo(url=f"{WEB_URL}?id={uid}&username={username}&name={name}"))]]
    await update.message.reply_text(f"🎉 স্বাগতম {name}! ৫০ টাকা বোনাস পেয়েছেন!", reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    if BOT_TOKEN:
        a = ApplicationBuilder().token(BOT_TOKEN).build(); a.add_handler(CommandHandler("start", start)); a.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
