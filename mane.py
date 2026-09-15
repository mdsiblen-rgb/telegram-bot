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
                "primary": "#8b5cf6", "secondary": "#f59e0b",
                "ad": 0.5, "pop": 0.3, "clim": 80, "plim": 80, "min": 200, "ref": 20,
                "company_ad_id": "9876543", "popup_ad_id": "1234567", "direct_link": "https://google.com",
                "spon_title": "🔥 Biggest Earning Offer", "spon_desc": "প্রতিদিন কাজ করে আয় করুন", "spon_link": "https://google.com", "spon_btn": "🚀 Claim Now",
                "task_page_title": "Tasks & Company Links", "task_page_sub": "প্রতি Task এ ৳20-25 + Diamond",
                "task_bottom_title": "🔥 Special Offer", "task_bottom_desc": "Admin থেকে চেঞ্জ হবে", "task_bottom_btn": "Claim Now", "task_bottom_link": "https://google.com",
                "ref_title": "Refer & Earn", "ref_desc": "বন্ধুদের Invite করে Unlimited আয়", "ref_banner": "🎉 Refer Contest চলছে!", "ref_rules": "1. বন্ধুকে লিংক শেয়ার করো\n2. বন্ধু Join করলে ৳20 পাবে\n3. বন্ধু Ads দেখলে 15% Commission",
                "refer_bottom_title": "🔥 Refer Special Bonus", "refer_bottom_desc": "Admin থেকে লিখতে পারবে", "refer_bottom_btn": "Join Now", "refer_bottom_link": "https://google.com",
                "sup_title": "Support Center", "sup_desc": "যেকোনো সমস্যায় যোগাযোগ করুন - 24/7", "sup_tg": "https://t.me/", "sup_wa": "https://wa.me/8801", "sup_fb": "https://facebook.com", "sup_email": "support@dailyworkbd.com",
                "sup_notice": "⚠️ রাত ১০টার পর Withdraw বন্ধ থাকে\n✅ সকাল ৯টার পর আবার চালু হয়",
                "sup_faq1_q": "Withdraw কতক্ষণে পাবো?", "sup_faq1_a": "২৪ ঘণ্টার ভিতরে", "sup_faq2_q": "Refer টাকা কখন পাবো?", "sup_faq2_a": "বন্ধু Join করলেই", "sup_faq3_q": "Ads দেখলে টাকা আসে না কেন?", "sup_faq3_a": "VPN বন্ধ করুন",
                "sup_rules": "1. একাধিক একাউন্ট খুলবেন না\n2. ভুল তথ্য দিবেন না\n3. Fake Refer করবেন না",
                "support_bottom_title": "📢 Important Update", "support_bottom_desc": "Admin থেকে কন্ট্রোল", "support_bottom_btn": "Contact Now", "support_bottom_link": "https://t.me/",
                "profile_bottom_title": "💎 VIP Membership", "profile_bottom_desc": "VIP হলে বেশি ইনকাম", "profile_bottom_btn": "⭐ Upgrade Now", "profile_bottom_link": "https://google.com"
            },
            "tasks": [
                {"id":"t1","icon":"🌐","title":"Visit Company Website","reward":0.2,"link":"https://google.com"},
                {"id":"t2","icon":"▶️","title":"Watch Popup Ad","reward":0.3,"link":"https://youtube.com"},
                {"id":"t3","icon":"📢","title":"Join Telegram Channel","reward":0.5,"link":"https://t.me/"}
            ],
            "wds": []
        }
    with open(DB_FILE,"r") as f: return json.load(f)

def save_db(db):
    with open(DB_FILE,"w") as f: json.dump(db,f,indent=2)

# ---------- HOME - 5 PAGES ----------
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
.spon-big{{background:linear-gradient(135deg,#2D1B4E,#1A1033);border:1px solid #f59e0b;padding:18px;border-radius:22px;margin:12px}}
.contest{{background:linear-gradient(90deg,#f59e0b,#f97316);color:#000;padding:14px;border-radius:18px;margin:12px;text-align:center;font-weight:800}}
.proImg{{width:90px;height:90px;border-radius:20px;background:#0B0E1C;border:2px solid #8b5cf6;display:flex;align-items:center;justify-content:center;font-size:40px;overflow:hidden;margin:0 auto}}
.stat4{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}}.stat4 div{{background:#0B0E1C;border:1px solid #1e293b;padding:14px;border-radius:16px;text-align:center}}
.inputDark{{width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px;outline:none}}
.page{{display:none}}.page.active{{display:block}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:22px;display:block}}
</style></head><body>
<div id='p-home' class='page active'>
  <div class='top2'><div class='topbox'>👑 {s['app_name']}</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD ✅ <span style='float:right;color:#22c55e' id='balTop'>৳20</span></div></div>
  <div class='glass'><b id='balShow' style='color:#22c55e;font-size:26px'>৳20</b><br><small>💎 <span id='diamondTop'>2000</span> Diamond | <span id='adsCount'>0/80</span> Ads</small></div>
  <div style='display:flex;gap:10px;margin:0 12px'><div class='glass' style='flex:1;margin:0'><b>Company ৳{s['ad']}</b><br><small id='cToday'>0/{s['clim']}</small><button class='btn' onclick='watchAd("c")'>Start</button></div><div class='glass' style='flex:1;margin:0'><b>Popup ৳{s['pop']}</b><br><small id='pToday'>0/{s['plim']}</small><button class='btn' style='background:{s['secondary']};color:#000' onclick='watchAd("p")'>Watch</button></div></div>
  <div class='glass'><h3>💸 Withdraw</h3><div style='display:flex;gap:10px;margin-top:12px'><div class='meth on' id='m-bKash' onclick="setMeth('bKash')">bKash</div><div class='meth' id='m-Nagad' onclick="setMeth('Nagad')">Nagad</div></div><input id='wNum' class='inputDark' placeholder='01XXXXXXXXX' /><input id='wAmt' class='inputDark' type='number' placeholder='Min {s['min']}' /><button class='btn' onclick='doWD()'>Withdraw Now</button></div>
  <div class='spon-big'><h3>🔥 {s['spon_title']}</h3><p>{s['spon_desc']}</p><button class='btn' style='background:#f59e0b;color:#000' onclick="window.open('{s['spon_link']}')">{s['spon_btn']}</button></div>
</div>
<div id='p-tasks' class='page'><div class='glass'><h2>🎯 {s['task_page_title']}</h2><p style='opacity:.6'>{s['task_page_sub']}</p><div id='tasksList'></div></div><div class='spon-big' style='border-color:#8b5cf6'><h3>{s['task_bottom_title']}</h3><p>{s['task_bottom_desc']}</p><button class='btn' onclick="window.open('{s['task_bottom_link']}')">{s['task_bottom_btn']}</button></div></div>
<div id='p-refer' class='page'><div class='contest'>{s['ref_banner']}</div><div class='glass'><h2>👥 {s['ref_title']}</h2><p>{s['ref_desc']}</p><div class='inputDark' id='refLinkBox'>Loading...</div><button class='btn' onclick='copyRef()'>Copy Link</button><div style='white-space:pre-line;margin-top:10px'>{s['ref_rules']}</div></div><div class='spon-big' style='border-color:#22c55e'><h3>{s['refer_bottom_title']}</h3><p>{s['refer_bottom_desc']}</p><button class='btn' style='background:#22c55e;color:#000' onclick="window.open('{s['refer_bottom_link']}')">{s['refer_bottom_btn']}</button></div></div>
<div id='p-support' class='page'><div class='glass'><h2>{s['sup_title']}</h2><p>{s['sup_desc']}</p></div><div class='glass'><h3>📞 Contact Us</h3><div style='display:flex;gap:10px;margin-top:10px'><div style='flex:1;background:#8b5cf6;padding:12px;border-radius:12px;text-align:center' onclick="window.open('{s['sup_tg']}')">Telegram</div><div style='flex:1;background:#f59e0b;color:#000;padding:12px;border-radius:12px;text-align:center' onclick="window.open('{s['sup_wa']}')">WhatsApp</div></div><div class='inputDark'>📧 {s['sup_email']}</div></div><div class='glass' style='border-color:#f59e0b'><h3>📢 Notice</h3><div style='white-space:pre-line'>{s['sup_notice']}</div></div><div class='glass'><h3>❓ FAQ</h3><p><b>{s['sup_faq1_q']}</b><br>{s['sup_faq1_a']}</p><p style='margin-top:8px'><b>{s['sup_faq2_q']}</b><br>{s['sup_faq2_a']}</p></div><div class='glass'><h3>📜 Rules</h3><div style='white-space:pre-line'>{s['sup_rules']}</div></div><div class='glass' style='border-color:#22c55e'><h3>{s['support_bottom_title']}</h3><p>{s['support_bottom_desc']}</p><button class='btn' style='background:#22c55e;color:#000' onclick="window.open('{s['support_bottom_link']}')">{s['support_bottom_btn']}</button></div></div>
<div id='p-profile' class='page'><div class='glass' style='text-align:center'><div class='proImg' id='proImgWrap'><img id='proImg' src='' style='width:100%;height:100%;object-fit:cover;display:none'><span id='proEmoji'>💎</span></div><h2 id='pNameShow'>User 4250</h2><p id='pJoin' style='opacity:.6'>Join: 2026-09-15</p><p>💎 <span id='pDiamond'>2000</span> Diamond | <span id='pBal2'>20</span> Taka</p></div><div class='glass'><h3>📊 Statistics</h3><div class='stat4'><div><b style='color:#22c55e' id='statEarned'>৳20</b><br><small>Total Earned</small></div><div><b style='color:#8b5cf6' id='statBal'>৳20</b><br><small>Balance</small></div><div><b style='color:#f59e0b' id='statAds'>0</b><br><small>Ads</small></div><div><b style='color:#ec4899' id='statRefer'>0</b><br><small>Refer</small></div></div></div><div class='glass'><h3>⚙️ Account</h3><div class='inputDark' id='accId'>...</div><input class='inputDark' id='accNameInput' placeholder='Name' /><input type='file' id='accPhoto' accept='image/*' class='inputDark' onchange='previewPhoto(this)' /><div id='previewWrap' style='display:none;margin-top:8px'><img id='previewImg' style='width:80px;height:80px;border-radius:12px;object-fit:cover'></div><button class='btn' onclick='saveProfile()'>💾 Save Profile</button></div><div class='glass'><h3>💸 Withdraw History</h3><div id='wdHistList'>No withdraw</div></div><div class='glass' style='border-color:#8b5cf6'><h3>{s['profile_bottom_title']}</h3><p>{s['profile_bottom_desc']}</p><button class='btn' onclick="window.open('{s['profile_bottom_link']}')">{s['profile_bottom_btn']}</button></div></div>
<div class='btm'><div class='on' id='b-home' onclick="showP('home')"><span>🏠</span>Home</div><div id='b-tasks' onclick="showP('tasks')"><span>🎯</span>Tasks</div><div id='b-refer' onclick="showP('refer')"><span>👥</span>Refer</div><div id='b-support' onclick="showP('support')"><span>💬</span>Support</div><div id='b-profile' onclick="showP('profile')"><span>👤</span>Profile</div></div>
<script>
let curMeth='bKash'; let uid=localStorage.getItem('uid')||'8807178385_4250'; localStorage.setItem('uid',uid);
function setMeth(m){{curMeth=m;document.querySelectorAll('.meth').forEach(e=>e.classList.remove('on'));document.getElementById('m-'+m).classList.add('on');}}
function showP(id){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p-'+id).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));document.getElementById('b-'+id).classList.add('on'); if(id=='tasks') loadTasks(); init();}}
function watchAd(t){{let fn=t=='c'?window['show_{s["company_ad_id"]}']:window['show_{s["popup_ad_id"]}']; if(typeof fn==='function'){{fn().then(()=>sendReward(t)).catch(()=>sendReward(t));}} else {{ setTimeout(()=>sendReward(t),1500);}}}}
function sendReward(t){{fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:t}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}}
function doWD(){{let num=document.getElementById('wNum').value;let amt=document.getElementById('wAmt').value; if(!num||!amt) return alert('Number & Amount দিন'); fetch('/api/wd',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,amt:amt,num:num,m:curMeth}})}}).then(r=>r.json()).then(d=>alert(d.msg));}}
function loadTasks(){{fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}}).then(r=>r.json()).then(d=>{{let html=''; d.tasks.forEach(t=>{{html+=`<div class='task-card'><div><b>${{t.icon}} ${{t.title}}</b><div style='color:#22c55e'>৳${{t.reward}}</div></div><button style='background:#8b5cf6;color:#fff;border:none;padding:8px 16px;border-radius:20px' onclick="window.open('${{t.link}}','_blank'); setTimeout(()=>{{fetch('/api/task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,tid:t.id}})}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}},30000);">Go</button></div>`;}}); document.getElementById('tasksList').innerHTML=html;}});}}
function copyRef(){{let txt=document.getElementById('refLinkBox').innerText; navigator.clipboard.writeText(txt).then(()=>alert('Copy Done!'));}}
function previewPhoto(input){{ if(input.files && input.files[0]){{ let r=new FileReader(); r.onload=e=>{{document.getElementById('previewImg').src=e.target.result; document.getElementById('previewWrap').style.display='block'; document.getElementById('proImg').src=e.target.result; document.getElementById('proImg').style.display='block'; document.getElementById('proEmoji').style.display='none';}}; r.readAsDataURL(input.files[0]);}}}}
function saveProfile(){{let name=document.getElementById('accNameInput').value; let file=document.getElementById('accPhoto').files[0]; let fd=new FormData(); fd.append('id',uid); fd.append('name',name); if(file) fd.append('photo',file); fetch('/api/profile',{{method:'POST',body:fd}}).then(r=>r.json()).then(d=>{{alert(d.msg); init();}});}}
function init(){{fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}}).then(r=>r.json()).then(d=>{{let u=d.user; document.getElementById('balShow').innerText='৳'+u.bal; document.getElementById('balTop').innerText='৳'+u.bal; let b2=document.getElementById('balTop2'); if(b2) b2.innerText='৳'+u.bal; document.getElementById('diamondTop').innerText=u.diamonds; document.getElementById('pNameShow').innerText=u.name; document.getElementById('pDiamond').innerText=u.diamonds; document.getElementById('pBal2').innerText=u.bal; document.getElementById('statEarned').innerText='৳'+u.bal; document.getElementById('statBal').innerText='৳'+u.bal; document.getElementById('statAds').innerText=(u.c_today||0)+(u.p_today||0); document.getElementById('statRefer').innerText=u.refl?u.refl.length:0; document.getElementById('accId').innerText=u.id; document.getElementById('cToday').innerText=(u.c_today||0)+'/{s['clim']}'; document.getElementById('pToday').innerText=(u.p_today||0)+'/{s['plim']}'; if(u.photo){{document.getElementById('proImg').src=u.photo; document.getElementById('proImg').style.display='block'; document.getElementById('proEmoji').style.display='none';}} document.getElementById('refLinkBox').innerText=window.location.origin+'/?ref='+u.id; if(d.wds.length>0) document.getElementById('wdHistList').innerHTML=d.wds.map(w=>`<div style="padding:10px;background:#0B0E1C;border-radius:10px;margin-top:6px;display:flex;justify-content:space-between"><div>${{w.m}} ${{w.num}}</div><div>৳${{w.amt}} ${{w.st}}</div></div>`).join('');}});}} init(); loadTasks();
</script></body></html>
""")

# ---------- ADMIN PANEL - এটা আগে ছিল না, এখন যোগ করলাম ----------
@app.route('/admin')
def admin():
    db=load_db(); s=db["settings"]
    # সব সেটিংস input এ দেখানোর জন্য
    fields_html=""
    for k,v in s.items():
        # textarea for long text
        if len(str(v))>60 or "desc" in k or "rules" in k or "notice" in k:
            fields_html+=f"<label>{k}</label><textarea name='{k}' style='width:100%;padding:10px;margin:6px 0;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333'>{v}</textarea>"
        else:
            fields_html+=f"<label>{k}</label><input name='{k}' value='{v}' style='width:100%;padding:10px;margin:6px 0;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333' />"

    tasks_json=json.dumps(db["tasks"],indent=2,ensure_ascii=False)
    wds_html="".join([f"<div style='background:#111;padding:10px;margin:5px 0;border-radius:8px;display:flex;justify-content:space-between'><div>{w['uid']} - {w['m']} {w['num']} - ৳{w['amt']} - {w['st']}</div><div><a href='/admin/approve/{w['uid']}/{w['amt']}' style='color:#22c55e'>Approve</a> | <a href='/admin/reject/{w['uid']}/{w['amt']}' style='color:#ef4444'>Reject</a></div></div>" for w in db.get("wds",[])])

    return render_template_string(f"""
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><style>
body{{background:#0B0E1C;color:#fff;font-family:system-ui;max-width:700px;margin:auto;padding:20px}}
label{{font-weight:700;margin-top:12px;display:block;color:#a78bfa}}
.btn{{width:100%;padding:14px;background:#8b5cf6;color:#fff;border:none;border-radius:12px;font-weight:800;margin-top:20px;cursor:pointer}}
.card{{background:#1A2040;padding:16px;border-radius:16px;margin:12px 0;border:1px solid #2a2f4a}}
</style></head><body>
<h1>🔧 Admin Panel - সব কন্ট্রোল</h1>
<p>Link: /admin - এখান থেকে ৫টা পেইজের নিচের বক্স সহ সব চেঞ্জ করতে পারবে</p>
<form method='POST' action='/admin/save'>
<div class='card'><h3>⚙️ General Settings</h3>{fields_html}</div>
<div class='card'><h3>🎯 Tasks JSON (Icon, Title, Reward, Link)</h3><textarea name='tasks_json' style='width:100%;height:200px;padding:10px;background:#0B0E1C;color:#fff;border-radius:8px'>{tasks_json}</textarea></div>
<button class='btn'>💾 Save All Settings</button>
</form>
<div class='card'><h3>💸 Withdraw Requests - {len(db.get("wds",[]))} টা</h3>{wds_html if wds_html else "<p>No withdraw</p>"}</div>
<div class='card'><h3>👥 Users - {len(db["users"])} জন</h3><div style='max-height:300px;overflow:auto'>{"".join([f"<div style='padding:6px;border-bottom:1px solid #333'>{u['id']} - {u['name']} - ৳{u['bal']} - 💎{u['diamonds']} - Refer:{len(u.get('refl',[]))}</div>" for u in db["users"].values()])}</div></div>
</body></html>
""")

@app.route('/admin/save', methods=['POST'])
def admin_save():
    db=load_db()
    for k in db["settings"].keys():
        if k in request.form:
            # number handle
            v=request.form[k]
            # try float
            try:
                if k in ["ad","pop"]: db["settings"][k]=float(v)
                elif k in ["clim","plim","min","ref"]: db["settings"][k]=int(float(v))
                else: db["settings"][k]=v
            except: db["settings"][k]=v
    # tasks json
    if "tasks_json" in request.form:
        try:
            db["tasks"]=json.loads(request.form["tasks_json"])
        except: pass
    save_db(db)
    return "<script>alert('✅ Saved!'); location.href='/admin';</script>"

@app.route('/admin/approve/<uid>/<amt>')
def admin_approve(uid,amt):
    db=load_db()
    for w in db.get("wds",[]):
        if w["uid"]==uid and str(w["amt"])==amt:
            w["st"]="Approved"
    save_db(db)
    return "<script>location.href='/admin';</script>"

@app.route('/admin/reject/<uid>/<amt>')
def admin_reject(uid,amt):
    db=load_db()
    for w in db.get("wds",[]):
        if w["uid"]==uid and str(w["amt"])==amt:
            w["st"]="Rejected"
            # refund
            if w["uid"] in db["users"]:
                db["users"][w["uid"]]["bal"]+=float(w["amt"])
    save_db(db)
    return "<script>location.href='/admin';</script>"

@app.route('/api/init', methods=['POST'])
def api_init():
    db=load_db(); d=request.json; uid=d.get('id','4250')
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":20,"diamonds":2000,"c_today":0,"p_today":0,"refl":[],"photo":"","join":datetime.now().strftime("%Y-%m-%d")}
        # refer check
        ref=d.get('ref') or request.args.get('ref')
        if ref and ref in db["users"]:
            db["users"][uid]["referred_by"]=ref
            db["users"][ref].setdefault("refl",[]).append(uid)
            db["users"][ref]["bal"]+=db["settings"]["ref"]
        save_db(db)
    u=db["users"][uid]; wds=[w for w in db.get("wds",[]) if w.get("uid")==uid]
    return jsonify({"user":u,"tasks":db["tasks"],"wds":wds})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    db=load_db(); d=request.json; uid=d["id"]; typ=d["type"]; u=db["users"].get(uid); s=db["settings"]
    if not u: return jsonify({"msg":"User not found"})
    if typ=="c" and u["c_today"]>=s["clim"]: return jsonify({"msg":f"Limit {s['clim']} done"})
    if typ=="p" and u["p_today"]>=s["plim"]: return jsonify({"msg":f"Limit {s['plim']} done"})
    reward=s["ad"] if typ=="c" else s["pop"]; u["bal"]+=reward; u["diamonds"]+=int(reward*100)
    if typ=="c": u["c_today"]+=1
    else: u["p_today"]+=1
    save_db(db); return jsonify({"msg":f"✅ ৳{reward} Added!"})

@app.route('/api/task', methods=['POST'])
def api_task():
    db=load_db(); d=request.json; uid=d["id"]; tid=d["tid"]; u=db["users"].get(uid)
    task=next((t for t in db["tasks"] if t["id"]==tid),None)
    if not task: return jsonify({"msg":"Task not found"})
    u["bal"]+=task["reward"]; u["diamonds"]+=int(task["reward"]*100); save_db(db)
    return jsonify({"msg":f"✅ ৳{task['reward']} + Diamond Added!"})

@app.route('/api/wd', methods=['POST'])
def api_wd():
    db=load_db(); d=request.json; uid=d["id"]; amt=float(d["amt"]); s=db["settings"]; u=db["users"].get(uid)
    if amt < s["min"]: return jsonify({"msg":f"Min ৳{s['min']}"})
    if u["bal"] < amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt; db.setdefault("wds",[]).append({"uid":uid,"amt":amt,"num":d["num"],"m":d["m"],"st":"Pending","time":datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_db(db); return jsonify({"msg":"✅ Withdraw Sent!"})

@app.route('/api/profile', methods=['POST'])
def save_profile():
    db=load_db(); uid=request.form.get('id') or (request.json.get('id') if request.is_json else None)
    name=request.form.get('name') or (request.json.get('name') if request.is_json else None)
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    if name: db["users"][uid]["name"]=name
    if 'photo' in request.files:
        f=request.files['photo']; b64=base64.b64encode(f.read()).decode()
        db["users"][uid]["photo"]=f"data:{f.mimetype};base64,{b64}"
    save_db(db); return jsonify({"msg":"✅ Profile Saved!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
