from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="font-family:sans-serif; text-align:center; padding:20px;">
    <h1>✅ Bot is LIVE!</h1>
    <p>Template Error Fixed!</p>
    <p>Monetag Zone: 11760259 Connected</p>
    <br>
    <script src='//libtl.com/sdk.js' data-zone='11760259' data-sdk='show_11760259'></script>
    <button onclick="show_11760259()" style="padding:15px 30px; background:green; color:white; border:none; border-radius:10px; font-size:18px;">📺 Ad দেখো (Test)</button>
    <br><br>
    <a href="/admin">Admin Panel</a>
    </body>
    </html>
    """

@app.route("/admin")
def admin():
    return "<h2>Admin Panel V11 - Working</h2><p>Real users will show here after fix</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
