from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daily Earn</title>
<style>
body { background:#000; color:#fff; text-align:center; font-family:sans-serif; padding-top:50px; }
.diamond { width:120px; height:120px; background:linear-gradient(135deg,#00d4ff,#0066ff); transform:rotate(45deg); margin:0 auto; box-shadow:0 0 30px #00d4ff; border-radius:20px; }
h1 { margin-top:80px; }
.btn { background:#00aaff; padding:15px 30px; border:none; border-radius:10px; color:white; font-size:18px; margin-top:30px; }
</style>
</head>
<body>
<div class="diamond"></div>
<h1>💎 Protodin Kaj 💎</h1>
<p>Telegram Login Bot is Live!</p>
<button class="btn" onclick="window.Telegram.WebApp.close()">Open Telegram</button>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
