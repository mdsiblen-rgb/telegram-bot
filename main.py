from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3
import time
import os

# ================= APP CONFIG =================
app = FastAPI()
DB_PATH = "database.db"

# এডমিন ID - Koyeb ENV থেকে নিবে, না থাকলে যে প্রথম ঢুকবে সেই এডমিন
ADMIN_ID = os.getenv("ADMIN_ID", "")

WELCOME_BONUS = 10
REF_BONUS = 25
TASK_REWARD = 5
AD_REWARD = 10

# ================= DATABASE =================
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
            withdraw_pending INTEGER DEFAULT 0
        )
    """)
    # পুরনো DB হলে কলাম Add করবে
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
        c.execute("ALTER TABLE users ADD COLUMN withdraw_pending INTEGER DEFAULT 0")
    except:
        pass

    conn.commit()
    conn.close()

init_db()

# ================= HOME HTML - FULL 350+ LINE LOGIC =================
def get_home_html(uid):
    return f"""
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Protidin Kaj BD - Daily Income</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<!-- Monetag SDK - তোমার Zone 11764581 -->
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
    body {{
        background: #f0f2f5;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 12px;
        color: #333;
    }}
   .card {{
        background: white;
        border-radius: 15px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
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
    #welcomeModal, #editModal {{
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
        animation: pop 0.3s ease;
    }}
    @keyframes pop {{
        from {{ transform: scale(0.8); opacity: 0; }}
        to {{ transform: scale(1); opacity: 1; }}
    }}
    #profilePic {{
        width: 92px;
        height: 92px;
        border-radius: 50%;
        border: 3.5px solid #28a745;
        object-fit: cover;
        background: #eee;
    }}
   .info-label {{
        font-size: 12px;
        color: #666;
        margin-top: 8px;
        margin-bottom: 4px;
    }}
   .ref-box {{
        background: #f8f9fa;
        border: 1px dashed #28a745;
        padding: 10px;
        border-radius: 10px;
        word-break: break-all;
        font-size: 11.5px;
    }}
</style>
</head>
<body>

<!-- ============ WELCOME MODAL - তোমার আগেরটা হুবহু ============ -->
<div id="welcomeModal">
  <div class="modal-box">
    <div style="font-size:55px;">🎉</div>
    <h2 style="color:#28a745; margin:5px 0;">স্বাগতম!</h2>
    <p style="font-size:14px;">Protidiner Kaj BD Bot এ আপনাকে স্বাগতম</p>
    <h3 style="background:#d4edda; color:#155724; padding:12px; border-radius:10px; margin:12px 0;">
        {WELCOME_BONUS} TK বোনাস পেয়েছেন!
    </h3>
    <p style="font-size:12.5px; color:#666;">
        প্রতিদিন কাজ করে আয় করুন<br>
        রেফার করে {REF_BONUS} TK করে আয় করুন
    </p>
    <button class="btn btn-green" onclick="closeWelcome()">🚀 শুরু করুন</button>
  </div>
</div>

<!-- ============ PROFILE EDIT MODAL ============ -->
<div id="editModal">
  <div class="modal-box">
    <h3 style="margin-top:0;">✏️ প্রোফাইল পরিবর্তন</h3>
    <p class="info-label" style="text-align:left;">নতুন নাম লিখুন (যেকোনো সময় পরিবর্তন করতে পারবেন):</p>
    <input id="newName" type="text" placeholder="যেমন: Rakib Hasan" style="width:100%; padding:11px; border-radius:9px; border:1px solid #ccc; box-sizing:border-box;">

    <p class="info-label" style="text-align:left; margin-top:12px;">নতুন ছবি সিলেক্ট করুন:</p>
    <input id="newPhoto" type="file" accept="image/*" style="width:100%; margin-bottom:12px;">

    <img id="preview" style="width:85px; height:85px; border-radius:50%; display:none; margin:0 auto 12px; object-fit:cover; border:2px solid #28a745;">

    <button class="btn btn-green" onclick="saveProfile()">💾 সেভ করুন</button>
    <button class="btn" style="background:#e9ecef; color:#333;" onclick="document.getElementById('editModal').style.display='none'">❌ বাতিল</button>
  </div>
</div>

<!-- ============ PROFILE CARD ============ -->
<div class="card" style="text-align:center;">
  <img id="profilePic" src="https://cdn-icons-png.flaticon.com/512/149/149071.png" alt="profile">
  <h3 id="profileName" style="margin:10px 0 0 0; font-size:18px;">Loading...</h3>
  <p id="uid_show" style="font-size:11px; color:#888; margin:4px 0 0 0;">ID:...</p>
  <button onclick="openEdit()" style="margin-top:10px; padding:7px 16px; border-radius:20px; border:1.5px solid #28a745; background:white; color:#28a745; font-weight:bold; cursor:pointer;">
    ✏️ নাম / ছবি পরিবর্তন করুন
  </button>
</div>

<!-- ============ BALANCE CARD - তোমার আগের bal, refCount, refLink ============ -->
<div class="card">
  <h3 id="bal" style="margin:0 0 6px 0;">Balance: Loading...</h3>
  <p id="refCount" style="margin:0; color:#555; font-size:14px;">রেফার: 0 জন</p>
  <p id="totalEarn" style="margin:6px 0 0 0; color:#28a745; font-size:13px; font-weight:bold;">মোট আয়: 0 TK</p>

  <p class="info-label">আপনার রেফার লিংক:</p>
  <div id="refLink" class="ref-box">Loading...</div>
  <p style="font-size:11px; color:#888; margin-top:6px;">এই লিংক শেয়ার করলে প্রতি রেফারে {REF_BONUS} TK</p>
</div>

<!-- ============ ACTION BUTTONS ============ -->
<div class="card">
  <button id="adBtn" class="btn btn-green" onclick="watchAd()">🎬 বিজ্ঞাপন দেখুন - {AD_REWARD} TK ইনকাম</button>
  <button id="taskBtn" class="btn btn-blue" onclick="completeTask()">✅ টাস্ক পূরণ করুন - {TASK_REWARD} TK</button>
  <button class="btn btn-dark" onclick="goEarn()">💰 My Earnings & Withdraw History</button>
  <button class="btn btn-yellow" onclick="copyRef()">📋 রেফার লিংক কপি করুন</button>
</div>

<div style="text-align:center; padding:10px; font-size:11px; color:#999;">
    Protidin Kaj BD © 2026 - All tasks inside Telegram
</div>

<!-- ================= JAVASCRIPT - তোমার আগের সব ফাংশন হুবহু রাখা ================= -->
<script>
let userId = "{uid}";

// Telegram ID বের করার ফাংশন - তোমার আগেরটা
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

// ID সেট করা
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

// Balance Load - তোমার আগেরটা
function loadBalance(){{
    fetch('/api/balance?user_id=' + userId)
   .then(r => r.json())
   .then(d => {{
        document.getElementById('bal').innerText = 'Balance: ' + d.balance + ' TK';
        document.getElementById('refCount').innerText = 'রেফার: ' + d.ref_count + ' জন';
        document.getElementById('totalEarn').innerText = 'মোট আয়: ' + (d.balance + (d.withdraw_pending || 0)) + ' TK';

        if(d.custom_name && d.custom_name.trim()!= ""){{
            document.getElementById('profileName').innerText = d.custom_name;
        }}
        if(d.custom_photo && d.custom_photo.startsWith('data:image')){{
            document.getElementById('profilePic').src = d.custom_photo;
        }}

        // Welcome Modal - তোমার আগের লজিক
        if(d.is_new &&!localStorage.getItem('welcomed_' + userId)){{
            setTimeout(() => {{
                document.getElementById('welcomeModal').style.display = 'flex';
            }}, 700);
        }}
    }});
}}
loadBalance();

function closeWelcome(){{
    document.getElementById('welcomeModal').style.display = 'none';
    localStorage.setItem('welcomed_' + userId, '1');
}}

// Task Complete - তোমার আগের completeTask()
function completeTask(){{
    let btn = document.getElementById('taskBtn');
    let oldText = btn.innerText;
    btn.innerText = "⌛ Loading...";
    btn.disabled = true;

    fetch('/api/task?user_id=' + userId)
   .then(r => r.text())
   .then(a => {{
        if(a.includes("সেকেন্ড")){{
            if(window.Telegram && Telegram.WebApp){{
                Telegram.WebApp.showAlert(a);
            }} else {{
                alert(a);
            }}
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

        if(window.Telegram && Telegram.WebApp){{
            Telegram.WebApp.showAlert(a);
        }} else {{
            alert(a);
        }}
    }});
}}

function goEarn(){{
    location.href = '/earnings/' + userId;
}}

function copyRef(){{
    let t = document.getElementById('refLink').innerText;
    if(navigator.clipboard){{
        navigator.clipboard.writeText(t).then(() => {{
            alert('✅ কপি হয়েছে!\\n' + t);
        }});
    }} else {{
        alert(t);
    }}
}}

// Profile Edit
function openEdit(){{
    document.getElementById('editModal').style.display = 'flex';
}}

document.getElementById('newPhoto').addEventListener('change', function(e){{
    let file = e.target.files[0];
    if(file){{
        if(file.size > 800000){{
            alert('ছবি 800KB এর কম হতে হবে');
            return;
        }}
        let reader = new FileReader();
        reader.onload = function(ev){{
            document.getElementById('preview').src = ev.target.result;
            document.getElementById('preview').style.display = 'block';
        }};
        reader.readAsDataURL(file);
    }}
}});

function saveProfile(){{
    let name = document.getElementById('newName').value.trim();
    let photo = document.getElementById('preview').src;

    if(photo.includes('flaticon')){{
        photo = '';
    }}

    if(!name && (!photo || photo == '')){{
        alert('নাম বা ছবি দিন');
        return;
    }}

    if(name){{
        document.getElementById('profileName').innerText = name;
    }}
    if(photo && photo.startsWith('data:image')){{
        document.getElementById('profilePic').src = photo;
    }}

    fetch('/api/update_profile?user_id=' + userId + '&name=' + encodeURIComponent(name) + '&photo=' + encodeURIComponent(photo))
   .then(() => {{
        document.getElementById('editModal').style.display = 'none';
        alert('✅ প্রোফাইল আপডেট হয়েছে! যেকোনো সময় আবার পরিবর্তন করতে পারবেন।');
        document.getElementById('newName').value = '';
    }});
}}

// ================= MONETAG AD - নতুন In-App Rewarded Interstitial =================
let timerStarted = false;

function watchAd(){{
    if(timerStarted){{
        return;
    }}

    if(typeof show_11764581!== 'function'){{
        alert('Ad SDK লোড হচ্ছে... 2 সেকেন্ড পর আবার ক্লিক করুন');
        setTimeout(() => {{ location.reload(); }}, 1500);
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
            btn.innerText = "✅ Done! 30s Wait";
            setTimeout(() => {{
                btn.innerText = oldText;
                btn.disabled = false;
                timerStarted = false;
            }}, 30000);

            if(window.Telegram && Telegram.WebApp){{
                Telegram.WebApp.showAlert(a);
            }} else {{
                alert(a);
            }}
        }});
    }}).catch((e) => {{
        console.log(e);
        timerStarted = false;
        btn.innerText = oldText;
        btn.disabled = false;
        alert('Ad দেখা সম্পূর্ণ হয়নি, আবার চেষ্টা করুন');
    }});
}}
</script>
</body>
</html>
"""

# ================= ROUTES =================
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
            "INSERT INTO users (user_id, balance, referred_by, total_earned) VALUES (?,?,?,?)",
            (uid, WELCOME_BONUS, start_ref, WELCOME_BONUS)
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
    c.execute("SELECT balance, ref_count, custom_name, custom_photo, total_earned, withdraw_pending FROM users WHERE user_id=?", (user_id,))
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
            "withdraw_pending": 0
        })

    return JSONResponse({
        "balance": row[0],
        "ref_count": row[1],
        "is_new": False,
        "custom_name": row[2] or "",
        "custom_photo": row[3] or "",
        "total_earned": row[4] or row[0],
        "withdraw_pending": row[5] or 0
    })

@app.get("/api/task")
async def api_task(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_task FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return HTMLResponse("User not found")
    now = int(time.time())
    if now - row[0] < 30:
        wait = 30 - (now - row[0])
        conn.close()
        return HTMLResponse(f"⏳ {wait} সেকেন্ড পর আবার চেষ্টা করুন")
    c.execute("UPDATE users SET balance = balance +?, last_task =?, total_earned = total_earned +? WHERE user_id=?", (TASK_REWARD, now, TASK_REWARD, user_id))
    conn.commit()
    conn.close()
    return HTMLResponse(f"✅ {TASK_REWARD} TK যোগ হয়েছে!")

@app.get("/api/ad")
async def api_ad(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_ad FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return HTMLResponse("User not found")
    now = int(time.time())
    if now - row[0] < 30:
        wait = 30 - (now - row[0])
        conn.close()
        return HTMLResponse(f"⏳ {wait} সেকেন্ড পর Ad দেখতে পারবেন")
    c.execute("UPDATE users SET balance = balance +?, last_ad =?, total_earned = total_earned +? WHERE user_id=?", (AD_REWARD, now, AD_REWARD, user_id))
    conn.commit()
    conn.close()
    return HTMLResponse(f"🎉 {AD_REWARD} TK বোনাস পেয়েছেন! Monetag Ad দেখার জন্য ধন্যবাদ!")

@app.get("/api/update_profile")
async def update_profile(user_id: str, name: str = "", photo: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if name and len(name) <= 50:
        c.execute("UPDATE users SET custom_name=? WHERE user_id=?", (name, user_id))
    if photo and "data:image" in photo and len(photo) < 400000:
        c.execute("UPDATE users SET custom_photo=? WHERE user_id=?", (photo, user_id))
    conn.commit()
    conn.close()
    return JSONResponse({"status": "ok", "message": "Profile Updated Anytime"})

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
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:sans-serif; padding:20px; background:#f0f2f5;}}.card{{background:white; padding:15px; border-radius:12px;}}</style>
    </head><body>
    <div class="card">
    <h2>💰 My Earnings</h2>
    <p>Current Balance: <b>{bal} TK</b></p>
    <p>Total Earned: <b>{total} TK</b></p>
    <p>Total Refer: <b>{ref} জন</b></p>
    <hr>
    <p style="font-size:13px; color:gray;">Withdraw: 500 TK হলে বিকাশে নিতে পারবেন</p>
    <a href="/?id={uid}" style="display:block; text-align:center; background:#28a745; color:white; padding:12px; border-radius:10px; text-decoration:none; margin-top:10px;">Back to Home</a>
    </div>
    </body></html>
    """)

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    uid = request.query_params.get("id", "")
    global ADMIN_ID
    if not ADMIN_ID and uid:
        ADMIN_ID = uid
    if not uid or uid!= ADMIN_ID:
        return HTMLResponse(f"<h2>⛔ Admin Only</h2><p>Your ID: {uid}<br>First user becomes admin if ADMIN_ID not set.</p>")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, balance, ref_count, custom_name, total_earned FROM users ORDER BY balance DESC LIMIT 150")
    users = c.fetchall()
    conn.close()
    rows = ""
    for u in users:
        rows += f"<tr><td>{u[0]}</td><td>{u[3] or 'No Name'}</td><td>{u[1]} TK</td><td>{u[4] or u[1]} TK</td><td>{u[2]}</td></tr>"
    return HTMLResponse(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>table{{border-collapse:collapse; width:100%;}} td,th{{border:1px solid #ccc; padding:6px; font-size:12px;}} body{{font-family:sans-serif; padding:10px;}}</style>
    </head><body>
    <h2>👑 Admin Panel - Total {len(users)} Users</h2>
    <p>Admin ID: {ADMIN_ID}</p>
    <table><tr><th>User ID</th><th>Custom Name</th><th>Balance</th><th>Total Earned</th><th>Refs</th></tr>{rows}</table>
    <br><a href="/?id={ADMIN_ID}">Go Home</a>
    </body></html>
    """)
