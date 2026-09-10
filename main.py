from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    html = '''
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - FINAL FIXED</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<style>
*{box-sizing:border-box;font-family:sans-serif}body{margin:0;background:#f5f3ff;padding-bottom:110px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:0 0 22px 22px;position:sticky;top:0;z-index:20}
.card{background:#fff;margin:12px;border-radius:18px;padding:16px;box-shadow:0 6px 18px #0001}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:10px;left:10px;right:10px;background:#fff;display:flex;justify-content:space-around;padding:12px 0;border-radius:22px;box-shadow:0 10px 30px #0003;z-index:50}
.nav div{flex:1;text-align:center;font-size:11px;opacity:0.45;cursor:pointer}.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
#adOverlay,#welcomeOverlay{display:none;position:fixed;inset:0;background:#000c;z-index:200;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:14px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
.logo-box{width:62px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#fff}
.bkash-bg{background:#e2136e}.nagad-bg{background:#f6921e}
input{width:100%;padding:14px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px;outline:none}
</style></head><body>

<div class="header" style="display:flex;justify-content:space-between"><div><b>PROTIDINER KAJ BD</b><div style="font-size:11px">Pro - Admin 8807178385</div></div><div id="adBadge" style="background:#fff3;padding:7px 14px;border-radius:20px;font-size:12px">Ad: 20</div></div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between"><div><div style="opacity:0.85;font-size:12px">Balance</div><div id="balMain" style="font-size:36px;font-weight:800">0 TK</div></div><img id="topPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:72px;height:72px;border-radius:50%;background:#fff"></div>

<div id="welcomeOverlay" style="background:linear-gradient(135deg,#6d28d9f2,#4f46e5f2);z-index:300"><div style="background:#fff;color:#000;padding:24px;border-radius:22px;width:92%;max-width:360px;text-align:center"><div style="font-size:62px">🎉</div><h2 style="margin:8px 0 0;color:#6d28d9">Welcome!</h2><div style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:16px;font-size:32px;font-weight:800;margin:14px 0">10 TK Bonus</div><p style="font-size:11px;color:#666">First join only - Not every day</p><button class="btn purple" style="margin-top:14px" onclick="closeWelcome()">Start Work</button></div></div>

<div id="p-home" class="page active"><div class="card"><h3 style="margin:0">Ad Dekhun</h3><button id="adBtn" class="btn purple" style="margin-top:14px" onclick="watchAd()">Ad Dekhun O 2 TK Nin</button><p id="adText" style="text-align:right;font-size:12px;color:#666;margin:6px 0 0">20/20 baki</p></div><div class="card"><h3 style="margin:0 0 10px">Refer Link</h3><div id="refLink" style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:13px"></div></div></div>

<div id="p-tasks" class="page"><div class="card"><h3>Daily Task</h3><div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #eee"><div><b>Daily Check-in</b><div style="font-size:12px;color:#666" id="checkStatus">Daily 5 TK</div></div><button id="checkBtn" class="btn purple" style="width:auto;padding:8px 18px" onclick="doCheck()">5 TK</button></div><div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0"><div><b>10 Ad Dekhun</b><div style="font-size:12px;color:#666" id="taskAd">0/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff;padding:8px 16px" onclick="go('home')">Jan</button></div></div></div>

<div id="p-invite" class="page"><div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center"><h1 style="margin:0;font-size:48px">10 TK</h1><p>Per Refer</p><div id="refLink2" style="background:#fff2;padding:12px;border-radius:12px;margin-top:14px;font-size:12px;word-break:break-all"></div></div></div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><h1 id="bal2" style="margin:0;color:#6d28d9">0 TK</h1><div style="font-size:12px;color:#666">Withdrawable - Min 100 TK</div></div>
<div class="card">
<h3 style="margin:0">Taka Tulun - Sudhu bKash Nagad - Logo Fixed</h3>
<div id="bkashOpt" class="withdraw-opt active" onclick="selectMethod('bKash')"><div class="logo-box bkash-bg">bKash</div><div style="flex:1"><b>bKash Personal</b></div><div style="font-weight:800;color:#6d28d9">✓</div></div>
<div id="nagadOpt" class="withdraw-opt" onclick="selectMethod('Nagad')"><div class="logo-box nagad-bg">Nagad</div><div style="flex:1"><b>Nagad Personal</b></div></div>
<input id="accNum" placeholder="Apnar number"><input id="amount" type="number" placeholder="Amount Min 100"><button class="btn purple" style="margin-top:14px" onclick="doWithdraw()">Withdraw</button>
</div>
</div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center"><img id="uPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:92px;height:92px;border-radius:50%;border:4px solid #8b5cf6"><h2 id="uName">Riyad Ahmed</h2><p style="color:#666">ID: 8807178385 ADMIN</p></div>
<div class="card" style="border:2px solid #6d28d9"><h3 style="margin:0">Admin Dashboard</h3><div style="display:flex;gap:8px;margin-top:14px"><div style="background:#ede9fe;padding:12px;border-radius:12px;flex:1;text-align:center"><div id="statUsers" style="font-size:20px;font-weight:800">127</div><div style="font-size:10px">Users</div></div><div style="background:#fef3c7;padding:12px;border-radius:12px;flex:1;text-align:center"><div id="statRef" style="font-size:20px;font-weight:800">342</div><div style="font-size:10px">Refers</div></div><div style="background:#dcfce7;padding:12px;border-radius:12px;flex:1;text-align:center"><div style="font-size:20px;font-weight:800">10 TK</div><div style="font-size:10px">Welcome</div></div></div></div>
<div class="card"><h3 style="margin:0">Support</h3><button class="btn" style="background:#0ea5e9;color:#fff;margin-top:12px" onclick="window.open('https://t.me/ProtidinerKaj_BD_Bot','_blank')">Admin Ke Message</button><div style="margin-top:12px;background:#f5f3ff;padding:12px;border-radius:12px"><input id="supportMsg" placeholder="Apnar somossa likhun"><button class="btn purple" style="margin-top:8px;padding:10px" onclick="sendSupport()">Pathan</button><div id="supportHistory" style="font-size:12px;margin-top:8px"></div></div></div>
</div>

<div id="adOverlay"><h2>Ad Cholche...</h2><div id="timer" style="font-size:64px;font-weight:800">15</div><p>15 sec dekhun</p></div>

<div class="nav">
<div id="nav-home" class="active" onclick="go('home')"><div style="font-size:20px">🏠</div>Home</div>
<div id="nav-tasks" onclick="go('tasks')"><div style="font-size:20px">🎯</div>Tasks</div>
<div id="nav-invite" onclick="go('invite')"><div style="font-size:20px">👥</div>Invite</div>
<div id="nav-wallet" onclick="go('wallet')"><div style="font-size:20px">💰</div>Wallet</div>
<div id="nav-profile" onclick="go('profile')"><div style="font-size:20px">👤</div>Profile</div>
</div>

<script>
let bal=parseInt(localStorage.getItem('f_bal')||'0');
let adLeft=parseInt(localStorage.getItem('f_ad')||'20');
let adDone=parseInt(localStorage.getItem('f_ad_done')||'0');
let firstJoin=localStorage.getItem('f_first');
let lastCheck=localStorage.getItem('f_check')||'';
function init(){
document.getElementById('balMain').innerText=bal+' TK';
document.getElementById('bal2').innerText=bal+' TK';
document.getElementById('adBadge').innerText='Ad: '+adLeft;
document.getElementById('adText').innerText=adLeft+'/20 baki';
document.getElementById('taskAd').innerText=adDone+'/10';
let today=new Date().toDateString();
if(lastCheck===today){document.getElementById('checkBtn').innerText='Done';document.getElementById('checkBtn').disabled=true;document.getElementById('checkStatus').innerText='Aj complete - kal abar';}else{document.getElementById('checkBtn').innerText='5 TK';document.getElementById('checkBtn').disabled=false;}
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';
document.getElementById('refLink').innerText=link;
document.getElementById('refLink2').innerText=link;
if(!firstJoin){setTimeout(()=>{document.getElementById('welcomeOverlay').style.display='flex';},600);}
}
function closeWelcome(){document.getElementById('welcomeOverlay').style.display='none';if(!firstJoin){bal+=10;localStorage.setItem('f_bal',bal);localStorage.setItem('f_first','done');init();alert('Welcome! 10 TK Bonus Added - First time only');}}
function go(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav-'+p).classList.add('active')}
function watchAd(){if(adLeft<=0){alert('Limit sesh');return}document.getElementById('adOverlay').style.display='flex';let t=15;document.getElementById('timer').innerText=t;let ti=setInterval(()=>{t--;document.getElementById('timer').innerText=t;if(t<=0){clearInterval(ti);document.getElementById('adOverlay').style.display='none';bal+=2;adLeft--;adDone++;localStorage.setItem('f_bal',bal);localStorage.setItem('f_ad',adLeft);localStorage.setItem('f_ad_done',adDone);init();alert('2 TK Added!');}},1000);if(typeof show_11760259==='function'){show_11760259().catch(()=>{})}}
function doCheck(){let today=new Date().toDateString();if(lastCheck===today){alert('Aj korechen, kal abar');return}bal+=5;lastCheck=today;localStorage.setItem('f_bal',bal);localStorage.setItem('f_check',today);init();alert('5 TK Bonus!');}
function selectMethod(m){document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad')}
function doWithdraw(){let n=document.getElementById('accNum').value;let a=parseInt(document.getElementById('amount').value);if(!n||!a){alert('Number O Amount din');return}if(a<100){alert('Min 100');return}if(a>bal){alert('Balance kom');return}bal-=a;localStorage.setItem('f_bal',bal);init();alert(a+' TK Withdraw Request!');}
function sendSupport(){let m=document.getElementById('supportMsg').value;if(!m){alert('Message likhun');return}document.getElementById('supportHistory').innerHTML+='<div style="background:#ede9fe;padding:10px;border-radius:10px;margin-top:8px"><b>Apni:</b> '+m+'<br><span style="color:#10b981"><b>Admin:</b> Peyechi, 2 ghontay somadhan debo</span></div>';document.getElementById('supportMsg').value='';alert('Support Ticket Admin kache geche!');}
init();
</script>
</body></html>
    '''
    return HTMLResponse(content=html)

@app.get("/health")
async def health():
    return {"ok": True, "version": "FINAL_FIXED_NO_TRIPLE_QUOTE_ERROR"}
