import os, json, time
from flask import Flask, request, jsonify
app = Flask(__name__)
DB = "database.json"

def load_db():
    if not os.path.exists(DB):
        d = {
            "users": {}, "wds": [],
            "settings": {
                "app_name": "প্রতিদিনের কাজ বিডি",
                "ad": 0.5, "pop": 0.3, "clim": 80, "plim": 80, "min": 200, "ref": 20,
                "direct_link": "https://omg10.com/4/11760259",
                "spon_link": "https://google.com",
                "notice": "রাত ১০টার পর Withdraw বন্ধ"
            },
            "tasks": [
                {"t": "Visit Company Website - 20Tk", "s": "0.2Tk", "i": "🌐"},
                {"t": "Watch Video - 25Tk", "s": "0.25Tk", "i": "▶️"}
            ]
        }
        open(DB, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
        return d
    return json.load(open(DB, "r", encoding="utf-8"))

def save_db(db):
    open(DB, "w", encoding="utf-8").write(json.dumps(db, ensure_ascii=False, indent=2))

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "name": "User 4250", "bal": 21.1, "diamonds": 2110, "c": 2, "p": 1}
    return db["users"][uid]

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin', '*')
    return r

@app.route('/api/init', methods=['POST'])
def api_init():
    db = load_db()
    data = request.json or {}
    uid = str(data.get('id', '0'))
    u = get_user(db, uid)
    save_db(db)
    return jsonify({"user": u, "s": db["settings"]})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    db = load_db()
    data = request.json or {}
    uid = str(data.get('id', '0'))
    typ = data.get('type', 'c')
    u = get_user(db, uid)
    s = db["settings"]
    if typ == 'c':
        if u["c"] >= s["clim"]:
            return jsonify({"msg": "Limit sesh"})
        u["c"] = u["c"] + 1
        u["bal"] = round(u["bal"] + float(s["ad"]), 2)
    else:
        if u["p"] >= s["plim"]:
            return jsonify({"msg": "Limit sesh"})
        u["p"] = u["p"] + 1
        u["bal"] = round(u["bal"] + float(s["pop"]), 2)
    save_db(db)
    return jsonify({"msg": "Taka Added", "bal": u["bal"]})

@app.route('/')
def index():
    db = load_db()
    s = db["settings"]
    # NO F-STRING - SAFE
    html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:110px}
.top{display:flex;gap:8px;padding:12px}
.ib{width:56px;height:56px;background:#151A2D;border:2px solid #8b5cf6;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:32px}
.tt{flex:1;background:#151A2D;border:1px solid #f59e0b;border-radius:14px;padding:10px;font-weight:700;font-size:13px}
.card{background:#1A2040;border:1px solid #1e293b;border-radius:22px;padding:18px;margin:12px}
.bal{color:#22c55e;font-size:40px;font-weight:900}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;background:#8b5cf6;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:10px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b}
.btm div{flex:1;text-align:center;color:#64748b;font-size:12px;cursor:pointer}
.btm div.on{color:#8b5cf6}
.page{display:none}.page.active{display:block}
.list{background:#1A2040;border-radius:18px;padding:14px;margin:10px 12px;display:flex;justify-content:space-between;align-items:center}
.offer{background:#2D1B4E;border:2px solid #8b5cf6;border-radius:22px;padding:18px;margin:12px}
</style></head><body>

<div id="p1" class="page active">
<div class="top"><div class="ib">💎</div><div class="tt">👑 প্রতিদিনের কাজ<br>বিডি</div><div class="tt">Daily Work BD ✅<br><span style="color:#22c55e">৳21.1</span></div></div>
<div class="card"><div>Diamond Member • Level 1</div><div class="bal">৳21.1</div><div>💎 2110 Diamond | 2/80 Ads</div></div>
<div style="display:flex;gap:10px;margin:0 12px">
<div class="card" style="flex:1;margin:0"><b>Company Ads<br><span style="color:#f59e0b">৳0.5</span></b><br><small>1/80</small><br><button class="btn" onclick="doAd('c')">Start - ৳0.5</button></div>
<div class="card" style="flex:1;margin:0"><b>Popup Ads<br><span style="color:#f59e0b">৳0.3</span></b><br><small>1/80</small><br><button class="btn" style="background:#f59e0b;color:#000" onclick="doAd('p')">Watch - ৳0.3</button></div>
</div>
<div class="card"><b>💸 Withdraw</b><br><button class="btn" style="margin-top:10px" onclick="show(4)">Withdraw Now</button></div>
<div class="offer"><h2>🔥🔥 Biggest Earning Offer</h2><p>প্রতিদিন কাজ করে আয় করুন</p><button class="btn" style="background:#f59e0b;color:#000;margin-top:10px" onclick="openLink()">🚀 Claim Now</button></div>
</div>

<div id="p2" class="page"><div class="top"><div class="ib">🎯</div><div class="tt">Tasks</div><div class="tt">Daily Work BD</div></div><div class="card"><b>🎯 Tasks & Company Links</b></div><div class="list"><div>🌐 Visit Company Website - 20Tk</div><button style="background:#8b5cf6;color:#fff;padding:8px 14px;border:none;border-radius:10px">Go</button></div></div>

<div id="p3" class="page"><div class="top"><div class="ib">👥</div><div class="tt">Refer</div><div class="tt">Daily Work BD</div></div><div style="background:#f59e0b;color:#000;padding:12px;border-radius:14px;margin:12px;font-weight:800;text-align:center">🎉🎉 Refer Contest চলছে! - 5000 পুরস্কার</div><div class="card"><b>👥 Refer & Earn</b><div id="refLink" style="background:#0B0E1C;padding:10px;border-radius:10px;font-size:11px;margin-top:8px;word-break:break-all"></div><button class="btn" style="margin-top:10px" onclick="copyRef()">Copy Link</button></div></div>

<div id="p4" class="page"><div class="top"><div class="ib">💬</div><div class="tt">Support</div><div class="tt">Daily Work BD</div></div><div class="card"><b>💎 Support Center</b></div><div class="card"><b>📢 Notice Board</b><br>রাত ১০টার পর Withdraw বন্ধ<br>সকাল ৯টায় চালু<br>Fake Account ব্যান</div><div class="card"><b>❓ FAQ</b><br>Withdraw ২৪ ঘণ্টা<br>Refer সাথে সাথে</div></div>

<div id="p5" class="page"><div class="top"><div class="ib">👤</div><div class="tt">Profile</div><div class="tt">Daily Work BD ৳21.1</div></div><div class="card" style="text-align:center"><div class="ib" style="width:90px;height:90px;margin:0 auto;font-size:48px">👤</div><br><h2>User 4250</h2><div>💎 2110 Diamond</div></div><div class="card"><b>Account - নাম/ছবি</b><input id="nameIn" placeholder="নতুন নাম" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><input type="file" style="margin-top:8px"><button class="btn" style="margin-top:10px">Save Profile</button></div></div>

<div class="btm">
<div class="on" onclick="show(1);setOn(this)"><span>🏠</span>Home</div>
<div onclick="show(2);setOn(this)"><span>🎯</span>Tasks</div>
<div onclick="show(3);setOn(this)"><span>👥</span>Refer</div>
<div onclick="show(4);setOn(this)"><span>💬</span>Support</div>
<div onclick="show(5);setOn(this)"><span>👤</span>Profile</div>
</div>

<script>
var tg = window.Telegram.WebApp; tg.expand();
var uid = String(tg.initDataUnsafe && tg.initDataUnsafe.user? tg.initDataUnsafe.user.id : "4250");
document.getElementById('refLink').innerText = "https://t.me/YourBot?start=" + uid;
function show(n){ var pages = document.querySelectorAll('.page'); for(var i=0;i<pages.length;i++){ pages[i].classList.remove('active'); } document.getElementById('p'+n).classList.add('active'); }
function setOn(el){ var btns = document.querySelectorAll('.btm div'); for(var i=0;i<btns.length;i++){ btns[i].classList.remove('on'); } el.classList.add('on'); }
function openLink(){ window.open('DIRECT_LINK_PLACEHOLDER','_blank'); }
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied'); }
async function doAd(t){
  window.open('DIRECT_LINK_PLACEHOLDER','_blank');
  setTimeout(async function(){
    var r = await fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})});
    var j = await r.json(); alert(j.msg);
  },2000);
}
</script></body></html>
"""
    html = html.replace("DIRECT_LINK_PLACEHOLDER", s["direct_link"])
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
