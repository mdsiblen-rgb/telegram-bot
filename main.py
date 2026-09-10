from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - FINAL V7</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;font-family:'Hind Siliguri',sans-serif}body{margin:0;background:#f5f3ff;padding-bottom:110px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:0 0 22px 22px;position:sticky;top:0;z-index:20}
.card{background:#fff;margin:12px;border-radius:18px;padding:16px;box-shadow:0 6px 18px #0001}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer}
.btn:disabled{opacity:0.5}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:10px;left:10px;right:10px;background:#fff;display:flex;justify-content:space-around;padding:12px 0;border-radius:22px;box-shadow:0 10px 30px #0003;z-index:50}
.nav div{flex:1;text-align:center;font-size:11px;opacity:0.45;cursor:pointer}.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
#adOverlay,#welcomeOverlay{display:none;position:fixed;inset:0;background:#000c;z-index:200;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:14px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
.logo-box{width:62px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#fff;flex-shrink:0}
.bkash-bg{background:#e2136e} .nagad-bg{background:#f6921e}
input{width:100%;padding:14px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px;outline:none}
input:focus{border-color:#8b5cf6}
</style></head><body>

<div class="header" style="display:flex;justify-content:space-between;align-items:center">
<div><b style="font-size:18px">💎 Protidiner Kaj BD</b><div style="font-size:11px;opacity:0.9">Pro • Trusted • Admin: 8807178385</div></div>
<div id="adBadge" style="background:#fff2;padding:7px 14px;border-radius:20px;font-size:12px;font-weight:700">Ad: 20</div>
</div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between;align-items:center">
<div><div style="opacity:0.85;font-size:12px">আপনার ব্যালেন্স</div><div id="balMain" style="font-size:36px;font-weight:800">0 TK</div><div style="font-size:11px;background:#fff2;padding:4px 10px;border-radius:20px;display:inline-block;margin-top:4px">ID: 8807178385 • Active</div></div>
<img id="topPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:72px;height:72px;border-radius:50%;background:#fff;object-fit:cover">
</div>

<!-- WELCOME 10 TK ONLY FIRST JOIN -->
<div id="welcomeOverlay" style="background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2);z-index:300">
<div style="background:#fff;color:#000;padding:24px;border-radius:22px;width:92%;max-width:360px;text-align:center;box-shadow:0 20px 40px #0004">
<div style="font-size:62px">🎉</div>
<h2 style="margin:8px 0 0;color:#6d28d9">স্বাগতম!</h2>
<p style="margin:4px 0;color:#666;font-size:13px">Protidiner Kaj BD তে আপনাকে স্বাগতম</p>
<div style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:16px;font-size:32px;font-weight:800;margin:14px 0">10 TK বোনাস 💰</div>
<p style="font-size:11px;color:#666;line-height:1.4">প্রথম জয়েনের জন্য 10 TK বোনাস পেয়েছেন<br>এটা শুধু একবারই পাবেন, প্রতিদিন নয়</p>
<button class="btn purple" style="margin-top:14px" onclick="closeWelcome()">🚀 কাজ শুরু করুন</button>
</div>
</div>

<!-- HOME -->
<div id="p-home" class="page active">
<div class="card">
<div style="display:flex;justify-content:space-between"><h3 style="margin:0">🎬 বিজ্ঞাপন দেখুন</h3><span style="font-size:11px;background:#fef3c7;padding:4px 8px;border-radius:8px">2 TK / Ad</span></div>
<button id="adBtn" class="btn purple" style="margin-top:14px" onclick="watchAd()">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button>
<div style="background:#ede9fe;height:10px;border-radius:20px;margin-top:14px;overflow:hidden"><div id="adProg" style="background:#6d28d9;height:100%;width:100%"></div></div>
<p id="adText" style="text-align:right;font-size:12px;color:#666;margin:6px 0 0">20/20 বাকি</p>
</div>
<div class="card">
<h3 style="margin:0 0 10px">🔗 আপনার রেফার লিংক - 10 TK পাবেন</h3>
<div id="refLink" style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:13px"></div>
<div style="display:flex;gap:10px;margin-top:12px"><button class="btn" style="background:#fbbf24;flex:1" onclick="copyRef()">📋 কপি</button><button class="btn" style="background:#0ea5e9;color:#fff;flex:1" onclick="shareRef()">📤 শেয়ার</button></div>
</div>
</div>

<!-- TASKS -->
<div id="p-tasks" class="page">
<div class="card">
<h3 style="margin:0 0 12px">🎯 ডেইলি টাস্ক</h3>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #f1f1f1"><div><b>🎁 ডেইলি চেক-ইন</b><div style="font-size:12px;color:#666" id="checkStatus">প্রতিদিন 5 TK</div></div><button id="checkBtn" class="btn purple" style="width:auto;padding:8px 18px" onclick="doCheck()">5 TK</button></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #f1f1f1"><div><b>🎬 10 টা Ad দেখুন</b><div style="font-size:12px;color:#666" id="taskAd">0/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff;padding:8px 16px" onclick="go('home')">যান</button></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0"><div><b>👥 3 জনকে Invite</b><div style="font-size:12px;color:#666">প্রতি Invite 10 TK</div></div><button class="btn" style="width:auto;background:#10b981;color:#fff;padding:8px 16px" onclick="go('invite')">Invite</button></div>
</div>
</div>

<!-- INVITE -->
<div id="p-invite" class="page"><div class="card" style="background:linear-gradient(135deg,#6
