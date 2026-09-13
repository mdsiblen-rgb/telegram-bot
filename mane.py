import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime, timedelta
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    default = {
        "users": {}, "w": [],
        "s": {
            "admin_name": "প্রতিদিনের কাজ BD",
            "admin_pic": "https://i.pravatar.cc/150?img=32",
            "profile_box": "✅ Official Telegram - @ProtidinerKajBD",
            "ads_limit": 100, "ads_reward": 2, "refer_bonus": 20,
            "notice_title": "অফিসিয়াল নোটিস",
            "notice_sub": "প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম করুন",
            "slider": [
                "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600",
                "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600",
                "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"
            ],
            "tasks": [
                {"title": "YouTube Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626", "btn": "Join & Get 25 Tk"},
                {"title": "Telegram Join", "reward": 10, "link": "https://t.me", "color": "#1e40af", "btn": "Join & Get 10 Tk"},
                {"title": "Facebook Follow", "reward": 15, "link": "https://facebook.com", "color": "#0ea5e9", "btn": "Follow & Get 15 Tk"},
                {"title": "Website Visit", "reward": 20, "link": "https://google.com", "color": "#7c3aed", "btn": "Visit & Get 20 Tk"},
                {"title": "Group Join", "reward": 20, "link": "https://t.me", "color": "#0f766e", "btn": "Join & Get 20 Tk"},
                {"title": "Post Like", "reward": 20, "link": "https://facebook.com", "color": "#be123c", "btn": "Like & Get 20 Tk"}
            ]
        }
    }
    if not os.path.exists(DB_FILE):
        return default
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(f, d, indent=2, ensure_ascii=False)

def get_user(db, uid):
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "bal": 60, "ads": 0, "uname": f"User {uid[-4:]}", "upic": "", "tasks": {}, "date": str(datetime.now().date())}
    return db["users"][uid]

@app.route('/')
def home():
    return render_template_string(USER_PAGE)

@app.route('/admin')
def admin_page():
    if request.args.get('id')!= ADMIN_ID:
        return "Admin Only"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/bal')
def api_bal():
    uid = request.args.get('id', ADMIN_ID)
    db = load_db()
    u = get_user(db, uid)
    save_db(db)
    return jsonify({"bal": u["bal"], "ads": u["ads"], "id": uid, "uname": u["uname"], "upic": u["upic"], "tasks": u["tasks"], "w": db["w"][-15:][::-1], "s": db["s"]})

@app.route('/api/add')
def api_add():
    uid = request.args.get('id', ADMIN_ID)
    db = load_db()
    u = get_user(db, uid)
    if u["ads"] >= db["s"]["ads_limit"]:
        return jsonify({"ok": False, "msg": "Limit শেষ"})
    u["bal"] += db["s"]["ads_reward"]
    u["ads"] += 1
    save_db(db)
    return jsonify({"ok": True, "bal": u["bal"]})

@app.route('/api/claim_task')
def api_claim():
    uid = request.args.get('id', ADMIN_ID)
    tid = request.args.get('tid', '0')
    db = load_db()
    u = get_user(db, uid)
    if tid in u["tasks"]:
        return jsonify({"ok": False, "msg": "DONE ✅ - 24h পরে আবার"})
    reward = db["s"]["tasks"][int(tid)]["reward"]
    u["tasks"][tid] = str(datetime.now())
    u["bal"] += reward
    save_db(db)
    return jsonify({"ok": True, "msg": f"৳{reward} Added ✅"})

@app.route('/api/wd')
def api_wd():
    uid = request.args.get('id', ADMIN_ID)
    db = load_db()
    u = get_user(db, uid)
    amt = int(request.args.get('amt', 0))
    if u["bal"] < amt or amt < 1000:
        return jsonify({"msg": "Min ৳1000"})
    u["bal"] -= amt
    db["w"].append({"id": uid, "amt": amt, "num": request.args.get('num', ''), "met": request.args.get('met', 'bKash'), "time": str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg": "Withdraw Success"})

@app.route('/api/save', methods=['POST'])
def api_save():
    db = load_db()
    data = request.json
    db["s"].update(data)
    save_db(db)
    return jsonify({"msg": "Saved"})

@app.route('/api/update_profile', methods=['POST'])
def api_upd():
    j = request.json
    uid = j.get('id', ADMIN_ID)
    db = load_db()
    u = get_user(db, uid)
    if j.get('uname'):
        u["uname"] = j.get('uname')
    if j.get('upic'):
        u["upic"] = j.get('upic')
    save_db(db)
    return jsonify({"msg": "Updated"})

USER_PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#081028;color:#fff;max-width:430px;margin:0 auto;padding-bottom:95px}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 28px 28px;padding:18px}
.hdr-top{display:flex;justify-content:space-between;align-items:center}
.hdr-name{font-size:19px;font-weight:800}
.hdr-pic{width:46px;height:46px;border-radius:50%;border:2px solid #2ef36c;object-fit:cover}
.bal{font-size:52px;font-weight:900;color:#2ef36c;margin-top:8px}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:18px;padding:14px;display:flex;justify-content:space-between;align-items:center;border:2px solid #2ef36c}
.dot{width:10px;height:10px;background:#2ef36c;border-radius:50%;animation:blk 0.8s infinite}
@keyframes blk{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:18px;height:185px;position:relative;overflow:hidden;background:#000}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:18px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:12px;font-weight:800;color:#fff;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0 6px 0;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px;cursor:pointer}
.btm div.on{color:#2ef36c}
.btm span{font-size:20px;display:block}
.inp{width:100%;padding:13px;border-radius:12px;border:1px solid #2a3a5f;background:#0b142d;color:#fff;margin-top:10px}
.meth{display:flex;gap:8px;margin-top:12px}
.meth div{flex:1;background:#0b142d;border:2px solid #2a3a5f;border-radius:12px;padding:12px;text-align:center;cursor:pointer}
.meth div.on{border-color:#ff2d7a;background:#1a1430}
</style></head><body>
<div id="p-home"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName">👑 প্রতিদিনের কাজ BD ✅</div><img id="hdrPic" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div><div style="opacity:0.7;font-size:13px">Ads: <span class="adsV">0</span>/100</div></div>
<div class="notice"><div><div style="font-weight:900">অফিসিয়াল নোটিস</div><div style="font-size:12px;opacity:0.8">প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম</div></div><div style="background:#2ef36c;color:#000;font-weight:900;padding:10px 18px;border-radius:30px;display:flex;gap:6px;align-items:center"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"><img class="on" src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600"><img src="https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600"><img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"></div>
<div class="card"><div style="font-weight:900">🎬 স্পেশাল অফার - বোনাস Ads</div><button class="btn" style="background:#0ea5e9;margin-top:12px" onclick="watchAds()">ADS দেখুন - ৳2 বোনাস</button></div>
<div id="tasksHome"></div></div>

<div id="p-tasks" style="display:none"><div class="hdr"><div class="hdr-top"><div class="hdr-name" id="hdrName2">👑 প্রতিদিনের কাজ BD ✅</div><img id="hdrPic2" class="hdr-pic" src=""></div><div class="bal">৳ <span class="balV">60</span></div></div><div id="tasksAll"></div></div>

<div id="p-refer" style="display:none"><div class="hdr"><div style="font-weight:700">রেফার করুন</div><div class="bal">৳ <span class="balV">60</span></div></div><div class="card"><div style="font-weight:900">Refer & Earn ৳20</div><input class="inp" id="refLink" readonly><button class="btn" style="background:#2563eb;margin-top:12px" onclick="copyR()">Copy Link</button></div></div>

<div id="p-wallet" style="display:none"><div class="hdr"><div style="font-weight:700">আমার ওয়ালেট</div><div class="bal">৳ <span class="balV">60</span></div><div style="opacity:0.7;font-size:13px">সর্বনিম্ন ৳1000</div></div><div class="card"><div style="font-weight:900">আমার ব্যালেন্স</div><div style="font-size:38px;font-weight:900;color:#2ef36c">৳ <span class="balV">60</span></div></div><div class="card"><input class="inp" id="wAmt" placeholder="Amount - Min 1000" type="number"><div class="meth"><div class="on" id="m-bkash" onclick="sel('bKash')">bKash</div><div id="m-nagad" onclick="sel('Nagad')">Nagad</div></div><input class="inp" id="wNum" placeholder="Number"><button class="btn" style="background:#2563eb;margin-top:12px" onclick="wd()">Withdraw করুন</button></div><div class="card" style="border:2px solid #2ef36c"><div style="font-weight:900;color:#2ef36c">🟢 Live Withdraw</div><div id="liveList"></div></div></div>

<div id="p-profile" style="display:none"><div class="hdr" style="text-align:center"><img id="userPic" style="width:90px;height:90px;border-radius:50%;border:4px solid #2ef36c;object-fit:cover" src=""><div style="font-weight:900;font-size:18px;margin-top:10px" id="userName">User</div><div style="opacity:0.7;font-size:13px">ID: <span id="pid">----</span> - Verified ✅</div><div class="bal" style="text-align:center">৳ <span class="balV">60</span></div></div><div class="card" style="border:2px solid #22c55e"><div style="font-weight:900">✏️ প্রোফাইল পরিবর্তন</div><input class="inp" id="editName" placeholder="আপনার নাম"><input class="inp" id="editPic" placeholder="ছবির Link"><button class="btn" style="background:#22c55e;color:#000;margin-top:12px" onclick="saveProfile()">💾 Save Profile</button></div><div class="card" style="border:2px solid #f59e0b"><div style="font-weight:900;color:#fbbf24">📢 Admin Notice</div><div id="adminBoxText"></div></div></div>

<div class="btm"><div class="on" id="b-home" onclick="go('home')"><span>🏠</span>Home</div><div id="b-tasks" onclick="go('tasks')"><span>✅</span>Tasks</div><div id="b-refer" onclick="go('refer')"><span>👥</span>Refer</div><div id="b-wallet" onclick="go('wallet')"><span>💰</span>Wallet</div><div id="b-profile" onclick="go('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385'; let method='bKash';
let tasksData=[];
function go(p){['home','tasks','refer','wallet','profile'].forEach(x=>{document.getElementById('p-'+x).style.display=x==p?'block':'none';document.getElementById('b-'+x).classList.toggle('on',x==p);});}
function sel(m){method=m;document.querySelectorAll('.meth div').forEach(d=>d.classList.remove('on'));document.getElementById('m-'+m.toLowerCase()).classList.add('on');}
function copyR(){navigator.clipboard.writeText(document.getElementById('refLink').value).then(()=>alert('Copied'));}
function watchAds(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(()=>load());});}else{fetch('/api/add?id='+uid).then(()=>load());}}
function doTask(i,link){window.open(link,'_blank');setTimeout(()=>{fetch('/api/claim_task?id='+uid+'&tid='+i).then(r=>r.json()).then(j=>{alert(j.msg);load();});},2500);}
function wd(){let a=document.getElementById('wAmt').value,n=document.getElementById('wNum').value;if(!a||!n){alert('Amount & Number');return;}fetch('/api/wd?id='+uid+'&amt='+a+'&num='+n+'&met='+method).then(r=>r.json()).then(x=>{alert(x.msg);load();});}
function saveProfile(){let nm=document.getElementById('editName').value,pic=document.getElementById('editPic').value;fetch('/api/update_profile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,uname:nm,upic:pic})}).then(()=>{alert('Updated ✅');load();});}
let slIdx=0;setInterval(()=>{let imgs=document.querySelectorAll('#sl img');imgs.forEach(im=>im.classList.remove('on'));slIdx=(slIdx+1)%imgs.length;imgs[slIdx].classList.add('on');},3000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{document.querySelectorAll('.balV').forEach(e=>e.innerText=d.bal);document.querySelectorAll('.adsV').forEach(e=>e.innerText=d.ads);document.getElementById('pid').innerText=d.id.slice(0,4)+'****'+d.id.slice(-2);document.getElementById('refLink').value=location.origin+'/?ref='+d.id;document.getElementById('userName').innerText=d.uname||'User';document.getElementById('userPic').src=d.upic||'https://i.pravatar.cc/150?img=8';document.getElementById('adminBoxText').innerText=d.s.profile_box||'';document.getElementById('hdrName').innerText='👑 '+d.s.admin_name+' ✅';document.getElementById('hdrName2').innerText='👑 '+d.s.admin_name+' ✅';document.getElementById('hdrPic').src=d.s.admin_pic;document.getElementById('hdrPic2').src=d.s.admin_pic;tasksData=d.s.tasks;let h='';tasksData.forEach((t,i)=>{let done=d.tasks[i]!==undefined;let txt=done?'DONE ✅ - 24h পরে আবার':t.btn;let col=done?'#475569':t.color;h+=`<div class="card"><div style="display:flex;justify-content:space-between"><div>⭐ ${t.title}</div><div>৳${t.reward}</div></div><button class="btn" style="background:${col};margin-top:10px" onclick="doTask(${i},'${t.link}')">${txt}</button></div>`;});document.getElementById('tasksHome').innerHTML=h;document.getElementById('tasksAll').innerHTML=h;let live='';if(d.w.length==0)live='এখনো কেউ Withdraw করেনি';else d.w.forEach(w=>{live+=`<div style="padding:6px 0">💸 ID:${w.id.slice(-4)} - ৳${w.amt}</div>`;});document.getElementById('liveList').innerHTML=live;});}
load();
</script></body></html>
"""
ADMIN_PAGE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#081028;color:#fff;font-family:sans-serif;padding:14px;max-width:500px;margin:auto}</style></head><body><h2>Admin OK - 5 Button Restored ✅</h2><div id="a"></div><script>fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{document.getElementById('a').innerHTML=`Total Users: ${Object.keys(d).length}<br>Tasks: ${d.s.tasks.length} টা আছে<br>Slider: ${d.s.slider.length} টা আছে<br>সব ঠিক আছে`;});</script></body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
