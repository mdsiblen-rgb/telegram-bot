import os, json, time
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
DB = 'database.json'

def load_db():
    d = {
        "app_name":"👑 প্রতিদিনের কাজ বিডি","primary":"#8b5cf6","secondary":"#f59e0b",
        "bonus":20,"ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"direct_link":"https://omg10.com/4/11760259",
        "spon_title":"🔥 আজকের সেরা অফার","spon_desc":"প্রতিদিন ৫০০ টাকা ইনকাম করুন!","spon_btn":"🚀 Claim Now","spon_link":"https://google.com",
        "sup_notice":"⚠️ রাত ১০টার পর Withdraw বন্ধ","sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে পাবেন।","sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু Join করলেই ৳৮০ সাথে সাথে।","sup_faq3_q":"📢 Ads আসে না কেন?","sup_faq3_a":"VPN বন্ধ করুন।","sup_rules":"1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান","levels":[0,500,2000,5000,10000]
    }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2))
        return data
    return json.load(open(DB,'r',encoding='utf-8'))

def save_db(db):
    open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))

def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c_today":0,"p_today":0,"ad_date":str(datetime.now().date()),"diamonds":2000}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["bal"]+=db["settings"]["ref"]
    return db["users"][uid]

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin','*')
    r.headers.add('Access-Control-Allow-Headers','*')
    r.headers.add('Access-Control-Allow-Methods','*')
    return r

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db(); j=request.json; u=get_user(db,str(j.get('id')),j.get('ref')); save_db(db)
    return jsonify({"user":u,"s":db["settings"]})

@app.route('/api/ads',methods=['POST'])
def ads():
    db=load_db(); j=request.json; uid=str(j.get('id')); typ=str(j.get('type') or 'c')
    u=get_user(db,uid); s=db["settings"]; today=time.strftime("%Y-%m-%d")
    if u.get("ad_date")!=today:
        u["ad_date"]=today; u["c_today"]=0; u["p_today"]=0
    if typ=='c':
        if u.get("c_today",0)>=s["clim"]: return jsonify({"msg":"Limit sesh"})
        reward=float(s["ad"]); u["c_today"]+=1
    else:
        if u.get("p_today",0)>=s["plim"]: return jsonify({"msg":"Limit sesh"})
        reward=float(s["pop"]); u["p_today"]+=1
    u["bal"]+=reward; save_db(db)
    return jsonify({"msg":f"{reward} Taka Added","bal":u["bal"]})

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    # f-string এর ভিতরে JS এর {} ডাবল {{}} করা হয়েছে যাতে Error না আসে
    html = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}
body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}}
.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}}
.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{s['primary']};cursor:pointer;margin-top:10px}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}
.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:22px;display:block}}.page{{display:none}}.page.active{{display:block}}
</style></head><body>
<div id="p1" class="page active">
<div class="glass">👑 {s['app_name']} - Balance: <span id="bal">0</span></div>
<div class="glass">Company Ads ৳{s['ad']} <button class="btn" onclick="doAd('c')">Start - ৳{s['ad']}</button></div>
<div class="glass">Popup Ads ৳{s['pop']} <button class="btn" style="background:{s['secondary']};color:#000" onclick="doAd('p')">Watch - ৳{s['pop']}</button></div>
<div class="glass">📥 Inbox Help<br><small>{s['sup_notice']}</small><br><br><b>{s['sup_faq1_q']}</b><br><small>{s['sup_faq1_a']}</small><br><br><b>{s['sup_faq2_q']}</b><br><small>{s['sup_faq2_a']}</small></div>
</div>
<div id="p5" class="page"><div class="glass"><b>📜 Rules</b><br><small>{s['sup_rules']}</small></div></div>
<div class="btm">
<div class="on" onclick="showP(1,this)"><span>🏠</span>Home</div>
<div onclick="showP(5,this)"><span>📥</span>Inbox</div>
</div>
<script>
let tg=window.Telegram.WebApp;tg.expand();
let uid=String(tg.initDataUnsafe?.user?.id||"999");
let user={{}};
async function init(){{
  let r=await fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}});
  let j=await r.json(); user=j.user; document.getElementById('bal').innerText=j.user.bal;
}}
function showP(n,e){{
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('p'+n).classList.add('active');
  document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));
  e.classList.add('on');
}}
async function doAd(t){{
  window.open('{s['direct_link']}','_blank');
  setTimeout(async()=>{{
    let r=await fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:t}})}});
    let j=await r.json(); alert(j.msg); init();
  }},3000);
}}
init();
</script></body></html>
    """
    return html

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
