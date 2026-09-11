# প্রতিদিনের কাজ BD - FINAL + BIG BUTTONS
import os, sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, session, redirect
app = Flask(__name__)
app.secret_key = 'bd_final_big_btn_2026'
DB = 'bd_final.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, telegram_id TEXT UNIQUE, name TEXT, username TEXT, photo_url TEXT,
        balance INTEGER DEFAULT 60, total_earned INTEGER DEFAULT 60, ads_watched INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0, refer_code TEXT, referred_by TEXT,
        join_date TEXT, join_time TEXT, last_active TEXT
    )''')
    c.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS withdraws (
        id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id TEXT, amount INTEGER, method TEXT, number TEXT,
        status TEXT DEFAULT 'pending', request_time TEXT, approve_time TEXT
    )''')
    c.execute('CREATE TABLE IF NOT EXISTS ad_views (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id TEXT, view_time TEXT)')
    defaults = {
        'monetag_zone': '11764581', 'ad_timer': '30', 'ad_limit': '100', 'welcome_bonus': '60',
        'daily_bonus': '10', 'refer_bonus': '50',
        'telegram_channel': 'https://t.me/yourchannel', 'youtube': 'https://youtube.com/@yourchannel',
        'facebook': 'https://facebook.com/yourpage', 'company_task_1': 'https://example.com/task1',
        'company_task_2': 'https://example.com/task2', 'company_task_3': 'https://example.com/task3',
        'refer_link_base': 'https://t.me/yourbot?start=',
        'page1_own_ad': '🔥 নিজের বিজ্ঞাপন: এডমিন থেকে যেকোনো লেখা দিতে পারবেন',
        'page3_custom_text': 'আমাদের সাপোর্ট টিম ২৪ ঘন্টা আপনাদের সেবায় নিয়োজিত।',
        'page4_payment_time': 'পেমেন্ট সময়: প্রতিদিন বিকাল ৫টা - রাত ১০টা',
        'page4_bkash_number': '017XXXXXXXX', 'page4_nagad_number': '018XXXXXXXX',
        'slider1': '', 'slider2': '', 'slider3': '', 'admin_total_earning': '0', 'monetag_dollars': '0'
    }
    for k,v in defaults.items(): c.execute('INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)', (k,v))
    conn.commit(); conn.close()
init_db()

def get_setting(k):
    conn=get_db(); row=conn.execute('SELECT value FROM settings WHERE key=?',(k,)).fetchone(); conn.close()
    return row['value'] if row else ''

INDEX_HTML = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>প্রতিদিনের কাজ BD</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}body{background:#eef2ff}
.header{background:#3040c8;color:white;padding:12px 15px;display:flex;justify-content:space-between;align-items:center}
.header img{width:45px;height:45px;border-radius:50%;background:white}.balance{font-size:22px;font-weight:bold}
.card{background:white;margin:15px;border-radius:20px;padding:15px;box-shadow:0 4px 12px rgba(0,0,0,.1)}
.btn{width:100%;padding:14px;border:none;border-radius:12px;color:white;font-size:16px;font-weight:bold;margin:8px 0;cursor:pointer}
.btn-blue{background:#1a3ec1}.btn-red{background:#ff0000}.btn-lightblue{background:#2d8cff}
.page{display:none;padding-bottom:110px}.page.active{display:block}
.slider{width:100%;height:140px;border-radius:15px;object-fit:cover;margin-bottom:10px}
.ad-box{background:linear-gradient(135deg,#ffe259,#ffa751);padding:12px;border-radius:12px;margin:10px 0;text-align:center;font-weight:bold}
.withdraw-card{background:linear-gradient(135deg,#ff006a,#ff8a00);color:white;border-radius:20px;padding:20px;margin:10px 0}

/* ===== BIG BUTTONS FINAL ===== */
.bottom-nav{
  position:fixed;bottom:0;left:0;right:0;
  background:white;
  display:flex;justify-content:space-around;
  padding:14px 0 18px 0;
  border-top:1px solid #ddd;
  box-shadow:0 -4px 15px rgba(0,0,0,.08);
  z-index:999;
}
.nav-item{
  text-align:center;
  font-size:14px;
  font-weight:700;
  cursor:pointer;
  color:#777;
  padding:10px 16px;
  border-radius:14px;
  min-width:64px;
  line-height:1.3;
  transition:.2s;
}
.nav-item.active{
  color:#1a3ec1;
  background:#e8edff;
  transform:scale(1.18);
}
</style>
</head><body>
<div class="header"><div style="display:flex;align-items:center;gap:10px"><img id="userPhoto" src="https://via.placeholder.com/45"><span style="font-weight:bold">প্রতিদিনের কাজ BD</span></div><div class="balance">৳<span id="balance">60</span></div></div>

<div id="page-home" class="page active"><div class="card"><div id="sliderBox"></div><div class="ad-box" id="page1OwnAd"></div><button class="btn btn-blue" onclick="watchAd()">📺 বিজ্ঞাপন দেখুন (৩০ সেকেন্ড)</button><p style="text-align:center">আজ: <span id="adsCount">0</span>/100</p><button class="btn btn-lightblue" onclick="dailyCheckin()">🎁 ডেইলি চেক-ইন ৳10</button></div>
<div class="card"><h3>কোম্পানির কাজ</h3><button class="btn btn-blue" onclick="doTask('telegram_channel')">📢 Telegram</button><button class="btn btn-red" onclick="doTask('youtube')">▶️ YouTube</button><button class="btn btn-lightblue" onclick="doTask('facebook')">📘 Facebook</button><button class="btn btn-blue" onclick="doTask('company_task_1')">🏢 কোম্পানি টাস্ক ১</button><button class="btn btn-blue" onclick="doTask('company_task_2')">🏢 টাস্ক ২</button><button class="btn btn-blue" onclick="doTask('company_task_3')">🏢 টাস্ক ৩</button></div></div>

<div id="page-income" class="page"><div class="card"><h2>💰 আয় করুন</h2><button class="btn btn-blue" onclick="copyRefer()">🔗 রেফার লিংক কপি করুন</button><p id="referLink" style="word-break:break-all;background:#f0f0f0;padding:10px;border-radius:8px;margin:10px 0"></p><p>মোট রেফার: <span id="referCount">0</span></p></div></div>

<div id="page-support" class="page"><div class="card"><h2 style="text-align:center">🎧 সাপোর্ট সেন্টার</h2><button class="btn btn-blue" onclick="openLink('telegram_channel')">📢 Telegram Channel</button><button class="btn btn-red" onclick="openLink('youtube')">▶️ YouTube</button><button class="btn btn-lightblue" onclick="openLink('facebook')">📘 Facebook Page</button><div style="margin-top:20px;padding:15px;background:#f9f9ff;border-radius:12px;white-space:pre-wrap" id="customSupportText"></div></div></div>

<div id="page-withdraw" class="page"><div class="card"><h2>💳 উইথড্র</h2><p id="payTime"></p><div class="withdraw-card"><h3>bKash</h3><p id="bkashNum"></p></div><div class="withdraw-card" style="background:linear-gradient(135deg,#ff5f00,#ff9a00)"><h3>Nagad</h3><p id="nagadNum"></p></div><input id="wdAmount" type="number" placeholder="টাকার পরিমাণ" style="width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc"><select id="wdMethod" style="width:100%;padding:12px;border-radius:8px"><option>bKash</option><option>Nagad</option></select><input id="wdNumber" type="text" placeholder="আপনার নাম্বার" style="width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc"><button class="btn btn-blue" onclick="withdraw()">উইথড্র রিকোয়েস্ট</button></div></div>

<div id="page-profile" class="page"><div class="card" style="text-align:center"><img id="profilePhoto" src="https://via.placeholder.com/80" style="width:80px;height:80px;border-radius:50%"><h2 id="profileName"></h2><p id="profileUsername"></p><div style="text-align:left;margin-top:15px;line-height:28px"><p>🆔 ID: <span id="pId"></span></p><p>📅 জয়েন: <span id="pJoinDate"></span> <span id="pJoinTime"></span></p><p>💰 মোট আয়: ৳<span id="pEarned"></span></p><p>💵 ব্যালেন্স: ৳<span id="pBalance"></span></p><p>📺 এড: <span id="pAds"></span> টি</p><p>👥 রেফার: <span id="pRef"></span> জন</p></div></div></div>

<div class="bottom-nav">
  <div class="nav-item active" onclick="showPage('home',this)">🏠<br>হোম</div>
  <div class="nav-item" onclick="showPage('income',this)">📦<br>আয়</div>
  <div class="nav-item" onclick="showPage('support',this)">🎧<br>সাপোর্ট</div>
  <div class="nav-item" onclick="showPage('withdraw',this)">💳<br>উইথড্র</div>
  <div class="nav-item" onclick="showPage('profile',this)">👤<br>প্রোফাইল</div>
</div>

<script>
let tg=window.Telegram.WebApp; tg.expand();
let user=tg.initDataUnsafe.user||{id:'12345',first_name:'Test',username:'test',photo_url:''};
if(user.photo_url){document.getElementById('userPhoto').src=user.photo_url;document.getElementById('profilePhoto').src=user.photo_url;}
document.getElementById('profileName').innerText=user.first_name;document.getElementById('profileUsername').innerText='@'+(user.username||'');document.getElementById('pId').innerText=user.id;
function showPage(p,el){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('page-'+p).classList.add('active');document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));if(el)el.classList.add('active');}
function loadData(){
 fetch('/api/user?tg_id='+user.id+'&name='+encodeURIComponent(user.first_name)+'&username='+(user.username||'')+'&photo='+(user.photo_url||'')+'&refer='+(tg.initDataUnsafe.start_param||'')).then(r=>r.json()).then(d=>{
  document.getElementById('balance').innerText=d.balance;document.getElementById('adsCount').innerText=d.ads_watched;document.getElementById('referCount').innerText=d.referrals;document.getElementById('referLink').innerText=d.refer_link;
  document.getElementById('pJoinDate').innerText=d.join_date;document.getElementById('pJoinTime').innerText=d.join_time;document.getElementById('pEarned').innerText=d.total_earned;document.getElementById('pBalance').innerText=d.balance;document.getElementById('pAds').innerText=d.ads_watched;document.getElementById('pRef').innerText=d.referrals;
  document.getElementById('page1OwnAd').innerText=d.page1_own_ad;document.getElementById('customSupportText').innerText=d.page3_text;document.getElementById('payTime').innerText=d.pay_time;document.getElementById('bkashNum').innerText=d.bkash;document.getElementById('nagadNum').innerText=d.nagad;
  let sBox=document.getElementById('sliderBox');sBox.innerHTML='';[d.slider1,d.slider2,d.slider3].forEach(s=>{if(s){let img=document.createElement('img');img.src=s;img.className='slider';sBox.appendChild(img);}});
 });
}loadData();
function watchAd(){let btn=event.target;btn.innerText='⏳ 30s...';btn.disabled=true;if(typeof show_11764581==='function'){show_11764581();}let sec=30;let iv=setInterval(()=>{sec--;btn.innerText='⏳ '+sec+'s';if(sec<=0){clearInterval(iv);fetch('/api/watch_ad?tg_id='+user.id).then(r=>r.json()).then(()=>{alert('✅ ৳1 যোগ!');loadData();btn.innerText='📺 বিজ্ঞাপন দেখুন';btn.disabled=false;});}},1000);}
function dailyCheckin(){fetch('/api/daily?tg_id='+user.id).then(r=>r.json()).then(d=>{alert(d.msg);loadData();});}
function doTask(k){fetch('/api/get_task?key='+k).then(r=>r.json()).then(d=>{window.open(d.url,'_blank');});}
function openLink(k){doTask(k);}function copyRefer(){navigator.clipboard.writeText(document.getElementById('referLink').innerText);alert('কপি হয়েছে!');}
function withdraw(){let a=document.getElementById('wdAmount').value,m=document.getElementById('wdMethod').value,n=document.getElementById('wdNumber').value;fetch(`/api/withdraw?tg_id=${user.id}&amount=${a}&method=${m}&number=${n}`).then(r=>r.json()).then(d=>alert(d.msg));}
</script></body></html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/api/user')
def api_user():
    tg_id=request.args.get('tg_id'); name=request.args.get('name'); username=request.args.get('username'); photo=request.args.get('photo'); refer=request.args.get('refer')
    conn=get_db(); user=conn.execute('SELECT * FROM users WHERE telegram_id=?',(tg_id,)).fetchone()
    if not user:
        now=datetime.now(); jd=now.strftime('%Y-%m-%d'); jt=now.strftime('%I:%M %p')
        conn.execute('INSERT INTO users (telegram_id,name,username,photo_url,refer_code,referred_by,join_date,join_time,last_active) VALUES (?,?,?,?,?,?,?,?,?)',(tg_id,name,username,photo,f"REF{tg_id}",refer,jd,jt,now.isoformat()))
        if refer:
            ru=conn.execute('SELECT * FROM users WHERE telegram_id=? OR refer_code=?',(refer,refer)).fetchone()
            if ru: conn.execute('UPDATE users SET balance=balance+50, total_earned=total_earned+50, referrals=referrals+1 WHERE telegram_id=?',(ru['telegram_id'],))
        conn.commit()
    else:
        conn.execute('UPDATE users SET name=?,username=?,photo_url=?,last_active=? WHERE telegram_id=?',(name,username,photo,datetime.now().isoformat(),tg_id)); conn.commit()
    user=conn.execute('SELECT * FROM users WHERE telegram_id=?',(tg_id,)).fetchone()
    settings=dict(conn.execute('SELECT * FROM settings').fetchall()); conn.close()
    return jsonify({'balance':user['balance'],'total_earned':user['total_earned'],'ads_watched':user['ads_watched'],'referrals':user['referrals'],'join_date':user['join_date'],'join_time':user['join_time'],'refer_link':settings.get('refer_link_base','https://t.me/yourbot?start=')+tg_id,'slider1':settings.get('slider1'),'slider2':settings.get('slider2'),'slider3':settings.get('slider3'),'page1_own_ad':settings.get('page1_own_ad'),'page3_text':settings.get('page3_custom_text'),'pay_time':settings.get('page4_payment_time'),'bkash':settings.get('page4_bkash_number'),'nagad':settings.get('page4_nagad_number')})

@app.route('/api/watch_ad')
def watch_ad():
    tg_id=request.args.get('tg_id'); conn=get_db(); user=conn.execute('SELECT * FROM users WHERE telegram_id=?',(tg_id,)).fetchone()
    if user and user['ads_watched']<100:
        conn.execute('UPDATE users SET ads_watched=ads_watched+1, balance=balance+1, total_earned=total_earned+1 WHERE telegram_id=?',(tg_id,)); conn.execute('INSERT INTO ad_views (telegram_id,view_time) VALUES (?,?)',(tg_id,datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))); conn.commit()
    conn.close(); return jsonify({'ok':True})

@app.route('/api/daily')
def daily():
    tg_id=request.args.get('tg_id'); conn=get_db(); conn.execute('UPDATE users SET balance=balance+10, total_earned=total_earned+10 WHERE telegram_id=?',(tg_id,)); conn.commit(); conn.close()
    return jsonify({'msg':'✅ ডেইলি ৳10 যোগ!'})

@app.route('/api/get_task')
def get_task(): return jsonify({'url':get_setting(request.args.get('key'))})

@app.route('/api/withdraw')
def api_withdraw():
    tg_id=request.args.get('tg_id'); amount=request.args.get('amount'); method=request.args.get('method'); number=request.args.get('number')
    conn=get_db(); user=conn.execute('SELECT * FROM users WHERE telegram_id=?',(tg_id,)).fetchone()
    if not user or int(user['balance'])<int(amount or 0): conn.close(); return jsonify({'msg':'❌ ব্যালেন্স কম!'})
    conn.execute('UPDATE users SET balance=balance-? WHERE telegram_id=?',(int(amount),tg_id))
    conn.execute('INSERT INTO withdraws (telegram_id,amount,method,number,request_time) VALUES (?,?,?,?,?)',(tg_id,amount,method,number,datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))); conn.commit(); conn.close()
    return jsonify({'msg':'✅ উইথড্র রিকোয়েস্ট গেছে!'})

@app.route('/admin')
def admin():
    if request.args.get('pass')!='admin123' and session.get('admin')!=True: return '<form method=post action=/admin/login><input name=pass placeholder=Password><button>Login</button></form>'
    conn=get_db(); settings=dict(conn.execute('SELECT * FROM settings').fetchall()); users=conn.execute('SELECT * FROM users ORDER BY id DESC').fetchall(); withdraws=conn.execute('SELECT * FROM withdraws ORDER BY id DESC').fetchall(); conn.close()
    html=f"<body style='font-family:sans-serif;padding:15px'><h2>Admin A-Z + Big Buttons Final</h2><div style='background:white;padding:15px;border-radius:12px'>Dollars: ${settings.get('monetag_dollars')} | Total: {settings.get('admin_total_earning')} | Users: {len(users)}</div>"
    html+="<form method=post action='/admin/save?pass=admin123'>"
    for k,v in settings.items(): html+=f"<label>{k}</label><input name='{k}' value='{v}' style='width:100%;padding:8px;margin:4px 0'><br>"
    html+="<button>Save All</button></form><h3>Users A-Z</h3><table border=1><tr><th>ID</th><th>Name</th><th>Join</th><th>Bal</th><th>Earn</th><th>Ads</th><th>Ref</th></tr>"
    for u in users: html+=f"<tr><td>{u['telegram_id']}</td><td>{u['name']}</td><td>{u['join_date']} {u['join_time']}</td><td>{u['balance']}</td><td>{u['total_earned']}</td><td>{u['ads_watched']}</td><td>{u['referrals']}</td></tr>"
    html+="</table><h3>Withdraws</h3><table border=1><tr><th>User</th><th>Amt</th><th>Method</th><th>Num</th><th>Request</th><th>Paid</th><th>Action</th></tr>"
    for w in withdraws: html+=f"<tr><td>{w['telegram_id']}</td><td>{w['amount']}</td><td>{w['method']}</td><td>{w['number']}</td><td>{w['request_time']}</td><td>{w['approve_time'] or '-'}</td><td><a href='/admin/approve?id={w['id']}&pass=admin123'>Paid</a></td></tr>"
    html+="</table></body>"; return html

@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.form.get('pass')=='admin123': session['admin']=True
    return redirect('/admin?pass=admin123')

@app.route('/admin/save', methods=['POST'])
def admin_save():
    conn=get_db()
    for k,v in request.form.items(): conn.execute('INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)',(k,v))
    conn.commit(); conn.close(); return redirect('/admin?pass=admin123')

@app.route('/admin/approve')
def admin_approve():
    conn=get_db(); conn.execute('UPDATE withdraws SET status=?, approve_time=? WHERE id=?',('paid',datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),request.args.get('id'))); conn.commit(); conn.close()
    return redirect('/admin?pass=admin123')

if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
