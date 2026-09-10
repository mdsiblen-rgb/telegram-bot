import os, sqlite3, threading
from flask import Flask, request, render_template_string, redirect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- তোমার লিংকগুলো এখানে সেট করা আছে ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
WEB_URL = "https://telegram-bot-1-v77g.onrender.com"
AD_LINK = "https://omg10.com/4/11760259"

def init_db():
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, balance INTEGER, referred_by TEXT, refer_count INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, method TEXT, number TEXT, amount INTEGER, status TEXT)")
    con.commit()
    con.close()
init_db()

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Protidin Kaj BD</title>
<style>
body{margin:0;font-family:sans-serif;background:#f0f2f5}
.header{background:linear-gradient(135deg,#00b09b,#96c93d);color:white;padding:25px;text-align:center;border-radius:0 0 25px 25px}
.card{background:white;margin:12px;padding:16px;border-radius:16px;box-shadow:0 4px 10px rgba(0,0,0,.07)}
.balance{font-size:34px;font-weight:900;text-align:center;color:#00a854}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-size:16px;font-weight:bold;margin-top:10px;cursor:pointer}
.btn-g{background:#00b14f;color:white}.btn-o{background:#ff8c00;color:white}.btn-b{background:#0084ff;color:white}
.welcome{background:#d4edda;color:#155724;padding:12px;border-radius:10px;text-align:center;font-weight:bold;border:1px solid #c3e6cb}
.ad{background:#fff8e1;border:1px dashed #ffc107;padding:10px;border-radius:10px;text-align:center}
input,select{width:100%;padding:12px;margin-top:8px;border-radius:10px;border:1px solid #ddd;box-sizing:border-box}
</style>
<script>
function doTask(uid){
    window.open('""" + AD_LINK + """', '_blank');
    setTimeout(function(){ fetch('/complete_task?id='+uid).then(()=>location.reload()); }, 2000);
}
</script>
</head><body>
<div class="header"><h2 style="margin:0">🏢 Protidin Kaj BD</h2><p>প্রতিদিন কাজ, প্রতিদিন ইনকাম</p></div>

{% if new_user %}
<div class="card"><div class="welcome">🎉 স্বাগতম! আপনি ৫০ টাকা বোনাস পেয়েছেন!</div></div>
{% endif %}

<div class="card"><div style="color:gray;font-size:13px;text-align:center">আপনার ব্যালেন্স</div><div class="balance">৳ {{balance}}</div>
<button class="btn btn-g" onclick="doTask('{{user_id}}')">💲 টাস্ক করুন - ১০ টাকা ইনকাম</button>
<p style="font-size:11px;color:gray;text-align:center">ক্লিক করলে বিজ্ঞাপন খুলবে, ২ সেকেন্ড পর টাকা যোগ হবে</p>
</div>

<div class="card ad"><b>📢 কোম্পানির স্পন্সর বিজ্ঞাপন</b><br><span style="font-size:11px">বিজ্ঞাপন দেখলেই আপনার ইনকাম হবে</span></div>

<div class="card"><h3>👥 রেফার করে ইনকাম</h3><p style="font-size:13px">প্রতি রেফারে পাবেন ২৫ টাকা!</p>
<div style="background:#eef1ff;padding:10px;border-radius:10px;text-align:center;font-weight:bold;word-break:break-all;font-size:13px">{{ref_link}}</div>
<button class="btn btn-b" onclick="navigator.clipboard.writeText('{{ref_link}}');alert('লিংক কপি হয়েছে!')">লিংক কপি করুন</button>
<p style="font-size:13px">আপনি জয়েন করিয়েছেন: <b>{{refer_count}} জন</b></p></div>

<div class="card"><h3>💸 বিকাশ / নগদে টাকা তুলুন</h3><form method="POST" action="/withdraw"><input type="hidden" name="user_id" value="{{user_id}}">
<select name="method" required><option value="">bKash / Nagad সিলেক্ট করুন</option><option value="bKash">bKash</option><option value="Nagad">Nagad</option></select>
<input type="text" name="number" placeholder="আপনার নাম্বার" required><input type="number" name="amount" placeholder="পরিমান (সর্বনিম্ন ৫০০)" min="500" required>
<button class="btn btn-o" type="submit">উইথড্র রিকোয়েস্ট দিন</button></form></div>

<div class="card"><a href="/admin" style="display:block;text-align:center;text-decoration:none;color:gray;font-size:12px">Admin Panel</a></div>
</body></html>
"""

@app.route('/')
def home():
    user_id = request.args.get('id', 'guest_'+os.urandom(4).hex())
    ref = request.args.get('ref')
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    new_user = False
    if not user:
        cur.execute("INSERT INTO users VALUES (?,?,?,0)", (user_id, 50, ref))
        new_user = True
        if ref and ref!= user_id:
            cur.execute("SELECT * FROM users WHERE user_id=?", (ref,))
            if cur.fetchone():
                cur.execute("UPDATE users SET balance=balance+25, refer_count=refer_count+1 WHERE user_id=?", (ref,))
        con.commit()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    u = cur.fetchone()
    balance, refer_count = u[1], u[3]
    con.close()
    ref_link = f"https://t.me/ProtidinerKaj_BD_Bot?start={user_id}"
    return render_template_string(HTML_PAGE, user_id=user_id, balance=balance, refer_count=refer_count, ref_link=ref_link, new_user=new_user)

@app.route('/complete_task')
def complete_task():
    uid = request.args.get('id')
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("UPDATE users SET balance=balance+10 WHERE user_id=?", (uid,))
    con.commit()
    con.close()
    return "ok"

@app.route('/withdraw', methods=['POST'])
def withdraw():
    user_id, method, number, amount = request.form['user_id'], request.form['method'], request.form['number'], int(request.form['amount'])
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    if row and row[0] >= amount:
        cur.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (amount, user_id))
        cur.execute("INSERT INTO withdraws (user_id, method, number, amount, status) VALUES (?,?,?,?,?)", (user_id, method, number, amount, 'Pending'))
        con.commit()
    con.close()
    return redirect(f"/?id={user_id}")

@app.route('/admin')
def admin_panel():
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("SELECT * FROM users ORDER BY balance DESC")
    users = cur.fetchall()
    cur.execute("SELECT * FROM withdraws ORDER BY id DESC")
    w = cur.fetchall()
    con.close()
    html = "<h2>সব ইউজার - কার কত টাকা</h2><table border=1 cellpadding=6><tr><th>User ID</th><th>Balance</th><th>Ref By</th><th>Ref Count</th></tr>"
    for u in users: html+=f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td></tr>"
    html+="</table><h2>বিকাশ/নগদ উইথড্র লিস্ট</h2><table border=1 cellpadding=6><tr><th>User</th><th>Method</th><th>Number</th><th>Amount</th><th>Status</th></tr>"
    for x in w: html+=f"<tr><td>{x[1]}</td><td>{x[2]}</td><td>{x[3]}</td><td>{x[4]}</td><td>{x[5]}</td></tr>"
    html+="</table><br><a href='/'>Home</a>"
    return html

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    if not cur.fetchone():
        ref = context.args[0] if context.args else None
        cur.execute("INSERT INTO users VALUES (?,?,?,0)", (uid, 50, ref))
        if ref and ref!= uid:
            cur.execute("SELECT * FROM users WHERE user_id=?", (ref,))
            if cur.fetchone():
                cur.execute("UPDATE users SET balance=balance+25, refer_count=refer_count+1 WHERE user_id=?", (ref,))
        con.commit()
    con.close()
    keyboard = [[InlineKeyboardButton("💰 অ্যাপ ওপেন করুন", web_app=WebAppInfo(url=f"{WEB_URL}?id={uid}"))],
                [InlineKeyboardButton("📢 চ্যানেল জয়েন", url="https://t.me/ProtidinerKajBD")]]
    await update.message.reply_text(f"🎉 স্বাগতম! আপনি ৫০ টাকা বোনাস পেয়েছেন!\n\nআপনার রেফার লিংক: https://t.me/ProtidinerKaj_BD_Bot?start={uid}\nপ্রতি রেফারে ২৫ টাকা!", reply_markup=InlineKeyboardMarkup(keyboard))

def run_bot():
    if "PUT_YOUR" not in BOT_TOKEN:
        app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
