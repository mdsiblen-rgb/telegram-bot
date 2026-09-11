# main.py - FINAL WITH LINK EDIT
from flask import Flask, request, jsonify
import json, os
from datetime import date
app = Flask(__name__)
DB="database.json"
SET={
 "welcome":60,"ref":10,"ad":1,"limit":30,"min":200,"yt":25,"tg":10,
 "zone":"11764581","theme":"#0f766e","name":"প্রতিদিনের কাজ BD",
 "bot":"ProtidinerKaj_BD_Bot","channel":"ProtidinerKajBD","admin":"ProtidinerKajBD","admin_id":"8807178385",
 "yt_link":"https://youtube.com/@ProtidinerKajBD",
 "channel_link":"https://t.me/ProtidinerKajBD",
 "admin_link":"https://t.me/ProtidinerKajBD",
 "video_link":"https://t.me/ProtidinerKajBD",
 "notice":"প্রতিদিন ১০+ রিয়েল কাজ"
}
def load():
    if not os.path.exists(DB): return {"users":{},"wds":[],"s":SET}
    try:
        with open(DB,"r",encoding="utf-8") as f: d=json.load(f)
        if "s" not in d: d["s"]=SET
        for k in SET:
            if k not in d["s"]: d["s"][k]=SET[k]
        return d
    except: return {"users":{},"wds":[],"s":SET}
def save(d):
    with open(DB,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    db=load(); s=db["s"]
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='"""+s["zone"]+"""' data-sdk='show_"""+s["zone"]+"""'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<style>body{background:#eaf6f5;padding-bottom:90px}*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}.top{background:"""+s["theme"]+""";color:#fff;padding:14px;display:flex;justify-content:space-between;font-weight:800}.card{background:#fff;border-radius:18px;margin:12px;padding:14px}.big{font-size:42px;font-weight:900;color:"""+s["theme"]+""";text-align:center}.green{background:"""+s["theme"]+""";color:#fff;border-radius:22px;margin:12px;padding:20px;text-align:center}.btnG{background:"""+s["theme"]+""";color:#fff;border:none;padding:12px 16px;border-radius:12px;font-weight:800;cursor:pointer}.btnW{background:#fff;color:"""+s["theme"]+""";border:none;padding:12px;border-radius:14px;width:100%;font-weight:900}.bottom{position:fixed;bottom:0;left:0;right:0;background:#fff;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #eee}.bi{flex:1;text-align:center;color:#94a3b8;font-size:11px;cursor:pointer}.bi.active{color:"""+s["theme"]+"""}.page{display:none}.page.active{display:block}.scard{display:flex;justify-content:space-between;align-items:center;padding:14px;border:1px solid #eee;border-radius:16px;margin:10px;background:#fff;cursor:pointer}</style></head><body>
<div class="top"><span>"""+s["name"]+"""</span><span id="hbal">৳0</span></div>
<div id="p_home" class="page active"><div class="card"><div class="big">৳<span id="b1">0</span></div></div></div>
<div id="p_earn" class="page"><div class="green"><div>প্রতি Ads এ ৳"""+str(s["ad"])+"""</div><div style="font-size:48px;font-weight:900">৳"""+str(s["ad"])+"""</div><button class="btnW" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button></div>
<div class="scard" onclick="openLink('"""+s["yt_link"]+"""','yt')"><div><b>YouTube ভিডিও</b><br>৳"""+str(s["yt"])+"""</div><button class="btnG">শুরু করুন</button></div>
<div class="scard" onclick="openLink('"""+s["channel_link"]+"""','tg')"><div><b>Join Telegram</b><br>৳"""+str(s["tg"])+"""</div><button class="btnG">Join</button></div></div>
<div id="p_support" class="page">
<div class="scard" onclick="openLink('"""+s["admin_link"]+"""')"><div><b>Admin Message</b><br>"""+s["admin"]+"""</div><b>→</b></div>
<div class="scard" onclick="openLink('"""+s["channel_link"]+"""')"><div><b>অফিশিয়াল চ্যানেল</b><br>"""+s["channel"]+"""</div><b>→</b></div>
<div class="scard" style="background:#dc2626;color:#fff" onclick="openLink('"""+s["video_link"]+"""')"><div><b>কিভাবে কাজ করবেন?</b></div><b>→</b></div></div>
<div id="p_withdraw" class="page"><div class="card"><div class="big">৳<span id="b2">0</span></div><button class="btnG" style="width:100%" onclick="wd()">উইথড্র</button></div></div>
<div class="bottom"><div class="bi active" onclick="showP('p_home',this)"><i class="fa-solid fa-house"></i><br>হোম</div><div class="bi" onclick="showP('p_earn',this)"><i class="fa-solid fa-coins"></i><br>আয়</div><div class="bi" onclick="showP('p_support',this)"><i class="fa-solid fa-headset"></i><br>সাপোর্ট</div><div class="bi" onclick="showP('p_withdraw',this)"><i class="fa-solid fa-wallet"></i><br>উইথড্র</div></div>
<script>
let UID=Telegram.WebApp.initDataUnsafe?.user?.id||"8807178385";
function showP(id,el){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.bi').forEach(b=>b.classList.remove('active'));el.classList.add('active')}
function openLink(url,type){window.open(url,'_blank'); if(type){setTimeout(async()=>{let r=await fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:UID,type:type})});let j=await r.json();alert(j.msg);load();},1500);}}
async function load(){let r=await fetch('/api/user?id='+UID);let j=await r.json();document.getElementById('b1').innerText=j.bal;document.getElementById('b2').innerText=j.bal;document.getElementById('hbal').innerText='৳'+j.bal;}
async function watchAd(){try{if(typeof show_"""+s["zone"]+"""==='function'){await show_"""+s["zone"]+"""();}}catch(e){}let r=await fetch('/api/ad',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:UID})});let j=await r.json();alert(j.msg);load();}
async function wd(){let r=await fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:UID,number:'01',amount:'200'})});let j=await r.json();alert(j.msg);}
load();
</script></body></html>
"""
@app.route("/api/user")
def api_user():
    db=load(); uid=str(request.args.get("id","0")); t=str(date.today())
    if uid not in db["users"]: db["users"][uid]={"bal":db["s"]["welcome"],"today":0,"date":t,"tasks":[]}
    u=db["users"][uid]
    if u.get("date")!=t: u["today"]=0; u["date"]=t
    save(db); return jsonify({"bal":u["bal"],"today":u["today"]})
@app.route("/api/ad",methods=["POST"])
def api_ad():
    db=load(); uid=str(request.json.get("id")); u=db["users"].get(uid)
    if u["today"]>=db["s"]["limit"]: return jsonify({"msg":"আজ শেষ"})
    u["today"]+=1; u["bal"]+=db["s"]["ad"]; save(db); return jsonify({"msg":"৳"+str(db["s"]["ad"])+" যোগ হয়েছে"})
@app.route("/api/task",methods=["POST"])
def api_task():
    db=load(); d=request.json; uid=str(d.get("id")); typ=d.get("type"); u=db["users"].get(uid)
    if typ in u.get("tasks",[]): return jsonify({"msg":"আগেই করেছেন"})
    rw=db["s"]["yt"] if typ=="yt" else db["s"]["tg"]
    u["bal"]+=rw; u["tasks"].append(typ); save(db); return jsonify({"msg":"৳"+str(rw)+" পেয়েছেন"})
@app.route("/api/withdraw",methods=["POST"])
def api_wd():
    db=load(); d=request.json; uid=str(d.get("id")); u=db["users"].get(uid)
    try: amt=float(d.get("amount",200))
    except: amt=200
    if u["bal"]<amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["bal"]-=amt; db["wds"].append(d); save(db); return jsonify({"msg":"উইথড্র সফল"})
@app.route("/admin")
def admin():
    db=load(); s=db["s"]
    if request.args.get("id")!=s["admin_id"]: return "Unauthorized id=8807178385 দাও"
    return """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;padding:12px;background:#f0fdfa}.card{background:#fff;padding:16px;border-radius:14px;margin:12px 0}input{width:100%;padding:12px;margin:6px 0;border:1px solid #ddd;border-radius:10px}button{background:"""+s["theme"]+""";color:#fff;border:none;padding:14px;width:100%;border-radius:12px;font-weight:800;margin-top:10px}</style></head><body>
<h2>🔗 লিংক এডিট - কোম্পানি এডমিন</h2>
<div class="card"><h3>🎥 লিংক সেটিংস - এখানে বসালেই অ্যাপসে কাজ করবে</h3>
YouTube Video Link:<input id="yt_link" value='"""+s["yt_link"]+"""' placeholder="https://youtube.com/...">
Channel Link:<input id="channel_link" value='"""+s["channel_link"]+"""' placeholder="https://t.me/ProtidinerKajBD">
Admin Message Link:<input id="admin_link" value='"""+s["admin_link"]+"""' placeholder="https://t.me/ProtidinerKajBD">
Tutorial Video Link:<input id="video_link" value='"""+s["video_link"]+"""' placeholder="https://t.me/ProtidinerKajBD"><br>
App Name:<input id="name" value='"""+s["name"]+"""'>
Monetag Zone ID:<input id="zone" value='"""+s["zone"]+"""'>
Per Ad:<input id="ad" value='"""+str(s["ad"])+"""'>
YouTube Reward:<input id="yt" value='"""+str(s["yt"])+"""'>
Telegram Reward:<input id="tg" value='"""+str(s["tg"])+"""'>
<button onclick="saveL()">💾 SAVE - সব লিংক আপডেট করুন</button>
</div>
<script>
async function saveL(){
let data={
yt_link:document.getElementById('yt_link').value,
channel_link:document.getElementById('channel_link').value,
admin_link:document.getElementById('admin_link').value,
video_link:document.getElementById('video_link').value,
name:document.getElementById('name').value,
zone:document.getElementById('zone').value,
ad:parseInt(document.getElementById('ad').value),
yt:parseInt(document.getElementById('yt').value),
tg:parseInt(document.getElementById('tg').value)
};
let r=await fetch('/api/admin/save?id="""+s["admin_id"]+"""',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
let j=await r.json(); alert(j.msg); location.reload();
}
</script></body></html>"""
@app.route("/api/admin/save",methods=["POST"])
def save_admin():
    db=load()
    if request.args.get("id")!=db["s"]["admin_id"]: return jsonify({"msg":"Unauthorized"})
    d=request.json
    for k in d: db["s"][k]=d[k]
    save(db); return jsonify({"msg":"✅ সব লিংক সেট হয়েছে! এখন অ্যাপসে গিয়ে টেস্ট করো"})

if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
