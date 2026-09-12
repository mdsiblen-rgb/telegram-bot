"title": "YouTube ভিডিও দেখুন",
                    "reward": 25,
                    "link": "https://youtube.com/@ProtidinerKajBD",
                    "btn": "শুরু করুন",
                    "type": "youtube",
                    "color": "#065f46"
                },
                {
                    "title": "Telegram Channel Join",
                    "reward": 10,
                    "link": "https://t.me/ProtidinerKajBD",
                    "btn": "Join",
                    "type": "telegram",
                    "color": "#1e40af"
                },
                {
                    "title": "Facebook Follow",
                    "reward": 15,
                    "link": "https://www.facebook.com/share/1AXw16vWRj/",
                    "btn": "Follow",
                    "type": "facebook",
                    "color": "#1877F2"
                },
                {
                    "title": "Company Task 1",
                    "reward": 20,
                    "link": "https://t.me/ProtidinerKajBD",
                    "btn": "Visit",
                    "type": "company",
                    "color": "#7c3aed"
                },
                {
                    "title": "Company Task 2",
                    "reward": 20,
                    "link": "https://t.me/ProtidinerKajBD",
                    "btn": "Visit",
                    "type": "company",
                    "color": "#0f766e"
                },
                {
                    "title": "Company Task 3",
                    "reward": 20,
                    "link": "https://t.me/ProtidinerKajBD",
                    "btn": "Visit",
                    "type": "company",
                    "color": "#be123c"
                }
            ]
        }
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def is_admin(id):
    try:
        return int(id) == ADMIN_ID
    except:
        return False

def keep_alive():
    while True:
        try:
            time.sleep(240)
            requests.get(f"{SELF_URL}/health", timeout=5)
        except:
            pass

threading.Thread(target=keep_alive, daemon=True).start()

# =========================================================================
# USER HTML - BIG FILE ORIGINAL - 5 NUMBER PAGE BLUE FIXED
# =========================================================================
USER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD - BIG FILE - FINAL BLUE</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src='https://libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@500;700&display=swap" rel="stylesheet">
<style>
* { font-family: 'Hind Siliguri', sans-serif; box-sizing: border-box; margin: 0; padding: 0 }
body { max-width: 430px; margin: 0 auto; background: #eef2ff; padding-bottom: 160px }
.top { background: #1e40af; color: #fff; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 10 }
.top img { width: 36px; height: 36px; border-radius: 50%; background: #fff; object-fit: cover }
.card { background: #fff; margin: 12px; border-radius: 20px; padding: 16px; box-shadow: 0 4px 18px rgba(0,0,0,.06) }
.bal-big { font-size: 52px; font-weight: 900; text-align: center; color: #1e40af }
.btn-blue { width: 100%; background: #1e40af; color: #fff; padding: 14px; border: none; border-radius: 14px; font-weight: 700; font-size: 16px }
.btn-yellow { background: #f59e0b; color: #fff; padding: 12px 22px; border: none; border-radius: 12px; font-weight: 700 }
.slider { margin: 12px; border-radius: 22px; height: 185px; overflow: hidden; position: relative; background: #000 }
.slide { position: absolute; inset: 0; opacity: 0; transition:.8s }
.slide.active { opacity: 1 }
.slide img { width: 100%; height: 100%; object-fit: cover }
.dots { text-align: center; margin-top: 8px }
.dot { width: 8px; height: 8px; background: #cbd5e1; border-radius: 50%; display: inline-block; margin: 0 3px }
.dot.active { background: #1e40af; width: 20px }
.wd-method { display: flex; gap: 10px }
.wd-card { flex: 1; border: 2px solid #e2e8f0; border-radius: 16px; padding: 14px; text-align: center; cursor: pointer; background: #fff }
.wd-card.selected { border-color: #e2136e; box-shadow: 0 0 0 3px rgba(226,19,110,.15) }
.wd-card img { width: 60px; height: 60px; object-fit: contain }
.wd-input { width: 100%; padding: 14px; border-radius: 14px; border: 1px solid #e2e8f0; margin-top: 12px; background: #f8fafc; font-size: 15px }
.btm { position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 430px; background: #fff; display: flex; border-top: 1px solid #e2e8f0; padding: 14px 0 18px 0; z-index: 99; box-shadow: 0 -4px 15px rgba(0,0,0,.08) }
.btm div { flex: 1; text-align: center; color: #94a3b8; font-size: 14px; font-weight: 700; cursor: pointer; padding: 8px 4px; border-radius: 14px; transition:.2s; line-height: 1.2 }
.btm div.on { color: #1e40af; background: #e8edff; transform: scale(1.15) }
.btm div span.icon { font-size: 24px; display: block }
/* 5 NUMBER PAGE - BEFORE GREEN - NOW BLUE - AS YOU SAID */
.prof { background: linear-gradient(135deg,#1e40af,#1e3a8a); color: #fff; margin: 12px; border-radius: 22px; padding: 18px; display: flex; gap: 14px }
.prof img { width: 64px; height: 64px; border-radius: 50%; background: #fff; object-fit: cover; border: 2px solid #fff }
.gcard { background: #1e40af; color: #fff; margin: 10px 12px; border-radius: 16px; padding: 14px; display: flex; justify-content: space-between; align-items: center }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 12px }
.scard { background: #fff; border-radius: 16px; padding: 14px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,.05) }
</style>
</head>
<body>

<div class="top">
    <div style="display:flex;gap:10px;align-items:center;font-weight:700">
        <img id="companyLogo" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png">
        <span id="appNameTop">প্রতিদিনের কাজ BD</span>
    </div>
    <div style="font-weight:900">৳<span id="topBal">60</span></div>
</div>

<!-- HOME -->
<div id="t-home">
    <div class="slider" id="slider"></div>
    <div class="dots" id="dots"></div>
    <div class="card">
        <div class="bal-big">৳<span id="bal">60</span></div>
        <div style="text-align:center;color:#64748b;margin:8px 0">আপনার বর্তমান ব্যালেন্স</div>
        <button class="btn-blue" onclick="go('earn')">💰 আয় করুন</button>
    </div>
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
                <div style="font-size:18px">🎁 Daily Check-in</div>
                <div style="color:#64748b;font-size:13px">প্রতিদিন বোনাস ৳10</div>
            </div>
            <button class="btn-yellow" onclick="dailyCheck()">আজকের বোনাস নিন</button>
        </div>
    </div>
    <div class="card" style="border:2px dashed #1e40af;background:#f0f7ff">
        <div style="font-weight:700;color:#1e40af" id="myAdTitle">🔥 আজকের স্পেশাল অফার</div>
        <div style="font-size:14px;margin-top:6px" id="myAdDesc">এখানে তোমার নিজের বিজ্ঞাপন লিখবে</div>
    </div>
    <div class="card">
        <div style="font-weight:700">Admin Message</div>
        <div style="font-weight:900;font-size:17px;margin:6px 0" id="adminTitle">অফিশিয়াল চ্যানেল</div>
        <div style="font-size:13px;color:#334155" id="adminDesc">Ads দেখুন, Task করুন</div>
    </div>
<button class="btn-blue" id="adBtn" onclick="watchAd()">▶ বিজ্ঞাপন দেখুন</button>
        <div style="font-size:12px;margin-top:8px;color:#64748b">Limit: <span id="adLim">100</span> | Watched: <span id="watched">0</span></div>
    </div>
    <div id="tasksBox"></div>
    <div class="card" style="background:#1e40af;color:#fff">
        <b>🔗 রেফার লিংক - ৳<span id="rb">20</span> বোনাস</b>
        <div id="rl" style="background:#fff;color:#000;padding:10px;border-radius:10px;margin-top:8px;word-break:break-all;font-size:12px"></div>
        <button class="btn-blue" style="background:#f59e0b;margin-top:8px" onclick="copyR()">📋 কপি করুন</button>
        <div style="margin-top:8px">মোট রেফার: <span id="rc">0</span> জন</div>
    </div>
</div>

<!-- SUPPORT -->
<div id="t-support" style="display:none">
    <div class="card">
        <h3 id="sT" style="text-align:center">🎧 সাপোর্ট সেন্টার</h3>
        <div id="sD" style="text-align:center;margin:8px 0"></div>
        <div id="sE" style="background:#fff7ed;padding:10px;border-radius:10px;text-align:center"></div>
        <button class="btn-blue" style="margin-top:12px" onclick="window.open(document.getElementById('chLink').value)">📢 Telegram Channel</button>
        <button class="btn-blue" style="margin-top:10px;background:#FF0000" onclick="window.open(document.getElementById('ytLink').value)">▶️ YouTube</button>
        <button class="btn-blue" style="margin-top:10px;background:#1877F2" onclick="window.open(document.getElementById('fbLink').value)">📘 Facebook Page</button>
        <div id="customSupportBox" style="margin-top:16px;background:#f0fdf4;border:2px dashed #0f766e;padding:14px;border-radius:14px;display:none">
            <div style="font-weight:700;color:#0f766e;text-align:center">📝 এডমিনের নতুন বার্তা - তোমার খালি জায়গা</div>
            <div id="customSupport" style="margin-top:8px;text-align:center;font-size:14px;color:#334155;white-space:pre-wrap"></div>
        </div>
    </div>
</div>

<!-- WITHDRAW -->
<div id="t-withdraw" style="display:none">
    <div class="card">
        <div style="font-weight:700;text-align:center">💳 পেমেন্ট মেথড</div>
        <div class="wd-method" style="margin-top:14px">
            <div class="wd-card selected" id="cardBkash" onclick="sel('bKash')">
                <img src="https://upload.wikimedia.org/wikipedia/commons/f/f2/BKash-bKash-Logo.wine.png">
                <div style="margin-top:8px;color:#e2136e;font-weight:700;font-size:13px">✓ bKash</div>
            </div>
            <div class="wd-card" id="cardNagad" onclick="sel('Nagad')">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1e/Nagad_Logo.png">
                <div style="margin-top:8px;font-weight:700;font-size:13px">Nagad</div>
            </div>
        </div>
        <input class="wd-input" id="wNum" placeholder="01XXXXXXXXXX - Number">
        <input class="wd-input" id="wAmt" type="number" placeholder="Amount - Min ৳1000">
        <button class="btn-blue" style="margin-top:12px" onclick="doWd()">💸 Withdraw Request</button>
        <div style="margin-top:12px;background:#f8fafc;padding:10px;border-radius:10px;font-size:12px">
            <div>⏰ Payment Time: <span id="payTime"></span></div>
            <div>📜 Rules: <span id="payRule"></span></div>
        </div>
    </div>
</div>

<!-- PROFILE - 5 NUMBER PAGE - NOW BLUE -->
<div id="t-profile" style="display:none">
    <div class="prof">
        <img id="pImg" src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png">
        <div style="flex:1">
            <div id="pn" style="font-weight:900;font-size:18px">User</div>
            <div style="font-size:13px;opacity:.9">ID: <span id="pid"></span></div>
            <div style="font-size:13px;opacity:.9">UID2: <span id="uid2"></span></div>
            <input id="en" class="wd-input" style="padding:8px;color:#000;background:#fff" placeholder="নতুন নাম লিখুন">
            <input id="av" class="wd-input" style="padding:8px;margin-top:6px;color:#000;background:#fff" placeholder="ছবির লিংক https://...">
    
</div><button onclick="cn()" style="width:100%;background:#f59e0b;color:#fff;padding:10px;border:none;border-radius:10px;margin-top:8px;font-weight:700">✅ নাম + ছবি সেভ করুন</button>
        </div>
    </div>
    <div class="gcard">
        <span>💼 ব্যালেন্স</span>
        <b>৳<span id="pBal">0</span></b>
    </div>
    <div class="grid">
        <div class="scard">
            <small>আজকের আয়</small><br>
            <b id="pt">৳0</b>
        </div>
        <div class="scard">
            <small>মোট Ads</small><br>
            <b id="pa">0 টি</b>
        </div>
        <div class="scard">
            <small>গতকাল</small><br>
            <b id="py">৳0</b>
        </div>
        <div class="scard">
            <small>মোট উইথড্র</small><br>
            <b id="ptw">0</b>
        </div>
    </div>
    <div class="gcard">
        <span>👥 মোট রেফার</span>
        <b id="pr">0 জন</b>
    </div>
    <div class="gcard">
        <span>💰 মোট আয়</span>
        <b id="ptot">৳0</b>
    </div>
</div>

<div class="btm">
    <div id="b-home" class="on" onclick="go('home')"><span class="icon">🏠</span>হোম</div>
    <div id="b-earn" onclick="go('earn')"><span class="icon">📦</span>আয়</div>
    <div id="b-support" onclick="go('support')"><span class="icon">🎧</span>সাপোর্ট</div>
    <div id="b-withdraw" onclick="go('withdraw')"><span class="icon">💳</span>উইথড্র</div>
    <div id="b-profile" onclick="go('profile')"><span class="icon">👤</span>প্রোফাইল</div>
</div>

<script>
let uid = new URLSearchParams(location.search).get('id')  '8807178385';
let curSlide = 0;
let selectedMethod = 'bKash';

function go(t){
    ['home','earn','support','withdraw','profile'].forEach(x=>{
        document.getElementById('t-'+x).style.display = x==t? 'block' : 'none';
        document.getElementById('b-'+x).classList.toggle('on', x==t);
    });
}

function sel(m){
    selectedMethod = m;
    document.getElementById('cardBkash').classList.toggle('selected', m=='bKash');
    document.getElementById('cardNagad').classList.toggle('selected', m=='Nagad');
}

function load(){
    fetch("/api/get_full?id="+uid)
   .then(r=>r.json())
   .then(d=>{
        document.getElementById('topBal').innerText = d.user.balance;
        document.getElementById('bal').innerText = d.user.balance;
        document.getElementById('pBal').innerText = d.user.balance;
        document.getElementById('pid').innerText = uid;
        document.getElementById('uid2').innerText = uid;
        document.getElementById('pn').innerText = d.user.name;
        document.getElementById('watched').innerText = d.user.ads_watched  0;
        document.getElementById('pa').innerText = (d.user.ads_watched  0) + ' টি';
        document.getElementById('pt').innerText = '৳' + (d.user.today_earn  0);
        document.getElementById('py').innerText = '৳' + (d.user.yesterday_earn  0);
        document.getElementById('ptw').innerText = d.user.total_withdraw  0;
        document.getElementById('pr').innerText = (d.user.refer_count  0) + ' জন';
        document.getElementById('rc').innerText = d.user.refer_count  0;
        document.getElementById('ptot').innerText = '৳' + (d.user.total_earn  0);
        document.getElementById('adRate').innerText = d.settings.ad_reward;
        document.getElementById('adRate2').innerText = d.settings.ad_reward;
        document.getElementById('adLim').innerText = d.settings.ad_limit;
        document.getElementById('rb').innerText = d.settings.ref_bonus;
        document.getElementById('appNameTop').innerText = d.settings.app_name;
        document.getElementById('adminTitle').innerText = d.settings.admin_msg_title;
        document.getElementById('adminDesc').innerText = d.settings.admin_msg_desc;
        document.getElementById('myAdTitle').innerText = d.settings.my_ad_title;
        document.getElementById('myAdDesc').innerText = d.settings.my_ad_desc;
        document.getElementById('payTime').innerText = d.settings.payment_time;
        document.getElementById('payRule').innerText = d.settings.payment_rules;

<!-- EARN -->
<div id="t-earn" style="display:none">
    <div class="card">
        <div style="font-size:14px">প্রতি Ads ৳<span id="adRate">1</span> | Timer 30s</div>
        <div class="bal-big" style="margin:10px 0">৳<span id="adRate2">1</span></div>


        document.getElementById('sT').innerText = d.settings.support_title;
        document.getElementById('sD').innerText = d.settings.support_desc;
        document.getElementById('sE').innerText = d.settings.support_extra;
        let cs = d.settings.support_custom  '';
        document.getElementById('customSupport').innerText = cs;
        document.getElementById('customSupportBox').style.display = cs? 'block' : 'none';
        document.getElementById('rl').innerText = 'https://t.me/ProtidinerKajBD_bot?start=' + uid;
        document.getElementById('companyLogo').src = d.settings.company_logo;

        // Slider
        let sBox = document.getElementById('slider');
        let dBox = document.getElementById('dots');
        sBox.innerHTML = '';
        dBox.innerHTML = '';
        d.slider.forEach((s,i)=>{
            sBox.innerHTML += <div class="slide ${i==0?'active':''}" onclick="window.open('${s.link}')"><img src="${s.img}"></div>;
            dBox.innerHTML += <div class="dot ${i==0?'active':''}"></div>;
        });

        // Tasks
        let tBox = document.getElementById('tasksBox');
        tBox.innerHTML = '';
        d.tasks.forEach((t,idx)=>{
            tBox.innerHTML += 
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-weight:700">${t.title}</span>
                    <b style="color:#1e40af">৳${t.reward}</b>
                </div>
                <div style="display:flex;gap:8px;margin-top:10px">
                    <button class="btn-blue" style="background:${t.color};flex:1" onclick="window.open('${t.link}')">🔗 Link</button>
                    <button class="btn-blue" style="background:#0f766e;flex:1" onclick="claimTask(${idx})">✅ Claim</button>
                </div>
            </div>;
        });
    });
}

setInterval(()=>{
    let sl = document.querySelectorAll('.slide');
    let dt = document.querySelectorAll('.dot');
    if(!sl.length) return;
    sl[curSlide].classList.remove('active');
    dt[curSlide].classList.remove('active');
    curSlide = (curSlide+1)%sl.length;
    sl[curSlide].classList.add('active');
    dt[curSlide].classList.add('active');
},3000);

function watchAd(){
    if(typeof show_11764581!== 'undefined'){
        show_11764581().then(()=>{
            fetch("/api/reward?id="+uid).then(r=>r.json()).then(x=>{ alert(x.msg); load(); });
        });
    }else{
        fetch("/api/reward?id="+uid).then(r=>r.json()).then(x=>{ alert(x.msg); load(); });
    }
}

function claimTask(i){
    fetch("/api/claim_task?id="+uid+"&idx="+i).then(r=>r.json()).then(x=>{ alert(x.msg); load(); });
}

function doWd(){
    let n = document.getElementById('wNum').value;
    let a = document.getElementById('wAmt').value;
    fetch("/api/withdraw?id="+uid+"&num="+n+"&amt="+a+"&method="+selectedMethod).then(r=>r.json()).then(x=>alert(x.msg));
}

function cn(){
    let v = document.getElementById('en').value.trim();
    let av = document.getElementById('av').value.trim();
    fetch("/api/update_profile?id="+uid+"&name="+encodeURIComponent(v)+"&avatar="+encodeURIComponent(av))
   .then(r=>r.json()).then(x=>{ alert(x.msg); load(); });
}

function copyR(){
    navigator.clipboard.writeText(document.getElementById('rl').innerText).then(()=>alert('Copy ✅'));
}

function dailyCheck(){
    fetch("/api/daily?id="+uid).then(r=>r.json()).then(x=>{ alert(x.msg); load(); });
}

load();
</script>
</body>
</html>
"""

# =========================================================================
# ADMIN HTML - BIG FILE ORIGINAL - RAJA PANEL
# =========================================================================
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Admin Raja - BIG FILE FINAL BLUE</title>
<style>
body{max-width:700px;margin:0 auto;background:#eef6f3;font-family:sans-serif;padding-bottom:100px}

.card{background:#fff;border-radius:16px;padding:14px;margin:10px;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.inp{width:100%;padding:12px;border-radius:12px;border:1px solid #ddd;margin-top:6px}
.lab{font-weight:700;margin-top:12px;display:block;font-size:14px}
.tab{padding:10px 14px;border-radius:12px;background:#e2e8f0;margin:3px;cursor:pointer;display:inline-block;font-weight:700}
.tab.on{background:#1e40af;color:#fff}
</style>
</head>
<body>

<div style="background:linear-gradient(135deg,#1e40af,#1e3a8a);color:#fff;padding:18px;border-radius:18px;margin:10px">
    <h1>👑 ADMIN RAJA - BIG FILE FINAL BLUE A-Z</h1>
    <p>Company Logo + Profile Blue + সব টাকা কন্ট্রোল + খালি জায়গা</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:12px">
        <div style="background:rgba(255,255,255,.2);padding:10px;border-radius:12px;text-align:center"><b id="sUsers">0</b><div style="font-size:11px">Users</div></div>
        <div style="background:rgba(255,255,255,.2);padding:10px;border-radius:12px;text-align:center"><b id="sWd">0</b><div style="font-size:11px">Pending</div></div>
        <div style="background:rgba(255,255,255,.2);padding:10px;border-radius:12px;text-align:center"><b id="sEarn">0</b><div style="font-size:11px">Taka</div></div>
    </div>
</div>

<div style="margin:10px">
    <span class="tab on" id="tab-dash" onclick="showTab('dash')">Dash</span>
    <span class="tab" id="tab-users" onclick="showTab('users')">Users</span>
    <span class="tab" id="tab-wd" onclick="showTab('wd')">Wd</span>
    <span class="tab" id="tab-settings" onclick="showTab('settings')">Settings Raja - BIG</span>
</div>

<div id="t-dash">
    <div class="card">Big File - Final Blue - A-Z সব আছে ভাই</div>
</div>

<div id="t-users" style="display:none">
    <div class="card"><h3>👥 Users List</h3><div id="userList"></div></div>
</div>

<div id="t-wd" style="display:none">
    <div class="card"><h3>💸 Withdraw Requests</h3><div id="wdList"></div></div>
</div>

<div id="t-settings" style="display:none">

    <div class="card">
        <h2 style="font-weight:900">🏢 Company Logo - ওই কোনাতে</h2>
        <label class="lab">Company Logo URL:</label>
        <input id="companyLogo" class="inp" placeholder="https://...">
        <label class="lab">App Name:</label>
        <input id="appName" class="inp">
    </div>

    <div class="card">
        <h2 style="font-weight:900">💰 টাকার সিস্টেম - 100% চেঞ্জ হবে - তোমার দাবি</h2>
        <label class="lab">Per Ads Reward:</label><input id="perAd" class="inp" type="number">
        <label class="lab">Ads Limit:</label><input id="adLim" class="inp" type="number">
        <label class="lab">YouTube Reward:</label><input id="ytR" class="inp" type="number">
        <label class="lab">Telegram Reward:</label><input id="tgR" class="inp" type="number">
        <label class="lab">Facebook Reward:</label><input id="fbR" class="inp" type="number">
        <label class="lab">Company1 Reward:</label><input id="c1R" class="inp" type="number">
        <label class="lab">Company2 Reward:</label><input id="c2R" class="inp" type="number">
        <label class="lab">Company3 Reward:</label><input id="c3R" class="inp" type="number">
        <label class="lab">Welcome Bonus:</label><input id="wel" class="inp" type="number">
        <label class="lab">Refer Bonus:</label><input id="rb" class="inp" type="number">
        <label class="lab">Min Withdraw:</label><input id="minW" class="inp" type="number">
    </div>

    <div class="card">
        <h2 style="font-weight:900">📢 Home + Support Edit</h2>
        <label class="lab">My Ad Title:</label><input id="myAdTitle" class="inp">
        <label class="lab">My Ad Desc:</label><input id="myAdDesc" class="inp">
        <label class="lab">Admin Title:</label><input id="adTitle" class="inp">
        <label class="lab">Admin Desc:</label><input id="adDesc" class="inp">
        <label class="lab">Support Title:</label><input id="sT" class="inp">
        <label class="lab">Support Desc:</label><input id="sD" class="inp">
        <label class="lab">Support Extra:</label><input id="sE" class="inp">
        <label class="lab" style="color:#0f766e">📝 Support Custom - খালি জায়গায় লেখা (তোমার নতুন ফিক্স):</label>
        <textarea id="sCustom" class="inp" rows="4" placeholder="এখানে যা লিখবে Support পেজের নিচে খালি জায়গায় দেখাবে"></textarea>
    </div>

    <div class="card">
        <h2 style="font-weight:900">🔗 6 টা লিংক - তোমার বড় ফাইলের</h2>
        <label class="lab">YouTube Link:</label><input id="ytLink" class="inp">
        <label class="lab">Telegram Channel Link:</label><input id="chLink" class="inp">
        <label class="lab">Facebook Page Link:</label><input id="fbLink" class="inp">
        <label class="lab">Company Link 1:</label><input id="c1" class="inp">
        <label class="lab">Company Link 2:</label><input id="c2" class="inp">
        <label class="lab">Company Link 3:</label><input id="c3" class="inp">
    </div>

    <div class="card">
        <h2 style="font-weight:900">💸 Withdraw Setting</h2>
        <label class="lab">Payment Time:</label><input id="payTime" class="inp">
        <label class="lab">Payment Rules:</label><input id="payRule" class="inp">
    </div>

    <div class="card">
        <h2 style="font-weight:900">🖼️ Slider Images</h2>
        <label class="lab">Slider 1 Image URL:</label><input id="s1" class="inp">
        <label class="lab">Slider 2 Image URL:</label><input id="s2" class="inp">
        <label class="lab">Slider 3 Image URL:</label><input id="s3" class="inp">
    </div>

    <button onclick="saveAll()" style="width:100%;background:#1e40af;color:#fff;padding:16px;border-radius:14px;font-weight:900;margin:12px 0">💾 SAVE ALL - FINAL BIG FILE A-Z BLUE</button>
</div>

<script>
let qp = new URLSearchParams(location.search);
let aid = qp.get('id')  '8807178385';

function showTab(t){
    ['dash','users','wd','settings'].forEach(x=>{
        document.getElementById('t-'+x).style.display = x==t? 'block' : 'none';
        document.getElementById('tab-'+x).classList.toggle('on', x==t);
    });
}

function load(){
    fetch("/api/admin/stats?id="+aid).then(r=>r.json()).then(d=>{
        document.getElementById('sUsers').innerText = d.total_users;
        document.getElementById('sWd').innerText = d.pending_wd;
        document.getElementById('sEarn').innerText = d.total_taka;
    });

    fetch("/api/get_full?id="+aid).then(r=>r.json()).then(d=>{
        document.getElementById('companyLogo').value = d.settings.company_logo;
        document.getElementById('appName').value = d.settings.app_name;
        document.getElementById('perAd').value = d.settings.ad_reward;
        document.getElementById('adLim').value = d.settings.ad_limit;
        document.getElementById('ytR').value = d.tasks[0].reward;
        document.getElementById('tgR').value = d.tasks[1].reward;
        document.getElementById('fbR').value = d.tasks[2].reward;
        document.getElementById('c1R').value = d.tasks[3].reward;
        document.getElementById('c2R').value = d.tasks[4].reward;
        document.getElementById('c3R').value = d.tasks[5].reward;
        document.getElementById('wel').value = d.settings.welcome_bonus;
        document.getElementById('rb').value = d.settings.ref_bonus;
        document.getElementById('minW').value = d.settings.min_withdraw;
        document.getElementById('myAdTitle').value = d.settings.my_ad_title;
        document.getElementById('myAdDesc').value = d.settings.my_ad_desc;
        document.getElementById('adTitle').value = d.settings.admin_msg_title;

document.getElementById('fbLink').value = d.tasks[2].link;
        document.getElementById('c1').value = d.tasks[3].link;
        document.getElementById('c2').value = d.tasks[4].link;
        document.getElementById('c3').value = d.tasks[5].link;
        document.getElementById('payTime').value = d.settings.payment_time;
        document.getElementById('payRule').value = d.settings.payment_rules;
        document.getElementById('s1').value = d.slider[0].img;
        document.getElementById('s2').value = d.slider[1].img;
        document.getElementById('s3').value = d.slider[2].img;
    });

    fetch("/api/admin/users?id="+aid).then(r=>r.json()).then(d=>{
        let l = document.getElementById('userList');
        l.innerHTML = '';
        d.forEach(u=>{
            l.innerHTML += <div style="display:flex;gap:10px;padding:10px;background:#f9fafb;margin:6px 0;border-radius:10px"><img src="${u.avatar||'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'}" style="width:40px;height:40px;border-radius:50%;object-fit:cover"><div><b>${u.name}</b><br>৳${u.balance} | ${u.id}</div></div>
        });
    });

    fetch("/api/admin/withdraws?id="+aid).then(r=>r.json()).then(d=>{
        let l = document.getElementById('wdList');
        l.innerHTML = '';
        d.forEach(w=>{
            l.innerHTML += <div style="display:flex;justify-content:space-between;padding:10px;background:#f9fafb;margin:6px 0;border-radius:10px"><div>${w.uid} - ৳${w.amt} - ${w.num}</div><button onclick="approve('${w.uid}','${w.amt}')" style="background:green;color:#fff;padding:6px 12px;border-radius:6px">Approve</button></div>
        });
    });
}

function saveAll(){
    let data = {
        companyLogo: document.getElementById('companyLogo').value,
        appName: document.getElementById('appName').value,
        perAd: document.getElementById('perAd').value,
        adLim: document.getElementById('adLim').value,
        ytR: document.getElementById('ytR').value,
        tgR: document.getElementById('tgR').value,
        fbR: document.getElementById('fbR').value,
        c1R: document.getElementById('c1R').value,
        c2R: document.getElementById('c2R').value,
        c3R: document.getElementById('c3R').value,
        wel: document.getElementById('wel').value,
        refB: document.getElementById('rb').value,
        minW: document.getElementById('minW').value,
        myAdTitle: document.getElementById('myAdTitle').value,
        myAdDesc: document.getElementById('myAdDesc').value,
        adTitle: document.getElementById('adTitle').value,
        adDesc: document.getElementById('adDesc').value,
        sT: document.getElementById('sT').value,
        sD: document.getElementById('sD').value,
        sE: document.getElementById('sE').value,
        sCustom: document.getElementById('sCustom').value,
        ytLink: document.getElementById('ytLink').value,
        chLink: document.getElementById('chLink').value,
        fbLink: document.getElementById('fbLink').value,
        c1: document.getElementById('c1').value,
        c2: document.getElementById('c2').value,
        c3: document.getElementById('c3').value,
        payTime: document.getElementById('payTime').value,
        payRule: document.getElementById('payRule').value,
        s1: document.getElementById('s1').value,
        s2: document.getElementById('s2').value,
        s3: document.getElementById('s3').value
    };
    fetch("/api/admin/save_all?id="+aid,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data)
    }).then(()=>alert('✅ Save - Big File Final Blue'));
}

function approve(uid,amt){
    fetch("/api/admin/approve?id="+aid+"&uid="+uid+"&amt="+amt).then(()=>{ alert('Approved'); load(); });
}

load();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(USER_HTML)

@app.route('/admin')
def admin_page():
    if not is_admin(request.args.get('id')):
        return "Unauthorized", 403
    return render_template_string(ADMIN_HTML)

@app.route('/health')
def health():
        
        document.getElementById('adDesc').value = d.settings.admin_msg_desc;
        document.getElementById('sT').value = d.settings.support_title;
        document.getElementById('sD').value = d.settings.support_desc;
        document.getElementById('sE').value = d.settings.support_extra;
        document.getElementById('sCustom').value = d.settings.support_custom  '';
        document.getElementById('ytLink').value = d.tasks[0].link;
        document.getElementById('chLink').value = d.tasks[1].link;


        return "ok", 200

@app.route('/api/get_full')
def get_full():
    uid = request.args.get('id', '8807178385')
    d = load_db()
    if uid not in d['users']:
        d['users'][uid] = {
            "balance": d['settings']['welcome_bonus'],
            "ads_watched": 0,
            "name": f"User {uid[-4:]}",
            "avatar": "",
            "today_earn": 0,
            "yesterday_earn": 0,
            "total_earn": d['settings']['welcome_bonus'],
            "total_withdraw": 0,
            "refer_count": 0,
            "task_claims": {}
        }
        save_db(d)
    return jsonify({
        "user": d['users'][uid],
        "settings": d['settings'],
        "slider": d['slider'],
        "tasks": d['tasks']
    })

@app.route('/api/reward')
def reward():
    uid = request.args.get('id')
    d = load_db()
    if d['users'][uid]['ads_watched'] >= d['settings']['ad_limit']:
        return jsonify({"msg": "লিমিট শেষ - কাল আবার"})
    d['users'][uid]['balance'] += d['settings']['ad_reward']
    d['users'][uid]['ads_watched'] += 1
    d['users'][uid]['today_earn'] = d['users'][uid].get('today_earn', 0) + d['settings']['ad_reward']
    d['users'][uid]['total_earn'] = d['users'][uid].get('total_earn', 0) + d['settings']['ad_reward']
    save_db(d)
    return jsonify({"msg": f"৳{d['settin
