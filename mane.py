import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

def load_db():
    if not os.path.exists(DB):
        d = {
            "users": {},
            "withdraws": [],
            "settings": {
                "app_name": "Protidiner Kaj BD",
                "admin_name": "SHIBLI NOMAN",
                "app_logo": "👑",
                "top_banner_img": "",
                "slider1": "🎉 Daily Bonus Available Today",
                "slider2": "📢 Company Sponsored - 100% Safe",
                "slider3": "🎁 50 Ads দেখলে ৳100 বোনাস!",
                "slider4": "💰 100% Payment Guaranteed",
                "slider5": "🔥 প্রতিদিন কাজ করুন",
                "company_reward": 2,
                "popup_reward": 3,
                "company_limit": 30,
                "popup_limit": 20,
                "balance_target": 2000,
                "min_withdraw": 500,
                "bkash_logo": "৳",
                "nagad_logo": "৳",
                "tele_link": "https://t.me/",
                "yt_link": "https://youtube.com/",
                "fb_link": "https://facebook.com/"
            }
        }
        with open(DB, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        return d
    with open(DB, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def get_user(db, uid):
    uid = str(uid)
    today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "name": "User " + uid[-4:],
            "balance": 1122,
            "company": 1,
            "popup": 0,
            "total": 1,
            "tasks": [],
            "img": "",
            "join": "2026-09-13",
            "last": today
        }
    return db["users"][uid]

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/admin')
def admin():
    if request.args.get('id')!= '8807178385':
        return "Use /admin?id=8807178385", 403
    return render_template_string(ADMIN)

@app.route('/api/get')
def api_get():
    db = load_db()
    u = get_user(db, request.args.get('id','8807178385'))
    save_db(db)
    uw = [w for w in db["withdraws"] if w["uid"] == u["id"]]
    return jsonify({"user": u, "settings": db["settings"], "withdraws": uw})

@app.route('/api/admin/get')
def admin_get(): return jsonify(load_db())

@app.route('/api/admin/save', methods=['POST'])
def admin_save():
    db = load_db()
    j = request.json
    db["settings"].update(j.get('settings', j))
    save_db(db)
    return jsonify({"msg": "✅ Save হয়েছে"})

@app.route('/api/admin/balance', methods=['POST'])
def admin_bal():
    db = load_db()
    j = request.json
    uid = str(j.get('uid'))
    amt = int(j.get('amt',0))
    if uid in db["users"]:
        db["users"][uid]["balance"] += amt
        save_db(db)
        return jsonify({"msg": f"✅ {amt} যোগ/বিয়োগ হয়েছে"})
    return jsonify({"msg": "User নাই"})

@app.route('/api/reward')
def reward():
    db = load_db()
    u = get_user(db, request.args.get('id'))
    t = request.args.get('type')
    if t == 'company':
        if u["company"] >= db["settings"]["company_limit"]:
            return jsonify({"msg": "Limit"})
        u["company"] += 1
        u["balance"] += int(db["settings"]["company_reward"])
    else:
        if u["popup"] >= db["settings"]["popup_limit"]:
            return jsonify({"msg": "Limit"})
        u["popup"] += 1
        u["balance"] += int(db["settings"]["popup_reward"])
    u["total"] = u["company"]+u["popup"]
    save_db(db)
    return jsonify({"msg": "ok"})

@app.route('/api/withdraw', methods=['POST'])
def wd():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    amt = int(j.get('amt',0))
    if amt < int(db["settings"]["min_withdraw"]):
        return jsonify({"msg": f"❌ মিনিমাম ৳{db['settings']['min_withdraw']}"})
    if u["balance"] < amt:
        return jsonify({"msg": "❌ ব্যালেন্স কম"})
    u["balance"] -= amt
    db["withdraws"].append({"uid": u["id"], "amt": amt, "num": j.get('num'), "method": j.get('method'), "status": "Pending", "time": str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg": "✅ Withdraw পাঠানো হয়েছে"})

@app.route('/api/task/done', methods=['POST'])
def td():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    tid = str(j.get('tid'))
    if tid not in u["tasks"]:
        u["tasks"].append(tid)
        u["balance"] += int(j.get('amt',20))
    save_db(db)
    return jsonify({"msg": "✅ Bonus"})

@app.route('/api/profile/save', methods=['POST'])
def ps():
    db = load_db()
    j = request.json
    u = get_user(db, j.get('id'))
    u["name"] = j.get('name', u["name"])
    if j.get('img'): u["img"] = j.get('img')
    save_db(db)
    return jsonify({"msg": "✅ Save"})

ADMIN = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>
body{background:#070710;color:#fff;max-width:900px;margin:0 auto;padding:12px;font-family:system-ui}
.card{background:#15152a;border-radius:16px;padding:16px;margin:14px 0;border:1px solid #222}
input{width:100%;padding:12px;border-radius:10px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:6px}
label{font-size:11px;color:#aaa;margin-top:10px;display:block}
.btn{width:100%;padding:14px;background:#6d4cff;border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:14px;cursor:pointer}
</style></head><body>
<h2 style="text-align:center">👑 Full Admin Control</h2>
<div class="card">
<h3>🎨 A to Z Control</h3>
<label>App Name</label><input id="app_name">
<label>Admin Name</label><input id="admin_name">
<label>App Logo (Emoji/Img URL)</label><input id="app_logo">
<label>Top Banner Image URL (খালি রাখলে Gradient)</label><input id="top_banner_img">
<label>Slider 1</label><input id="slider1">
<label>Slider 2</label><input id="slider2">
<label>Slider 3</label><input id="slider3">
<label>Slider 4</label><input id="slider4">
<label>Slider 5</label><input id="slider5">
<label>Company Ads Reward ৳</label><input id="company_reward" type="number">
<label>Popup Ads Reward ৳</label><input id="popup_reward" type="number">
<label>Company Limit</label><input id="company_limit" type="number">
<label>Popup Limit</label><input id="popup_limit" type="number">
<label>Balance Target (লাল বার 100% কত টাকায় ভরবে)</label><input id="balance_target" type="number">
<label>Min Withdraw</label><input id="min_withdraw" type="number">
<label>bKash Logo (Emoji/URL)</label><input id="bkash_logo">
<label>Nagad Logo (Emoji/URL)</label><input id="nagad_logo">
<label>Telegram Link</label><input id="tele_link">
<label>YouTube Link</label><input id="yt_link">
<label>Facebook Link</label><input id="fb_link">
<button class="btn" onclick="saveAll()">💾 SAVE EVERYTHING</button>
</div>
<div class="card"><h3>💰 টাকা বাড়ানো/কমানো</h3><label>User ID</label><input id="uid"><label>Amount ( +100 বা -50 )</label><input id="amt" type="number"><button class="btn" onclick="addBal()">Update Balance</button></div>
<div id="msg" style="text-align:center;color:#22c55e"></div>
<script>
function load(){fetch('/api/admin/get').then(r=>r.json()).then(d=>{for(let k in d.settings){let el=document.getElementById(k);if(el)el.value=d.settings[k];}});}
function saveAll(){let s={};document.querySelectorAll('input').forEach(e=>{if(e.id!='uid'&&e.id!='amt')s[e.id]=e.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:s})}).then(r=>r.json()).then(d=>{document.getElementById('msg').innerText=d.msg;alert('✅ সব Save হয়েছে');});}
function addBal(){fetch('/api/admin/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uid:document.getElementById('uid').value,amt:document.getElementById('amt').value})}).then(r=>r.json()).then(d=>alert(d.msg));}
load();
</script></body></html>
"""

HTML = """<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#000;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.header{background:#0a0a18;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bottomNav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;justify-content:space-around;padding:10px 0 14px;border-radius:24px 24px 0 0;z-index:99;border-top:1px solid #1e1e3a}
.navItem{text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.navItem.active{color:#fff}.navItem span{font-size:24px;display:block}
.page{display:none}.page.active{display:block}

/* ===== FIXED GAP - NO BIG SPACE ===== */
.sliderWrap{margin:8px 12px 0 12px;position:relative}
.slider{height:110px;border-radius:24px;display:flex;align-items:center;justify-content:center;font-weight:800;background:linear-gradient(90deg,#ff9a00,#ff3d00);overflow:hidden;position:relative}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;transition:.8s;padding:10px;text-align:center;font-size:18px}.slide.active{opacity:1}
.dotWrap{display:flex;gap:6px;justify-content:center;margin:6px 0 0 0}.dot{width:6px;height:6px;background:#fff4;border-radius:50%}.dot.active{background:#fff;width:20px}

/* BALANCE CARD WITH RED LONG BAR */
.balanceCard{background:linear-gradient(135deg,#2a5bff,#00d1b2);border-radius:24px;padding:16px 16px 12px 16px;text-align:center;margin:8px 12px 10px 12px}
.progressBg{width:100%;height:10px;background:#00000030;border-radius:20px;margin-top:12px;overflow:hidden;border:1px solid #ffffff20}
.progressFill{height:100%;background:linear-gradient(90deg,#ff0000,#ff4444);border-radius:20px;transition:1s;width:0%}

.btn{width:100%;padding:16px;border:none;border-radius:16px;font-weight:800;color:#fff;margin:6px 0;cursor:pointer}
.btn-purple{background:#6d28d9}.btn-green{background:#16a34a}
</style></head><body>
<div class="header"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px" id="logoShow">👑</div><div><div style="font-weight:900"><span id="appNameShow">Protidiner Kaj BD</span> <span style="background:#22c55e;padding:2px 6px;border-radius:50%;font-size:10px">✓</span></div><div style="font-size:11px;color:#9ca3af">Admin: <span id="adminNameShow">SHIBLI NOMAN</span></div></div></div><div style="width:42px;height:42px;border-radius:50%;background:#1e1e3a;border:2px solid #6d4cff;display:flex;align-items:center;justify-content:center;overflow:hidden" onclick="goP('profile')"><img id="topProfileImg" style="width:100%;height:100%;object-fit:cover;display:none"><span id="topProfileIcon">👤</span></div></div>

<div id="p-home" class="page active">
<!-- TOP BANNER - NO GAP -->
<div class="sliderWrap"><div class="slider" id="sliderBg"><div id="s1" class="slide active"><span id="st1">Bonus</span></div><div id="s2" class="slide"><span id="st2">Company 100% Safe</span></div><div id="s3" class="slide"><span id="st3">Bonus</span></div><div id="s4" class="slide"><span id="st4">Payment</span></div><div id="s5" class="slide"><span id="st5">কাজ</span></div></div><div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div></div>

<!-- BALANCE WITH RED BAR - EXACT AS YOUR MARK -->
<div class="balanceCard">
<div style="font-size:13px">💰 <span id="balTitle">আপনার বর্তমান ব্যালেন্স</span></div>
<div style="font-size:54px;font-weight:900" id="balHome">৳1122</div>
<div style="display:flex;gap:6px;justify-content:center;margin-top:8px"><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bC">Company 1/30</span><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bP">Popup 0/20</span><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bT">Total 1</span></div>
<!-- লাল লম্বা বার যেটা টাকা ভরাট হয় -->
<div class="progressBg"><div id="progBar" class="progressFill"></div></div>
</div>

<div style="background:#15151f;border-radius:24px;padding:12px;margin:0 12px 12px 12px"><button class="btn btn-purple" onclick="doR('company')">📺 COMPANY ADS (৳<span id="cr">2</span>) - <span id="btnC">1/30</span></button><button class="btn btn-green" onclick="doR('popup')">💰 POPUP ADS (৳<span id="pr">3</span>) - <span id="btnP">0/20</span></button></div>
</div>

<div id="p-tasks" class="page"></div><div id="p-wallet" class="page"></div><div id="p-support" class="page"></div><div id="p-profile" class="page"></div>

<div class="bottomNav"><div class="navItem active" id="n-home" onclick="goP('home')"><span>🏠</span>Home</div><div class="navItem" id="n-tasks" onclick="goP('tasks')"><span>📋</span>Task</div><div class="navItem" id="n-wallet" onclick="goP('wallet')"><span>💰</span>Wallet</div><div class="navItem" id="n-support" onclick="goP('support')"><span>💬</span>Support</div><div class="navItem" id="n-profile" onclick="goP('profile')"><span>👤</span>Profile</div></div>

<script>
let uid='8807178385',cur=0;
function goP(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.navItem').forEach(e=>e.classList.remove('active'));document.getElementById('n-'+p).classList.add('active');}
function init(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{
 let u=d.user; let s=d.settings;
 document.getElementById('appNameShow').innerText=s.app_name;
 document.getElementById('adminNameShow').innerText=s.admin_name;
 document.getElementById('logoShow').innerText=s.app_logo;
 for(let i=1;i<=5;i++){document.getElementById('st'+i).innerText=s['slider'+i]||'';}
 document.getElementById('cr').innerText=s.company_reward;
 document.getElementById('pr').innerText=s.popup_reward;
 document.getElementById('balHome').innerText='৳'+u.balance;
 document.getElementById('bC').innerText='Company '+u.company+'/'+s.company_limit;
 document.getElementById('bP').innerText='Popup '+u.popup+'/'+s.popup_limit;
 document.getElementById('bT').innerText='Total '+u.total;
 document.getElementById('btnC').innerText=u.company+'/'+s.company_limit;
 document.getElementById('btnP').innerText=u.popup+'/'+s.popup_limit;
 // লাল বার ভরাট - ব্যালেন্স অনুযায়ী
 let target = parseInt(s.balance_target)||2000;
 let pct = Math.min(100, Math.round((u.balance/target)*100));
 document.getElementById('progBar').style.width = pct+'%';
 if(u.img){document.getElementById('topProfileImg').src=u.img;document.getElementById('topProfileImg').style.display='block';document.getElementById('topProfileIcon').style.display='none';}
 if(s.top_banner_img){document.getElementById('sliderBg').style.background='url('+s.top_banner_img+') center/cover';}
});}
function doR(t){fetch('/api/reward?id='+uid+'&type='+t).then(()=>{init();if(typeof show_11764581==='function')show_11764581();});}
setInterval(()=>{cur=(cur+1)%5;for(let i=1;i<=5;i++){let el=document.getElementById('s'+i);let d=document.getElementById('d'+i);if(el)el.classList.toggle('active',i-1==cur);if(d)d.classList.toggle('active',i-1==cur);}},2500);
init();
</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
