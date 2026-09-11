from flask import Flask, request, jsonify
import json, os
from datetime import date
app = Flask(__name__)
DB_FILE="database.json"
S={"name":"প্রতিদিনের কাজ BD","theme":"#0f766e","welcome":60,"ref":10,"ad":1,"limit":30,"min":200,"zone":"11764581","logo":"https://cdn-icons-png.flaticon.com/512/5968/5968819.png","bot":"ProtidinerKaj_BD_Bot","channel":"ProtidinerKajBD","admin":"ProtidinerKajBD"}

def load_db():
    if not os.path.exists(DB_FILE): return {"users":{},"wd":[],"s":S}
    with open(DB_FILE,"r",encoding="utf-8") as f:
        db=json.load(f); db["s"]=S; return db
def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)
def get_u(db,uid):
    uid=str(uid); t=str(date.today())
    if uid not in db["users"]: db["users"][uid]={"bal":S["welcome"],"today":0,"total":0,"tk":0,"d":t,"name":"USER"}
    u=db["users"][uid]
    if u["d"]!=t: u["today"]=0; u["tk"]=0; u["d"]=t
    return u

@app.route("/")
def idx():
    s=S
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='{s['zone']}' data-sdk='show_{s['zone']}'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}}body{{background:#eef7f6;padding-bottom:80px}}
.hd{{background:{s['theme']};color:white;padding:14px;display:flex;gap:12px;align-items:center}}.av{{width:48px;height:48px;background:white;border-radius:50%;overflow:hidden}}
.card{{background:white;border-radius:18px;margin:12px;padding:14px}}.big{{font-size:42px;font-weight:800;color:{s['theme']};text-align:center}}
.dark{{background:#134e4a;color:white;border-radius:22px;margin:12px;padding:18px}}.green{{background:{s['theme']};color:white;border-radius:26px;margin:12px;padding:20px;text-align:center}}
.btnG{{background:{s['theme']};color:white;border:none;padding:13px;border-radius:12px;width:100%;font-weight:800}}.btnW{{background:white;color:{s['theme']};border:none;padding:14px;border-radius:14px;width:100%;font-weight:800}}
.bottom{{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #e2e8f0}}.bi{{text-align:center;color:#94a3b8;font-size:11px;flex:1}}.bi.active{{color:{s['theme']}}}.bi i{{font-size:20px;display:block}}.page{{display:none}}.page.active{{display:block}}.input{{width:100%;padding:14px;border:1px solid #e2e8f0;border-radius:14px;background:#f8fafc;margin:6px 0}}</style></head><body>
<div class="hd"><div class="av"><img src="{s['logo']}" width="100%"></div><div><b id="uname">USER</b> <i class="fa-solid fa-circle-check" style="color:#5eead4"></i><br>৳<span id="hbal">60.00</span></div></div>
<div id="home" class="page active"><div class="card"><div class="big">৳<span id="b1">60.00</span></div></div>
<div class="card"><small>আপনার রেফারাল লিংক:</small><div style="display:flex;gap:8px;margin-top:8px"><div id="rl" style="flex:1;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px;font-size:12px">https://t.me/{s['bot']}?start=123</div><button onclick="navigator.clipboard.writeText(document.getElementById('rl').innerText)">📋</button></div><button class="btnG" style="margin-top:12px">🔗 রেফার লিংক শেয়ার করুন</button></div>
<div class="dark"><b>📢 অফিশিয়াল নোটিশ</b><div style="font-size:13px;line-height:1.8;margin-top:10px">✨ আমাদের প্ল্যাটফর্মে ইনকাম করা এখন আগের চেয়ে আরও সহজ।<br>💸 প্রতিটি রেফারে পাবেন {s['ref']} টাকা।<br>📺 প্রতিটি বিজ্ঞাপন দেখলে পাবেন {s['ad']} টাকা।<br>🎁 একাউন্ট খুললেই {s['welcome']} টাকা বোনাস।<br>🏦 {s['min']} টাকা হলেই উইথড্র।</div></div></div>
<div id="earn" class="page"><div class="green"><div>প্রতি বিজ্ঞাপনে নিশ্চিত আয়</div><div style="font-size:48px;font-weight:800">৳{s['ad']}.00</div>
<div style="display:flex;gap:10px;margin:12px 0"><div style="flex:1;background:rgba(255,255,255,.18);border-radius:14px;padding:12px"><div>আজ দেখা</div><b><span id="tdc">0</span> টি</b></div><div style="flex:1;background:rgba(255,255,255,.18);border-radius:14px;padding:12px"><div>আজ আয়</div><b>৳<span id="tdi">0</span></b></div></div>
<button class="btnW" onclick="watchAd()">▶ বিজ্ঞাপন শুরু করুন (<span id="left">{s['limit']}</span> টি বাকি | আজ <span id="tdc2">0</span>/{s['limit']})</button></div>
<div class="card" style="display:flex;justify-content:space-between"><div style="display:flex;gap:10px"><div style="width:48px;height:48px;background:#fee2e2;border-radius:12px;display:flex;align-items:center;justify-content:center;color:red"><i class="fa-brands fa-youtube"></i></div><div><b>YouTube video</b><br><b>৳25.00</b></div></div><button class="btnG" style="width:auto">শুরু করুন</button></div>
<div class="card" style="display:flex;justify-content:space-between"><div style="display:flex;gap:10px"><div style="width:48px;height:48px;background:#e0f2fe;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#0284c7"><i class="fa-solid fa-paper-plane"></i></div><div><b>Join telegram</b><br><b>৳10.00</b></div></div><button class="btnG" style="width:auto">শুরু করুন</button></div></div>
<div id="support" class="page"><div class="card" style="display:flex;justify-content:space-between"><div style="display:flex;gap:12px"><div style="width:52px;height:52px;background:#3b82f6;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white"><i class="fa-brands fa-telegram"></i></div><div><b>Admin কে Message করুন</b><br><small>@{s['admin']}</small></div></div>→</div>
<div class="card" style="display:flex;justify-content:space-between"><div style="display:flex;gap:12px"><div style="width:52px;height:52px;background:#3b82f6;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white"><i class="fa-brands fa-telegram"></i></div><div><b>অফিশিয়াল চ্যানেল</b><br><small>@{s['channel']}</small></div></div>→</div></div>
<div id="withdraw" class="page"><div class="card"><div class="big">৳<span id="b2">60.00</span></div><div style="text-align:center;color:#64748b">বর্তমান ব্যালেন্স</div>
<input id="num" class="input" placeholder="Bkash/Nagad Number"><input id="amt" class="input" placeholder="পরিমাণ"><button class="btnG" onclick="wd()">উইথড্র করুন</button></div></div>
<div id="profile" class="page"><div class="card" style="text-align:center"><div class="av" style="width:70px;height:70px;margin:auto"><img src="{s['logo']}" width="100%"></div><b id="pname">USER</b><br>৳<span id="pb">60.00</span><br><small>মোট Ads: <span id="pt">0</span> | Joined: আজ</small></div></div>
<div class="bottom"><div class="bi active" onclick="showP('home',this)"><i class="fa-solid fa-house"></i>হোম</div><div class="bi" onclick="showP('earn',this)"><i class="fa-solid fa-coins"></i>আয় করুন</div><div class="bi" onclick="showP('support',this)"><i class="fa-solid fa-headset"></i>সাপোর্ট</div><div class="bi" onclick="showP('withdraw',this)"><i class="fa-solid fa-wallet"></i>উইথড্র</div><div class="bi" onclick="showP('profile',this)"><i class="fa-solid fa-user"></i>প্রোফাইল</div></div>
<script>
let UID=Telegram.WebApp.initDataUnsafe?.user?.id || "8807178385"; let METHOD="bkash";
function showP(id,el){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.bi').forEach(b=>b.classList.remove('active'));el.classList.add('active')}}
async function load(){{let r=await fetch('/api/user?id='+UID);let j=await r.json();document.getElementById('hbal').innerText=j.bal.toFixed(2);document.getElementById('b1').innerText=j.bal.toFixed(2);document.getElementById('b2').innerText=j.bal.toFixed(2);document.getElementById('pb').innerText=j.bal.toFixed(2);document.getElementById('tdc').innerText=j.today;document.getElementById('tdc2').innerText=j.today;document.getElementById('left').innerText={s['limit']}-j.today;document.getElementById('tdi').innerText=j.tk;document.getElementById('pt').innerText=j.total;document.getElementById('rl').innerText='https://t.me/{s['bot']}?start='+UID;}}
async function watchAd(){{if(typeof show_{s['zone']}!=='function'){{alert('Ad লোড হচ্ছে...');return}}try{{await show_{s['zone']}();let r=await fetch('/api/ad',{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:UID}})});let j=await r.json();if(j.ok){{alert('৳{s['ad']} যোগ হয়েছে!');load()}}else{{alert(j.msg)}}}}catch(e){{alert('Ads দেখা হয়নি')}}}}
async function wd(){{let n=document.getElementById('num').value;let a=document.getElementById('amt').value;if(!n||!a){{alert('সব পূরণ করুন');return}}let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:UID,number:n,amount:a,method:METHOD}})}});let j=await r.json();alert(j.msg);load()}}
load();
</script></body></html>"""

@app.route("/api/user")
def api_user():
    db=load_db(); u=get_u(db,request.args.get("id","0")); save_db(db)
    return jsonify({"bal":u["bal"],"today":u["today"],"total":u["total"],"tk":u["tk"]})

@app.route("/api/ad",methods=["POST"])
def api_ad():
    db=load_db(); d=request.json; u=get_u(db,d.get("id"))
    if u["today"]>=S["limit"]: return jsonify({"ok":False,"msg":f"আজ {S['limit']} টা শেষ!"})
    u["today"]+=1; u["total"]+=1; u["bal"]+=S["ad"]; u["tk"]+=S["ad"]; save_db(db)
    return jsonify({"ok":True})

@app.route("/api/withdraw",methods=["POST"])
def api_wd():
    db=load_db(); d=request.json; u=get_u(db,d.get("id")); amt=float(d.get("amount",0))
    if amt<S["min"]: return jsonify({"msg":f"মিনিমাম {S['min']} টাকা!"})
    if u["bal"]<amt: return jsonify({"msg":"ব্যালেন্স কম!"})
    u["bal"]-=amt; db["wd"].append({"id":d.get("id"),"num":d.get("number"),"amt":amt,"date":str(datetime.now())}); save_db(db)
    return jsonify({"msg":"উইথড্র রিকোয়েস্ট পাঠানো হয়েছে!"})

@app.route("/admin")
def admin():
    db=load_db();
    if request.args.get("id")!=S["zone"] and request.args.get("id")!="8807178385": return "Unauthorized"
    return f"<h2>Admin - Total Users: {len(db['users'])} - Withdraws: {len(db['wd'])}</h2><pre>{json.dumps(db,ensure_ascii=False,indent=2)}</pre>"

if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
