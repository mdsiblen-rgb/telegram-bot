from flask import Flask, request, jsonify
import json, os, time
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"
ADMIN_ID = "8807178385"

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
        "bot_username": "ProtidinerKaj_BD_Bot",
        "channel_username": "ProtidinerKajBD",
        "group_link": "+hb8X-V4buToxYmJI",
        "admin_username": "ProtidinerKajBD",
        "video_link": "https://t.me/ProtidinerKajBD",
        "notice_title": "Communitytask",
        "notice_text": "✨ আমাদের প্ল্যাটফর্মে ইনকাম করা এখন আগের চেয়ে আরও সহজ ও বিশ্বাসযোগ্য।\n🚀 ঘরে বসেই অল্প সময় দিয়ে আয় করার দারুণ সুযোগ।\n👉 দ্রুত পেমেন্ট সিস্টেম।\n🌟 নতুনদের জন্য সহজ এবং সবার জন্য লাভজনক একটি প্ল্যাটফর্ম।\n💸 প্রতিটি রেফারে পাবেন 10 টাকা।\n📺 প্রতিটি বিজ্ঞাপন দেখলে পাবেন 1 টাকা।\n🎁 একাউন্ট খুললেই সাথে সাথে 10 টাকা বোনাস।\n🏦 200 টাকা হলেই উইথড্র করতে পারবেন বিকাশ ও নগদের মাধ্যমে।( সম্পূর্ণ অটোমেশন সিস্টেম)",
        "tasks": [
            {"id": "yt", "title": "YouTube video", "reward": 25, "icon": "youtube", "link": "https://youtube.com"},
            {"id": "tg", "title": "Join telegram", "reward": 10, "icon": "telegram", "link": "https://t.me/ProtidinerKajBD"}
        ]
    }
}

def load_db():
    if not os.path.exists(DB_FILE):
        return json.loads(json.dumps(DEFAULT_DB))
    try:
        with open(DB_FILE,"r",encoding="utf-8") as f:
            db=json.load(f)
            for k in DEFAULT_DB:
                if k not in db:
                    db[k]=DEFAULT_DB[k]
            for k in DEFAULT_DB["settings"]:
                if k not in db["settings"]:
                    db["settings"][k]=DEFAULT_DB["settings"][k]
            return db
    except:
        return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    db=load_db(); s=db["settings"]
    return f"""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['app_name']}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<!-- ✅ YOUR MONETAG COMPANY CODE - ZONE 11764581 CONNECTED -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
:root{{--t:{s['theme']}}};
*{{font-family:system-ui}}
body{{margin:0;background:#f5f7fb;padding-bottom:85px}}
.topbar{{background:#b8f0e8;display:flex;align-items:center;justify-content:space-between;padding:12px 15px;position:sticky;top:0;z-index:100}}
.header{{background:var(--t);color:white;padding:14px 15px;display:flex;align-items:center;gap:12px}}
.avatar{{width:52px;height:52px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--t);font-weight:bold;font-size:22px}}
.card{{background:white;border-radius:22px;padding:15px;margin:12px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}}
.balance-big{{font-size:42px;font-weight:800;color:var(--t);text-align:center}}
.ref-box{{background:#f1f5f4;border:1px solid #ddd;border-radius:14px;padding:12px;display:flex;justify-content:space-between;align-items:center;margin:10px 0;word-break:break-all}}
.green-btn{{background:var(--t);color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:bold;font-size:16px;cursor:pointer}}
.dark-card{{background:#1a3c34;color:white;border-radius:22px;padding:18px;margin:12px}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #e5e7eb;z-index:100}}
.b-item{{text-align:center;font-size:11px;color:#9ca3af;cursor:pointer;flex:1}}.b-item.active{{color:var(--t)}}.b-item i{{font-size:22px;display:block;margin-bottom:2px}}
.page{{display:none}}.page.active{{display:block}}
.ad-card{{background:var(--t);color:white;border-radius:26px;padding:20px;text-align:center;margin:12px}}
.task-row{{display:flex;justify-content:space-between;align-items:center;padding:14px;background:white;border-radius:18px;margin:10px 12px}}
.method{{border:2px solid #e5e7eb;border-radius:16px;padding:12px;text-align:center;flex:1;cursor:pointer}}.method.sel{{border-color:var(--t);background:#f0efff}}
.w-input{{width:92%;padding:14px;border:1px solid #ddd;border-radius:14px;margin:6px 0}}
.support-row{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:white;border-radius:18px;margin:10px 12px;cursor:pointer}}
#topMenu{{position:absolute;top:50px;right:10px;background:white;border-radius:14px;box-shadow:0 8px 25px rgba(0,0,0,0.15);padding:8px 0;width:180px;display:none;z-index:200}}
#topMenu div{{padding:12px 16px;font-size:13px;cursor:pointer}}
</style>
</head>
<body>
<div class="topbar"><b>{s['app_name']}</b><i class="fas fa-ellipsis-v" onclick="document.getElementById('topMenu').style.display='block'"></i></div>
<div id="topMenu"><div>Profile</div><div>Support</div></div>
<div class="header"><div class="avatar">U</div><div><b id="uname">User</b><br><small>Welcome Bonus {s['welcome']} Tk</small></div></div>
<div class="card"><div class="balance-big" id="bal">0</div><center>Your Balance</center></div>
<div class="ad-card"><h2>Watch Ads & Earn</h2><p>প্রতিটি Ads এ {s['ad_reward']} টাকা</p><button class="green-btn" style="background:white;color:var(--t)" onclick="watchAd()">Watch Ad</button></div>
<div class="bottom"><div class="b-item active"><i class="fas fa-home"></i>Home</div><div class="b-item"><i class="fas fa-tasks"></i>Task</div><div class="b-item"><i class="fas fa-wallet"></i>Wallet</div><div class="b-item"><i class="fas fa-user"></i>Profile</div></div>
<script>
function watchAd(){{
  if(typeof show_11764581 === 'function'){{
    show_11764581().then(()=>{{ fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:window.Telegram.WebApp.initDataUnsafe?.user?.id || '123'}})}}).then(r=>r.json()).then(d=>{{document.getElementById('bal').innerText=d.balance; alert('1 Tk Added! Last Time: '+d.last_ads_time)}}) }})
  }} else {{ alert('Ad not ready') }}
}}
</script>
</body></html>"""

@app.route("/api/register", methods=["POST"])
def register():
    data=request.json; uid=str(data.get("user_id")); db=load_db()
    if uid not in db["users"]:
        db["users"][uid]={
            "balance": db["settings"]["welcome"],
            "total": db["settings"]["welcome"],
            "today_ads": 0,
            "total_ads": 0,
            "last_date": datetime.now().strftime("%d/%m/%Y"),
            "last_ads_time": "", # ✅ যোগ করা হলো
            "joined": datetime.now().strftime("%d/%m/%Y %I:%M %p")
        }
        save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/do_task", methods=["POST"])
def do_task():
    uid=str(request.json.get("user_id")); tid=request.json.get("task_id"); db=load_db()
    if uid not in db["users"]: return jsonify({"ok":False}),404
    task=next((t for t in db["settings"]["tasks"] if t["id"]==tid), None)
    if not task: return jsonify({"ok":False}),404
    db["users"][uid]["balance"]+=task["reward"]; db["users"][uid]["total"]+=task["reward"]; save_db(db)
    return jsonify({"ok":True,"link":task.get("link")})

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid=str(request.json.get("user_id")); db=load_db(); s=db["settings"]
    if uid not in db["users"]: return jsonify({"ok":False})
    u=db["users"][uid]
    if u.get("last_date")!=datetime.now().strftime("%d/%m/%Y"):
        u["today_ads"]=0; u["last_date"]=datetime.now().strftime("%d/%m/%Y")
    if u.get("today_ads",0)>=s["ad_limit"]:
        return jsonify({"error":f"আজ {s['ad_limit']} টা শেষ!"}),400
    # ✅ এখানেই টাইম যোগ করা হলো - তোমার মেইন চাওয়া
    u["balance"]+=s["ad_reward"]; u["total"]+=s["ad_reward"]; u["today_ads"]=u.get("today_ads",0)+1; u["total_ads"]=u.get("total_ads",0)+1
    u["last_ads_time"]=datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_db(db)
    return jsonify(u)

@app.route("/api/settings")
def get_settings():
    return jsonify(load_db()["settings"])

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
