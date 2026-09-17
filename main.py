import os, json, time
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"

def load_db():
    try:
        if not os.path.exists(DB_FILE):
            data = {
                "users": {},
                "wds": [],
                "settings": {
                    "app_name": "প্রতিদিনের কাজ বিডি",
                    "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 30, "min": 500, "ref": 15,
                    "direct_link": "https://omg10.com/4/11760259",
                    "spon_title": "🔥 আজকের সেরা অফার",
                    "spon_desc": "প্রতিদিন 500 টাকা ইনকাম করুন",
                    "spon_btn": "Claim Now", "spon_link": "https://google.com",
                    "notice": "রাত 10টার পর Withdraw বন্ধ"
                },
                "tasks": []
            }
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return data
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users": {}, "wds": [], "settings": {"app_name": "প্রতিদিনের কাজ বিডি", "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 30, "min": 500, "ref": 15, "direct_link": "https://omg10.com/4/11760259", "spon_title": "অফার", "spon_desc": "ইনকাম করুন", "spon_btn": "Claim", "spon_link": "https://google.com", "notice": "Notice"}, "tasks": []}

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except: pass

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "name": "User " + uid[-4:], "bal": 20.0, "c": 0, "p": 0, "diamonds": 2000, "refl": [], "img": "", "date": time.strftime("%Y-%m-%d")}
    # reset daily
    if db["users"][uid].get("date")!= time.strftime("%Y-%m-%d"):
        db["users"][uid]["c"] = 0
        db["users"][uid]["p"] = 0
        db["users"][uid]["date"] = time.strftime("%Y-%m-%d")
    return db["users"][uid]

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin', '*')
    r.headers.add('Access-Control-Allow-Headers', '*')
    r.headers.add('Access-Control-Allow-Methods', '*')
    return r

@app.route('/api/init', methods=['POST'])
def init_api():
    try:
        db = load_db()
        uid = str((request.json or {}).get('id', '0'))
        u = get_user(db, uid)
        save_db(db)
        return jsonify({"user": u, "s": db["settings"]})
    except Exception as e:
        return jsonify({"user": {"bal": 0, "c": 0, "p": 0, "diamonds": 0, "name": "User"}, "s": load_db()["settings"]})

@app.route('/api/ads', methods=['POST'])
def ads_api():
    try:
        db = load_db()
        j = request.json or {}
        uid = str(j.get('id', '0'))
        typ = j.get('type', 'c')
        u = get_user(db, uid)
        s = db["settings"]
        if typ == 'c':
            if u["c"] >= s["clim"]:
                return jsonify({"msg": "আজকের লিমিট শেষ"})
            u["c"] += 1
            u["bal"] = round(u["bal"] + float(s["ad"]), 2)
            u["diamonds"] += 25
        else:
            if u["p"] >= s["plim"]:
                return jsonify({"msg": "আজকের লিমিট শেষ"})
            u["p"] += 1
            u["bal"] = round(u["bal"] + float(s["pop"]), 2)
            u["diamonds"] += 20
        save_db(db)
        return jsonify({"msg": "টাকা যোগ হয়েছে", "bal": u["bal"]})
    except Exception as e:
        return jsonify({"msg": "Error"})

@app.route('/')
def home():
    db = load_db()
    s = db["settings"]
    # No f-string - safe HTML
    html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}
.glass{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:16px;margin:12px}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:#8b5cf6;cursor:pointer;margin-top:10px}
.btn2{background:#f59e0b;color:#000}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:10px 0 16px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b}
.btm div{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}
.btm div.on{color:#8b5cf6}
.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
</style></head><body>
<div id="p1" class="page active">
<div class="glass">APP_NAME - Balance: <span id="bal">0</span> | Diamonds: <span id="diam">0</span></div>
<div class="glass">Company Ads - RATE_C <span id="c_t">0/CLIM</span><button class="btn" onclick="doAd('c')">Start - RATE_C</button></div>
<div class="glass">Popup Ads - RATE_P <span id="p_t">0/PLIM</span><button class="btn btn2" onclick="doAd('p')">Watch - RATE_P</button></div>
<div class="glass">NOTICE_TEXT<br><br>Withdraw - Min MIN Tk<br><button class="btn" style="background:#22c55e" onclick="go(4)">Withdraw Now</button></div>
<div class="glass" style="background:linear-gradient(135deg,#2D1B4E,#1A1033);border-color:#f59e0b"><b>SPON_TITLE</b><br>SPON_DESC<br><button class="btn btn2" onclick="window.open('SPON_LINK','_blank')">SPON_BTN</button></div>
</div>
<div id="p2" class="page"><div class="glass"><b>🎯 Tasks</b><br>Task complete করে বোনাস নিন</div><div class="glass">📢 Join Telegram - ৳2<button class="btn" onclick="window.open('https://t.me/','_blank')">Start</button></div></div>
<div id="p3" class="page"><div class="glass"><b>👥 Refer & Earn</b><br>প্রতি রেফারে 15 টাকা<br><div id="refLink" style="background:#0B0E1C;padding:10px;border-radius:10px;font-size:12px;margin-top:8px;word-break:break-all"></div><button class="btn" onclick="copyRef()">Copy Link</button></div></div>
<div id="p4" class="page"><div class="glass"><b>💸 Withdraw</b><br><input id="acc" placeholder="bKash/Nagad Number" style="width:100%;padding:12px;border-radius:10px;background:#0B0E1C;color:#fff;border:1px solid #2a2f4a;margin-top:8px"><input id="amt" placeholder="Amount" type="number" style="width:100%;padding:12px;border-radius:10px;background:#0B0E1C;color:#fff;border:1px solid #2a2f4a;margin-top:8px"><button class="btn" style="background:#22c55e" onclick="alert('Withdraw Request Done')">Withdraw</button></div></div>
<div id="p5" class="page"><div class="glass" style="text-align:center"><div style="width:80px;height:80px;background:#0B0E1C;border:2px solid #8b5cf6;border-radius:18px;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:36px">👤</div><br><b id="pName">User</b><br><input id="newName" placeholder="নতুন নাম" style="width:100%;padding:10px;border-radius:10px;background:#0B0E1C;color:#fff;border:1px solid #2a2f4a;margin-top:8px"><input type="file" id="imgIn" style="margin-top:8px"><button class="btn" onclick="alert('Profile Saved')">Save Profile</button></div><div class="glass"><b>📥 Inbox Help</b><br>1. দিনে CLIM+PLIM টা Ads<br>2. 12 ঘন্টা পর Reset<br>3. Withdraw 24h<br>4. Support: t.me/</div></div>
<div class="btm">
<div class="on" onclick="go(1);this.className='on';clr(this)"><span>🏠</span>Home</div>
<div onclick="go(2);clr(this)"><span>🎯</span>Tasks</div>
<div onclick="go(3);clr(this)"><span>👥</span>Refer</div>
<div onclick="go(4);clr(this)"><span>💸</span>Withdraw</div>
<div onclick="go(5);clr(this)"><span>📥</span>Inbox</div>
</div>
<script>
let tg=window.Telegram.WebApp;tg.expand();
let uid=String(tg.initDataUnsafe?.user?.id||"12345");
document.getElementById('refLink').innerText="https://t.me/YourBot?start="+uid;
function go(n){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p'+n).classList.add('active');}
function clr(el){document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));el.classList.add('on');}
async function init(){try{let r=await fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})});let j=await r.json();document.getElementById('bal').innerText='৳'+j.user.bal;document.getElementById('diam').innerText=j.user.diamonds;document.getElementById('c_t').innerText=j.user.c+'/CLIM';document.getElementById('p_t').innerText=j.user.p+'/PLIM';document.getElementById('pName').innerText=j.user.name;}catch(e){}}
async function doAd(t){window.open('DIRECT_LINK','_blank');setTimeout(async()=>{let r=await fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})});let j=await r.json();alert(j.msg);init();},3000);}
function copyRef(){navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('Copied');}
init();
</script></body></html>
    """
    html = html.replace("APP_NAME", s["app_name"])
    html = html.replace("RATE_C", str(s["ad"])).replace("RATE_P", str(s["pop"]))
    html = html.replace("CLIM", str(s["clim"])).replace("PLIM", str(s["plim"]))
    html = html.replace("MIN", str(s["min"]))
    html = html.replace("SPON_TITLE", s["spon_title"]).replace("SPON_DESC", s["spon_desc"]).replace("SPON_BTN", s["spon_btn"]).replace("SPON_LINK", s["spon_link"])
    html = html.replace("DIRECT_LINK", s["direct_link"])
    html = html.replace("NOTICE_TEXT", s["notice"])
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
