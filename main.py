from flask import Flask, request, jsonify
import json, os
from datetime import date, datetime
app = Flask(__name__)
DB_FILE="database.json"
DEFAULT={"welcome":60,"ref":10,"ad":1,"limit":30,"min":200,"yt":25,"tg":10,"zone":"11764581","theme":"#0f766e","name":"প্রতিদিনের কাজ BD","logo":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","bot":"ProtidinerKaj_BD_Bot","channel":"ProtidinerKajBD","admin":"ProtidinerKajBD","admin_id":"8807178385","notice":"রেফারে 10 টাকা | Ads এ 1 টাকা | বোনাস 60 টাকা | উইথড্র 200 টাকা"}

def load_db():
    if not os.path.exists(DB_FILE): return {"users":{},"wds":[],"s":DEFAULT}
    try:
        with open(DB_FILE,"r",encoding="utf-8") as f:
            db=json.load(f)
            if "s" not in db: db["s"]=DEFAULT
            for k in DEFAULT:
                if k not in db["s"]: db["s"][k]=DEFAULT[k]
            return db
    except: return {"users":{},"wds":[],"s":DEFAULT}

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)

@app.route("/")
def index():
    db=load_db(); s=db["s"]
    th=s["theme"]; zn=s["zone"]; nm=s["name"]; bt=s["bot"]; ch=s["channel"]; ad=s["admin"]
    ad_reward=s["ad"]; lim=s["limit"]; yt=s["yt"]; tg=s["tg"]; notice=s["notice"]; mn=s["min"]; ref=s["ref"]; wel=s["welcome"]

    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='//libtl.com/sdk.js' data-zone='"""+zn+"""' data-sdk='show_"""+zn+"""'></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#eaf6f5;padding-bottom:90px}
.top{background:"""+th+""";color:white;padding:14px 16px;font-weight:700;font-size:18px;display:flex;justify-content:space-between}
.card{background:white;border-radius:18px;margin:12px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.big{font-size:44px;font-weight:900;color:"""+th+""";text-align:center}
.dark{background:#134e4a;color:white;border-radius:22px;margin:12px;padding:18px}
.green{background:"""+th+""";color:white;border-radius:26px;margin:12px;padding:20px;text-align:center}
.btnG{background:"""+th+""";color:white;border:none;padding:14px;border-radius:14px;width:100%;font-weight:800;font-size:15px;cursor:pointer}
.btnW{background:white;color:"""+th+""";border:none;padding:14px;border-radius:16px;width:100%;font-weight:900;cursor:pointer}
.bottom{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #e2e8f0;z-index:99}
.bi{text-align:center;color:#94a3b8;font-size:11px;flex:1;cursor:pointer}.bi.active{color:"""+th+"""}.page{display:none}.page.active{display:block}
.input{width:100%;padding:14px;border:1px solid #e2e8f0;border-radius:14px;background:#f8fafc;margin:7px 0}
.scard{border:1px solid #e2e8f0;border-radius:14px;padding:12px;margin:8px 0;display:flex;justify-content:space-between;align-items:center;cursor:pointer}
</style></head><body>
<div class="top"><span>"""+nm+"""</span><span id="hbal2">৳0</span></div>

<div id="home" class="page active">
<div class="card"><div class="big">৳<span id="b1">"""+str(wel)+"""</span></div><div style="text-align:center;color:#64748b">বর্তমান ব্যালেন্স</div></div>
<div class="card"><div style="display:flex;gap:8px"><div id="rl" style="flex:1;background:#f1f5f9;border:1px solid #e2e8f0;padding:12px;border-radius:12px;font-size:12px;word-break:break-all">https://t.me/"""+bt+"""?start=123</div><button onclick="copyR()" style="border:none;background:"""+th+""";color:white;border-radius:10px;padding:0 14px">📋</button></div>
<div style="display:flex;gap:8px;margin-top:12px"><button class="btnG" onclick="copyR()">🔗 কপি করুন</button><button class="btnG" style="background:#25D366" onclick="shareR()">📤 শেয়ার</button></div></div>
<div class="dark"><div style="font-weight:800">📢 অফিশিয়াল নোটিশ</div><div style="margin-top:10px;line-height:1.8">"""+notice+"""<br>💸 রেফার: """+str(ref)+"""৳ | 📺 Ads: """+str(ad_reward)+"""৳ | 🎁 বোনাস: """+str(wel)+"""৳ | 🏦 উইথড্র: """+str(mn)+"""৳</div></div>
</div>

<div id="earn" class="page">
<div class="green"><div>প্রতি বিজ্ঞাপনে নিশ্চিত আয়</div><div style="font-size:52px;font-weight:900">৳"""+str(ad_reward)+""".00</div>
<div style="display:flex;gap:10px;margin:14px 0"><div style="flex:1;background:rgba(255,255,255,.18);border-radius:14px;padding:12px"><div>আজ দেখা</div><b><span id="tdc">0</span> টি</b></div><div style="flex:1;background:rgba(255,255,255,.18);border-radius:14px;padding:12px"><div>আজ আয়</div><b>৳<span id="tdi">0</span></b></div></div>
<button class="btnW" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন (<span id="left">"""+str(lim)+"""</span> বাকি)</button>
<div style="font-size:12px;margin-top:8px">আজ <span id="tdc2">0</span>/"""+str(lim)+""" টা দেখেছেন</div></div>
<div class="card scard" onclick="doTask('yt')"><div style="display:flex;gap:12px;align-items:center"><div style="width:48px;height:48px;background:#fee2e2;border-radius:12px;display:flex;align-items:center;justify-content:center;color:red"><i class="fa-brands fa-youtube"></i></div><div><b>YouTube ভিডিও দেখুন</b><br><b style="color:"""+th+"""">৳"""+str(yt)+"""</b></div></div><button class="btnG" style="width:auto;padding:10px 16px">শুরু করুন</button></div>
<div class="card scard" onclick="doTask('tg')"><div style="display:flex;gap:12px;align-items:center"><div style="width:48px;height:48px;background:#e0f2fe;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#0284c7"><i class="fa-brands fa-telegram"></i></div><div><b>Join Telegram Channel</b><br><b style="color:"""+th+"""">৳"""+str(tg)+"""</b></div></div><button class="btnG" style="width:auto;padding:10px 16px">Join</button></div>
</div>

<div id="support" class="page">
<div class="card scard" onclick="openTg('"""+ad+"""')"><div style="display:flex;gap:12px;align-items:center"><div style="width:52px;height:52px;background:#3b82f6;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white;font-size:22px"><i class="fa-brands fa-telegram"></i></div><div><b>Admin কে Message করুন</b><br><small>@"""+ad+"""</small></div></div><i class="fa-solid fa-arrow-right"></i></div>
<div class="card scard" onclick="openTg('"""+ch+"""')"><div style="display:flex;gap:12px;align-items:center"><div style="width:52px;height:52px;background:#3b82f6;border-radius:16px;display:flex;align-items:center;justify-content:center;color:white;font-size:22px"><i class="fa-brands fa-telegram"></i></div><div><b>অফিশিয়াল চ্যানেল</b><br><small>@"""+ch+"""</small></div></div><i class="fa-solid fa-arrow-right"></i></div>
<div class="card scard" style="background:#dc2626;color:white" onclick="openVideo()"><div style="display:flex;gap:12px;align-items:center"><div style="width:52px;height:52px;background:#f59e0b;border-radius:12px;display:flex;align-items:center;justify-content:center">▶</div><div><b>কিভাবে কাজ করবেন?</b><br><small>ভিডিও টিউটোরিয়াল দেখুন</small></div></div><i class="fa-solid fa-arrow-right"></i></div>
<div class="card"><b>💬 Live Support</b><br><small>২৪ ঘন্টা সাপোর্ট - Monetag Company Connected Zone """+zn+"""</small></div>
</div>

<div id="withdraw" class="page">
<div class="card"><div class="big">৳<span id="b2">0</span></div><div style="text-align:center;color:#64748b">বর্তমান ব্যালেন্স</div>
<div style="display:flex;gap:10px;margin:12px 0"><div id="bk" class="input" style="text-align:center;font-weight:800;border:2px solid """+th+""";cursor:pointer" onclick="sel('bkash')">Bkash</div><div id="ng" class="input" style="text-align:center;font-weight:800;cursor:pointer" onclick="sel('nagad')">Nagad</div></div>
<input id="num" class="input" placeholder="Bkash/Nagad Number - 01XXXXXXXXX"><input id="amt" class="input" type="number" placeholder="পরিমাণ - Min """+str(mn)+""" টাকা"><button class="btnG" onclick="wd()">💸 উইথড্র করুন</button>
<div style="margin-top:12px;color:#64748b;font-size:13px">⚠️ """+str(mn)+""" টাকা হলেই উইথড্র করতে পারবেন</div></div>
<div class="card"><b>📜 উইথড্র হিস্ট্রি</b><div id="wdList" style="font-size:12px;margin-top:8px;color:#64748b">লোড হচ্ছে...</div></div>
</div>

<div class="bottom">
<div class="bi active" onclick="showP('home',this)"><i class="fa-solid fa-house"></i><br>হোম</div>
<div class="bi" onclick="showP('earn',this)"><i class="fa-solid fa-coins"></i><br>আয়</div>
<div class="bi" onclick="showP('support',this)"><i class="fa-solid fa-headset"></i><br>সাপোর্ট</div>
<div class="bi" onclick="showP('withdraw',this)"><i class="fa-solid fa-wallet"></i><br>উইথড্র</div>
</div>

<script>
let UID=Telegram.WebApp.initDataUnsafe?.user?.id||"8807178385"; let METHOD="bkash";
function showP(id,el){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.bi').forEach(b=>b.classList.remove('active'));el.classList.add('active'); if(id=='withdraw') loadWd();}
function copyR(){let t=document.getElementById('rl').innerText; navigator.clipboard.writeText(t); Telegram.WebApp.showAlert('✅ লিংক কপি হয়েছে: '+t);}
function shareR(){let t=document.getElementById('rl').innerText; if(navigator.share){navigator.share({title:'"""+nm+"""',text:'আয় করুন',url:t});} else {copyR();}}
function sel(m){METHOD=m; document.getElementById('bk').style.border='1px solid #e2e8f0'; document.getElementById('ng').style.border='1px solid #e2e8f0'; document.getElementById(m=='bkash'?'bk':'ng').style.border='2px solid """+th+"""';}
function openTg(username){let url='https://t.me/'+username; if(Telegram.WebApp.openTelegramLink){Telegram.WebApp.openTelegramLink(url);} else {window.open(url,'_blank');}}
function openVideo(){openTg('"""+ch+"""');}

async function load(){try{
let r=await fetch('/api/user?id='+UID); let j=await r.json();
document.getElementById('b1').innerText=j.bal; document.getElementById('b2').innerText=j.bal; document.getElementById('hbal2').innerText='৳'+j.bal;
document.getElementById('tdc').innerText=j.today; document.getElementById('tdc2').innerText=j.today;
document.getElementById('tdi').innerText=j.today*"""+str(ad_reward)+""";
document.getElementById('left').innerText="""+str(lim)+"""-j.today;
document.getElementById('rl').innerText='https://t.me/"""+bt+"""?start='+UID;
}catch(e){}
}
async function loadWd(){try{let r=await fetch('/api/wds?id='+UID); let j=await r.json(); let h=''; if(j.length==0) h='কোনো উইথড্র নেই'; else j.forEach(w=>{h+='<div style="border-bottom:1px solid #eee;padding:6px 0">'+w.method+' - '+w.number+' - ৳'+w.amount+' - '+w.status+'</div>';}); document.getElementById('wdList').innerHTML=h;}catch(e){}}
async function watchAd(){let btn=event.target; btn.innerText='⏳ লোড হচ্ছে...'; try{if(typeof show_"""+zn+"""==='function'){await show_"""+zn+"""();}}catch(e){} let r=await fetch('/api/ad',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:UID})}); let j=await r.json(); Telegram.WebApp.showAlert(j.msg); load(); btn.innerText='▶ বিজ্ঞাপন দেখুন';}
async function doTask(type){Telegram.WebApp.showConfirm('এই টাস্ক করতে টেলিগ্রামে যাবেন?',async function(ok){ if(!ok) return; if(type=='yt'){openTg('"""+ch+"""');} else {openTg('"""+ch+"""');} setTimeout(async()=>{let r=await fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:UID,type:type})}); let j=await r.json(); Telegram.WebApp.showAlert(j.msg); load();},2000); });}
async function wd(){let n=document.getElementById('num').value; let a=document.getElementById('amt').value; if(!n||!a){Telegram.WebApp.showAlert('❌ নাম্বার ও টাকা লেখো'); return;} let r=await fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:UID,number:n,amount:a,method:METHOD})}); let j=await r.json(); Telegram.WebApp.showAlert(j.msg); load(); loadWd();}
load();
</script></body></html>
"""

@app.route("/api/user")
def api_user():
    db=load_db(); uid=str(request.args.get("id","0")); t=str(date.today())
    if uid not in db["users"]: db["users"][uid]={"bal":db["s"]["welcome"],"today":0,"total":0,"date":t,"tasks":[]}
    u=db["users"][uid]
    if u.get("date")!=t: u["today"]=0; u["date"]=t
    save_db(db); return jsonify({"bal":u["bal"],"today":u["today"],"total":u["total"]})

@app.route("/api/ad",methods=["POST"])
def api_ad():
    db=load_db(); uid=str(request.json.get("id")); u=db["users"].get(uid)
    if not u: return jsonify({"msg":"❌ User পাওয়া যায়নি"})
    if u["today"]>=db["s"]["limit"]: return jsonify({"msg":"❌ আজ "+str(db["s"]["limit"])+"টা শেষ! কাল আসুন"})
    u["today"]+=1; u["total"]+=1; u["bal"]+=db["s"]["ad"]; save_db(db)
    return jsonify({"msg":"✅ ৳"+str(db["s"]["ad"])+" যোগ হয়েছে!"})

@app.route("/api/task",methods=["POST"])
def api_task():
    db=load_db(); d=request.json; uid=str(d.get("id")); typ=d.get("type"); u=db["users"].get(uid)
    if not u: return jsonify({"msg":"User নেই"})
    if typ in u.get("tasks",[]): return jsonify({"msg":"⚠️ এই টাস্ক আগেই করেছেন!"})
    reward=db["s"]["yt"] if typ=="yt" else db["s"]["tg"]
    u["bal"]+=reward; u["total"]+=1
    if "tasks" not in u: u["tasks"]=[]
    u["tasks"].append(typ); save_db(db)
    return jsonify({"msg":"✅ ৳"+str(reward)+" বোনাস পেয়েছেন!"})

@app.route("/api/withdraw",methods=["POST"])
def api_wd():
    db=load_db(); d=request.json; uid=str(d.get("id")); u=db["users"].get(uid)
    try: amt=float(d.get("amount",0))
    except: return jsonify({"msg":"❌ টাকা সঠিক লেখো"})
    if amt<db["s"]["min"]: return jsonify({"msg":"❌ মিনিমাম "+str(db["s"]["min"])+" টাকা!"})
    if u["bal"]<amt: return jsonify({"msg":"❌ ব্যালেন্স কম! আছে ৳"+str(u["bal"])})
    u["bal"]-=amt; d["status"]="Pending"; d["time"]=str(datetime.now()); db["wds"].append(d); save_db(db)
    return jsonify({"msg":"✅ উইথড্র রিকোয়েস্ট সফল! ২৪ ঘন্টায় পাবেন"})

@app.route("/api/wds")
def api_wds():
    db=load_db(); uid=str(request.args.get("id","0"))
    my=[w for w in db["wds"] if str(w.get("id"))==uid]
    return jsonify(my[-10:])

@app.route("/admin")
def admin():
    db=load_db(); s=db["s"]
    if request.args.get("id")!=s["admin_id"]: return "Unauthorized -?id=8807178385 দাও"
    total_bal=sum(u["bal"] for u in db["users"].values())
    return """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
    body{font-family:sans-serif;background:#f0fdfa;padding:12px}.card{background:white;padding:16px;border-radius:16px;margin:12px 0}
   .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.kpi{background:"""+s["theme"]+""";color:white;padding:14px;border-radius:14px;text-align:center}
    input,textarea{width:100%;padding:12px;margin:6px 0;border:1px solid #e2e8f0;border-radius:10px}
    button{background:"""+s["theme"]+""";color:white;border:none;padding:14px;width:100%;border-radius:12px;font-weight:800;margin-top:8px;cursor:pointer}
    </style></head><body>
    <h2>🏢 COMPANY ADMIN - ULTIMATE</h2>
    <div style="background:#134e4a;color:white;padding:12px;border-radius:12px">✅ Monetag Company LIVE - Zone """+s["zone"]+""" | Bot @"""+s["bot"]+"""</div>
    <div class="grid"><div class="kpi"><div>মোট ইউজার</div><h2>"""+str(len(db["users"]))+"""</h2></div><div class="kpi"><div>মোট ব্যালেন্স</div><h2>৳"""+str(total_bal)+"""</h2></div><div class="kpi"><div>উইথড্র</div><h2>"""+str(len(db["wds"]))+"""</h2></div><div class="kpi"><div>কোম্পানি লাভ</div><h2>৳"""+str(len(db["users"])*5)+"""</h2></div></div>

    <div class="card"><h3>💰 টাকা কন্ট্রোল - সব এডিট</h3>
    Welcome Bonus:<input id="welcome" value='"""+str(s["welcome"])+"""'>
    Per Ad Reward:<input id="ad" value='"""+str(s["ad"])+"""'>
    Refer Bonus:<input id="ref" value='"""+str(s["ref"])+"""'>
    Daily Limit:<input id="limit" value='"""+str(s["limit"])+"""'>
    Min Withdraw:<input id="min" value='"""+str(s["min"])+"""'>
    YouTube Reward:<input id="yt" value='"""+str(s["yt"])+"""'>
    Telegram Reward:<input id="tg" value='"""+str(s["tg"])+"""'>
    </div>

    <div class="card"><h3>📢 বিজ্ঞাপন এডিটিং - Monetag Company Ad</h3>
    Zone ID (Company Ad ID):<input id="zone" value='"""+s["zone"]+"""'>
    <small>Monetag থেকে নতুন Zone পেলে এখানে বসাও - কোম্পানির সাথে Ads যুক্ত থাকবে</small>
    </div>

    <div class="card"><h3>🎨 লোগো ও প্রোফাইল পরিবর্তন</h3>
    App Name:<input id="name" value='"""+s["name"]+"""'>
    Logo URL (লোগো লিংক দাও):<input id="logo" value='"""+s["logo"]+"""'>
    <img src='"""+s["logo"]+"""' style="width:60px;height:60px;border-radius:50%;margin:8px 0"><br>
    Bot Username:<input id="bot" value='"""+s["bot"]+"""'>
    Channel:<input id="channel" value='"""+s["channel"]+"""'>
    Admin Username:<input id="admin" value='"""+s["admin"]+"""'>
    Theme Color:<input id="theme" value='"""+s["theme"]+"""'>
    Notice Text:<textarea id="notice" rows="3">"""+s["notice"]+"""</textarea>
    </div>

    <button onclick="saveAll()">💾 SAVE - সবকিছু কোম্পানির সাথে আপডেট করুন</button>
    <div class="card"><h3>📋 লেটেস্ট উইথড্র - Approve/Reject</h3><pre style="font-size:11px;overflow:auto">"""+json.dumps(db["wds"][-20:],ensure_ascii=False,indent=2)+"""</pre></div>
    <script>
    async function saveAll(){
      let data={
        welcome:parseInt(document.getElementById('welcome').value),
        ad:parseInt(document.getElementById('ad').value),
        ref:parseInt(document.getElementById('ref').value),
        limit:parseInt(document.getElementById('limit').value),
        min:parseInt(document.getElementById('min').value),
        yt:parseInt(document.getElementById('yt').value),
        tg:parseInt(document.getElementById('tg').value),
        zone:document.getElementById('zone').value,
        name:document.getElementById('name').value,
        logo:document.getElementById('logo').value,
        bot:document.getElementById('bot').value,
        channel:document.getElementById('channel').value,
        admin:document.getElementById('admin').value,
        theme:document.getElementById('theme').value,
        notice:document.getElementById('notice').value
      };
      let r=await fetch('/api/admin/save?id="""+s["admin_id"]+"""',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
      let j=await r.json(); alert(j.msg); location.reload();
    }
    </script></body></html>"""

@app.route("/api/admin/save",methods=["POST"])
def admin_save():
    db=load_db()
    if request.args.get("id")!=db["s"]["admin_id"]: return jsonify({"msg":"Unauthorized"})
    d=request.json
    for k in d: db["s"][k]=d[k]
    save_db(db); return jsonify({"msg":"✅ সফল! কোম্পানির সাথে সব আপডেট হয়েছে - লোগো, প্রোফাইল, বিজ্ঞাপন সব!"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
