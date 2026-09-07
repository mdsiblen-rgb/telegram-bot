import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8851083480:AAFmYq35DcAH7jPpMj_Y9ANLI7iI5AnCvq4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_url = "https://telegram-bot-1-k77g.onrender.com"

    keyboard = [
        [InlineKeyboardButton("🚀 App Open করো", web_app=web_app_url)],
        [InlineKeyboardButton("📢 পেমেন্ট চ্যানেল", url="https://t.me/tap2earn_real_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 **COMMUNITY TASK এ স্বাগতম!**\n"
        "✅ প্রতি বিজ্ঞাপনে ১৫ টাকা\n"
        "✅ প্রতি রেফারে ১১০ টাকা\n"
        "নিচে App Open এ চাপ দাও",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
