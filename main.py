from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Protidin Kaj</title>
<style>
body{margin:0;background:#e8f8f6;font-family:Arial,sans-serif;padding-bottom:80px}
.head{background:#0a7a6d;color:white;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;font-weight:bold}
.card{background:white;margin:12px;border-radius:18px;padding:16px;box-shadow:0 2px 8px #0001}
.green{background:#0f8a7c;color:white;border-radius:20px;padding:20px;text-align:center;margin:12px}
.btn{background:#0a8a6e;color:white;border:none;width:100%;padding:14px;border-radius:12px;font-weight:bold;font-size:16px}
.inp{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;box-sizing:border-box}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #ddd;z-index:10}
.bottom div{text-align:center;font-size:13px}
</style>
</head>
<body>
<div class="head">
<div>☰ SHIBLI NOMAN</div>
<div>705.00 TK</div>
</div>

<div class="card">
<b>Refer Link</b><br><br>
<input class="inp" value="https://t.me/ProtidinerKaj_BD_Bot?start=123"><br><br>
<button class="btn">Share Refer Link</button>
</div>

<div class="card" style="background:#0a3d38;color:white;line-height:1.8">
<b>Official Notice</b><br>
- Per Refer 110 TK<br>
- Per Ad 15 TK<br>
- Min Withdraw 1000 TK<br>
- 5% Bonus on 20 Refer
</div>

<div class="green">
<div style="opacity:0.9">Your Balance</div>
<h1 style="font-size:48px;margin:10px 0">15.00 TK</h1>
<p>Per Ad Income</p>
<div style="background:#ffffff22;padding:14px;border-radius:14px;margin-top:15px;font-weight:bold">▶ Start Ad</div>
</div>

<div class="bottom">
<div>🏠<br>Home</div>
<div>💰<br>Earn</div>
<div>💬<br>Support</div>
<div>🏦<br>Withdraw</div>
<div>👤<br>Profile</div>
</div>

</body>
</html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
