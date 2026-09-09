from flask import Flask, render_template
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup
import os

app = Flask(__name__)
URL = "https://telegram-bot-1-v77g.onrender.com"

@app.route('/')
def home():
    return render_template('index.html')

# এটা তোমার বটের মেনু ঠিক করবে
def get_main_menu():
    keyboard = [
        ["💰 Balance", "👥 My Referrals"],
        ["🎁 Daily Bonus", "🔗 Refer Link"],
        ["🌐 Community Task", "🛠️ Admin Panel"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
