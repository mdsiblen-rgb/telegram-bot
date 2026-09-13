from flask import Flask, request, render_template_string
import json, os
app = Flask(__name__)
FILE="config.json"
CFG={
 "app_name":"Protidiner Kaj BD",
 "balance":60,
 "daily_limit":30,
 "zone":"11764581",
 "direct":"https://omg10.com/4/11760259",
 "banner":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
 "profile_name":"Md Shamim",
 "profile_photo":"https://i.pravatar.cc/150?img=68",
 "support_link":"https://t.me/your_support",
 "bkash":"01700000000","nagad":"01700000000",
 "notice_title":"Official Notice","notice_text":"Watch Ads Daily - Earn Upto ৳500",
 "offer_title":"আজকের ধামাকা অফার","offer_text":"আজ 30 টা Ads দেখলেই 100 TK বোনাস!","offer_btn":"Join Now",
 "tasks":[{"title":f"Daily Task {i+1}","reward":5,"link":"https://omg10.com/4/11760259"} for i in range(30)]
}
def load():
    if os.path.exists(FILE):
        try:
            with open(FILE,'r',encoding='utf-8') as f: return json.load(f)
        except: return CFG
    return CFG

HTML="""
<!DOCTYPE html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='{{c.zone}}' data-sdk='show_{{c.zone}}'></script>
<style>
body{margin:0;background:#06122e;color:#fff;font-family:sans-serif;padding-bottom:95px}
.header{background:#0e2252;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:20;border-bottom:2px solid #00ff88}
.h-left{display:flex;align-items:center;gap:8px}
.center-name{flex:1;text-align:center;font-size:22px;font-weight:900;letter-spacing:1px;background:linear-gradient(90deg,#fff,#00ff88);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tick{background:#00ff88;color:#000;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 0 10px #00ff88}
.header-pic{width:42px;height:42px;border-radius:50%;border:3px solid #00ff88;object-fit:cover}
.balbox{background:linear-gradient(180deg,#0a1940,#06122e);padding:18px 22px;border-radius:0 0 28px 28px;border-bottom:1px solid #102a5e}
.bal{color:#00ff88;font-size:52px;font-weight:900}
.limit-bar{background:#102a5e;height:10px;border-radius:10px;margin-top:10px;overflow:hidden}
.limit-fill{background:#00ff88;height:100%;width:0%;transition:0.5s}
.notice{margin:12px;background:#102a5e;border:2px solid #00ff88;border-radius:16px;padding:13px;display:flex;justify-content:space-between;align-items:center}
.live{background:#00ff88;color:#000;padding:7px 16px;border-radius:22px;font-weight:900;display:flex;align-items:center;gap:7px;animation:liveBlink 1s infinite}
.dot{width:10px;height:10px;background:#005500;border-radius:50%;animation:dotBlink 0.8s infinite}
@keyframes liveBlink{0%{box-shadow:0 0 5px #00ff88} 50%{box-shadow:0 0 25px #00ff88} 100%{box-shadow:0 0 5px #00ff88}}
@keyframes dotBlink{0%{opacity:1} 50%{opacity:0} 100%{opacity:1}}
.banner{margin:12px;height:200px;border-radius:20px;background:url('{{c.banner}}') center/cover;border:2px solid #1a3a7a}
.box{margin:12px;background:#102a5e;border-radius:18px;padding:16px;border:1px solid #1a3a7a}
.company-box{border:2px solid #00aaff;background:#0d1f4a;text-align:center;min-height:100px;display:flex;align-items:center;justify-content:center;flex-direction:column}
.offer-box{background:linear-gradient(90deg,#ff8c00,#ff5e00)}
.support-box{background:linear-gradient(90deg,#00aaff,#0066ff);display:flex;justify-content:space-between;align-items:center}
.btn{width:100%;padding:14px 16px;border:none;border-radius:12px;font-weight:800;font-size:16px;margin-top:10px}
.btn-white{background:#fff;color:#ff5e00}
.btn-green{background:linear-gradient(90deg,#00ff88,#00cc6a);color:#000}
.btn-red{background:linear-gradient(90deg,#ff3b3b,#cc0000);color:#fff}
.taskbox{margin:10px 12px;background:#102a5e;padding:14px;border-radius:12px;display:flex;justify-content:space-between;align-items:center}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:0;width:100%;background:#0a1940;display:flex;justify-content:space-around;padding:10px 0;border-top:2px solid #00ff88;z-index:20}
.nav div{opacity:0.5;text-align:center;font-size:12px}.nav div.on{opacity:1;color:#00ff88;font-weight:900}
.profile-card{margin:16px;background:#102a5e;padding:20px;border-radius:20px;text-align:center;border:2px solid #00ff88}
.profile-card img{width:110px;height:110px;border-radius:50%;border:4px solid #00ff88}
.withdraw-logo{width:60px;height:60px;background:#fff;border-radius:12px;padding:8px;object-fit:contain}
</style>
</head><body>
<div class="header">
  <div class="h-left"><span>👑</span><span class="tick">✓</span></div>
  <div class="center-name">{{c.app_name}}</div>
  <img src="{{c.profile_photo}}" class="header-pic">
</div>

<div id="home" class="page active">
  <div class="balbox">
    <div class="bal">৳ {{c.balance}}</div>
    <div style="display:flex;justify-content:space-between"><span>Ads Today:</span><span id="adsCount">0 / {{c.daily_limit}}</span></div>
    <div class="limit-bar"><div id="limitFill" class="limit-fill"></div></div>
    <small id="limitMsg" style="color:#00ff88"></small>
  </div>

  <div class="notice"><div><b>{{c.notice_title}}</b><br><small>{{c.notice_text}}</small></div><div class="live"><div class="dot"></div>LIVE</div></div>
  <div class="banner"></div>

  <!-- মাঝখানে কোম্পানির এড - সুন্দর ছোট এড, ঢুকলেই আসবে না -->
  <div class="box company-box" id="companyBox">
    <small style="color:#00aaff">Ads by Monetag</small>
    <b style="margin-top:5px">📢 স্পন্সরড এড আসছে...</b>
    <small>12 সেকেন্ড পর লোড হবে</small>
  </div>

  <div class="box offer-box"><b>🔥 {{c.offer_title}}</b><br><small>{{c.offer_text}}</small><br>
  <button class="btn btn-white" onclick="handleAd('{{c.direct}}')">{{c.offer_btn}}</button></div>

  <div class="box support-box"><div><b>💬 সাপোর্ট বক্স</b><br><small>যেকোনো সমস্যায় মেসেজ দিন</small></div><button onclick="window.open('{{c.support_link}}','_blank')" style="background:#fff;color:#0066ff;border:none;padding:10px 18px;border-radius:20px;font-weight:900">Support</button></div>

  <div class="box"><b>🎬 ডেইলি বোনাস</b><br><button class="btn btn-green" onclick="handleAd('{{c.direct}}')">▶ ADS দেখুন - ৳2</button></div>
</div>

<div id="tasks" class="page"><div style="padding:16px"><h2>Tasks - 30 টা</h2><small>প্রতিদিন {{c.daily_limit}} টা লিমিট</small></div>
{% for t in c.tasks %}
<div class="taskbox"><span>⭐ {{t.title}}</span><b>৳{{t.reward}}</b></div>
<div style="margin:0 12px 12px 12px"><button class="btn btn-red" onclick="handleAd('{{t.link}}')">▶ দেখুন ও আয় করুন</button></div>
{% endfor %}</div>

<div id="refer" class="page"><div style="padding:16px"><div class="box"><h3>👥 রেফার বক্স</h3><p>প্রতি রেফারে ৳20 বোনাস</p><div style="background:#06122e;padding:12px;border-radius:10px;word-break:break-all">https://protidiner-kaj.com/ref?{{c.profile_name}}</div><button class="btn btn-green">Copy Link</button></div></div></div>

<div id="wallet" class="page"><div style="padding:16px">
  <div class="box" style="text-align:center"><h2>💰 Wallet ৳{{c.balance}}</h2></div>
  <div class="box"><h3>💸 উইথড্র সিস্টেম</h3>
    <div style="display:flex;gap:10px;justify-content:center;margin:15px 0">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/BKash_Logo_Icon.svg/1200px-BKash_Logo_Icon.svg.png" class="withdraw-logo">
      <img src="https://download.logo.wine/logo/Nagad/Nagad-Logo.wine.png" class="withdraw-logo">
      <img src="https://play-lh.googleusercontent.com/1p1Zp5x0g8d5h5Y5Y5Y5Y5Y5Y5Y5Y5Y5" class="withdraw-logo" onerror="this.src='https://cdn-icons-png.flaticon.com/512/825/825462.png'">
    </div>
    Bkash: {{c.bkash}}<br>Nagad: {{c.nagad}}<br><br>
    <input id="wdAmount" placeholder="Amount (Min 500)" style="width:100%;padding:12px;border-radius:10px;border:none">
    <select style="width:100%;padding:12px;border-radius:10px;margin-top:10px"><option>bKash</option><option>Nagad</option><option>Rocket</option></select>
    <button class="btn btn-green" onclick="alert('Withdraw Request Sent!')">Withdraw</button>
  </div>
</div></div>

<div id="profile" class="page"><div class="profile-card"><img src="{{c.profile_photo}}"><h2>{{c.profile_name}}</h2><p>Admin - {{c.app_name}}</p><div style="background:#06122e;padding:10px;border-radius:10px;margin-top:10px">👑 Verified Admin<br>📞 Support: {{c.support_link}}</div></div>
<div class="box"><b>ℹ️ About</b><br><small>এটি একটি আর্নিং প্ল্যাটফর্ম। প্রতিদিন {{c.daily_limit}} টা এড দেখে আয় করুন।</small></div>
</div>

<div class="nav">
  <div class="on" onclick="go('home',this)">🏠<br>Home</div>
  <div onclick="go('tasks',this)">✅<br>Tasks</div>
  <div onclick="go('refer',this)">👥<br>Refer</div>
  <div onclick="go('wallet',this)">💰<br>Wallet</div>
  <div onclick="go('profile',this)">👤<br>Profile</div>
</div>

<script>
let adsToday = parseInt(localStorage.getItem('adsToday') || '0');
let lastDate = localStorage.getItem('adsDate') || '';
let today = new Date().toDateString();
if(lastDate!== today){ adsToday=0; localStorage.setItem('adsDate', today); localStorage.setItem('adsToday','0'); }
let LIMIT = {{c.daily_limit}};

function updateLimitUI(){
  document.getElementById('adsCount').innerText = adsToday + ' / ' + LIMIT;
  document.getElementById('limitFill').style.width = (adsToday/LIMIT*100)+'%';
  if(adsToday>=LIMIT){ document.getElementById('limitMsg').innerText='আজকের লিমিট শেষ! কাল আবার দেখতে পারবেন'; }
  else{ document.getElementById('limitMsg').innerText= (LIMIT-adsToday)+' টা বাকি আছে'; }
}
updateLimitUI();

function go(id,el){
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 document.getElementById(id).classList.add('active');
 document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('on'));
 el.classList.add('on');
}

function handleAd(link){
  if(adsToday>=LIMIT){ alert('আজকের '+LIMIT+' টা এড দেখা শেষ! কাল আসুন'); return; }
  // এড দেখাও - শুধু বাটনে ক্লিক করলে
  show_{{c.zone}}().then(()=>{
    adsToday++; localStorage.setItem('adsToday', adsToday); updateLimitUI();
    window.open(link,'_blank');
  });
}

// কোম্পানির ছোট এড - 12 সেকেন্ড পর, ঢুকলেই না, ইউজার বিরক্ত হবে না
setTimeout(()=>{
  document.getElementById('companyBox').innerHTML = '<small style=color:#00aaff>Ads by Monetag - Sponsor</small><div style=margin-top:8px>Company Ad Loaded</div>';
  show_{{c.zone}}({type:'inApp', inAppSettings:{frequency:1,capping:0,interval:30,timeout:5,everyPage:false}});
}, 12000);
</script>
</body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML, c=load())
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "No Access"
    c=load()
    th="".join([f"<div style='background:#fff;padding:8px;margin:5px;border-radius:8px'><b>{i+1}</b><input name=title{i} value='{t['title']}' style='width:95%'><br>Reward:<input name=reward{i} value='{t['reward']}' style='width:60px'> Link:<input name=link{i} value='{t['link']}' style='width:95%'></div>" for i,t in enumerate(c['tasks'])])
    return f'''
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <div style="padding:12px;background:#f0f2f5;font-family:sans-serif">
    <h2>👑 Admin Panel - তোর সব কন্ট্রোল</h2>
    <form method=POST action=/admin/save?id=8807178385>
    App Name (বড় করে মাঝখানে দেখাবে):<br><input name=app_name value="{c['app_name']}" style="width:100%;padding:14px;font-size:18px"><br><br>
    তোর ছবি URL (ফিক্সড, আর চেঞ্জ হবে না):<br><input name=profile_photo value="{c['profile_photo']}" style="width:100%;padding:12px"><br><img src="{c['profile_photo']}" style="width:70px;height:70px;border-radius:50%;border:3px solid #00ff88;margin-top:5px"><br><br>
    তোর নাম:<br><input name=profile_name value="{c['profile_name']}" style="width:100%;padding:12px"><br><br>
    Banner URL:<br><input name=banner value="{c['banner']}" style="width:100%;padding:12px"><br><br>
    Daily Limit (30):<br><input name=daily_limit value="{c['daily_limit']}" style="width:100%;padding:12px"><br><br>
    Direct Link:<br><input name=direct value="{c['direct']}" style="width:100%;padding:12px"><br><br>
    Support Telegram Link:<br><input name=support_link value="{c['support_link']}" style="width:100%;padding:12px"><br><br>
    Bkash Number:<br><input name=bkash value="{c['bkash']}" style="width:100%;padding:12px"><br>
    Nagad Number:<br><input name=nagad value="{c['nagad']}" style="width:100%;padding:12px"><br><br>
    <h3>Offer Box</h3>
    Title:<input name=offer_title value="{c['offer_title']}" style="width:100%;padding:12px"><br>
    Text:<textarea name=offer_text style="width:100%;padding:12px">{c['offer_text']}</textarea><br><br>
    <h3>30 Tasks</h3>{th}
    <button style="width:100%;padding:18px;background:#00ff88;color:#000;font-weight:900;font-size:20px;border:none;border-radius:14px;margin-top:20px">💾 SAVE ALL - ফোন থেকে সেভ</button>
    </form></div>'''
@app.route('/admin/save', methods=['POST'])
def save():
    c=load()
    for k in ['app_name','banner','profile_photo','profile_name','direct','support_link','bkash','nagad','offer_title','offer_text']:
        if request.form.get(k): c[k]=request.form.get(k)
    if request.form.get('daily_limit'): c['daily_limit']=int(request.form.get('daily_limit'))
    if request.form.get('balance'): c['balance']=request.form.get('balance')
    nt=[]
    for i in range(30):
        if request.form.get(f'title{i}'): nt.append({"title":request.form.get(f'title{i}'),"reward":int(request.form.get(f'reward{i}') or 5),"link":request.form.get(f'link{i}')})
    if nt: c['tasks']=nt
    with open(FILE,'w',encoding='utf-8') as f: json.dump(c,f,ensure_ascii=False,indent=2)
    return f"✅ Saved! <a href=/>Home দেখো</a> | <a href=/admin?id=8807178385>Admin Back</a>"
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
