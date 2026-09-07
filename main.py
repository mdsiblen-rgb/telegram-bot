from flask import Flask
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Protidin Kaj - Professional</title>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Hind Siliguri',sans-serif}
body{background:#e8f5f3}
.header{background:linear-gradient(135deg,#0f766e,#0d9488);color:white;padding:16px;display:flex;align-items:center;justify-content:space-between}
.user-box{display:flex;align-items:center;gap:10px}
.avatar{width:50px;height:50px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px}
.card-green{background:linear-gradient(135deg,#059669,#10b981);color:white;border-radius:16px;padding:16px;margin:12px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 12px rgba(0,0,0,0.15)}
.card-dark-green{background:#065f46;color:white;border-radius:16px;padding:12px 16px;margin:0 12px;display:flex;justify-content:space-between}
.white-card{background:white;border-radius:16px;padding:14px;margin:10px 12px;box-shadow:0 2px 8px rgba(0,0,0,0.06);display:flex;justify-content:space-between;align-items:center}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px}
.small-card{background:white;border-radius:16px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.small-card b{font-size:20px;color:#0f766e}
.diamond{background:linear-gradient(135deg,#0f766e,#14b8a6);color:white;border-radius:18px;padding:18px;margin:12px;text-align:center}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:700;cursor:pointer;margin-top:10px}
.btn-white{background:white;color:#0f766e;font-size:16px}
.bottom{position:fixed;bottom:0;width:100%;background:white;display:flex;justify-content:space-around;padding:10px 0;box-shadow:0 -2px 10px rgba(0,0,0,0.1)}
.bottom div{text-align:center;font-size:12px;color:#64748b}
.bottom .active{color:#0f766e;font-weight:700}
.tag{background:rgba(255,255,255,0.25);padding:4px 10px;border-radius:20px;font-size:12px}
</style>
</head>
<body>
<div class="header">
  <div class="user-box">
    <div class="avatar">💎</div>
    <div>
      <div style="font-weight:700">SHIBLI NOMAN</div>
      <div>৳705.00 <span style="font-size:12px">● Diamond: 715</span></div>
    </div>
  </div>
  <div style="font-size:20px">⋮</div>
</div>

<div style="background:#0f766e;color:white;padding:10px 16px;display:flex;gap:10px;align-items:center">
  <img src="https://i.ibb.co/4W2yZJ5/logo.png" style="width:40px;height:40px;border-radius:50%;background:white">
  <div>
    <div style="font-weight:700">SHIBLI NOMAN</div>
    <div style="font-size:13px;opacity:0.9">@ShibliNoman_BD | ID: 8807178385</div>
  </div>
</div>

<div class="card-green">
  <div>💼 বর্তমান ব্যালেন্স<br><small style="opacity:0.8">Diamond Balance</small></div>
  <div style="font-size:26px;font-weight:800">৳715.00</div>
</div>

<div class="card-dark-green" style="background:linear-gradient(135deg,#0e7a6b,#149b8a)">
  <div>✅ মোট সফল উইথড্র</div>
  <div style="font-size:22px;font-weight:700">৳0.00</div>
</div>

<div class="diamond">
  <div style="opacity:0.9">প্রতি বিজ্ঞাপনে নিশ্চিত আয় + ডায়মন্ড</div>
  <div style="font-size:42px;font-weight:900;margin:8px 0">৳18.00 💎</div>
  <div style="display:flex;gap:10px;margin-top:10px">
    <div style="flex:1;background:rgba(255,255,255,0.2);border-radius:12px;padding:10px">
      আজকের বিজ্ঞাপন দেখা<br><b style="font-size:22px">0 টি</b>
    </div>
    <div style="flex:1;background:rgba(255,255,255,0.2);border-radius:12px;padding:10px">
      আজকের বিজ্ঞাপন আয়<br><b style="font-size:22px">৳ 0.00</b>
    </div>
  </div>
  <button class="btn btn-white">▶ বিজ্ঞাপন শুরু করুন (15 টি বাকি | আজ 0/15)</button>
</div>

<div class="grid">
  <div class="small-card">📅 আজকের মোট আয়<br><b style="color:#059669">৳0.00</b></div>
  <div class="small-card">📅 গতকালের আয়<br><b style="color:#000">৳315.00</b></div>
  <div class="small-card">▶ মোট বিজ্ঞাপন দেখেছেন<br><b>37 টি</b></div>
  <div class="small-card">👥 মোট রেফার<br><b style="color:orange">0 জন</b></div>
</div>

<div class="white-card"><span>🪪 ইউজার আইডি</span><span style="color:#0f766e;font-weight:700">108365</span></div>
<div class="white-card"><span>📊 মোট আয়</span><span style="font-weight:700">৳715.00</span></div>

<div style="display:flex;gap:10px;margin:12px">
  <div style="flex:1;background:#134e4a;color:white;border-radius:12px;padding:12px;text-align:center">🕒 আয়ের ইতিহাস</div>
  <div style="flex:1;background:#f59e0b;color:white;border-radius:12px;padding:12px;text-align:center">📋 Rules</div>
</div>

<br><br><br><br>
<div class="bottom">
  <div class="active">🏠<br>হোম</div>
  <div>📄<br>আয় করুন</div>
  <div>❓<br>সাপোর্ট</div>
  <div>💳<br>উইথড্র</div>
  <div>👤<br>প্রোফাইল</div>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
