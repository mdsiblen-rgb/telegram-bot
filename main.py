import os, json, asyncio
from flask import Flask, request, render_template_string
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = "ProtidinerKaj_BD_Bot"

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# Database
DB_FILE = "database.json"
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)
def get_user(user_id):
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {
            "balance": 705.0,
            "diamonds": 397,
            "total_withdraw": 0,
            "today_income": 315.0,
            "yesterday_income": 400.0,
            "total_ads": 37,
            "total_refer": 0,
            "today_ads": 21
        }
        save_db(db)
    return db[uid]

# HTML TEMPLATE - PROFESSIONAL DIAMOND THEME
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{font-family:'Hind Siliguri', sans-serif; background:#f0f4f8;}</style>
</head>
<body class="pb-20">
<!-- HEADER -->
<div class="bg-[#0F172A] text-white p-4 flex justify-between items-center sticky top-0 z-50">
    <div class="flex items-center gap-3">
        <img src="https://i.ibb.co/3mQ6b2X/logo.png" class="w-10 h-10 rounded-full bg-white">
        <div>
            <p class="font-bold text-sm">SHIBLI NOMAN</p>
            <p class="text-[12px] text-yellow-400">৳{{user.balance}} | 💎 {{user.diamonds}} Diamond</p>
        </div>
    </div>
    <div class="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center">✓</div>
</div>

{% if page == 'profile' %}
<!-- PROFILE PAGE - তোমার ছবির মতো -->
<div class="m-4">
    <div class="bg-gradient-to-r from-[#0F172A] to-[#1E3A8A] rounded-[20px] p-5 text-white flex items-center gap-4">
        <img src="https://i.ibb.co/3mQ6b2X/logo.png" class="w-16 h-16 rounded-full border-2 border-yellow-400 bg-white">
        <div>
            <h2 class="font-bold text-lg">SHIBLI NOMAN</h2>
            <p class="text-sm opacity-80">@ShibliNoman_BD</p>
            <span class="bg-white/20 px-3 py-1 rounded-full text-xs mt-1 inline-block">💎 ID: 8807178385</span>
        </div>
    </div>
    <div class="bg-gradient-to-r from-[#1E3A8A] to-[#0F172A] rounded-[16px] p-4 mt-4 flex justify-between text-white">
        <span>💼 বর্তমান ব্যালেন্স</span><span class="font-bold text-xl">৳{{user.balance}}</span>
    </div>
    <div class="bg-gradient-to-r from-yellow-500 to-amber-600 rounded-[16px] p-4 mt-3 flex justify-between text-white">
        <span>💎 ডায়মন্ড ব্যালেন্স</span><span class="font-bold text-xl">{{user.diamonds}} 💎</span>
    </div>
    <div class="grid grid-cols-2 gap-3 mt-4">
        <div class="bg-white rounded-[14px] p-3 shadow"><p class="text-xs text-gray-500">📅 আজকের মোট আয়</p><p class="font-bold text-[#0F172A]">৳{{user.today_income}}</p></div>
        <div class="bg-white rounded-[14px] p-3 shadow"><p class="text-xs text-gray-500">📅 গতকালের আয়</p><p class="font-bold">৳{{user.yesterday_income}}</p></div>
        <div class="bg-white rounded-[14px] p-3 shadow"><p class="text-xs text-gray-500">▶ মোট বিজ্ঞাপন দেখেছেন</p><p class="font-bold text-blue-600">{{user.total_ads}} টি</p></div>
        <div class="bg-white rounded-[14px] p-3 shadow"><p class="text-xs text-gray-500">👥 মোট রেফার</p><p class="font-bold text-amber-500">{{user.total_refer}} জন</p></div>
    </div>
</div>
{% elif page == 'withdraw' %}
<!-- WITHDRAW PAGE -->
<div class="bg-gradient-to-br from-[#0F172A] to-[#1E3A8A] rounded-b-[30px] p-8 text-center text-white">
    <p class="opacity-80">আপনার ব্যালেন্স</p>
    <h1 class="text-4xl font-bold mt-1">৳{{user.balance}}</h1>
    <div class="flex gap-2 justify-center mt-3"><span class="bg-white/20 px-3 py-1 rounded-full text-xs">মিনিমাম: ৳1,000.00</span><span class="bg-white/20 px-3 py-1 rounded-full text-xs">💎 {{user.diamonds}} Diamond</span></div>
</div>
<div class="bg-white m-4 rounded-[20px] p-4 shadow">
    <h3 class="font-bold text-[#0F172A]">💎 টাকা উত্তোলন - Diamond to TK</h3>
    <p class="text-xs text-gray-500">১০০ Diamond = ৳১৮.০০ - BKash / Nagad এ পেমেন্ট পান</p>
    <div class="grid grid-cols-2 gap-3 mt-4">
        <div class="border-2 border-[#0F172A] rounded-xl p-3 text-center"><img src="https://upload.wikimedia.org/wikipedia/commons/f/f7/BKash_Logo.png" class="h-8 mx-auto"><p class="text-xs mt-2 text-[#0F172A] font-bold">✓ Selected</p></div>
        <div class="border rounded-xl p-3 text-center opacity-60"><img src="https://seeklogo.com/images/N/nagad-logo-0E8A5C0B3A-seeklogo.com.png" class="h-8 mx-auto"><p class="text-xs mt-2">Tap to select</p></div>
    </div>
</div>
{% else %}
<!-- EARN PAGE -->
<div class="bg-gradient-to-r from-[#0F172A] to-[#1E3A8A] m-4 rounded-[20px] p-6 text-white text-center">
    <p class="text-sm opacity-80">প্রতি বিজ্ঞাপনে নিশ্চিত আয়</p>
    <h1 class="text-5xl font-bold my-2">💎 10</h1>
    <p class="text-yellow-400">= ৳18.00</p>
    <div class="grid grid-cols-2 gap-3 mt-5">
        <div class="bg-white/10 rounded-xl p-3"><p class="text-xs">আজকের বিজ্ঞাপন দেখা</p><p class="font-bold text-lg">{{user.today_ads}} টি</p></div>
        <div class="bg-white/10 rounded-xl p-3"><p class="text-xs">আজকের ডায়মন্ড আয়</p><p class="font-bold text-lg">💎 {{user.today_ads * 10}}</p></div>
    </div>
    <button onclick="watchAd()" class="w-full bg-gradient-to-r from-yellow-400 to-amber-500 text-black font-bold py-3 rounded-xl mt-4">▶ বিজ্ঞাপন দেখুন ও ডায়মন্ড জিতুন</button>
</div>
{% endif %}

<!-- BOTTOM NAV -->
<div class="fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-2">
    <a href="/?page=home" class="text-center"><div>🏠</div><p class="text-xs">হোম</p></a>
    <a href="/?page=earn" class="text-center"><div>📋</div><p class="text-xs">আয় করুন</p></a>
    <a href="/?page=support" class="text-center"><div>❓</div><p class="text-xs">সাপোর্ট</p></a>
    <a href="/?page=withdraw" class="text-center"><div>💳</div><p class="text-xs">উইথড্র</p></a>
    <a href="/?page=profile" class="text-center text-blue-600"><div>👤</div><p class="text-xs">প্রোফাইল</p></a>
</div>

<script>
function watchAd(){
    alert('বিজ্ঞাপন দেখা হচ্ছে... ১০ 💎 যোগ হবে!');
    fetch('/api/add_diamond?uid=108365').then(()=>location.reload());
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    uid = request.args.get('uid', '108365')
    page = request.args.get('page', 'profile')
    user = get_user(uid)
    return render_template_string(HTML, user=user, page=page)

@app.route('/api/add_diamond')
def add_diamond():
    uid = request.args.get('uid', '108365')
    db = load_db()
    user = get_user(uid)
    user['diamonds'] += 10
    user['balance'] += 18.0
    user['total_ads'] += 1
    user['today_ads'] += 1
    user['today_income'] += 18.0
    db[str(uid)] = user
    save_db(db)
    return {"status": "ok", "diamonds": user['diamonds']}

# Telegram Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 App Open করুন", reply_markup={
        "inline_keyboard": [[{"text": "💎 Open Diamond App", "web_app": {"url": "https://telegram-bot-1-v77g.onrender.com"}}]]
    })

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    # telegram webhook
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
