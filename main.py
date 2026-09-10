from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - FINAL V8</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<style>
*{box-sizing:border-box;font-family:sans-serif}
body{margin:0;background:#f5f3ff;padding-bottom:110px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:0 0 22px 22px;position:sticky;top:0;z-index:20}
.card{background:#fff;margin:12px;border-radius:18px;padding:16px;box-shadow:0 6px 18px #0001}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer}
.btn:disabled{opacity:0.5}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:10px;left:10px;right:10px;background:#fff;display:flex;justify-content:space-around;padding:12px 0;border-radius:22px;box-shadow:0 10px 30px #0003;z-index:50}
.nav div{flex:1;text-align:center;font-size:11px;opacity:0.45;cursor:pointer}
.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
#adOverlay,#welcomeOverlay{display:none;position:fixed;inset:0;background:#000c;z-index:200;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:14px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
.logo-box{width:62px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#fff}
.bkash-bg{background:#e2136e}
.nagad-bg{background:#ef4444}
input{width:100%;padding:14px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px;outline:none}
</style>
</head>
<body>

<div class="header" style="display:flex;justify-content:space-between;align-items:center">
<div><b>PROTIDINER KAJ BD</b><div style="font-size:11px;opacity:0.9">Admin ID: 8807178385 - FINAL</div></div>
<div id="adBadge" style="background:#fff3;padding:7px 14px;border-radius:20px;font-size:12px">Ad: 20</div>
</div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between;align-items:center">
<div><div style="opacity:0.85;font-size:12px">Balance</div><div id="balMain" style="font-size:36px;font-weight:800">0 TK</div><div style="font-size:11px;background:#fff2;padding:4px 10px;border-radius:20px;display:inline-block;margin-top:4px">Verified User</div></div>
<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:72px;height:72px;border-radius:50%;background:#fff">
</div>

<div id="welcomeOverlay" style="background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2);z-index:300">
<div style="background:#fff;color:#000;padding:24px;border-radius:22px;width:92%;max-width:360px;text-align:center">
<div style="font-size:62px">🎉</div>
<h2 style="margin:8px 0 0;color:#6d28d9">স্বাগতম!</h2>
<p style="margin:4px 0;color:#666;font-size:13px">Protidiner Kaj BD তে</p>
<div style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:16px;font-size:32px;font-weight:800;margin:14px 0">10 TK বোনাস</div>
<p style="font-size:11px;color:#666">প্রথম জয়েনে 10 TK - প্রতিদিন নয়, শুধু 1 বার</p>
<button class="btn purple" style="margin-top:14px" onclick="closeWelcome()">কাজ শুরু করুন</button>
</div>
</div>

<div id="p-home" class="page active">
<div class="card">
<div style="display:flex;justify-content:space-between"><h3 style="margin:0">বিজ্ঞাপন দেখুন</h3><span style="font-size:11px;background:#fef3c7;padding:4px 8px;border-radius:8px">2 TK / Ad</span></div>
<button class="btn purple" style="margin-top:14px" onclick="watchAd()">বিজ্ঞাপন দেখুন ও 2 TK নিন</button>
<div style="background:#ede9fe;height:10px;border-radius:20px;margin-top:14px;overflow:hidden"><div id="adProg" style="background:#6d28d9;height:100%;width:100%"></div></div>
<p id="adText" style="text-align:right;font-size:12px;color:#666;margin:6px 0 0">20/20 বাকি</p>
</div>
<div class="card">
<h3 style="margin:0 0 10px">আপনার রেফার লিংক - 10 TK</h3>
<div id="refLink" style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:13px"></div>
<div style="display:flex;gap:10px;margin-top:12px"><button class="btn" style="background:#fbbf24;flex:1" onclick="copyRef()">কপি</button><button class="btn" style="background:#0ea5e9;color:#fff;flex:1" onclick="shareRef()">শেয়ার</button></div>
</div>
</div>

<div id="p-tasks" class="page">
<div class="card">
<h3 style="margin:0 0 12px">ডেইলি টাস্ক</h3>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #f1f1f1"><div><b>ডেইলি চেক-ইন</b><div style="font-size:12px;color:#666" id="checkStatus">প্রতিদিন 5 TK</div></div><button id="checkBtn" class="btn purple" style="width:auto;padding:8px 18px" onclick="doCheck()">5 TK</button></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0"><div><b>10 টা Ad দেখুন</b><div style="font-size:12px;color:#666" id="taskAd">0/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff;padding:8px 16px" onclick="go('home')">যান</button></div>
</div>
</div>

<div id="p-invite" class="page">
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center"><h1 style="margin:0;font-size:48px">10 TK</h1><p>প্রতি রেফারে</p><div id="refLink2" style="background:#fff2;padding:12px;border-radius:12px;margin-top:14px;font-size:12px;word-break:break-all"></div></div>
</div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><h1 id="bal2" style="margin:0;color:#6d28d9">0 TK</h1><div style="font-size:12px;color:#666">Min Withdraw 100 TK</div></div>
<div class="card">
<h3 style="margin:0">টাকা তুলুন - শুধু বিকাশ নগদ - Logo Fixed</h3>
<div id="bkashOpt" class="withdraw-opt active" onclick="selectMethod('bKash')">
<div class="logo-box bkash-bg">bKash</div>
<div style="flex:1"><b>bKash Personal</b><div style="font-size:11px;color:#666">017xxxxxxxx</div></div>
<div style="font-weight:800;color:#6d28d9">✓</div>
</div>
<div id="nagadOpt" class="withdraw-opt" onclick="selectMethod('Nagad')">
<div class="logo-box nagad-bg">Nagad</div>
<div style="flex:1"><b>Nagad Personal</b><div style="font-size:11px;color:#666">018xxxxxxxx</div></div>
</div>
<input id="accNum" placeholder="আপনার নাম্বার দিন">
<input id="amount" type="number" placeholder="Amount Min 100">
<button class="btn purple" style="margin-top:14px" onclick="doWithdraw()">Withdraw করুন</button>
</div>
</div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:92px;height:92px;border-radius:50%;border:4px solid #8b5cf6"><h2>Riyad - ADMIN</h2><p>ID: 8807178385</p></div>
<div class="card" style="border:2px solid #6d28d9"><h3 style="margin:0">Admin Dashboard</h3><div style="display:flex;gap:8px;margin-top:14px"><div style="background:#ede9fe;padding:12px;border-radius:12px;flex:1;text-align:center"><div style="font-size:20px;font-weight:800">127</div><div style="font-size:10px">মোট ইউজার</div></div><div style="background:#fef3c7;padding:12px;border-radius:12px;flex:1;text-align:center"><div style="font-size:20px;font-weight:800">342</div><div style="font-size:10px">মোট রেফার</div></div><div style="background:#dcfce7;padding:12px;border-radius:12px;flex:1;text-align:center"><div style="font-size:20px;font-weight:800">10</div><div style="font-size:10px">Bonus</div></div></div></div>
<div class="card"><h3>Support System</h3><button class="btn" style="background:#0ea5e9;color:#fff;margin-top:12px" onclick="window.open('https://t.me/ProtidinerKaj_BD_Bot','_blank')">Admin কে মেসেজ করুন</button><div style="margin-top:12px;background:#f5f3ff;padding:12px;border-radius:12px"><input id="supportMsg" placeholder="আপনার সমস্যা লিখুন"><button class="btn purple" style="margin-top:8px;padding:10px" onclick="sendSupport()">পাঠান</button><div id="supportHistory" style="font-size:12px;margin-top:8px"></div></div></div>
</div>

<div id="adOverlay"><h2 style="margin:0">বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:64px;font-weight:800;margin:10px 0">15</div><p>15 সেকেন্ড দেখুন, তাহলেই টাকা পাবেন</p></div>

<div class="nav">
<div id="nav-home" class="active" onclick="go('home')"><div style="font-size:20px">🏠</div>Home</div>
<div id="nav-tasks" onclick="go('tasks')"><div style="font-size:20px">🎯</div>Tasks</div>
<div id="nav-invite" onclick="go('invite')"><div style="font-size:20px">👥</div>Invite</div>
<div id="nav-wallet" onclick="go('wallet')"><div style="font-size:20px">💰</div>Wallet</div>
<div id="nav-profile" onclick="go('profile')"><div style="font-size:20px">👤</div>Profile</div>
</div>

<script>
let bal=parseInt(localStorage.getItem('v8_bal')||'0');
let adLeft=parseInt(localStorage.getItem('v8_ad')||'20');
let adDone=parseInt(localStorage.getItem('v8_ad_done')||'0');
let firstJoin=localStorage.getItem('v8_first');
let lastCheck=localStorage.getItem('v8_check')||'';

function init(){
document.getElementById('balMain').innerText=bal+' TK';
document.getElementById('bal2').innerText=bal+' TK';
document.getElementById('adBadge').innerText='Ad: '+adLeft;
document.getElementById('adText').innerText=adLeft+'/20 বাকি';
document.getElementById('adProg').style.width=(adLeft/20*100)+'%';
document.getElementById('taskAd').innerText=adDone+'/10';
let today=new Date().toDateString();
if(lastCheck===today){document.getElementById('checkBtn').innerText='✓ Done';document.getElementById('checkBtn').disabled=true;document.getElementById('checkStatus').innerText='আজ কমপ্লিট - কাল আবার 5 TK';}
else{document.getElementById('checkBtn').innerText='5 TK';document.getElementById('checkBtn').disabled=false;document.getElementById('checkStatus').innerText='প্রতিদিন 5 TK - দিনে 1 বার';}
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';
document.getElementById('refLink').innerText=link;
document.getElementById('refLink2').innerText=link;
if(!firstJoin){setTimeout(function(){document.getElementById('welcomeOverlay').style.display='flex';},600);}
}

function closeWelcome(){
document.getElementById('welcomeOverlay').style.display='none';
if(!firstJoin){
bal+=10;
localStorage.setItem('v8_bal',bal);
localStorage.setItem('v8_first','done');
init();
alert('🎉 স্বাগতম! 10 TK বোনাস যোগ হয়েছে! এটা শুধু প্রথমবার পাবেন, প্রতিদিন নয়।');
}
}

function go(p){
document.querySelectorAll('.page').forEach(function(e){e.classList.remove('active')});
document.getElementById('p-'+p).classList.add('active');
document.querySelectorAll('.nav div').forEach(function(e){e.classList.remove('active')});
document.getElementById('nav-'+p).classList.add('active');
}

function watchAd(){
if(adLeft<=0){alert('আজকের Ad লিমিট শেষ - কাল আবার');return}
document.getElementById('adOverlay').style.display='flex';
let t=15;
document.getElementById('timer').innerText=t;
let ti=setInterval(function(){
t--;
document.getElementById('timer').innerText=t;
if(t<=0){
clearInterval(ti);
document.getElementById('adOverlay').style.display='none';
bal+=2;adLeft--;adDone++;
localStorage.setItem('v8_bal',bal);
localStorage.setItem('v8_ad',adLeft);
localStorage.setItem('v8_ad_done',adDone);
init();
alert('✅ 2 TK যোগ হয়েছে! Balance: '+bal+' TK');
}
},1000);
if(typeof show_11760259==='function'){show_11760259().catch(function(){})}
}

function doCheck(){
let today=new Date().toDateString();
if(lastCheck===today){alert('আজ চেক-ইন করেছেন! কাল আবার পাবেন');return}
bal+=5;lastCheck=today;
localStorage.setItem('v8_bal',bal);
localStorage.setItem('v8_check',today);
init();
alert('✅ 5 TK Daily Bonus!');
}

function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ কপি হয়েছে!')}
function shareRef(){let l=document.getElementById('refLink').innerText;if(navigator.share){navigator.share({title:'Join',url:l})}else{copyRef()}}

function selectMethod(m){
document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');
document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad');
}

function doWithdraw(){
let n=document.getElementById('accNum').value;
let a=parseInt(document.getElementById('amount').value);
if(!n||!a){alert('নাম্বার ও Amount দিন');return}
if(a<100){alert('Min 100 TK');return}
if(a>bal){alert('ব্যালেন্স কম');return}
bal-=a;
localStorage.setItem('v8_bal',bal);
init();
alert(a+' TK Withdraw Request গেছে!');
}

function sendSupport(){
let m=document.getElementById('supportMsg').value;
if(!m){alert('মেসেজ লিখুন');return}
document.getElementById('supportHistory').innerHTML+='<div style="background:#ede9fe;padding:10px;border-radius:10px;margin-top:8px"><b>আপনি:</b> '+m+'<br><span style="color:#10b981"><b>Admin:</b> পেয়েছি, 2 ঘন্টায় সমাধান দেবো</span></div>';
document.getElementById('supportMsg').value='';
alert('✅ Support Ticket Admin এর কাছে গেছে!');
}

init();
</script>
</body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(content=HTML)

@app.get("/health")
async def health():
    return {"ok": True, "final": "V8"}

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return HTMLResponse(content=HTML)
