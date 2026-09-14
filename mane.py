# mane.py - FINAL FIXED - Admin ভিতরে নাই, 1st page ঠিক
import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"Premium Diamond","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80}
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[
            {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
            {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},
            {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}
        ]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    return json.load(open(DB,'r',encoding='utf-8'))

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[]}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refl"].append(uid)
    return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')),j.get('ref'));save_db(db);return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"]})

@app.route('/api/task',methods=['POST'])
def task_done():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));tid=int(j.get('tid'))
    if tid not in u["done"]:
        t=next((x for x in db["tasks"] if x["id"]==tid),None);u["done"].append(tid);u["bal"]+=t["reward"];u["total"]+=t["reward"];save_db(db)
    return jsonify({"msg":f"৳{t['reward']} যোগ"})

@app.route('/api/ads',methods=['POST'])
def ads():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));s=db["settings"]
    if j.get('type')=='c': u["c"]+=1;u["bal"]+=s["ad"];u["total"]+=s["ad"]
    else: u["p"]+=1;u["bal"]+=s["pop"];u["total"]+=s["pop"]
    save_db(db);return jsonify({"msg":"Added"})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        if request.form.get('act')=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif request.form.get('act')=='del_task':
            db["tasks"]=[t for t in db["tasks"] if t["id"]!=int(request.form.get('id'))]
        save_db(db)
    rows="".join([f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']}</td><td>৳{t['reward']}</td><td>{t['link'][:25]}</td><td><form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button style='background:red;color:#fff;border:none;padding:4px 8px;border-radius:6px'>Delete</button></form></td></tr>" for t in db["tasks"]])
    return render_template_string(f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui}}.card{{background:#151A2D;padding:14px;border-radius:14px;margin-bottom:12px;border:1px solid #1e293b}} input{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}} table{{width:100%;border-collapse:collapse}} td,th{{border:1px solid #1e293b;padding:6px;font-size:12px}}</style></head><body><h3>Admin - 2nd Page Control</h3><div class='card'><form method='post'><input type='hidden' name='act' value='add_task'><input name='title' placeholder='Title' required><input name='link' placeholder='Link https://' required><input name='reward' type='number' value='20'><input name='icon' placeholder='Icon 📢' value='📢'><button style='background:#8b5cf6;color:#fff;width:100%;margin-top:8px;padding:10px;border:none;border-radius:8px'>Add Task</button></form></div><div class='card'><table><tr><th>ID</th><th>Title</th><th>Reward</th><th>Link</th><th>Del</th></tr>{rows}</table></div><a href='/' style='color:#8b5cf6'>← Back to App</a></body></html>")

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui} body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.glass{background:linear-gradient(135deg,#151A2D,#1A2040);border:1px solid rgba(139,92,246,.2);border-radius:20px;padding:16px;margin:12px;box-shadow:0 8px 30px rgba(0,0,0,.3)}
.btn{width:100%;padding:12px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(135deg,#8b5cf6,#7c3aed);margin-top:8px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(21,26,45,.96);backdrop-filter:blur(15px);display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer}.btm div.on{color:#a78bfa}.btm div span{font-size:20px;display:block}
.page{display:none}.page.active{display:block}
.task-card{display:flex;justify-content:space-between;align-items:center;padding:14px;background:#0F1429;border:1px solid #1e293b;border-radius:14px;margin-top:10px}
</style></head><body>
<div style='padding:14px 16px;display:flex;justify-content:space-between;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b'><b>💎 Premium App</b><b id='bal' style='color:#22c55e'>৳0</b></div>

<div id='p-home' class='page active'>
<div class='glass'><div style='display:flex;justify-content:space-between'><div><small style='color:#a78bfa'>Diamond Member • Level 3</small><br><b>Good Evening, User!</b></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2></div></div></div>
<div style='display:flex;gap:10px;margin:0 12px'><div style='flex:1;background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:16px;padding:14px;border:1px solid rgba(139,92,246,.15)'><div style='width:36px;height:36px;background:#8b5cf6;border-radius:8px;display:flex;align-items:center;justify-content:center'>📢</div><b style='display:block;margin:6px 0'>Company Ads</b><button class='btn' style='padding:8px;font-size:12px' onclick='doAd("c")'>Start Earning</button></div><div style='flex:1;background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:16px;padding:14px;border:1px solid rgba(245,158,11,.15)'><div style='width:36px;height:36px;background:#f59e0b;border-radius:8px;display:flex;align-items:center;justify-content:center'>▶️</div><b style='display:block;margin:6px 0'>Popup Ads</b><button class='btn' style='background:linear-gradient(135deg,#f59e0b,#f97316);padding:8px;font-size:12px' onclick='doAd("p")'>Watch & Earn</button></div></div>
<div class='glass'><h4>💸 Withdraw <span style='float:right;font-size:10px;background:#16a34a30;color:#4ade80;padding:3px 8px;border-radius:8px'>Secure</span></h4><button class='btn' style='background:#6366f1'>Withdraw Now</button></div>
<div style='margin:12px;background:#0F1429;border:1px dashed #f59e0b;border-radius:12px;padding:12px;display:flex;justify-content:space-between;align-items:center'><div><small style='background:#f59e0b;color:#000;padding:2px 6px;border-radius:4px;font-size:9px'>SPONSORED</small><br><b style='font-size:13px'>Company Ads Box</b></div><button style='background:#8b5cf6;color:#fff;border:none;padding:6px 12px;border-radius:8px'>Explore</button></div>
</div>

<div id='p-tasks' class='page'>
<div class='glass'><h4>🎯 Tasks & Company Links</h4><p style='font-size:11px;opacity:.6;margin:6px 0'>Telegram, Company, YouTube লিংক এখানে</p><div id='tList'></div></div>
</div>

<div id='p-refer' class='page'><div class='glass'><h4>👥 Refer</h4><p style='opacity:.6;font-size:12px'>Refer system coming...</p></div></div>
<div id='p-support' class='page'><div class='glass'><h4>💎 Support</h4></div></div>
<div id='p-profile' class='page'><div class='glass'><h4>👤 Profile</h4></div></div>

<div class='btm'>
<div onclick="show('home')" id='b-home' class='on'><span>🏠</span>Home</div>
<div onclick="show('tasks')" id='b-tasks'><span>🎯</span>Tasks</div>
<div onclick="show('refer')" id='b-refer'><span>👥</span>Refer</div>
<div onclick="show('support')" id='b-support'><span>💬</span>Support</div>
<div onclick="show('profile')" id='b-profile'><span>👤</span>Profile</div>
</div>

<script>
let uid=localStorage.getItem('uid'); if(!uid){uid='u_'+Date.now();localStorage.setItem('uid',uid)}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})}).then(r=>r.json()).then(d=>{
document.getElementById('bal').innerText='৳'+d.user.bal; document.getElementById('bal2').innerText='৳'+d.user.bal;
let tl=''; d.tasks.forEach(t=>{
let done=d.user.done.includes(t.id);
tl+=`<div class='task-card'><div style='display:flex;gap:10px;align-items:center'><div style='font-size:22px'>${t.icon}</div><div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`;
}); document.getElementById('tList').innerHTML=tl;
})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doAd(t){fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(r=>r.json()).then(d=>{load()})}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
load()
</script></body></html>
    """)

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
