from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

@bot.message_handler(func=lambda m: m.text == "🌐 Community Task")
def community_task(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏢 Open Company App", web_app=WebAppInfo(url="https://telegram-bot-1-v77g.onrender.com")))
    bot.send_message(m.chat.id, "✅ নিচে কোম্পানি Mini App ওপেন করুন:\n\n১ রেফার = ৫ টাকা\n১০০ টাকায় উইথড্র\n\n👇 Open App এ ক্লিক করুন", reply_markup=markup)
