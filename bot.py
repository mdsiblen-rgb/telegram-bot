import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8851083480:AAFmYq35DcAH7jPpMj_Y9ANLI7iI5AnCvq4"
WEB_URL = "https://telegram-bot-1-k77g.onrender.com"

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "<h1>Bot is Live! Dashboard is Ready</h1>"

# --- Bot Logic ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("💰 Balance"), KeyboardButton("👥 My Referrals")],
        [KeyboardButton("🔗 Refer Link"), KeyboardButton("💳 Withdraw")],
        [KeyboardButton("🌐 Community Task"), KeyboardButton("🎁 Daily Bonus")],
        [KeyboardButton("📱 Open Community App")],
        [KeyboardButton("🛠️ Admin Panel")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Protidin Kaj এ স্বাগতম! নিচ থেকে বাটন চাপো:", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Balance" in text:
        await update.message.reply_text("💰 আপনার ব্যালেন্স: ৳0")
    elif "Referrals" in text:
        await update.message.reply_text("👥 মোট রেফার: ০ জন")
    elif "Refer Link" in text:
        user_id = update.effective_user.id
        await update.message.reply_text(f"🔗 আপনার রেফার লিংক:\nhttps://t.me/ProtidinKaj_bot?start={user_id}")
    elif "Withdraw" in text:
        await update.message.reply_text("💳 মিনিমাম উইথড্র ৫০০ টাকা। ব্যালেন্স কম আছে।")
    elif "Daily Bonus" in text:
        await update.message.reply_text("🎁 Daily Bonus: ৳10 পেয়েছেন! (Demo)")
    elif "Community Task" in text or "Open Community" in text:
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🚀 App Open করো", web_app=WebAppInfo(url=WEB_URL))]])
        await update.message.reply_text("👇 নিচে App Open এ চাপ দাও:", reply_markup=btn)
    elif "Admin Panel" in text:
        await update.message.reply_text("🛠️ Admin Panel: শুধু এডমিনের জন্য।")
    else:
        await update.message.reply_text("বাটন থেকে সিলেক্ট করুন")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
