from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

def run_bot():
    try:
        import bot
        print("Telegram bot started...")
    except Exception as e:
        print(f"Bot error: {e}")

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run()
