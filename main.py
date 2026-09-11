from flask import Flask, request, jsonify
import json, os
from datetime import date, datetime
app = Flask(__name__)
DB_FILE="database.json"
DEFAULT_SETTINGS={"welcome":60,"ref":10,"ad":1,"limit":30,"min":200,"zone":"11764581","theme":"#0f766e","app_name":"প্রতিদিনের কাজ BD","logo":"https://cdn-icons-png.flaticon.com/512/5968/5968819.png","bot":"ProtidinerKaj_BD_Bot","channel":"ProtidinerKajBD","admin":"ProtidinerKajBD","admin_id":"8807178385"}

def load_db():
    if not os.path.exists(DB_FILE): return {"users":{},"withdraws":[],"settings":DEFAULT_SETTINGS}
    with open(DB_FILE,"r",encoding="utf-8") as f:
        db=json.load(f)
        if "settings" not in db: db["settings"]=DEFAULT_SETTINGS
        for k in DEFAULT_SETTINGS:
            if k not in db["settings"]: db["settings"][k]=DEFAULT_SETTINGS[k]
        return db
def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    db=load_db(); s=db["settings"]
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="https://telegram.org/js/telegram-web-app.js"></script><script src='//libtl.com/sdk.js' data-zone='{s['zone']}' data-sdk='show_{s['zone']}'></script><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"><style>body{{background:#eef7f6;font-family:sans-serif;margin:0;padding-bottom:80px}}.hd{{background:{s['theme']};color:white;padding:14px;display:flex;gap:12px}}.card{{background:white;border-radius:18px;margin:12px;padding:14px}}.big{{font-size:42px;font-weight:800;color:{s['theme']};text-align:center}}.dark{{background:#134e4a;color:white;border-radius:22px;margin:12px;padding:18px}}.green{{background:{s['theme']};color:white;border-radius:26px;margin:12px;padding:20px;text-align:center}}.btnG{{background:{s['theme']};color:white;border:none;padding:13px;border-radius:12px;width:100%;font-weight:800}}.btnW{{background:white;color:{s['theme']};border:none;padding:14px;border-radius:14px;width:100%;font-weight:800}}.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #e2e8f0}}.bi{{text-align:center;color:#94a3b8;font-size:11px;flex:1}}.bi.active{{color:{s['theme']}}}.page{{display:none}}.page.active{{display:block}}.input{{width:100%;padding:12px;border:1px solid #e2e8f0;border-radius:12px;margin:6px 0}}</style></head><body>
<div class="hd"><b>{s['app_name']}</b></div>
<div id="home" class="page active"><div class="card"><div class="big">৳<span id="b1">0</span></div></div><div class="card"><div id="rl" style="background:#f8fafc;border:1px solid #e2e8f0;padding:10px;border-radius:10px;font-size:12px"></div><button class="btnG" style="margin-top:10px" onclick="navigator.clipboard.writeText(document.getElementById('rl').innerText)">🔗 রেফার লিংক কপি</button></div><div class="dark"><b>📢 অফিশিয়াল নোটিশ</b><br><br>💸 রেফারে {s['ref']} টাকা<br>📺 Ads এ {s['ad']} টাকা<br>🎁 বোনাস {s['welcome']} টাকা<br>🏦 উইথড্র {s['min']} টাকা</div></div>
<div id="earn" class="page"><div class="green"><div>প্রতি Ads এ আয়</div><div style="font-size:48px;font-weight:800">৳{s['ad']}.00</div><button class="btnW" onclick="watchAd()" style="margin-top:12px">▶ বিজ্ঞাপন দেখুন (<span id="left">{s['limit']}</span> বাকি)</button></div></div>
<div id="support" class="page"><div class="card"><b>Admin: @{s['admin']}</b><br>Channel: @{s['channel']}</div></div>
<div id="withdraw" class="page"><div class="card"><input id="num" class="input" placeholder="Number"><input id="amt" class="input" placeholder="Amount"><button class="btnG" onclick="wd()">উইথড্র</button></div></div>
<div class="bottom"><div class="bi active" onclick="showP('home',this)"><i class="fa-solid fa-house"></i>হোম</div><div class="bi" onclick="showP('earn',this)"><i class="fa-solid fa-coins"></i>আয়</div><div class="bi" onclick="showP('support',this)"><i class="fa-solid fa-headset"></i>সাপোর্ট</div><div class="bi" onclick="showP('withdraw',this)"><i class="fa-solid fa-wallet"></i>উইথড্র</div></div>
<script>
let UID=Telegram.WebApp.initDataUnsafe?.user?.id||"8807178385";
function showP(id,el){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.bi').forEach(b=>b.classList.remove('active'));el.classList.add('active')}}
async function load(){{let r=await fetch('/api/settings');let s=await r.json();let r2=await fetch('/api/user?id='+UID);let u=await r2.json();document.getElementById('b1').innerText=u.bal;document.getElementById('left').innerText=s.limit-u.today;document.getElementById('rl').innerText='https://t.me/'+s.bot+'?start='+UID;}}
async function watchAd(){{if(typeof show_{s['zone']}!=='function')return alert('Ad লোড হচ্ছে');await show_{s['zone']}();let r=await fetch('/api/ad',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:UID}})}});let j=await r.json();alert(j.msg);load();}}
async function wd(){{let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:UID,number:document.getElementById('num').value,amount:document.getElementById('amt').value}})}});let j=await r.json();alert(j.msg);}}
load();
</script></body></html>"""

@app.route("/api/settings")
def get_settings():
    db=load_db(); return jsonify({**db["settings"],"today":0})

@app.route("/api/user")
def get_user():
    db=load_db(); uid=str(request.args.get("id","0")); t=str(date.today())
    if uid not in db["users"]: db["users"][uid]={"bal":db["settings"]["welcome"],"today":0,"total":0}
    if db["users"][uid].get("date")!=t: db["users"][uid]["today"]=0; db["users"][uid]["date"]=t
    save_db(db); u=db["users"][uid]; return jsonify({"bal":u["bal"],"today":u["today"],"total":u["total"]})

@app.route("/api/register",methods=["POST"])
def reg():
    db=load_db(); data=request.json or {}; uid=str(data.get("id") or request.args.get("id") or "0")
    if uid not in db["users"]: db["users"][uid]={"bal":db["settings"]["welcome"],"today":0,"total":0,"date":str(date.today())}
    save_db(db); return jsonify({"ok":True})

@app.route("/api/ad",methods=["POST"])
def ad():
    db=load_db(); uid=str(request.json.get("id")); u=db["users"].get(uid)
    if not u: return jsonify({"msg":"User not found"})
    if u["today"]>=db["settings"]["limit"]: return jsonify({"msg":f"আজ {db['settings']['limit']}টা শেষ"})
    u["today"]+=1; u["total"]+=1; u["bal"]+=db["settings"]["ad"]; save_db(db)
    return jsonify({"msg":f"৳{db['settings']['ad']} যোগ হয়েছে!"})

@app.route("/api/withdraw",methods=["POST"])
def withdraw():
    db=load_db(); d=request.json; uid=str(d.get("id")); u=db["users"].get(uid)
    amt=float(d.get("amount",0))
    if amt<db["settings"]["min"]: return jsonify({"msg":f"মিনিমাম {db['settings']['min']} টাকা"})
    if u["bal"]<amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["bal"]-=amt; db["withdraws"].append({"id":uid,"num":d.get("number"),"amt":amt,"time":str(datetime.now())}); save_db(db)
    return jsonify({"msg":"উইথড্র সফল!"})

@app.route("/admin")
def admin():
    db=load_db(); s=db["settings"]
    if request.args.get("id")!=s["admin_id"]: return "Unauthorized - তোমার ID ভুল"
    return f"""
    <html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{font-family:sans-serif;padding:20px;background:#f8fafc}}.card{{background:white;padding:16px;border-radius:12px;margin:10px 0}} input{{width:100%;padding:10px;margin:6px 0;border:1px solid #e2e8f0;border-radius:8px}} button{{background:#0f766e;color:white;border:none;padding:12px;width:100%;border-radius:10px;font-weight:800}}</style></head><body>
    <h2>⚙️ এডমিন কন্ট্রোল - {s['app_name']}</h2>
    <div class="card"><h3>💰 টাকার সেটিংস</h3>
    <label>Welcome Bonus (এখন {s['welcome']}):</label><input id="welcome" type="number" value="{s['welcome']}">
    <label>Per Ad Reward (এখন {s['ad']}):</label><input id="ad" type="number" value="{s['ad']}">
    <label>Refer Bonus (এখন {s['ref']}):</label><input id="ref" type="number" value="{s['ref']}">
    <label>Daily Ad Limit (এখন {s['limit']}):</label><input id="limit" type="number" value="{s['limit']}">
    <label>Min Withdraw (এখন {s['min']}):</label><input id="min" type="number" value="{s['min']}">
    </div>
    <div class="card"><h3>🎨 ডিজাইন ও লোগো</h3>
    <label>App Name:</label><input id="app_name" value="{s['app_name']}">
    <label>Logo URL:</label><input id="logo" value="{s['logo']}">
    <label>Theme Color:</label><input id="theme" value="{s['theme']}">
    <label>Monetag Zone ID (এখন {s['zone']}):</label><input id="zone" value="{s['zone']}">
    <label>Bot Username:</label><input id="bot" value="{s['bot']}">
    </div>
    <button onclick="save()">💾 Save Settings - সবকিছু আপডেট করুন</button>
    <div class="card"><h3>📊 ইউজার: {len(db['users'])} জন | উইথড্র: {len(db['withdraws'])} টা</h3><pre>{json.dumps(db['withdraws'][-10:],ensure_ascii=False,indent=2)}</pre></div>
    <script>
    async function save(){{
        let data={{welcome:parseInt(document.getElementById('welcome').value),ad:parseInt(document.getElementById('ad').value),ref:parseInt(document.getElementById('ref').value),limit:parseInt(document.getElementById('limit').value),min:parseInt(document.getElementById('min').value),app_name:document.getElementById('app_name').value,logo:document.getElementById('logo').value,theme:document.getElementById('theme').value,zone:document.getElementById('zone').value,bot:document.getElementById('bot').value}};
        let r=await fetch('/api/admin/save?id={s['admin_id']}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}});
        let j=await r.json(); alert(j.msg);
    }}
    </script></body></html>
    """

@app.route("/api/admin/save",methods=["POST"])
def admin_save():
    db=load_db()
    if request.args.get("id")!=db["settings"]["admin_id"]: return jsonify({"msg":"Unauthorized"})
    d=request.json
    for k in d: db["settings"][k]=d[k]
    save_db(db); return jsonify({"msg":"✅ সফল! সবকিছু আপডেট হয়েছে - পেছনের ডাটা ঠিক আছে!"})

if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
