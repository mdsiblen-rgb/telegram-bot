import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# তোমার বটের টোকেন এখানে বসাও
BOT_TOKEN = "8851083480:AAGdSjS3mN9-lH8Wf3b49-ZQzlzJPHtsqEQ"
WEBAPP_URL = "https://telegram-bot-1-v77g.onrender.com"

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Protidin Kaj</title>
<style>
body{margin:0;background:#e8f8f6;font-family:Arial;padding-bottom:90px}
.head{background:#0a7a6d;color:white;padding:14px 16px;display:flex;justify-content:space-between;font-weight:bold;position:sticky;top:0}
.card{background:white;margin:12px;border-radius:18px;padding:16px;box-shadow:0 2px 8px #0001}
.green{background:linear-gradient(135deg,#0f8a7c,#0a6a5c);color:white;border-radius:20px;padding:20px;text-align:center;margin:12px}
.btn{background:#0a8a6e;color:white;border:none;width:100%;padding:14px;border-radius:12px;font-weight:bold;font-size:16px;cursor:pointer}
.inp{width:100%;padding:12px;border-radius:10px;border:1px solid #ddd;box-sizing:border-box}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #ddd}
.bottom div{text-align:center;font-size:13px;cursor:pointer;opacity:0.6}
.bottom div.active{opacity:1;color:#0a7a6d;font-weight:bold}
.page{display:none}.page.active{display:block}
</style></head><body>
<div class="head"><div>☰ SHIBLI NOMAN</div><div><span id="topBal">705.00</span> TK</div></div>
<div id="homePage" class="page active">
<div class="card"><b>Refer Link</b><br><br><input class="inp" id="refLink" value="https://t.me/ProtidinerKaj_BD_Bot?start=123"><br><br><button class="btn" onclick="shareRef()">Share Refer Link</button></div>
<div class="card" style="background:#0a3d38;color:white;line-height:1.8"><b>Official Notice</b><br>- Per Refer 110 TK<br>- Per Ad 15 TK<br>- Min Withdraw 1000 TK<br>- 5% Bonus on 20 Refer</div>
<div class="green"><div>Your Balance</div><h1 style="font-size:42px;margin:10px 0"><span id="bal">15.00</span> TK</h1><div style="background:#ffffff22;padding:14px;border-radius:14px;margin-top:15px;font-weight:bold" onclick="startAd()">▶ Start Ad</div></div>
</div>
<div id="earnPage" class="page"><div class="card" style="text-align:center"><h2>Daily Tasks</h2></div><div class="card" style="text-align:center"><h3>Watch Ad - 15 TK</h3><button class="btn" onclick="startAd()">Watch Now</button></div></div>
<div id="withdrawPage" class="page"><div class="green"><h1><span id="bal2">15.00</span> TK</h1></div><div class="card"><select class="inp"><option>bKash</option><option>Nagad</option></select><br><br><input class="inp" placeholder="Number"><br><br><input class="inp" placeholder="Amount"><br><br><button class="btn" onclick="alert('Min 1000 TK')">Withdraw</button></div></div>
<div id="profilePage" class="page"><div class="card" style="text-align:center"><h2>👤 SHIBLI NOMAN</h2><p>Total Earning: <span id="bal3">15.00</span> TK</p></div></div>
<div class="bottom">
<div id="b_home" class="active" onclick="openPage('homePage','b_home')">🏠<br>Home</div>
<div onclick="openPage('earnPage','b_earn')" id="b_earn">💰<br>Earn</div>
<div onclick="openPage('withdrawPage','b_withdraw')" id="b_withdraw">🏦<br>Withdraw</div>
<div onclick="openPage('profilePage','b_profile')" id="b_profile">👤<br>Profile</div>
</div>
<script>
let balance=15; let topBal=705;
function openPage(p,b){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById(p).classList.add('active');document.querySelectorAll('.bottom div').forEach(x=>x.classList.remove('active'));document.getElementById(b).classList.add('active')}
function shareRef(){let l=document.getElementById('refLink').value;navigator.clipboard.writeText(l);alert('Link Copied: '+l)}
function startAd(){let btn=event.target;btn.innerHTML='⏳ 5s...';let s=5;let t=setInterval(()=>{s--;btn.innerHTML='⏳ '+s+'s...';if(s<=0){clearInterval(t);balance+=15;topBal+=15;document.getElementById('bal').innerText=balance.toFixed(2);document.getElementById('bal2').innerText=balance.toFixed(2);document.getElementById('bal3').innerText=balance.toFixed(2);document.getElementById('topBal').innerText=topBal.toFixed(2);btn.innerHTML='✅ 15 TK Added!';setTimeout(()=>btn.innerHTML='▶ Start Ad',2000)}},1000)}
</script></body></html>
    """

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💰 Open App", web_app=WebAppInfo(url=WEBAPP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Protidin Kaj এ স্বাগতম! নিচের বাটনে চাপ দাও 👇", reply_markup=reply_markup)

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_bot()
