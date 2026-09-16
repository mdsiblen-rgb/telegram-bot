from flask import Flask, request, jsonify, render_template_string
import json, os, base64
from datetime import datetime
app = Flask(__name__)
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "settings": {
            "app_name": "প্রতিদিনের কাজ বিডি",
            "primary": "#8b5cf6", "secondary": "#f59e0b",
            "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 30, "min": 500, "ref": 10,
            "company_ad_id": "11764581", "popup_ad_id": "11798857",
            "direct_link1": "https://omg10.com/4/11760259",
            "direct_link2": "",
            "home_corner_diamond": "💎",
            "home_small_diamond_icon": "💎",
            "home_diamond_big_size": "28",
            "home_name_font_size": "20",
            "spon_title": "Biggest Earning Offer", "spon_desc": "প্রতিদিন কাজ করে আয় করুন, বড় বোনাস নিন", "spon_link": "https://google.com", "spon_btn": "🚀 Claim Now", "spon_big_height": "180",
            "task_page_title": "Tasks & Company Links", "task_page_sub": "প্রতি Task এ ৳20-25 + Diamond",
            "task_bottom_title": "🔥 Special Offer", "task_bottom_desc": "এই বক্স Admin থেকে চেঞ্জ হবে", "task_bottom_btn": "Claim Now", "task_bottom_link": "https://google.com",
            "ref_title": "Refer & Earn", "ref_desc": "বন্ধুদের Invite করে Unlimited আয়", "ref_banner": "🎉 Refer Contest চলছে! - ৳5000 পুরস্কার", "ref_rules": "1. বন্ধুকে লিংক শেয়ার করো\n2. বন্ধু Join করলে ৳20 পাবে\n3. বন্ধু Ads দেখলে 15% Commission পাবে",
            "refer_bottom_title": "🔥 Refer Special Bonus", "refer_bottom_desc": "এখানে Admin থেকে যেকোনো লিংক/অফার লিখতে পারবে", "refer_bottom_btn": "Join Now", "refer_bottom_link": "https://google.com",
            "sup_title": "Support Center", "sup_desc": "যেকোনো সমস্যায় যোগাযোগ করুন - 24/7", "sup_tg": "https://t.me/dailyworkbd", "sup_wa": "https://wa.me/8801", "sup_fb": "https://facebook.com", "sup_email": "support@dailyworkbd.com",
            "sup_notice": "⚠️ রাত ১০টার পর Withdraw বন্ধ থাকে\n✅ সকাল ৯টার পর আবার চালু হয়\n📢 Fake Account করলে ব্যান",
            "sup_faq1_q": "Withdraw কতক্ষণে পাবো?", "sup_faq1_a": "২৪ ঘণ্টার ভিতরে পেমেন্ট করা হয়",
            "sup_faq2_q": "Refer টাকা কখন পাবো?", "sup_faq2_a": "বন্ধু Join করলেই সাথে সাথে",
            "sup_faq3_q": "Ads দেখলে টাকা আসে না কেন?", "sup_faq3_a": "VPN বন্ধ করে আবার চেষ্টা করুন",
            "sup_rules": "1. একাধিক একাউন্ট খুলবেন না\n2. ভুল তথ্য দিবেন না\n3. Fake Refer করবেন না\n4. Admin এর সিদ্ধান্তই চূড়ান্ত",
            "support_bottom_title": "📢 Important Update", "support_bottom_desc": "এই জায়গাটা Admin থেকে কন্ট্রোল করতে পারবে", "support_bottom_btn": "Contact Now", "support_bottom_link": "https://t.me/",
            "profile_bottom_title": "💎 VIP Membership - বড় বক্স", "profile_bottom_desc": "VIP হলে বেশি ইনকাম পাবেন। Admin থেকে অফার লিখুন", "profile_bottom_btn": "⭐ Upgrade Now", "profile_bottom_link": "https://google.com"
        }, "tasks": [
            {"id":"t1","icon":"🌐","title":"Visit Company Website - ৳20","reward":0.2,"link":"https://google.com"},
            {"id":"t2","icon":"▶️","title":"Watch Video - ৳25","reward":0.25,"link":"https://youtube.com"},
            {"id":"t3","icon":"📢","title":"Join Telegram - ৳30","reward":0.3,"link":"https://t.me/"}
        ], "wds": []}
    with open(DB_FILE,"r") as f: return json.load(f)
def save_db(db):
    with open(DB_FILE,"w") as f: json.dump(db,f,indent=2)

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    return render_template_string(f"""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='//libtl.com/sdk.js' data-zone='{s["company_ad_id"]}' data-sdk='show_{s["company_ad_id"]}'></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}
body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}}
.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}}
.top2{{display:flex;gap:10px;margin:12px;align-items:center}}
.topbox{{flex:1;background:#151A2D;border:1px solid #8b5cf6;padding:12px;border-radius:14px;font-weight:700;font-size:14px}}
.cornerDiamond{{width:58px;height:58px;background:linear-gradient(135deg,#1A2040,#2D1B4E);border:2px solid #8b5cf6;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:34px;box-shadow:0 0 20px rgba(139,92,246,.6)}}
.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{s['primary']};cursor:pointer;margin-top:10px;font-size:16px}}
.meth{{flex:1;padding:12px;border-radius:14px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C;font-weight:800}}.meth.on{{border-color:{s['primary']};background:rgba(139,92,246,.25)}}
.inputDark{{width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px}}
.task-card{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:#0F1429;border:1px solid #1e293b;border-radius:18px;margin:10px 12px}}
.proImg{{width:92px;height:92px;border-radius:22px;background:#0B0E1C;border:2px solid #8b5cf6;display:flex;align-items:center;justify-content:center;font-size:40px;overflow:hidden;margin:0 auto}}
.stat4{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}}.stat4 div{{background:#0B0E1C;border:1px solid #1e293b;padding:14px;border-radius:16px;text-align:center}}
.spon-big{{background:linear-gradient(135deg,#2D1B4E,#1A1033);border:2px solid #f59e0b;padding:32px 20px;border-radius:26px;margin:16px;min-height:{s['spon_big_height']}px}}
.contest{{background:linear-gradient(90deg,#f59e0b,#f97316);color:#000;padding:14px;border-radius:18px;margin:12px;text-align:center;font-weight:800}}
.page{{display:none}}.page.active{{display:block}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:22px;display:block}}
</style></head><body>

<div id='p-home' class='page active'>
  <div class='top2'>
    <div class='cornerDiamond'>{s['home_corner_diamond']}</div>
    <div class='topbox'>👑 {s['app_name']}</div>
    <div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span style='float:right;color:#22c55e' id='balTopRight'>৳20.3</span></div>
  </div>
  <div class='glass'>
    <div style='display:flex;justify-content:space-between;align-items:center'>
      <span style='color:#a78bfa;font-size:{s['home_name_font_size']}px;font-weight:800'>Diamond Member • Level 1</span>
      <div style='text-align:right'><span style='opacity:.7;font-size:13px'>Balance</span><br><b id='balTopBalance' style='color:#22c55e;font-size:20px'>৳20.3</b></div>
    </div>
    <b id='balShow' style='color:#22c55e;font-size:34px;display:block;margin-top:8px'>৳20.3</b>
    <div style='margin-top:10px;display:flex;align-items:center;gap:10px'>
      <span style='font-size:{s['home_diamond_big_size']}px'>{s['home_small_diamond_icon']}</span>
      <span style='font-size:19px;font-weight:800;opacity:.95'><span id='diamondTop'>2030</span> Diamond | <span id='adsCount'>0/80</span> Ads</span>
    </div>
  </div>
  <div style='display:flex;gap:10px;margin:0 12px'>
    <div class='glass' style='flex:1;margin:0'><b>Company Ads <span style='color:#f59e0b'>৳{s['ad']}</span></b><br><small id='cToday'>0/{s['clim']}</small><button class='btn' onclick='watchAd("c")'>Start - ৳{s['ad']}</button></div>
    <div class='glass' style='flex:1;margin:0'><b>Popup Ads <span style='color:#f59e0b'>৳{s['pop']}</span></b><br><small id='pToday'>0/{s['plim']}</small><button class='btn' style='background:{s['secondary']};color:#000' onclick='watchAd("p")'>Watch - ৳{s['pop']}</button></div>
  </div>
  <div class='glass'><h3>💸 Withdraw</h3><div style='display:flex;gap:10px;margin-top:12px'><div class='meth on' id='m-bKash' onclick="setMeth('bKash')">bKash</div><div class='meth' id='m-Nagad' onclick="setMeth('Nagad')">Nagad</div></div><input id='wNum' class='inputDark' placeholder='01XXXXXXXXXX' /><input id='wAmt' class='inputDark' type='number' placeholder='Min {s['min']}' /><button class='btn' onclick='doWD()'>Withdraw Now</button></div>
  <div class='spon-big'><h2 style='font-size:26px'>🔥🔥 {s['spon_title'].replace('🔥🔥 ','').replace('🔥','')}</h2><p style='font-size:19px;margin-top:12px;opacity:.9;line-height:1.5'>{s['spon_desc']}</p><button class='btn' style='background:#f59e0b;color:#000;margin-top:18px;font-size:19px;padding:18px' onclick="window.open('{s['spon_link']}')">{s['spon_btn']}</button></div>
</div>

<div id='p-tasks' class='page'>
  <div class='top2'><div class='cornerDiamond'>🎯</div><div class='topbox'>Tasks</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span id='balTopTasks' style='float:right;color:#22c55e'>৳0</span></div></div>
  <div class='glass'><h2>🎯 {s['task_page_title']}</h2><p style='opacity:.6'>{s['task_page_sub']}</p><div id='tasksList' style='margin-top:12px'></div></div>
  <div class='spon-big' style='border-color:#8b5cf6'><h3 style='font-size:22px'>{s['task_bottom_title']}</h3><p style='font-size:17px;margin-top:8px'>{s['task_bottom_desc']}</p><button class='btn' onclick="window.open('{s['task_bottom_link']}')">{s['task_bottom_btn']}</button></div>
</div>

<div id='p-refer' class='page'>
  <div class='top2'><div class='cornerDiamond'>👥</div><div class='topbox'>Refer</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span id='balTopRefer' style='float:right;color:#22c55e'>৳0</span></div></div>
  <div class='contest'>🎉 {s['ref_banner']}</div>
  <div class='glass'><h2 style='font-size:22px'>👥 {s['ref_title']}</h2><p style='opacity:.7;margin-top:6px'>{s['ref_desc']}</p><div style='display:flex;gap:10px;margin-top:14px'><div style='flex:1;background:#0F1429;padding:14px;border-radius:14px;text-align:center'><b id='refCount' style='color:#8b5cf6;font-size:22px'>0</b><br><small>Total Refer</small></div><div style='flex:1;background:#0F1429;padding:14px;border-radius:14px;text-align:center'><b style='color:#22c55e;font-size:22px'>৳{s['ref']}</b><br><small>Per Refer</small></div></div><div class='inputDark' id='refLinkBox' style='margin-top:12px;font-size:13px'>Loading...</div><button class='btn' onclick='copyRef()'>🔗 Copy Refer Link</button><div style='margin-top:14px;white-space:pre-line;line-height:1.8;opacity:.9'>{s['ref_rules']}</div></div>
  <div class='spon-big' style='border-color:#22c55e;background:linear-gradient(135deg,#14532d,#0B1E13)'><h3 style='font-size:22px'>{s['refer_bottom_title']}</h3><p style='font-size:17px;margin-top:8px'>{s['refer_bottom_desc']}</p><button class='btn' style='background:#22c55e;color:#000' onclick="window.open('{s['refer_bottom_link']}')">{s['refer_bottom_btn']}</button></div>
</div>

<div id='p-support' class='page'>
  <div class='top2'><div class='cornerDiamond'>💬</div><div class='topbox'>Support</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅</div></div>
  <div class='glass'><h2>💎 {s['sup_title']}</h2><p style='opacity:.7;margin-top:6px'>{s['sup_desc']}</p></div>
  <div class='glass'><h3>📞 Contact Us</h3><div style='display:flex;gap:10px;margin-top:12px'><div style='flex:1;background:#8b5cf6;padding:14px;border-radius:14px;text-align:center;font-weight:800;cursor:pointer' onclick="window.open('{s['sup_tg']}')">✈️ Telegram</div><div style='flex:1;background:#f59e0b;color:#000;padding:14px;border-radius:14px;text-align:center;font-weight:800;cursor:pointer' onclick="window.open('{s['sup_wa']}')">💬 WhatsApp</div></div><div class='inputDark'>📧 {s['sup_email']}</div></div>
  <div class='glass' style='border-color:#f59e0b;background:#1a1500'><h3>📢 Notice Board</h3><div style='margin-top:10px;white-space:pre-line;line-height:1.7'>{s['sup_notice']}</div></div>
  <div class='glass'><h3>❓ FAQ</h3><div style='margin-top:10px'><div style='background:#0B0E1C;padding:14px;border-radius:12px;margin-top:10px'><b>▶️ {s['sup_faq1_q']}</b><p style='opacity:.7;margin-top:6px'>{s['sup_faq1_a']}</p></div><div style='background:#0B0E1C;padding:14px;border-radius:12px;margin-top:10px'><b>▶️ {s['sup_faq2_q']}</b><p style='opacity:.7;margin-top:6px'>{s['sup_faq2_a']}</p></div><div style='background:#0B0E1C;padding:14px;border-radius:12px;margin-top:10px'><b>▶️ {s['sup_faq3_q']}</b><p style='opacity:.7;margin-top:6px'>{s['sup_faq3_a']}</p></div></div></div>
  <div class='glass'><h3>📜 Rules</h3><div style='white-space:pre-line;opacity:.85;line-height:1.8;margin-top:8px'>{s['sup_rules']}</div></div>
  <div class='spon-big' style='border-color:#06b6d4;background:linear-gradient(135deg,#0e4a5a,#082f3a)'><h3 style='font-size:22px'>{s['support_bottom_title']}</h3><p style='font-size:17px;margin-top:8px;white-space:pre-line'>{s['support_bottom_desc']}</p><button class='btn' style='background:#06b6d4;color:#000' onclick="window.open('{s['support_bottom_link']}')">{s['support_bottom_btn']}</button></div>
</div>

<div id='p-profile' class='page'>
  <div class='top2'><div class='cornerDiamond' id='cornerPro'>👤</div><div class='topbox'>Profile</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span id='balTopProfile' style='float:right;color:#22c55e'>৳0</span></div></div>
  <div class='glass' style='text-align:center'><div class='proImg' id='proImgWrap'><img id='proImg' src='' style='width:100%;height:100%;object-fit:cover;display:none'><span id='proEmoji'>👤</span></div><div style='background:#f59e0b;color:#000;display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:800;margin-top:10px'>Level 1</div><h2 id='pNameShow' style='margin-top:10px'>User 4250</h2><p id='pJoin' style='opacity:.6;font-size:13px'>Join: 2026-09-15</p><p style='margin-top:6px'>💎 <span id='pDiamond'>2030</span> Diamond | <span id='pBal2'>20.3</span> Taka</p></div>
  <div class='glass'><h3>📊 Statistics</h3><div class='stat4'><div><b style='color:#22c55e;font-size:20px' id='statEarned'>৳20</b><br><small>Total Earned</small></div><div><b style='color:#8b5cf6;font-size:20px' id='statBal'>৳20</b><br><small>Balance</small></div><div><b style='color:#f59e0b;font-size:20px' id='statAds'>0</b><br><small>Ads</small></div><div><b style='color:#ec4899;font-size:20px' id='statRefer'>0</b><br><small>Refer</small></div></div></div>
  <div class='glass'><h3>⚙️ Account - নাম/ছবি গ্যালারি থেকে</h3><div class='inputDark' id='accId'>Loading...</div><input class='inputDark' id='accNameInput' placeholder='Your Name' /><input type='file' id='accPhoto' accept='image/*' class='inputDark' onchange='previewPhoto(this)' /><div id='previewWrap' style='display:none;margin-top:10px'><img id='previewImg' style='width:90px;height:90px;border-radius:16px;object-fit:cover'></div><button class='btn' onclick='saveProfile()'>💾 Save Profile</button></div>
  <div class='glass'><h3>💸 Withdraw History</h3><div id='wdHistList' style='opacity:.6'>No withdraw</div></div>
  <div class='spon-big' style='border-color:#8b5cf6;background:linear-gradient(135deg,#1e1b4b,#2D1B4E)'><h3 style='font-size:22px'>{s['profile_bottom_title']}</h3><p style='font-size:17px;margin-top:8px;white-space:pre-line'>{s['profile_bottom_desc']}</p><button class='btn' onclick="window.open('{s['profile_bottom_link']}')">{s['profile_bottom_btn']}</button></div>
</div>

<div class='btm'>
  <div class='on' id='b-home' onclick="showP('home')"><span>🏠</span>Home</div>
  <div id='b-tasks' onclick="showP('tasks')"><span>🎯</span>Tasks</div>
  <div id='b-refer' onclick="showP('refer')"><span>👥</span>Refer</div>
  <div id='b-support' onclick="showP('support')"><span>💬</span>Support</div>
  <div id='b-profile' onclick="showP('profile')"><span>👤</span>Profile</div>
</div>

<script>
let curMeth='bKash'; let uid=localStorage.getItem('uid')||'8807178385_4250'; localStorage.setItem('uid',uid);
function setMeth(m){{curMeth=m;document.querySelectorAll('.meth').forEach(e=>e.classList.remove('on'));document.getElementById('m-'+m).classList.add('on');}}
function showP(id){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p-'+id).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));document.getElementById('b-'+id).classList.add('on'); if(id=='tasks') loadTasks(); init();}}
function watchAd(t){{
let directLink = t=='c'? '{s['direct_link1']}' : '{s['direct_link2']}';
window.open(directLink, '_blank');
let fn = t=='c'? window['show_{s['company_ad_id']}'] : window['show_{s['popup_ad_id']}'];
if(typeof fn==='function'){{ fn().then(()=>sendReward(t)).catch(()=>sendReward(t)); }}
else {{ setTimeout(()=>sendReward(t),1800); }}
}}
function sendReward(t){{fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:t}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}}
function doWD(){{let num=document.getElementById('wNum').value;let amt=document.getElementById('wAmt').value; if(!num||!amt) return alert('Number & Amount দিন'); fetch('/api/wd',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,amt:amt,num:num,m:curMeth}})}}).then(r=>r.json()).then(d=>alert(d.msg));}}
function loadTasks(){{fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}}).then(r=>r.json()).then(d=>{{let html=''; d.tasks.forEach(t=>{{html+=`<div class='task-card'><div><b>${{t.icon}} ${{t.title}}</b><div style='color:#22c55e'>৳${{t.reward}}</div></div><button style='background:#8b5cf6;color:#fff;border:none;padding:10px 20px;border-radius:20px' onclick="window.open('${{t.link}}','_blank'); setTimeout(()=>{{fetch('/api/task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,tid:t.id}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}},30000);">Go</button></div>`;}}); document.getElementById('tasksList').innerHTML=html;}});}}
function copyRef(){{let txt=document.getElementById('refLinkBox').innerText; navigator.clipboard.writeText(txt).then(()=>alert('Copy Done! ✅'));}}
function previewPhoto(input){{ if(input.files && input.files[0]){{ let r=new FileReader(); r.onload=e=>{{document.getElementById('previewImg').src=e.target.result; document.getElementById('previewWrap').style.display='block'; document.getElementById('proImg').src=e.target.result; document.getElementById('proImg').style.display='block'; document.getElementById('proEmoji').style.display='none';}}; r.readAsDataURL(input.files[0]);}}}}
function saveProfile(){{let name=document.getElementById('accNameInput').value; let file=document.getElementById('accPhoto').files[0]; let fd=new FormData(); fd.append('id',uid); fd.append('name',name); if(file) fd.append('photo',file); fetch('/api/profile',{{method:'POST',body:fd}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}}
function init(){{fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}}).then(r=>r.json()).then(d=>{{let u=d.user; let bal='৳'+u.bal; document.getElementById('balShow').innerText=bal; document.getElementById('balTopRight').innerText=bal; document.getElementById('balTopBalance').innerText=bal; ['balTopTasks','balTopRefer','balTopProfile'].forEach(id=>{{let el=document.getElementById(id); if(el) el.innerText=bal;}}); document.getElementById('diamondTop').innerText=u.diamonds||2030; document.getElementById('pNameShow').innerText=u.name; document.getElementById('pDiamond').innerText=u.diamonds; document.getElementById('pBal2').innerText=u.bal; document.getElementById('statEarned').innerText=bal; document.getElementById('statBal').innerText=bal; document.getElementById('statAds').innerText=(u.c_today||0)+(u.p_today||0); document.getElementById('statRefer').innerText=u.refl?u.refl.length:0; document.getElementById('accId').innerText=u.id; document.getElementById('accNameInput').value=u.name; document.getElementById('cToday').innerText=(u.c_today||0)+'/{s['clim']}'; document.getElementById('pToday').innerText=(u.p_today||0)+'/{s['plim']}'; document.getElementById('adsCount').innerText=(u.c_today||0)+(u.p_today||0)+'/80'; document.getElementById('refLinkBox').innerText=window.location.origin+'/?ref='+u.id; document.getElementById('refCount').innerText=u.refl?u.refl.length:0; if(u.photo){{document.getElementById('proImg').src=u.photo; document.getElementById('proImg').style.display='block'; document.getElementById('proEmoji').style.display='none';}} if(d.wds && d.wds.length>0){{document.getElementById('wdHistList').innerHTML=d.wds.map(w=>`<div style="padding:10px;background:#0B0E1C;border-radius:10px;margin-top:6px;display:flex;justify-content:space-between"><div>${{w.m}} ${{w.num}}</div><div>৳${{w.amt}} ${{w.st}}</div></div>`).join('');}} }});}} init(); loadTasks();
</script></body></html>
""")

@app.route('/admin')
def admin():
    db=load_db(); s=db["settings"]; fields="";
    for k,v in s.items():
        if len(str(v))>40 or "desc" in k or "rules" in k or "notice" in k:
            fields+=f"<label>{k}</label><textarea name='{k}' style='width:100%;padding:10px;margin:6px 0;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333'>{v}</textarea>"
        else:
            fields+=f"<label>{k}</label><input name='{k}' value='{v}' style='width:100%;padding:10px;margin:6px 0;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333' />"
    return render_template_string(f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;max-width:700px;margin:auto;padding:20px;font-family:system-ui}}label{{color:#a78bfa;font-weight:700;margin-top:12px;display:block}}.btn{{width:100%;padding:14px;background:#8b5cf6;color:#fff;border:none;border-radius:12px;font-weight:800;margin-top:20px}}.card{{background:#1A2040;padding:16px;border-radius:16px;margin:12px 0;border:1px solid #2a2f4a}}</style></head><body><h1>🔧 Admin Panel - A to Z Control</h1><form method='POST' action='/admin/save'><div class='card'><h3>⚙️ Home Page - তোমার লাল দাগের ফিক্স</h3><p>home_corner_diamond=কোনার বড় ডাইমন্ড | home_small_diamond_icon=ছোট ডাইমন্ড | home_diamond_big_size=সাইজ | home_name_font_size=নাম সাইজ | direct_link1=Company Ad কোম্পানি | direct_link2=Popup Ad কোম্পানি | spon_big_height=নিচের বড় বক্স হাইট</p>{fields}</div><button class='btn'>💾 Save All Settings - সব সেভ</button></form></body></html>")

@app.route('/admin/save', methods=['POST'])
def admin_save():
    db=load_db()
    for k in list(db["settings"].keys()):
        if k in request.form:
            v=request.form[k]
            try:
                if k in ["ad","pop"]: db["settings"][k]=float(v)
                elif k in ["clim","plim","min","ref"]: db["settings"][k]=int(float(v))
                else: db["settings"][k]=v
            except: db["settings"][k]=v
    save_db(db)
    return "<script>alert('✅ Saved!'); location.href='/admin';</script>"

@app.route('/api/init', methods=['POST'])
def api_init():
    db=load_db(); d=request.json; uid=d.get('id','4250')
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":20.3,"diamonds":2030,"c_today":0,"p_today":0,"refl":[],"photo":"", "join":datetime.now().strftime("%Y-%m-%d")}
        save_db(db)
    return jsonify({"user":db["users"][uid],"tasks":db.get("tasks",[]),"wds":[w for w in db.get("wds",[]) if w["uid"]==uid]})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    import time
    db=load_db(); d=request.json; uid=d["id"]; typ=d["type"]; u=db["users"][uid]; s=db["settings"]
    now = time.time()
    if now - u.get("last_ad_time", 0) < 15:
        return jsonify({"msg": f"⏳ {15 - int(now - u.get('last_ad_time',0))}s wait!"})
    if typ=="c" and u["c_today"]>=s["clim"]: return jsonify({"msg":"Limit Done"})
    if typ=="p" and u["p_today"]>=s["plim"]: return jsonify({"msg":"Limit Done"})
    reward=s["ad"] if typ=="c" else s["pop"]; u["bal"]=round(u["bal"]+reward,2); u["diamonds"]+=int(reward*100)
    if typ=="c": u["c_today"]+=1
    else: u["p_today"]+=1
    u["last_ad_time"] = now
    save_db(db); return jsonify({"msg":f"✅ ৳{reward} Added!"})

@app.route('/api/wd', methods=['POST'])
def api_wd():
    db=load_db(); d=request.json; uid=d["id"]; amt=float(d["amt"]); s=db["settings"]; u=db["users"][uid]
    if amt < s["min"]: return jsonify({"msg":f"Min ৳{s['min']}"})
    if u["bal"] < amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt; db.setdefault("wds",[]).append({"uid":uid,"amt":amt,"num":d["num"],"m":d["m"],"st":"Pending","time":datetime.now().strftime("%Y-%m-%d")})
    save_db(db); return jsonify({"msg":"✅ Withdraw Sent!"})

@app.route('/api/profile', methods=['POST'])
def save_profile():
    db=load_db(); uid=request.form.get('id'); name=request.form.get('name')
    if uid in db["users"]:
        if name: db["users"][uid]["name"]=name
        if 'photo' in request.files:
            f=request.files['photo']; b64=base64.b64encode(f.read()).decode()
            db["users"][uid]["photo"]=f"data:{f.mimetype};base64,{b64}"
        save_db(db)
    return jsonify({"msg":"✅ Profile Saved!"})

@app.route('/api/task', methods=['POST'])
def api_task():
    db=load_db(); d=request.json; uid=d["id"]; tid=d["tid"]; u=db["users"][uid]
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    if t: u["bal"]=round(u["bal"]+t["reward"],2); u["diamonds"]+=int(t["reward"]*100); save_db(db)
    return jsonify({"msg":f"✅ ৳{t['reward']} Added!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
