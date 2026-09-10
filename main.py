from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import sqlite3
import time
import os
from datetime import datetime

# ======================================================
# App Config
# ======================================================
app = FastAPI()

DB_PATH = "database.db"

# Admin ID ENV থেকে
ADMIN_ID = os.getenv("ADMIN_ID", "")

# Rewards
WELCOME_BONUS = 10
REF_BONUS = 25
TASK_REWARD = 5
AD_REWARD = 10

# Ad Limit Config - তোমার চাওয়া অনুযায়ী
DAILY_AD_LIMIT = 20
AD_COOLDOWN = 60

# ======================================================
# Database Init
# ======================================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            ref_count INTEGER DEFAULT 0,
            last_task INTEGER DEFAULT 0,
            last_ad INTEGER DEFAULT 0,
            referred_by TEXT,
            custom_name TEXT DEFAULT '',
            custom_photo TEXT DEFAULT '',
            total_earned INTEGER DEFAULT 0,
            ad_today INTEGER DEFAULT 0,
            last_ad_date TEXT DEFAULT ''
        )
    """)

    # পুরনো DB হলে কলাম Add
    try:
        c.execute("ALTER TABLE users ADD COLUMN custom_name TEXT DEFAULT ''")
    except:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN custom_photo TEXT DEFAULT ''")
    except:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN total_earned INTEGER DEFAULT 0")
    except:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN ad_today INTEGER DEFAULT 0")
    except:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN last_ad_date TEXT DEFAULT ''")
    except:
        pass

    conn.commit()
    conn.close()

# DB Init Call
init_db()

# ======================================================
# Profile Update Model - POST এর জন্য
# ======================================================
class ProfileUpdate(BaseModel):
    user_id: str
    name: str = ""
    photo: str = ""

# ======================================================
# Home HTML - Full 600+ Line Version
# ======================================================
def get_home_html(uid):

    # HTML Start
    return f"""
<!DOCTYPE html>
<html lang="bn">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Protidin Kaj BD - Daily Income</title>

<!-- Telegram WebApp SDK -->
<script src="https://telegram.org/js/telegram-web-app.js"></script>

<!-- Monetag SDK - Zone 11764581 -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>

<style>

    /* Body Style */
    body {{
        background: #f0f2f5;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 12px;
        color: #333;
    }}

    /* Card Style */
   .card {{
        background: white;
        border-radius: 15px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    /* Button Style */
   .btn {{
        width: 100%;
        padding: 13px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        margin-top: 10px;
        font-size: 14px;
        transition: 0.2s;
    }}

   .btn:active {{
        transform: scale(0.97);
    }}

   .btn-green {{
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
    }}

   .btn-blue {{
        background: linear-gradient(135deg, #007bff, #00bfff);
        color: white;
    }}

   .btn-dark {{
        background: #343a40;
        color: white;
    }}

   .btn-yellow {{
        background: #ffc107;
        color: #000;
    }}

    /* Modal Style */
    #welcomeModal,
    #editModal {{
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.65);
        z-index: 9999;
        justify-content: center;
        align-items: center;
        padding: 15px;
    }}

   .modal-box {{
        background: white;
        padding: 22px;
        border-radius: 18px;
        width: 100%;
        max-width: 360px;
        text-align: center;
    }}

    /* Profile Pic */
    #profilePic {{
        width: 92px;
        height: 92px;
        border-radius: 50%;
        border: 3.5px solid #28a745;
        object-fit: cover;
        background: #eee;
    }}

   .ref-box {{
        background: #f8f9fa;
        border: 1px dashed #28a745;
        padding: 10px;
        border-radius: 10px;
        word-break: break-all;
        font-size: 11.5px;
    }}

   .info-label {{
        font-size: 12px;
        color: #666;
        text-align: left;
        margin-top: 10px;
    }}

</style>

</head>

<body>

<!-- ================= WELCOME MODAL ================= -->
<div id="welcomeModal">
  <div class="modal-box">

    <div style="font-size:55px;">🎉</div>

    <h2 style="color:#28a745;">স্বাগতম!</h2>

    <p>Protidiner Kaj BD Bot এ আপনাকে স্বাগতম</p>

    <h3 style="background:#d4edda; color:#155724; padding:12px; border-radius:10px;">
        {WELCOME_BONUS} TK বোনাস পেয়েছেন!
    </h3>

    <p style="font-size:12px; color:gray;">
        রেফার করে {REF_BONUS} TK করে আয় করুন
    </p>

    <button class="btn btn-green" onclick="closeWelcome()">
        🚀 শুরু করুন
    </button>

  </div>
</div>

<!-- ================= PROFILE EDIT MODAL / SETTINGS ================= -->
<div id="editModal">
  <div class="modal-box">

    <h3 style="margin-top:0;">⚙️ প্রোফাইল সেটিংস</h3>

    <p class="info-label">
        নতুন নাম (যেকোনো সময় পরিবর্তন করতে পারবেন):
    </p>

    <input
        id="newName"
        type="text"
        placeholder="যেমন: Rakib Hasan"
        style="width:100%; padding:11px; border-radius:9px; border:1px solid #ccc; box-sizing:border-box;"
    >

    <p class="info-label">
        নতুন ছবি সিলেক্ট করুন (800KB এর কম):
    </p>

    <input
        id="newPhoto"
        type="file"
        accept="image/*"
        style="width:100%;"
    >

    <img
        id="preview"
        data-base64=""
        style="width:85px; height:85px; border-radius:50%; display:none; margin:12px auto; object-fit:cover; border:2px solid #28a745;"
    >

    <button class="btn btn-green" onclick="saveProfile()">
        💾 সেভ করুন
    </button>

    <button class="btn" style="background:#e9ecef;" onclick="document.getElementById('editModal').style.display='none'">
        ❌ বাতিল
    </button>

  </div>
</div>

<!-- ================= PROFILE CARD ================= -->
<div class="card" style="text-align:center;">

    <img
        id="profilePic"
        src="https://cdn-icons-png.flaticon.com/512/149/149071.png"
        alt="profile"
    >

    <h3 id="profileName" style="margin:10px 0 0 0;">
        Loading...
    </h3>

    <p id="uid_show" style="font-size:11px; color:#888;">
        ID:...
    </p>

    <p id="adLeft" style="font-size:12px; color:#dc3545; font-weight:bold; margin-top:8px;">
        Ad বাকি: Loading...
    </p>

    <button
        onclick="openEdit()"
        style="margin-top:10px; padding:7px 16px; border-radius:20px; border:1.5px solid #28a745; background:white; color:#28a745; font-weight:bold; cursor:pointer;"
    >
        ⚙️ সেটিংস / নাম-ছবি পরিবর্তন
    </button>

</div>

<!-- ================= BALANCE CARD ================= -->
<div class="card">

    <h3 id="bal" style="margin:0;">
        Balance: Loading...
    </h3>

    <p id="refCount" style="margin:6px 0;">
        রেফার: 0 জন
    </p>

    <p id="totalEarn" style="color:#28a745; font-weight:bold; font-size:13px;">
        মোট আয়: 0 TK
    </p>

    <p class="info-label">
        আপনার রেফার লিংক:
    </p>

    <div id="refLink" class="ref-box">
        Loading...
    </div>

    <p style="font-size:11px; color:#888;">
        এই লিংক শেয়ার করলে প্রতি রেফারে {REF_BONUS} TK
    </p>

</div>

<!-- ================= ACTION BUTTONS ================= -->
<div class="card">

    <button id="adBtn" class="btn btn-green" onclick="watchAd()">
        🎬 বিজ্ঞাপন দেখুন - {AD_REWARD} TK
    </button>

    <button id="taskBtn" class="btn btn-blue" onclick="completeTask()">
        ✅ টাস্ক পূরণ করুন - {TASK_REWARD} TK
    </button>

    <button class="btn btn-dark" onclick="goEarn()">
        💰 My Earnings & Withdraw
    </button>

    <button class="btn btn-yellow" onclick="copyRef()">
        📋 রেফার লিংক কপি করুন
    </button>

</div>

<div style="text-align:center; padding:10px; font-size:11px; color:#999;">
    Protidin Kaj BD © 2026 - Daily Limit {DAILY_AD_LIMIT} Ads
</div>

<!-- ================= JAVASCRIPT ================= -->
<script>

// User ID
let userId = "{uid}";

// Telegram ID বের করার ফাংশন
function getTgId(){{
    try{{
        if(window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user){{
            return Telegram.WebApp.initDataUnsafe.user.id.toString();
        }}
    }}catch(e){{}}
    return null;
}}

let tgId = getTgId();

let tgUser = null;

try{{
    tgUser = window.Telegram.WebApp.initDataUnsafe.user;
}}catch(e){{}}

// ID Set
if(tgId){{
    userId = tgId;

    document.getElementById('uid_show').innerText = 'ID: ' + userId;

    document.getElementById('refLink').innerText = 'https://t.me/ProtidinerKaj_BD_Bot?start=' + userId;

    if(tgUser){{
        if(tgUser.photo_url){{
            document.getElementById('profilePic').src = tgUser.photo_url;
        }}

        let fullName = (tgUser.first_name || '') + ' ' + (tgUser.last_name || '');

        if(fullName.trim()){{
            document.getElementById('profileName').innerText = fullName.trim();
        }}
    }}
}}

// Guest হলে URL Replace
if("{uid}" == "guest" && tgId){{
    history.replaceState(null, '', '/?id=' + tgId);
}}

// Balance Load Function
function loadBalance(){{

    // Local থেকে আগে লোড - যাতে সাথে সাথে দেখায়
    let localName = localStorage.getItem('my_name_' + userId);
    let localPhoto = localStorage.getItem('my_photo_' + userId);

    if(localName){{
        document.getElementById('profileName').innerText = localName;
    }}

    if(localPhoto){{
        document.getElementById('profilePic').src = localPhoto;
    }}

    fetch('/api/balance?user_id=' + userId)
  .then(r => r.json())
  .then(d => {{

        document.getElementById('bal').innerText = 'Balance: ' + d.balance + ' TK';

        document.getElementById('refCount').innerText = 'রেফার: ' + d.ref_count + ' জন';

        document.getElementById('totalEarn').innerText = 'মোট আয়: ' + (d.total_earned || d.balance) + ' TK';

        document.getElementById('adLeft').innerText = 'আজ Ad বাকি: ' + (d.ad_left || 0) + ' টি';

        if(d.custom_name){{
            document.getElementById('profileName').innerText = d.custom_name;
            localStorage.setItem('my_name_' + userId, d.custom_name);
        }}

        if(d.custom_photo && d.custom_photo.startsWith('data:image')){{
            document.getElementById('profilePic').src = d.custom_photo;
            localStorage.setItem('my_photo_' + userId, d.custom_photo);
        }}

        // Welcome Modal
        if(d.is_new &&!localStorage.getItem('welcomed_' + userId)){{
            setTimeout(() => {{
                document.getElementById('welcomeModal').style.display = 'flex';
            }}, 700);
        }}

        // Ad Limit শেষ হলে Disable
        if(d.ad_left <= 0){{
            let b = document.getElementById('adBtn');
            b.innerText = '❌ আজকের লিমিট শেষ';
            b.disabled = true;
            b.style.background = '#ccc';
        }}

    }});
}}

// Load Balance Call
loadBalance();

// Welcome Close
function closeWelcome(){{
    document.getElementById('welcomeModal').style.display = 'none';
    localStorage.setItem('welcomed_' + userId, '1');
}}

// Task Complete
function completeTask(){{
    let btn = document.getElementById('taskBtn');
    let oldText = btn.innerText;

    btn.innerText = "⌛ Loading...";
    btn.disabled = true;

    fetch('/api/task?user_id=' + userId)
  .then(r => r.text())
  .then(a => {{

        if(a.includes("সেকেন্ড")){{
            alert(a);
            btn.innerText = oldText;
            btn.disabled = false;
            return;
        }}

        loadBalance();

        btn.innerText = "✅ Done! 30s Wait";

        setTimeout(() => {{
            btn.innerText = oldText;
            btn.disabled = false;
        }}, 30000);

        alert(a);

    }});
}}

// Go Earn Page
function goEarn(){{
    location.href = '/earnings/' + userId;
}}

// Copy Ref Link
function copyRef(){{
    let t = document.getElementById('refLink').innerText;

    navigator.clipboard.writeText(t).then(() => {{
        alert('✅ কপি হয়েছে!\\n' + t);
    }});
}}

// Open Edit Modal - Settings
function openEdit(){{
    document.getElementById('editModal').style.display = 'flex';
}}

// Photo Preview
document.getElementById('newPhoto').addEventListener('change', function(e){{

    let file = e.target.files[0];

    if(!file) return;

    if(file.size > 900000){{
        alert('ছবি 900KB এর কম হতে হবে, ছোট ছবি দিন');
        return;
    }}

    let reader = new FileReader();

    reader.onload = function(ev){{
        let img = document.getElementById('preview');
        img.src = ev.target.result;
        img.setAttribute('data-base64', ev.target.result);
        img.style.display = 'block';
    }};

    reader.readAsDataURL(file);

}});

// Save Profile - POST দিয়ে
function saveProfile(){{
    let name = document.getElementById('newName').value.trim();
    let photo = document.getElementById('preview').getAttribute('data-base64') || '';

    if(!name &&!photo){{
        alert('নাম বা ছবি দিন');
        return;
    }}

    if(name){{
        document.getElementById('profileName').innerText = name;
        localStorage.setItem('my_name_' + userId, name);
    }}

    if(photo){{
        document.getElementById('profilePic').src = photo;
        localStorage.setItem('my_photo_' + userId, photo);
    }}

    fetch('/api/update_profile', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{user_id: userId, name: name, photo: photo}})
    }})
  .then(r => r.json())
  .then(d => {{
        document.getElementById('editModal').style.display = 'none';
        document.getElementById('newName').value = '';
        alert('✅ প্রোফাইল সেভ হয়েছে! যেকোনো সময় চেঞ্জ করতে পারবেন');
    }});

}}

// Ad Watch - Monetag In-App + Limit
let timerStarted = false;

function watchAd(){{

    if(timerStarted) return;

    if(typeof show_11764581!== 'function'){{
        alert('Ad SDK লোড হচ্ছে... 2 সেকেন্ড পর আবার ক্লিক করুন');
        return;
    }}

    timerStarted = true;

    let btn = document.getElementById('adBtn');
    let oldText = btn.innerText;

    btn.innerText = '⏳ বিজ্ঞাপন লোড হচ্ছে...';
    btn.disabled = true;

    show_11764581().then(() => {{

        btn.innerText = '✅ যাচাই করা হচ্ছে...';

        fetch('/api/ad?user_id=' + userId)
      .then(r => r.text())
      .then(a => {{

            loadBalance();

            if(a.includes("লিমিট") || a.includes("সেকেন্ড")){{
                alert(a);
                btn.innerText = oldText;
                btn.disabled = false;
                timerStarted = false;
                return;
            }}

            btn.innerText = "✅ Done! 60s Wait";

            setTimeout(() => {{
                btn.innerText = oldText;
                btn.disabled = false;
                timerStarted = false;
            }}, 60000);

            alert(a);

        }});

    }})
  .catch(() => {{
        timerStarted = false;
        btn.innerText = oldText;
        btn.disabled = false;
        alert('Ad দেখা হয়নি, আবার চেষ্টা করুন');
    }});

}}

</script>

</body>
</html>
    """

# ======================================================
# Routes
# ======================================================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):

    uid = request.query_params.get("id", "guest")
    start_ref = request.query_params.get("start", None)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT user_id FROM users WHERE user_id=?", (uid,))
    exists = c.fetchone()

    if not exists and uid!= "guest":

        c.execute(
            "INSERT INTO users (user_id, balance, referred_by, total_earned, ad_today, last_ad_date) VALUES (?,?,?,?,?,?)",
            (uid, WELCOME_BONUS, start_ref, WELCOME_BONUS, 0, "")
        )

        if start_ref and start_ref!= uid:
            c.execute("SELECT user_id FROM users WHERE user_id=?", (start_ref,))
            if c.fetchone():
                c.execute(
                    "UPDATE users SET balance = balance +?, ref_count = ref_count + 1, total_earned = total_earned +? WHERE user_id=?",
                    (REF_BONUS, REF_BONUS, start_ref)
                )

        conn.commit()

    conn.close()

    return HTMLResponse(get_home_html(uid))

@app.get("/api/balance")
async def api_balance(user_id: str):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    c.execute(
        "SELECT balance, ref_count, custom_name, custom_photo, total_earned, ad_today, last_ad_date FROM users WHERE user_id=?",
        (user_id,)
    )

    row = c.fetchone()

    conn.close()

    if not row:
        return JSONResponse({
            "balance": 0,
            "ref_count": 0,
            "is_new": True,
            "custom_name": "",
            "custom_photo": "",
            "total_earned": 0,
            "ad_left": DAILY_AD_LIMIT
        })

    ad_today = row[5] or 0
    last_date = row[6] or ""

    if last_date!= today:
        ad_today = 0

    ad_left = DAILY_AD_LIMIT - ad_today

    return JSONResponse({
        "balance": row[0],
        "ref_count": row[1],
        "is_new": False,
        "custom_name": row[2] or "",
        "custom_photo": row[3] or "",
        "total_earned": row[4] or row[0],
        "ad_left": ad_left if ad_left >= 0 else 0
    })

@app.get("/api/task")
async def api_task(user_id: str):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT last_task FROM users WHERE user_id=?", (user_id,))

    r = c.fetchone()

    if not r:
        conn.close()
        return HTMLResponse("User not found")

    now = int(time.time())

    if now - r[0] < 30:
        conn.close()
        return HTMLResponse(f"⏳ {30-(now-r[0])} সেকেন্ড পর আবার চেষ্টা করুন")

    c.execute(
        "UPDATE users SET balance = balance +?, last_task =?, total_earned = total_earned +? WHERE user_id=?",
        (TASK_REWARD, now, TASK_REWARD, user_id)
    )

    conn.commit()
    conn.close()

    return HTMLResponse(f"✅ {TASK_REWARD} TK যোগ হয়েছে!")

@app.get("/api/ad")
async def api_ad(user_id: str):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    c.execute("SELECT last_ad, ad_today, last_ad_date FROM users WHERE user_id=?", (user_id,))

    r = c.fetchone()

    if not r:
        conn.close()
        return HTMLResponse("User not found")

    last_ad, ad_today, last_date = r[0] or 0, r[1] or 0, r[2] or ""

    if last_date!= today:
        ad_today = 0

    if ad_today >= DAILY_AD_LIMIT:
        conn.close()
        return HTMLResponse(f"❌ আজকের {DAILY_AD_LIMIT} টা Ad লিমিট শেষ! আগামীকাল আবার দেখতে পারবেন")

    now = int(time.time())

    if now - last_ad < AD_COOLDOWN:
        conn.close()
        return HTMLResponse(f"⏳ {AD_COOLDOWN-(now-last_ad)} সেকেন্ড পর Ad দেখতে পারবেন")

    c.execute(
        "UPDATE users SET balance = balance +?, last_ad =?, total_earned = total_earned +?, ad_today =?, last_ad_date =? WHERE user_id=?",
        (AD_REWARD, now, AD_REWARD, ad_today+1, today, user_id)
    )

    conn.commit()
    conn.close()

    left = DAILY_AD_LIMIT - (ad_today+1)

    return HTMLResponse(f"🎉 {AD_REWARD} TK পেয়েছেন! আজ আর {left} টা Ad দেখতে পারবেন")

@app.post("/api/update_profile")
async def update_profile_post(data: ProfileUpdate):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if data.name and len(data.name) <= 50:
        c.execute("UPDATE users SET custom_name=? WHERE user_id=?", (data.name, data.user_id))

    if data.photo and "data:image" in data.photo and len(data.photo) < 900000:
        c.execute("UPDATE users SET custom_photo=? WHERE user_id=?", (data.photo, data.user_id))

    conn.commit()
    conn.close()

    return JSONResponse({"status": "ok"})

@app.get("/api/update_profile")
async def update_profile_get(user_id: str, name: str = "", photo: str = ""):
    return JSONResponse({"status": "ok"})

@app.get("/earnings/{uid}", response_class=HTMLResponse)
async def earnings_page(uid: str):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT balance, ref_count, total_earned FROM users WHERE user_id=?", (uid,))

    row = c.fetchone()

    conn.close()

    bal = row[0] if row else 0
    ref = row[1] if row else 0
    total = row[2] if row else bal

    return HTMLResponse(f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body{{font-family:sans-serif; padding:15px; background:#f0f2f5;}}
          .card{{background:white; padding:18px; border-radius:15px;}}
          .btn{{width:100%; padding:12px; border-radius:10px; border:none; font-weight:bold; margin-top:10px;}}
          .green{{background:#28a745; color:white;}}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>💰 My Earnings</h2>
            <p>Current Balance: <b>{bal} TK</b></p>
            <p>Total Earned: <b>{total} TK</b></p>
            <p>Total Refer: <b>{ref} জন</b></p>
            <p style="font-size:12px; color:gray;">Ad Limit: দিনে {DAILY_AD_LIMIT} টা</p>
            <button class="btn green" onclick="if({bal}>=500){{alert('✅ Withdraw Request পাঠানো হয়েছে!');}}else{{alert('❌ 500 TK লাগবে');}}">🏦 Withdraw Request</button>
            <button class="btn" style="background:#6c757d; color:white;" onclick="location.href='/?id={uid}'">⬅️ Back to Home</button>
        </div>
    </body>
    </html>
    """)

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):

    uid = request.query_params.get("id", "")

    global ADMIN_ID

    if not ADMIN_ID and uid:
        ADMIN_ID = uid

    if not uid or uid!= ADMIN_ID:
        return HTMLResponse(f"<h2>⛔ Admin Only</h2><p>Your ID: {uid}</p>")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT user_id, balance, ref_count, custom_name FROM users ORDER BY balance DESC LIMIT 150")

    users = c.fetchall()

    conn.close()

    rows = ""

    for u in users:
        rows += f"<tr><td>{u[0]}</td><td>{u[3] or ''}</td><td>{u[1]}</td><td>{u[2]}</td></tr>"

    return HTMLResponse(f"""
    <html>
    <body>
        <h2>👑 Admin - {len(users)} Users - Limit {DAILY_AD_LIMIT}/day</h2>
        <table border=1 cellpadding=6>
            <tr><th>ID</th><th>Name</th><th>Bal</th><th>Ref</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """)
