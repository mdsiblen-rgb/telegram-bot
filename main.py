import os
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN not found in Environment!")
    exit(1)

# Token ঠিক আছে কিনা চেক
BOT_TOKEN = BOT_TOKEN.strip()
print(f"Token loaded, has colon: {':' in BOT_TOKEN}")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    try:
        args = msg.text.split()
        inviter_id = None

        # রেফারেল চেক: /start 123_456 বা /start_123
        if len(args) > 1 and args[1].startswith("ref_"):
            inviter_id = args[1].split("_")[1]
            print(f"User {msg.from_user.id} invited by {inviter_id}")
            # এখানে ডাটাবেসে সেভ করো
        elif "_" in args[0]:
            # t.me/bot?start=123_456 এই ফরম্যাটের জন্য
            try:
                inviter_id = args[0].split("_")[1]
                print(f"User {msg.from_user.id} invited by {inviter_id}")
            except:
                pass

        if inviter_id:
            bot.send_message(msg.chat.id, f"Welcome! 🎉\nYou were invited by user {inviter_id}")
        else:
            bot.send_message(msg.chat.id, "Welcome! 🎉\nSend your referral link: t.me/your_bot?start=ref_" + str(msg.from_user.id))

    except Exception as e:
        print(f"Error in start: {e}")
        bot.send_message(msg.chat.id, "Welcome!")

print("Bot is running...")
bot.infinity_polling()
