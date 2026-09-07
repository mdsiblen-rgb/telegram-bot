from flask import Flask, render_template
import threading
import asyncio
import bot

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run_bot():
    asyncio.run(bot.application.run_polling())

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
