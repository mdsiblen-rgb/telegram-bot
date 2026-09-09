import telebot
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    args = msg.text.split()
    if len(args) > 1 and args[1].startswith("invite_"):
        inviter_id = args[1].split("_")[1]
        print(f"User {msg.from_user.id} invited by {inviter_id}")
        # এখানে ডাটাবেসে সেভ করো
    bot.send_message(msg.chat.id, "Welcome! Mini App open করো")

bot.infinity_polling()
