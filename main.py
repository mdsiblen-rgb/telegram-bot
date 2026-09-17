import os, json
from flask import Flask, request, jsonify
app = Flask(__name__)
DB = "database.json"

def load_db():
    if not os.path.exists(DB):
        d = {
            "users": {},
            "settings": {
                "app_name": "প্রতিদিনের কাজ বিডি",
                "app_name2": "Daily Work BD",
                "ad_c": 0.5,
                "ad_p": 0.3,
                "clim": 80,
                "plim": 80,
                "min": 200,
                "ref": 20,
                "bonus": 20,
                "direct_link": "https://omg10.com/4/11760259",
                "spon_link": "https://google.com",
                "notice": "রাত ১০টার পর Withdraw বন্ধ থাকে\nসকাল ৯টার পর আবার চালু হয়\nFake Account করলে ব্যান"
            },
            "tasks": [
                {"t": "Visit Company Website - ৳20", "s": "৳0.2", "i": "🌐"},
                {"t": "Watch Video - ৳25", "s": "৳0.25", "i": "▶️"},
                {"t": "Join Telegram - ৳30", "s": "৳0.3", "i": "📢"}
            ]
        }
        f = open(DB, "w", encoding="utf-8")
        f.write(json.dumps(d, ensure_ascii=False, indent=2))
        f.close()
        return d
    f = open(DB, "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    return data

def save_db(db):
    f = open(DB, "w", encoding="utf-8")
    f.write(json.dumps(db, ensure_ascii=False, indent=2))
    f.close()

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "name": "User 4250",
            "bal": 21.1,
            "total": 21.1,
            "diamonds": 2110,
            "c": 2,
            "p": 1,
            "refl": 0,
            "join": "2026-09-15",
            "img": ""
        }
    return db["users"][uid]

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin', '*')
    return r

@app.route('/api/init', methods=['POST'])
def api_init():
    db = load_db()
    j = request.json or {}
    uid = str(j.get('id', '4250'))
    ref = j.get('ref')
    u = get_user(db, uid)
    if ref and ref!= uid and ref in db["users"]:
        # refer bonus - admin থেকে control
        pass
    save_db(db)
    return jsonify({"user": u, "s": db["settings"], "tasks": db.get("tasks", [])})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    db = load_db()
    j = request.json or {}
    uid = str(j.get('id', '4250'))
    typ = j.get('type', 'c')
    u = get_user(db, uid)
    s = db["settings"]
    if typ == 'c':
        if u["c"] >= s["clim"]:
            return jsonify({"msg": "আজকের 80 টা শেষ"})
        u["c"] = u["c"] + 1
        u["bal"] = round(u["bal"] + float(s["ad_c"]), 2)
        u["diamonds"] = u["diamonds"] + 25
    else:
        if u["p"] >= s["plim"]:
            return jsonify({"msg": "আজকের 80 টা শেষ"})
        u["p"] = u["p"] + 1
        u["bal"] = round(u["bal"] + float(s["ad_p"]), 2)
        u["diamonds"] = u["diamonds"] + 20
    save_db(db)
    return jsonify({"msg": "টাকা যোগ হয়েছে", "bal": u["bal"]})

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    db = load_db()
    if request.method == 'POST':
        f = request.form
        s = db["settings"]
        if f.get('app_name'): s['app_name'] = f.get('app_name')
        if f.get('ad_c'): s['ad_c'] = float(f.get('ad_c'))
        if f.get('ad_p'): s['ad_p'] = float(f.get('ad_p'))
        if f.get('clim'): s['clim'] = int(f.get('clim'))
        if f.get('plim'): s['plim'] = int(f.get('plim'))
        if f.get('min'): s['min'] = int(f.get('min'))
        if f.get('ref'): s['ref'] = int(f.get('ref'))
        if f.get('direct_link'): s['direct_link'] = f.get('direct_link')
        if f.get('spon_link'): s['spon_link'] = f.get('spon_link')
        if f.get('notice'): s['notice'] = f.get('notice')
        save_db(db)
    s = db["settings"]
    html_admin = """
    <body style="background:#0B0E1C;color:#fff;padding:15px;font-family:system-ui;max-width:500px;margin:auto">
    <h2>Admin Panel - APP_NAME</h2>
    <form method="POST" style="background:#1A2040;padding:15px;border-radius:12px;margin-top:15px">
    App Name: <input name="app_name" value="APP_NAME" style="width:100%;padding:8px;margin:5px 0"><br>
    Company Ad Taka: <input name="ad_c" value="AD_C" type="number" step="0.01"><br>
    Popup Ad Taka: <input name="ad_p" value="AD_P" type="number" step="0.01"><br>
    Company Limit: <input name="clim" value="CLIM" type="number"> Popup Limit: <input name="plim" value="PLIM" type="number"><br>
    Min Withdraw: <input name="min" value="MINW" type="number"> Refer Bonus: <input name="ref" value="REFB" type="number"><br>
    Monetag Direct Link: <input name="direct_link" value="DLINK" style="width:100%"><br>
    Sponsor Link: <input name="spon_link" value="SLINK" style="width:100%"><br>
    Notice: <textarea name="notice" style="width:100%;height:80px">NOTICE_TXT</textarea><br>
    <button style="width:100%;padding:12px;background:#8b5cf6;color:#fff;border:none;border-radius:8px;font-weight:800">Save - সব Admin থেকে কন্ট্রোল</button>
    </form>
    <p>Total Users: USERS_COUNT</p>
    </body>
    """
    html_admin = html_admin.replace("APP_NAME", s["app_name"])
    html_admin = html_admin.replace("AD_C", str(s["ad_c"]))
    html_admin = html_admin.replace("AD_P", str(s["ad_p"]))
    html_admin = html_admin.replace("CLIM", str(s["clim"]))
    html_admin = html_admin.replace("PLIM", str(s["plim"]))
    html_admin = html_admin.replace("MINW", str(s["min"]))
    html_admin = html_admin.replace("REFB", str(s["ref"]))
    html_admin = html_admin.replace("DLINK", s["direct_link"])
    html_admin = html_admin.replace("SLINK", s["spon_link"])
    html_admin = html_admin.replace("NOTICE_TXT", s["notice"])
    html_admin = html_admin.replace("USERS_COUNT", str(len(db["users"])))
    return html_admin

@app.route('/')
def home():
    db = load_db()
    s = db["settings"]

    tasks_html = ""
    for x in db.get("tasks", []):
        tasks_html = tasks_html + '<div class="list"><div><b>' + x["i"] + ' ' + x["t"] + '</b><br><small style="color:#22c55e">' + x["s"] + '</small></div><button class="go">Go</button></div>'

    html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}
.top{display:flex;gap:8px;padding:12px}
.ib{width:56px;height:56px;background:#151A2D;border:2px solid #8b5cf6;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:32px}
.tt{flex:1;background:#151A2D;border:1px solid #f59e0b;border-radius:14px;padding:10px;font-weight:700;font-size:13px}
.card{background:#1A2040;border:1px solid #1e293b;border-radius:22px;padding:18px;margin:12px}
.bal{color:#22c55e;font-size:40px;font-weight:900}
.list{background:#1A2040;border-radius:18px;padding:14px;margin:10px 12px;display:flex;justify-content:space-between;align-items:center}
.go{background:#8b5cf6;border:none;color:#fff;padding:10px 18px;border-radius:12px;font-weight:700}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;background:#8b5cf6;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:10px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b}
.btm div{flex:1;text-align:center;color:#64748b;font-size:12px;cursor:pointer}
.btm div.on{color:#8b5cf6}
.page{display:none}
.page.active{display:block}
.offer{background:#2D1B4E;border:2px solid #8b5cf6;border-radius:22px;padding:18px;margin:12px}
.notice{background:#1a1500;border:1px solid #f59e0b;border-radius:18px;padding:16px;margin:12px}
.faq{background:#0B0E1C;border-radius:14px;padding:12px;margin:8px 0}
</style></head><body>

<div id="p1" class="page active">
<div class="top"><div class="ib">💎</div><div class="tt">APP_NAME_TITLE<br>বিডি</div><div class="tt" style="border-color:#f59e0b">Daily Work BD ✅<br><span style="color:#22c55e">৳21.1</span></div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><span style="color:#a78bfa">💎 Diamond Member • Level 1</span><span>Balance<br><b style="color:#22c55e">৳21.1</b></span></div><div class="bal">৳21.1</div><div>💎 2110 Diamond | 2/80 Ads</div></div>
<div style="display:flex;gap:10px;margin:0 12px">
<div class="card" style="flex:1;margin:0"><b>Company Ads<br><span style="color:#f59e0b">AD_C_TK</span></b><br><small>1/80</small><br><button class="btn" onclick="doAd('c')">Start - AD_C_TK</button></div>
<div class="card" style="flex:1;margin:0"><b>Popup Ads<br><span style="color:#f59e0b">AD_P_TK</span></b><br><small>1/80</small><br><button class="btn" style="background:#f59e0b;color:#000" onclick="doAd('p')">Watch - AD_P_TK</button></div>
</div>
<div class="card"><b>💸 Withdraw</b><div style="display:flex;gap:8px;margin-top:10px"><button class="btn" style="flex:1">bKash</button><button class="btn" style="flex:1;background:#0B0E1C;border:1px solid #2a2f4a">Nagad</button></div><input placeholder="01XXXXXXXXX" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><input placeholder="Min MIN_TK" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><button class="btn" style="margin-top:10px">Withdraw Now</button></div>
<div class="offer"><h2>🔥🔥 Biggest Earning Offer</h2><p>প্রতিদিন কাজ করে আয় করুন, বড় বোনাস নিন</p><button class="btn" style="background:#f59e0b;color:#000;margin-top:10px" onclick="openSpon()">🚀 Claim Now</button></div>
</div>

<div id="p2" class="page">
<div class="top"><div class="ib">🎯</div><div class="tt">Tasks</div><div class="tt">Daily Work BD ✅</div></div>
<div class="card"><b>🎯 Tasks & Company Links</b><br><small>প্রতি Task এ ৳20-25 + Diamond</small></div>
TASKS_PLACE
<div class="offer"><h3>🔥 Special Offer</h3><small>এই বক্স Admin থেকে চেঞ্জ হবে</small><br><button class="btn" style="margin-top:10px" onclick="openSpon()">Claim Now</button></div>
</div>

<div id="p3" class="page">
<div class="top"><div class="ib">👥</div><div class="tt">Refer</div><div class="tt">Daily Work BD ✅</div></div>
<div style="background:#f59e0b;color:#000;padding:12px;border-radius:14px;margin:12px;font-weight:800;text-align:center">🎉🎉 Refer Contest চলছে! - ৳5000 পুরস্কার</div>
<div class="card"><b>👥 Refer & Earn</b><br><small>বন্ধুদের Invite করে Unlimited আয়</small><div style="display:flex;gap:10px;margin-top:10px"><div class="list" style="flex:1;flex-direction:column;margin:0"><b style="color:#8b5cf6;font-size:24px">0</b><small>Total Refer</small></div><div class="list" style="flex:1;flex-direction:column;margin:0"><b style="color:#22c55e;font-size:24px">REF_TK</b><small>Per Refer</small></div></div><div style="background:#0B0E1C;padding:10px;border-radius:10px;font-size:11px;margin-top:10px;word-break:break-all" id="refLink"></div><button class="btn" style="margin-top:10px" onclick="copyRef()">🔗 Copy Refer Link</button></div>
<div class="card" style="background:linear-gradient(135deg,#0a2e0a,#123e12);border-color:#22c55e"><b>🔥 Refer Special Bonus</b><br><small>Admin থেকে লিংক/অফার চেঞ্জ হবে</small><br><button class="btn" style="background:#22c55e;margin-top:10px">Join Now</button></div>
</div>

<div id="p4" class="page">
<div class="top"><div class="ib">💬</div><div class="tt">Support</div><div class="tt">Daily Work BD ✅</div></div>
<div class="card"><b>💎 Support Center</b><br><small>যেকোনো সমস্যায় যোগাযোগ করুন - 24/7</small></div>
<div class="card"><b>📞 Contact Us</b><div style="display:flex;gap:10px;margin:10px 0"><button class="btn" style="flex:1">✈️ Telegram</button><button class="btn" style="flex:1;background:#f59e0b;color:#000">💬 WhatsApp</button></div><div style="background:#0B0E1C;padding:10px;border-radius:10px">📧 support@dailyworkbd.com</div></div>
<div class="notice"><b>📢 Notice Board</b><br><div style="margin-top:8px">NOTICE_BOARD</div></div>
<div class="card"><b>❓ FAQ</b><div class="faq"><b>▶️ Withdraw কতক্ষণে পাবো?</b><br><small>২৪ ঘণ্টার ভিতরে পেমেন্ট করা হয়</small></div><div class="faq"><b>▶️ Refer টাকা কখন পাবো?</b><br><small>বন্ধু Join করলেই সাথে সাথে</small></div><div class="faq"><b>▶️ Ads দেখলে টাকা আসে না কেন?</b><br><small>VPN বন্ধ করে আবার চেষ্টা করুন</small></div></div>
<div class="card"><b>📜 Rules</b><div style="margin-top:8px;line-height:1.8">1. একাধিক একাউন্ট খুলবেন না<br>2. ভুল তথ্য দিবেন না<br>3. Fake Refer করবেন না<br>4. Admin এর সিদ্ধান্তই চূড়ান্ত</div></div>
</div>

<div id="p5" class="page">
<div class="top"><div class="ib">👤</div><div class="tt">Profile</div><div class="tt">Daily Work BD ✅ ৳21.1</div></div>
<div class="card" style="text-align:center"><div class="ib" style="width:90px;height:90px;margin:0 auto;font-size:48px">👤</div><br><span style="background:#f59e0b;color:#000;padding:4px 12px;border-radius:20px;font-weight:700;font-size:12px">Level 1</span><br><h2 style="margin-top:8px">User 4250</h2><small>Join: 2026-09-15</small><br><div style="margin-top:6px">💎 2110 Diamond | 21.1 Taka</div></div>
<div class="card"><b>📊 Statistics</b><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px"><div class="list" style="flex-direction:column;margin:0"><b style="color:#22c55e">৳21.1</b><small>Total Earned</small></div><div class="list" style="flex-direction:column;margin:0"><b style="color:#8b5cf6">৳21.1</b><small>Balance</small></div><div class="list" style="flex-direction:column;margin:0"><b style="color:#f59e0b">2</b><small>Ads</small></div><div class="list" style="flex-direction:column;margin:0"><b style="color:#ec4899">0</b><small>Refer</small></div></div></div>
<div class="card"><b>⚙️ Account - নাম/ছবি গ্যালারি থেকে</b><input id="nameInput" value="User 4250" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><input type="file" id="imgInput" style="margin-top:8px"><button class="btn" style="margin-top:10px" onclick="saveProfile()">💾 Save Profile</button></div>
<div class="card"><b>💸 Withdraw History</b><br><small>No withdraw</small></div>
</div>

<div class="btm">
<div class="on" id="b1" onclick="showPage(1)"><span>🏠</span>Home</div>
<div id="b2" onclick="showPage(2)"><span>🎯</span>Tasks</div>
<div id="b3" onclick="showPage(3)"><span>👥</span>Refer</div>
<div id="b4" onclick="showPage(4)"><span>💬</span>Support</div>
<div id="b5" onclick="showPage(5)"><span>👤</span>Profile</div>
</div>

<script>
var tg = window.Telegram.WebApp;
tg.expand();
var uid = "4250";
try { uid = String(tg.initDataUnsafe.user.id); } catch(e){}
var directLink = "DIRECT_LINK";
var sponLink = "SPON_LINK";
document.getElementById('refLink').innerText = "https://t.me/YourBot?start=" + uid;

function showPage(n){
  var pages = document.querySelectorAll('.page');
  for(var i=0;i<pages.length;i++){ pages[i].classList.remove('active'); }
  document.getElementById('p'+n).classList.add('active');
  var btns = document.querySelectorAll('.btm div');
  for(var i=0;i<btns.length;i++){ btns[i].classList.remove('on'); }
  document.getElementById('b'+n).classList.add('on');
}
function openSpon(){ window.open(sponLink, '_blank'); }
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Refer Link Copied'); }
function saveProfile(){ alert('Profile Saved - Admin Control এ Save হবে'); }
function doAd(t){
  window.open(directLink, '_blank');
  setTimeout(function(){
    fetch('/api/ads', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id:uid, type:t})})
   .then(function(r){ return r.json(); })
   .then(function(j){ alert(j.msg); location.reload(); });
  }, 2500);
}
</script></body></html>
    """
    html = html.replace("APP_NAME_TITLE", s["app_name"])
    html = html.replace("AD_C_TK", "৳" + str(s["ad_c"]))
    html = html.replace("AD_P_TK", "৳" + str(s["ad_p"]))
    html = html.replace("MIN_TK", str(s["min"]))
    html = html.replace("REF_TK", "৳" + str(s["ref"]))
    html = html.replace("DIRECT_LINK", s["direct_link"])
    html = html.replace("SPON_LINK", s["spon_link"])
    html = html.replace("NOTICE_BOARD", s["notice"].replace("\n", "<br>"))
    html = html.replace("TASKS_PLACE", tasks_html)
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
