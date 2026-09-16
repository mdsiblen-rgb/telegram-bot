from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json, os, time
from datetime import date, datetime

app = Flask(__name__)
CORS(app)
DB_FILE = "db.json"

DEFAULT_SETTINGS = {
    "app_name": "প্রতিদিনের কাজ বিডি",
    "primary": "#8b5cf6",
    "secondary": "#f59e0b",
    "ad": 0.25,
    "pop": 0.20,
    "clim": 30,
    "plim": 50,
    "min": 500,
    "ref": 10,
    "company_ad_id": "11764581",
    "popup_ad_id": "11798857",
    "direct_link1": "https://omg10.com/4/11760259",
    "direct_link2": "",
    "spon_title": "Biggest Earning Offer",
    "spon_desc": "প্রতিদিন কাজ করে আয় করুন",
    "spon_link": "https://google.com",
    "spon_btn": "Claim Now",
    "spon_big_height": "180",
    "task_page_title": "Tasks & Company Links",
    "task_page_sub": "প্রতি Task এ ৳20-25 + Diamond",
    "task_bottom_title": "Special Offer",
    "task_bottom_desc": "Admin থেকে চেঞ্জ হবে",
    "task_bottom_btn": "Claim Now",
    "task_bottom_link": "https://google.com",
    "ref_title": "Refer & Earn",
    "ref_desc": "বন্ধুদের Invite করে Unlimited আয়",
    "ref_banner": "Refer Contest চলছে! - ৳5000",
    "ref_rules": "1. লিংক শেয়ার 2. Join ৳20 3. 15% Commission",
    "refer_bottom_title": "Refer Special Bonus",
    "refer_bottom_desc": "Admin থেকে অফার",
    "refer_bottom_btn": "Join Now",
    "refer_bottom_link": "https://google.com",
    "sup_title": "Support Center",
    "sup_desc": "24/7 সাপোর্ট",
    "sup_tg": "https://t.me/dailyworkbd",
    "sup_wa": "https://wa.me/8801",
    "sup_fb": "https://facebook.com",
    "sup_email": "support@dailyworkbd.com",
    "sup_notice": "রাত ১০টার পর Withdraw বন্ধ",
    "sup_faq1_q": "Withdraw কতক্ষণে?",
    "sup_faq1_a": "২৪ ঘণ্টায়",
    "sup_faq2_q": "Refer টাকা কখন?",
    "sup_faq2_a": "Join করলেই",
    "sup_faq3_q": "Ads সমস্যা?",
    "sup_faq3_a": "VPN ছাড়া দেখুন",
    "sup_rules": "1. এক আইডি 2. ফেক ব্যান",
    "support_bottom_title": "Important Notice",
    "support_bottom_desc": "Admin থেকে কন্ট্রোল",
    "support_bottom_btn": "Contact Now",
    "support_bottom_link": "https://t.me/",
    "profile_bottom_title": "VIP Membership",
    "profile_bottom_desc": "VIP হলে বেশি ইনকাম",
    "profile_bottom_btn": "Upgrade Now",
    "profile_bottom_link": "https://google.com",
    "home_title": "Daily Work BD"
}

DEFAULT_TASKS = [
    {"id":"t1","icon":"🌐","title":"Visit Company - ৳20","reward":0.2,"link":"https://google.com","url":"https://google.com"},
    {"id":"t2","icon":"🎥","title":"Watch Video - ৳25","reward":0.25,"link":"https://youtube.com","url":"https://youtube.com"},
    {"id":"t3","icon":"📢","title":"Join Telegram - ৳30","reward":0.3,"link":"https://t.me/","url":"https://t.me/"}
]

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users":{}, "settings":DEFAULT_SETTINGS.copy(), "tasks":DEFAULT_TASKS.copy(), "wds":[]}
    try:
        with open(DB_FILE,"r",encoding="utf-8") as f:
            db=json.load(f)
        db.setdefault("users",{})
        db.setdefault("wds",[])
        db.setdefault("tasks",DEFAULT_TASKS.copy())
        s=db.setdefault("settings",{})
        for k,v in DEFAULT_SETTINGS.items():
            if k not in s: s[k]=v
        return db
    except:
        return {"users":{}, "settings":DEFAULT_SETTINGS.copy(), "tasks":DEFAULT_TASKS.copy(), "wds":[]}

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False,indent=2)

@app.route('/api/init',methods=['POST'])
def api_init():
    db=load_db()
    d=request.json or {}
    uid=str(d.get("id") or d.get("uid") or "").strip()
    name=d.get("name") or "User"
    if not uid: return jsonify({"error":"No ID"}),400
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":name,"bal":20.3,"c_today":0,"p_today":0,"last_date":str(date.today()),"last_time":0,"ref_by":None,"refs":0,"tasks_done":[]}
    u=db["users"][uid]
    today=str(date.today())
    if u.get("last_date")!=today:
        u["c_today"]=0; u["p_today"]=0; u["last_date"]=today
    u["name"]=name
    save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"tasks":db.get("tasks",[])})

@app.route('/api/ads',methods=['POST'])
def api_ads():
    db=load_db()
    d=request.json or {}
    uid=str(d.get("id") or d.get("uid") or "").strip()
    typ=str(d.get("type") or "c").lower()
    if not uid: return jsonify({"msg":"❌ Reload দিন","bal":0})
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":"User","bal":20.3,"c_today":0,"p_today":0,"last_date":str(date.today()),"last_time":0,"ref_by":None,"refs":0,"tasks_done":[]}
    s=db["settings"]; u=db["users"][uid]
    today=str(date.today())
    if u.get("last_date")!=today:
        u["c_today"]=0; u["p_today"]=0; u["last_date"]=today
    now=time.time()
    if now - float(u.get("last_time",0)) < 15:
        return jsonify({"msg":f"⏳ {int(15-(now-float(u.get('last_time',0))))}s অপেক্ষা","bal":u["bal"],"c_today":u["c_today"],"p_today":u["p_today"]})
    if typ=="c" and int(u.get("c_today",0))>=int(s.get("clim",30)):
        return jsonify({"msg":"❌ Company লিমিট শেষ","bal":u["bal"]})
    if typ=="p" and int(u.get("p_today",0))>=int(s.get("plim",50)):
        return jsonify({"msg":"❌ Popup লিমিট শেষ","bal":u["bal"]})
    reward=float(s.get("ad",0.25) if typ=="c" else s.get("pop",0.2))
    u["bal"]=round(float(u.get("bal",0))+reward,3)
    if typ=="c": u["c_today"]=int(u.get("c_today",0))+1
    else: u["p_today"]=int(u.get("p_today",0))+1
    u["last_time"]=now
    save_db(db)
    return jsonify({"msg":f"✅ +{reward} ৳ যোগ হয়েছে","bal":u["bal"],"c_today":u["c_today"],"p_today":u["p_today"]})

@app.route('/api/pop',methods=['POST'])
def api_pop():
    d=request.json or {}
    d["type"]="p"
    request._cached_json=(d,d)
    return api_ads()

@app.route('/api/task',methods=['POST'])
def api_task():
    db=load_db()
    d=request.json or {}
    uid=str(d.get("id") or "").strip()
    tid=d.get("task_id")
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    u=db["users"][uid]
    if tid in u.get("tasks_done",[]): return jsonify({"msg":"Already done"})
    task=next((t for t in db.get("tasks",[]) if t["id"]==tid),None)
    if not task: return jsonify({"msg":"Task not found"})
    reward=float(task.get("reward",0.2))
    u["bal"]=round(float(u.get("bal",0))+reward,3)
    u.setdefault("tasks_done",[]).append(tid)
    save_db(db)
    return jsonify({"msg":f"✅ +{reward} ৳","bal":u["bal"]})

@app.route('/api/withdraw',methods=['POST'])
def api_withdraw():
    db=load_db()
    d=request.json or {}
    uid=str(d.get("id") or "").strip()
    amount=float(d.get("amount") or 0)
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    u=db["users"][uid]
    min_wd=float(db["settings"].get("min",500))
    if amount < min_wd: return jsonify({"msg":f"❌ Minimum {min_wd} ৳"})
    if float(u.get("bal",0)) < amount: return jsonify({"msg":"❌ Balance কম"})
    u["bal"]-=amount
    db["wds"].append({"uid":uid,"name":u.get("name"),"amount":amount,"method":d.get("method"),"number":d.get("number"),"date":str(datetime.now()),"status":"pending"})
    save_db(db)
    return jsonify({"msg":"✅ Request Sent","bal":u["bal"]})

@app.route('/api/settings',methods=['GET'])
def get_settings():
    return jsonify(load_db()["settings"])

@app.route('/api/save_settings',methods=['POST'])
def save_settings():
    db=load_db()
    d=request.json or {}
    for k,v in d.items(): db["settings"][k]=v
    save_db(db)
    return jsonify({"msg":"✅ Saved"})

@app.route('/admin')
def admin():
    db=load_db(); s=db["settings"]
    html=f"""
    <html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
    <style>body{{font-family:system-ui;background:#0B0E1C;color:#fff;padding:20px}}input,textarea{{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#151A2D;color:#fff}}button{{padding:12px 20px;background:#8b5cf6;color:#fff;border:none;border-radius:10px;font-weight:700;cursor:pointer;width:100%}}.card{{background:#1A2040;padding:15px;border-radius:15px;margin-bottom:15px}}</style>
    </head><body>
    <h2>Daily Work BD - Admin Control</h2>
    <div class='card'><h3>💰 টাকা বাড়া/কমা - এখান থেকে সব কন্ট্রোল</h3>
    <label>Company Ads টাকা (ad)</label><input id='ad' value='{s.get('ad')}'>
    <label>Popup Ads টাকা (pop)</label><input id='pop' value='{s.get('pop')}'>
    <label>Company Limit (clim)</label><input id='clim' value='{s.get('clim')}'>
    <label>Popup Limit (plim)</label><input id='plim' value='{s.get('plim')}'>
    <label>Withdraw Minimum (min)</label><input id='min' value='{s.get('min')}'>
    <label>Refer Bonus (ref)</label><input id='ref' value='{s.get('ref')}'>
    </div>
    <div class='card'><h3>🔗 Ads Link</h3>
    <label>Direct Link 1</label><input id='direct_link1' value='{s.get('direct_link1')}'>
    <label>Direct Link 2</label><input id='direct_link2' value='{s.get('direct_link2')}'>
    <label>Company Ad ID</label><input id='company_ad_id' value='{s.get('company_ad_id')}'>
    <label>Popup Ad ID</label><input id='popup_ad_id' value='{s.get('popup_ad_id')}'>
    </div>
    <div class='card'><h3>📢 সব নোটিশ</h3>
    <label>Support Notice</label><textarea id='sup_notice'>{s.get('sup_notice')}</textarea>
    <label>Support Bottom Title</label><input id='support_bottom_title' value='{s.get('support_bottom_title')}'>
    <label>Profile Bottom Title</label><input id='profile_bottom_title' value='{s.get('profile_bottom_title')}'>
    <label>Task Bottom Title</label><input id='task_bottom_title' value='{s.get('task_bottom_title')}'>
    <label>Refer Banner</label><input id='ref_banner' value='{s.get('ref_banner')}'>
    </div>
    <button onclick='save()'>💾 Save All Settings</button>
    <p id='msg'></p>
    <div class='card'><h3>Users: {len(db["users"])} | Withdraw: {len(db["wds"])}</h3></div>
    <script>
    async function save(){{
        let data={{}};
        document.querySelectorAll('input,textarea').forEach(e=>{{data[e.id]=e.value}});
        let r=await fetch('/api/save_settings',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}});
        let j=await r.json();
        document.getElementById('msg').innerText=j.msg;
        alert(j.msg);
    }}
    </script>
    </body></html>
    """
    return render_template_string(html)

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    # FIXED FRONTEND - আগে টাকা, পরে লিংক
    return render_template_string(f"""
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:100px}}
.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}}
.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{s['primary']};cursor:pointer;margin-top:10px}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0;z-index:99}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}
</style></head><body>
<div class='glass'>👑 {s['app_name']} | Balance: <span id='bal'>20.3</span>৳ | <span id='c'>0</span>/{s['clim']} | <span id='p'>0</span>/{s['plim']}</div>
<div class='glass'><h3>Company Ads - ৳{s['ad']}</h3><button class='btn' onclick="doAd('c')">Start - ৳{s['ad']}</button></div>
<div class='glass'><h3>Popup Ads - ৳{s['pop']}</h3><button class='btn' onclick="doAd('p')">Watch - ৳{s['pop']}</button></div>
<div class='glass'><p>{s['sup_notice']}</p></div>
<div class='glass'><h3>{s['spon_title']}</h3><p>{s['spon_desc']}</p><button class='btn' onclick="window.open('{s['spon_link']}','_blank')">{s['spon_btn']}</button></div>
<div class='btm'><div class='on'>Home</div><div>Task</div><div>Refer</div><div>Support</div></div>
<script>
let uid = new URLSearchParams(location.search).get('id') || '8807178385';
async function init(){{
 let r=await fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}});
 let j=await r.json();
 if(j.user){{document.getElementById('bal').innerText=j.user.bal; document.getElementById('c').innerText=j.user.c_today; document.getElementById('p').innerText=j.user.p_today;}}
}}
async function doAd(type){{
 // আগে টাকা, তারপর এড - এটাই ফিক্স
 let r=await fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:type}})}});
 let j=await r.json();
 alert(j.msg);
 if(j.bal!==undefined){{document.getElementById('bal').innerText=j.bal;}}
 if(j.c_today!==undefined)document.getElementById('c').innerText=j.c_today;
 if(j.p_today!==undefined)document.getElementById('p').innerText=j.p_today;
 window.open('{s['direct_link1']}' || 'https://google.com','_blank');
}}
init();
</script>
</body></html>
    """)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
