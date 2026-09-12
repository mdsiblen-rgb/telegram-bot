# FINAL COMPLETE A TO Z - BIG ADMIN 8807178385 - TOKEN 11764581 - ONE FILE ONLY - PASTE IN app.py
# MEDIUM 5 BTN 30px icon 15px font 88px height + PROFILE BIG ENGLISH 26px FIXED + 5 NUMBER PAGE CLEAN + ${t.btn} BUG FIXED + 17 COMPANY LINKS + UNLIMITED ADD + JOIN THEN MONEY + 24H TIMER + BIG ADMIN EDITABLE ALL
import os, json, time
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database.json'
BIG_ADMIN_ID = "8807178385"
TOKEN = "11764581"

def default_db():
    return {
        "users": {},
        "withdraws": [],
        "settings": {
            "app_name": f"Protidiner Kaj BD - FINAL - BIG ADMIN {BIG_ADMIN_ID}",
            "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "bkash_logo": "https://download.logo.wine/logo/BKash/bKash-Logo.wine.png",
            "nagad_logo": "https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png",
            "welcome_bonus": 60,
            "ad_reward": 2,
            "ad_limit": 100,
            "min_withdraw": 1000,
            "ref_bonus": 20,
            "task_cooldown_hours": 24,
            "official_title": f"Official Notes - {TOKEN} - BIG ADMIN {BIG_ADMIN_ID}",
            "official_desc": f"Daily Ads and Tasks - Token {TOKEN} - Big Admin {BIG_ADMIN_ID} - FINAL",
            "official_live": "LIVE",
            "home_ad_top_title": f"Special Offer - Mini Boy Ads - BIG ADMIN {BIG_ADMIN_ID} FINAL",
            "home_ad_btn": f"Watch ADS - Token {TOKEN} - Claim 2 Tk - FINAL",
            "support_title": f"Support Center - {BIG_ADMIN_ID} - BIG ADMIN",
            "support_desc": f"Contact us\nTelegram: @ProtidinerKajBD\nBig Admin ID: {BIG_ADMIN_ID}\nToken: {TOKEN}\nFINAL BIG ADMIN FILE - A TO Z",
            "support_tg": "https://t.me/ProtidinerKajBD",
            "support_channel": "https://t.me/ProtidinerKajBD",
            "support_rules": f"Rules: 100 Ads daily - Fake Ban - Big Admin {BIG_ADMIN_ID}",
            "ref_bottom_title": f"How Refer Works? - BIG ADMIN {BIG_ADMIN_ID}",
            "ref_bottom_desc": f"1. Share link\n2. Friend join\n3. Get 20 Tk\n4. Instant balance\nBig Admin: {BIG_ADMIN_ID}",
            "banner1": "https://img.freepik.com/free-vector/flat-design-referral-program-concept-landing-page_52683-25433.jpg",
            "banner2": "https://img.freepik.com/free-vector/make-money-online-concept-landing-page_23-2148538418.jpg",
            "banner3": "https://img.freepik.com/free-vector/earning-money-online-concept-landing-page_52683-25203.jpg",
            "wallet_bottom_title": "Withdraw Rules - Big Admin Can Change All - FINAL A TO Z",
            "wallet_bottom_desc": "1. Min 1000 Tk\n2. Correct bKash/Nagad Number\n3. Payment in 24h\n4. Wrong number your responsibility\n5. Multi account = Ban\nBig Admin Editable - FINAL",
            "wallet_rules": f"Fake Account = Ban - Big Admin {BIG_ADMIN_ID} - Token {TOKEN} - FINAL A TO Z"
        },
        "tasks": [
            {"title": "YouTube Subscribe - Company Link 1", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "Join & Get 25 Tk"},
            {"title": "Telegram Join - Company Link 2", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af", "btn": "Join & Get 10 Tk"},
            {"title": "Facebook Follow - Company Link 3", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "Join & Get 15 Tk"},
            {"title": "Website Visit - Company Link 4", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "Visit & Get 20 Tk"},
            {"title": "Group Join - Company Link 5", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "Join & Get 20 Tk"},
            {"title": "Post Like - Company Link 6", "reward": 20, "link": "https://t.me", "color": "#be123c", "btn": "Like & Get 20 Tk"},
            {"title": "Post Share - Company Link 7", "reward": 20, "link": "https://t.me", "color": "#065f46", "btn": "Share & Get 20 Tk"},
            {"title": "Comment Task - Company Link 8", "reward": 20, "link": "https://t.me", "color": "#2563eb", "btn": "Comment & Get 20 Tk"},
            {"title": "Refer 3 Friend - Company Link 9", "reward": 20, "link": "https://t.me", "color": "#d97706", "btn": "Refer & Get 20 Tk"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d = default_db()
        save_db(d)
        return d
    with open(DB_FILE,'r',encoding='utf-8') as f:
        try:
            d = json.load(f)
        except:
            d = default_db()
            save_db(d)
            return d
    dd = default_db()
    for k,v in dd["settings"].items():
        if k not in d["settings"]:
            d["settings"][k] = v
    if "tasks" not in d:
        d["tasks"] = dd["tasks"]
    return d

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f:
        json.dump(d,f,indent=2,ensure_ascii=False)

def get_user(db,uid):
    uid = str(uid)
    today = str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "balance": db["settings"]["welcome_bonus"],
            "ads_watched": 0,
            "ads_today": 0,
            "last_date": today,
            "claimed": [],
            "task_times": {},
            "ref_count": 0,
            "total_earn": db["settings"]["welcome_bonus"],
            "is_big_admin": uid == BIG_ADMIN_ID
        }
    u = db["users"][uid]
    if u.get("last_date")!= today:
        u["ads_today"] = 0
        u["last_date"] = today
    if "task_times" not in u: u["task_times"] = {}
    if "claimed" not in u: u["claimed"] = []
    if "total_earn" not in u: u["total_earn"] = u["balance"]
    u["is_big_admin"] = uid == BIG_ADMIN_ID
    return u

@app.route('/health')
def health():
    return f"OK - BIG ADMIN FINAL A TO Z - ID {BIG_ADMIN_ID} - TOKEN {TOKEN} - MEDIUM 5 BTN + PROFILE BIG ENGLISH FIXED - ALL SYSTEM INSIDE",200

@app.route('/')
def index():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin():
    if request.args.get('id')!= BIG_ADMIN_ID:
        return f"Need?id={BIG_ADMIN_ID} - BIG ADMIN ONLY - TOKEN {TOKEN}",403
    return render_template_string(ADMIN_HTML)

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id', BIG_ADMIN_ID)
    db = load_db()
    u = get_user(db, uid)
    save_db(db)
    return jsonify({
        "user": u,
        "settings": db["settings"],
        "tasks": db["tasks"],
        "withdraws": [w for w in db["withdraws"] if str(w["uid"]) == str(uid)],
        "recent_withdraws": db["withdraws"][-20:][::-1],
        "big_admin_id": BIG_ADMIN_ID,
        "token": TOKEN
    })

@app.route('/api/reward')
def reward():
    db = load_db()
    u = get_user(db, request.args.get('id'))
    u["balance"] += db["settings"]["ad_reward"]
    u["ads_watched"] += 1
    u["ads_today"] += 1
    u["total_earn"] += db["settings"]["ad_reward"]
    save_db(db)
    return jsonify({"msg": f"৳{db['settings']['ad_reward']} Added - BIG ADMIN {BIG_ADMIN_ID} - FINAL A TO Z"})

@app.route('/api/claim_task')
def claim_task():
    db = load_db()
    idx = int(request.args.get('idx'))
    uid = request.args.get('id')
    u = get_user(db, uid)
    now = time.time()
    last = float(u["task_times"].get(str(idx),0))
    cooldown = int(db["settings"].get("task_cooldown_hours",24)) * 3600
    if last!= 0 and (now - last) < cooldown:
        remain_h = int((cooldown - (now - last)) / 3600)
        remain_m = int(((cooldown - (now - last)) % 3600) / 60)
        return jsonify({"msg": f"⏰ Already Joined - {remain_h}h {remain_m}m পর আবার Join করতে পারবে - BIG ADMIN {BIG_ADMIN_ID} - TIMER {db['settings']['task_cooldown_hours']}h"})
    u["task_times"][str(idx)] = now
    if idx not in u["claimed"]:
        u["claimed"].append(idx)
    u["balance"] += db["tasks"][idx]["reward"]
    u["total_earn"] += db["tasks"][idx]["reward"]
    save_db(db)
    return jsonify({"msg": f"✅ Joined Success - ৳{db['tasks'][idx]['reward']} Added - Next {db['settings']['task_cooldown_hours']}h later - BIG ADMIN {BIG_ADMIN_ID}"})

@app.route('/api/withdraw')
def withdraw():
    db = load_db()
    uid = request.args.get('id')
    amt = int(request.args.get('amount',0))
    num = request.args.get('number')
    method = request.args.get('method','bKash')
    u = get_user(db, uid)
    if amt < db["settings"]["min_withdraw"]:
        return jsonify({"msg": f"Min {db['settings']['min_withdraw']} Tk - BIG ADMIN {BIG_ADMIN_ID}"})
    if u["balance"] < amt:
        return jsonify({"msg": "Low Balance - BIG ADMIN"})
    u["balance"] -= amt
    db["withdraws"].append({"uid": uid, "amount": amt, "number": num, "method": method, "time": str(datetime.now())[:19], "status": "Pending"})
    save_db(db)
    return jsonify({"msg": f"Withdraw Request Success - BIG ADMIN {BIG_ADMIN_ID} - TOKEN {TOKEN}"})

@app.route('/api/admin/full')
def a_full():
    return jsonify(load_db())

@app.route('/api/admin/save_settings',methods=['POST'])
def a_save():
    db = load_db()
    j = request.json
    for k,v in j.get("settings",{}).items():
        if k in db["settings"]:
            if k == "task_cooldown_hours":
                try: db["settings"][k] = int(v)
                except: db["settings"][k] = 24
            else:
                db["settings"][k] = v
    if "tasks" in j and isinstance(j["tasks"], list):
        db["tasks"] = j["tasks"]
    save_db(db)
    return jsonify({"msg": f"Saved - BIG ADMIN {BIG_ADMIN_ID} FINAL A TO Z - MEDIUM 5 BTN (30px icon,15px font,88px height) + PROFILE BIG ENGLISH 26px FIXED + 5 NUMBER PAGE CLEAN + ${{t.btn}} FIXED + 17 COMPANY LINKS + UNLIMITED ADD BUTTON SYSTEM + JOIN THEN MONEY + {db['settings']['task_cooldown_hours']}h TIMER - ALL INSIDE - TOKEN {TOKEN}"})

@app.route('/api/admin/approve')
def a_approve():
    db = load_db()
    idx = int(request.args.get('idx',0))
    if 0 <= idx < len(db["withdraws"]):
        db["withdraws"].pop(idx)
        save_db(db)
    return jsonify({"msg": f"Approved - BIG ADMIN {BIG_ADMIN_ID}"})

USER_HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>BIG ADMIN FINAL A TO Z - 8807178385</title><script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script><style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#0a1222;color:#fff;max-width:430px;margin:0 auto;padding-bottom:180px}.top{background:linear-gradient(135deg,#1e3a8a,#0f172a);padding:16px;border-radius:0 0 24px 24px;display:flex;justify-content:space-between;align-items:center}.bal{color:#22c55e;font-size:44px;font-weight:900}.card{background:#162032;margin:12px;border-radius:18px;padding:16px;border:1px solid #22314a}.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;font-size:15px;cursor:pointer}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f1b33;display:flex;border-top:2px solid #1e3a5f;padding:8px 0 14px 0;z-index:99;height:88px}.btm div{flex:1;text-align:center;color:#7a8aa8;font-size:15px;padding:10px 3px;border-radius:12px;font-weight:700;cursor:pointer}.btm div.on{color:#38bdf8;background:rgba(56,189,248,0.15);transform:scale(1.08)}.btm div span.icon{font-size:30px;display:block;margin-bottom:4px}.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #334155;background:#0f172a;color:#fff;margin-top:8px}.slider{position:relative;margin:12px;border-radius:18px;overflow:hidden;height:170px;border:1px solid #22314a;background:#000}.slides{display:flex;transition:transform 0.6s;width:300%}.slide{min-width:100%;height:170px}.slide img{width:100%;height:170px;object-fit:cover}.dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px}.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.4)}.dot.on{background:#38bdf8;width:20px;border-radius:10px}.mcard{flex:1;background:#0f172a;border:2px solid #334155;border-radius:14px;padding:12px;text-align:center;cursor:pointer}.mcard.sel{border-color:#e2136e;background:rgba(226,19,110,0.1)}.spacer{height:100px}.profile-header{background:linear-gradient(135deg,#1e3a8a,#0f172a);margin:12px;border-radius:20px;padding:26px;text-align:center;border:2px solid #2a3f63}.profile-avatar{width:95px;height:95px;border-radius:50%;background:#fff;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;font-size:48px;border:3px solid #38bdf8}.support-card{background:#162032;margin:12px;border-radius:18px;padding:18px;border:1px solid #22314a}</style></head><body><div class="top"><div><div>Protidiner Kaj BD - BIG ADMIN - 11764581 - A TO Z</div><div class="bal">৳ <span id="bal">60</span></div><div>Ads: <span id="ads">0</span>/100 | ID: 8807178385</div></div><img id="cLogo" src="" style="width:54px;height:54px;border-radius:50%;background:#fff;border:2px solid #38bdf8"></div><div id="p-home"><div class="card" style="background:linear-gradient(90deg,#1e40af,#0f766e);display:flex;justify-content:space-between;align-items:center"><div><b id="offTitle"></b><br><small id="offDesc"></small></div><div style="background:#22c55e;color:#000;padding:10px;border-radius:50%;width:54px;height:54px;display:flex;align-items:center;justify-content:center;font-weight:900" id="offLive">LIVE</div></div><div class="slider"><div class="slides" id="slides"><div class="slide"><img id="b1"></div><div class="slide"><img id="b2"></div><div class="slide"><img id="b3"></div></div><div class="dots"><div class="dot on" id="d0"></div><div class="dot" id="d1"></div><div class="dot" id="d2"></div></div></div><div class="card"><b id="adTopTitle"></b><br><button class="btn" style="background:linear-gradient(90deg,#0ea5e9,#0284c7);margin-top:10px;font-size:16px" onclick="watchAd()" id="adBtn"></button></div><div id="homeTasks"></div><div class="spacer"></div></div><div id="p-tasks" style="display:none"><div id="allTasks"></div><div class="spacer"></div></div><div id="p-refer" style="display:none"><div class="card"><b>Refer - 20 Tk - BIG ADMIN 8807178385</b><div class="inp" id="refLink"></div><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyRef()">Copy Link - BIG ADMIN</button></div><div class="card"><b id="refBottomTitle"></b><div id="refBottomDesc" style="white-space:pre-line;margin-top:8px"></div></div><div class="spacer"></div></div><div id="p-wallet" style="display:none"><div class="card"><b>Wallet - BIG ADMIN 8807178385 - A TO Z</b><div class="bal">৳ <span id="wBal">60</span></div>Min ৳<span id="minW">1000</span></div><div class="card"><input class="inp" id="wAmt" placeholder="Amount" type="number"><div style="display:flex;gap:10px;margin-top:12px"><div class="mcard sel" id="m-bkash" onclick="setM('bKash')"><img id="bkLogo" style="width:48px"><div style="margin-top:6px;font-weight:700">bKash</div></div><div class="mcard" id="m-nagad" onclick="setM('Nagad')"><img id="naLogo" style="width:48px"><div style="margin-top:6px;font-weight:700">Nagad</div></div></div><input class="inp" id="wNum" placeholder="Number"><button class="btn" style="background:linear-gradient(90deg,#2563eb,#1d4ed8);margin-top:12px" onclick="doWithdraw()">Withdraw - BIG ADMIN A TO Z</button></div><div id="wHistory"></div><div class="card" style="border:2px solid #22c55e"><b style="color:#22c55e">Live Withdraw - BIG ADMIN</b><div id="liveW" style="max-height:220px;overflow-y:auto;margin-top:10px"></div></div><div class="card" style="border:2px solid #38bdf8"><b id="walletBottomTitle"></b><div id="walletBottomDesc" style="white-space:pre-line;margin-top:8px"></div><div id="walletRules" style="background:#0a1222;padding:12px;border-radius:10px;margin-top:10px;border:1px dashed #334155"></div></div><div class="spacer"></div></div><div id="p-profile" style="display:none"><div class="profile-header"><div class="profile-avatar">👤</div><div style="font-size:26px;font-weight:900;color:#38bdf8;letter-spacing:0.5px;text-transform:uppercase;">PROFILE - 8807178385 - BIG ADMIN - ENGLISH BIG - FIXED</div><div style="font-size:16px;font-weight:700;color:#fff;margin-top:4px;">TOKEN: 11764581 - BIG ADMIN SYSTEM - A TO Z FINAL</div><div style="font-size:14px;margin-top:8px;color:#cbd5e1">USER ID: <span id="pId" style="color:#22c55e;font-weight:800"></span></div><div style="font-size:38px;font-weight:900;color:#22c55e;margin-top:10px">৳ <span id="pBal">0</span></div><div style="font-size:13px;opacity:.7;margin-top:2px">Total Balance - BIG ADMIN A TO Z</div><div style="margin-top:12px;display:flex;gap:8px;justify-content:center"><div style="background:rgba(56,189,248,0.15);padding:8px 14px;border-radius:20px;font-size:13px">Ads: <span id="pAds">0</span></div><div style="background:rgba(34,197,94,0.15);padding:8px 14px;border-radius:20px;font-size:13px">Earn: ৳<span id="pEarn">0</span></div></div></div><div class="support-card"><b id="supTitle" style="color:#38bdf8;font-size:17px">Support - BIG ADMIN</b><div id="supDesc" style="white-space:pre-line;font-size:14px;margin-top:8px"></div><div style="margin-top:16px;display:flex;gap:10px"><a id="tgLink" href="#" target="_blank" style="flex:1;background:#229ED9;color:#fff;padding:13px;border-radius:12px;text-align:center;text-decoration:none;font-weight:800">Telegram</a><a id="chLink" href="#" target="_blank" style="flex:1;background:#25D366;color:#fff;padding:13px;border-radius:12px;text-align:center;text-decoration:none;font-weight:800">Channel</a></div><div style="margin-top:12px;background:#0a1222;padding:10px;border-radius:10px;font-size:12px;opacity:.7" id="supRules"></div></div><div class="spacer"></div></div><div class="btm"><div class="on" id="b-home" onclick="go('home')"><span class="icon">🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span class="icon">✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span class="icon">👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span class="icon">💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span class="icon">👤</span>Profile</div></div><script>let uid=new URLSearchParams(location.search).get('id')||'8807178385';let method='bKash';let cur=0;function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{let el=document.getElementById('p-'+x);if(el)el.style.display=x==p?'block':'none';let b=document.getElementById('b-'+x);if(b)b.classList.toggle('on',x==p);});window.scrollTo(0,0);}function setM(m){method=m;document.getElementById('m-bkash').classList.toggle('sel',m=='bKash');document.getElementById('m-nagad').classList.toggle('sel',m=='Nagad');}function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('Copied - BIG ADMIN 8807178385');}function load(){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{document.getElementById('bal').innerText=d.user.balance;document.getElementById('wBal').innerText=d.user.balance;document.getElementById('pBal').innerText=d.user.balance;document.getElementById('pEarn').innerText=d.user.total_earn;document.getElementById('pAds').innerText=d.user.ads_watched;document.getElementById('ads').innerText=d.user.ads_watched;document.getElementById('pId').innerText=d.user.id;document.getElementById('cLogo').src=d.settings.company_logo;document.getElementById('bkLogo').src=d.settings.bkash_logo;document.getElementById('naLogo').src=d.settings.nagad_logo;document.getElementById('offTitle').innerText=d.settings.official_title;document.getElementById('offDesc').innerText=d.settings.official_desc;document.getElementById('offLive').innerText=d.settings.official_live;document.getElementById('adTopTitle').innerText=d.settings.home_ad_top_title;document.getElementById('adBtn').innerText=d.settings.home_ad_btn;document.getElementById('refLink').innerText=location.origin+'/?id='+d.user.id;document.getElementById('supTitle').innerText=d.settings.support_title;document.getElementById('supDesc').innerText=d.settings.support_desc;document.getElementById('supRules').innerText=d.settings.support_rules;document.getElementById('tgLink').href=d.settings.support_tg;document.getElementById('chLink').href=d.settings.support_channel;document.getElementById('refBottomTitle').innerText=d.settings.ref_bottom_title;document.getElementById('refBottomDesc').innerText=d.settings.ref_bottom_desc;document.getElementById('b1').src=d.settings.banner1;document.getElementById('b2').src=d.settings.banner2;document.getElementById('b3').src=d.settings.banner3;document.getElementById('walletBottomTitle').innerText=d.settings.wallet_bottom_title;document.getElementById('walletBottomDesc').innerText=d.settings.wallet_bottom_desc;document.getElementById('walletRules').innerText=d.settings.wallet_rules;document.getElementById('minW').innerText=d.settings.min_withdraw;let ht='';d.tasks.forEach((t,i)=>{let done=false;let tt=d.user.task_times?d.user.task_times[String(i)]:0;if(tt){let now=Date.now()/1000;let cool=d.settings.task_cooldown_hours*3600;if((now-tt)<cool)done=true;}ht+=`<div class="card"><div style="display:flex;justify-content:space-between"><div style="font-weight:700">⭐ ${t.title}</div><div style="color:#22c55e;font-weight:800">৳${t.reward}</div></div><div style="font-size:11px;opacity:.5;margin-top:4px">${t.link}</div><div style="display:flex;gap:8px;margin-top:10px"><button class="btn" style="background:${t.color};flex:1" ${done?'disabled':''} onclick="claim(${i})">${done?'⏰ Joined - Wait '+d.settings.task_cooldown_hours+'h':t.btn}</button><button class="btn" style="background:#334155;flex:1" onclick="window.open('${t.link}','_blank')">🔗 Visit</button></div></div>`;});document.getElementById('homeTasks').innerHTML=ht;document.getElementById('allTasks').innerHTML=ht;let live='';d.recent_withdraws.forEach(w=>{live+=`<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e293b;font-size:14px"><span>💰 ${w.method} ৳${w.amount}</span><span style="opacity:.6">${w.number.slice(0,4)}****</span></div>`;});document.getElementById('liveW').innerHTML=live||'No withdraw - BIG ADMIN A TO Z';});}function watchAd(){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load();});});}function claim(i){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{let t=d.tasks[i];window.open(t.link,'_blank');setTimeout(()=>{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});},3000);});}function doWithdraw(){let a=document.getElementById('wAmt').value;let n=document.getElementById('wNum').value;fetch(`/api/withdraw?id=${uid}&amount=${a}&number=${n}&method=${method}`).then(r=>r.json()).then(x=>{alert(x.msg);load();});}load();setInterval(()=>{cur=(cur+1)%3;let s=document.getElementById('slides');if(s)s.style.transform=`translateX(-${cur*100}%)`;document.querySelectorAll('.dot').forEach((d,i)=>{d.classList.toggle('on',i==cur)});},3000);</script></body></html>"""

ADMIN_HTML = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>BIG ADMIN FINAL A TO Z - 8807178385 - FULL FILE</title><style>body{background:#0f172a;color:#fff;padding:12px;font-family:sans-serif;max-width:650px;margin:0 auto}.card{background:#1e293b;padding:16px;border-radius:14px;margin:12px 0;border:1px solid #2a3f63}input,textarea{width:100%;padding:11px;border-radius:10px;border:1px solid #334155;background:#0f172a;color:#fff;margin:6px 0}button{padding:12px;border:none;border-radius:10px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}label{font-size:11px;opacity:.7;margin-top:8px;display:block;color:#38bdf8;font-weight:600}h3{color:#38bdf8;margin-bottom:10px;border-bottom:1px solid #334155;padding-bottom:8px}.task-box{background:#0f172a;padding:12px;border-radius:12px;margin:8px 0;border:1px solid #1e3a5f}</style></head><body><h2 style="color:#22c55e">🔧 BIG ADMIN A TO Z - 8807178385 - TOKEN 11764581 - COMPLETE FILE - SAME DESIGN</h2><div id="stats" class="card" style="background:linear-gradient(90deg,#1e40af,#0f172a)"></div><div class="card" style="border:2px solid #f59e0b"><h3>⏰ Timer - Big Admin - A TO Z</h3><label>Task Cooldown Hours - কত ঘন্টা পর আবার Join?</label><input id="task_cooldown_hours" type="number"><small>24=1দিন,12=12ঘন্টা,1=1ঘন্টা,0.5=30মিনিট - তুমি যা দেবে তাই হবে - BIG ADMIN</small></div><div class="card" style="border:2px solid #22c55e"><h3>💬 Support Links - Company - Big Admin</h3><label>Telegram Link</label><input id="support_tg"><label>Channel Link</label><input id="support_channel"><label>Title</label><input id="support_title"><label>Desc</label><textarea id="support_desc" rows="3"></textarea><label>Rules</label><textarea id="support_rules" rows="2"></textarea></div><div class="card" style="border:2px solid #38bdf8"><h3>📢 Banner 3 - Company Links - 17 Links Part</h3><label>Banner1</label><input id="banner1"><label>Banner2</label><input id="banner2"><label>Banner3</label><input id="banner3"></div><div class="card" style="border:2px solid #e2136e"><h3>🔗 Task Company Links - Unlimited Add - JOIN THEN MONEY - Big Admin - A TO Z</h3><div id="tasksEdit"></div><button style="background:#22c55e;width:100%;margin-top:12px;padding:18px;font-size:17px" onclick="addNewTask()">➕ Add New Button Link - যত খুশি তত - Unlimited</button><small style="opacity:.6">এখানে যত খুশি তত YouTube/Group/Channel Link Add করো - User Join করার পর টাকা পাবে - আগে না - BIG ADMIN</small></div><div class="card" style="border:2px solid #f59e0b"><h3>💳 Wallet Rules - Big Admin Editable</h3><label>Title</label><input id="wallet_bottom_title"><label>Desc</label><textarea id="wallet_bottom_desc" rows="3"></textarea><label>Rules</label><textarea id="wallet_rules" rows="2"></textarea></div><div class="card"><h3>Logos + Official - BIG ADMIN A TO Z</h3><label>Company Logo</label><input id="company_logo"><label>bKash Logo</label><input id="bkash_logo"><label>Nagad Logo</label><input id="nagad_logo"><label>Official Title</label><input id="official_title"><label>Official Desc</label><input id="official_desc"><label>Home Ad Title</label><input id="home_ad_top_title"><label>Ad Button</label><input id="home_ad_btn"><label>Ref Title</label><input id="ref_bottom_title"><label>Ref Desc</label><textarea id="ref_bottom_desc" rows="2"></textarea></div><div class="card" style="background:linear-gradient(90deg,#22c55e,#16a34a)"><button style="background:#fff;color:#16a34a;width:100%;padding:20px;font-size:18px;font-weight:900" onclick="saveAll()">💾 SAVE ALL - BIG ADMIN 8807178385 - FINAL A TO Z - SAME DESIGN</button></div><div class="card"><h3>Withdraw Requests - BIG ADMIN CONTROL</h3><div id="wds"></div></div><script>let DB={};function load(){fetch('/api/admin/full?id=8807178385').then(r=>r.json()).then(d=>{DB=d;for(let k in d.settings){let el=document.getElementById(k);if(el)el.value=d.settings[k];}let h='';d.tasks.forEach((t,i)=>{h+=`<div class="task-box"><b style="color:#38bdf8">Task ${i+1} - ${t.title} - BIG ADMIN</b> <button style="background:#dc2626;float:right;padding:6px 12px" onclick="delTask(${i})">❌ Delete</button><label>Title - Company Link Name</label><input id="task_title_${i}" value="${t.title}"><label>Company Link URL - Join Then Money System</label><input id="task_link_${i}" value="${t.link}" style="border:2px solid #22c55e"><label>Reward Tk</label><input id="task_reward_${i}" type="number" value="${t.reward}"><label>Color Code</label><input id="task_color_${i}" value="${t.color}"><label>Button Text - ex: Join & Get 20 Tk</label><input id="task_btn_${i}" value="${t.btn}"></div>`;});document.getElementById('tasksEdit').innerHTML=h;document.getElementById('stats').innerHTML=`BIG ADMIN ID: 8807178385 | TOKEN: 11764581 | Users: ${Object.keys(d.users).length} | Withdraws: ${d.withdraws.length} | Tasks: ${d.tasks.length} | MEDIUM 5 BTN: 30px icon, 15px font, 88px height | PROFILE: BIG ENGLISH 26px FIXED CLEAN | ${'${t.btn}'} BUG FIXED | 17 COMPANY LINKS: 3 Logo + 3 Banner + 2 Support + ${d.tasks.length} Task | JOIN THEN MONEY | TIMER: ${d.settings.task_cooldown_hours}h | A TO Z COMPLETE | SAME DESIGN`;document.getElementById('wds').innerHTML=d.withdraws.map((w,i)=>`<div style="border:1px solid #334155;padding:8px;margin:4px;border-radius:8px;display:flex;justify-content:space-between"><span>💰 ${w.method} ৳${w.amount} | ${w.number} | ${w.uid}</span><button onclick="approve(${i})" style="background:#22c55e;padding:6px 12px">Approve</button></div>`).join('')||'No withdraw';});}function addNewTask(){DB.tasks.push({title:"New Company Link "+(DB.tasks.length+1),link:"https://t.me/YourNewGroup",reward:20,color:"#2563eb",btn:"Join & Get 20 Tk"});renderTasks();}function delTask(i){if(confirm("Delete Task "+(i+1)+" - "+DB.tasks[i].title+"?")){DB.tasks.splice(i,1);renderTasks();}}function renderTasks(){let h='';DB.tasks.forEach((t,i)=>{h+=`<div class="task-box"><b style="color:#38bdf8">Task ${i+1} - BIG ADMIN</b> <button style="background:#dc2626;float:right;padding:6px 12px" onclick="delTask(${i})">❌ Delete</button><label>Title</label><input id="task_title_${i}" value="${t.title}"><label>Company Link URL</label><input id="task_link_${i}" value="${t.link}" style="border:2px solid #22c55e"><label>Reward</label><input id="task_reward_${i}" type="number" value="${t.reward}"><label>Color</label><input id="task_color_${i}" value="${t.color}"><label>Button Text</label><input id="task_btn_${i}" value="${t.btn}"></div>`;});document.getElementById('tasksEdit').innerHTML=h;}function saveAll(){let s={};['company_logo','bkash_logo','nagad_logo','banner1','banner2','banner3','wallet_bottom_title','wallet_bottom_desc','wallet_rules','official_title','official_desc','home_ad_top_title','home_ad_btn','support_title','support_desc','support_tg','support_channel','support_rules','ref_bottom_title','ref_bottom_desc','task_cooldown_hours'].forEach(k=>{let el=document.getElementById(k);if(el)s[k]=el.value;});let tasks=[];for(let i=0;i<DB.tasks.length;i++){let te=document.getElementById('task_title_'+i);if(!te) continue;tasks.push({title:te.value,link:document.getElementById('task_link_'+i).value,reward:parseInt(document.getElementById('task_reward_'+i).value)||20,color:document.getElementById('task_color_'+i).value,btn:document.getElementById('task_btn_'+i).value});}fetch('/api/admin/save_settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:s,tasks:tasks})}).then(r=>r.json()).then(x=>{alert(x.msg);load();});}function approve(i){fetch('/api/admin/approve?idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load();});}load();</script></body></html>"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
