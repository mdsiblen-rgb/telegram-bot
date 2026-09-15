from flask import Flask, request, jsonify, render_template_string
import json, os, base64
from datetime import datetime

app = Flask(__name__)
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},
            "settings": {
                "app_name": "প্রতিদিনের কাজ বিডি",
                "primary": "#8b5cf6",
                "secondary": "#f59e0b",
                "ad": 0.5, "pop": 0.3,
                "clim": 80, "plim": 80,
                "min": 200, "ref": 20,
                "company_ad_id": "9876543",
                "popup_ad_id": "1234567",
                "direct_link": "https://google.com",
                "spon_title": "🔥 Biggest Earning Offer",
                "spon_desc": "প্রতিদিন কাজ করে আয় করুন",
                "spon_link": "https://google.com",
                "spon_btn": "🚀 Claim Now",

                # 2nd Page - Tasks
                "task_page_title": "Tasks & Company Links",
                "task_page_sub": "প্রতি Task এ ৳20-25 + Diamond",
                "task_bottom_title": "🔥 Special Offer",
                "task_bottom_desc": "এই বক্স Admin থেকে চেঞ্জ হবে",
                "task_bottom_btn": "Claim Now",
                "task_bottom_link": "https://google.com",

                # 3rd Page - Refer
                "ref_title": "Refer & Earn",
                "ref_desc": "বন্ধুদের Invite করে Unlimited আয়",
                "ref_banner": "🎉 Refer Contest চলছে!",
                "ref_rules": "1. বন্ধুকে লিংক শেয়ার করো\n2. বন্ধু Join করলে ৳20 পাবে\n3. বন্ধু Ads দেখলে 15% Commission",
                "refer_bottom_title": "🔥 Refer Special Bonus",
                "refer_bottom_desc": "এখানে Admin থেকে যেকোনো লিংক/অফার লিখতে পারবে",
                "refer_bottom_btn": "Join Now",
                "refer_bottom_link": "https://google.com",

                # 4th Page - Support
                "sup_title": "Support Center",
                "sup_desc": "যেকোনো সমস্যায় আমাদের সাথে যোগাযোগ করুন - 24/7",
                "sup_tg": "https://t.me/dailyworkbd",
                "sup_wa": "https://wa.me/8801XXXXXXXXX",
                "sup_fb": "https://facebook.com",
                "sup_email": "support@dailyworkbd.com",
                "sup_notice": "⚠️ রাত ১০টার পর Withdraw বন্ধ থাকে\n✅ সকাল ৯টার পর আবার চালু হয়",
                "sup_faq1_q": "Withdraw কতক্ষণে পাবো?",
                "sup_faq1_a": "২৪ ঘণ্টার ভিতরে পেমেন্ট করা হয়",
                "sup_faq2_q": "Refer টাকা কখন পাবো?",
                "sup_faq2_a": "বন্ধু Join করলেই সাথে সাথে",
                "sup_faq3_q": "Ads দেখলে টাকা আসে না কেন?",
                "sup_faq3_a": "VPN বন্ধ করে আবার চেষ্টা করুন",
                "sup_rules": "1. একাধিক একাউন্ট খুলবেন না\n2. ভুল তথ্য দিবেন না\n3. Fake Refer করবেন না\n4. Admin এর সিদ্ধান্তই চূড়ান্ত",
                "support_bottom_title": "📢 Important Update",
                "support_bottom_desc": "এই জায়গাটা Admin থেকে কন্ট্রোল করতে পারবে",
                "support_bottom_btn": "Contact Now",
                "support_bottom_link": "https://t.me/",

                # 5th Page - Profile
                "profile_bottom_title": "💎 VIP Membership",
                "profile_bottom_desc": "VIP হলে বেশি ইনকাম পাবেন। Admin থেকে অফার লিখুন",
                "profile_bottom_btn": "⭐ Upgrade Now",
                "profile_bottom_link": "https://google.com"
            },
            "tasks": [
                {"id":"t1","icon":"🌐","title":"Visit Company Website","reward":0.2,"link":"https://google.com"},
                {"id":"t2","icon":"▶️","title":"Watch Popup Ad","reward":0.3,"link":"https://youtube.com"},
                {"id":"t3","icon":"📢","title":"Join Telegram Channel","reward":0.5,"link":"https://t.me/"}
            ],
            "wds": []
        }
    with open(DB_FILE,"r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE,"w") as f:
        json.dump(db,f,indent=2)

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    return render_template_string(f"""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='//libtl.com/sdk.js' data-zone='{s["company_ad_id"]}' data-sdk='show_{s["company_ad_id"]}'></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}
body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:110px}}
.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:16px;margin:12px}}
.top2{{display:flex;gap:10px;margin:12px;align-items:center}}.topbox{{flex:1;background:#151A2D;border:1px solid #8b5cf6;padding:12px;border-radius:14px;font-weight:700;font-size:13px}}
.btn{{width:100%;padding:13px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{s['primary']};cursor:pointer;margin-top:10px}}
.meth{{flex:1;padding:12px;border-radius:14px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C;font-weight:800}}.meth.on{{border-color:{s['primary']};background:rgba(139,92,246,.25)}}
.task-card{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:#0F1429;border:1px solid #1e293b;border-radius:18px;margin:10px 12px}}
.goBtn{{background:#8b5cf6;color:#fff;border:none;padding:10px 22px;border-radius:22px;font-weight:800;cursor:pointer}}
.spon-big{{background:linear-gradient(135deg,#2D1B4E,#1A1033);border:1px solid #f59e0b;padding:18px;border-radius:22px;margin:12px}}
.contest{{background:linear-gradient(90deg,#f59e0b,#f97316);color:#000;padding:14px;border-radius:18px;margin:12px;text-align:center;font-weight:800}}
.proImg{{width:90px;height:90px;border-radius:20px;background:#0B0E1C;border:2px solid #8b5cf6;display:flex;align-items:center;justify-content:center;font-size:40px;overflow:hidden;margin:0 auto}}
.stat4{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}}.stat4 div{{background:#0B0E1C;border:1px solid #1e293b;padding:14px;border-radius:16px;text-align:center}}
.inputDark{{width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px;outline:none}}
.page{{display:none}}.page.active{{display:block}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:22px;display:block}}
</style></head><body>

<!-- HOME -->
<div id='p-home' class='page active'>
  <div class='top2'><div class='topbox'>👑 {s['app_name']}</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span style='float:right;color:#22c55e' id='balTop'>৳20</span></div></div>
  <div class='glass'><div style='display:flex;justify-content:space-between'><span style='color:#a78bfa'>Diamond Member • Level 1</span><span id='balTopSmall'>Balance</span></div><b id='balShow' style='color:#22c55e;font-size:26px'>৳20</b><br><small style='opacity:.6'>💎 <span id='diamondTop'>2000</span> Diamond | <span id='adsCount'>0/80</span> Ads</small></div>
  <div style='display:flex;gap:10px;margin:0 12px'><div class='glass' style='flex:1;margin:0'><b>Company Ads</b> <span style='color:#f59e0b'>৳{s['ad']}</span><br><small id='cToday'>0/{s['clim']}</small><button class='btn' onclick='watchAd("c")'>Start - ৳{s['ad']}</button></div><div class='glass' style='flex:1;margin:0'><b>Popup Ads</b> <span style='color:#f59e0b'>৳{s['pop']}</span><br><small id='pToday'>0/{s['plim']}</small><button class='btn' style='background:{s['secondary']};color:#000' onclick='watchAd("p")'>Watch - ৳{s['pop']}</button></div></div>
  <div class='glass'><h3>💸 Withdraw</h3><div style='display:flex;gap:10px;margin-top:12px'><div class='meth on' id='m-bKash' onclick="setMeth('bKash')">bKash</div><div class='meth' id='m-Nagad' onclick="setMeth('Nagad')">Nagad</div></div><input id='wNum' class='inputDark' placeholder='01XXXXXXXXX' /><input id='wAmt' class='inputDark' type='number' placeholder='Min {s['min']}' /><button class='btn' onclick='doWD()'>Withdraw Now</button></div>
  <div class='spon-big'><h3>🔥 {s['spon_title']}</h3><p style='opacity:.8;margin-top:6px'>{s['spon_desc']}</p><button class='btn' style='background:#f59e0b;color:#000' onclick="window.open('{s['spon_link']}')">{s['spon_btn']}</button></div>
</div>

<!-- TASKS - 2nd Page -->
<div id='p-tasks' class='page'>
  <div class='glass'><h2>🎯 {s['task_page_title']}</h2><p style='opacity:.6'>{s['task_page_sub']}</p><div id='tasksList' style='margin-top:12px'></div></div>
  <div class='spon-big' style='border-color:#8b5cf6'><h3>{s['task_bottom_title']}</h3><p style='opacity:.8;margin-top:6px'>{s['task_bottom_desc']}</p><button class='btn' onclick="window.open('{s['task_bottom_link']}')">{s['task_bottom_btn']}</button></div>
</div>

<!-- REFER - 3rd Page -->
<div id='p-refer' class='page'>
  <div class='contest'>🎉 {s['ref_banner']}</div>
  <div class='glass'><h2>👥 {s['ref_title']}</h2><p style='opacity:.7'>{s['ref_desc']}</p><div style='display:flex;gap:10px;margin-top:12px'><div style='flex:1;background:#0F1429;padding:12px;border-radius:12px;text-align:center'><b id='refCount' style='color:#8b5cf6'>0</b><br><small>Refer</small></div><div style='flex:1;background:#0F1429;padding:12px;border-radius:12px;text-align:center'><b style='color:#22c55e'>৳{s['ref']}</b><br><small>Per Refer</small></div></div><div class='inputDark' id='refLinkBox' style='margin-top:12px'>Loading...</div><button class='btn' onclick='copyRef()'>🔗 Copy Refer Link</button><div style='margin-top:12px;white-space:pre-line;line-height:1.7'>{s['ref_rules']}</div></div>
  <div class='spon-big' style='border-color:#22c55e;background:linear-gradient(135deg,#14532d,#0B1E13)'><h3>{s['refer_bottom_title']}</h3><p style='opacity:.9;margin-top:6px'>{s['refer_bottom_desc']}</p><button class='btn' style='background:#22c55e;color:#000' onclick="window.open('{s['refer_bottom_link']}')">{s['refer_bottom_btn']}</button></div>
</div>

<!-- SUPPORT - 4th Page -->
<div id='p-support' class='page'>
  <div class='glass'><h2>💎 {s['sup_title']}</h2><p style='opacity:.6'>{s['sup_desc']}</p></div>
  <div class='glass'><h3>📞 Contact Us</h3><div style='display:flex;gap:10px;margin-top:12px'><div style='flex:1;background:#8b5cf6;padding:14px;border-radius:14px;text-align:center;font-weight:800;cursor:pointer' onclick="window.open('{s['sup_tg']}')">✈️ Telegram</div><div style='flex:1;background:#f59e0b;color:#000;padding:14px;border-radius:14px;text-align:center;font-weight:800;cursor:pointer' onclick="window.open('{s['sup_wa']}')">💬 WhatsApp</div></div><div class='inputDark'>📧 {s['sup_email']}</div></div>
  <div class='glass' style='border-color:#f59e0b;background:#1a1500'><h3>📢 Notice Board</h3><div style='margin-top:8px;white-space:pre-line'>{s['sup_notice']}</div></div>
  <div class='glass'><h3>❓ FAQ</h3><div style='margin-top:10px'><div style='background:#0B0E1C;padding:12px;border-radius:12px;margin-top:8px'><b>▶️ {s['sup_faq1_q']}</b><p style='opacity:.7;margin-top:6px'>{s['sup_faq1_a']}</p></div><div style='background:#0B0E1C;padding:12px;border-radius:12px;margin-top:8px'><b>▶️ {s['sup_faq2_q']}</b><p style='opacity:.7;margin-top:6px'>{s['sup_faq2_a']}</p></div><div style='background:#0B0E1C;padding:12px;border-radius:12px;margin-top:8px'><b>▶️ {s['sup_faq3_q']}</b><p style='opacity:.7;margin-top:6px'>{s['sup_faq3_a']}</p></div></div></div>
  <div class='glass'><h3>📜 Rules</h3><div style='white-space:pre-line;opacity:.8;margin-top:8px'>{s['sup_rules']}</div></div>
  <div class='glass' style='border-color:#22c55e'><h3>{s['support_bottom_title']}</h3><p style='opacity:.8;margin-top:6px;white-space:pre-line'>{s['support_bottom_desc']}</p><button class='btn' style='background:#22c55e;color:#000' onclick="window.open('{s['support_bottom_link']}')">{s['support_bottom_btn']}</button></div>
</div>

<!-- PROFILE - 5th Page - তোমার ছবির মতো -->
<div id='p-profile' class='page'>
  <div class='top2'><div style='width:44px;height:44px;background:#151A2D;border:1px solid #8b5cf6;border-radius:12px;display:flex;align-items:center;justify-content:center'>💎</div><div class='topbox'>👑 {s['app_name']}</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span style='float:right;color:#22c55e' id='balTop2'>৳20</span></div></div>
  <div class='glass' style='text-align:center'><div class='proImg' id='proImgWrap'><img id='proImg' src='' style='width:100%;height:100%;object-fit:cover;display:none'><span id='proEmoji'>💎</span></div><div style='background:#f59e0b;color:#000;display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:800;margin-top:10px'>Level 1</div><h2 id='pNameShow' style='margin-top:10px'>User 4250</h2><p id='pJoin' style='opacity:.6;font-size:13px'>Join: 2026-09-15</p><p style='opacity:.8;margin-top:4px;font-size:14px'>💎 <span id='pDiamond'>2000</span> Diamond | <span id='pBal2'>20</span> Taka</p></div>
  <div class='glass'><h3>📊 Statistics</h3><div class='stat4'><div><b style='color:#22c55e;font-size:20px' id='statEarned'>৳20</b><br><small>Total Earned</small></div><div><b style='color:#8b5cf6;font-size:20px' id='statBal'>৳20</b><br><small>Balance</small></div><div><b style='color:#f59e0b;font-size:20px' id='statAds'>0</b><br><small>Ads</small></div><div><b style='color:#ec4899;font-size:20px' id='statRefer'>0</b><br><small>Refer</small></div></div></div>
  <div class='glass'><h3>📈 Level Progress</h3><div style='display:flex;justify-content:space-between;margin-top:8px;opacity:.7;font-size:14px'><span>Level 1</span><span>Next: ৳500</span></div><div style='width:100%;height:10px;background:#0B0E1C;border-radius:10px;margin-top:10px'><div style='width:8%;height:100%;background:#8b5cf6;border-radius:10px'></div></div><p style='opacity:.6;font-size:13px;margin-top:8px'>💎 Diamond Member - Level বাড়ান, বেশি ইনকাম করুন!</p></div>
  <div class='glass'><h3>⚙️ Account - ইউজার নিজে নাম/ছবি বদলাবে</h3><div style='margin-top:10px'><label style='opacity:.7;font-size:13px'>User ID</label><div class='inputDark' id='accId'>Loading...</div><label style='opacity:.7;font-size:13px;margin-top:12px;display:block'>Profile Name</label><input class='inputDark' id='accNameInput' placeholder='User 4250' /><label style='opacity:.7;font-size:13px;margin-top:12px;display:block'>Profile Photo - Gallery থেকে</label><input type='file' id='accPhoto' accept='image/*' class='inputDark' style='padding:10px' onchange='previewPhoto(this)' /><div id='previewWrap' style='margin-top:10px;display:none'><img id='previewImg' style='width:80px;height:80px;border-radius:12px;object-fit:cover'></div><button class='btn' onclick='saveProfile()'>💾 Save Profile</button></div></div>
  <div class='glass'><h3>💸 Withdraw History</h3><div id='wdHistList' style='margin-top:10px;opacity:.6'>No withdraw</div></div>
  <div class='glass' style='background:linear-gradient(135deg,#1e1b4b,#2D1B4E);border-color:#8b5cf6'><span style='background:#22c55e;color:#000;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:800'>✨ ADMIN BOX</span><h2 style='margin-top:12px'>{s['profile_bottom_title']}</h2><p style='margin-top:8px;opacity:.9;white-space:pre-line'>{s['profile_bottom_desc']}</p><button class='btn' style='background:#22c55e;color:#000' onclick="window.open('{s['profile_bottom_link']}')">{s['profile_bottom_btn']}</button></div>
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
function showP(id){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p-'+id).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));document.getElementById('b-'+id).classList.add('on'); if(id=='tasks') loadTasks(); if(id=='refer'||id=='profile'||id=='home') init();}}
function watchAd(t){{let fn=t=='c'?window['show_{s['company_ad_id']}']:window['show_{s['popup_ad_id']}']; if(typeof fn==='function'){{fn().then(()=>sendReward(t)).catch(()=>sendReward(t));}} else {{ setTimeout(()=>sendReward(t),1500);}}}}
function sendReward(t){{fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:t}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}}
function doWD(){{let num=document.getElementById('wNum').value;let amt=document.getElementById('wAmt').value; if(!num||!amt) return alert('Number & Amount দিন'); fetch('/api/wd',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,amt:amt,num:num,m:curMeth}})}}).then(r=>r.json()).then(d=>alert(d.msg));}}
function loadTasks(){{fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}}).then(r=>r.json()).then(d=>{{let html=''; d.tasks.forEach(t=>{{html+=`<div class='task-card'><div><b>${{t.icon}} ${{t.title}}</b><div style='color:#22c55e'>৳${{t.reward}} + 💎${{t.reward*100}}</div></div><button class='goBtn' onclick="doTask('${{t.id}}','${{t.link}}')">Go</button></div>`;}}); document.getElementById('tasksList').innerHTML=html;}});}}
let taskTimers={{}}; function doTask(tid,link){{window.open(link,'_blank'); if(!taskTimers[tid]){{taskTimers[tid]=Date.now(); alert('Link e 30 sec thakun, tarpor abar Go din'); return;}} let left=30-Math.floor((Date.now()-taskTimers[tid])/1000); if(left>0) return alert('Aro '+left+' sec baki'); fetch('/api/task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,tid:tid,ts:tid}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); delete taskTimers[tid]; init();}});}}
function copyRef(){{let txt=document.getElementById('refLinkBox').innerText; navigator.clipboard.writeText(txt).then(()=>alert('Copy Done! ✅'));}}
function previewPhoto(input){{ if(input.files && input.files[0]){{ let r=new FileReader(); r.onload=e=>{{document.getElementById('previewImg').src=e.target.result; document.getElementById('previewWrap').style.display='block'; document.getElementById('proImg').src=e.target.result; document.getElementById('proImg').style.display='block'; document.getElementById('proEmoji').style.display='none';}}; r.readAsDataURL(input.files[0]);}}}}
function saveProfile(){{let name=document.getElementById('accNameInput').value; let file=document.getElementById('accPhoto').files[0]; let fd=new FormData(); fd.append('id',uid); fd.append('name',name); if(file) fd.append('photo',file); fetch('/api/profile',{{method:'POST',body:fd}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}}
function init(){{fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}}).then(r=>r.json()).then(d=>{{let u=d.user; document.getElementById('balShow').innerText='৳'+u.bal; document.getElementById('balTop').innerText='৳'+u.bal; document.getElementById('balTop2').innerText='৳'+u.bal; document.getElementById('diamondTop').innerText=u.diamonds||0; document.getElementById('pNameShow').innerText=u.name||'User '+u.id.slice(-4); document.getElementById('pDiamond').innerText=u.diamonds||0; document.getElementById('pBal2').innerText=u.bal; document.getElementById('statEarned').innerText='৳'+u.bal; document.getElementById('statBal').innerText='৳'+u.bal; document.getElementById('statAds').innerText=(u.c_today||0)+(u.p_today||0); document.getElementById('statRefer').innerText=u.refl?u.refl.length:0; document.getElementById('accId').innerText=u.id; document.getElementById('accNameInput').value=u.name||''; document.getElementById('cToday').innerText=(u.c_today||0)+'/{s['clim']}'; document.getElementById('pToday').innerText=(u.p_today||0)+'/{s['plim']}'; if(u.photo){{document.getElementById('proImg').src=u.photo; document.getElementById('proImg').style.display='block'; document.getElementById('proEmoji').style.display='none';}} let link=window.location.origin+'/?ref='+u.id; document.getElementById('refLinkBox').innerText=link; document.getElementById('refCount').innerText=u.refl?u.refl.length:0; if(d.wds && d.wds.length>0){{document.getElementById('wdHistList').innerHTML=d.wds.map(w=>`<div style="display:flex;justify-content:space-between;padding:10px;background:#0B0E1C;border-radius:10px;margin-top:8px"><div>${{w.m}} ${{w.num}}</div><div>৳${{w.amt}} <small style="color:${{w.st=='Approved'?'#22c55e':'#f59e0b'}}">${{w.st}}</small></div></div>`).join('');}}}});}} init(); loadTasks();
</script>
</body></html>
""")

@app.route('/api/init', methods=['POST'])
def api_init():
    db=load_db(); d=request.json; uid=d.get('id','4250')
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":20,"diamonds":2000,"c_today":0,"p_today":0,"refl":[],"photo":"", "join": datetime.now().strftime("%Y-%m-%d")}
        save_db(db)
    u=db["users"][uid]
    wds=[w for w in db.get("wds",[]) if w.get("uid")==uid]
    return jsonify({"user":u,"tasks":db["tasks"],"wds":wds})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    db=load_db(); d=request.json; uid=d["id"]; typ=d["type"]
    u=db["users"].get(uid); s=db["settings"]
    if not u: return jsonify({"msg":"User not found"})
    if typ=="c" and u["c_today"]>=s["clim"]: return jsonify({"msg":f"Company Ads limit {s['clim']} done"})
    if typ=="p" and u["p_today"]>=s["plim"]: return jsonify({"msg":f"Popup limit {s['plim']} done"})
    reward=s["ad"] if typ=="c" else s["pop"]
    u["bal"]+=reward; u["diamonds"]+=int(reward*100)
    if typ=="c": u["c_today"]+=1
    else: u["p_today"]+=1
    save_db(db)
    return jsonify({"msg":f"✅ ৳{reward} Added!"})

@app.route('/api/task', methods=['POST'])
def api_task():
    db=load_db(); d=request.json; uid=d["id"]; tid=d["tid"]
    u=db["users"].get(uid)
    task=next((t for t in db["tasks"] if t["id"]==tid),None)
    if not task: return jsonify({"msg":"Task not found"})
    u["bal"]+=task["reward"]; u["diamonds"]+=int(task["reward"]*100)
    save_db(db)
    return jsonify({"msg":f"✅ Task Done! ৳{task['reward']} + Diamond"})

@app.route('/api/wd', methods=['POST'])
def api_wd():
    db=load_db(); d=request.json; uid=d["id"]; amt=float(d["amt"])
    s=db["settings"]; u=db["users"].get(uid)
    if amt < s["min"]: return jsonify({"msg":f"Min Withdraw ৳{s['min']}"})
    if u["bal"] < amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt
    db.setdefault("wds",[]).append({"uid":uid,"amt":amt,"num":d["num"],"m":d["m"],"st":"Pending","time":datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_db(db)
    return jsonify({"msg":"✅ Withdraw Request Sent!"})

@app.route('/api/profile', methods=['POST'])
def save_profile():
    db=load_db()
    uid=request.form.get('id') or (request.json.get('id') if request.is_json else None)
    name=request.form.get('name') or (request.json.get('name') if request.is_json else None)
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    if name: db["users"][uid]["name"]=name
    if 'photo' in request.files:
        f=request.files['photo']
        b64=base64.b64encode(f.read()).decode()
        db["users"][uid]["photo"]=f"data:{f.mimetype};base64,{b64}"
    save_db(db)
    return jsonify({"msg":"✅ Profile Saved!","photo":db["users"][uid].get("photo",""),"name":db["users"][uid]["name"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
