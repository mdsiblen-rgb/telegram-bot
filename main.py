from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11760259" data-sdk="show_11760259"></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;font-family:'Hind Siliguri',sans-serif}body{margin:0;background:#f5f3ff;padding-bottom:100px}
.header{background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;padding:16px;border-radius:0 0 20px 20px;position:sticky;top:0;z-index:10}
.card{background:#fff;margin:12px;border-radius:18px;padding:16px;box-shadow:0 4px 15px #0001}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;font-size:15px;cursor:pointer}
.btn:disabled{opacity:0.5}
.purple{background:linear-gradient(135deg,#6d28d9,#8b5cf6);color:#fff}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:10px;left:10px;right:10px;background:#fff;display:flex;justify-content:space-around;padding:10px;border-radius:20px;box-shadow:0 10px 30px #0003;z-index:50}
.nav div{flex:1;text-align:center;font-size:11px;opacity:0.4;cursor:pointer}.nav div.active{opacity:1;color:#6d28d9;font-weight:800}
#adOverlay{display:none;position:fixed;inset:0;background:#000d;z-index:100;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:12px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
input,select{width:100%;padding:13px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px}
</style></head><body>

<div class="header" style="display:flex;justify-content:space-between;align-items:center">
<div><b>💎 Protidiner Kaj BD</b><div style="font-size:11px;opacity:0.8">Pro • Trusted • Admin: 8807178385</div></div>
<div style="background:#fff3;padding:6px 12px;border-radius:20px;font-size:12px" id="adBadge">Ad: 12</div>
</div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between">
<div><div style="opacity:0.8;font-size:12px">ব্যালেন্স</div><div style="font-size:34px;font-weight:800" id="balMain">61 TK</div></div>
<img id="topPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:70px;height:70px;border-radius:50%;background:#fff">
</div>

<div id="p-home" class="page active">
<div class="card">
<h3 style="margin:0">🎬 বিজ্ঞাপন দেখুন</h3>
<button id="adBtn" class="btn purple" style="margin-top:12px" onclick="watchAd()">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button>
<div style="background:#ede9fe;height:10px;border-radius:20px;margin-top:12px;overflow:hidden"><div id="adProg" style="background:#6d28d9;height:100%;width:60%"></div></div>
<p id="adText" style="text-align:right;font-size:12px;color:#666;margin:6px 0 0">12/20 বাকি</p>
</div>
<div class="card"><h3 style="margin:0 0 10px">🔗 রেফার লিংক</h3><div id="refLink" style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:13px"></div>
<div style="display:flex;gap:10px;margin-top:10px"><button class="btn" style="background:#fbbf24;flex:1" onclick="copyRef()">📋 কপি</button><button class="btn" style="background:#0ea5e9;color:#fff;flex:1" onclick="shareRef()">📤 শেয়ার</button></div>
</div>
</div>

<div id="p-tasks" class="page">
<div class="card"><h3 style="margin:0 0 12px">🎯 ডেইলি টাস্ক</h3>
<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #eee"><div><b>🎁 ডেইলি চেক-ইন</b><div style="font-size:12px;color:#666">প্রতিদিন 5 TK</div></div><button class="btn purple" style="width:auto;padding:8px 16px" onclick="doCheck()">5 TK</button></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #eee"><div><b>🎬 10 টা Ad দেখুন</b><div style="font-size:12px;color:#666" id="taskAd">8/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff;padding:8px 16px" onclick="go('home')">যান</button></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0"><div><b>👥 3 জনকে Invite</b><div style="font-size:12px;color:#666">প্রতি 10 TK</div></div><button class="btn" style="width:auto;background:#10b981;color:#fff;padding:8px 16px" onclick="go('invite')">Invite</button></div>
</div>
</div>

<div id="p-invite" class="page">
<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center"><h1 style="margin:0;font-size:44px">10 TK</h1><p>প্রতি রেফারে</p><div id="refLink2" style="background:#fff2;padding:10px;border-radius:10px;margin-top:10px;font-size:12px;word-break:break-all"></div></div>
</div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><div style="font-size:12px;color:#666">Withdrawable</div><h1 id="bal2" style="margin:4px 0;color:#6d28d9;font-size:36px">61 TK</h1></div>
<div class="card">
<h3 style="margin:0">🏦 টাকা তোলার মাধ্যম (এডিট করা যায়)</h3>
<div id="bkashOpt" class="withdraw-opt active" onclick="selectMethod('bKash')"><img id="bkashLogo" src="https://download.logo.wine/logo/BKash/bKash-Logo.wine.png" style="width:50px;height:30px;object-fit:contain"><div style="flex:1"><b>bKash Personal</b><div style="font-size:11px;color:#666">017xxxxxxxx</div></div><div>✓</div></div>
<div id="nagadOpt" class="withdraw-opt" onclick="selectMethod('Nagad')"><img id="nagadLogo" src="https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png" style="width:50px;height:30px;object-fit:contain"><div style="flex:1"><b>Nagad Personal</b><div style="font-size:11px;color:#666">018xxxxxxxx</div></div></div>
<input id="accNum" placeholder="আপনার বিকাশ/নগদ নাম্বার">
<input id="amount" type="number" placeholder="Amount Min 100">
<button class="btn purple" style="margin-top:12px" onclick="doWithdraw()">💸 Withdraw করুন</button>
<div style="margin-top:14px;padding-top:12px;border-top:1px dashed #ddd">
<p style="font-size:12px;margin:0 0 6px"><b>👑 এডমিন লোগো এডিট:</b></p>
<input type="file" id="editBkash" accept="image/*" style="font-size:11px"><div style="font-size:10px;color:#666">bKash লোগো চেঞ্জ</div>
<input type="file" id="editNagad" accept="image/*" style="font-size:11px;margin-top:6px"><div style="font-size:10px;color:#666">Nagad লোগো চেঞ্জ</div>
</div>
</div>
</div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center">
<img id="uPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:90px;height:90px;border-radius:50%;border:4px solid #8b5cf6;object-fit:cover">
<h2 id="uName" style="margin:8px 0 0">Riyad Ahmed</h2><p style="color:#666;font-size:13px">ID: 8807178385</p>
<button class="btn purple" onclick="openEdit()">✏️ নাম ও ছবি এডিট করুন</button>
</div>
</div>

<!-- Ad Overlay with Timer -->
<div id="adOverlay">
<h2 style="font-size:28px">⏳ বিজ্ঞাপন চলছে...</h2>
<div style="font-size:60px;font-weight:800" id="timer">15</div>
<p>অনুগ্রহ করে 15 সেকেন্ড অপেক্ষা করুন<br>Ad বন্ধ করবেন না, তাহলে টাকা পাবেন না</p>
<div style="background:#fff3;width:80%;height:8px;border-radius:20px;margin-top:14px;overflow:hidden"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div>
<button onclick="closeAdEarly()" style="margin-top:20px;background:transparent;border:1px solid #fff;color:#fff;padding:8px 18px;border-radius:20px">✕ বন্ধ করুন (টাকা পাবেন না)</button>
</div>

<div id="editModal" style="display:none;position:fixed;inset:0;background:#0008;z-index:200;justify-content:center;align-items:center">
<div style="background:#fff;width:90%;max-width:340px;padding:18px;border-radius:18px"><h3>✏️ প্রোফাইল এডিট</h3><input id="editName" placeholder="নতুন নাম"><input type="file" id="editPhoto" accept="image/*"><img id="prev" style="width:60px;height:60px;border-radius:50%;display:none;margin-top:10px;object-fit:cover"><button class="btn purple" style="margin-top:12px" onclick="saveProfile()">Save</button><button class="btn" style="margin-top:8px;background:#eee" onclick="closeEdit()">বন্ধ</button></div>
</div>

<div class="nav">
<div id="nav-home" class="active" onclick="go('home')"><div style="font-size:20px">🏠</div>Home</div>
<div id="nav-tasks" onclick="go('tasks')"><div style="font-size:20px">🎯</div>Tasks</div>
<div id="nav-invite" onclick="go('invite')"><div style="font-size:20px">👥</div>Invite</div>
<div id="nav-wallet" onclick="go('wallet')"><div style="font-size:20px">💰</div>Wallet</div>
<div id="nav-profile" onclick="go('profile')"><div style="font-size:20px">👤</div>Profile</div>
</div>

<script>
let bal=parseInt(localStorage.getItem('bal_final')||'61');
let adLeft=parseInt(localStorage.getItem('ad_final')||'12');
let adDone=parseInt(localStorage.getItem('ad_done_final')||'8');
let pic=localStorage.getItem('pic_final')||'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';
let name=localStorage.getItem('name_final')||'Riyad Ahmed';
let selected='bKash';
let timerInt=null;
let bkashLogoStored=localStorage.getItem('bkash_logo');
let nagadLogoStored=localStorage.getItem('nagad_logo');
function init(){
document.getElementById('balMain').innerText=bal+' TK';
document.getElementById('bal2').innerText=bal+' TK';
document.getElementById('adBadge').innerText='🎬 Ad: '+adLeft;
document.getElementById('adText').innerText=adLeft+'/20 বাকি';
document.getElementById('adProg').style.width=(adLeft/20*100)+'%';
document.getElementById('taskAd').innerText=adDone+'/10';
document.getElementById('topPic').src=pic;
document.getElementById('uPic').src=pic;
document.getElementById('uName').innerText=name;
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';
document.getElementById('refLink').innerText=link;
document.getElementById('refLink2').innerText=link;
if(bkashLogoStored) document.getElementById('bkashLogo').src=bkashLogoStored;
if(nagadLogoStored) document.getElementById('nagadLogo').src=nagadLogoStored;
}
function go(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav-'+p).classList.add('active')}
function watchAd(){
if(adLeft<=0){alert('আজকের লিমিট শেষ');return}
document.getElementById('adOverlay').style.display='flex';
let t=15; document.getElementById('timer').innerText=t;
timerInt=setInterval(()=>{
t--; document.getElementById('timer').innerText=t;
document.getElementById('timerProg').style.width=(t/15*100)+'%';
if(t<=0){clearInterval(timerInt); finishAd()}
},1000);
// Monetag Ad Call - Telegram Safe
if(typeof show_11760259==='function'){show_11760259().then(()=>{console.log('ad shown')}).catch(()=>{})}
}
function closeAdEarly(){clearInterval(timerInt);document.getElementById('adOverlay').style.display='none';alert('❌ Ad সম্পূর্ণ দেখেননি, টাকা পাননি!')}
function finishAd(){
document.getElementById('adOverlay').style.display='none';
bal+=2; adLeft--; adDone++;
localStorage.setItem('bal_final',bal);localStorage.setItem('ad_final',adLeft);localStorage.setItem('ad_done_final',adDone);
init();alert('✅ 2 TK যোগ হয়েছে! নতুন ব্যালেন্স: '+bal+' TK');
}
function doCheck(){bal+=5;localStorage.setItem('bal_final',bal);init();alert('✅ 5 TK Bonus!')}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ কপি হয়েছে!')}
function shareRef(){let l=document.getElementById('refLink').innerText;if(navigator.share)navigator.share({url:l});else copyRef()}
function selectMethod(m){selected=m;document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad')}
function doWithdraw(){
let n=document.getElementById('accNum').value;
let a=parseInt(document.getElementById('amount').value);
if(!n||!a){alert('নাম্বার ও Amount দিন');return}
if(a<100){alert('Min 100 TK');return}
if(a>bal){alert('ব্যালেন্স কম');return}
bal-=a;localStorage.setItem('bal_final',bal);init();alert('✅ '+a+' TK Withdraw Request!\\nMethod: '+selected+'\\nNumber: '+n+'\\n24h এ পাবেন');
}
// Logo Edit
document.getElementById('editBkash').addEventListener('change',function(e){let f=e.target.files[0];let r=new FileReader();r.onload=function(ev){localStorage.setItem('bkash_logo',ev.target.result);document.getElementById('bkashLogo').src=ev.target.result;alert('bKash লোগো চেঞ্জ হয়েছে!')};r.readAsDataURL(f)});
document.getElementById('editNagad').addEventListener('change',function(e){let f=e.target.files[0];let r=new FileReader();r.onload=function(ev){localStorage.setItem('nagad_logo',ev.target.result);document.getElementById('nagadLogo').src=ev.target.result;alert('Nagad লোগো চেঞ্জ হয়েছে!')};r.readAsDataURL(f)});
// Profile Edit
function openEdit(){document.getElementById('editModal').style.display='flex';document.getElementById('editName').value=name}
function closeEdit(){document.getElementById('editModal').style.display='none'}
document.getElementById('editPhoto').addEventListener('change',function(e){let f=e.target.files[0];let r=new FileReader();r.onload=function(ev){document.getElementById('prev').src=ev.target.result;document.getElementById('prev').style.display='block';document.getElementById('prev').dataset.b64=ev.target.result};r.readAsDataURL(f)});
function saveProfile(){let nn=document.getElementById('editName').value;let b64=document.getElementById('prev').dataset.b64;if(nn){name=nn;localStorage.setItem('name_final',nn)}if(b64){pic=b64;localStorage.setItem('pic_final',b64)}init();closeEdit();alert('✅ প্রোফাইল আপডেট!')}
init();
</script>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML
@app.get("/health")
async def health():
    return {"ok": True, "fix": "timer_15s_only_bkash_nagad_editable"}
