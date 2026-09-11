from flask import Flask, request, jsonify
import json, os, time
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"
ADMIN_ID = "8807178385"

# ==================== YOUR ORIGINAL DATABASE - 300+ LINES FILE ====================
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
            {"id": "yt", "title": "YouTube Video Dekhun", "reward": 25, "icon": "youtube", "link": "https://youtube.com/@protidinerkaj"},
            {"id": "tg", "title": "Telegram Channel Join", "reward": 10, "icon": "telegram", "link": "https://t.me/ProtidinerKajBD"},
            {"id": "tg2", "title": "Telegram Group Join", "reward": 10, "icon": "users", "link": "https://t.me/+hb8X-V4buToxYmJI"}
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
    except Exception as e:
        print("DB Error", e)
        return json.loads(json.dumps(DEFAULT_DB))

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False,indent=2)

# ==================== YOUR ORIGINAL MINI APP HTML - SAME AS BEFORE ====================
@app.route("/")
def home():
    db=load_db()
    s=db["settings"]
    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['app_name']}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<!-- YOUR MONETAG CODE - ZONE 11764581 - SAME AS YOUR SCREENSHOT -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
:root{{--t:{s['theme']}}};
*{{font-family:system-ui, -apple-system, sans-serif;box-sizing:border-box}}
body{{margin:0;background:#f5f7fb;padding-bottom:90px;color:#111}}
.topbar{{background:#b8f0e8;display:flex;align-items:center;justify-content:space-between;padding:12px 15px;position:sticky;top:0;z-index:100}}
.topbar b{{font-size:16px}}
.header{{background:var(--t);color:white;padding:14px 15px;display:flex;align-items:center;gap:12px}}
.avatar{{width:52px;height:52px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--t);font-weight:bold;font-size:22px}}
.card{{background:white;border-radius:22px;padding:15px;margin:12px;box-shadow:0 2px 10px rgba(0,0,0,0.04)}}
.balance-big{{font-size:44px;font-weight:800;color:var(--t);text-align:center;line-height:1}}
.ref-box{{background:#f1f5f4;border:1px solid #ddd;border-radius:14px;padding:12px;display:flex;justify-content:space-between;align-items:center;margin:12px 0;word-break:break-all;font-size:12px}}
.green-btn{{background:var(--t);color:white;border:none;padding:14px 16px;border-radius:14px;width:100%;font-weight:700;font-size:15px;cursor:pointer}}
.green-btn:active{{opacity:0.9}}
.dark-card{{background:#1a3c34;color:white;border-radius:22px;padding:18px;margin:12px;line-height:1.6}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0 6px 0;border-top:1px solid #e5e7eb;z-index:100}}
.b-item{{text-align:center;font-size:11px;color:#9ca3af;cursor:pointer;flex:1;transition:0.2s}}
.b-item.active{{color:var(--t)}}
.b-item i{{font-size:22px;display:block;margin-bottom:3px}}
.page{{display:none;animation:fade 0.2s}}
.page.active{{display:block}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.ad-card{{background:var(--t);color:white;border-radius:26px;padding:22px 20px;text-align:center;margin:12px;box-shadow:0 8px 20px rgba(108,92,231,0.3)}}
.task-row{{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;background:white;border-radius:18px;margin:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,0.03)}}
.method{{border:2px solid #e5e7eb;border-radius:16px;padding:14px;text-align:center;flex:1;cursor:pointer;transition:0.2s}}
.method.sel{{border-color:var(--t);background:#f0efff;color:var(--t)}}
.w-input{{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:14px;margin:8px 0;font-size:15px;outline:none}}
.w-input:focus{{border-color:var(--t)}}
.support-row{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:white;border-radius:18px;margin:10px 12px;cursor:pointer}}
#topMenu{{position:absolute;top:50px;right:10px;background:white;border-radius:14px;box-shadow:0 8px 25px rgba(0,0,0,0.15);padding:8px 0;width:180px;display:none;z-index:200}}
#topMenu div{{padding:12px 16px;font-size:13px;cursor:pointer}}
#topMenu div:hover{{background:#f5f7fb}}
.badge{{background:#ff4757;color:white;padding:2px 8px;border-radius:20px;font-size:10px;margin-left:6px}}
</style>
</head>
<body>

<div class="topbar">
  <b>{s['app_name']}</b>
  <div style="position:relative">
    <i class="fas fa-ellipsis-v" style="padding:8px;cursor:pointer" onclick="document.getElementById('topMenu').style.display=document.getElementById('topMenu').style.display=='block'?'none':'block'"></i>
    <div id="topMenu">
      <div onclick="showPage('profile');hideMenu()"><i class="fas fa-user"></i> My Profile</div>
      <div onclick="window.open('https://t.me/{s['channel_username']}');hideMenu()"><i class="fab fa-telegram"></i> Channel</div>
      <div onclick="window.open('https://t.me/{s['admin_username']}');hideMenu()"><i class="fas fa-headset"></i> Support</div>
    </div>
  </div>
</div>

<div class="header">
  <div class="avatar" id="av">U</div>
  <div>
    <b id="uname">User</b><br>
    <small>Welcome Bonus {s['welcome']} Tk | Ref Bonus {s['ref_bonus']} Tk</small>
  </div>
</div>

<!-- HOME PAGE - SAME AS YOUR SCREENSHOT -->
<div id="home" class="page active">
  <div class="card">
    <div class="balance-big" id="bal">0</div>
    <center style="color:#6b7280;margin-top:4px">Your Balance</center>
    <div class="ref-box">
      <span id="reflink" style="flex:1">Loading referral...</span>
      <button onclick="copyRef()" style="background:var(--t);color:white;border:none;padding:7px 12px;border-radius:8px;margin-left:8px;font-weight:600">Copy</button>
    </div>
    <center><small style="color:#6b7280">প্রতি রেফারে {s['ref_bonus']} টাকা পাবেন</small></center>
  </div>

  <div class="ad-card">
    <h2 style="margin:6px 0 8px 0;font-size:24px">Watch Ads & Earn</h2>
    <p style="margin:0 0 14px 0;opacity:0.95">প্রতিটি Ads এ {s['ad_reward']} টাকা | আজ <b><span id="today">0</span>/{s['ad_limit']}</b> টা দেখেছেন</p>
    <button class="green-btn" style="background:white;color:var(--t);font-size:17px" onclick="watchAd()"><i class="fas fa-play"></i> Watch Ad</button>
    <small id="lastTime" style="display:block;margin-top:10px;opacity:0.85;font-size:12px"></small>
  </div>

  <div class="dark-card">
    <b style="font-size:15px"><i class="fas fa-bullhorn"></i> {s['notice_title']}</b><br>
    <small style="white-space:pre-line;font-size:13px;opacity:0.95">{s['notice_text']}</small>
  </div>
</div>

<!-- TASK PAGE -->
<div id="task" class="page">
  <h3 style="padding:5px 18px;margin:10px 0">Daily Tasks <span class="badge">New</span></h3>
  <div id="taskList"><center style="padding:20px;color:#999">Loading tasks...</center></div>
  <div class="card" style="background:#fff8e1;border:1px dashed #fbbf24"><small>💡 টাস্ক কমপ্লিট করলে সাথে সাথে ব্যালেন্সে টাকা যোগ হবে</small></div>
</div>

<!-- WALLET PAGE -->
<div id="wallet" class="page">
  <div class="card">
    <h3 style="margin:0 0 6px 0">Withdraw Money</h3>
    <p style="margin:0 0 12px 0;color:#6b7280;font-size:13px">Minimum Withdraw {s['min_wd']} Tk | বিকাশ / নগদ</p>
    <div style="display:flex;gap:10px;margin-bottom:6px">
      <div class="method sel" id="m_bkash" onclick="selM('bkash')"><i class="fas fa-mobile-alt" style="font-size:20px"></i><br><b>Bkash</b></div>
      <div class="method" id="m_nagad" onclick="selM('nagad')"><i class="fas fa-wallet" style="font-size:20px"></i><br><b>Nagad</b></div>
    </div>
    <input id="w_number" class="w-input" placeholder="Bkash/Nagad Number (01XXXXXXXXX)">
    <input id="w_amount" class="w-input" placeholder="Amount (Min {s['min_wd']})" type="number">
    <button class="green-btn" onclick="doWithdraw()">Withdraw Request</button>
  </div>
  <div class="card">
    <h4 style="margin:0 0 10px 0">Withdraw History</h4>
    <div id="whistory" style="font-size:13px;color:#6b7280">কোনো হিস্ট্রি নেই</div>
  </div>
</div>

<!-- PROFILE PAGE -->
<div id="profile" class="page">
  <div class="card">
    <h3 style="margin-top:0"><i class="fas fa-user-circle"></i> My Profile</h3>
    <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f3f4f6"><span>Total Earn</span><b id="total">0 Tk</b></div>
    <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f3f4f6"><span>Total Ads Watched</span><b id="tads">0</b></div>
    <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f3f4f6"><span>Today Ads</span><b id="today2">0</b></div>
    <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f3f4f6"><span>Last Ad Time</span><b id="lastTime2" style="font-size:12px">Never</b></div>
    <div style="display:flex;justify-content:space-between;padding:10px 0"><span>Joined</span><b id="joined" style="font-size:12px">-</b></div>
  </div>
  <div class="support-row" onclick="window.open('https://t.me/{s['channel_username']}')"><span><i class="fab fa-telegram" style="color:var(--t)"></i> Our Channel</span><i class="fas fa-chevron-right" style="color:#ccc"></i></div>
  <div class="support-row" onclick="window.open('https://t.me/{s['group_link']}')"><span><i class="fas fa-users" style="color:var(--t)"></i> Our Group</span><i class="fas fa-chevron-right" style="color:#ccc"></i></div>
  <div class="support-row" onclick="window.open('https://t.me/{s['admin_username']}')"><span><i class="fas fa-headset" style="color:var(--t)"></i> Support / Admin</span><i class="fas fa-chevron-right" style="color:#ccc"></i></div>
  <div class="support-row" onclick="window.open('{s['video_link']}')"><span><i class="fab fa-youtube" style="color:red"></i> Tutorial Video</span><i class="fas fa-chevron-right" style="color:#ccc"></i></div>
</div>

<!-- BOTTOM NAV - SAME AS YOUR SCREENSHOT -->
<div class="bottom">
  <div class="b-item active" id="nav_home" onclick="showPage('home',this)"><i class="fas fa-home"></i>Home</div>
  <div class="b-item" id="nav_task" onclick="showPage('task',this)"><i class="fas fa-list-check"></i>Task</div>
  <div class="b-item" id="nav_wallet" onclick="showPage('wallet',this)"><i class="fas fa-wallet"></i>Wallet</div>
  <div class="b-item" id="nav_profile" onclick="showPage('profile',this)"><i class="fas fa-user"></i>Profile</div>
</div>

<script>
let UID = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || new URLSearchParams(location.search).get('id') || '123456';
let METHOD='bkash';
function hideMenu(){{document.getElementById('topMenu').style.display='none'}}
function showPage(p,el){{
  document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));
  document.getElementById(p).classList.add('active');
  document.querySelectorAll('.b-item').forEach(x=>x.classList.remove('active'));
  if(el) el.classList.add('active');
  else document.getElementById('nav_'+p)?.classList.add('active');
  hideMenu();
  window.scrollTo(0,0);
}}
function selM(m){{
  METHOD=m;
  document.querySelectorAll('.method').forEach(x=>x.classList.remove('sel'));
  document.getElementById('m_'+m).classList.add('sel');
}}
function copyRef(){{
  let t=document.getElementById('reflink').innerText;
  navigator.clipboard.writeText(t).then(()=>alert('✅ Refer Link Copied!\\n'+t));
}}
function loadData(){{
  fetch('/api/register',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}})
 .then(r=>r.json()).then(u=>{{
    document.getElementById('bal').innerText=u.balance;
    document.getElementById('total').innerText=u.total+' Tk';
    document.getElementById('today').innerText=u.today_ads||0;
    document.getElementById('today2').innerText=u.today_ads||0;
    document.getElementById('tads').innerText=u.total_ads||0;
    document.getElementById('joined').innerText=u.joined||'-';
    let lt=u.last_ads_time||'';
    document.getElementById('lastTime').innerText=lt? '⏰ Last Ad: '+lt : 'প্রথম Ads দেখুন';
    document.getElementById('lastTime2').innerText=lt||'Never';
    document.getElementById('uname').innerText='User '+String(UID).slice(-4);
    document.getElementById('av').innerText=String(UID).slice(-1);
    document.getElementById('reflink').innerText='https://t.me/{s['bot_username']}?start='+UID;
  }});
  fetch('/api/settings').then(r=>r.json()).then(s=>{{
    let h='';
    (s.tasks||[]).forEach(t=>{{
      h+=`<div class='task-row'><div style='display:flex;align-items:center;gap:10px'><div style='width:36px;height:36px;background:#f3f4f6;border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--t)'><i class='fab fa-${{t.icon}}'></i></div><div><b style='font-size:14px'>${{t.title}}</b><br><small style='color:#10b981'>+${{t.reward}} Tk</small></div></div><button class='green-btn' style='width:auto;padding:8px 16px;font-size:13px' onclick="window.open('${{t.link}}','_blank');fetch('/api/do_task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID,task_id:t.id}})}}).then(()=>loadData())">Go</button></div>`;
    }});
    document.getElementById('taskList').innerHTML=h||'<center style=color:#999;padding:20px>No tasks</center>';
  }});
}}
function watchAd(){{
  if(typeof show_11764581==='function'){{
    show_11764581().then(()=>{{
      fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}})
     .then(r=>r.json()).then(d=>{{
        if(d.error){{alert('❌ '+d.error);}}
        else{{
          document.getElementById('bal').innerText=d.balance;
          document.getElementById('today').innerText=d.today_ads;
          document.getElementById('today2').innerText=d.today_ads;
          document.getElementById('lastTime').innerText='⏰ Last Ad: '+d.last_ads_time;
          document.getElementById('lastTime2').innerText=d.last_ads_time;
          alert('✅ Success!\\n'+d.last_ads_time+'\\n1 Tk Added!\\nBalance: '+d.balance);
        }}
      }})
    }})
  }}else{{
    // Testing without Monetag
    fetch('/api/task_complete',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID}})}})
   .then(r=>r.json()).then(d=>{{
      document.getElementById('bal').innerText=d.balance;
      document.getElementById('today').innerText=d.today_ads;
      document.getElementById('lastTime').innerText='⏰ Last: '+d.last_ads_time;
      document.getElementById('lastTime2').innerText=d.last_ads_time;
      alert('✅ Test Ad - 1 Tk Added!\\n'+d.last_ads_time);
    }})
  }}
}}
function doWithdraw(){{
  let num=document.getElementById('w_number').value.trim();
  let amt=document.getElementById('w_amount').value.trim();
  if(!num||!amt) return alert('⚠️ Number and Amount দিন');
  fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{user_id:UID,method:METHOD,number:num,amount:parseInt(amt)}})}})
 .then(r=>r.json()).then(d=>{{
    if(d.error) alert('❌ '+d.error);
    else {{alert('✅ '+d.msg); document.getElementById('w_amount').value=''; loadData();}}
  }})
}}
document.addEventListener('click',function(e){{if(!e.target.closest('.topbar')) hideMenu();}});
loadData();
</script>
</body>
</html>"""

@app.route("/api/register", methods=["POST"])
def register():
    data=request.json
    uid=str(data.get("user_id"))
    db=load_db()
    if uid not in db["users"]:
        db["users"][uid]={
            "balance": db["settings"]["welcome"],
            "total": db["settings"]["welcome"],
            "today_ads": 0,
            "total_ads": 0,
            "last_date": datetime.now().strftime("%d/%m/%Y"),
            "last_ads_time": "", # ✅ TIME SAVE FIELD - ADDED
            "joined": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "refer_by": data.get("ref") if data.get("ref")!=uid else None
        }
        # Refer bonus
        if data.get("ref") and str(data.get("ref")) in db["users"] and str(data.get("ref"))!=uid:
            db["users"][str(data.get("ref"))]["balance"]+=db["settings"]["ref_bonus"]
            db["users"][str(data.get("ref"))]["total"]+=db["settings"]["ref_bonus"]
        save_db(db)
    return jsonify(db["users"][uid])

@app.route("/api/user/<uid>")
def get_user(uid):
    db=load_db()
    if uid not in db["users"]:
        return jsonify({"error":"not found"}),404
    return jsonify(db["users"][uid])

@app.route("/api/do_task", methods=["POST"])
def do_task():
    uid=str(request.json.get("user_id"))
    tid=request.json.get("task_id")
    db=load_db()
    if uid not in db["users"]:
        return jsonify({"ok":False,"error":"no user"}),404
    task=next((t for t in db["settings"]["tasks"] if t["id"]==tid), None)
    if not task:
        return jsonify({"ok":False,"error":"task not found"}),404
    db["users"][uid]["balance"]+=task["reward"]
    db["users"][uid]["total"]+=task["reward"]
    save_db(db)
    return jsonify({"ok":True,"link":task.get("link"),"reward":task.get("reward")})

@app.route("/api/task_complete", methods=["POST"])
def task_complete():
    uid=str(request.json.get("user_id"))
    db=load_db()
    s=db["settings"]
    if uid not in db["users"]:
        return jsonify({"ok":False,"error":"no user"}),404
    u=db["users"][uid]
    today_str=datetime.now().strftime("%d/%m/%Y")
    if u.get("last_date")!=today_str:
        u["today_ads"]=0
        u["last_date"]=today_str
    if u.get("today_ads",0) >= s["ad_limit"]:
        return jsonify({"error":f"আজ {s['ad_limit']} টা Ads শেষ! কাল আবার দেখতে পারবেন"}),400
    # ✅ MAIN FIX - Balance + Time Save Together
    u["balance"]+=s["ad_reward"]
    u["total"]+=s["ad_reward"]
    u["today_ads"]=u.get("today_ads",0)+1
    u["total_ads"]=u.get("total_ads",0)+1
    u["last_ads_time"]=datetime.now().strftime("%d/%m/%Y %I:%M %p")
    save_db(db)
    return jsonify(u)

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data=request.json
    uid=str(data.get("user_id"))
    db=load_db()
    s=db["settings"]
    if uid not in db["users"]:
        return jsonify({"error":"User not found"}),404
    u=db["users"][uid]
    try:
        amt=int(data.get("amount",0))
    except:
        return jsonify({"error":"Invalid amount"}),400
    if amt < s["min_wd"]:
        return jsonify({"error":f"Minimum withdraw {s['min_wd']} Tk"})
    if u["balance"] < amt:
        return jsonify({"error":f"Balance কম আছে। আপনার ব্যালেন্স {u['balance']} Tk"})
    u["balance"]-=amt
    db["withdraws"].append({
        "user_id": uid,
        "method": data.get("method","bkash"),
        "number": data.get("number",""),
        "amount": amt,
        "time": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
        "status": "pending"
    })
    save_db(db)
    return jsonify({"msg":f"✅ Withdraw Request Success! {amt} Tk - {data.get('method')}"})

@app.route("/api/settings")
def get_settings():
    db=load_db()
    return jsonify(db["settings"])

@app.route("/api/stats")
def stats():
    db=load_db()
    return jsonify({"total_users":len(db["users"]), "total_withdraws":len(db["withdraws"])})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
