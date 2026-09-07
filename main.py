from flask import Flask, render_template
import os
import threading
from bot import application
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run_bot():
    asyncio.run(application.run_polling())

if __name__ == '__main__':
    # বট আলাদা থ্রেডে চালু হবে
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
