import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # এখানে তোমার Render এর লিংক বসবে
    web_app_url = "https://telegram-bot-1-4v0v.onrender.com"
    
    keyboard = [
        [InlineKeyboardButton("🚀 App Open করুন", web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton("📢 পেমেন্ট চ্যানেল", url="https://t.me/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 **COMMUNITY TASK এ স্বাগতম!**\n\n"
        "✅ প্রতি বিজ্ঞাপনে ১৫ টাকা\n"
        "✅ প্রতি রেফারে ১১০ টাকা\n"
        "✅ ১০০০ টাকা হলেই উইথড্র\n\n"
        "নিচে App Open এ ক্লিক করুন।",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
