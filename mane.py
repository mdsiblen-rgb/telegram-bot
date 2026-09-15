@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='https://telegram.org/js/telegram-web-app.js'></script>
<script src='//libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
<style>
:root{--p:{{s["primary"]}};--s:{{s["secondary"]}}}
body{margin:0;background:#0A0D1E;color:#fff;font-family:system-ui;padding:0 12px 90px}
.card{background:#151A2D;border:1px solid #1e293b;border-radius:20px;padding:14px;margin:12px 0}
.b{width:100%;padding:13px;border-radius:12px;background:#8b5cf6;color:#fff;border:none;font-weight:700;cursor:pointer}
.by{background:#f59e0b;color:#000}.bd{background:#0B0E1C;border:1px solid #333;color:#fff}
.nav{position:fixed;bottom:0;left:0;right:0;background:#151A2D;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1e293b;z-index:99}
.nav div{text-align:center;font-size:11px;opacity:.6;cursor:pointer}.nav div.active{opacity:1;color:#8b5cf6}
input{width:100%;padding:12px;border-radius:12px;background:#0B0E1C;color:#fff;border:1px solid #333;box-sizing:border-box;margin-top:8px}
.tab{display:none}.tab.active{display:block}
</style></head><body>

<div style='display:flex;gap:8px;padding:12px 0;align-items:center'>
<div class='card' style='margin:0;padding:8px 12px'>💎</div>
<div class='card' style='margin:0;flex:1'>👑 {{s["app_name"]}}</div>
<div class='card' style='margin:0;flex:1;border:1px solid #f59e0b'>{{s["app_name2"]}}</div>
<div style='color:#00ff88;font-weight:700' id='balTop'>৳0</div>
</div>

<!-- HOME TAB -->
<div id='tab-home' class='tab active'>
  <div class='card'>
    <div style='display:flex;justify-content:space-between'><span style='color:#8b5cf6'>Diamond Member • Level <span id='lvl'>1</span></span><span>Total Balance</span></div>
    <h2 style='margin:6px 0'>Good Evening, <span id='uname'>User</span>!</h2>
    <div style='display:flex;justify-content:space-between'><span>💎 <span id='dia'>0</span> Diamond | 100=৳1</span><span style='color:#00ff88;font-size:22px'>৳<span id='bal'>0</span></span></div>
    <div style='text-align:right;color:#f59e0b;font-size:12px'><span id='adsCount'>0/80</span> Ads</div>
  </div>
  <div style='display:flex;gap:10px'>
    <div class='card' style='flex:1'><div style='display:flex;justify-content:space-between'>Company Ads <span style='color:#f59e0b'>৳{{s["ad"]}}</span></div><small id='cCount'>0/{{s["clim"]}} today</small><button class='b' onclick='watchAd("c")'>Start - ৳{{s["ad"]}}</button></div>
    <div class='card' style='flex:1'><div style='display:flex;justify-content:space-between'>Popup Ads <span style='color:#f59e0b'>৳{{s["pop"]}}</span></div><small id='pCount'>0/{{s["plim"]}} today</small><button class='b by' onclick='watchAd("p")'>Watch - ৳{{s["pop"]}}</button></div>
  </div>
  <div class='card'><h3 style='margin:0 0 10px'>💸 Withdraw</h3><div style='display:flex;gap:8px'><button class='b bd' id='bkBtn'>bKash</button><button class='b bd' id='ngBtn'>Nagad</button></div><input id='wdNum' placeholder='01XXXXXXXXX'><input id='wdAmt' type='number' placeholder='Min {{s["min"]}} Taka'><button class='b' onclick='doWD()'>Withdraw Now</button><p style='color:#666;font-size:12px'>No history</p></div>
  <div class='card' style='background:linear-gradient(135deg,#2d1b69,#1a0f3d);border:1px solid #f59e0b'><div style='display:flex;justify-content:space-between'><span style='background:#f59e0b;color:#000;padding:4px 12px;border-radius:20px;font-size:12px'>🔥 SPONSORED • BIGGEST AD</span><small>Monetag Active</small></div><h2>🔥 {{s["spon_title"]}}</h2><p style='white-space:pre-line'>{{s["spon_desc"]}}</p><button class='b by' onclick='Telegram.WebApp.openLink(S.spon_link)'>{{s["spon_btn"]}}</button></div>
</div>

<!-- TASKS TAB -->
<div id='tab-tasks' class='tab'>
  <div class='card'><h2 style='margin:0'>🎯 Tasks & Company Links</h2><p style='color:#888'>প্রতি Task এ ৳20-25 + Diamond</p><div id='taskList'></div></div>
</div>

<!-- REFER TAB -->
<div id='tab-refer' class='tab'>
  <div class='card' style='background:linear-gradient(90deg,#f59e0b,#ff8c00);color:#000'><b>🎉 {{s["ref_banner"]}}</b></div>
  <div class='card'><h2 style='margin:0'>👥 {{s["ref_title"]}}</h2><p style='color:#888'>{{s["ref_desc"]}}</p>
    <div style='display:flex;gap:8px'><div class='card bd' style='flex:1;text-align:center'><div style='font-size:22px;color:#8b5cf6' id='rTotal'>0</div>Total Refer</div><div class='card bd' style='flex:1;text-align:center'><div style='font-size:22px;color:#0f0' id='rEarn'>৳0</div>Earned</div><div class='card bd' style='flex:1;text-align:center'><div style='font-size:22px;color:#f59e0b'>15%</div>Commission</div></div>
    <div class='card bd' style='word-break:break-all;font-size:12px' id='refLink'>https://...</div><button class='b' onclick='copyRef()'>🔗 Copy Refer Link</button>
  </div>
  <div class='card'><h3>📋 How Refer Works</h3><p style='white-space:pre-line'>{{s["ref_rules"]}}</p></div>
  <div class='card'><h3>👥 My Refer List</h3><p style='color:#888' id='refList'>No refer yet</p></div>
</div>

<!-- SUPPORT TAB -->
<div id='tab-support' class='tab'>
  <div class='card'><h2>💎 {{s["sup_title"]}}</h2><p style='color:#888'>{{s["sup_desc"]}}</p></div>
  <div class='card'><h3>📞 Contact Us</h3><div style='display:flex;gap:8px'><button class='b' onclick='Telegram.WebApp.openLink(S.sup_tg)'>✈️ Telegram</button><button class='b by' onclick='Telegram.WebApp.openLink(S.sup_wa)'>💬 WhatsApp</button></div><div class='card bd' style='margin-top:10px'>📧 Email: {{s["sup_email"]}}</div></div>
  <div class='card' style='border:1px solid #f59e0b;background:#1a1500'><h3>📢 Notice Board</h3><p style='white-space:pre-line'>{{s["sup_notice"]}}</p></div>
  <div class='card'><h3>❓ FAQ</h3><details class='card bd'><summary>{{s["sup_faq1_q"]}}</summary><p>{{s["sup_faq1_a"]}}</p></details><details class='card bd'><summary>{{s["sup_faq2_q"]}}</summary><p>{{s["sup_faq2_a"]}}</p></details><details class='card bd'><summary>{{s["sup_faq3_q"]}}</summary><p>{{s["sup_faq3_a"]}}</p></details></div>
  <div class='card'><h3>📜 Rules</h3><p style='white-space:pre-line'>{{s["sup_rules"]}}</p></div>
</div>

<!-- PROFILE TAB -->
<div id='tab-profile' class='tab'>
  <div class='card' style='text-align:center'><div style='width:80px;height:80px;background:#0B0E1C;border:2px solid #8b5cf6;border-radius:20px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:40px'>💎</div><div style='background:#f59e0b;color:#000;display:inline-block;padding:2px 12px;border-radius:20px;font-size:12px;margin-top:10px'>Level <span id='pLvl'>1</span></div><h2 style='margin:8px 0' id='pName'>User 4250</h2><small>Join: <span id='pJoin'>2026-09-15</span></small><br><small>💎 <span id='pDia'>2000</span> Diamond | <span id='pBal'>20</span> Taka</small></div>
  <div class='card'><h3>📊 Statistics</h3><div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'><div class='card bd' style='text-align:center'><div style='color:#0f0;font-size:20px'>৳<span id='sEarn'>20</span></div>Total Earned</div><div class='card bd' style='text-align:center'><div style='color:#8b5cf6;font-size:20px'>৳<span id='sBal'>20</span></div>Balance</div><div class='card bd' style='text-align:center'><div style='color:#f59e0b;font-size:20px' id='sAds'>0</div>Ads</div><div class='card bd' style='text-align:center'><div style='color:#ff5a9a;font-size:20px' id='sRef'>0</div>Refer</div></div></div>
  <div class='card'><h3>📈 Level Progress</h3><div style='display:flex;justify-content:space-between'><span>Level <span id='lpLvl'>1</span></span><span>Next: ৳<span id='lpNext'>500</span></span></div><div style='background:#0B0E1C;height:10px;border-radius:10px;margin:8px 0'><div id='lpBar' style='height:10px;background:#8b5cf6;width:10%;border-radius:10px'></div></div><small>💎 Diamond Member - Level বাড়ান, বেশি ইনকাম করুন!</small></div>
  <div class='card'><h3>⚙️ Account</h3><div class='card bd'>User ID<br><b id='accId'>8807178385_4250</b></div><div class='card bd'><span id='accName'>User 4250</span></div><input type='file' id='fileIn'><button class='b' onclick='saveProfile()'>💾 Save Profile</button></div>
  <div class='card'><h3>💸 Withdraw History</h3><p style='color:#888'>No withdraw</p></div>
</div>

<div class='nav'>
  <div id='n-home' class='active' onclick="openTab('home')">🏠<br>Home</div>
  <div id='n-tasks' onclick="openTab('tasks')">🎯<br>Tasks</div>
  <div id='n-refer' onclick="openTab('refer')">👥<br>Refer</div>
  <div id='n-support' onclick="openTab('support')">💬<br>Support</div>
  <div id='n-profile' onclick="openTab('profile')">👤<br>Profile</div>
</div>

<script>
const S={{s|tojson}}; let curM='bKash';
function openTab(name){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.nav div').forEach(n=>n.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  document.getElementById('n-'+name).classList.add('active');
}
document.getElementById('bkBtn').onclick=function(){curM='bKash'; this.style.borderColor='#8b5cf6'; document.getElementById('ngBtn').style.borderColor='#333'};
document.getElementById('ngBtn').onclick=function(){curM='Nagad'; this.style.borderColor='#8b5cf6'; document.getElementById('bkBtn').style.borderColor='#333'};
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Link Copied')}
function watchAd(type){
  let zone=type=='c'?`show_{{s["company_ad_id"]}}`:`show_{{s["popup_ad_id"]}}`;
  if(typeof window[zone]==='function'){
    window[zone]().then(()=>{
      fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,type:type})}).then(r=>r.json()).then(d=>{
        if(d.bal!==undefined){document.getElementById('bal').innerText=d.bal; document.getElementById('balTop').innerText='৳'+d.bal; document.getElementById('sBal').innerText=d.bal; document.getElementById('pBal').innerText=d.bal; document.getElementById('dia').innerText=d.diamonds; document.getElementById('pDia').innerText=d.diamonds;}
        document.getElementById('cCount').innerText=(d.c_today||0)+'/'+S.clim+' today'; document.getElementById('pCount').innerText=(d.p_today||0)+'/'+S.plim+' today';
        alert(d.msg)
      })
    })
  } else {alert('Ad not ready - ID Safe')}
}
function doWD(){
  let amt=document.getElementById('wdAmt').value, num=document.getElementById('wdNum').value;
  fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id,amt:amt,num:num,m:curM})}).then(r=>r.json()).then(d=>alert(d.msg))
}
function saveProfile(){alert('Profile Saved')}
fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:(Telegram.WebApp.initDataUnsafe.user||{id:'8807178385_4250'}).id})}).then(r=>r.json()).then(d=>{
  document.getElementById('bal').innerText=d.user.bal; document.getElementById('balTop').innerText='৳'+d.user.bal; document.getElementById('sBal').innerText=d.user.bal; document.getElementById('pBal').innerText=d.user.bal; document.getElementById('sEarn').innerText=d.user.total;
  document.getElementById('dia').innerText=d.user.diamonds; document.getElementById('pDia').innerText=d.user.diamonds;
  document.getElementById('uname').innerText=d.user.name; document.getElementById('pName').innerText=d.user.name; document.getElementById('accName').innerText=d.user.name; document.getElementById('accId').innerText=d.user.id;
  document.getElementById('lvl').innerText=d.level; document.getElementById('pLvl').innerText=d.level; document.getElementById('lpLvl').innerText=d.level; document.getElementById('lpNext').innerText=d.next; document.getElementById('lpBar').style.width=d.prog+'%';
  document.getElementById('pJoin').innerText=d.user.join; document.getElementById('sAds').innerText=(d.user.c_today||0)+(d.user.p_today||0); document.getElementById('sRef').innerText=d.user.refl.length; document.getElementById('rTotal').innerText=d.user.refl.length;
  document.getElementById('refLink').innerText=location.origin+'/?ref='+d.user.id;
  let h=''; d.tasks.forEach(t=>{h+=`<div style='display:flex;justify-content:space-between;align-items:center;background:#0B0E1C;padding:12px;margin:8px 0;border-radius:14px'><div>📢 ${t.title}<br><small style='color:#0f0'>৳${t.reward} + 💎${t.reward*100}</small></div><button style='width:auto;padding:8px 16px;background:#8b5cf6;border:none;border-radius:10px;color:#fff' onclick="Telegram.WebApp.openLink('${t.link}')">Go</button></div>`}); document.getElementById('taskList').innerHTML=h;
  if(d.user.refl.length>0){document.getElementById('refList').innerText=d.user.refl.join(', ')}
  document.getElementById('cCount').innerText=(d.user.c_today||0)+'/'+S.clim+' today'; document.getElementById('pCount').innerText=(d.user.p_today||0)+'/'+S.plim+' today'; document.getElementById('adsCount').innerText=(d.user.c_today+d.user.p_today)+'/80';
})
</script></body></html>
    """, s=s)
