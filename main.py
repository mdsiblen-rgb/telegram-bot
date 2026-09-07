import threading
import os
from flask import Flask
import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_bot():
    try:
        if hasattr(bot, 'main'):
            bot.main()
        elif hasattr(bot, 'run'):
            bot.run()
    except Exception as e:
        print(f"Bot error: {e}")

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
