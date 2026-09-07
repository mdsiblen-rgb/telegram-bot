from flask import Flask
app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Diamond Kormo BD</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#070d0c;background-image:radial-gradient(circle at 20% 30%, rgba(0,255,148,0.15) 0%, transparent 50%);min-height:100vh;padding-bottom:90px;color:white}
.top{backdrop-filter:blur(12px);background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);margin:12px;border-radius:16px;padding:14px;display:flex;justify-content:space-between;align-items:center}
.glass{backdrop-filter:blur(16px);background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);margin:12px;border-radius:20px;padding:18px;box-shadow:0 8px 32px rgba(0,0,0,0.4)}
.btn{width:100%;padding:14px;background:linear-gradient(135deg,#00ff94,#00cc76);color:#003d25;border:0;border-radius:14px;font-weight:800;font-size:16px;cursor:pointer;margin-top:10px;box-shadow:0 0 18px rgba(0,255,148,0.4)}
.btn2{background:rgba(255,255,255,0.1);color:white;border:1px solid rgba(255,255,255,0.15)}
.nav{position:fixed;bottom:12px;left:12px;right:12px;background:rgba(15,25,23,0.95);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.12);border-radius:20px;display:flex;justify-content:space-around;padding:12px 0;z-index:999}
.nav div{color:rgba(255,255,255,0.6);cursor:pointer;font-size:13px;text-align:center}.active{color:#00ff94!important;font-weight:800}
.page{display:none}.active-page{display:block}
input,select{width:100%;padding:12px;margin-top:8px;border-radius:12px;border:1px solid rgba(255,255,255,0.15);background:rgba(0,0,0,0.3);color:white}
.pop{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:none;align-items:center;justify-content:center;z-index:1000}
.pop div{background:#111e1b;border:1px solid #00ff94;padding:24px;border-radius:20px;width:90%;max-width:350px;text-align:center}
.progress{width:100%;height:10px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden;margin-top:8px}.fill{height:100%;background:linear-gradient(90deg,#00ff94,#ffb700);transition:0.5s}
</style></head><body>
<div class="top"><div>💎 <b>Diamond Kormo BD</b><br><small>৳<span class="bal">715</span> | 💎<span class="dmd">715</span></small></div><div id="vipBadge" style="background:rgba(255,255,255,0.1);padding:6px 12px;border-radius:20px;font-size:12px">NORMAL</div></div>

<div id="home" class="active-page">
<div class="glass"><small>💼 বর্তমান ব্যালেন্স</small><div style="font-size:34px;font-weight:900">৳<span class="bal">715</span>.00</div><small id="perAd">প্রতি অ্যাড: ৳18 + 1💎</small>
<div style="display:flex;justify-content:space-between;margin-top:10px"><span>💎 VIP Progress</span><span><span class="dmd">715</span>/500</span></div><div class="progress"><div id="fill" class="fill" style="width:100%"></div></div>
<button id="vipBtn" class="btn" style="display:none;background:linear-gradient(135deg,#ffb700,#ff8c00);color:#3d1f00" onclick="becomeVip()">👑 VIP হোন (500💎)</button>
</div>

<div class="glass" style="text-align:center"><div style="font-size:14px;opacity:0.8">প্রতি বিজ্ঞাপনে আয় + ডায়মন্ড</div><div style="font-size:42px;font-weight:900">৳<span id="adPrice">18</span> + 1💎</div>
<div style="display:flex;gap:10px;margin-top:12px"><div style="flex:1;background:rgba(255,255,255,0.07);border-radius:14px;padding:10px">দেখেছেন<br><b><span class="cnt">0</span> টি</b></div><div style="flex:1;background:rgba(255,255,255,0.07);border-radius:14px;padding:10px">আজ আয়<br><b>৳<span class="today">0</span></b></div></div>
<button class="btn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button>
<button class="btn btn2" onclick="bonusAd()">🔥 বোনাস অ্যাড (100💎 = ৳30)</button>
<button class="btn btn2" onclick="convertDia()">💎➡৳ কনভার্ট (1000💎=৳100)</button>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px">
<div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);border-radius:16px;padding:14px;text-align:center" onclick="dailyBonus()">🎁<br>ডেইলি বোনাস<br><b style="color:#00ff94">৳50</b></div>
<div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);border-radius:16px;padding:14px;text-align:center" onclick="go('wd')">💳<br>উইথড্র<br><b>bKash/Nagad</b></div>
</div>
</div>

<div id="earn" class="page"><div class="glass">📄 আয় হিস্ট্রি<div id="hist" style="margin-top:10px;text-align:left;opacity:0.8">এখনো কোনো আয় নেই</div></div><button class="btn btn2" onclick="go('home')" style="margin:12px">⬅ হোম</button></div>
<div id="wd" class="page"><div class="glass" style="text-align:left">💳 উইথড্র - সর্বনিম্ন ৳500<br><select id="method"><option>bKash</option><option>Nagad</option><option>Rocket</option></select><input id="num" placeholder="01XXXXXXXXX নাম্বার দিন"><input id="amt" type="number" placeholder="টাকার পরিমান (500+)"><button class="btn" onclick="withdraw()">✅ উইথড্র রিকোয়েস্ট পাঠান</button></div><button class="btn btn2" onclick="go('home')" style="margin:12px">⬅ হোম</button></div>
<div id="pro" class="page"><div class="glass" style="text-align:left">👤 Diamond Kormo BD<br><br>ID: 8807178385<br>নাম: SHIBLI NOMAN<br>ব্যালেন্স: ৳<span class="bal">715</span><br>ডায়মন্ড: <span class="dmd">715</span><br>স্ট্যাটাস: <span id="status">NORMAL</span><br><br>💎 নিয়ম:<br>• 1 অ্যাড = ৳18 + 1💎<br>• VIP হলে ৳20<br>• 100💎 = বোনাস ৳30<br>• 1000💎 = ৳100<br>• লগইন বোনাস ৳50</div><button class="btn btn2" onclick="go('home')" style="margin:12px">⬅ হোম</button></div>

<div class="nav"><div id="n-home" class="active" onclick="go('home')">🏠<br>হোম</div><div id="n-earn" onclick="go('earn')">📄<br>আয়</div><div id="n-wd" onclick="go('wd')">💳<br>উইথড্র</div><div id="n-pro" onclick="go('pro')">👤<br>প্রোফাইল</div></div>
<div id="pop" class="pop"><div><h3 style="color:#00ff94">✅ সফল</h3><p id="popText" style="margin-top:10px;white-space:pre-line"></p><br><button class="btn" onclick="document.getElementById('pop').style.display='none'">OK</button></div></div>

<script>
let b=715,d=715,c=0,t=0,hist=[],isVip=false
function upd(){document.querySelectorAll('.bal').forEach(e=>e.innerText=b);document.querySelectorAll('.dmd').forEach(e=>e.innerText=d);document.querySelectorAll('.cnt').forEach(e=>e.innerText=c);document.querySelectorAll('.today').forEach(e=>e.innerText=t);let p=Math.min((d/500)*100,100);document.getElementById('fill').style.width=p+'%';if(d>=500 && !isVip){document.getElementById('vipBtn').style.display='block'} if(isVip){document.getElementById('adPrice').innerText='20';document.getElementById('perAd').innerText='VIP: ৳20 + 1💎';document.getElementById('vipBadge').innerText='👑 VIP';document.getElementById('vipBadge').style.background='#ffb700';document.getElementById('vipBadge').style.color='#3d1f00';document.getElementById('status').innerText='👑 VIP'}}
function pop(txt){document.getElementById('popText').innerText=txt;document.getElementById('pop').style.display='flex'}
function watchAd(){let earn=isVip?20:18;b+=earn;d+=1;c+=1;t+=earn;hist.unshift('+৳'+earn+' +1💎 - '+new Date().toLocaleTimeString());document.getElementById('hist').innerHTML=hist.join('<br>');upd();pop('✅ ৳'+earn+' + 1💎 পেয়েছেন!\\nব্যালেন্স: ৳'+b+' | 💎'+d)}
function bonusAd(){if(d<100)return pop('❌ 100💎 লাগবে! আছে '+d+'💎');d-=100;b+=30;upd();pop('🔥 বোনাস অ্যাড! ৳30 পেয়েছেন')}
function convertDia(){if(d<1000)return pop('❌ 1000💎 লাগবে! আছে '+d+'💎');d-=1000;b+=100;upd();pop('💎➡৳ কনভার্ট সফল! ৳100 যোগ')}
function becomeVip(){if(d<500)return;d-=500;isVip=true;upd();document.getElementById('vipBtn').style.display='none';pop('👑 VIP হয়েছেন! এখন থেকে প্রতি অ্যাডে ৳20')}
function dailyBonus(){let last=localStorage.getItem('daily');let today=new Date().toDateString();if(last==today)return pop('❌ আজকের বোনাস নিয়েছেন!');localStorage.setItem('daily',today);b+=50;d+=5;upd();pop('🎁 ডেইলি বোনাস ৳50 + 5💎!')}
function withdraw(){let m=document.getElementById('method').value,n=document.getElementById('num').value,a=document.getElementById('amt').value;if(!n||!a)return alert('নাম্বার ও টাকা দিন');if(a<500)return alert('সর্বনিম্ন ৳500');if(a>b)return alert('ব্যালেন্স কম');b-=a;upd();pop('✅ উইথড্র সফল!\\n'+m+': '+n+'\\n৳'+a+' - 24 ঘন্টায় পাবেন')}
function go(p){document.querySelectorAll('.page,.active-page').forEach(x=>x.className='page');document.getElementById(p).className='active-page';document.querySelectorAll('.nav div').forEach(x=>x.className='');let el=document.getElementById('n-'+p);if(el)el.className='active'}
window.onload=function(){let first=localStorage.getItem('firstLogin');if(!first){b+=50;d+=5;upd();localStorage.setItem('firstLogin','done');localStorage.setItem('loginDate',new Date().toDateString());pop('🎉 স্বাগতম Diamond Kormo BD তে!\\n\\n🎁 Welcome Bonus:\\n৳50 + 5💎 পেয়েছেন!\\n\\nএখন বিজ্ঞাপন দেখে আয় শুরু করুন!')}else{let last=localStorage.getItem('loginDate');let today=new Date().toDateString();if(last!=today){b+=10;d+=1;upd();localStorage.setItem('loginDate',today);pop('🎁 ডেইলি লগইন বোনাস!\\n৳10 + 1💎 পেয়েছেন!')}}}
upd();
</script></body></html>
"""
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def h(path): return HTML
if __name__ == '__main__': app.run(host='0.0.0.0',port=10000)
