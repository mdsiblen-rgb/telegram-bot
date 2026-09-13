import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime, timedelta
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"

def load_db():
    default = {
        "users":{},
        "w":[],
        "s":{
            "admin_name":"প্রতিদিনের কাজ BD",
            "admin_pic":"https://i.pravatar.cc/150?img=32",
            "profile_box":"✅ Official Telegram - @ProtidinerKajBD",
            "ads_limit":100,
            "ads_reward":2,
            "refer_bonus":20,
            "notice_title":"অফিসিয়াল নোটিস",
            "notice_sub":"প্রতিদিন Ads দেখুন - ৳500 পর্যন্ত ইনকাম",
            "slider":["https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600","https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"],
            "tasks":[
                {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","btn":"Join & Get 25 Tk"},
                {"title":"Telegram Join","reward":10,"link":"https://t.me","color":"#1e40af","btn":"Join & Get 10 Tk"},
                {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9","btn":"Follow & Get 15 Tk"},
                {"title":"Website Visit","reward":20,"link":"https://google.com","color":"#7c3aed","btn":"Visit & Get 20 Tk"},
                {"title":"Group Join","reward":20,"link":"https://t.me","color":"#0f766e","btn":"Join & Get 20 Tk"},
                {"title":"Post Like","reward":20,"link":"https://facebook.com","color":"#be123c","btn":"Like & Get 20 Tk"}
            ]
        }
    }
    if not os.path.exists(DB_FILE):
        return default
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f:
            j=json.load(f)
            if "s" not in j:
                j["s"]=default["s"]
            for k in default["s"]:
                if k not in j["s"]:
                    j["s"][k]=default["s"][k]
            return j
    except:
        return default

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f:
        json.dump(f,d,ensure_ascii=False,indent=2)

def get_user(db,uid):
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"bal":60,"ads":0,"uname":f"User {uid[-4:]}","upic":"","tasks":{},"last":str(datetime.now().date())}
    return db["users"][uid]

@app.route('/')
def home():
    return render_template_string(PAGE)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN)

@app.route('/api/bal')
def bal():
    uid=request.args.get('id','8807178385')
    db=load_db()
    u=get_user(db,uid)
    save_db(db)
    return jsonify({"bal":u["bal"],"ads":u["ads"],"id":uid,"uname":u["uname"],"upic":u["upic"],"tasks":u["tasks"],"w":db["w"][-10:][::-1],"s":db["s"],"total":len(db["users"])})

@app.route('/api/add')
def add():
    uid=request.args.get('id','8807178385')
    db=load_db()
    u=get_user(db,uid)
    if u["ads"]>=db["s"]["ads_limit"]:
        return jsonify({"ok":False,"msg":"Limit শেষ"})
    u["bal"]+=db["s"]["ads_reward"]
    u["ads"]+=1
    save_db(db)
    return jsonify({"ok":True})

@app.route('/api/claim')
def claim():
    uid=request.args.get('id','8807178385')
    tid=request.args.get('tid','0')
    db=load_db()
    u=get_user(db,uid)
    if tid in u["tasks"]:
        return jsonify({"ok":False,"msg":"DONE ✅ - 24h পরে আবার"})
    reward=db["s"]["tasks"][int(tid)]["reward"]
    u["tasks"][tid]=str(datetime.now())
    u["bal"]+=reward
    save_db(db)
    return jsonify({"ok":True,"msg":f"৳{reward} Added"})

@app.route('/api/wd')
def wd():
    uid=request.args.get('id','8807178385')
    db=load_db()
    u=get_user(db,uid)
    amt=int(request.args.get('amt',0))
    if u["bal"]<amt or amt<1000:
        return jsonify({"msg":"Min 1000"})
    u["bal"]-=amt
    db["w"].append({"id":uid,"amt":amt,"num":request.args.get('num',''),"time":str(datetime.now())[:16]})
    save_db(db)
    return jsonify({"msg":"Withdraw Done"})

@app.route('/api/save',methods=['POST'])
def save():
    db=load_db()
    db["s"].update(request.json)
    save_db(db)
    return jsonify({"msg":"Saved"})

PAGE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
body{background:#081028;color:#fff;max-width:430px;margin:auto;padding-bottom:90px;font-family:sans-serif}
.hdr{background:linear-gradient(135deg,#1e3a8a,#0f1f4d);border-radius:0 0 25px 25px;padding:18px}
.bal{font-size:50px;font-weight:900;color:#2ef36c}
.notice{background:linear-gradient(90deg,#1d3a8a,#0f6a6a);margin:12px;border-radius:15px;padding:12px;display:flex;justify-content:space-between;border:2px solid #2ef36c}
.dot{width:10px;height:10px;background:#2ef36c;border-radius:50%;animation:b 0.8s infinite}
@keyframes b{0%{opacity:1}50%{opacity:0.2}100%{opacity:1}}
.slider{margin:12px;border-radius:15px;height:180px;position:relative;overflow:hidden}
.slider img{position:absolute;width:100%;height:100%;object-fit:cover;opacity:0;transition:0.8s}
.slider img.on{opacity:1}
.card{background:#132042;margin:12px;border-radius:15px;padding:14px;border:1px solid #1e2d4f}
.btn{width:100%;padding:14px;border:0;border-radius:10px;font-weight:900;color:#fff}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f172a;display:flex;border-top:1px solid #1e293b;padding:8px 0}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px}
.btm div.on{color:#2ef36c}
</style></head><body>
<div id="p1"><div class="hdr"><div style="display:flex;justify-content:space-between"><div id="hn">👑 প্রতিদিনের কাজ BD ✅</div><img id="hp" style="width:40px;height:40px;border-radius:50%;border:2px solid #2ef36c" src=""></div><div class="bal">৳ <span id="b1">60</span></div><div style="opacity:0.7">Ads: <span id="a1">0</span>/100</div></div>
<div class="notice"><div><b>অফিসিয়াল নোটিস</b><br><small>প্রতিদিন Ads দেখুন</small></div><div style="background:#2ef36c;color:#000;padding:8px 15px;border-radius:20px;display:flex;gap:5px;align-items:center;font-weight:900"><span class="dot"></span>LIVE</div></div>
<div class="slider" id="sl"></div>
<div class="card"><b>🎬 স্পেশাল অফার</b><br><button class="btn" style="background:#0ea5e9;margin-top:10px" onclick="ads()">ADS দেখুন - ৳2 বোনাস</button></div>
<div id="t1"></div></div>
<div id="p2" style="display:none"><div class="hdr"><div id="hn2">👑 প্রতিদিনের কাজ BD ✅</div><div class="bal">৳ <span id="b2">60</span></div></div><div id="t2"></div></div>
<div id="p3" style="display:none"><div class="hdr"><div>Wallet - ৳ <span id="b3">60</span></div></div><div class="card"><div id="lw"></div></div></div>
<div class="btm"><div class="on" onclick="go(1)">🏠<br>Home</div><div onclick="go(2)">✅<br>Tasks</div><div onclick="go(3)">💰<br>Wallet</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
function go(n){document.getElementById('p1').style.display=n==1?'block':'none';document.getElementById('p2').style.display=n==2?'block':'none';document.getElementById('p3').style.display=n==3?'block':'none';}
function ads(){if(typeof show_11764581!=='undefined'){show_11764581().then(()=>{fetch('/api/add?id='+uid).then(()=>load());});}else{fetch('/api/add?id='+uid).then(()=>load());}}
function task(i,link){window.open(link,'_blank');setTimeout(()=>{fetch('/api/claim?id='+uid+'&tid='+i).then(r=>r.json()).then(j=>{alert(j.msg);load();});},2000);}
let sI=0;setInterval(()=>{let im=document.querySelectorAll('#sl img');if(im.length==0)return;im.forEach(e=>e.classList.remove('on'));sI=(sI+1)%im.length;im[sI].classList.add('on');},3000);
function load(){fetch('/api/bal?id='+uid).then(r=>r.json()).then(d=>{document.getElementById('b1').innerText=d.bal;document.getElementById('b2').innerText=d.bal;document.getElementById('b3').innerText=d.bal;document.getElementById('a1').innerText=d.ads;document.getElementById('hn').innerText='👑 '+d.s.admin_name+' ✅';document.getElementById('hn2').innerText='👑 '+d.s.admin_name+' ✅';document.getElementById('hp').src=d.s.admin_pic;let sl=document.getElementById('sl');sl.innerHTML='';d.s.slider.forEach((src,i)=>{sl.innerHTML+=`<img class="${i==0?'on':''}" src="${src}">`;});let h='';d.s.tasks.forEach((t,i)=>{let done=d.tasks[i]!==undefined;h+=`<div class=card><div style=display:flex;justify-content:space-between><div>⭐ ${t.title}</div><div>৳${t.reward}</div></div><button class=btn style=background:${done?'#555':t.color};margin-top:10px onclick=task(${i},'${t.link}')>${done?'DONE ✅':'${t.btn}'}</button></div>`;});document.getElementById('t1').innerHTML=h;document.getElementById('t2').innerHTML=h;let lw='Live Withdraw:<br>';d.w.forEach(w=>{lw+=`💸 ${w.id.slice(-4)} - ৳${w.amt}<br>`;});document.getElementById('lw').innerHTML=lw;});}
load();
</script></body></html>
"""
ADMIN = """<html><body style="background:#081028;color:#fff;font-family:sans-serif;padding:20px"><h2>Admin - সব আছে</h2><div id="i"></div><script>fetch('/api/bal?id=8807178385').then(r=>r.json()).then(d=>{document.getElementById('i').innerHTML=`Users: ${d.total}<br>Tasks: ${d.s.tasks.length}<br>Slider: ${d.s.slider.length}<br>Ads Limit: ${d.s.ads_limit}<br>সব ঠিক আছে ✅`;});</script></body></html>"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',10000)))
