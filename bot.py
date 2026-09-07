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
<style>
body{margin:0;background:#e8f8f6;font-family:Arial}
.head{background:#0a7a6d;color:white;padding:15px}
.card{background:white;margin:12px;border-radius:18px;padding:16px}
.green{background:#0f8a7c;color:white;border-radius:20px;padding:20px;text-align:center;margin:12px}
.btn{background:#0a8a6e;color:white;border:none;width:100%;padding:14px;border-radius:12px;font-weight:bold}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px;border-top:1px solid #ddd}
</style>
</head>
<body>
<div class="head">SHIBLI NOMAN - 705.00 TK</div>
<div class="card">Refer Link<br><input style="width:100%;padding:10px" value="https://t.me/ProtidinerKaj_BD_Bot"><br><br><button class="btn">Share Refer Link</button></div>
<div class="card" style="background:#0a3d38;color:white">Official Notice<br>Per Refer 110 TK<br>Per Ad 15 TK<br>1000 TK Withdraw</div>
<div class="green"><h1 style="font-size:50px">15.00 TK</h1><p>Per Ad Income</p><div style="background:#ffffff33;padding:12px;border-radius:12px">Start Ad</div></div>
<div class="bottom"><div>Home</div><div>Earn</div><div>Support</div><div>Withdraw</div><div>Profile</div></div>
</body>
</html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
