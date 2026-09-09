import os
import telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
print(f"Token check -> has_colon={':' in BOT_TOKEN}")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(msg):
    args = msg.text.split()
    ref_by = None
    if len(args) > 1 and "ref_" in args[1]:
        ref_by = args[1].split("ref_")[1]

    if ref_by:
        bot.send_message(msg.chat.id, f"Welcome! 🎉 You were invited by {ref_by}\nYour link: t.me/{bot.get_me().username}?start=ref_{msg.from_user.id}")
    else:
        bot.send_message(msg.chat.id, f"Welcome! 🎉\nYour referral link:\nt.me/{bot.get_me().username}?start=ref_{msg.from_user.id}")

keep_alive()
print("Bot is running...")

