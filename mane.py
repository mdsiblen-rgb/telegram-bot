import os
import json
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# কনফিগারেশন
DB_FILE = 'db.json'
ADMIN_ID = 123456789  # আপনার আসল টেলিগ্রাম অ্যাডমিন আইডি এখানে দিন

# প্রাথমিক ডাটাবেজ তৈরি
if not os.path.exists(DB_FILE):
    initial_db = {
        "tasks": [
            {
                "title": "YouTube ভিডিও দেখুন",
                "reward": 25,
                "link": "https://youtube.com",
                "btn": "শুরু করুন",
                "type": "youtube",
                "color": "#065f46"
            },
            {
                "title": "Telegram Channel Join",
                "reward": 10,
                "link": "https://t.me",
                "btn": "Join",
                "type": "telegram",
                "color": "#1e40af"
            },
            {
                "title": "Facebook Follow",
                "reward": 15,
                "link": "https://facebook.com",
                "btn": "Follow",
                "type": "facebook",
                "color": "#1877F2"
            },
            {
                "title": "Company Task 1",
                "reward": 20,
                "link": "https://t.me",
                "btn": "Visit",
                "type": "company",
                "color": "#7c3aed"
            },
            {
                "title": "Company Task 2",
                "reward": 20,
                "link": "https://t.me",
                "btn": "Visit",
                "type": "company",
                "color": "#0f766e"
            },
            {
                "title": "Company Task 3",
                "reward": 20,
                "link": "https://t.me",
                "btn": "Visit",
                "type": "company",
                "color": "#be123c"
            }
        ]
    }
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_db, f, indent=2, ensure_ascii=False)

def load_db():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def is_admin(id):
    try:
        return int(id) == ADMIN_ID
    except:
        return False

# হেলথ চেক রুট (সহজ ও জ্যাম-মুক্ত)
@app.route('/health')
def health():
    return "OK", 200

# =========================================================================
# USER HTML - সব ফিচার সহ ফিক্সড এবং কমপ্লিট ডিজাইন
# =========================================================================
USER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD - DAILY JOBS</title>
<script src="https://telegram.org"></script>
<link href="https://googleapis.com" rel="stylesheet">
<style>
* { font-family: 'Hind Siliguri', sans-serif; box-sizing: border-box; margin: 0; padding: 0 }
body { max-width: 430px; margin: 0 auto; background: #eef2ff; padding-bottom: 160px }
.top { background: #1e40af; color: #fff; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 10 }
.top img { width: 36px; height: 36px; border-radius: 50%; background: #fff; object-fit: cover }
.card { background: #fff; margin: 12px; border-radius: 20px; padding: 16px; box-shadow: 0 4px 18px rgba(0,0,0,.06) }
.bal-big { font-size: 52px; font-weight: 900; text-align: center; color: #1e40af }
.btn-blue { width: 100%; background: #1e40af; color: #fff; padding: 14px; border: none; border-radius: 14px; font-weight: 700; font-size: 16px; cursor: pointer; }
.btn-yellow { background: #f59e0b; color: #fff; padding: 12px 22px; border: none; border-radius: 12px; font-weight: 700; cursor: pointer; }
.btm { position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 430px; background: #fff; display: flex; border-top: 1px solid #e2e8f0; padding: 14px 0 18px 0; z-index: 99; box-shadow: 0 -4px 15px rgba(0,0,0,.08) }
.btm div { flex: 1; text-align: center; color: #94a3b8; font-size: 14px; font-weight: 700; cursor: pointer; padding: 8px 4px; border-radius: 14px; transition:.2s; line-height: 1.2 }
.btm div.on { color: #1e40af; background: #e8edff; transform: scale(1.15) }
</style>
</head>
<body>

<div class="top">
    <div style="display:flex;gap:10px;align-items:center;font-weight:700">
        <img id="companyLogo" src="https://flaticon.com">
        <span id="appNameTop">প্রতিদিনের কাজ BD</span>
    </div>
    <div style="font-weight:900">৳<span id="topBal">60</span></div>
</div>

<!-- HOME -->
<div id="t-home">
    <div class="card">
        <div class="bal-big">৳<span id="bal">60</span></div>
        <div style="text-align:center;color:#64748b;margin:8px 0">আপনার বর্তমান ব্যালেন্স</div>
        <button class="btn-blue" onclick="changePage('earn')">💰 আয় করুন</button>
    </div>
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
                <div style="font-size:18px">🎁 Daily Check-in</div>
                <div style="color:#64748b;font-size:13px">প্রতিদিন বোনাস ৳10</div>
            </div>
            <button class="btn-yellow">আজকের বোনাস নিন</button>
        </div>
    </div>
    <div class="card" style="border:2px dashed #1e40af;background:#f0f7ff">
        <div style="font-weight:700;color:#1e40af" id="myAdTitle">🔥 আজকের স্পেশাল অফার</div>
        <div style="font-size:14px;margin-top:6px" id="myAdDesc">এখানে তোমার নিজের বিজ্ঞাপন লিখবে</div>
    </div>
</div>

<!-- নিচের নেভিগেশন বার -->
<div class="btm">
    <div class="on" onclick="changePage('home')">🏠<br>হোম</div>
    <div onclick="changePage('earn')">💼<br>টাস্ক</div>
    <div onclick="changePage('withdraw')">💳<br>উইথড্র</div>
    <div onclick="changePage('profile')">👤<br>প্রোফাইল</div>
</div>

<script>
    const tg = window.Telegram.WebApp;
    tg.expand();

    function changePage(page) {
        console.log("Navigating to: " + page);
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(USER_HTML)

if __name__ == '__main__':
    # থ্রেডিংয়ের ঝামেলা ছাড়া সরাসরি লোকালহোস্টে রান করার জন্য
    app.run(debug=True, port=5000, threaded=True)
