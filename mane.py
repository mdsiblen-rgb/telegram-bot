# -*- coding: utf-8 -*-
# FINAL A-Z with Blink Blink - Protidiner Kaj BD
import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

def default():
    return {
        "users": {},
        "settings": {
            "app_name": "Protidiner Kaj BD",
            "admin_name": "SHIBLI NOMAN",
            "app_logo": "👑",
            "admin_profile": "",
            "admin_profile_img": "",
            "zone": "11764581",
            "bonus": 1120,
            "ad_reward": 2,
            "popup_reward": 3,
            "company_limit": 30,
            "popup_limit": 20,
            "task_limit": 5,
            "min_with": 500,
            "official_banners": [],
            "google_ads": [
                "🎉 Daily Bonus Available Today",
                "⭐ Official Ad • bKash • Nagad • Daraz • Trusted",
                "📢 Company Sponsored • 100% Safe"
            ],
            "offer_title": "🎉 আজকের স্পেশাল অফার",
            "offer_desc": "প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস! দ্রুত কাজ করুন",
            "balance_title": "আপনার বর্তমান ব্যালেন্স"
        },
        "tasks": [
            {"title": "Telegram Channel", "reward": 25, "icon": "✈️"},
            {"title": "Telegram Group", "reward": 20, "icon": "👥"},
            {"title": "YouTube Subscribe", "reward": 30, "icon": "▶️"},
            {"title": "Refer Friend", "reward": 50, "icon": "👨‍👩‍👧‍👦"},
            {"title": "Daily Check-in", "reward": 15, "icon": "✅"}
        ]
    }

def load():
    if not os.path.exists(DB):
        d = default()
        json.dump(d, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return d
    try:
        return json.load(open(DB, 'r', encoding='utf-8'))
    except:
        d = default()
        json.dump(d, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return d

def save(d):
    json.dump(d, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def getu(db, uid):
    uid = str(uid)
    today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "balance": db["settings"]["bonus"], "ads_today": 0, "popup_today": 0, "total": 0, "last": today}
    u = db["users"][uid]
    if u["last"]!= today:
        u["ads_today"] = 0
        u["popup_today"] = 0
        u["last"] = today
    return u

@app.route('/')
def home():
    return render_template_string(USER)

@app.route('/admin')
def admin_page():
    if request.args.get('id')!= '8807178385':
        return "Admin only? add?id=8807178385", 403
    return render_template_string(ADMIN)

@app.route('/api/get')
def api_get():
    db = load()
    u = getu(db, request.args.get('id', '0'))
    save(db)
    return jsonify({"user": u, "settings": db["settings"], "tasks": db["tasks"]})

@app.route('/api/reward')
def api_reward():
    db = load()
    u = getu(db, request.args.get('id'))
    typ = request.args.get('type', 'company')
    s = db["settings"]
    if typ == 'company':
        if u["ads_today"] >= s["company_limit"]:
            return jsonify({"ok": False, "msg": f"Company Limit {s['company_limit']} শেষ"})
        u["ads_today"] += 1
        u["balance"] += s["ad_reward"]
    else:
        if u["popup_today"] >= s["popup_limit"]:
            return jsonify({"ok": False, "msg": f"Popup Limit {s['popup_limit']} শেষ"})
        u["popup_today"] += 1
        u["balance"] += s["popup_reward"]
    u["total"] += 1
    save(db)
    return jsonify({"ok": True, "msg": f"৳{s['ad_reward' if typ=='company' else 'popup_reward']} যোগ হয়েছে ✅"})

@app.route('/api/admin/save', methods=['POST'])
def api_save():
    db = load()
    j = request.json
    for k in j:
        if k.startswith("google_ad"):
            try:
                idx = int(k[-1]) - 1
                if 0 <= idx < 3:
                    db["settings"]["google_ads"][idx] = j[k]
            except:
                pass
        else:
            db["settings"][k] = j[k]
    save(db)
    return jsonify({"msg": "✅ Saved - সাথে সাথে অ্যাপে আপডেট"})

@app.route('/api/admin/upload', methods=['POST'])
def upload():
    db = load()
    j = request.json
    if 'img' in j:
        db["settings"]["admin_profile_img"] = j['img']
        save(db)
        return jsonify({"msg": "✅ প্রোফাইল ছবি আপডেট হয়েছে"})
    if 'banner' in j:
        if len(db["settings"]["official_banners"]) >= 5:
            db["settings"]["official_banners"].pop(0)
        db["settings"]["official_banners"].append(j['banner'])
        save(db)
        return jsonify({"msg": f"✅ ব্যানার {len(db['settings']['official_banners'])}/5 যোগ হয়েছে"})
    if 'clear_banner' in j:
        db["settings"]["official_banners"] = []
        save(db)
        return jsonify({"msg": "🗑️ সব ব্যানার মুছে ফেলা হয়েছে"})
    return jsonify({"msg": "Error"})

USER = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#070710;color:#fff;max-width:430px;margin:0 auto;padding-bottom:125px}
.top{padding:14px 16px;display:flex;justify-content:space-between;align-items:center;background:#0e0e20;position:sticky;top:0;z-index:99;border-bottom:1px solid rgba(255,255,255,0.08)}
.card{margin:12px;border-radius:20px;padding:16px;background:linear-gradient(180deg,#17172a,#0e0e20);border:1px solid #222;position:relative;overflow:hidden}
.btn{width:100%;padding:18px;border:none;border-radius:16px;font-weight:900;font-size:15px;color:#fff;margin-top:12px;cursor:pointer}
.profile{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#1e293b,#334155);display:flex;align-items:center;justify-content:center;border:2px solid #6d4cff;overflow:hidden;box-shadow:0 0 15px rgba(109,76,255,0.5);font-size:26px}
.profile img{width:100%;height:100%;object-fit:cover}
@keyframes blinkGlow{0%{box-shadow:0 0 12px rgba(245,158,11,0.5);transform:scale(1)}50%{box-shadow:0 0 35px rgba(245,158,11,1),0 0 60px rgba(239,68,68,0.7);transform:scale(1.02)}100%{box-shadow:0 0 12px rgba(245,158,11,0.5);transform:scale(1)}}
@keyframes moneyBlink{0%{text-shadow:0 0 10px rgba(255,255,255,0.6);transform:scale(1)}50%{text-shadow:0 0 25px #fff,0 0 45px #fde047,0 0 70px #f59e0b;transform:scale(1.08)}100%{text-shadow:0 0 10px rgba(255,255,255,0.6);transform:scale(1)}}
@keyframes shineMove{0%{left:-100%}100%{left:200%}}
.bannerBox{margin:12px;border-radius:22px;overflow:hidden;height:185px;background:linear-gradient(90deg,#f59e0b,#ef4444);position:relative;border:2px solid rgba(255,255,255,0.2);animation:blinkGlow 2s infinite ease-in-out}
.bannerBox img{width:100%;height:100%;object-fit:cover}
.bannerText{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.9));padding:34px 14px 14px;font-weight:900;text-align:center;font-size:15px}
.shine{position:absolute;top:0;left:-100%;width:70%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.45),transparent);transform:skewX(-20deg);animation:shineMove 2.5s infinite;z-index:2}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(14,14,32,0.98);display:flex;padding:10px 0 14px;border-radius:24px 24px 0 0;border-top:1px solid #222;z-index:99}
.btm div{flex:1;text-align:center;color:#6b7280;font-size:11px;font-weight:800}.btm div.on{color:#fff}.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
.blinkBalance{animation:blinkGlow 2s infinite}
</style></head><body>

<div class="top">
<div style="display:flex;align-items:center;gap:10px">
<div style="font-size:30px" id="appLogo">👑</div>
<div>
<div style="font-weight:900;font-size:17px;display:flex;align-items:center;gap:6px"><span id="appName">Protidiner Kaj BD</span><span style="background:#22c55e;color:#fff;font-size:11px;padding:2px 6px;border-radius:6px">✓</span></div>
<div style="font-size:11px;opacity:0.6" id="adminName">Admin: SHIBLI NOMAN</div>
</div>
</div>
<div class="profile" id="profBox">👤</div>
</div>

<div id="p-home" class="page active">
<div class="bannerBox" id="bannerBox"><div class="shine"></div><div style="height:100%;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:900;font-size:16px" id="gAd">Loading...</div></div>

<div class="card blinkBalance" style="text-align:center;background:linear-gradient(135deg,#1e3a8a,#3b82f6,#06b6d4,#10b981,#f59e0b);padding:30px 18px;border:2px solid rgba(255,255,255,0.25);box-shadow:0 10px 40px rgba(59,130,246,0.35)">
<div class="shine"></div>
<div style="font-size:11px;letter-spacing:2px;color:#e0f2fe;font-weight:700;position:relative;z-index:3" id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div>
<div style="font-size:62px;font-weight:900;margin:10px 0;color:#fff;position:relative;z-index:3"><span style="display:inline-block;animation:moneyBlink 1.4s infinite">৳<span id="bal">0</span></span></div>
<div style="display:flex;justify-content:center;gap:6px;flex-wrap:wrap;position:relative;z-index:3">
<span style="background:rgba(0,0,0,0.35);padding:6px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,0.15)">Company <b id="ads" style="color:#fde047">0</b>/<span id="adsLim">30</span></span>
<span style="background:rgba(0,0,0,0.35);padding:6px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,0.15)">Popup <b id="pop" style="color:#86efac">0</b>/<span id="popLim">20</span></span>
<span style="background:rgba(0,0,0,0.35);padding:6px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,0.15)">Total <b id="total">0</b></span>
</div>
<div style="background:rgba(0,0,0,0.45);height:10px;border-radius:20px;margin-top:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.2);position:relative;z-index:3"><div id="prog" style="height:100%;background:linear-gradient(90deg,#fde047,#fbbf24);width:0%;border-radius:20px;transition:width 1s"></div></div>
</div>

<div class="card">
<button class="btn" style="background:linear-gradient(90deg,#6d4cff,#3a1aff)" onclick="watchAd()">📺 COMPANY ADS দেখুন (৳<span id="r1">2</span>) - <span id="ads2">0</span>/<span id="adsLim2">30</span></button>
<button class="btn" style="background:linear-gradient(90deg,#00c853,#009624)" onclick="watchPop()">💰 POPUP ADS (৳<span id="r2">3</span>) - <span id="pop2">0</span>/<span id="popLim2">20</span></button>
<button class="btn" style="background:#1e293b">📋 TASK BONUS - 5 টা/দিন</button>
</div>

<div class="card" style="border:2px solid #fbbf24;background:linear-gradient(135deg,rgba(251,191,36,0.15),#0e0e20)"><div style="font-weight:900" id="offerTitle"></div><div style="font-size:13px;margin-top:6px;opacity:0.9" id="offerDesc"></div></div>
</div>

<div class="btm"><div class="on"><span>🏠</span>Home</div><div><span>📋</span>Task</div><div><span>💰</span>Wallet</div><div><span>💬</span>Support</div><div><span>👤</span>Profile</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let gAds=[],banners=[],idx=0;
async function load(){
 let r=await fetch('/api/get?id='+uid).then(x=>x.json());let s=r.settings;let u=r.user;
 document.getElementById('bal').innerText=u.balance;
 document.getElementById('ads').innerText=u.ads_today;document.getElementById('pop').innerText=u.popup_today;
 document.getElementById('ads2').innerText=u.ads_today;document.getElementById('pop2').innerText=u.popup_today;
 document.getElementById('total').innerText=u.total;
 document.getElementById('adsLim').innerText=s.company_limit;document.getElementById('adsLim2').innerText=s.company_limit;
 document.getElementById('popLim').innerText=s.popup_limit;document.getElementById('popLim2').innerText=s.popup_limit;
 document.getElementById('r1').innerText=s.ad_reward;document.getElementById('r2').innerText=s.popup_reward;
 document.getElementById('appName').innerText=s.app_name;document.getElementById('adminName').innerText='Admin: '+s.admin_name;
 document.getElementById('appLogo').innerText=s.app_logo;document.getElementById('balTitle').innerText='💰 '+s.balance_title;
 document.getElementById('offerTitle').innerText=s.offer_title;document.getElementById('offerDesc').innerText=s.offer_desc;
 gAds=s.google_ads;banners=s.official_banners||[];
 document.getElementById('prog').style.width=((u.ads_today+u.popup_today)/(s.company_limit+s.popup_limit)*100)+'%';
 let pb=document.getElementById('profBox');
 if(s.admin_profile_img && s.admin_profile_img.startsWith('data:image')){pb.innerHTML=`<img src="${s.admin_profile_img}">`;}
 else{pb.innerHTML=s.admin_profile||'👤';}
 renderBanner();
}
function renderBanner(){
 let box=document.getElementById('bannerBox');
 if(banners.length>0){
   let img=banners[idx % banners.length];
   box.innerHTML=`<div class="shine"></div><img src="${img}"><div class="bannerText">${gAds[idx % gAds.length]||''}</div>`;
 }else{
   box.innerHTML=`<div class="shine"></div><div style="height:100%;display:flex;align-items:center;justify-content:center;padding:20px;text-align:center;font-weight:900;font-size:16px;background:linear-gradient(90deg,#f59e0b,#ef4444)">${gAds[idx % gAds.length]||'Official Ad'}</div>`;
 }
}
function watchAd(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে, 2 সেকেন্ড পর আবার চাপো');return;}show_11764581().then(()=>{fetch('/api/reward?id='+uid+'&type=company').then(x=>x.json()).then(d=>{alert(d.msg);load();});});}
function watchPop(){if(typeof show_11764581==='undefined'){alert('Ad Load হচ্ছে');return;}show_11764581('pop').then(()=>{fetch('/api/reward?id='+uid+'&type=popup').then(x=>x.json()).then(d=>{alert(d.msg);load();});}).catch(()=>{});}
setInterval(()=>{idx++;renderBanner();},3000);
load();
</script></body></html>
"""

ADMIN = """
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0f0f0f;color:#fff;font-family:sans-serif;padding:16px}
input,textarea{width:100%;padding:12px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff}
.card{background:#1e1e1e;padding:16px;border-radius:12px;margin:12px 0}
.btn{padding:14px;width:100%;border:none;border-radius:10px;background:#6d4cff;color:#fff;font-weight:900;margin-top:8px;cursor:pointer}
.prev{width:100%;height:140px;border-radius:12px;object-fit:cover;margin-top:8px;border:2px solid #333;display:none}
.prev2{width:80px;height:80px;border-radius:50%;object-fit:cover;margin-top:8px;border:2px solid #6d4cff;display:none}
</style>
</head><body>
<h2>👑 Full Admin - All Control + Blink</h2>

<div class="card" style="border:2px solid #f59e0b">
<h3>⭐ উপরের বড় ব্যানার - ফটো (মিট মিট করবে)</h3>
<input type="file" id="bannerFile" accept="image/*">
<img id="bannerPrev" class="prev">
<button class="btn" style="background:#f59e0b" onclick="uploadBanner()">📸 ব্যানার যোগ করুন - 5 টা পর্যন্ত</button>
<button class="btn" style="background:#ef4444" onclick="clearBanner()">🗑️ সব ব্যানার মুছুন</button>
<div id="bannerCount" style="font-size:12px;margin-top:8px"></div>
</div>

<div class="card" style="border:2px solid #6d4cff">
<h3>👤 প্রোফাইল ছবি - বড় (52px)</h3>
<input type="file" id="fileIn" accept="image/*">
<img id="preview" class="prev2">
<button class="btn" style="background:#00c853" onclick="uploadImg()">📤 প্রোফাইল আপলোড - গ্যালারি থেকে</button>
</div>

<div class="card"><h3>📝 নাম / লোগো / ব্যালেন্স টাইটেল</h3>App Name:<input id="app_name">Admin Name:<input id="admin_name">Logo Emoji:<input id="app_logo">Balance Title:<input id="balance_title"></div>
<div class="card"><h3>📢 নিচের Ad লেখা (3 টা ঘুরবে)</h3>Ad Text 1:<input id="g1">Ad Text 2:<input id="g2">Ad Text 3:<input id="g3"></div>
<div class="card"><h3>🎁 অফার বক্স</h3>Title:<input id="offer_title">Desc:<textarea id="offer_desc"></textarea></div>
<div class="card"><h3>💰 টাকা ও লিমিট</h3>Company Limit:<input id="company_limit" type="number">Company Reward:<input id="ad_reward" type="number">Popup Limit:<input id="popup_limit" type="number">Popup Reward:<input id="popup_reward" type="number"></div>

<button class="btn" style="background:#6d4cff;padding:18px;font-size:16px" onclick="save()">💾 Save All - সাথে সাথে অ্যাপে মিট মিট সহ আপডেট</button>
<div id="msg" style="text-align:center;margin-top:12px;font-weight:800;color:#fde047"></div>

<script>
let base64="",banner64="";
document.getElementById('fileIn').addEventListener('change',e=>{let r=new FileReader();r.onload=ev=>{base64=ev.target.result;let p=document.getElementById('preview');p.src=base64;p.style.display='block';};r.readAsDataURL(e.target.files[0]);});
document.getElementById('bannerFile').addEventListener('change',e=>{let r=new FileReader();r.onload=ev=>{banner64=ev.target.result;let p=document.getElementById('bannerPrev');p.src=banner64;p.style.display='block';};r.readAsDataURL(e.target.files[0]);});
async function uploadImg(){if(!base64){alert('আগে ছবি সিলেক্ট করো');return;}let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({img:base64})}).then(x=>x.json());msg.innerText=res.msg;}
async function uploadBanner(){if(!banner64){alert('ব্যানার ফটো সিলেক্ট করো');return;}let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({banner:banner64})}).then(x=>x.json());msg.innerText=res.msg;load();banner64='';}
async function clearBanner(){if(!confirm('সব ব্যানার মুছবে?'))return;let res=await fetch('/api/admin/upload',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({clear_banner:1})}).then(x=>x.json());msg.innerText=res.msg;load();}
async function load(){let s=await fetch('/api/get?id=8807178385').then(x=>x.json()).then(x=>x.settings);app_name.value=s.app_name;admin_name.value=s.admin_name;app_logo.value=s.app_logo;balance_title.value=s.balance_title;g1.value=s.google_ads[0];g2.value=s.google_ads[1];g3.value=s.google_ads[2];offer_title.value=s.offer_title;offer_desc.value=s.offer_desc;company_limit.value=s.company_limit;ad_reward.value=s.ad_reward;popup_limit.value=s.popup_limit;popup_reward.value=s.popup_reward;bannerCount.innerText=`বর্তমানে ${s.official_banners.length}/5 টা ব্যানার আছে - এগুলো মিট মিট করবে`;if(s.admin_profile_img){preview.src=s.admin_profile_img;preview.style.display='block';base64=s.admin_profile_img;}}
async function save(){let d={app_name:app_name.value,admin_name:admin_name.value,app_logo:app_logo.value,balance_title:balance_title.value,google_ad1:g1.value,google_ad2:g2.value,google_ad3:g3.value,offer_title:offer_title.value,offer_desc:offer_desc.value,company_limit:parseInt(company_limit.value),ad_reward:parseInt(ad_reward.value),popup_limit:parseInt(popup_limit.value),popup_reward:parseInt(popup_reward.value)};let res=await fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(x=>x.json());msg.innerText=res.msg;}
load();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
