import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from flask import Flask, send_from_directory
import threading
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = "https://telegram-bot-1-v77g.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('templates', 'admin.html')

@bot.message_handler(commands=['start'])
def start(m):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌐 Community Task", "💰 Balance")
    bot.send_message(m.chat.id, "✅ বট চালু আছে\nCommunity Task এ ক্লিক করো", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🌐 Community Task")
def community_task(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏢 Open Company App", web_app=WebAppInfo(url=APP_URL)))
    markup.add(InlineKeyboardButton("💲 Direct Link omg10.com", url="https://omg10.com/4/11760259"))
    bot.send_message(m.chat.id, "কোম্পানি অ্যাপ ওপেন করো 👇", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
