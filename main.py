from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "settings": {"app_name": "প্রতিদিনের কাজ বিডি", "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 30, "min": 500}, "wds": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users": {}, "settings": {"app_name": "প্রতিদিনের কাজ বিডি", "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 30, "min": 500}, "wds": []}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin', '*')
    r.headers.add('Access-Control-Allow-Headers', '*')
    r.headers.add('Access-Control-Allow-Methods', '*')
    return r

@app.route('/')
def home():
    db = load_db()
    s = db["settings"]
    ad = s.get("ad", 0.25)
    pop = s.get("pop", 0.20)
    clim = s.get("clim", 30)
    plim = s.get("plim", 50)

    html = f"""
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}
body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}}
.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}}
.top2{{display:flex;gap:10px;margin:12px;align-items:center}}
.topbox{{flex:1;background:#151A2D;border:1px solid #8b5cf6;padding:12px;border-radius:14px;font-weight:700;font-size:14px}}
.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:#8b5cf6;cursor:pointer;margin-top:10px;font-size:16px}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:22px;display:block}}
.page{{display:none}}.page.active{{display:block}}
</style>
</head>
<body>
<div id="p1" class="page active">
<div class="top2"><div class="topbox">👑 {s.get('app_name','Daily Work BD')}<br>✅ <span id="bal">৳0</span></div><div style="width:58px;height:58px;background:#1A2040;border:2px solid #8b5cf6;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:34px">💎</div></div>
<div class="glass">💎 Diamond Member • Level 1<br><b>Balance <span id="bal2">৳0</span></b> | <span id="diamond">0</span> Diamond | <span id="ads">0</span>/{clim+plim} Ads</div>
<div class="glass">Company Ads ৳{ad} <span id="cads">0</span>/{clim} <button class="btn" onclick="watchAd()">Start - ৳{ad}</button></div>
<div class="glass">Popup Ads ৳{pop} <span id="pads">0</span>/{plim} <button class="btn" style="background:#f59e0b;color:#000" onclick="watchPop()">Watch - ৳{pop}</button></div>
<div class="glass">💸 Withdraw<br><button class="btn" style="background:#22c55e" onclick="goWd()">Withdraw Now</button></div>
<div class="glass" style="background:linear-gradient(135deg,#2D1B4E,#1A1033);border-color:#f59e0b">🔥 Biggest Earning Offer<br>প্রতিদিন কাজ করে আয় করুন, বড় বোনাস নিন<br><button class="btn" style="background:#f59e0b;color:#000" onclick="window.open('https://google.com')">🚀 Claim Now</button></div>
</div>
<div id="p2" class="page"><div class="glass">🎯 Tasks<br>প্রতি Task এ ৳20-25 + Diamond</div><div class="glass">🌐 Visit Website - ৳20 <button class="btn" onclick="doTask(0.2)">Start</button></div></div>
<div id="p3" class="page"><div class="glass">👥 Refer & Earn<br><b id="refLink" style="font-size:12px;word-break:break-all"></b><br><button class="btn" onclick="copyRef()">Copy Link</button></div></div>
<div id="p4" class="page"><div class="glass">💸 Withdraw<br><div style="display:flex;gap:8px"><div id="m1" class="topbox" style="text-align:center;cursor:pointer" onclick="setM('bKash')">bKash</div><div id="m2" class="topbox" style="text-align:center;cursor:pointer" onclick="setM('Nagad')">Nagad</div></div><input id="acc" placeholder="Number" style="width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px"><button class="btn" onclick="doWithdraw()">Withdraw Now</button></div></div>
<div id="p5" class="page"><div class="glass">📥 Inbox Help<br>1. প্রতিদিন {clim+plim} টা Ads<br>2. 12 ঘন্টা পর Ads Reset<br>3. টাকা Safe থাকবে<br>4. Withdraw 24h এর মধ্যে<br>5. Support: t.me/dailyworkbd</div></div>
<div class="btm">
<div class="on" onclick="showP(1,this)"><span>🏠</span>Home</div>
<div onclick="showP(2,this)"><span>🎯</span>Tasks</div>
<div onclick="showP(3,this)"><span>👥</span>Refer</div>
<div onclick="showP(4,this)"><span>💸</span>Withdraw</div>
<div onclick="showP(5,this)"><span>📥</span>Inbox</div>
</div>
<script>
let tg=window.Telegram.WebApp;tg.expand();
let uid=String(tg.initDataUnsafe?.user?.id||"12345");
let method="bKash";
document.getElementById('refLink').innerText="https://t.me/YourBot?start="+uid;
function showP(n,e){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p'+n).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));e.classList.add('on');}}
function setM(m){{method=m;document.getElementById('m1').style.borderColor=m=='bKash'?'#8b5cf6':'#1e293b';document.getElementById('m2').style.borderColor=m=='Nagad'?'#8b5cf6':'#1e293b';}}
async function loadBal(){{
 try{{let r=await fetch('/api/balance?uid='+uid);let j=await r.json();document.getElementById('bal').innerText='৳'+j.balance;document.getElementById('bal2').innerText='৳'+j.balance;document.getElementById('ads').innerText=j.ads;document.getElementById('cads').innerText=j.ads;}}catch(e){{}}
}}
async function watchAd(){{
 window.open('https://www.profitablecpmrate.com/v2iyv02n?key=8a0f68d9fb7d1d9d05d5e6c6e8e8c6e8','_blank');
 setTimeout(async()=>{{let r=await fetch('/api/watch',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{uid:uid,type:'company'}})}});let j=await r.json();if(j.error)alert('Limit Done');else{{alert('৳{ad} Added');loadBal();}}}},3000);
}}
async function watchPop(){{
 window.open('https://www.profitablecpmrate.com/v2iyv02n?key=8a0f68d9fb7d1d9d05d5e6c6e8e8c6e8','_blank');
 setTimeout(async()=>{{let r=await fetch('/api/watch',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{uid:uid,type:'pop'}})}});let j=await r.json();if(j.error)alert('Limit Done');else{{alert('৳{pop} Added');loadBal();}}}},3000);
}}
function doTask(v){{watchAd();}}
function goWd(){{showP(4,document.querySelectorAll('.btm div')[3]);}}
async function doWithdraw(){{
 let acc=document.getElementById('acc').value;if(!acc){{alert('Number দাও');return;}}
 let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{uid:uid,amount:document.getElementById('bal').innerText.replace('৳',''),method:method,account:acc}})}});
 alert('Withdraw Request Done');
}}
function copyRef(){{navigator.clipboard.writeText(document.getElementById('refLink').innerText);alert('Copied');}}
loadBal();setM('bKash');
</script>
</body>
</html>
    """
    return html

@app.route('/api/balance')
def bal():
    db=load_db(); uid=str(request.args.get("uid","0"))
    u=db["users"].get(uid, {"balance":0,"ads":0})
    return jsonify(u)

@app.route('/api/watch', methods=["POST","OPTIONS"])
def watch():
    if request.method=="OPTIONS": return jsonify({})
    db=load_db(); data=request.json; uid=str(data.get("uid","0"))
    user=db["users"].setdefault(uid, {"balance":0,"ads":0})
    if user.get("ads",0)>=80: return jsonify({"error":"limit"}),400
    # company 0.25 pop 0.20
    inc = 0.25 if data.get("type")=="company" else 0.20
    user["balance"]=round(user.get("balance",0)+inc,2)
    user["ads"]=user.get("ads",0)+1
    save_db(db)
    return jsonify(user)

@app.route('/api/withdraw', methods=["POST","OPTIONS"])
def wd():
    if request.method=="OPTIONS": return jsonify({})
    db=load_db(); d=request.json
    db.setdefault("wds",[]).append({"uid":str(d.get("uid")),"amount":d.get("amount"),"method":d.get("method"),"account":d.get("account"),"time":str(datetime.now())})
    save_db(db)
    return jsonify({"success":True})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
