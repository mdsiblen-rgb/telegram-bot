import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFmYq35DcAH7jPpMj_Y9ANLI7iI5AnCvq4"
WEB_URL = "https://telegram-bot-1-k77g.onrender.com"

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return """
    <html><body style="text-align:center; padding-top:50px; font-family:sans-serif;">
    <h1>💰 COMMUNITY TASK</h1>
    <h2>Dashboard is Live!</h2>
    <p>প্রতি বিজ্ঞাপনে ১৫ টাকা | প্রতি রেফারে ১১০ টাকা</p>
    <br><a href='https://t.me/tap2earn_real_channel' style="padding:15px 30px; background:#0088cc; color:white; text-decoration:none; border-radius:10px;">Join Channel</a>
    </body></html>
    """

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 App Open করো", web_app=WebAppInfo(url=WEB_URL))],
        [InlineKeyboardButton("📢 পেমেন্ট চ্যানেল", url="https://t.me/tap2earn_real_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 COMMUNITY TASK এ স্বাগতম!\nনিচে App Open এ চাপ দাও", reply_markup=reply_markup)

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
