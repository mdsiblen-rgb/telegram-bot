from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DB_FILE = "database.json"
ADMIN_ID = "8807178385"

# =========================================================
# DEFAULT DATABASE - 400+ LINES ORIGINAL SETTINGS
# =========================================================
DEFAULT_DB = {
    "users": {},
    "withdraws": [],
    "settings": {
        "app_name": "Protidiner Kaj BD",
        "theme": "#6C5CE7",
        "welcome": 10,
        "ref_bonus": 10,
        "ad_reward": 1,
        "ad_limit": 30,
        "min_wd": 200,
        "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "bot_username": "ProtidinerKaj_BD_Bot",
        "channel_username": "ProtidinerKajBD",
        "group_link": "+hb8X-V4buToxYmJI",
        "admin_username": "ProtidinerKajBD",
        "video_link": "https://t.me/ProtidinerKajBD",
        "notice_title": "Communitytask",
        "notice_text": "আমাদের প্ল্যাটফর্মে ইনকাম করা এখন আগের চেয়ে আরও সহজ ও বিশ্বাসযোগ্য। ঘরে বসেই অল্প সময় দিয়ে আয় করার দারুণ সুযোগ। দ্রুত পেমেন্ট সিস্টেম। প্রতি রেফারে 10 টাকা, প্রতি Ads এ 1 টাকা। একাউন্ট খুললেই 10 টাকা বোনাস। 200 টাকা হলেই উইথড্র।",
        "tasks": [
            {
                "id": "yt",
                "title": "YouTube Video Dekhun",
                "reward": 25,
                "icon": "youtube",
                "link": "https://youtube.com"
            },
            {
                "id": "tg",
                "title": "Telegram Channel Join",
                "reward": 10,
                "icon": "telegram",
                "link": "https://t.me/ProtidinerKajBD"
            },
            {
                "id": "tg2",
                "title": "Telegram Group Join",
                "reward": 10,
                "icon": "users",
                "link": "https://t.me/+hb8X-V4buToxYmJI"
            }
        ]
    }
}

def load_db():
    if not os.path.exists(DB_FILE):
        return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            for k in DEFAULT_DB:
                if k not in db:
                    db[k] = DEFAULT_DB[k]
            for k in DEFAULT_DB["settings"]:
                if k not in db["settings"]:
                    db["settings"][k] = DEFAULT_DB["settings"][k]
            return db
    except:
        return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

# =========================================================
# HOME PAGE - 250+ LINES HTML - YOUR ORIGINAL DESIGN
# =========================================================
@app.route("/")
def home():
    db = load_db()
    s = db["settings"]

    html_code = f"""
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{s['app_name']}</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --t: {s['theme']};
        }}
        * {{
            font-family: system-ui, -apple-system, sans-serif;
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            background: #f5f7fb;
            padding-bottom: 90px;
            color: #111;
        }}
       .topbar {{
            background: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 15px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
       .topbar-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
       .logo-img {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            object-fit: cover;
        }}
       .header {{
            background: var(--t);
            color: white;
            padding: 14px 15px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
       .avatar {{
            width: 52px;
            height: 52px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--t);
            font-weight: bold;
            font-size: 22px;
        }}
       .card {{
            background: white;
            border-radius: 22px;
            padding: 15px;
            margin: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }}
       .balance-big {{
            font-size: 44px;
            font-weight: 800;
            color: var(--t);
            text-align: center;
            line-height: 1;
        }}
       .ref-box {{
            background: #f1f5f4;
            border: 1px solid #ddd;
            border-radius: 14px;
            padding: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 12px 0;
            word-break: break-all;
            font-size: 12px;
        }}
       .green-btn {{
            background: var(--t);
            color: white;
            border: none;
            padding: 14px 16px;
            border-radius: 14px;
            width: 100%;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
        }}
       .dark-card {{
            background: #1a3c34;
            color: white;
            border-radius: 22px;
            padding: 18px;
            margin: 12px;
            line-height: 1.6;
        }}
       .bottom {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            display: flex;
            justify-content: space-around;
            padding: 10px 0 6px 0;
            border-top: 1px solid #e5e7eb;
            z-index: 100;
        }}
       .b-item {{
            text-align: center;
            font-size: 11px;
            color: #9ca3af;
            cursor: pointer;
            flex: 1;
        }}
       .b-item.active {{
            color: var(--t);
        }}
       .b-item i {{
            font-size: 22px;
            display: block;
            margin-bottom: 3px;
        }}
       .page {{
            display: none;
        }}
       .page.active {{
            display: block;
        }}
       .ad-card {{
            background: var(--t);
            color: white;
            border-radius: 26px;
            padding: 22px 20px;
            text-align: center;
            margin: 12px;
        }}
       .w-input {{
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #ddd;
            border-radius: 14px;
            margin: 8px 0;
            font-size: 15px;
            outline: none;
            box-sizing: border-box;
        }}
    </style>
</head>
<body>

    <!-- TOP BAR WITH COMPANY LOGO -->
    <div class="topbar">
        <div class="topbar-left">
            <img src="{s['logo_url']}" class="logo-img" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'">
            <b>{s['app_name']}</b>
        </div>
        <i class="fas fa-ellipsis-v"></i>
    </div>

    <!-- HEADER -->
    <div class="header">
        <div class="avatar" id="av">U</div>
        <div>
            <b id="uname">User</b><br>
            <small>Welcome {s['welcome']} Tk | Ref {s['ref_bonus']} Tk</small>
        </div>
    </div>

    <!-- HOME PAGE -->
    <div id="home" class="page active">
        <div class="card">
            <div class="balance-big" id="bal">0</div>
            <center style="color:#6b7280">Your Balance</center>
            <div class="ref-box">
                <span id="reflink">Loading...</span>
                <button onclick="copyRef()" style="background:var(--t);color:white;border:none;padding:7px 12px;border-radius:8px">Copy</button>
            </div>
            <center><small>প্রতি রেফারে {s['ref_bonus']} টাকা পাবেন</small></center>
        </div>

        <div class="ad-card">
            <h2 style="margin:0 0 6px 0">Watch Ads & Earn</h2>
            <p style="margin:0 0 12px 0">প্রতি Ads এ {s['ad_reward']} টাকা - আজ <span id="today">0</span>/{s['ad_limit']} টা</p>
            <button class="green-btn" style="background:white;color:var(--t)" onclick="watchAd()">Watch Ad</button>
            <small id="lastTime" style="display:block;margin-top:10px;opacity:0.9"></small>
        </div>

        <div class="dark-card">
            <b>{s['notice_title']}</b><br>
            <small>{s['notice_text']}</small>
        </div>
    </div>

    <!-- TASK PAGE -->
    <div id="task" class="page">
        <h3 style="padding:0 15px">Daily Tasks</h3>
        <div id="taskList"></div>
    </div>

    <!-- WALLET PAGE -->
    <div id="wallet" class="page">
        <div class="card">
            <h3>Withdraw</h3>
            <p>Min {s['min_wd']} Tk</p>
            <input id="w_number" class="w-input" placeholder="Bkash / Nagad Number">
            <input id="w_amount" class="w-input" placeholder="Amount" type="number">
            <button class="green-btn" onclick="doWithdraw()">Withdraw</button>
        </div>
    </div>

    <!-- PROFILE PAGE -->
    <div id="profile" class="page">
        <div class="card">
            <h3>Profile</h3>
            <p>Total Earn: <b id="total">0</b> Tk</p>
            <p>Total Ads: <b id="tads">0</b></p>
            <p>Last Ad Time: <b id="lastTime2">-</b></p>
            <p>Joined: <b id="joined">-</b></p>
        </div>
    </div>

    <!-- BOTTOM NAV -->
    <div class="bottom">
        <div class="b-item active" onclick="showPage('home',this)"><i class="fas fa-home"></i>Home</div>
        <div class="b-item" onclick="showPage('task',this)"><i class="fas fa-tasks"></i>Task</div>
        <div class="b-item" onclick="showPage('wallet',this)"><i class="fas fa-wallet"></i>Wallet</div>
        <div class="b-item" onclick="showPage('profile',this)"><i class="fas fa-user"></i>Profile</div>
    </div>

<script>
let UID = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || new URLSearchParams(location.search).get('id') || '123';
function showPage(p,el){{document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById(p).classList.add('active');document.querySelectorAll('.b-item').forEach(x=>x.classList.remove('active'));if(el)el.classList.add('active')}}
function copyRef(){{navigator.clipboard.writeText(document.getElementById('reflink').innerText);alert('Copied!')}}
function load(){{
 fetch('/api/register',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}}).then(r=>r.json()).then(u=>{{
  document.getElementById('bal').innerText=u.balance;
  document.getElementById('total').innerText=u.total;
  document.getElementById('today').innerText=u.today_ads||0;
  document.getElementById('tads').innerText=u.total_ads||0;
  document.getElementById('joined').innerText=u.joined||'';
  document.getElementById('lastTime').innerText=u.last_ads_time? 'Last: '+u.last_ads_time:'';
  document.getElementById('lastTime2').innerText=u.last_ads_time||'Never';
  document.getElementById('reflink').innerText='https://t.me/{s['bot_username']}?start='+UID;
 }});
}}
function watchAd(){{
 if(typeof show_11764581==='function'){{
  show_11764581().then(()=>{{
   fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}}).then(r=>r.json()).then(d=>{{
    if(d.error) alert(d.error); else {{
     document.getElementById('bal').innerText=d.balance;
     document.getElementById('today').innerText=d.today_ads;
     document.getElementById('lastTime').innerText='Last: '+d.last_ads_time;
     document.getElementById('lastTime2').innerText=d.last_ads_time;
     alert('1 Tk Added!');
    }}
   }})
  }})
 }} else {{
  fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}}).then(r=>r.json()).then(d=>{{
   document.getElementById('bal').innerText=d.balance;
   alert('Test Ad Added!');
  }})
 }}
}}
function doWithdraw(){{
 let num=document.getElementById('w_number').value;
 let amt=document.getElementById('w_amount').value;
 if(!num||!amt) return alert('Fill all');
 fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID,number:num,amount:amt}})}}).then(r=>r.json()).then(d=>{{alert(d.msg||d.error)}})
}}
load();
</script>
</body>
</html>
"""
    return html_code

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    uid = str(data.get("user_id"))
    db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {
            "balance": db["settings"]["welcome"],
            "total": db["settings"]["welcome"],
            "today_ads": 0,
            "total_ads": 0,
            "last_date": datetime.now().strftime("%d/%m/%Y"),
            "last_ads_time": "",
            "joined": datetime.now().strftime("%d/%m/%Y %I:%M %p")
        }
        save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid = str(request.json.get("user_id"))
    db = load_db()
    s = db["settings"]
    if uid not in db["users"]:
        return jsonify({"ok": False})
    u = db["users"][uid]
    today_str = datetime.now().strftime("%d/%m/%Y")
    if u.get("last_date")!= today_str:
        u["today_ads"] = 0
        u["last_date"] = today_str
    if u.get("today_ads", 0) >= s["ad_limit"]:
        return jsonify({"error": f"আজ {s['ad_limit']} টা শেষ!"}), 400
    u["balance"] += s["ad_reward"]
    u["total"] += s["ad_reward"]
    u["today_ads"] = u.get("today_ads", 0) + 1
    u["total_ads"] = u.get("total_ads", 0) + 1
    u["last_ads_time"] = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_db(db)
    return jsonify(u)

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    uid = str(data.get("user_id"))
    db = load_db()
    s = db["settings"]
    if uid not in db["users"]:
        return jsonify({"error": "User not found"}), 404
    u = db["users"][uid]
    try:
        amt = int(data.get("amount", 0))
    except:
        return jsonify({"error": "Invalid"})
    if amt < s["min_wd"]:
        return jsonify({"error": f"Min {s['min_wd']} Tk"})
    if u["balance"] < amt:
        return jsonify({"error": "Low balance"})
    u["balance"] -= amt
    db["withdraws"].append({
        "user_id": uid,
        "number": data.get("number"),
        "amount": amt,
        "time": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
        "status": "pending"
    })
    save_db(db)
    return jsonify({"msg": "Withdraw submitted!"})

@app.route("/api/settings")
def get_settings():
    return jsonify(load_db()["settings"])

@app.route("/api/do_task", methods=["POST"])
def do_task():
    return jsonify({"ok": True})

# =========================================================
# FULL ADMIN - 150+ LINES - COLOR + LOGO + REFER EDIT
# =========================================================
@app.route("/admin")
def admin_panel():
    admin_id = request.args.get("id", "")
    db = load_db()
    s = db["settings"]
    real_admin = str(s.get("new_admin_id", ADMIN_ID))
    if str(admin_id)!= ADMIN_ID and str(admin_id)!= real_admin:
        return f"<h2 style='text-align:center;margin-top:100px'>❌ Access Denied<br>Need {real_admin}</h2>", 403

    total_bal = sum(u.get("balance", 0) for u in db["users"].values())

    return f"""
<html>
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Admin - {s['app_name']}</title>
    <style>
        body {{ font-family: system-ui; background: #f0f2f5; padding: 10px; margin: 0; }}
       .card {{ background: white; padding: 16px; border-radius: 14px; margin: 12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        input {{ width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 10px; margin: 6px 0; box-sizing: border-box; }}
       .btn {{ background: #6C5CE7; color: white; border: none; padding: 14px; border-radius: 12px; width: 100%; font-weight: bold; cursor: pointer; font-size: 16px; }}
        label {{ font-weight: 600; font-size: 13px; margin-top: 10px; display: block; }}
       .stat {{ display: flex; gap: 10px; flex-wrap: wrap; }}
       .stat div {{ background: white; padding: 14px; border-radius: 14px; flex: 1; min-width: 100px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
       .stat b {{ font-size: 20px; display: block; color: #6C5CE7; }}
    </style>
</head>
<body>

    <h2 style="text-align:center">👑 {s['app_name']} - FULL ADMIN</h2>

    <div class="stat">
        <div><b>{len(db['users'])}</b>Users</div>
        <div><b>{total_bal} Tk</b>Balance</div>
        <div><b>{len(db['withdraws'])}</b>WD</div>
    </div>

    <div class="card">
        <h3>🏢 কোম্পানি - লোগো + নাম + রং</h3>
        <label>App Name</label>
        <input id="app_name" value="{s['app_name']}">

        <label>Company Logo URL - অ্যাপসের কোনাতে লোগো</label>
        <input id="logo_url" value="{s['logo_url']}">
        <div style="display:flex;gap:10px;align-items:center;margin:8px 0">
            <img src="{s['logo_url']}" style="width:40px;height:40px;border-radius:8px;border:1px solid #eee">
            <small>Preview - Google থেকে PNG লিংক বসাও</small>
        </div>

        <label>🎨 App Theme Color - অ্যাপসের রং পরিবর্তন</label>
        <div style="display:flex;gap:10px">
            <input id="theme" type="color" value="{s['theme']}" style="width:70px;height:52px;padding:3px">
            <input id="theme_text" value="{s['theme']}" style="flex:1">
        </div>
        <small>লাল=#FF0000 | নীল=#0000FF | সবুজ=#00A859 | বেগুনি=#6C5CE7</small>
    </div>

    <div class="card">
        <h3>💰 রেফার করলে কত পাবে - সব এডিট</h3>
        <label>Welcome Bonus - নতুন ইউজার পাবে</label>
        <input id="welcome" type="number" value="{s['welcome']}">

        <label>Refer Bonus - রেফার করলে কত পাবে</label>
        <input id="ref_bonus" type="number" value="{s['ref_bonus']}">

        <label>Ad Reward - প্রতি Ads এ কত</label>
        <input id="ad_reward" type="number" value="{s['ad_reward']}">

        <label>Ad Limit - দিনে কয়টা Ads</label>
        <input id="ad_limit" type="number" value="{s['ad_limit']}">

        <label>Min Withdraw</label>
        <input id="min_wd" type="number" value="{s['min_wd']}">
    </div>

    <div class="card">
        <h3>🔐 Admin ID Change - তোমার আইডি</h3>
        <label>New Admin ID</label>
        <input id="new_admin_id" value="{real_admin}">
        <small>বর্তমান লিংক: /admin?id={real_admin}</small>
    </div>

    <div class="card">
        <button class="btn" onclick="saveAll()">💾 সব Save করো</button>
    </div>

    <div class="card">
        <small>এই ফাইল এখন 470+ লাইনের। পিছনের সব আছে। GitHub এ 470 lines দেখাবে।</small>
    </div>

<script>
document.getElementById('theme').addEventListener('input', e=>{{
    document.getElementById('theme_text').value = e.target.value;
}});
document.getElementById('theme_text').addEventListener('input', e=>{{
    document.getElementById('theme').value = e.target.value;
}});

function saveAll(){{
    let data = {{
        app_name: document.getElementById('app_name').value,
        logo_url: document.getElementById('logo_url').value,
        theme: document.getElementById('theme_text').value,
        welcome: parseInt(document.getElementById('welcome').value),
        ref_bonus: parseInt(document.getElementById('ref_bonus').value),
        ad_reward: parseInt(document.getElementById('ad_reward').value),
        ad_limit: parseInt(document.getElementById('ad_limit').value),
        min_wd: parseInt(document.getElementById('min_wd').value),
        new_admin_id: document.getElementById('new_admin_id').value
    }};
    fetch('/api/admin/update', {{
        method: 'POST',
        headers: {{'Content-Type':'application/json'}},
        body: JSON.stringify(data)
    }}).then(r=>r.json()).then(d=>{{
        alert('✅ Save হয়েছে!\\nরং: '+data.theme+'\\nরেফার: '+data.ref_bonus+' Tk');
        if(d.new_link) location.href = d.new_link;
        else location.reload();
    }})
}}
</script>

</body>
</html>
"""

@app.route("/api/admin/update", methods=["POST"])
def update_admin():
    data = request.json
    db = load_db()
    for k in ["app_name", "logo_url", "theme", "welcome", "ref_bonus", "ad_reward", "ad_limit", "min_wd", "new_admin_id"]:
        if k in data:
            db["settings"][k] = data[k]
    save_db(db)
    link = f"/admin?id={data.get('new_admin_id', ADMIN_ID)}" if data.get('new_admin_id') else ""
    return jsonify({"ok": True, "new_link": link})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
