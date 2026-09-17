import os, json, time
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

def load_db():
    d = {
        "app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅",
        "primary":"#8b5cf6","secondary":"#f59e0b",
        "bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস পেয়েছেন!",
        "ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,
        "company_ad_id":"11764581","popup_ad_id":"11798857",
        "direct_link":"https://omg10.com/4/11760259",
        "spon_title":"🔥 আজকের সেরা অফার - BIG AD!",
        "spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন!",
        "spon_btn":"🚀 Explore Now","spon_link":"https://google.com",
        "ref_title":"👥 Refer & Earn","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!",
        "ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০!",
        "sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট",
        "sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/",
        "sup_notice":"⚠️ রাত ১০টার পর Withdraw বন্ধ",
        "sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে পাবেন।",
        "sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই ৳৮০ সাথে সাথে।",
        "sup_faq3_q":"📢 Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN বন্ধ করুন, ১০ সেকেন্ড দেখুন।",
        "sup_rules":"1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান",
        "pro_title":"👤 My Profile","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]
    }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[
            {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
            {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},
            {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}
        ]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2))
        return data
    db=json.load(open(DB,'r',encoding='utf-8'))
    for k,v in d.items():
        if k not in db["settings"]: db["settings"][k]=v
    return db

def save_db(db):
    open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))

def get_level(total, levels):
    lvl=1
    for i,th in enumerate(levels):
        if total>=th: lvl=i+1
    return lvl

def get_user(db,uid,ref=None):
    uid=str(uid)
    is_new=False
    if uid not in db["users"]:
        is_new=True
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"diamonds":db["settings"]["bonus"]*db["settings"]["diamond_rate"],"c_today":0,"p_today":0,"ad_date":str(datetime.now().date())}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["refl"].append(uid)
            db["users"][ref]["bal"]+=db["settings"]["ref"]
            db["users"][ref]["total"]+=db["settings"]["ref"]
    return db["users"][uid], is_new

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin','*')
    r.headers.add('Access-Control-Allow-Headers','*')
    r.headers.add('Access-Control-Allow-Methods','*')
    return r

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db(); j=request.json; u,is_new=get_user(db,str(j.get('id')),j.get('ref')); save_db(db)
    wds=[x for x in db["wds"] if x["uid"]==u["id"]]
    lvl=get_level(u["total"], db["settings"]["levels"])
    nxt=db["settings"]["levels"][lvl] if lvl < len(db["settings"]["levels"]) else db["settings"]["levels"][-1]
    prog=int((u["total"]/nxt*100)) if nxt>0 else 0
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds,"level":lvl,"next":nxt,"prog":prog,"is_new":is_new})

@app.route('/api/ads', methods=['POST'])
def handle_ads():
    db = load_db(); data = request.json; uid = str(data.get('id') or data.get('uid') or ''); ad_type = str(data.get('type') or 'c')
    user,_ = get_user(db, uid); s = db["settings"]; today = time.strftime("%Y-%m-%d")
    if user.get("ad_date")!= today:
        user["ad_date"]=today; user["c_today"]=0; user["p_today"]=0
    if ad_type == 'c':
        if user.get("c_today",0) >= s.get("clim",50): return jsonify({"msg":"Ajker Company limit sesh"})
        reward=float(s.get("ad",0.2)); user["c_today"]=user.get("c_today",0)+1
    else:
        if user.get("p_today",0) >= s.get("plim",30): return jsonify({"msg":"Ajker Popup limit sesh"})
        reward=float(s.get("pop",0.3)); user["p_today"]=user.get("p_today",0)+1
    user["bal"]=float(user.get("bal",0))+reward; user["total"]=float(user.get("total",0))+reward; user["diamonds"]=int(user.get("diamonds",0))+int(reward*100)
    save_db(db); return jsonify({"msg":f"{reward} Taka Added","bal":user["bal"],"diamonds":user["diamonds"]})

@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db(); j=request.json; u,_=get_user(db,str(j.get('id'))); s=db["settings"]
    try: amt=int(float(j.get('amt',0)))
    except: amt=0
    if amt < s.get("min",500): return jsonify({"msg":f"Minimum {s.get('min')} Taka"})
    if u["bal"] < amt: return jsonify({"msg":"Balance kom"})
    u["bal"]-=amt; db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")})
    save_db(db); return jsonify({"msg":"Withdraw সফল"})

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    return render_template_string(f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}}.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}}.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{s['primary']};cursor:pointer;margin-top:10px}}.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0}}.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:22px;display:block}}.page{{display:none}}.page.active{{display:block}}</style></head><body>
<div id="p1" class="page active">
<div class="glass">👑 {s['app_name']} - Balance: <span id="bal">0</span> | <span id="ads">0</span> Ads</div>
<div class="glass">Company Ads ৳{s['ad']} <span id="cads">0</span>/{s['clim']} <button class="btn" onclick="doAd('c')">Start - ৳{s['ad']}</button></div>
<div class="glass">Popup Ads ৳{s['pop']} <span id="pads">0</span>/{s['plim']} <button class="btn" style="background:{s['secondary']};color:#000" onclick="doAd('p')">Watch - ৳{s['pop']}</button></div>
<div class="glass" style="background:linear-gradient(135deg,#2D1B4E,#1A1033);border-color:#f59e0b"><b>{s['spon_title']}</b><br><small>{s['spon_desc']}</small><br><button class="btn" style="background:{s['secondary']};color:#000" onclick="window.open('{s['spon_link']}')">{s['spon_btn']}</button></div>
</div>
<div id="p5" class="page">
<div class="glass" style="background:linear-gradient(135deg,#8b5cf6,#6366f1)">📥 Inbox Help - Full Design</div>
<div class="glass">⚠️ {s['sup_notice']}</div>
<div class="glass"><b>{s['sup_faq1_q']}</b><br><small>{s['sup_faq1_a']}</small></div>
<div class="glass"><b>{s['sup_faq2_q']}</b><br><small>{s['sup_faq2_a']}</small></div>
<div class="glass"><b>{s['sup_faq3_q']}</b><br><small>{s['sup_faq3_a']}</small></div>
<div class="glass"><b>📜 Rules</b><br><small>{s['sup_rules']}</small></div>
</div>
<div class="btm">
<div class="on" onclick="showP(1,this)"><span>🏠</span>Home</div>
<div onclick="showP(5,this)"><span>📥</span>Inbox</div>
</div>
<script>
let tg=window.Telegram.WebApp;tg.expand();let uid=String(tg.initDataUnsafe?.user?.id||"999");
let user={};
async function init(){{let r=await fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}});let j=await r.json();user=j.user;document.getElementById('bal').innerText=j.user.bal;}}
function showP(n,e){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p'+n).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));e.classList.add('on');}}
async function doAd(t){{window.open('{s['direct_link']}','_blank');setTimeout(async()=>{{let r=await fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:t}})}});let j=await r.json();alert(j.msg);init();}},3000);}}
init();
</script></body></html>
    """)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
