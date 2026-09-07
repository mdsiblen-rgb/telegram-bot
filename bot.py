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
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:sans-serif; text-align:center; background:#f0f8ff; padding:20px;}
    .card{background:white; padding:20px; border-radius:15px; box-shadow:0 4px 10px #ccc; max-width:400px; margin:auto;}
    .btn{display:block; background:#0088cc; color:white; padding:15px; margin:10px 0; border-radius:10px; text-decoration:none; font-weight:bold;}
    </style>
    </head>
    <body>
    <div class="card">
    <h1>💰 COMMUNITY TASK</h1>
    <p>আজকের আয়: ৳০ | রেফার: ০</p>
    <a class="btn" href="#">📺 বিজ্ঞাপন দেখো - ৳১৫</a>
    <a class="btn" href="#">👥 রেফার করো - ৳১১০</a>
    <a class="btn" href="https://t.me/tap2earn_real_channel">📢 পেমেন্ট চ্যানেল</a>
    <p>মিনিমাম উইথড্র ৫০০ টাকা (বিকাশ/নগদ)</p>
    </div>
    </body>
    </html>
    """

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚀 App Open করো", web_app=WebAppInfo(url=WEB_URL))]]
    await update.message.reply_text("👋 স্বাগতম! App Open করো", reply_markup=InlineKeyboardMarkup(keyboard))

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
