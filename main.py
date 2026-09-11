from flask import Flask, request, jsonify
import json, os
from datetime import date, datetime
app = Flask(__name__)
DB_FILE="database.json"
S={"welcome":60,"ref":10,"ad":1,"limit":30,"min":200,"zone":"11764581","theme":"#0f766e","name":"প্রতিদিনের কাজ BD","logo":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","bot":"ProtidinerKaj_BD_Bot","channel":"ProtidinerKajBD","admin":"ProtidinerKajBD","admin_id":"8807178385"}

def load_db():
    if not os.path.exists(DB_FILE): return {"users":{},"wds":[],"s":S}
    with open(DB_FILE,"r",encoding="utf-8") as f:
        db=json.load(f); db["s"]=S; return db
def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)

@app.route("/")
def index():
    s=S
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='{s["zone"]}' data-sdk='show_{s["zone"]}'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:Hind Siliguri,sans-serif}}body{{background:#eaf6f5;padding-bottom:90px}}
.top{{background:{s["theme"]};color:white;padding:14px 16px;font-weight:700;font-size:18px}}
.card{{background:white;border-radius:18px;margin:12px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.big{{font-size:44px;font-weight:900;color:{s["theme"]};text-align:center}}
.dark{{background:#134e4a;color:white;border-radius:22px;margin:12px;padding:18px}}
.green{{background:{s["theme"]};color:white;border-radius:26px;margin:12px;padding:20px;text-align:center}}
.btnG{{background:{s["theme"]};color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:800;font-size:16px}}
.btnW{{background:white;color:{s["theme"]};border:none;padding:14px;border-radius:16px;width:100%;font-weight:900;font-size:16px}}
.stat{{display:flex;gap:10px;margin:14px 0}}.st{{flex:1;background:rgba(255,255,255,.18);border-radius:14px;padding:12px}}
.row{{display:flex;justify-content:space-between;align-items:center}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #e5e7eb;z-index:99}}
.bi{{text-align:center;color:#94a3b8;font-size:12px;flex:1;cursor:pointer}}.bi.active{{color:{s["theme"]}}}.bi i{{font-size:20px;display:block;margin-bottom:3px}}
.page{{display:none}}.page.active{{display:block}}.input{{width:100%;padding:14px;border:1px solid #e2e8f0;border-radius:14px;background:#f8fafc;margin:7px 0}}
</style></head><body>
<div class="top">{s["name"]}</div>

<!-- HOME - তোমার ১নং ছবির মতো -->
<div id="home" class="page active">
<div class="card"><div class="big">৳<span id="b1">62</span></div></div>
<div class="card"><div style="display:flex;gap:8px"><div id="rl" style="flex:1;background:#f1f5f9;border:1px solid #e2e8f0;padding:12px;border-radius:12px;font-size:13px;overflow:hidden">https://t.me/{s["bot"]}?start=8807178385</div><button onclick="copyR()" style="border:1px solid #e2e8f0;background:white;border-radius:10px;padding:0 14px">📋</button></div><button class="btnG" style="margin-top:12px" onclick="copyR()">🔗 রেফার লিংক কপি</button></div>
<div class="dark"><div style="font-size:18px;font-weight:800">📢 অফিশিয়াল নোটিশ</div><div style="margin-top:14px;line-height:2;font-size:16px">💸 রেফারে {s["ref"]} টাকা<br>📺 Ads এ {s["ad"]} টাকা<br>🎁 বোনাস {s["welcome"]} টাকা<br>🏦 উইথড্র {s["min"]} টাকা</div></div>
</div>

<!-- EARN - তোমার ২নং ছবির মতো -->
<div id="earn" class="page">
<div class="green"><div style="font-size:16px">প্রতি Ads এ আয়</div><div style="font-size:56px;font-weight:900">৳{s["ad"]}.00</div><div class="stat"><div class="st"><div>আজ দেখা</div><b style="font-size:20px"><span id="tdc">2</span> টি</b></div><div class="st"><div>আজ আয়</div><b style="font-size:20px">৳<span id="tdi">2</span></b></div></div><button class="btnW" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন (<span id="left">28</span> বাকি)</button></div>
<div class="card row"><div style="display:flex;gap:12px;align-items:center"><div style="width:50px;height:50px;background:#fee2e2;border-radius:14px;display:flex;align-items:center;justify-content:center;color:red;font-size:22px"><i class="fa-brands fa-youtube"></i></div><div><b>YouTube ভিডিও</b><br><b style="color:{s["theme"]}">৳25.00</b></div></div><button class="btnG" style="width:auto;padding:10px 18px">শুরু করুন</button></div>
<div class="card row"><div style="display:flex;gap:12px;align-items:center"><div style="width:50px;height:50px;background:#e0f2fe;border-radius:14px;display:flex;align-items:center;justify-content:center;color:#0284c7;font-size:22px"><i class="fa-brands fa-telegram"></i></div><div><b>Join Telegram</b><br><b style="color:{s["theme"]}">৳10.00</b></div></div><button class="btnG" style="width:auto;padding:10px 18px">শুরু করুন</button></div>
</div>

<!-- SUPPORT - তোমার ৩নং ছবির মতো ভরা -->
<div id="support" class="page">
<div class="card row" style="background:#eef2ff"><div style="display:flex;gap:12px;align-items:center"><div style="width:52px;height:52px;background:#3b82f6;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white;font-size:24px"><i class="fa-brands fa-telegram"></i></div><div><b>Admin কে Message করুন</b><br><small>@{s["admin"]}</small></div></div><i class="fa-solid fa-arrow-right" style="color:{s["theme"]}"></i></div>
<div class="card row" style="background:#eef2ff"><div style="display:flex;gap:12px;align-items:center"><div style="width:52px;height:52px;background:#3b82f6;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white;font-size:24px"><i class="fa-brands fa-telegram"></i></div><div><b>অফিশিয়াল চ্যানেল</b><br><small>@{s["channel"]}</small></div></div><i class="fa-solid fa-arrow-right" style="color:{s["theme"]}"></i></div>
<div class="card row" style="background:#dc2626;color:white"><div style="display:flex;gap:12px;align-items:center"><div style="width:52px;height:52px;background:#f59e0b;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white">▶</div><div><b>কিভাবে কাজ করবেন?</b><br><small>ভিডিও দেখুন</small></div></div><i class="fa-solid fa-arrow-right"></i></div>
</div>

<!-- WITHDRAW - তোমার ৪নং ছবির মতো -->
<div id="withdraw" class="page">
<div class="card"><div class="big">৳<span id="b2">62</span></div><div style="text-align:center;color:#64748b">বর্তমান ব্যালেন্স</div>
<div style="display:flex;gap:10px;margin:12px 0"><div id="bk" class="input" style="text-align:center;font-weight:800;cursor:pointer;border:2px solid {s["theme"]}" onclick="sel('bkash')">Bkash</div><div id="ng" class="input" style="text-align:center;font-weight:800;cursor:pointer" onclick="sel('nagad')">Nagad</div></div>
<input id="num" class="input" placeholder="Number - 01XXXXXXXXX"><input id="amt" class="input" placeholder="Amount - Min {s["min"]} টাকা"><button class="btnG" onclick="wd()">উইথড্র</button></div>
</div>

<div class="bottom"><div class="bi active" onclick="showP('home',this)"><i class="fa-solid fa-house"></i>হোম</div><div class="bi" onclick="showP('earn',this)"><i class="fa-solid fa-coins"></i>আয়</div><div class="bi" onclick="showP('support',this)"><i class="fa-solid fa-headset"></i>সাপোর্ট</div><div class="bi" onclick="showP('withdraw',this)"><i class="fa-solid fa-wallet"></i>উইথড্র</div></div>

<script>
let UID=Telegram.WebApp.initDataUnsafe?.user?.id||"8807178385"; let METHOD="bkash";
function showP(id,el){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.bi').forEach(b=>b.classList.remove('active'));el.classList.add('active')}}
function copyR(){{navigator.clipboard.writeText(document.getElementById('rl').innerText);alert('লিংক কপি হয়েছে!')}}
function sel(m){{METHOD=m;document.getElementById('bk').style.border='1px solid #e2e8f0';document.getElementById('ng').style.border='1px solid #e2e8f0';document.getElementById(m=='bkash'?'bk':'ng').style.border='2px solid {s["theme"]}'}}
async function load(){{try{{let r=await fetch('/api/user?id='+UID);let j=await r.json();document.getElementById('b1').innerText=j.bal;document.getElementById('b2').innerText=j.bal;document.getElementById('tdc').innerText=j.today;document.getElementById('tdi').innerText=j.today*{s["ad"]};document.getElementById('left').innerText={s["limit"]}-j.today;document.getElementById('rl').innerText='https://t.me/{s["bot"]}?start='+UID;}}catch(e){{}}}}
async function watchAd(){{if(typeof show_{s["zone"]}==='function'){{try{{await show_{s["zone"]}();}}catch(e){{}}}} let r=await fetch('/api/ad',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:UID}})}});let j=await r.json();alert(j.msg);load();}}
async function wd(){{let n=document.getElementById('num').value;let a=document.getElementById('amt').value;if(!n||!a)return alert('সব লেখো');let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:UID,number:n,amount:a,method:METHOD}})}});let j=await r.json();alert(j.msg);load();}}
load();
</script></body></html>"""

@app.route("/api/user")
def api_user():
    db=load_db(); uid=str(request.args.get("id","0")); t=str(date.today())
    if uid not in db["users"]: db["users"][uid]={"bal":S["welcome"],"today":0,"total":0,"date":t}
    u=db["users"][uid]
    if u.get("date")!=t: u["today"]=0; u["date"]=t
    save_db(db); return jsonify({"bal":u["bal"],"today":u["today"],"total":u["total"]})

@app.route("/api/ad",methods=["POST"])
def api_ad():
    db=load_db(); uid=str(request.json.get("id")); u=db["users"].get(uid)
    if not u: return jsonify({"msg":"User পাওয়া যায়নি"})
    if u["today"]>=S["limit"]: return jsonify({"msg":f"আজ {S['limit']}টা শেষ!"})
    u["today"]+=1; u["total"]+=1; u["bal"]+=S["ad"]; save_db(db)
    return jsonify({"msg":f"৳{S['ad']} যোগ হয়েছে!"})

@app.route("/api/withdraw",methods=["POST"])
def api_wd():
    db=load_db(); d=request.json; uid=str(d.get("id")); u=db["users"].get(uid)
    amt=float(d.get("amount",0))
    if amt<S["min"]: return jsonify({"msg":f"মিনিমাম {S['min']} টাকা!"})
    if u["bal"]<amt: return jsonify({"msg":"ব্যালেন্স কম!"})
    u["bal"]-=amt; db["wds"].append(d); save_db(db)
    return jsonify({"msg":"উইথড্র রিকোয়েস্ট সফল!"})

@app.route("/admin")
def admin():
    db=load_db()
    if request.args.get("id")!=S["admin_id"]: return "Unauthorized"
    s=S; return f"<h2>Admin Panel</h2><p>Users: {len(db['users'])}</p><pre>{json.dumps(db['wds'][-20:],ensure_ascii=False,indent=2)}</pre>"

if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
