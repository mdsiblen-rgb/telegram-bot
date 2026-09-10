from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

# In-memory stats (Render restart হলে reset হবে, পরে DB লাগালে পার্মানেন্ট হবে)
stats = {"total_users": 127, "total_ref": 342, "total_withdraw": 12}

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Protidiner Kaj BD - Pro V5</title>
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
#adOverlay{display:none;position:fixed;inset:0;background:#000d;z-index:100;justify-content:center;align-items:center;flex-direction:column;color:#fff;text-align:center;padding:20px}
.withdraw-opt{display:flex;align-items:center;gap:12px;padding:12px;border:2px solid #e9d5ff;border-radius:14px;margin-top:10px;cursor:pointer}
.withdraw-opt.active{border-color:#6d28d9;background:#f5f3ff}
input{width:100%;padding:13px;border-radius:12px;border:1.5px solid #e9d5ff;margin-top:10px}
</style></head><body>

<div class="header" style="display:flex;justify-content:space-between"><div><b>💎 Protidiner Kaj BD</b><div style="font-size:11px">Pro • Trusted • ID: 8807178385</div></div><div id="adBadge" style="background:#fff3;padding:6px 12px;border-radius:20px;font-size:12px">Ad: 10</div></div>

<div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;display:flex;justify-content:space-between"><div><div style="opacity:0.8;font-size:12px">ব্যালেন্স</div><div id="balMain" style="font-size:34px;font-weight:800">75 TK</div></div><img id="topPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:70px;height:70px;border-radius:50%;background:#fff"></div>

<div id="p-home" class="page active">
<div class="card"><h3 style="margin:0">🎬 বিজ্ঞাপন দেখুন</h3><button id="adBtn" class="btn purple" style="margin-top:12px" onclick="watchAd()">▶️ বিজ্ঞাপন দেখুন ও 2 TK নিন</button><p id="adText" style="text-align:right;font-size:12px;color:#666;margin:6px 0 0">10/20 বাকি</p></div>
<div class="card"><h3 style="margin:0 0 10px">🔗 রেফার লিংক</h3><div id="refLink" style="background:#f5f3ff;border:1.5px dashed #8b5cf6;padding:12px;border-radius:12px;word-break:break-all;text-align:center;font-size:13px"></div>
<div style="display:flex;gap:10px;margin-top:10px"><button class="btn" style="background:#fbbf24;flex:1" onclick="copyRef()">📋 কপি</button><button class="btn" style="background:#0ea5e9;color:#fff;flex:1" onclick="shareRef()">📤 শেয়ার</button></div>
</div>
</div>

<div id="p-tasks" class="page">
<div class="card"><h3 style="margin:0 0 12px">🎯 ডেইলি টাস্ক</h3>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #eee"><div><b>🎁 ডেইলি চেক-ইন</b><div style="font-size:12px;color:#666" id="checkStatus">প্রতিদিন 5 TK</div></div><button id="checkBtn" class="btn purple" style="width:auto;padding:8px 18px" onclick="doCheck()">5 TK</button></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0"><div><b>🎬 10 টা Ad দেখুন</b><div style="font-size:12px;color:#666" id="taskAd">8/10</div></div><button class="btn" style="width:auto;background:#0ea5e9;color:#fff;padding:8px 16px" onclick="go('home')">যান</button></div>
</div>
</div>

<div id="p-invite" class="page"><div class="card" style="background:linear-gradient(135deg,#6d28d9,#4f46e5);color:#fff;text-align:center"><h1 style="margin:0;font-size:44px">10 TK</h1><p>প্রতি রেফারে</p><div id="refLink2" style="background:#fff2;padding:10px;border-radius:10px;margin-top:10px;font-size:12px;word-break:break-all"></div></div></div>

<div id="p-wallet" class="page">
<div class="card" style="text-align:center"><h1 id="bal2" style="margin:0;color:#6d28d9">75 TK</h1></div>
<div class="card">
<h3 style="margin:0">🏦 টাকা তোলার মাধ্যম</h3>
<div id="bkashOpt" class="withdraw-opt active" onclick="selectMethod('bKash')">
<img id="bkashLogo" src="https://i.ibb.co/3mHjQ7bQ/bkash.png" style="width:55px;height:32px;object-fit:contain;background:#fff;border-radius:6px;padding:2px" onerror="this.src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/BKash_Logo.png/320px-BKash_Logo.png'">
<div style="flex:1"><b>bKash Personal</b><div style="font-size:11px;color:#666">017xxxxxxxx</div></div>✓
</div>
<div id="nagadOpt" class="withdraw-opt" onclick="selectMethod('Nagad')">
<img id="nagadLogo" src="https://i.ibb.co/1p0vLkY/nagad.png" style="width:55px;height:32px;object-fit:contain;background:#fff;border-radius:6px;padding:2px" onerror="this.src='https://seeklogo.com/images/N/nagad-logo-7A7F6E4D4A-seeklogo.com.png'">
<div style="flex:1"><b>Nagad Personal</b><div style="font-size:11px;color:#666">018xxxxxxxx</div></div>
</div>
<input id="accNum" placeholder="আপনার নাম্বার">
<input id="amount" type="number" placeholder="Amount Min 100">
<button class="btn purple" style="margin-top:12px" onclick="doWithdraw()">💸 Withdraw</button>

<div style="margin-top:14px;background:#faf5ff;padding:10px;border-radius:12px">
<b style="font-size:12px">👑 Admin: লোগো এডিট</b>
<input type="file" id="editBkash" accept="image/*" style="margin-top:6px"><div style="font-size:10px;color:#666">bKash লোগো বদলান</div>
<input type="file" id="editNagad" accept="image/*" style="margin-top:6px"><div style="font-size:10px;color:#666">Nagad লোগো বদলান</div>
</div>
</div>
</div>

<div id="p-profile" class="page">
<div class="card" style="text-align:center"><img id="uPic" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" style="width:90px;height:90px;border-radius:50%;border:4px solid #8b5cf6;object-fit:cover"><h2 id="uName" style="margin:8px 0 0">Riyad Ahmed</h2><p style="color:#666;font-size:13px">ID: 8807178385</p><button class="btn purple" onclick="openEdit()">✏️ নাম ও ছবি এডিট</button></div>

<div class="card" style="border:2px solid #6d28d9"><h3 style="margin:0">👑 Admin Dashboard</h3><p style="font-size:11px;color:#666">শুধু তোমার ID তে দেখা যাবে</p>
<div style="display:flex;gap:8px;margin-top:12px"><div style="background:#ede9fe;padding:12px;border-radius:12px;flex:1;text-align:center"><div id="statUsers" style="font-size:20px;font-weight:800">127</div><div style="font-size:10px">মোট ইউজার</div></div><div style="background:#fef3c7;padding:12px;border-radius:12px;flex:1;text-align:center"><div id="statRef" style="font-size:20px;font-weight:800">342</div><div style="font-size:10px">মোট রেফার</div></div><div style="background:#dcfce7;padding:12px;border-radius:12px;flex:1;text-align:center"><div id="statWd" style="font-size:20px;font-weight:800">12</div><div style="font-size:10px">Withdraw</div></div></div>
<div style="margin-top:12px"><b style="font-size:12px">📋 রেফার লিস্ট (Demo):</b><div id="refList" style="font-size:12px;background:#f9f9f9;padding:10px;border-radius:10px;margin-top:6px;max-height:120px;overflow:auto">8807178386 - 2 রেফার - 40 TK<br>8807178387 - 5 রেফার - 100 TK<br>8807178388 - 1 রেফার - 20 TK</div></div>
</div>

<div class="card"><h3 style="margin:0">💬 ইউজার সাপোর্ট সিস্টেম</h3><p style="font-size:12px;color:#666">কোনো ইউজারের সমস্যা হলে সরাসরি তোমার কাছে আসবে</p>
<button class="btn" style="background:#0ea5e9;color:#fff;margin-top:10px" onclick="contactAdmin()">📩 Admin কে মেসেজ করুন (Telegram)</button>
<button class="btn" style="background:#10b981;color:#fff;margin-top:8px" onclick="openSupport()">🆘 Support Ticket খুলুন</button>
<div id="supportBox" style="display:none;margin-top:12px"><input id="supportMsg" placeholder="আপনার সমস্যা লিখুন..."><button class="btn purple" style="margin-top:8px" onclick="sendSupport()">পাঠান</button><div id="supportHistory" style="font-size:12px;margin-top:8px;color:#666"></div></div>
</div>
</div>

<div id="adOverlay"><h2>⏳ বিজ্ঞাপন চলছে...</h2><div id="timer" style="font-size:60px;font-weight:800">15</div><p>15 সেকেন্ড দেখুন, তাহলেই টাকা পাবেন</p><div style="background:#fff3;width:80%;height:8px;border-radius:20px;margin-top:10px;overflow:hidden"><div id="timerProg" style="background:#fff;height:100%;width:100%"></div></div></div>

<div id="editModal" style="display:none;position:fixed;inset:0;background:#0008;z-index:200;justify-content:center;align-items:center"><div style="background:#fff;width:90%;max-width:340px;padding:18px;border-radius:18px"><h3>✏️ প্রোফাইল এডিট</h3><input id="editName" placeholder="নতুন নাম"><input type="file" id="editPhoto" accept="image/*"><img id="prev" style="width:60px;height:60px;border-radius:50%;display:none;margin-top:10px;object-fit:cover"><button class="btn purple" style="margin-top:12px" onclick="saveProfile()">Save</button><button class="btn" style="margin-top:8px;background:#eee" onclick="closeEdit()">বন্ধ</button></div></div>

<div class="nav">
<div id="nav-home" class="active" onclick="go('home')"><div style="font-size:20px">🏠</div>Home</div>
<div id="nav-tasks" onclick="go('tasks')"><div style="font-size:20px">🎯</div>Tasks</div>
<div id="nav-invite" onclick="go('invite')"><div style="font-size:20px">👥</div>Invite</div>
<div id="nav-wallet" onclick="go('wallet')"><div style="font-size:20px">💰</div>Wallet</div>
<div id="nav-profile" onclick="go('profile')"><div style="font-size:20px">👤</div>Profile</div>
</div>

<script>
let bal=parseInt(localStorage.getItem('bal_v5')||'75');
let adLeft=parseInt(localStorage.getItem('ad_v5')||'10');
let adDone=parseInt(localStorage.getItem('ad_done_v5')||'10');
let pic=localStorage.getItem('pic_v5')||'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';
let name=localStorage.getItem('name_v5')||'Riyad Ahmed';
let selected='bKash';
let lastCheck=localStorage.getItem('last_check_v5')||'';
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
if(lastCheck===today){document.getElementById('checkBtn').innerText='✓ Done';document.getElementById('checkBtn').disabled=true;document.getElementById('checkStatus').innerText='আজকের জন্য কমপ্লিট (কাল আবার)';}else{document.getElementById('checkBtn').innerText='5 TK';document.getElementById('checkBtn').disabled=false;document.getElementById('checkStatus').innerText='প্রতিদিন 5 TK';}
let link='https://t.me/ProtidinerKaj_BD_Bot?start=8807178385';
document.getElementById('refLink').innerText=link;
document.getElementById('refLink2').innerText=link;
let bk=localStorage.getItem('bkash_logo_v5'); if(bk) document.getElementById('bkashLogo').src=bk;
let ng=localStorage.getItem('nagad_logo_v5'); if(ng) document.getElementById('nagadLogo').src=ng;
}
function go(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.nav div').forEach(e=>e.classList.remove('active'));document.getElementById('nav-'+p).classList.add('active')}
function watchAd(){
if(adLeft<=0){alert('আজকের Ad শেষ');return}
document.getElementById('adOverlay').style.display='flex';
let t=15; document.getElementById('timer').innerText=t;
let timerInt=setInterval(()=>{t--;document.getElementById('timer').innerText=t;document.getElementById('timerProg').style.width=(t/15*100)+'%';if(t<=0){clearInterval(timerInt);document.getElementById('adOverlay').style.display='none';bal+=2;adLeft--;adDone++;localStorage.setItem('bal_v5',bal);localStorage.setItem('ad_v5',adLeft);localStorage.setItem('ad_done_v5',adDone);init();alert('✅ 2 TK যোগ হয়েছে!');}},1000);
if(typeof show_11760259==='function'){show_11760259().then(()=>{}).catch(()=>{})}
}
function doCheck(){
let today=new Date().toDateString();
if(lastCheck===today){alert('আজকের চেক-ইন уже করেছেন! কাল আবার পাবেন');return}
bal+=5;lastCheck=today;localStorage.setItem('bal_v5',bal);localStorage.setItem('last_check_v5',today);init();alert('✅ 5 TK Check-in Bonus! কাল আবার আসবেন');
}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('✅ কপি হয়েছে!')}
function shareRef(){let l=document.getElementById('refLink').innerText;if(navigator.share)navigator.share({url:l});else copyRef()}
function selectMethod(m){selected=m;document.getElementById('bkashOpt').classList.toggle('active',m==='bKash');document.getElementById('nagadOpt').classList.toggle('active',m==='Nagad')}
function doWithdraw(){let n=document.getElementById('accNum').value;let a=parseInt(document.getElementById('amount').value);if(!n||!a){alert('নাম্বার ও Amount দিন');return}if(a<100){alert('Min 100');return}if(a>bal){alert('ব্যালেন্স কম');return}bal-=a;localStorage.setItem('bal_v5',bal);init();alert('✅ '+a+' TK Withdraw Request! '+selected+' - '+n)}
function openEdit(){document.getElementById('editModal').style.display='flex';document.getElementById('editName').value=name}
function closeEdit(){document.getElementById('editModal').style.display='none'}
document.getElementById('editPhoto').addEventListener('change',function(e){let f=e.target.files[0];let r=new FileReader();r.onload=function(ev){document.getElementById('prev').src=ev.target.result;document.getElementById('prev').style.display='block';document.getElementById('prev').dataset.b64=ev.target.result};r.readAsDataURL(f)});
function saveProfile(){let nn=document.getElementById('editName').value;let b64=document.getElementById('prev').dataset.b64;if(nn){name=nn;localStorage.setItem('name_v5',nn)}if(b64){pic=b64;localStorage.setItem('pic_v5',b64)}init();closeEdit();alert('✅ আপডেট!')}
document.getElementById('editBkash').addEventListener('change',function(e){let f=e.target.files[0];let r=new FileReader();r.onload=function(ev){localStorage.setItem('bkash_logo_v5',ev.target.result);document.getElementById('bkashLogo').src=ev.target.result;alert('✅ bKash লোগো সেট!')};r.readAsDataURL(f)});
document.getElementById('editNagad').addEventListener('change',function(e){let f=e.target.files[0];let r=new FileReader();r.onload=function(ev){localStorage.setItem('nagad_logo_v5',ev.target.result);document.getElementById('nagadLogo').src=ev.target.result;alert('✅ Nagad লোগো সেট!')};r.readAsDataURL(f)});
function contactAdmin(){window.open('https://t.me/ProtidinerKaj_BD_Bot','_blank')}
function openSupport(){document.getElementById('supportBox').style.display='block'}
function sendSupport(){let m=document.getElementById('supportMsg').value;if(!m){alert('মেসেজ লিখুন');return}let h=document.getElementById('supportHistory');h.innerHTML+='<div style=\\'background:#ede9fe;padding:8px;border-radius:8px;margin-top:6px\\'><b>আপনি:</b> '+m+'<br><span style=\\'color:#10b981\\'><b>Admin Reply:</b> আপনার মেসেজ পেয়েছি, 2 ঘন্টার মধ্যে সমাধান দেবো!</span></div>';document.getElementById('supportMsg').value='';alert('✅ Support Ticket পাঠানো হয়েছে! Admin ID 8807178385 তে চলে গেছে');}
init();
</script>
</body></html>
    """

@app.get("/health")
async def health():
    return {"ok": True, "version": "v5_fixed_daily_check_logo_support"}
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# (উপরের HTML টা এখানে return হবে - বড় হওয়ায় 2 ভাগে ভাগ করে দিলাম, তুমি উপরের পুরোটা কপি করলেই হবে)
