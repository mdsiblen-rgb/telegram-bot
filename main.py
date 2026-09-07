from flask import Flask
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Protidin Kaj - Diamond System</title>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Hind Siliguri',sans-serif}
body{background:#eef7f5;padding-bottom:80px}
.top{background:linear-gradient(135deg,#0f766e,#14b8a6);color:#fff;padding:18px;display:flex;justify-content:space-between;align-items:center}
.card{margin:12px;border-radius:18px;padding:16px;color:white;box-shadow:0 6px 16px rgba(0,0,0,0.15)}
.c1{background:linear-gradient(135deg,#059669,#10b981)}
.c2{background:linear-gradient(135deg,#0e9488,#14b8a6);text-align:center}
.c2 h1{font-size:38px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px}
.item{background:white;border-radius:16px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,0.07)}
.btn{background:white;color:#0f766e;border:none;width:100%;padding:14px;border-radius:12px;font-weight:800;margin-top:12px;font-size:16px}
.nav{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:12px 0;box-shadow:0 -2px 12px rgba(0,0,0,0.1)}
.active{color:#0f766e;font-weight:800}
</style>
</head>
<body>
<div class="top">
 <div>💎 <b>SHIBLI NOMAN</b><br><small>৳705.00 | Diamond: 715 💎</small></div>
 <div>ID: 8807178385</div>
</div>
<div class="card c1"><div>💼 বর্তমান ব্যালেন্স</div><div style="font-size:28px;font-weight:900">৳715.00</div></div>
<div class="card c2">
 <div>প্রতি বিজ্ঞাপনে নিশ্চিত আয় + ডায়মন্ড</div>
 <h1>৳18.00 💎</h1>
 <div style="display:flex;gap:8px;margin-top:10px"><div style="flex:1;background:rgba(255,255,255,0.25);border-radius:12px;padding:10px">আজ দেখেছেন<br><b>0 টি</b></div><div style="flex:1;background:rgba(255,255,255,0.25);border-radius:12px;padding:10px">আজ আয়<br><b>৳0.00</b></div></div>
 <button class="btn">▶ বিজ্ঞাপন শুরু করুন</button>
</div>
<div class="grid">
 <div class="item">📅 আজকের আয়<br><b style="color:#059669;font-size:20px">৳0.00</b></div>
 <div class="item">📅 গতকালের আয়<br><b style="font-size:20px">৳315.00</b></div>
 <div class="item">▶ মোট বিজ্ঞাপন<br><b style="font-size:20px">37 টি</b></div>
 <div class="item">👥 মোট রেফার<br><b style="font-size:20px;color:orange">0 জন</b></div>
</div>
<div class="nav"><div class="active">🏠 হোম</div><div>📄 আয়</div><div>❓ সাপোর্ট</div><div>💳 উইথড্র</div><div>👤 প্রোফাইল</div></div>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
