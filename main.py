import os, json, time
from datetime import datetime
import telebot
from telebot import types
from flask import Flask
from threading import Thread

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) # Render Environment এ তোমার ID বসাবে

# Simple Database
DB_FILE = "users.json"
def load_db():
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}
def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

@app.route('/')
def home(): return "Bot is Live ✅"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
Thread(target=run, daemon=True).start()

# Keyboards
def main_menu():
    mk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mk.row("💰 Balance", "👥 My Referrals")
    mk.row("🎁 Daily Bonus", "🔗 Refer Link")
    mk.row("🌐 Community Task", "🛠️ Admin Panel")
    return mk

@bot.message_handler(commands=['start'])
def start(msg):
    db = load_db()
    uid = str(msg.from_user.id)
    args = msg.text.split()
    ref_by = None
    if len(args) > 1 and "ref_" in args[1]:
        ref_by = args[1].split("ref_")[-1]

    if uid not in db:
        db[uid] = {"balance": 0, "referrals": 0, "referred_by": ref_by, "last_bonus": 0}
        if ref_by and ref_by!= uid and ref_by in db:
            db[ref_by]["balance"] += 20
            db[ref_by]["referrals"] += 1
        save_db(db)
        if ref_by:
            try: bot.send_message(ref_by, f"🎉 নতুন রেফার! {msg.from_user.first_name} তোমার লিংকে জয়েন করেছে। +20৳")
            except: pass

    bot.send_message(msg.chat.id, f"👋 স্বাগতম {msg.from_user.first_name}!\n\nProtidin Kaj বটে আপনাকে স্বাগতম। নিচের মেনু থেকে কাজ করুন।", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(m):
    db = load_db()
    u = db.get(str(m.from_user.id), {"balance":0})
    bot.send_message(m.chat.id, f"💰 আপনার ব্যালেন্স: {u['balance']}৳")

@bot.message_handler(func=lambda m: m.text == "👥 My Referrals")
def myref(m):
    db = load_db()
    u = db.get(str(m.from_user.id), {"referrals":0})
    bot.send_message(m.chat.id, f"👥 আপনার মোট রেফার: {u['referrals']} জন")

@bot.message_handler(func=lambda m: m.text == "🔗 Refer Link")
def reflink(m):
    username = bot.get_me().username
    link = f"https://t.me/{username}?start=ref_{m.from_user.id}"
    bot.send_message(m.chat.id, f"🔗 আপনার রেফার লিংক:\n{link}\n\nপ্রতি রেফারে ২০৳ পাবেন।")

@bot.message_handler(func=lambda m: m.text == "🎁 Daily Bonus")
def bonus(m):
    db = load_db()
    uid = str(m.from_user.id)
    now = time.time()
    u = db.get(uid)
    if not u: return
    if now - u.get("last_bonus",0) > 86400:
        u["balance"] += 10
        u["last_bonus"] = now
        save_db(db)
        bot.send_message(m.chat.id, "🎁 Daily Bonus পেয়েছেন 10৳!")
    else:
        bot.send_message(m.chat.id, "⏳ আজকের বোনাস নেওয়া হয়ে গেছে, কাল আবার চেষ্টা করুন।")

@bot.message_handler(func=lambda m: m.text == "🌐 Community Task")
def task(m):
    bot.send_message(m.chat.id, "🌐 আমাদের চ্যানেলে জয়েন করুন: @YourChannelLink")

@bot.message_handler(func=lambda m: m.text == "🛠️ Admin Panel")
def admin(m):
    if m.from_user.id!= ADMIN_ID:
        return bot.send_message(m.chat.id, "❌ আপনি এডমিন না।")
    db = load_db()
    bot.send_message(m.chat.id, f"🛠️ Admin Panel\nTotal Users: {len(db)}")

print("Bot is running with full features...")
bot.infinity_polling()
