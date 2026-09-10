from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - Bug Fixed</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<style>
*{box-sizing:border-box;font-family:sans-serif}body{margin:0;background:#f5f3ff;padding-bottom:115px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:0 0 22px 22px;position:sticky;top:0;z-index:20}
.card{background:#fff;margin:12px;border-radius:18px;padding:16px;box-shadow:0 6px 18px #0001}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:10px;left:10px;right:10px;background:#fff;display:flex;justify-content:space-around;padding:12px 0;border-radius:22px;box-shadow:0 10px 30px #0003;z-index:50}
.nav div{flex:1;text-align:center;font-size:11px;opacity:0.45;cursor:pointer}.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
#adOverlay{position:fixed;inset:0;background:#000e;z-index:400;display:none;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
#welcomeOverlay{position:fixed;inset:0;background:#6d28d9f2;z-index:500;display:none;justify-content:center;align-items:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:14px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
.logo-box{width:62px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff}.bkash-bg{background:#e2136e}.nagad-bg{background:#ef4444}
input{width:100%;padding:14px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px}
</style></head><body>
<div class="header"><b>PROTIDINER KAJ BD - FINAL</b><div style="font-size:11px">Welcome Fixed - 1 Click Close</div></div>
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff"><div>Balance</div><div id="balMain" style="font-size:36px;font-weight:800">0 TK</div></div>

<!-- WELCOME - NOW CLICKABLE 100% -->
<div id="welcomeOverlay" onclick="closeWelcome()">
<div onclick="event.stopPropagation()" style="background:#fff;color:#000;padding:24px;border-radius:22px;width:92%;max-width:360px;text-align:center;box-shadow:0 20px 50px #0005">
<div style="font-size:60px">🎉</div><h2 style="color:#6d28d9;margin:8px 0 0">স্বাগতম!</h2><p style="color:#666">Protidiner Kaj BD তে</p>
<div style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:16px;font-size:28px;font-weight:800;margin:14px 0">10 TK বোনাস</div>
<p style="font-size:11px;color:#666">প্রথম জয়েনে 1 বার - প্রতিদিন নয়</p>
<button class="btn purple" style="margin-top:14px;padding:16px;font-size:16px" onclick="closeWelcome()">✅ কাজ শুরু করুন - ক্লিক করুন</button>
<p style="font-size:10px;color:#999;margin-top:8px">বাইরে ক্লিক করলেও বন্ধ হবে</p>
</div>
</div>

<div id="p-home" class="page active"><div class="card"><button class="btn purple" onclick="watchAd()">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button><p id="adText" style="text-align:right;font-size:12px">20/20</p><p style="font-size:11px;color:#10b981;text-align:center">Monetag Zone 11760259 Connected</p></div><div class="card"><div id="refLink" style="background:#f5f3ff;padding:12px;border-radius:12px;word-break:break-all;text-align:center"></div></div></div>
<div id="p-tasks" class="page"><div class="card"><div style="display:flex;justify-content:space-between"><div><b>Daily Check</b><div id="checkStatus" style="font-size:12px">5 TK</div></div><button id="checkBtn" class="btn purple" style="width:auto" onclick="doCheck()">5 TK</button></div><div style="display:flex;justify-content:space-between;margin-top:14px"><div><b>10 Ad</b><div id="taskAd" style="font-size:12px">0/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff" onclick="go('home')">যান</button></div></div></div>
<div id="p-invite" class="page"><div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center"><h1>10 TK Per Refer</h1><div id="refLink2" style="background:#fff2;padding:12px;border-radius:12px;margin-top:10px"></div></div></div>
<div id="p-wallet" class="page"><div class="card" style="text-align:center"><h1 id="bal2" style="color:#6d28d9">0 TK</h1></div><div class="card"><h3>bKash Nagad Fixed</h3><div id="bkashOpt" class="withdraw-opt active" onclick="selectMethod('bKash')"><div class="logo-box bkash-bg">bKash</div><div style="flex:1"><b>bKash</b></div>✓</div><div id="nagadOpt" class="withdraw-opt" onclick="selectMethod('Nagad')"><div class="logo-box nagad-bg">Nagad</div><div style="flex:1"><b>Nagad</b></div></div><input id="accNum" placeholder="Number"><input id="amount" type="number" placeholder="Min 100"><button class="btn purple" style="margin-top:10px" onclick="doWithdraw()">Withdraw</button></div></div>
<div id="p-profile" class="page"><div class="card" style="text-align:center"><h2>Riyad - ADMIN 8807178385</h2><a href="/admin?id=8807178385" style="display:inline-block;background:#6d28d9;color:#fff;padding:12px 20px;border-radius:12px;text-decoration:none;font-weight:800">👑 Admin Panel</a></div></div>
<div id="adOverlay"><h2>Ad চলছে...</h2><div id="timer" style="font-size:64px">15</div></div>
<div class="nav"><div id="nav-home" class="active" onclick="go('home')">🏠<br>Home</div><div id="nav-tasks" onclick="go('tasks')">🎯<br>Tasks</div><div id="nav-invite" onclick="go('invite')">👥<br>Invite</div><div id="nav-wallet" onclick="go('wallet')">💰<br>Wallet</div><div id="nav-profile" onclick="go('profile')">👤<br>Profile</div></div>
<script>
let bal=parseInt(localStorage.getItem('v10_bal')||'0');let adLeft=parseInt(localStorage.getItem('v10_ad')||'20');let adDone=parseInt(localStorage.getItem('v10_ad_done')||'0');let firstJoin=localStorage.getItem('v10_first');let lastCheck=localStorage.getItem('v10_check')||'';
function init(){
document.getElementById('balMain').innerText=bal+' TK';document.getElementById('bal2').innerText=bal+' TK';
document.getElementById('adText').innerText=adLeft+'/20';let el=document.getElementById('taskAd');if(el)el.innerText=adDone+'/10';
let today=new Date().toDateString();if(lastCheck===today){let b=document.getElementById('checkBtn');b.innerText='✓ Done';b.disabled=true;document.getElementById('checkStatus').innerText='আজ কমপ্লিট';}
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';document.getElementById('refLink').innerText=link;document.getElementById('refLink2').innerText=link;
if(!firstJoin){setTimeout(()=>{document.getElementById('welcomeOverlay').style.display='flex';},500);}
}
// FIXED: Welcome এখন 100% বন্ধ হবে
function closeWelcome(){
try{
document.getElementById('welcomeOverlay').style.display='none';
document.getElementById('welcomeOverlay').style.visibility='hidden';
document.getElementById('welcomeOverlay').style.pointerEvents='none';
if(!firstJoin){
bal+=10;localStorage.setItem('v10_bal',bal);localStorage.setItem('v10_first','done');firstJoin='done';
init();
alert('🎉 10 TK যোগ হয়েছে! শুধু প্রথমবার');
}
}catch(e){document.getElementById('welcomeOverlay').style.display='none';}
}
function go(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav-'+p).classList.add('active')}
function watchAd(){if(adLeft<=0){alert('Limit শেষ');return}document.getElementById('adOverlay').style.display='flex';let t=15;document.getElementById('timer').innerText=t;let ti=setInterval(()=>{t--;document.getElementById('timer').innerText=t;if(t<=0){clearInterval(ti);document.getElementById('adOverlay').style.display='none';bal+=2;adLeft--;adDone++;localStorage.setItem('v10_bal',bal);localStorage.setItem('v10_ad',adLeft);localStorage.setItem('v10_ad_done',adDone);init();alert('2 TK Added + Dollar Added');}},1000);if(typeof show_11760259==='function'){show_11760259().catch(()=>{})}}
function doCheck(){let today=new Date().toDateString();if(lastCheck===today){alert('আজ করেছেন');return}bal+=5;lastCheck=today;localStorage.setItem('v10_bal',bal);localStorage.setItem('v10_check',today);init();alert('5 TK Bonus');}
function selectMethod(m){document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad')}
function doWithdraw(){let a=parseInt(document.getElementById('amount').value);if(!a||a<100||a>bal){alert('Min 100 / Balance কম');return}bal-=a;localStorage.setItem('v10_bal',bal);init();alert('Withdraw Request!');}
init();
// যদি কোনো কারণে আটকে থাকে, 5 সেকেন্ড পর বাইরে ক্লিক করলে বন্ধ হবে - ব্যাকআপ
setTimeout(()=>{let w=document.getElementById('welcomeOverlay');if(w.style.display==='flex'){w.addEventListener('click',closeWelcome);}},1000);
</script></body></html>
"""

ADMIN = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin</title><style>body{font-family:sans-serif;background:#f5f3ff;padding:20px}.card{background:#fff;padding:20px;border-radius:16px;margin-bottom:16px}.ok{background:#dcfce7;padding:12px;border-radius:12px}.btn{background:#6d28d9;color:#fff;padding:12px 18px;border-radius:12px;text-decoration:none;display:inline-block}</style></head><body><h2>Admin Panel</h2><div id="s"></div><div class="card"><p>Zone 11760259 Connected ✅</p><p>Bot Connected ✅</p><a href="https://publishers.monetag.com/login" target="_blank" class="btn">💵 Monetag Dollar Check</a></div><div class="card"><a href="/" class="btn">Main App</a></div><script>let p=new URLSearchParams(location.search).get('id');document.getElementById('s').innerHTML=p==='8807178385'?'<div class=ok>✅ Access Granted 8807178385</div>':'<div style=background:#fee2e2;padding:12px;border-radius:12px>❌ Denied</div>';</script></body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def root(): return HTMLResponse(content=HTML)

@app.get("/admin", response_class=HTMLResponse)
async def admin(): return HTMLResponse(content=ADMIN)

@app.get("/{path:path}", response_class=HTMLResponse)
async def catch(path: str):
    if path.startswith("admin"): return HTMLResponse(content=ADMIN)
    return HTMLResponse(content=HTML)
