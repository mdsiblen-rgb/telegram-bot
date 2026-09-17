import os, json, time, base64
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

DEFAULT_SETTINGS = {
    "app_name": "👑 প্রতিদিনের কাজ বিডি",
    "app_name2": "Daily Work BD ✅",
    "primary": "#8b5cf6", "secondary": "#f59e0b",
    "bonus": 20, "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 30, "min": 500, "ref": 15, "diamond_rate": 100,
    "company_ad_id": "11764581", "popup_ad_id": "11798857",
    "direct_link": "https://omg10.com/4/11760259",
    "spon_title": "🔥 আজকের সেরা অফার - BIG AD!",
    "spon_desc": "প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন",
    "spon_btn": "🚀 Claim Now", "spon_link": "https://google.com",
    "ref_title": "👥 Refer & Earn Unlimited", "ref_desc": "প্রতি রেফারে ৳১৫ + ১০% কমিশন",
    "ref_banner": "🎉 Refer Contest চলছে! Top 10 পাবে ৳5000",
    "sup_notice": "⚠️ রাত ১০টার পর Withdraw বন্ধ, সকাল ৯টায় চালু",
    "sup_faq1_q": "💸 Withdraw কতক্ষণে পাবো?", "sup_faq1_a": "৫-৩০ মিনিটের মধ্যে bKash/Nagad এ পাবেন।",
    "sup_faq2_q": "👥 Refer টাকা কখন পাবো?", "sup_faq2_a": "বন্ধু Join করলেই সাথে সাথে।",
    "sup_faq3_q": "📢 Ads দেখলে টাকা আসে না কেন?", "sup_faq3_a": "VPN বন্ধ করে ১০ সেকেন্ড দেখুন।",
    "sup_rules": "1. এক ফোনে এক আইডি\n2. ভুয়া রেফার করলে ব্যান\n3. VPN ব্যবহার করবেন না",
    "levels": [0,500,2000,5000,10000,20000]
}

def load_db():
    if not os.path.exists(DB):
        data = {"users": {}, "wds": [], "settings": DEFAULT_SETTINGS, "tasks": [
            {"id": 1, "title": "Join Telegram Channel", "reward": 2, "link": "https://t.me/", "icon": "📢"},
            {"id": 2, "title": "Visit Company Website", "reward": 3, "link": "https://google.com", "icon": "🌐"},
        ]}
        with open(DB, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    with open(DB, 'r', encoding='utf-8') as f:
        db = json.load(f)
        for k,v in DEFAULT_SETTINGS.items():
            if k not in db["settings"]: db["settings"][k]=v
        db.setdefault("users",{}); db.setdefault("wds",[]); db.setdefault("tasks",[])
        return db

def save_db(db):
    with open(DB, 'w', encoding='utf-8') as f: json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(db, uid, ref=None):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid, "name": f"User {uid[-4:]}", "img": "", "bal": float(db["settings"]["bonus"]),
            "total": float(db["settings"]["bonus"]), "c_today": 0, "p_today": 0,
            "ad_date": time.strftime("%Y-%m-%d"), "diamonds": db["settings"]["bonus"]*100,
            "refl": [], "ref_by": ref, "join": datetime.now().strftime("%Y-%m-%d")
        }
        if ref and ref in db["users"] and ref!= uid:
            db["users"][ref]["refl"].append(uid)
            db["users"][ref]["bal"] += float(db["settings"]["ref"])
            db["users"][ref]["total"] += float(db["settings"]["ref"])
    return db["users"][uid]

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin','*'); r.headers.add('Access-Control-Allow-Headers','*'); r.headers.add('Access-Control-Allow-Methods','*')
    return r

@app.route('/api/init', methods=['POST'])
def init_api():
    db=load_db(); j=request.json or {}; uid=str(j.get('id') or '0')
    u=get_user(db, uid, j.get('ref')); save_db(db)
    return jsonify({"user":u, "s":db["settings"], "tasks":db["tasks"]})

@app.route('/api/ads', methods=['POST'])
def ads_api():
    db=load_db(); j=request.json or {}; uid=str(j.get('id') or '0'); typ=j.get('type','c')
    u=get_user(db, uid); s=db["settings"]; today=time.strftime("%Y-%m-%d")
    if u.get("ad_date")!= today:
        u["ad_date"]=today; u["c_today"]=0; u["p_today"]=0
    if typ=='c':
        if u.get("c_today",0) >= s["clim"]: return jsonify({"msg":f"আজকের {s['clim']}টা Company Ads শেষ! কাল আবার"})
        reward=float(s["ad"]); u["c_today"]+=1
    else:
        if u.get("p_today",0) >= s["plim"]: return jsonify({"msg":f"আজকের {s['plim']}টা Popup Ads শেষ!"})
        reward=float(s["pop"]); u["p_today"]+=1
    u["bal"]=round(float(u["bal"])+reward,2); u["total"]=round(float(u["total"])+reward,2)
    u["diamonds"]=int(u.get("diamonds",0))+int(reward*s["diamond_rate"])
    save_db(db)
    return jsonify({"msg":f"৳{reward} + {int(reward*s['diamond_rate'])} 💎 Added","bal":u["bal"],"diamonds":u["diamonds"],"c_today":u["c_today"],"p_today":u["p_today"]})

@app.route('/api/wd', methods=['POST'])
def wd_api():
    db=load_db(); j=request.json or {}; u=get_user(db, str(j.get('id')))
    try: amt=int(float(j.get('amt',0)))
    except: amt=0
    s=db["settings"]
    if amt < s["min"]: return jsonify({"msg":f"Minimum Withdraw ৳{s['min']}"})
    if float(u["bal"]) < amt: return jsonify({"msg":"Balance কম আছে"})
    u["bal"]=round(float(u["bal"])-amt,2)
    db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"time":datetime.now().strftime("%d-%m %H:%M"),"st":"Pending"})
    save_db(db); return jsonify({"msg":"Withdraw Request সফল! 24h এর মধ্যে পাবেন"})

@app.route('/api/profile', methods=['POST'])
def profile_api():
    db=load_db(); j=request.json or {}; u=get_user(db, str(j.get('id')))
    if j.get('name'): u["name"]=j.get('name')[:25]
    if j.get('img'): u["img"]=j.get('img') # base64
    save_db(db); return jsonify({"msg":"Profile Updated","user":u})

@app.route('/admin', methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        for k in db["settings"]:
            if request.form.get(k):
                v=request.form.get(k)
                if k in ["ad","pop","bonus","ref","diamond_rate"]:
                    try: db["settings"][k]=float(v)
                    except: db["settings"][k]=v
                elif k in ["clim","plim","min"]:
                    try: db["settings"][k]=int(float(v))
                    except: db["settings"][k]=v
                else: db["settings"][k]=v
        save_db(db)
    s=db["settings"]
    return render_template_string("""
    <body style="background:#0B0E1C;color:#fff;padding:15px;font-family:system-ui;max-width:600px;margin:auto">
    <h2>👑 Admin Panel - {{s.app_name}}</h2>
    <div style="background:#1A2040;padding:15px;border-radius:12px;margin-top:10px">
    <form method="POST">
    App Name: <input name="app_name" value="{{s.app_name}}" style="width:100%;padding:8px;margin:5px 0"><br>
    Company Ad Rate: <input name="ad" value="{{s.ad}}" type="number" step="0.01">
    Limit: <input name="clim" value="{{s.clim}}" type="number"><br>
    Popup Ad Rate: <input name="pop" value="{{s.pop}}" type="number" step="0.01">
    Limit: <input name="plim" value="{{s.plim}}" type="number"><br>
    Min Withdraw: <input name="min" value="{{s.min}}" type="number">
    Refer Bonus: <input name="ref" value="{{s.ref}}" type="number"><br>
    Direct Link (Monetag): <input name="direct_link" value="{{s.direct_link}}" style="width:100%"><br>
    Sponsor Title: <input name="spon_title" value="{{s.spon_title}}" style="width:100%"><br>
    Sponsor Desc: <input name="spon_desc" value="{{s.spon_desc}}" style="width:100%"><br>
    Notice: <input name="sup_notice" value="{{s.sup_notice}}" style="width:100%"><br><br>
    <button style="width:100%;padding:12px;background:#8b5cf6;color:#fff;border:none;border-radius:8px;font-weight:800">Save All - Admin থেকে Control</button>
    </form></div>
    <p>Users: {{db.users|length}} | Withdraws: {{db.wds|length}}</p>
    {% for w in db.wds[-20:] %}<div style="background:#151A2D;padding:8px;margin:4px 0;border-radius:8px">{{w.name}} - {{w.amt}}Tk - {{w.num}} ({{w.m}}) - {{w.st}}</div>{% endfor %}
    </body>
    """, s=s, db=db)

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    template = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:110px}
.glass{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:16px;margin:12px}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{{s.primary}};cursor:pointer;margin-top:10px;font-size:15px}
.btn2{background:{{s.secondary}};color:#000}
.top2{display:flex;gap:10px;margin:12px;align-items:center}
.topbox{flex:1;background:#151A2D;border:1px solid {{s.primary}};padding:12px;border-radius:14px;font-weight:700;font-size:14px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:10px 0 16px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}
.btm div.on{color:{{s.primary}}}
.btm div span{font-size:22px;display:block}
.page{display:none}.page.active{display:block}
.proImg{width:72px;height:72px;border-radius:18px;background:#0B0E1C;border:2px solid {{s.primary}};display:flex;align-items:center;justify-content:center;font-size:32px;overflow:hidden}
</style></head><body>

<div id="p1" class="page active">
  <div class="top2">
    <div class="topbox" onclick="showP(5,document.querySelectorAll('.btm div')[4])">👑 {{s.app_name}}<br>✅ <span id="bal">৳0</span> | 💎 <span id="diam">0</span></div>
    <div class="proImg" id="proImg">💎</div>
  </div>
  <div class="glass">💎 Diamond Member • Level <span id="lvl">1</span><br><small><span id="c_now">0</span>/{{s.clim}} Company | <span id="p_now">0</span>/{{s.plim}} Popup | Total Ads <span id="ads">0</span></small>
    <div style="background:#0B0E1C;height:8px;border-radius:10px;margin-top:8px"><div id="prog" style="height:8px;width:0%;background:{{s.primary}};border-radius:10px"></div></div>
  </div>
  <div class="glass">Company Ads ৳{{s.ad}} <small style="float:right" id="c_text">0/{{s.clim}}</small><button class="btn" onclick="doAd('c')">Start - ৳{{s.ad}}</button></div>
  <div class="glass">Popup Ads ৳{{s.pop}} <small style="float:right" id="p_text">0/{{s.plim}}</small><button class="btn btn2" onclick="doAd('p')">Watch - ৳{{s.pop}}</button></div>
  <div class="glass">💸 Withdraw (Min ৳{{s.min}})<button class="btn" style="background:#22c55e" onclick="showP(4,document.querySelectorAll('.btm div')[3])">Withdraw Now</button></div>
  <div class="glass" style="background:linear-gradient(135deg,#2D1B4E,#1A1033);border-color:{{s.secondary}}"><b>{{s.spon_title}}</b><br><small>{{s.spon_desc}}</small><br><button class="btn btn2" onclick="window.open('{{s.spon_link}}','_blank')">{{s.spon_btn}}</button></div>
</div>

<div id="p2" class="page">
  <div class="glass"><b>🎯 Tasks & Company Links</b><br><small>প্রতি Task এ ৳2-5 + Diamond</small></div>
  <div id="taskList"></div>
  <div class="glass" style="border-color:{{s.secondary}}"><b>🔥 Special Offer</b><br><small>{{s.spon_desc}}</small></div>
</div>

<div id="p3" class="page">
  <div class="glass" style="background:linear-gradient(90deg,{{s.secondary}},#f97316);color:#000;text-align:center;font-weight:800">{{s.ref_banner}}</div>
  <div class="glass"><b>{{s.ref_title}}</b><br><small>{{s.ref_desc}}</small><br><br><div style="background:#0B0E1C;padding:10px;border-radius:10px;font-size:12px;word-break:break-all" id="refLink"></div><button class="btn" onclick="copyRef()">Copy Refer Link</button><br><small>My Refer: <span id="myRef">0</span> জন</small></div>
</div>

<div id="p4" class="page">
  <div class="glass"><b>💸 Withdraw</b><br><small>Min {{s.min}} Tk</small>
    <div style="display:flex;gap:8px;margin-top:10px"><div id="m1" class="topbox" style="text-align:center;cursor:pointer" onclick="setM('bKash')">bKash</div><div id="m2" class="topbox" style="text-align:center;cursor:pointer" onclick="setM('Nagad')">Nagad</div></div>
    <input id="acc" placeholder="bKash/Nagad Number" style="width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px">
    <input id="amt" placeholder="Amount - Min {{s.min}}" type="number" style="width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px">
    <button class="btn" style="background:#22c55e" onclick="doWd()">Withdraw Now</button>
  </div>
</div>

<div id="p5" class="page">
  <div class="glass" style="text-align:center"><div class="proImg" id="proImg2" style="margin:0 auto 10px;width:90px;height:90px;font-size:40px">💎</div><b id="pName">User</b><br><small>💎 <span id="pDiam">0</span> Diamond | Level <span id="pLvl">1</span></small><br><br>
    <input id="newName" placeholder="নতুন নাম লিখো" style="width:100%;padding:10px;border-radius:10px;background:#0B0E1C;color:#fff;border:1px solid #2a2f4a">
    <input type="file" id="imgIn" accept="image/*" style="margin-top:8px">
    <button class="btn" onclick="saveProfile()">Save Profile - নাম/ছবি চেঞ্জ</button>
  </div>
  <div class="glass" style="background:linear-gradient(135deg,{{s.primary}},#6366f1)"><b>📥 Inbox Help Center</b><br><small>{{s.sup_notice}}</small></div>
  <div class="glass"><b>{{s.sup_faq1_q}}</b><br><small style="color:#94a3b8">{{s.sup_faq1_a}}</small></div>
  <div class="glass"><b>{{s.sup_faq2_q}}</b><br><small style="color:#94a3b8">{{s.sup_faq2_a}}</small></div>
  <div class="glass"><b>{{s.sup_faq3_q}}</b><br><small style="color:#94a3b8">{{s.sup_faq3_a}}</small></div>
  <div class="glass"><b>📜 Rules</b><br><small style="color:#94a3b8;white-space:pre-line">{{s.sup_rules}}</small></div>
</div>

<div class="btm">
  <div class="on" onclick="showP(1,this)"><span>🏠</span>Home</div>
  <div onclick="showP(2,this)"><span>🎯</span>Tasks</div>
  <div onclick="showP(3,this)"><span>👥</span>Refer</div>
  <div onclick="showP(4,this)"><span>💸</span>Withdraw</div>
  <div onclick="showP(5,this)"><span>👤</span>Profile</div>
</div>

<script>
let tg=window.Telegram.WebApp;tg.expand();
let uid=String(tg.initDataUnsafe?.user?.id||"12345");
let method="bKash"; let user={}; let settings={{}};
document.getElementById('refLink').innerText="https://t.me/YourBot?start="+uid;

function showP(n,e){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('p'+n).classList.add('active');
  document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));
  if(e) e.classList.add('on');
}
function setM(m){
  method=m;
  document.getElementById('m1').style.borderColor=m=='bKash'?'{{s.primary}}':'#1e293b';
  document.getElementById('m2').style.borderColor=m=='Nagad'?'{{s.primary}}':'#1e293b';
}
async function init(){
  let r=await fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})});
  let j=await r.json(); user=j.user; settings=j.s;
  document.getElementById('bal').innerText='৳'+Number(user.bal).toFixed(2);
  document.getElementById('diam').innerText=user.diamonds;
  document.getElementById('pDiam').innerText=user.diamonds;
  document.getElementById('pName').innerText=user.name;
  document.getElementById('c_now').innerText=user.c_today; document.getElementById('p_now').innerText=user.p_today;
  document.getElementById('ads').innerText=user.c_today+user.p_today;
  document.getElementById('c_text').innerText=user.c_today+'/{{s.clim}}';
  document.getElementById('p_text').innerText=user.p_today+'/{{s.plim}}';
  document.getElementById('myRef').innerText=(user.refl||[]).length;
  document.getElementById('prog').style.width=Math.min(100, ((user.c_today+user.p_today)/({{s.clim}}+{{s.plim}})*100))+'%';
  if(user.img){ document.getElementById('proImg').innerHTML='<img src="'+user.img+'" style="width:100%;height:100%;object-fit:cover">'; document.getElementById('proImg2').innerHTML='<img src="'+user.img+'" style="width:100%;height:100%;object-fit:cover">'; }
  let tl=""; (j.tasks||[]).forEach(t=>{
    tl+=`<div class="glass">`+t.icon+` `+t.title+` <small>৳`+t.reward+`</small><button class="btn" onclick="window.open('`+t.link+`','_blank')">Start</button></div>`;
  }); document.getElementById('taskList').innerHTML=tl;
}
async function doAd(t){
  window.open('{{s.direct_link}}','_blank');
  setTimeout(async()=>{
    let r=await fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})});
    let j=await r.json(); alert(j.msg); init();
  },3000);
}
async function doWd(){
  let acc=document.getElementById('acc').value; let amt=document.getElementById('amt').value;
  if(!acc||!amt){alert('Number ও Amount দাও');return;}
  let r=await fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:acc,amt:amt,m:method})});
  let j=await r.json(); alert(j.msg); init();
}
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Refer Link Copied!'); }
async function saveProfile(){
  let name=document.getElementById('newName').value;
  let file=document.getElementById('imgIn').files[0];
  let imgData="";
  if(file){
    imgData=await new Promise(res=>{let fr=new FileReader(); fr.onload=()=>res(fr.result); fr.readAsDataURL(file);});
  }
  let r=await fetch('/api/profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:name,img:imgData})});
  let j=await r.json(); alert(j.msg); init();
}
setM('bKash'); init();
</script>
</body></html>
    """
    return render_template_string(template, s=s)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
