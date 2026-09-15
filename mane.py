from flask import Flask, request, jsonify, render_template_string
import json, os, base64
from datetime import datetime
app = Flask(__name__)
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "settings": {
            "app_name": "প্রতিদিনের কাজ বিডি", "primary": "#8b5cf6", "secondary": "#f59e0b",
            "ad": 0.5, "pop": 0.3, "clim": 80, "plim": 80, "min": 200, "ref": 20,
            "company_ad_id": "11760259",
            "direct_link1": "https://omg10.com/4/11760259",
            "direct_link2": "https://www.profitablecpmrate.com/f2v8tu11?key=a1998c4e8a19d594fced08b38af06b9e",
            "home_corner_diamond": "💎", "home_small_diamond_icon": "💎", "home_diamond_big_size": "28", "home_name_font_size": "20",
            "spon_title": "Biggest Earning Offer", "spon_desc": "প্রতিদিন কাজ করে আয় করুন", "spon_link": "https://google.com", "spon_btn": "Claim Now", "spon_big_height": "200",
            "task_bottom_title": "Special Offer", "task_bottom_desc": "Admin Box", "task_bottom_btn": "Claim", "task_bottom_link": "https://google.com",
            "refer_bottom_title": "Bonus", "refer_bottom_desc": "Admin Box", "refer_bottom_btn": "Join", "refer_bottom_link": "https://google.com",
            "support_bottom_title": "Update", "support_bottom_desc": "Admin Box", "support_bottom_btn": "Contact", "support_bottom_link": "https://t.me/",
            "profile_bottom_title": "VIP", "profile_bottom_desc": "VIP Offer", "profile_bottom_btn": "Upgrade", "profile_bottom_link": "https://google.com"
        }, "tasks": [
            {"id":"t1","icon":"🌐","title":"Visit Company","reward":0.2,"link":"https://google.com"},
            {"id":"t2","icon":"▶️","title":"Watch Video","reward":0.25,"link":"https://youtube.com"}
        ], "wds": []}
    with open(DB_FILE,"r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE,"w") as f:
        json.dump(db,f,indent=2)

HTML = """
<!DOCTYPE html>
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='//libtl.com/sdk.js' data-zone='11760259' data-sdk='show_11760259'></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}
.glass{background:#1A2040;border:1px solid #2a2f4a;border-radius:22px;padding:18px;margin:12px}
.top2{display:flex;gap:10px;margin:12px;align-items:center}
.topbox{flex:1;background:#151A2D;border:1px solid #8b5cf6;padding:12px;border-radius:14px;font-weight:700}
.cornerDiamond{width:60px;height:60px;background:#1A2040;border:2px solid #8b5cf6;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:36px}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;background:#8b5cf6;cursor:pointer;margin-top:10px}
.meth{flex:1;padding:12px;border-radius:14px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C;font-weight:800}.meth.on{border-color:#8b5cf6;background:rgba(139,92,246,.25)}
.inputDark{width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f4a;background:#0B0E1C;color:#fff;margin-top:10px}
.task-card{display:flex;justify-content:space-between;align-items:center;padding:16px;background:#0F1429;border:1px solid #1e293b;border-radius:18px;margin:10px 12px}
.proImg{width:92px;height:92px;border-radius:22px;background:#0B0E1C;border:2px solid #8b5cf6;display:flex;align-items:center;justify-content:center;font-size:40px;overflow:hidden;margin:0 auto}
.stat4{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}.stat4 div{background:#0B0E1C;border:1px solid #1e293b;padding:14px;border-radius:16px;text-align:center}
.spon-big{background:linear-gradient(135deg,#2D1B4E,#1A1033);border:2px solid #f59e0b;padding:36px 22px;border-radius:26px;margin:16px;min-height:200px}
.page{display:none}.page.active{display:block}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:12px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:11px;font-weight:700;cursor:pointer}.btm div.on{color:#8b5cf6}.btm div span{font-size:22px;display:block}
</style></head><body>
<div id='p-home' class='page active'>
  <div class='top2'><div class='cornerDiamond'>💎</div><div class='topbox'>প্রতিদিনের কাজ বিডি</div><div class='topbox' style='border-color:#f59e0b'>Daily Work BD <span id='balTopRight' style='float:right;color:#22c55e'>0</span></div></div>
  <div class='glass'><div style='display:flex;justify-content:space-between'><span style='color:#a78bfa;font-size:20px;font-weight:800'>Diamond Member</span><div style='text-align:right'><span style='opacity:.7'>Balance</span><br><b id='balTopBalance' style='color:#22c55e;font-size:20px'>0</b></div></div><b id='balShow' style='color:#22c55e;font-size:36px;display:block;margin-top:8px'>0</b><div style='margin-top:10px;display:flex;align-items:center;gap:10px'><span style='font-size:28px'>💎</span><span style='font-size:20px;font-weight:800'><span id='diamondTop'>0</span> Diamond | <span id='adsCount'>0/80</span> Ads</span></div></div>
  <div style='display:flex;gap:10px;margin:0 12px'><div class='glass' style='flex:1;margin:0'><b>Company Ads 0.5</b><br><small id='cToday'>0/80</small><button class='btn' id='btnC' onclick='watchAd("c")'>Start - 0.5</button></div><div class='glass' style='flex:1;margin:0'><b>Popup Ads 0.3</b><br><small id='pToday'>0/80</small><button class='btn' id='btnP' style='background:#f59e0b;color:#000' onclick='watchAd("p")'>Watch - 0.3</button></div></div>
  <div class='glass'><h3>Withdraw</h3><div style='display:flex;gap:10px;margin-top:12px'><div class='meth on' id='m-bKash' onclick="setMeth('bKash')">bKash</div><div class='meth' id='m-Nagad' onclick="setMeth('Nagad')">Nagad</div></div><input id='wNum' class='inputDark' placeholder='01XXXXXXXXXX' /><input id='wAmt' class='inputDark' type='number' placeholder='Min 200' /><button class='btn' onclick='doWD()'>Withdraw Now</button></div>
  <div class='spon-big'><h2>Biggest Earning Offer</h2><p style='font-size:18px;margin-top:10px'>প্রতিদিন কাজ করে আয় করুন</p><button class='btn' style='background:#f59e0b;color:#000;margin-top:16px' onclick="window.open('https://google.com')">Claim Now</button></div>
</div>
<div id='p-tasks' class='page'><div class='glass'><h2>Tasks</h2><div id='tasksList'></div></div></div>
<div id='p-refer' class='page'><div class='glass'><h2>Refer</h2><div id='refLinkBox'>Loading</div><button class='btn' onclick='copyRef()'>Copy Link</button></div></div>
<div id='p-support' class='page'><div class='glass'><h2>Support</h2><p>24/7 Support</p></div></div>
<div id='p-profile' class='page'><div class='glass'><h2>Profile</h2><div id='accId'>Loading</div><input id='accNameInput' class='inputDark' placeholder='Name'/><input type='file' id='accPhoto' accept='image/*' class='inputDark' onchange='previewPhoto(this)'/><div id='previewWrap' style='display:none;margin-top:8px'><img id='previewImg' style='width:90px;height:90px;border-radius:12px;object-fit:cover'></div><button class='btn' onclick='saveProfile()'>Save Profile</button></div></div>
<div class='btm'><div class='on' id='b-home' onclick="showP('home')"><span>🏠</span>Home</div><div id='b-tasks' onclick="showP('tasks')"><span>🎯</span>Tasks</div><div id='b-refer' onclick="showP('refer')"><span>👥</span>Refer</div><div id='b-support' onclick="showP('support')"><span>💬</span>Support</div><div id='b-profile' onclick="showP('profile')"><span>👤</span>Profile</div></div>
<script>
let curMeth='bKash'; let uid=localStorage.getItem('uid')||'8807178385_4250'; localStorage.setItem('uid',uid);
function setMeth(m){curMeth=m;document.querySelectorAll('.meth').forEach(e=>e.classList.remove('on'));document.getElementById('m-'+m).classList.add('on');}
function showP(id){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p-'+id).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));document.getElementById('b-'+id).classList.add('on'); if(id=='tasks') loadTasks(); init();}
function watchAd(t){
  let btn=document.getElementById(t=='c'?'btnC':'btnP');
  let directLink=t=='c'?'https://omg10.com/4/11760259':'https://www.profitablecpmrate.com/f2v8tu11?key=a1998c4e8a19d594fced08b38af06b9e';
  btn.innerText='Ad Loading...'; btn.disabled=true;
  window.open(directLink,'_blank');
  let adFunc=window['show_11760259'];
  if(typeof adFunc==='function'){
    adFunc().then(function(){ doReward(t); }).catch(function(){ setTimeout(function(){ doReward(t); },3000); });
  } else {
    setTimeout(function(){ doReward(t); },4000);
  }
}
function doReward(t){
  fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})})
 .then(function(r){return r.json();}).then(function(d){
    alert(d.msg);
    document.getElementById('btnC').innerText='Start - 0.5'; document.getElementById('btnC').disabled=false;
    document.getElementById('btnP').innerText='Watch - 0.3'; document.getElementById('btnP').disabled=false;
    init();
  });
}
function doWD(){let n=document.getElementById('wNum').value;let a=document.getElementById('wAmt').value; if(!n||!a) return alert('Number'); fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,amt:a,num:n,m:curMeth})}).then(function(r){return r.json();}).then(function(d){alert(d.msg);});}
function loadTasks(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})}).then(function(r){return r.json();}).then(function(d){let h=''; for(let i=0;i<d.tasks.length;i++){let t=d.tasks[i]; h+="<div class='task-card'><div><b>"+t.icon+" "+t.title+"</b><div style='color:#22c55e'>"+t.reward+"</div></div><button style='background:#8b5cf6;color:#fff;border:none;padding:10px 20px;border-radius:20px' onclick=\\"window.open('"+t.link+"','_blank')\\">Go</button></div>";} document.getElementById('tasksList').innerHTML=h;});}
function copyRef(){let txt=document.getElementById('refLinkBox').innerText; navigator.clipboard.writeText(txt).then(function(){alert('Copy Done');});}
function previewPhoto(i){ if(i.files && i.files[0]){ let r=new FileReader(); r.onload=function(e){document.getElementById('previewImg').src=e.target.result; document.getElementById('previewWrap').style.display='block';}; r.readAsDataURL(i.files[0]);}}
function saveProfile(){let name=document.getElementById('accNameInput').value; let file=document.getElementById('accPhoto').files[0]; let fd=new FormData(); fd.append('id',uid); fd.append('name',name); if(file) fd.append('photo',file); fetch('/api/profile',{method:'POST',body:fd}).then(function(r){return r.json();}).then(function(d){alert(d.msg); init();});}
function init(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})}).then(function(r){return r.json();}).then(function(d){let u=d.user; let bal='Tk '+u.bal; document.getElementById('balShow').innerText=bal; document.getElementById('balTopRight').innerText=bal; document.getElementById('balTopBalance').innerText=bal; document.getElementById('diamondTop').innerText=u.diamonds; document.getElementById('cToday').innerText=(u.c_today||0)+'/80'; document.getElementById('pToday').innerText=(u.p_today||0)+'/80'; document.getElementById('adsCount').innerText=(u.c_today||0)+(u.p_today||0)+'/80'; document.getElementById('refLinkBox').innerText=location.origin+'/?ref='+u.id; document.getElementById('accId').innerText=u.id; document.getElementById('accNameInput').value=u.name;});} init(); loadTasks();
</script></body></html>
"""

@app.route('/')
def home():
    db=load_db()
    return render_template_string(HTML)

@app.route('/admin')
def admin():
    db=load_db()
    s=db["settings"]
    html=""
    for k in s:
        v=s[k]
        html=html+"<label>"+k+"</label><input name='"+k+"' value='"+str(v)+"' style='width:100%;padding:10px;margin:5px 0;background:#0B0E1C;color:#fff;border-radius:8px;border:1px solid #333' />"
    tasks=json.dumps(db["tasks"], indent=2, ensure_ascii=False)
    page="<body style='background:#0B0E1C;color:#fff;max-width:600px;margin:auto;padding:20px'><h1>Admin Fixed</h1><form method='POST' action='/admin/save'><div style='background:#1A2040;padding:16px;border-radius:16px'>"+html+"<label>tasks JSON</label><textarea name='tasks_json' style='width:100%;height:150px;background:#0B0E1C;color:#fff'>"+tasks+"</textarea></div><button style='width:100%;padding:14px;background:#8b5cf6;color:#fff;border-radius:12px;margin-top:15px;font-weight:800'>Save All</button></form></body>"
    return render_template_string(page)

@app.route('/admin/save', methods=['POST'])
def admin_save():
    db=load_db()
    for k in db["settings"]:
        if k in request.form:
            db["settings"][k]=request.form[k]
    if "tasks_json" in request.form:
        try:
            db["tasks"]=json.loads(request.form["tasks_json"])
        except:
            pass
    save_db(db)
    return "<script>alert('Saved'); location.href='/admin';</script>"

@app.route('/api/init', methods=['POST'])
def api_init():
    db=load_db()
    uid=request.json.get('id','4250')
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":"User "+uid[-4:],"bal":20.3,"diamonds":2030,"c_today":0,"p_today":0,"refl":[],"photo":""}
        save_db(db)
    return jsonify({"user":db["users"][uid],"tasks":db.get("tasks",[]),"wds":[]})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    db=load_db()
    d=request.json
    uid=d["id"]
    typ=d["type"]
    u=db["users"][uid]
    s=db["settings"]
    reward=float(s["ad"]) if typ=="c" else float(s["pop"])
    u["bal"]=round(u["bal"]+reward,2)
    u["diamonds"]=u["diamonds"]+int(reward*100)
    if typ=="c":
        u["c_today"]=u["c_today"]+1
    else:
        u["p_today"]=u["p_today"]+1
    save_db(db)
    return jsonify({"msg":"Ad দেখেছো! Taka Added!"})

@app.route('/api/wd', methods=['POST'])
def api_wd():
    db=load_db()
    d=request.json
    uid=d["id"]
    amt=float(d["amt"])
    u=db["users"][uid]
    if u["bal"]<amt:
        return jsonify({"msg":"Balance কম"})
    u["bal"]=u["bal"]-amt
    save_db(db)
    return jsonify({"msg":"Withdraw Sent!"})

@app.route('/api/profile', methods=['POST'])
def save_profile():
    db=load_db()
    uid=request.form.get('id')
    name=request.form.get('name')
    if uid in db["users"]:
        if name:
            db["users"][uid]["name"]=name
        if 'photo' in request.files:
            f=request.files['photo']
            b64=base64.b64encode(f.read()).decode()
            db["users"][uid]["photo"]="data:"+f.mimetype+";base64,"+b64
        save_db(db)
    return jsonify({"msg":"Profile Saved!"})

@app.route('/api/task', methods=['POST'])
def api_task():
    db=load_db()
    d=request.json
    uid=d["id"]
    u=db["users"][uid]
    u["bal"]=round(u["bal"]+0.2,2)
    save_db(db)
    return jsonify({"msg":"Task Done!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
