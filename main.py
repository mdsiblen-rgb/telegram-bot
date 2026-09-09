import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from flask import Flask, send_from_directory
import threading

BOT_TOKEN = "এখানে তোমার টোকেন বসাও"
APP_URL = "https://telegram-bot-1-v77g.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(m):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌐 Community Task", "💰 Balance")
    bot.send_message(m.chat.id, "বট চালু আছে ✅\nCommunity Task এ ক্লিক করো", reply_markup=markup)

# ✅ এইটা এখন bot এর নিচে আছে, তাই Error হবে না
@bot.message_handler(func=lambda m: m.text == "🌐 Community Task")
def community_task(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏢 Open Company App", web_app=WebAppInfo(url=APP_URL)))
    markup.add(InlineKeyboardButton("💲 Direct Link - omg10.com", url="https://omg10.com/4/11760259"))
    bot.send_message(m.chat.id, "কোম্পানি অ্যাপ ওপেন করো 👇", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

def run_web():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
