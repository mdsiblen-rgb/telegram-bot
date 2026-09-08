from flask import Flask, render_template
import os
import threading

# Flask App for Render
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Telegram Bot Part - এটা না থাকলেও ওয়েবসাইট চলবে
try:
    import telebot
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if BOT_TOKEN:
        bot = telebot.TeleBot(BOT_TOKEN)
        
        @bot.message_handler(commands=['start'])
        def start(message):
            bot.reply_to(message, "Bot is Live ✅")
        
        def run_bot():
            bot.infinity_polling()
        
        # Bot আলাদা Thread এ চলবে
        threading.Thread(target=run_bot, daemon=True).start()
except Exception as e:
    print(f"Bot not started: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
