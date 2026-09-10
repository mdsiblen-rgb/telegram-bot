from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - Pro</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@500;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;font-family:'Hind Siliguri',sans-serif}
body{margin:0;background:#f5f3ff;padding-bottom:90px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:18px 16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10;border-radius:0 0 20px 20px}
.header b{font-size:18px}
.card{background:#fff;margin:12px;border-radius:20px;padding:16px;box-shadow:0 8px 20px #6d28d91a}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer;transition:0.2s}
.btn:active{transform:scale(0.97)}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.blue{background:linear-gradient(135deg,#0ea5e9,#4f46e5);color:#fff}
.yellow{background:linear-gradient(135deg,#f59e0b,#fbbf24);color:#000}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:12px;left:12px;right:12px;background:#fff;display:flex;justify-content:space-around;padding:10px 0;border-radius:20px;box-shadow:0 10px 30px #0002;z-index:20}
.nav div{text-align:center;font-size:11px;cursor:pointer;opacity:0.4;flex:1}.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
.icon-box{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px}
.task-row{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #f1f1f1}
.task-row:last-child{border:none}
input,select{width:100%;padding:13px;border-radius:12px;border:1.5px solid #e9d5ff;background:#faf5ff;outline:none;margin-top:8px}
</style></head><body>

<div class="header"><div><b id="appName">💎 Protidiner Kaj BD</b><div style="font-size:11px;opacity:0.9">Pro Version • Trusted</div></div><div style="background:#fff2;padding:6px 14px;border-radius:20px;font-size:12px" id="adBadge">🎬 Ad: 20</div></div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between;align-items:center">
<div><div style="opacity:0.8;font-size:12px">আপনার ব্যালেন্স</div><div style="font-size:32px;font-weight:800" id="balMain">30 TK</div><div style="font-size:11px;background:#fff3;padding:4px 10px;border-radius:20px;display:inline-block;margin-top:6px">✓ Active • ID: 8807178385</div></div>
<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:80px;height:80px">
</div>

<div class="card" style="display:flex;justify-content:space-around;text-align:center;padding:10px">
<div><div style="font-size:20px">🔥</div><div style="font-size:11px;color:#666">Streak</div><b>5 দিন</b></div>
<div style="width:1px;background:#eee"></div>
<div><div style="font-size:20px">👥</div><div style="font-size:11px;color:#666">রেফার</div><b id="refCount">0 জন</b></div>
<div style="width:1px;background:#eee"></div>
<div><div style="font-size:20px">💰</div><div style="font-size:11px;color:#666">মোট আয়</div><b id="totalMain" style="color:#6d28d9">30 TK</b></div>
</div>

<div id="p-home" class="page active">
<div class="card">
<div style="display:flex;justify-content:space-between;align-items:center"><h3 style="margin:0">🎬 বিজ্ঞাপন দেখুন</h3><span style="font-size:11px;background:#fef3c7;padding:4px 8px;border-radius:8px">2 TK / Ad</span></div>
<button id="adBtn" class="btn purple" style="margin-top:14px" onclick="watchAd()">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button>
<div style="background:#ede9fe;height:10px;border-radius:20px;margin-top:14px;overflow:hidden"><div id="adProg" style="background:linear-gradient(90deg,#6d28d9,#8b5cf6);height:100%;width:100%"></div></div>
<p id="adText" style="text-align:right;font-size:12px;color:#6b7280;margin:6px 0 0">20/20 বাকি আছে</p>
</div>

<div class="card">
<h3 style="margin:0 0 10px">🔗 আপনার রেফার লিংক</h3>
<div style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:14px;border-radius:14px;word-break:break-all;text-align:center;font-size:13px" id="refLink"></div>
<div style="display:flex;gap:10px;margin-top:12px"><button class="btn yellow" style="flex:1" onclick="copyRef()">📋 কপি</button><button class="btn blue" style="flex:1" onclick="shareRef()">📤 শেয়ার</button></div>
</div>
</div>

<div id="p-tasks" class="page">
<div class="card"><h3 style="margin:0 0 10px">🎯 ডেইলি টাস্ক - ভরপুর ইনকাম</h3>
<div class="task-row"><div class="icon-box" style="background:#fef3c7">🎁</div><div style="flex:1"><b>ডেইলি চেক-ইন</b><div style="font-size:12px;color:#666">প্রতিদিন লগইন করুন</div></div><button class="btn purple" style="width:auto;padding:8px 18px" onclick="taskCheck()">5 TK</button></div>
<div class="task-row"><div class="icon-box" style="background:#dbeafe">🎬</div><div style="flex:1"><b>১০ টা Ad দেখুন</b><div style="font-size:12px;color:#666"><span id="adDone">0</span>/10 কমপ্লিট</div></div><button class="btn blue" style="width:auto;padding:8px 18px" onclick="go('home')">যান</button></div>
<div class="task-row"><div class="icon-box" style="background:#dcfce7">👥</div><div style="flex:1"><b>৩ জনকে Invite করুন</b><div style="font-size:12px;color:#666">প্রতি Invite 10 TK</div></div><button class="btn" style="width:auto;padding:8px 18px;background:#10b981;color:#fff" onclick="go('invite')">Invite</button></div>
<div class="task-row"><div class="icon-box" style="background:#ede9fe">📢</div><div style="flex:1"><b>Telegram চ্যানেলে জয়েন</b><div style="font-size:12px;color:#666">বোনাস 10 TK</div></div><button class="btn" style="width:auto;padding:8px 18px;background:#000;color:#fff" onclick="window.open('https://t.me/','_blank')">Join</button></div>
</div>
<div class="card" style="text-align:center"><img src="https://cdn-icons-png.flaticon.com/512/888/888879.png" style="width:60px"><h4>সব টাস্ক কমপ্লিট করুন</h4><p style="font-size:12px;color:#666">প্রতিদিন 100+ TK ইনকাম করুন</p></div>
</div>

<div id="p-invite" class="page">
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center">
<h1 style="margin:0;font-size:48px">10 TK</h1><p style="margin:0;opacity:0.9">প্রতি সফল রেফারে পাবেন</p>
<div style="background:#fff2;padding:12px;border-radius:14px;margin-top:14px"><div style="font-size:13px" id="refLink2"></div></div>
</div>
<div class="card"><h3 style="margin:0">📊 Invite Board</h3><div style="display:flex;justify-content:space-between;margin-top:14px;text-align:center"><div style="background:#f5f3ff;padding:12px;border-radius:14px;flex:1;margin-right:8px"><div style="font-size:22px;font-weight:800" id="totalRef">0</div><div style="font-size:11px">মোট Invite</div></div><div style="background:#fef3c7;padding:12px;border-radius:14px;flex:1"><div style="font-size:22px;font-weight:800">0 TK</div><div style="font-size:11px">Invite আয়</div></div></div></div>
</div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><div style="font-size:12px;color:#666">Withdrawable Balance</div><h1 style="margin:4px 0;font-size:38px;color:#6d28d9" id="bal2">30 TK</h1><div style="font-size:11px;background:#dcfce7;color:#166534;padding:4px 10px;border-radius:20px;display:inline-block">✓ Verified Account</div></div>

<div class="card">
<h3 style="margin:0 0 12px">🏦 টাকা তোলার মাধ্যম - সব আছে</h3>
<select id="method">
<option>💜 bKash Personal</option>
<option>💗 Nagad Personal</option>
<option>❤️ Rocket Personal</option>
<option>💙 Upay Personal</option>
<option>💛 Binance Pay</option>
<option>🖤 USDT (BEP20)</option>
</select>
<input id="accNum" placeholder="নাম্বার / Wallet Address দিন">
<input id="amount" type="number" placeholder="Amount - Min 100 TK">
<button class="btn purple" style="margin-top:14px" onclick="withdraw()">💸 Withdraw করুন</button>
<p style="font-size:11px;color:#666;text-align:center;margin-top:10px">⏰ 5-30 মিনিটের মধ্যে পেমেন্ট পাবেন<br>Min Withdraw 100 TK</p>
</div>
<div class="card"><h4 style="margin:0">📜 Withdraw History</h4><div style="text-align:center;padding:20px;color:#999;font-size:13px">কোনো History নেই<br>প্রথম Withdraw করুন</div></div>
</div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center">
<img id="uPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:100px;height:100px;border-radius:50%;border:4px solid #8b5cf6;object-fit:cover">
<h2 id="uName" style="margin:10px 0 0">Riyad Ahmed</h2>
<p style="margin:4px 0;color:#666;font-size:13px">ID: 8807178385 <span style="background:#6d28d9;color:#fff;padding:3px 10px;border-radius:20px;font-size:10px">PRO • ADMIN</span></p>
<button class="btn blue" style="margin-top:12px" onclick="openEdit()">✏️ নাম ও ছবি এডিট করুন</button>
</div>

<div class="card">
<h3 style="margin:0 0 10px">⚙️ সেটিংস</h3>
<div class="task-row"><div class="icon-box" style="background:#f5f3ff">🎨</div><div style="flex:1"><b>App Name</b><div style="font-size:12px;color:#666" id="setAppName">Protidiner Kaj BD</div></div><button class="btn" style="width:auto;background:#ede9fe;color:#6d28d9;padding:8px 14px" onclick="editAppName()">Edit</button></div>
<div class="task-row"><div class="icon-box" style="background:#fef3c7">🔔</div><div style="flex:1"><b>Notification</b><div style="font-size:12px;color:#666">On আছে</div></div><div style="background:#10b981;width:40px;height:22px;border-radius:20px;position:relative"><div style="background:#fff;width:18px;height:18px;border-radius:50%;position:absolute;right:2px;top:2px"></div></div></div>
</div>

<div class="card" style="border:2px solid #8b5cf6">
<h3 style="margin:0">👑 Admin Panel</h3><p style="font-size:11px;color:#666">শুধু আপনার জন্য</p>
<input id="adminAppName" placeholder="নতুন App Name লিখুন">
<input id="adminAdReward" placeholder="Ad Reward (যেমন 2)">
<button class="btn purple" style="margin-top:10px" onclick="saveAdmin()">💾 Save Settings</button>
</div>
</div>

<div id="editModal" style="display:none;position:fixed;inset:0;background:#0008;z-index:100;justify-content:center;align-items:center">
<div style="background:#fff;width:90%;max-width:360px;padding:20px;border-radius:20px">
<h3 style="margin:0">✏️ প্রোফাইল এডিট</h3>
<input id="editName" placeholder="নতুন নাম">
<input type="file" id="editPhoto" accept="image/*">
<img id="prevImg" style="width:70px;height:70px;border-radius:50%;margin-top:10px;display:none;object-fit:cover">
<button class="btn purple" style="margin-top:14px" onclick="saveProfile()">Save করুন</button>
<button class="btn" style="margin-top:8px;background:#f3f4f6" onclick="closeEdit()">বন্ধ করুন</button>
</div>
</div>

<div class="nav">
<div id="nav-home" class="active" onclick="go('home')"><div style="font-size:20px">🏠</div>Home</div>
<div id="nav-tasks" onclick="go('tasks')"><div style="font-size:20px">🎯</div>Tasks</div>
<div id="nav-invite" onclick="go('invite')"><div style="font-size:20px">👥</div>Invite</div>
<div id="nav-wallet" onclick="go('wallet')"><div style="font-size:20px">💰</div>Wallet</div>
<div id="nav-profile" onclick="go('profile')"><div style="font-size:20px">👤</div>Profile</div>
</div>

<script>
let tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand()}
let bal=parseInt(localStorage.getItem('bal_pro')||'30');
let adLeft=parseInt(localStorage.getItem('ad_pro')||'20');
let adDone=parseInt(localStorage.getItem('ad_done')||'0');
let pic=localStorage.getItem('pic_pro')||'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';
let name=localStorage.getItem('name_pro')||'Riyad Ahmed';
function init(){
document.getElementById('balMain').innerText=bal+' TK';
document.getElementById('bal2').innerText=bal+' TK';
document.getElementById('totalMain').innerText=bal+' TK';
document.getElementById('adBadge').innerText='🎬 Ad: '+adLeft;
document.getElementById('adText').innerText=adLeft+'/20 বাকি';
document.getElementById('adProg').style.width=(adLeft/20*100)+'%';
document.getElementById('adDone').innerText=adDone;
document.getElementById('uPic').src=pic;
document.getElementById('uName').innerText=name;
document.getElementById('refCount').innerText='0 জন';
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';
document.getElementById('refLink').innerText=link;
document.getElementById('refLink2').innerText=link;
}
function go(p){
document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));
document.getElementById('p-'+p).classList.add('active');
document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));
document.getElementById('nav-'+p).classList.add('active');
}
function watchAd(){
if(adLeft<=0){alert('আজকের Ad শেষ');return}
let btn=document.getElementById('adBtn');
btn.innerText='⏳ লোড হচ্ছে...'; btn.disabled=true;
if(typeof show_11760259==='function'){
show_11760259().then(()=>{doneAd()}).catch(()=>{doneAd()});
}else{setTimeout(doneAd,1000)}
}
function doneAd(){
bal+=2; adLeft--; adDone++;
localStorage.setItem('bal_pro',bal);localStorage.setItem('ad_pro',adLeft);localStorage.setItem('ad_done',adDone);
init();
document.getElementById('adBtn').innerText='▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন';
document.getElementById('adBtn').disabled=false;
alert('✅ 2 TK যোগ হয়েছে! ব্যালেন্স: '+bal+' TK');
}
function taskCheck(){bal+=5;localStorage.setItem('bal_pro',bal);init();alert('✅ 5 TK Check-in!')}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ কপি হয়েছে!')}
function shareRef(){let l=document.getElementById('refLink').innerText; if(navigator.share){navigator.share({title:'Join',text:l,url:l})}else{copyRef()}}
function withdraw(){
let m=document.getElementById('method').value;
let n=document.getElementById('accNum').value;
let a=parseInt(document.getElementById('amount').value);
if(!n||!a){alert('নাম্বার ও Amount দিন');return}
if(a<100){alert('Min 100 TK');return}
if(a>bal){alert('ব্যালেন্স কম');return}
bal-=a;localStorage.setItem('bal_pro',bal);init();alert('✅ '+a+' TK Withdraw Request গেছে!\\n'+m+'\\n'+n);
}
function openEdit(){document.getElementById('editModal').style.display='flex';document.getElementById('editName').value=name}
function closeEdit(){document.getElementById('editModal').style.display='none'}
document.getElementById('editPhoto').addEventListener('change',function(e){
let f=e.target.files[0];let r=new FileReader();
r.onload=function(ev){document.getElementById('prevImg').src=ev.target.result;document.getElementById('prevImg').style.display='block';document.getElementById('prevImg').dataset.b64=ev.target.result}
r.readAsDataURL(f);
});
function saveProfile(){
let nn=document.getElementById('editName').value;
let b64=document.getElementById('prevImg').dataset.b64;
if(nn){name=nn;localStorage.setItem('name_pro',nn)}
if(b64){pic=b64;localStorage.setItem('pic_pro',b64)}
init();closeEdit();alert('✅ প্রোফাইল আপডেট!');
}
function editAppName(){let n=prompt('নতুন App Name দিন');if(n){document.getElementById('appName').innerText='💎 '+n;document.getElementById('setAppName').innerText=n}}
function saveAdmin(){let n=document.getElementById('adminAppName').value;if(n){document.getElementById('appName').innerText='💎 '+n;alert('✅ Save হয়েছে!')} }
init();
</script>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML

@app.get("/health")
async def health():
    return {"status":"ok","design":"pro_v2_purple"}
