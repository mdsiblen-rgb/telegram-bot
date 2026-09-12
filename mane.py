# FINAL FULL BIG FILE - A TO Z - MINI BOY 11764581 - 9 TASK + FULL ADMIN CONTROL
from flask import Flask, jsonify, render_template_string, request
import json, os
from datetime import datetime

app = Flask(__name__)
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "users": {},
            "withdraws": [],
            "settings": {
                "app_name": "প্রতিদিনের কাজ BD",
                "ad_reward": 2,
                "ad_limit": 100,
                "ref_bonus": 20,
                "welcome_bonus": 60,
                "min_withdraw": 1000,
                "company_logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                "admin_msg_title": "অফিশিয়াল নোটিশ",
                "admin_msg_desc": "প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন",
                "my_ad_title": "🔥 স্পেশাল অফার",
                "my_ad_desc": "আজকের বোনাস",
                "payment_time": "২৪ ঘণ্টার ভিতর",
                "payment_rules": "মিনিমাম ১০০০ টাকা হলে Withdraw",
                "support_title": "🎧 সাপোর্ট",
                "support_desc": "যেকোনো সমস্যায় যোগাযোগ করুন",
                "support_extra": "২৪/৭ Active",
                "support_custom": "https://t.me/ProtidinerKajBD",
                "s1": "https://via.placeholder.com/600x250/1e40af/ffffff?text=Welcome+Bonus+60+Tk",
                "s2": "https://via.placeholder.com/600x250/0f766e/ffffff?text=Daily+100+Ads",
                "s3": "https://via.placeholder.com/600x250/be123c/ffffff?text=9+Tasks+Available"
            },
            "tasks": [
                {"title": "YouTube Channel Subscribe", "reward": 25, "link": "https://youtube.com", "color": "#dc2626"},
                {"title": "Telegram Channel Join", "reward": 10, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af"},
                {"title": "Facebook Page Follow", "reward": 15, "link": "https://facebook.com", "color": "#1877F2"},
                {"title": "Company Task 1 - Visit Site", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#7c3aed"},
                {"title": "Company Task 2 - Join Group", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#0f766e"},
                {"title": "Company Task 3 - Like Post", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#be123c"},
                {"title": "Company Task 4 - Share Post", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#065f46"},
                {"title": "Company Task 5 - Comment", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#1e40af"},
                {"title": "Company Task 6 - Invite Friend", "reward": 20, "link": "https://t.me/ProtidinerKajBD", "color": "#d97706"}
            ],
            "slider": [
                {"img": "https://via.placeholder.com/600x250/1e40af/ffffff?text=Bonus", "link": "https://t.me/ProtidinerKajBD"},
                {"img": "https://via.placeholder.com/600x250/0f766e/ffffff?text=Offer", "link": "https://t.me/ProtidinerKajBD"},
                {"img": "https://via.placeholder.com/600x250/be123c/ffffff?text=Reward", "link": "https://t.me/ProtidinerKajBD"}
            ]
        }
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def get_user(db, uid):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"balance": db["settings"]["welcome_bonus"], "ads_today": 0, "last_ad_date": str(datetime.now().date()), "claimed_tasks": [], "total_ref": 0, "ref_by": None, "joined": str(datetime.now())}
    u = db["users"][uid]
    if u["last_ad_date"]!= str(datetime.now().date()):
        u["ads_today"] = 0
        u["last_ad_date"] = str(datetime.now().date())
    return u

@app.route('/health')
def health(): return "ok", 200
@app.route('/')
def index(): return render_template_string(USER_HTML)
@app.route('/admin')
def admin_page(): return render_template_string(ADMIN_HTML)
@app.route('/api/get_full')
def get_full():
    db = load_db(); uid = request.args.get('id') or '8801'
    u = get_user(db, uid); save_db(db)
    return jsonify({"user": u, "settings": db["settings"], "tasks": db["tasks"], "slider": db["slider"]})
@app.route('/api/reward')
def reward():
    db = load_db(); uid = str(request.args.get('id')); u = get_user(db, uid)
    if u["ads_today"] >= db["settings"]["ad_limit"]: return jsonify({"msg": "আজকের Ads লিমিট শেষ!"})
    u["ads_today"] += 1; u["balance"] += db["settings"]["ad_reward"]; save_db(db)
    return jsonify({"msg": f'🎉 ৳{db["settings"]["ad_reward"]} যোগ হয়েছে!', "balance": u["balance"]})
@app.route('/api/claim_task')
def claim_task():
    db = load_db(); uid = str(request.args.get('id')); idx = int(request.args.get('idx')); u = get_user(db, uid)
    if idx in u["claimed_tasks"]: return jsonify({"msg": "এই টাস্ক আগেই নিয়েছেন!"})
    if idx >= len(db["tasks"]): return jsonify({"msg": "ভুল টাস্ক!"})
    u["claimed_tasks"].append(idx); u["balance"] += db["tasks"][idx]["reward"]; save_db(db)
    return jsonify({"msg": f'🎉 ৳{db["tasks"][idx]["reward"]} বোনাস পেয়েছেন!'})
@app.route('/api/withdraw')
def withdraw_req():
    db = load_db(); uid = str(request.args.get('id')); amount = int(request.args.get('amount', 0)); method = request.args.get('method'); num = request.args.get('number')
    u = get_user(db, uid)
    if u["balance"] < db["settings"]["min_withdraw"]: return jsonify({"msg": f'মিনিমাম ৳{db["settings"]["min_withdraw"]} লাগবে!'})
    if amount > u["balance"]: return jsonify({"msg": "ব্যালেন্স কম!"})
    u["balance"] -= amount; db["withdraws"].append({"uid": uid, "amount": amount, "method": method, "number": num, "time": str(datetime.now()), "status": "pending"}); save_db(db)
    return jsonify({"msg": "✅ Withdraw Request পাঠানো হয়েছে! ২৪ ঘণ্টার ভিতর পাবেন।"})
@app.route('/api/admin_all')
def admin_all(): return jsonify(load_db())
@app.route('/api/admin_save', methods=['POST'])
def admin_save():
    db = request.json; save_db(db); return jsonify({"msg": "Saved!"})

USER_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1'>
<title>Mini Boy 11764581</title>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
*{box-sizing:border-box}body{margin:0;background:#070f2b;color:#fff;font-family:'Segoe UI',system-ui;padding-bottom:85px}
.header{background:linear-gradient(135deg,#1e3a8a,#0f766e);padding:18px 16px 22px 16px;border-radius:0 0 24px 24px;position:sticky;top:0;z-index:10}
.bal{font-size:34px;font-weight:900;color:#4ade80;line-height:1}
.card{background:#111c44;border:1px solid #1e2d6a;margin:10px 12px;padding:14px;border-radius:16px}
.slider{height:160px;border-radius:16px;background:#1e2d6a;display:flex;align-items:center;justify-content:center;margin:10px 12px;overflow:hidden}
.slider img{width:100%;height:100%;object-fit:cover}
button{width:100%;padding:14px;background:linear-gradient(90deg,#2563eb,#0ea5e9);color:#fff;border:none;border-radius:12px;font-weight:800;font-size:15px}
.btn-task{margin-top:10px}
.nav{position:fixed;bottom:0;left:0;right:0;background:#0e1a3f;display:flex;justify-content:space-around;padding:10px 0 12px 0;border-top:1px solid #1e2d6a;z-index:20}
.nav div{text-align:center;font-size:11px;color:#7c8db0}.nav div.active{color:#3b82f6;font-weight:900}
.badge{background:#22c55e;color:#000;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:900}
</style></head><body>
<div id='root'>Loading Mini Boy 11764581 Full App...</div>
<div class='nav'><div class='active'>🏠<br>Home</div><div>✅<br>Tasks</div><div>👥<br>Refer</div><div>💰<br>Wallet</div></div>
<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';let DB={};
function load(){fetch('/api/get_full?id='+uid).then(r=>r.json()).then(d=>{DB=d;render()})}
function render(){
 let s=DB.settings,u=DB.user;
 let h=`<div class='header'><div style='display:flex;justify-content:space-between;align-items:center'><div><small style='opacity:.8'>${s.app_name}</small><div class='bal'>৳ ${u.balance}</div><small>Ads: ${u.ads_today}/${s.ad_limit} | Bonus: ৳${s.welcome_bonus}</small></div><img src='${s.company_logo}' style='width:48px;height:48px;border-radius:50%;border:2px solid #4ade80'></div></div>`;
 h+=`<div class='slider'><img src='${s.s1}' onerror="this.parentElement.innerHTML='🎁 Bonus Slider'"></div>`;
 h+=`<div class='card' style='background:linear-gradient(90deg,#1e3a8a,#0f766e)'><div style='display:flex;justify-content:space-between'><div><b>${s.admin_msg_title}</b><br><small>${s.admin_msg_desc}</small></div><span class='badge'>LIVE</span></div></div>`;
 h+=`<div class='card'><b>🎬 ${s.my_ad_title}</b> - <small>${s.my_ad_desc}</small><br><button onclick='watchAd()' style='margin-top:10px'>▶️ MINI BOY ADS দেখুন - ৳${s.ad_reward} পাবেন</button><small style='display:block;margin-top:6px;opacity:.6'>Zone: 11764581 - Monetag Many Boy</small></div>`;
 h+=`<div class='card'><b>📋 আজকের ৯ টি টাস্ক</b> - সবগুলোতে Mini Boy Ad বসানো আছে</div>`;
 DB.tasks.forEach((t,i)=>{
  let done=u.claimed_tasks.includes(i);
  h+=`<div class='card'><div style='display:flex;justify-content:space-between;align-items:center'><div><div style='font-weight:700'>${i<3?'⭐':'🏢'} ${t.title}</div><small style='opacity:.7'>Reward ৳${t.reward}</small></div><b style='color:${t.color}'>৳${t.reward}</b></div><button class='btn-task' onclick='claimTask(${i})' style='background:${done?'#16a34a':t.color}'>${done?'✅ Completed - Done':'👉 Claim + Watch Mini Boy Ad'}</button></div>`;
 });
 h+=`<div class='card'><b>${s.support_title}</b><br><small>${s.support_desc}</small><br><small style='color:#4ade80'>${s.support_extra}</small><br><small>Payment: ${s.payment_time}</small><br><small>${s.payment_rules}</small><br><button onclick="location.href='${s.support_custom}'" style='margin-top:10px;background:#0f766e'>💬 Support Join</button></div>`;
 h+=`<div class='card'><b>💰 Withdraw</b><br><input id='w_amount' type='number' placeholder='Amount - Min ${s.min_withdraw}' style='width:100%;padding:12px;border-radius:10px;border:1px solid #1e2d6a;background:#0a1229;color:#fff;margin:8px 0'><input id='w_method' placeholder='Bkash / Nagad' style='width:100%;padding:12px;border-radius:10px;border:1px solid #1e2d6a;background:#0a1229;color:#fff;margin-bottom:8px'><input id='w_number' placeholder='Number' style='width:100%;padding:12px;border-radius:10px;border:1px solid #1e2d6a;background:#0a1229;color:#fff;margin-bottom:8px'><button onclick='withdraw()'>Request Withdraw</button></div>`;
 document.getElementById('root').innerHTML=h;
}
function watchAd(){if(typeof show_11764581==='function'){show_11764581().then(()=>{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}).catch(()=>{alert('Ad Load হয়নি, আবার চেষ্টা করুন');})}else{fetch('/api/reward?id='+uid).then(r=>r.json()).then(x=>{alert(x.msg);load()})}}
function claimTask(i){if(typeof show_11764581==='function'){show_11764581().then(()=>{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})}).catch(()=>{alert('Ad দেখে Claim করুন')})}else{fetch('/api/claim_task?id='+uid+'&idx='+i).then(r=>r.json()).then(x=>{alert(x.msg);load()})}}
function withdraw(){let a=document.getElementById('w_amount').value,m=document.getElementById('w_method').value,n=document.getElementById('w_number').value;if(!a||!m||!n){alert('সব পূরণ করুন');return}fetch(`/api/withdraw?id=${uid}&amount=${a}&method=${m}&number=${n}`).then(r=>r.json()).then(x=>{alert(x.msg);load()})}
load();
</script></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Admin - Mini Boy 11764581 - Full A-Z</title>
<style>
body{margin:0;background:#070f2b;color:#fff;font-family:system-ui;padding:12px}
.card{background:#111c44;border:1px solid #1e2d6a;padding:14px;border-radius:14px;margin-bottom:12px}
button{padding:10px 14px;background:#2563eb;color:#fff;border:none;border-radius:8px;margin:4px;font-weight:700}
input,textarea{width:100%;padding:10px;border-radius:8px;border:1px solid #1e2d6a;background:#0a1229;color:#fff;margin:6px 0}
h2{color:#4ade80} table{width:100%;border-collapse:collapse} th,td{border:1px solid #1e2d6a;padding:8px;font-size:13px;text-align:left}
</style></head><body>
<h2>✅ ADMIN PANEL FULL - MINI BOY 11764581 - A TO Z</h2>
<div id='admin_root'>Loading Full Admin Data...</div>
<script>
let DB={};
function loadAdmin(){fetch('/api/admin_all').then(r=>r.json()).then(d=>{DB=d;renderAdmin()})}
function renderAdmin(){
 let s=DB.settings;
 let h=`<div class='card'><b>📊 Dashboard</b><br>Total Users: ${Object.keys(DB.users).length} | Withdraws: ${DB.withdraws.length} | Tasks: ${DB.tasks.length}<br><small>Zone: 11764581 - Monetag Many Boy SDK Active</small></div>`;
 h+=`<div class='card'><b>⚙️ Settings Control (Full A-Z)</b><br>
 App Name: <input id='app_name' value='${s.app_name}'><br>
 Ad Reward: <input id='ad_reward' type='number' value='${s.ad_reward}'> Ad Limit: <input id='ad_limit' type='number' value='${s.ad_limit}'><br>
 Welcome Bonus: <input id='welcome_bonus' type='number' value='${s.welcome_bonus}'> Min Withdraw: <input id='min_withdraw' type='number' value='${s.min_withdraw}'><br>
 Admin Title: <input id='admin_msg_title' value='${s.admin_msg_title}'><br>Admin Desc: <textarea id='admin_msg_desc'>${s.admin_msg_desc}</textarea><br>
 My Ad Title: <input id='my_ad_title' value='${s.my_ad_title}'><br>My Ad Desc: <input id='my_ad_desc' value='${s.my_ad_desc}'><br>
 Payment Time: <input id='payment_time' value='${s.payment_time}'><br>Payment Rules: <input id='payment_rules' value='${s.payment_rules}'><br>
 Support Title: <input id='support_title' value='${s.support_title}'><br>Support Desc: <input id='support_desc' value='${s.support_desc}'><br>Support Extra: <input id='support_extra' value='${s.support_extra}'><br>Support Link: <input id='support_custom' value='${s.support_custom}'><br>
 Slider1: <input id='s1' value='${s.s1}'><br>Slider2: <input id='s2' value='${s.s2}'><br>Slider3: <input id='s3' value='${s.s3}'><br>
 <button onclick='saveSettings()'>💾 Save All Settings</button></div>`;

 h+=`<div class='card'><b>👥 All Users (Full Control)</b><br><table><tr><th>User ID</th><th>Balance</th><th>Ads Today</th><th>Tasks Done</th></tr>`;
 Object.entries(DB.users).forEach(([uid,u])=>{h+=`<tr><td>${uid}</td><td>৳${u.balance}</td><td>${u.ads_today}</td><td>${u.claimed_tasks.length}</td></tr>`});
 h+=`</table></div>`;

 h+=`<div class='card'><b>💰 Withdraw Requests</b><br><table><tr><th>User</th><th>Amount</th><th>Method</th><th>Number</th><th>Time</th></tr>`;
 DB.withdraws.slice(-20).reverse().forEach(w=>{h+=`<tr><td>${w.uid}</td><td>৳${w.amount}</td><td>${w.method}</td><td>${w.number}</td><td>${w.time.slice(0,19)}</td></tr>`});
 h+=`</table></div>`;

 h+=`<div class='card'><b>📋 9 Tasks Control (Full Edit)</b><br>`;
 DB.tasks.forEach((t,i)=>{h+=`Task ${i+1}: <input id='t_title_${i}' value='${t.title}'> Reward: <input id='t_reward_${i}' type='number' value='${t.reward}' style='width:80px'> Link: <input id='t_link_${i}' value='${t.link}'> Color: <input id='t_color_${i}' value='${t.color}' style='width:100px'><br><br>`});
 h+=`<button onclick='saveTasks()'>💾 Save Tasks</button></div>`;

 h+=`<div class='card'><a href='/'><button>Go to User App</button></a> <a href='/api/admin_all'><button>View JSON</button></a></div>`;
 document.getElementById('admin_root').innerHTML=h;
}
function saveSettings(){
 let s=DB.settings;
 s.app_name=document.getElementById('app_name').value; s.ad_reward=parseInt(document.getElementById('ad_reward').value); s.ad_limit=parseInt(document.getElementById('ad_limit').value);
 s.welcome_bonus=parseInt(document.getElementById('welcome_bonus').value); s.min_withdraw=parseInt(document.getElementById('min_withdraw').value);
 s.admin_msg_title=document.getElementById('admin_msg_title').value; s.admin_msg_desc=document.getElementById('admin_msg_desc').value;
 s.my_ad_title=document.getElementById('my_ad_title').value; s.my_ad_desc=document.getElementById('my_ad_desc').value;
 s.payment_time=document.getElementById('payment_time').value; s.payment_rules=document.getElementById('payment_rules').value;
 s.support_title=document.getElementById('support_title').value; s.support_desc=document.getElementById('support_desc').value; s.support_extra=document.getElementById('support_extra').value; s.support_custom=document.getElementById('support_custom').value;
 s.s1=document.getElementById('s1').value; s.s2=document.getElementById('s2').value; s.s3=document.getElementById('s3').value;
 fetch('/api/admin_save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DB)}).then(r=>r.json()).then(x=>{alert(x.msg);loadAdmin()});
}
function saveTasks(){
 DB.tasks.forEach((t,i)=>{t.title=document.getElementById('t_title_'+i).value; t.reward=parseInt(document.getElementById('t_reward_'+i).value); t.link=document.getElementById('t_link_'+i).value; t.color=document.getElementById('t_color_'+i).value;});
 fetch('/api/admin_save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DB)}).then(r=>r.json()).then(x=>{alert(x.msg);loadAdmin()});
}
loadAdmin();
</script></body></html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
