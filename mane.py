from flask import Flask, request, render_template_string
import json, os
app = Flask(__name__)
FILE="config.json"
CFG={
 "app_name":"Protidiner Kaj BD","balance":60,"daily_limit":30,
 "direct":"https://omg10.com/4/11760259",
 "banner":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
 "profile_name":"Md Shamim","profile_photo":"https://i.pravatar.cc/150?img=68",
 "support_link":"https://t.me/your_support","bkash":"01700000000","nagad":"01700000000",
 "offer_title":"আজকের ধামাকা অফার","offer_text":"আজ 30 টা কাজ করলেই 100 TK বোনাস",
 "tasks":[{"title":f"Task {i+1}","reward":5,"link":"https://omg10.com/4/11760259"} for i in range(30)]
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
<style>
body{margin:0;background:#06122e;color:#fff;font-family:sans-serif;padding-bottom:95px}
.header{background:#0e2252;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:20;border-bottom:2px solid #00ff88}
.center-name{flex:1;text-align:center;font-size:22px;font-weight:900;color:#00ff88}
.header-pic{width:42px;height:42px;border-radius:50%;border:3px solid #00ff88}
.balbox{background:#0a1940;padding:18px 22px;border-radius:0 0 28px 28px}
.bal{color:#00ff88;font-size:50px;font-weight:900}
.notice{margin:12px;background:#102a5e;border:2px solid #00ff88;border-radius:16px;padding:13px;display:flex;justify-content:space-between}
.live{background:#00ff88;color:#000;padding:6px 14px;border-radius:20px;font-weight:900;animation:blink 1s infinite}
@keyframes blink{0%{box-shadow:0 0 5px #00ff88}50%{box-shadow:0 0 20px #00ff88}100%{box-shadow:0 0 5px #00ff88}}
.banner{margin:12px;height:200px;border-radius:20px;background:url('{{c.banner}}') center/cover}
.box{margin:12px;background:#102a5e;border-radius:18px;padding:16px}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;margin-top:10px}
.btn-green{background:#00ff88;color:#000}
.btn-red{background:#ff3b3b;color:#fff}
.btn-white{background:#fff;color:#ff5e00}
.taskbox{margin:10px 12px;background:#102a5e;padding:12px;border-radius:12px;display:flex;justify-content:space-between}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:0;width:100%;background:#0a1940;display:flex;justify-content:space-around;padding:10px 0;border-top:2px solid #00ff88}
.nav div{opacity:0.5;text-align:center;font-size:12px}.nav div.on{opacity:1;color:#00ff88}
.profile-card{margin:16px;background:#102a5e;padding:20px;border-radius:20px;text-align:center;border:2px solid #00ff88}
.profile-card img{width:110px;height:110px;border-radius:50%;border:4px solid #00ff88}
</style>
</head><body>
<div class="header"><div>👑 ✓</div><div class="center-name">{{c.app_name}}</div><img src="{{c.profile_photo}}" class="header-pic"></div>

<div id="home" class="page active">
  <div class="balbox"><div class="bal">৳ {{c.balance}}</div><div id="adsCount">0 / {{c.daily_limit}}</div></div>
  <div class="notice"><div><b>Official Notice</b><br><small>Watch Daily - Earn ৳500</small></div><div class="live">● LIVE</div></div>
  <div class="banner"></div>
  <div class="box" style="border:2px dashed #00aaff;text-align:center"><small style="color:#00aaff">Company Ads</small><br><b>এখানে কোম্পানির এড আসবে না, শুধু বাটনে ক্লিক করলে Direct Link খুলবে</b><br><button class="btn btn-green" onclick="handleAd('{{c.direct}}')">▶ Company Ad দেখুন</button></div>
  <div class="box" style="background:linear-gradient(90deg,#ff8c00,#ff5e00)"><b>🔥 {{c.offer_title}}</b><br><small>{{c.offer_text}}</small><br><button class="btn btn-white" onclick="handleAd('{{c.direct}}')">Join Now</button></div>
  <div class="box"><b>💬 Support Box</b><br><button onclick="window.open('{{c.support_link}}')" style="padding:8px 16px;border-radius:20px;border:none;background:#fff;color:#0066ff;font-weight:900">Support</button></div>
</div>

<div id="tasks" class="page"><div style="padding:16px"><h2>Tasks 30 টা</h2></div>
{% for t in c.tasks %}<div class="taskbox"><span>{{t.title}}</span><b>৳{{t.reward}}</b></div><div style="margin:0 12px 12px"><button class="btn btn-red" onclick="handleAd('{{t.link}}')">▶ Join</button></div>{% endfor %}</div>
<div id="refer" class="page"><div style="padding:16px"><div class="box"><h3>Refer Box</h3><button class="btn btn-green">Copy Link</button></div></div></div>
<div id="wallet" class="page"><div style="padding:16px"><div class="box"><h2>Wallet ৳{{c.balance}}</h2>Bkash: {{c.bkash}}<br>Nagad: {{c.nagad}}<br><br><input placeholder="Amount" style="width:100%;padding:12px;border-radius:10px;border:none"><br><button class="btn btn-green" style="margin-top:10px">Withdraw</button></div></div></div>
<div id="profile" class="page"><div class="profile-card"><img src="{{c.profile_photo}}"><h2>{{c.profile_name}}</h2><p>{{c.app_name}}</p></div></div>

<div class="nav">
  <div class="on" onclick="go('home',this)">🏠<br>Home</div>
  <div onclick="go('tasks',this)">✅<br>Tasks</div>
  <div onclick="go('refer',this)">👥<br>Refer</div>
  <div onclick="go('wallet',this)">💰<br>Wallet</div>
  <div onclick="go('profile',this)">👤<br>Profile</div>
</div>

<script>
let adsToday=parseInt(localStorage.getItem('adsToday')||'0');
let today=new Date().toDateString();
if(localStorage.getItem('adsDate')!==today){adsToday=0;localStorage.setItem('adsDate',today);}
let LIMIT={{c.daily_limit}};
document.getElementById('adsCount').innerText=adsToday+' / '+LIMIT+' Ads';
function go(id,el){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('on'));el.classList.add('on');}
function handleAd(link){
 if(adsToday>=LIMIT){alert('আজকের 30 টা শেষ, কাল আসুন');return;}
 adsToday++;localStorage.setItem('adsToday',adsToday);
 document.getElementById('adsCount').innerText=adsToday+' / '+LIMIT+' Ads';
 window.open(link,'_blank');
}
</script>
</body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML, c=load())
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "No"
    c=load()
    th="".join([f"<div style='background:#fff;padding:8px;margin:5px'><b>{i+1}</b><input name=title{i} value='{t['title']}' style='width:95%'><br><input name=link{i} value='{t['link']}' style='width:95%'></div>" for i,t in enumerate(c['tasks'])])
    return f'<meta name="viewport" content="width=device-width,initial-scale=1"><div style="padding:10px"><h2>Admin - Redmi Phone</h2><form method=POST action=/admin/save?id=8807178385>App Name বড় করে:<br><input name=app_name value="{c["app_name"]}" style="width:100%;padding:12px"><br><br>তোমার ছবি URL:<br><input name=profile_photo value="{c["profile_photo"]}" style="width:100%"><br><br>{th}<button style="width:100%;padding:15px;background:#00ff88;font-weight:900">SAVE</button></form></div>'
@app.route('/admin/save', methods=['POST'])
def save():
    c=load()
    for k in ['app_name','profile_photo','profile_name','banner','direct','bkash','nagad']:
        if request.form.get(k): c[k]=request.form.get(k)
    nt=[]
    for i in range(30):
        if request.form.get(f'title{i}'): nt.append({"title":request.form.get(f'title{i}'),"reward":5,"link":request.form.get(f'link{i}')})
    if nt: c['tasks']=nt
    with open(FILE,'w',encoding='utf-8') as f: json.dump(c,f,ensure_ascii=False,indent=2)
    return "Saved <a href=/>Home</a>"
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
