import os
from flask import Flask
from threading import Thread
import telebot

# তোমার বট টোকেন এখানে
BOT_TOKEN = os.environ.get("BOT_TOKEN", "তোমার টোকেন এখানে বসাও")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot Active! ✅")

def run_bot():
    bot.infinity_polling()

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_flask()
