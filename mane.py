import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={"app_name":"Premium","bonus":100,"ad":3,"pop":5,"clim":50,"plim":30,"min":300,"ref":80,"zone":"11764581"}
    if not os.path.exists(DB):
        data={
            "users":{},
            "wds":[],
            "settings":d,
            "tasks":[
                {"id":1,"title":"📢 Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
                {"id":2,"title":"🏢 Company Link","reward":25,"link":"https://google.com","icon":"🏢"},
                {"id":3,"title":"▶️ YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}
            ]
        }
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2))
        return data
    db=json.load(open(DB,'r',encoding='utf-8'))
    return db

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))

def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[]}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refl"].append(uid)
    return db["users"][uid]

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;uid=str(j.get('id'));ref=j.get('ref')
    u=get_user(db,uid,ref)
    if u["last"]!=str(datetime.now().date()): u["c"]=0;u["p"]=0;u["last"]=str(datetime.now().date())
    save_db(db); return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"]})

@app.route('/api/task',methods=['POST'])
def task_done():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));tid=int(j.get('tid'))
    if tid in u["done"]: return jsonify({"msg":"Already Done"})
    t=next((x for x in db["tasks"] if x["id"]==tid),None)
    if not t: return jsonify({"msg":"Not found"})
    u["done"].append(tid); u["bal"]+=t["reward"]; u["total"]+=t["reward"]; save_db(db)
    return jsonify({"msg":f"৳{t['reward']} যোগ হয়েছে"})

@app.route('/api/ads',methods=['POST'])
def ads():
    db=load_db();j=request.json;u=get_user(db,str(j.get('id')));s=db["settings"]
    if j.get('type')=='c':
        u["c"]+=1; u["bal"]+=s["ad"]; u["total"]+=s["ad"]
    else:
        u["p"]+=1; u["bal"]+=s["pop"]; u["total"]+=s["pop"]
    save_db(db); return jsonify({"msg":"Balance Added"})

# ========== ADMIN PANEL ==========
@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        act=request.form.get('act')
        if act=='add_task':
            new_id=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({
                "id":new_id,
                "title":request.form.get('title'),
                "reward":int(request.form.get('reward',20)),
                "link":request.form.get('link'),
                "icon":request.form.get('icon','🔗')
            })
        elif act=='del_task':
            tid=int(request.form.get('id'))
            db["tasks"]=[t for t in db["tasks"] if t["id"]!=tid]
        elif act=='update_set':
            for k in db["settings"]:
                if k in request.form:
                    try: db["settings"][k]=int(request.form.get(k))
                    except: db["settings"][k]=request.form.get(k)
        save_db(db)
    tasks_html=""
    for t in db["tasks"]:
        tasks_html+=f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']}</td><td>৳{t['reward']}</td><td style='max-width:120px;overflow:hidden'>{t['link'][:30]}</td><td><form method='post' style='display:inline'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button style='background:red;color:#fff;border:none;padding:4px 8px;border-radius:6px'>Delete</button></form></td></tr>"

    return render_template_string(f"""
    <html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>
    body{{background:#0B0E1C;color:#fff;font-family:system-ui;padding:16px;max-width:700px;margin:auto}}
   .card{{background:#151A2D;border:1px solid #1e293b;border-radius:14px;padding:14px;margin-bottom:12px}}
    input{{width:100%;padding:10px;border-radius:8px;border:1px solid #1e293b;background:#0B0E1C;color:#fff;margin-top:6px}}
    button{{padding:10px 16px;border:none;border-radius:8px;font-weight:700;cursor:pointer}}
    table{{width:100%;border-collapse:collapse;margin-top:10px}} td,th{{border:1px solid #1e293b;padding:8px;font-size:12px}} th{{background:#0B0E1C}}
    </style></head><body>
    <h2>⚙️ Admin Panel - 2nd Page Control</h2>
    <div class='card'>
        <h4>➕ নতুন লিংক যোগ করুন (Telegram / Company / YouTube)</h4>
        <form method='post'>
            <input type='hidden' name='act' value='add_task'>
            <input name='title' placeholder='Title যেমন: Join Telegram Group' required>
            <input name='link' placeholder='Link যেমন: https://t.me/yourgroup' required>
            <input name='reward' type='number' placeholder='Reward 20' value='20'>
            <input name='icon' placeholder='Icon 📢 🏢 ▶️' value='📢'>
            <button style='background:#8b5cf6;color:#fff;width:100%;margin-top:8px'>Add Task</button>
        </form>
    </div>
    <div class='card'>
        <h4>📋 বর্তমান Tasks (2nd Page এ যা দেখাবে)</h4>
        <table><tr><th>ID</th><th>Title</th><th>Reward</th><th>Link</th><th>Action</th></tr>{tasks_html}</table>
    </div>
    <a href='/'><button style='background:#334155;color:#fff;width:100%'>← User App দেখুন</button></a>
    </body></html>
    """)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.glass{background:linear-gradient(135deg,#151A2D,#1A2040);border:1px solid rgba(139,92,246,.2);border-radius:20px;padding:16px;margin:12px}
.btn{width:100%;padding:13px;border:none;border-radius:12px;font-weight:800;color:#fff;background:linear-gradient(135deg,#8b5cf6,#7c3aed);margin-top:8px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer}.btm div.on{color:#a78bfa}.btm div span{font-size:20px;display:block}
.page{display:none}.page.active{display:block}
.task-card{display:flex;justify-content:space-between;align-items:center;padding:14px;background:#0F1429;border:1px solid #1e293b;border-radius:14px;margin-top:10px}
</style></head><body>

<div style='padding:14px 16px;display:flex;justify-content:space-between;background:#0F1429;position:sticky;top:0;z-index:99'><b>💎 Premium App</b><b id='bal' style='color:#22c55e'>৳0</b></div>

<div id='p-home' class='page active'>
<div class='glass'><h4>💰 Balance</h4><h1 id='bal2' style='color:#22c55e'>৳0</h1><button class='btn' onclick='doAd("c")'>Company Ads</button><button class='btn' style='background:linear-gradient(135deg,#f59e0b,#f97316)' onclick='doAd("p")'>Popup Ads</button></div>
</div>

<div id='p-tasks' class='page active'>
<div class='glass'>
<h4>🎯 Tasks & Company Links</h4>
<p style='font-size:11px;opacity:.6;margin:6px 0'>Telegram Group, Company Link, YouTube সব এখানে আসবে</p>
<div id='tList'></div>
</div>
</div>

<div class='btm'>
<div onclick="show('home')" id='b-home'><span>🏠</span>Home</div>
<div onclick="show('tasks')" id='b-tasks' class='on'><span>🎯</span>Tasks</div>
<div onclick="location.href='/admin'"><span>⚙️</span>Admin</div>
<div><span>👥</span>Refer</div>
<div><span>👤</span>Profile</div>
</div>

<script>
let uid=localStorage.getItem('uid'); if(!uid){uid='u_'+Date.now();localStorage.setItem('uid',uid)}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})}).then(r=>r.json()).then(d=>{
document.getElementById('bal').innerText='৳'+d.user.bal; document.getElementById('bal2').innerText='৳'+d.user.bal;
let tl=''; d.tasks.forEach(t=>{
let done=d.user.done.includes(t.id);
tl+=`<div class='task-card'><div><div style='font-size:18px'>${t.icon}</div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward}</small></div><button class='btn' style='width:auto;padding:8px 16px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`;
}); document.getElementById('tList').innerHTML=tl;
})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doAd(t){fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
load()
</script></body></html>
    """)

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
