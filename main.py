import os, json, time
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
DB_FILE = "/tmp/users.json"
ADMIN_PASS = os.environ.get("ADMIN_PASS", "653598")

def load_db():
    try: return json.load(open(DB_FILE))
    except: return {}

def save_db(db):
    json.dump(db, open(DB_FILE, 'w'))

# --- USER APP (আগের সব ফিচার + জিরো থেকে শুরু) ---
USER_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#070d0c;color:#fff;font-family:sans-serif;padding-bottom:80px}.glass{margin:12px;padding:16px;border-radius:16px;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1)}.btn{width:100%;padding:14px;background:#00ff94;color:#003d25;border:0;border-radius:12px;font-weight:800;margin-top:8px}.nav{position:fixed;bottom:10px;left:10px;right:10px;display:flex;justify-content:space-around;background:#111;padding:10px;border-radius:16px}</style></head><body>
<div class="glass">💎 Diamond Kormo BD<br>৳<span id="b">0</span> | 💎<span id="d">0</span> | <span id="uid"></span></div>
<div class="glass" id="home"><div style="font-size:32px">৳<span id="b2">0</span></div><small>0 থেকে শুরু</small><br><br><button class="btn" onclick="earn(18,1)">▶ বিজ্ঞাপন দেখুন (৳18)</button><button class="btn" onclick="shareRef()">🔗 রেফার লিংক শেয়ার</button><div style="margin-top:10px">রেফার: <span id="refc">0</span> জন</div></div>
<div class="glass" id="wd"><input id="num" placeholder="bKash Number"><input id="amt" placeholder="500+"><button class="btn" onclick="wd()">উইথড্র</button></div>
<div class="nav"><div>🏠 হোম</div><div onclick="location.reload()">🔄 রিফ্রেশ</div></div>
<script>
let uid = localStorage.getItem('uid') || 'user_'+Date.now();
localStorage.setItem('uid',uid);
let b=parseInt(localStorage.getItem('b')||'0'), d=parseInt(localStorage.getItem('d')||'0'), refc=0;
if(!localStorage.getItem('first')){b=50;d=5;localStorage.setItem('first','1');}
function upd(){document.querySelectorAll('#b,#b2').forEach(e=>e.innerText=b);document.getElementById('d').innerText=d;document.getElementById('uid').innerText=uid; localStorage.setItem('b',b);localStorage.setItem('d',d); fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uid:uid,balance:b,diamond:d})})}
function earn(tb,td){b+=tb;d+=td;upd();}
function wd(){fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uid:uid,amount:document.getElementById('amt').value,number:document.getElementById('num').value})}).then(()=>alert('রিকোয়েস্ট গেছে, Admin দেখবে'))}
function shareRef(){let link=location.origin+'/?ref='+uid; if(navigator.share){navigator.share({title:'Join',url:link})}else{prompt('লিংক কপি করো:',link)} }
let ref=new URLSearchParams(location.search).get('ref');
fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uid:uid,ref:ref, time:new Date().toLocaleString()})}).then(r=>r.json()).then(j=>{b=j.balance;d=j.diamond;refc=j.refCount;document.getElementById('refc').innerText=refc;upd()});
upd();
</script></body></html>
"""

ADMIN_HTML = """
<h2 style="font-family:sans-serif">👑 Admin Panel - Diamond Kormo BD</h2>
<p>Password: 653598 | Total Users: {{total}}</p>
<table border=1 cellpadding=8 style="border-collapse:collapse;font-family:sans-serif;width:100%">
<tr><th>ছবি</th><th>UID</th><th>জয়েন টাইম</th><th>ব্যালেন্স</th><th>ডায়মন্ড</th><th>রেফার</th><th>উইথড্র</th></tr>
{% for u in users.values() %}
<tr><td><img src="https://t.me/i/userpic/320/{{u.uid}}.jpg" width=40 style="border-radius:50%" onerror="this.src='https://cdn-icons-png.flaticon.com/512/149/149071.png'"></td>
<td>{{u.uid}}</td><td>{{u.join_time}}</td><td>৳{{u.balance}}</td><td>{{u.diamond}}💎</td><td>{{u.ref_count}}</td><td>{{u.withdraws}}</td></tr>
{% endfor %}
</table>
"""

@app.route('/')
def home(): return USER_HTML

@app.route('/api/join', methods=['POST'])
def join():
    db=load_db(); data=request.json; uid=data['uid']
    if uid not in db: db[uid]={'uid':uid,'join_time':data.get('time',datetime.now().strftime("%Y-%m-%d %H:%M")),'balance':50,'diamond':5,'ref_count':0,'withdraws':[]}
    if data.get('ref') and data['ref'] in db and data['ref']!=uid:
        db[data['ref']]['ref_count']+=1; db[data['ref']]['balance']+=50
    save_db(db); return jsonify(db[uid])

@app.route('/api/update', methods=['POST'])
def update():
    db=load_db(); d=request.json; uid=d['uid']
    if uid in db: db[uid]['balance']=d['balance']; db[uid]['diamond']=d['diamond']; save_db(db)
    return jsonify({"ok":True})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    db=load_db(); data=request.json; uid=data['uid']
    if uid in db: db[uid]['withdraws'].append(f"{data['amount']} TK - {data['number']} - {datetime.now().strftime('%H:%M')}")
    save_db(db); return jsonify({"ok":True})

@app.route('/admin')
def admin():
    if request.args.get('pass')!=ADMIN_PASS: return "Wrong Pass!?pass=653598 দাও", 403
    db=load_db(); return render_template_string(ADMIN_HTML, users=db, total=len(db))

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
