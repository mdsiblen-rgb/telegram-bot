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
    "ad": 0.25, "pop": 0.20, "clim": 30, "plim": 50, "min": 500, "ref": 10,
    "company_ad_id": "11764581", "popup_ad_id": "11798857",
    "direct_link1": "https://omg10.com/4/11760259", "direct_link2": "",
    "home_corner_diamond": "💎", "home_small_diamond_icon": "💎",
    "home_diamond_big_size": "28", "home_name_font_size": "20",
    "spon_title": "Biggest Earning Offer", "spon_desc": "প্রতিদিন কাজ করে আয় করুন",
    "spon_link": "https://google.com", "spon_btn": "Claim Now", "spon_big_height": "180",
    "task_page_title": "Tasks & Company Links", "task_page_sub": "প্রতি Task এ ৳20-25 + Diamond",
    "task_bottom_title": "Special Offer", "task_bottom_desc": "Admin থেকে চেঞ্জ হবে",
    "task_bottom_btn": "Claim Now", "task_bottom_link": "https://google.com",
    "ref_title": "Refer & Earn", "ref_desc": "বন্ধুদের Invite করে Unlimited আয়",
    "ref_banner": "Refer Contest চলছে! - ৳5000", "ref_rules": "1. লিংক শেয়ার 2. Join ৳20 3. 15% Commission",
    "refer_bottom_title": "Refer Special Bonus", "refer_bottom_desc": "Admin থেকে অফার",
    "refer_bottom_btn": "Join Now", "refer_bottom_link": "https://google.com",
    "sup_title": "Support Center", "sup_desc": "24/7 সাপোর্ট",
    "sup_tg": "https://t.me/dailyworkbd", "sup_wa": "https://wa.me/8801", "sup_fb": "https://facebook.com", "sup_email": "support@dailyworkbd.com",
    "sup_notice": "রাত ১০টার পর Withdraw বন্ধ", "sup_faq1_q": "Withdraw কতক্ষণে?", "sup_faq1_a": "২৪ ঘণ্টায়", "sup_faq2_q": "Refer টাকা কখন?", "sup_faq2_a": "Join করলেই", "sup_faq3_q": "Ads সমস্যা?", "sup_faq3_a": "VPN ছাড়া দেখুন",
    "sup_rules": "1. এক আইডি 2. ফেক ব্যান", "support_bottom_title": "Important Notice", "support_bottom_desc": "Admin থেকে কন্ট্রোল", "support_bottom_btn": "Contact Now", "support_bottom_link": "https://t.me/",
    "profile_bottom_title": "VIP Membership", "profile_bottom_desc": "VIP হলে বেশি ইনকাম", "profile_bottom_btn": "Upgrade Now", "profile_bottom_link": "https://google.com"
}
DEFAULT_TASKS = [
    {"id":"t1","icon":"🌐","title":"Visit Company - ৳20","reward":0.2,"link":"https://google.com"},
    {"id":"t2","icon":"🎥","title":"Watch Video - ৳25","reward":0.25,"link":"https://youtube.com"},
    {"id":"t3","icon":"📢","title":"Join Telegram - ৳30","reward":0.3,"link":"https://t.me/"}
]

def load_db():
    if not os.path.exists(DB_FILE): return {"users":{}, "settings":DEFAULT_SETTINGS.copy(), "tasks":DEFAULT_TASKS.copy(), "wds":[]}
    try:
        with open(DB_FILE,"r",encoding="utf-8") as f: db=json.load(f)
        db.setdefault("users",{}); db.setdefault("wds",[]); db.setdefault("tasks",DEFAULT_TASKS.copy())
        s=db.setdefault("settings",{})
        for k,v in DEFAULT_SETTINGS.items():
            if k not in s: s[k]=v
        return db
    except: return {"users":{}, "settings":DEFAULT_SETTINGS.copy(), "tasks":DEFAULT_TASKS.copy(), "wds":[]}

def save_db(db):
    with open(DB_FILE,"w",encoding="utf-8") as f: json.dump(db,f,ensure_ascii=False,indent=2)

@app.route('/api/init',methods=['POST'])
def api_init():
    db=load_db(); d=request.json or {}; uid=str(d.get("id") or "").strip(); name=d.get("name") or "User"
    if not uid: return jsonify({"error":"no id"}),400
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":name,"bal":20.3,"c_today":0,"p_today":0,"last_date":str(date.today()),"last_time":0,"refs":0,"tasks_done":[]}
    u=db["users"][uid]; today=str(date.today())
    if u.get("last_date")!=today: u["c_today"]=0; u["p_today"]=0; u["last_date"]=today
    save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})

@app.route('/api/ads',methods=['POST'])
def api_ads():
    db=load_db(); d=request.json or {}; uid=str(d.get("id") or "").strip(); typ=str(d.get("type") or "c").lower()
    if not uid: return jsonify({"msg":"Reload","bal":0})
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":"User","bal":20.3,"c_today":0,"p_today":0,"last_date":str(date.today()),"last_time":0,"refs":0,"tasks_done":[]}
    s=db["settings"]; u=db["users"][uid]; now=time.time()
    if now-float(u.get("last_time",0))<15: return jsonify({"msg":f"⏳ {int(15-(now-float(u.get('last_time',0))))}s","bal":u["bal"]})
    reward=float(s.get("ad",0.25) if typ=="c" else s.get("pop",0.2))
    u["bal"]=round(float(u.get("bal",0))+reward,3)
    if typ=="c": u["c_today"]+=1
    else: u["p_today"]+=1
    u["last_time"]=now; save_db(db)
    return jsonify({"msg":f"✅ +{reward}৳","bal":u["bal"],"c_today":u["c_today"],"p_today":u["p_today"]})

@app.route('/api/pop',methods=['POST'])
def api_pop(): d=request.json or {}; d["type"]="p"; request._cached_json=(d,d); return api_ads()

@app.route('/api/task',methods=['POST'])
def api_task():
    db=load_db(); d=request.json or {}; uid=str(d.get("id") or "").strip(); tid=d.get("task_id")
    if uid not in db["users"]: return jsonify({"msg":"User not found"})
    u=db["users"][uid]
    if tid in u.get("tasks_done",[]): return jsonify({"msg":"Already Done"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    if not t: return jsonify({"msg":"Task not found"})
    u["bal"]=round(u["bal"]+float(t["reward"]),3); u["tasks_done"].append(tid); save_db(db)
    return jsonify({"msg":"✅ Task Done","bal":u["bal"]})

@app.route('/api/withdraw',methods=['POST'])
def api_withdraw():
    db=load_db(); d=request.json or {}; uid=str(d.get("id") or "").strip(); amount=float(d.get("amount") or 0)
    u=db["users"].get(uid)
    if not u: return jsonify({"msg":"User not found"})
    if amount<float(db["settings"]["min"]): return jsonify({"msg":f"Minimum {db['settings']['min']}৳"})
    if u["bal"]<amount: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amount; db["wds"].append({"uid":uid,"amount":amount,"method":d.get("method"),"number":d.get("number"),"date":str(datetime.now())}); save_db(db)
    return jsonify({"msg":"✅ Withdraw Request Sent","bal":u["bal"]})

@app.route('/api/save_settings',methods=['POST'])
def save_settings(): db=load_db(); db["settings"].update(request.json or {}); save_db(db); return jsonify({"msg":"Saved"})
@app.route('/api/settings',methods=['GET'])
def get_settings(): return jsonify(load_db()["settings"])

@app.route('/admin')
def admin():
    db=load_db(); s=db["settings"]
    h=f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;font-family:system-ui;padding:15px}}input,textarea{{width:100%;padding:10px;margin:5px 0;background:#151A2D;color:#fff;border:1px solid #333;border-radius:8px}}button{{width:100%;padding:14px;background:#8b5cf6;color:#fff;border:none;border-radius:10px;font-weight:700}}</style></head><body><h2>Admin - টাকা বাড়া/কমা</h2>Company ৳<input id='ad' value='{s['ad']}'> Popup ৳<input id='pop' value='{s['pop']}'> Company Limit<input id='clim' value='{s['clim']}'> Popup Limit<input id='plim' value='{s['plim']}'> Min Withdraw<input id='min' value='{s['min']}'> Refer Bonus<input id='ref' value='{s['ref']}'> Direct Link1<input id='direct_link1' value='{s['direct_link1']}'> Notice<textarea id='sup_notice'>{s['sup_notice']}</textarea><button onclick='save()'>Save</button><p id='m'></p><script>async function save(){{let d={{}};document.querySelectorAll('input,textarea').forEach(e=>d[e.id]=e.value);let r=await fetch('/api/save_settings',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}});let j=await r.json();document.getElementById('m').innerText=j.msg;alert(j.msg)}}</script></body></html>"
    return render_template_string(h)

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    return render_template_string(f"""
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}}body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:110px}}
.glass{{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}}
.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:{s['primary']};cursor:pointer;margin-top:10px}}
.page{{display:none}}.page.active{{display:block}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:10px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.btm div span{{font-size:20px;display:block}}
.inputDark{{width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px}}
.task-card{{display:flex;justify-content:space-between;align-items:center;padding:16px;background:#0F1429;border:1px solid #1e293b;border-radius:18px;margin:10px 12px}}
</style></head><body>
<div class='glass'>👑 {s['app_name']} | Balance: <span id='bal'>20.3</span>৳ | <span id='c'>0</span>/{s['clim']} | <span id='p'>0</span>/{s['plim']}</div>

<div id='p-home' class='page active'>
<div class='glass'><h3>Company Ads - ৳{s['ad']}</h3><button class='btn' onclick="doAd('c')">Start - ৳{s['ad']}</button></div>
<div class='glass'><h3>Popup Ads - ৳{s['pop']}</h3><button class='btn' onclick="doAd('p')">Watch - ৳{s['pop']}</button></div>
<div class='glass'>{s['sup_notice']}</div>
<div class='glass'><h3>{s['spon_title']}</h3><p>{s['spon_desc']}</p><button class='btn' onclick="window.open('{s['spon_link']}','_blank')">{s['spon_btn']}</button></div>
</div>

<div id='p-task' class='page'>
<div class='glass'><h3>{s['task_page_title']}</h3><p>{s['task_page_sub']}</p></div>
<div id='taskList'></div>
<div class='glass'><h3>{s['task_bottom_title']}</h3><p>{s['task_bottom_desc']}</p><button class='btn' onclick="window.open('{s['task_bottom_link']}','_blank')">{s['task_bottom_btn']}</button></div>
</div>

<div id='p-refer' class='page'>
<div class='glass'><h3>{s['ref_title']}</h3><p>{s['ref_desc']}</p><p style='background:linear-gradient(90deg,#f59e0b,#f97316);color:#000;padding:10px;border-radius:10px;margin-top:10px;font-weight:800'>{s['ref_banner']}</p><p style='margin-top:10px;white-space:pre-line'>{s['ref_rules']}</p><button class='btn' onclick="copyRef()">Copy Refer Link</button></div>
<div class='glass'><h3>{s['refer_bottom_title']}</h3><p>{s['refer_bottom_desc']}</p><button class='btn' onclick="window.open('{s['refer_bottom_link']}','_blank')">{s['refer_bottom_btn']}</button></div>
</div>

<div id='p-support' class='page'>
<div class='glass'><h3>{s['sup_title']}</h3><p>{s['sup_desc']}</p><p style='margin-top:10px;white-space:pre-line;background:#0B0E1C;padding:12px;border-radius:12px'>{s['sup_notice']}</p></div>
<div class='glass'><p><b>{s['sup_faq1_q']}</b><br>{s['sup_faq1_a']}</p><br><p><b>{s['sup_faq2_q']}</b><br>{s['sup_faq2_a']}</p><br><p><b>{s['sup_faq3_q']}</b><br>{s['sup_faq3_a']}</p></div>
<div class='glass'><h3>{s['support_bottom_title']}</h3><p>{s['support_bottom_desc']}</p><button class='btn' onclick="window.open('{s['support_bottom_link']}','_blank')">{s['support_bottom_btn']}</button></div>
</div>

<div id='p-profile' class='page'>
<div class='glass' style='text-align:center'><div style='width:80px;height:80px;border-radius:20px;background:#0B0E1C;border:2px solid #8b5cf6;display:flex;align-items:center;justify-content:center;font-size:36px;margin:0 auto'>👑</div><h3 id='pname' style='margin-top:10px'>User</h3><p>Balance: <span id='bal2'>20.3</span>৳</p></div>
<div class='glass'><h3>Withdraw</h3><select id='method' class='inputDark'><option>bKash</option><option>Nagad</option></select><input id='number' class='inputDark' placeholder='Number'><input id='amount' class='inputDark' type='number' placeholder='Amount Min {s['min']}'><button class='btn' onclick="withdraw()">Withdraw Now</button></div>
<div class='glass'><h3>{s['profile_bottom_title']}</h3><p>{s['profile_bottom_desc']}</p><button class='btn' onclick="window.open('{s['profile_bottom_link']}','_blank')">{s['profile_bottom_btn']}</button></div>
</div>

<div class='btm'>
<div id='b-home' class='on' onclick="show('home')"><span>🏠</span>Home</div>
<div id='b-task' onclick="show('task')"><span>🎯</span>Task</div>
<div id='b-refer' onclick="show('refer')"><span>👥</span>Refer</div>
<div id='b-support' onclick="show('support')"><span>💬</span>Support</div>
<div id='b-profile' onclick="show('profile')"><span>👤</span>Profile</div>
</div>

<script>
let uid = new URLSearchParams(location.search).get('id') || '8807178385';
let tasks = [];
function show(p){{document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on'));document.getElementById('b-'+p).classList.add('on');}}
async function init(){{
 let r=await fetch('/api/init',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid}})}});
 let j=await r.json();
 if(j.user){{document.getElementById('bal').innerText=j.user.bal;document.getElementById('bal2').innerText=j.user.bal;document.getElementById('c').innerText=j.user.c_today;document.getElementById('p').innerText=j.user.p_today;document.getElementById('pname').innerText=j.user.name||'User';}}
 tasks=j.tasks||[]; let html=''; tasks.forEach(t=>{{html+=`<div class='task-card'><div><span>${{t.icon||'🌐'}}</span> ${{t.title}}</div><button class='btn' style='width:auto;padding:8px 14px' onclick="doTask('${{t.id}}','${{t.link}}')">Go</button></div>`}}); document.getElementById('taskList').innerHTML=html;
}}
async function doAd(type){{
 let r=await fetch('/api/ads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,type:type}})}});
 let j=await r.json(); alert(j.msg);
 if(j.bal!==undefined){{document.getElementById('bal').innerText=j.bal;document.getElementById('bal2').innerText=j.bal;}}
 if(j.c_today!==undefined)document.getElementById('c').innerText=j.c_today;
 if(j.p_today!==undefined)document.getElementById('p').innerText=j.p_today;
 window.open('{s['direct_link1']}' || 'https://google.com','_blank');
}}
async function doTask(id,link){{
 let r=await fetch('/api/task',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,task_id:id}})}});
 let j=await r.json(); alert(j.msg); if(j.bal){{document.getElementById('bal').innerText=j.bal;document.getElementById('bal2').innerText=j.bal;}} window.open(link,'_blank');
}}
function copyRef(){{let l=location.origin+'/?start='+uid; navigator.clipboard.writeText(l); alert('Copied: '+l);}}
async function withdraw(){{let m=document.getElementById('method').value; let n=document.getElementById('number').value; let a=document.getElementById('amount').value; let r=await fetch('/api/withdraw',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:uid,method:m,number:n,amount:a}})}}); let j=await r.json(); alert(j.msg); if(j.bal){{document.getElementById('bal').innerText=j.bal;document.getElementById('bal2').innerText=j.bal;}}}}
init();
</script>
</body></html>
""")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
