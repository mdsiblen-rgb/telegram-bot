from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - V6 Welcome</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<style>
*{box-sizing:border-box;font-family:Hind Siliguri,sans-serif}body{margin:0;background:#f5f3ff;padding-bottom:100px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:0 0 20px 20px;position:sticky;top:0;z-index:10}
.card{background:#fff;margin:12px;border-radius:18px;padding:16px;box-shadow:0 4px 15px #0001}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:10px;left:10px;right:10px;background:#fff;display:flex;justify-content:space-around;padding:10px;border-radius:20px;box-shadow:0 10px 30px #0003;z-index:50}
.nav div{flex:1;text-align:center;font-size:11px;opacity:0.4;cursor:pointer}.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
#adOverlay,#welcomeOverlay{display:none;position:fixed;inset:0;background:#000d;z-index:200;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:12px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
input{width:100%;padding:13px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px}
</style></head><body>

<div class="header" style="display:flex;justify-content:space-between"><div><b>💎 Protidiner Kaj BD</b><div style="font-size:11px">Pro • Trusted • Admin: 8807178385</div></div><div id="adBadge" style="background:#fff3;padding:6px 12px;border-radius:20px;font-size:12px">Ad: 10</div></div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between"><div><div style="opacity:0.8;font-size:12px">ব্যালেন্স</div><div id="balMain" style="font-size:34px;font-weight:800">0 TK</div></div><img id="topPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:70px;height:70px;border-radius:50%;background:#fff"></div>

<!-- Welcome Popup -->
<div id="welcomeOverlay" style="background:linear-gradient(135deg,#6d28d9ee,#4f46e5ee);">
<div style="background:#fff;color:#000;padding:24px;border-radius:22px;width:90%;max-width:360px;text-align:center">
<div style="font-size:60px">🎉</div>
<h2 style="margin:10px 0 0;color:#6d28d9">স্বাগতম!</h2>
<h3 style="margin:6px 0">Protidiner Kaj BD তে</h3>
<p style="font-size:13px;color:#666;margin:8px 0">আপনি জয়েন করার জন্য বোনাস পেয়েছেন</p>
<div style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:14px;border-radius:14px;font-size:28px;font-weight:800;margin:14px 0">10 TK 💰</div>
<p style="font-size:11px;color:#666">এই টাকা দিয়ে কাজ শুরু করুন<br>প্রতিদিন Ad দেখে ইনকাম করুন</p>
<button class="btn purple" style="margin-top:14px" onclick="closeWelcome()">🚀 কাজ শুরু করুন</button>
</div>
</div>

<div id="p-home" class="page active">
<div class="card"><h3 style="margin:0">🎬 বিজ্ঞাপন দেখুন</h3><button id="adBtn" class="btn purple" style="margin-top:12px" onclick="watchAd()">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button><p id="adText" style="text-align:right;font-size:12px;color:#666;margin:6px 0 0">10/20 বাকি</p></div>
<div class="card"><h3 style="margin:0 0 10px">🔗 রেফার লিংক</h3><div id="refLink" style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:13px"></div></div>
</div>

<div id="p-tasks" class="page"><div class="card"><h3 style="margin:0 0 12px">🎯 ডেইলি টাস্ক</h3><div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #eee"><div><b>🎁 ডেইলি চেক-ইন</b><div style="font-size:12px;color:#666" id="checkStatus">প্রতিদিন 5 TK</div></div><button id="checkBtn" class="btn purple" style="width:auto;padding:8px 18px" onclick="doCheck()">5 TK</button></div><div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0"><div><b>🎬 10 টা Ad দেখুন</b><div style="font-size:12px;color:#666" id="taskAd">0/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff;padding:8px 16px" onclick="go('home')">যান</button></div></div></div>

<div id="p-invite" class="page"><div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center"><h1 style="margin:0;font-size:44px">10 TK</h1><p>প্রতি রেফারে</p><div id="refLink2" style="background:#fff2;padding:10px;border-radius:10px;margin-top:10px;font-size:12px;word-break:break-all"></div></div></div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><h1 id="bal2" style="margin:0;color:#6d28d9">0 TK</h1><div style="font-size:12px;color:#666">Withdrawable</div></div>
<div class="card">
<h3 style="margin:0">🏦 টাকা তুলুন - শুধু বিকাশ নগদ</h3>
<div id="bkashOpt" class="withdraw-opt active" onclick="selectMethod('bKash')"><img id="bkashLogo" src="https://download.logo.wine/logo/BKash/bKash-Logo.wine.png" style="width:55px;height:30px;object-fit:contain"><div style="flex:1"><b>bKash Personal</b></div>✓</div>
<div id="nagadOpt" class="withdraw-opt" onclick="selectMethod('Nagad')"><img id="nagadLogo" src="https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png" style="width:55px;height:30px;object-fit:contain"><div style="flex:1"><b>Nagad Personal</b></div></div>
<input id="accNum" placeholder="আপনার নাম্বার"><input id="amount" type="number" placeholder="Amount Min 100"><button class="btn purple" style="margin-top:12px" onclick="doWithdraw()">💸 Withdraw</button>
</div>
</div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center"><img id="uPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:90px;height:90px;border-radius:50%;border:4px solid #8b5cf6"><h2 id="uName">Riyad Ahmed</h2><p style="color:#666">ID: 8807178385</p></div>
<div class="card" style="border:2px solid #6d28d9"><h3 style="margin:0">👑 Admin Dashboard</h3><div style="display:flex;gap:8px;margin-top:10px"><div style="background:#ede9fe;padding:10px;border-radius:12px;flex:1;text-align:center"><div id="statUsers" style="font-weight:800;font-size:18px">0</div><div style="font-size:10px">ইউজার</div></div><div style="background:#fef3c7;padding:10px;border-radius:12px;flex:1;text-align:center"><div id="statRef" style="font-weight:800;font-size:18px">0</div><div style="font-size:10px">রেফার</div></div><div style="background:#dcfce7;padding:10px;border-radius:12px;flex:1;text-align:center"><div style="font-weight:800;font-size:18px">10 TK</div><div style="font-size:10px">Welcome Bonus</div></div></div>
<div id="refList" style="font-size:11px;background:#f9f9f9;padding:8px;border-radius:10px;margin-top:8px">নতুন ইউজার এলে এখানে দেখা যাবে...</div>
</div>
<div class="card"><h3 style="margin:0">💬 Support</h3><button class="btn" style="background:#0ea5e9;color:#fff;margin-top:10px" onclick="window.open('https://t.me/ProtidinerKaj_BD_Bot','_blank')">📩 Admin কে মেসেজ করুন</button></div>
</div>

<div id="adOverlay"><h2>⏳ বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:60px;font-weight:800">15</div><p>15 সেকেন্ড অপেক্ষা করুন</p></div>

<div class="nav">
<div id="nav-home" class="active" onclick="go('home')"><div style="font-size:20px">🏠</div>Home</div>
<div id="nav-tasks" onclick="go('tasks')"><div style="font-size:20px">🎯</div>Tasks</div>
<div id="nav-invite" onclick="go('invite')"><div style="font-size:20px">👥</div>Invite</div>
<div id="nav-wallet" onclick="go('wallet')"><div style="font-size:20px">💰</div>Wallet</div>
<div id="nav-profile" onclick="go('profile')"><div style="font-size:20px">👤</div>Profile</div>
</div>

<script>
let bal=parseInt(localStorage.getItem('bal_welcome_v6')||'0');
let adLeft=parseInt(localStorage.getItem('ad_welcome_v6')||'20');
let adDone=parseInt(localStorage.getItem('ad_done_welcome_v6')||'0');
let firstJoin=localStorage.getItem('first_join_v6');
let lastCheck=localStorage.getItem('last_check_v6')||'';
let pic=localStorage.getItem('pic_v6')||'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';
let name=localStorage.getItem('name_v6')||'Riyad Ahmed';

function init(){
document.getElementById('balMain').innerText=bal+' TK';
document.getElementById('bal2').innerText=bal+' TK';
document.getElementById('adBadge').innerText='Ad: '+adLeft;
document.getElementById('adText').innerText=adLeft+'/20 বাকি';
document.getElementById('taskAd').innerText=adDone+'/10';
document.getElementById('topPic').src=pic;
document.getElementById('uPic').src=pic;
document.getElementById('uName').innerText=name;
let today=new Date().toDateString();
if(lastCheck===today){document.getElementById('checkBtn').innerText='✓ Done';document.getElementById('checkBtn').disabled=true;document.getElementById('checkStatus').innerText='আজ কমপ্লিট (কাল আবার)';}
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';
document.getElementById('refLink').innerText=link;
document.getElementById('refLink2').innerText=link;

// Welcome System: প্রথমবার ঢুকলে 10 TK বোনাস + স্বাগতম পপআপ
if(!firstJoin){
setTimeout(()=>{document.getElementById('welcomeOverlay').style.display='flex';},800);
}
document.getElementById('statUsers').innerText=localStorage.getItem('total_users_v6')||'127';
document.getElementById('statRef').innerText=localStorage.getItem('total_ref_v6')||'342';
}

function closeWelcome(){
document.getElementById('welcomeOverlay').style.display='none';
if(!firstJoin){
bal+=10;
adDone=0;
localStorage.setItem('bal_welcome_v6',bal);
localStorage.setItem('first_join_v6','done');
localStorage.setItem('total_users_v6', parseInt(localStorage.getItem('total_users_v6')||'127')+1);
init();
alert('🎉 স্বাগতম! আপনার অ্যাকাউন্টে 10 TK বোনাস যোগ হয়েছে!');
}
}

function go(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav-'+p).classList.add('active')}

function watchAd(){
if(adLeft<=0){alert('আজকের লিমিট শেষ');return}
document.getElementById('adOverlay').style.display='flex';
let t=15; document.getElementById('timer').innerText=t;
let ti=setInterval(()=>{t--;document.getElementById('timer').innerText=t;if(t<=0){clearInterval(ti);document.getElementById('adOverlay').style.display='none';bal+=2;adLeft--;adDone++;localStorage.setItem('bal_welcome_v6',bal);localStorage.setItem('ad_welcome_v6',adLeft);localStorage.setItem('ad_done_welcome_v6',adDone);init();alert('✅ 2 TK যোগ হয়েছে!');}},1000);
if(typeof show_11760259==='function'){show_11760259().catch(()=>{})}
}

function doCheck(){
let today=new Date().toDateString();
if(lastCheck===today){alert('আজ চেক-ইন করেছেন, কাল আবার পাবেন');return}
bal+=5;lastCheck=today;localStorage.setItem('bal_welcome_v6',bal);localStorage.setItem('last_check_v6',today);init();alert('✅ 5 TK Daily Bonus!');
}

function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ কপি হয়েছে!')}
function shareRef(){let l=document.getElementById('refLink').innerText;if(navigator.share)navigator.share({url:l});else copyRef()}
function selectMethod(m){document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad')}
function doWithdraw(){let n=document.getElementById('accNum').value;let a=parseInt(document.getElementById('amount').value);if(!n||!a){alert('নাম্বার ও Amount দিন');return}if(a<100){alert('Min 100');return}if(a>bal){alert('ব্যালেন্স কম');return}bal-=a;localStorage.setItem('bal_welcome_v6',bal);init();alert('✅ '+a+' TK Withdraw Request গেছে!');}

init();
</script>
</body></html>
    """

@app.get("/health")
async def health():
    return {"ok": True, "feature": "welcome_10tk_bonus"}
