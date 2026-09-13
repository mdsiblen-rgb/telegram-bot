from flask import Flask, request, render_template_string
import json, os
app = Flask(__name__)
FILE="config.json"
CFG={
 "balance":60,"zone":"11764581","direct":"https://omg10.com/4/11760259",
 "app_name":"Protidiner Kaj BD",
 "banner":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
 "profile_name":"Md Shamim","profile_photo":"https://i.pravatar.cc/150",
 "custom_title":"🔥 আজকের ধামাকা অফার",
 "custom_text":"আজ 50 টা Ads দেখলেই 100 TK বোনাস!",
 "custom_btn":"Join Now",
 "tasks":[{"title":f"Task {i+1} - {['YouTube','Telegram','Facebook','Insta','Like'][i%5]}","reward":10,"link":"https://omg10.com/4/11760259"} for i in range(20)]
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
body{margin:0;background:#06122e;color:#fff;font-family:sans-serif;padding-bottom:90px}
.header{background:#0e2252;padding:14px 16px;display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:10}
.tick{background:#00ff88;color:#000;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:14px;box-shadow:0 0 10px #00ff88}
.balbox{background:#0a1940;padding:18px 22px;border-radius:0 0 28px 28px}
.bal{color:#00ff88;font-size:52px;font-weight:900}
.notice{margin:12px;background:#102a5e;border:2px solid #00ff88;border-radius:16px;padding:13px;display:flex;justify-content:space-between;align-items:center}
.live{background:#00ff88;color:#000;padding:7px 16px;border-radius:22px;font-weight:900;display:flex;align-items:center;gap:7px;box-shadow:0 0 15px #00ff88}
.dot{width:10px;height:10px;background:#000;border-radius:50%;animation:blink 0.8s infinite}
@keyframes blink{0%{opacity:1} 50%{opacity:0.1} 100%{opacity:1}}
.banner{margin:12px;height:210px;border-radius:20px;background:url('{{c.banner}}') center/cover}
.custom{background:linear-gradient(90deg,#ff8c00,#ff5e00);margin:12px;padding:16px;border-radius:18px}
.btn{width:100%;padding:13px 16px;border:none;border-radius:12px;font-weight:700;font-size:16px;margin-top:10px;box-shadow:0 4px 12px rgba(0,0,0,0.3)}
.btn:active{transform:scale(0.97)}
.btn-bonus{background:linear-gradient(90deg,#00ff88,#00cc6a);color:#000}
.btn-blue{background:linear-gradient(90deg,#00aaff,#0066ff);color:#fff}
.btn-red{background:linear-gradient(90deg,#ff3b3b,#cc0000);color:#fff}
.btn-white{background:#fff;color:#ff5e00}
.taskbox{margin:10px 12px;background:#102a5e;padding:14px;border-radius:12px;display:flex;justify-content:space-between}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:0;width:100%;background:#06122e;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1a3a7a}
.nav div{opacity:0.5;text-align:center;font-size:12px}.nav div.on{opacity:1;color:#00ff88}
.profile-card{margin:16px;background:#102a5e;padding:20px;border-radius:20px;text-align:center}
.profile-card img{width:90px;height:90px;border-radius:50%;border:3px solid #00ff88}
</style>
</head><body>
<div class="header"><span>👑</span><b>{{c.app_name}}</b><span class="tick">✓</span></div>

<div id="home" class="page active">
  <div class="balbox"><div class="bal">৳ {{c.balance}}</div><div>Ads: 0/100</div></div>
  <div class="notice"><div><b>Official Notice</b><br><small>Watch Ads Daily - Earn Upto ৳500</small></div><div class="live"><div class="dot"></div>LIVE</div></div>
  <div class="banner"></div>
  <div class="custom"><b>{{c.custom_title}}</b><br><small>{{c.custom_text}}</small><br>
  <button class="btn btn-white" onclick="show_{{c.zone}}('pop'); window.open('{{c.direct}}','_blank');">{{c.custom_btn}}</button></div>
  <div style="margin:12px;background:#102a5e;padding:16px;border-radius:16px"><b>🎬 স্পেশাল অফার</b>
  <button class="btn btn-bonus" onclick="show_{{c.zone}}().then(()=>window.open('{{c.direct}}','_blank'))">▶ ADS দেখুন - ৳2 বোনাস</button></div>
</div>

<div id="tasks" class="page"><div style="padding:16px"><h2>Tasks - 20 টা</h2></div>
{% for t in c.tasks %}
<div class="taskbox"><span>⭐ {{t.title}}</span><b>৳{{t.reward}}</b></div>
<div style="margin:0 12px 12px 12px"><button class="btn btn-red" onclick="show_{{c.zone}}().then(()=>window.open('{{t.link}}','_blank'))">▶ Join & Get {{t.reward}} Tk</button></div>
{% endfor %}</div>

<div id="refer" class="page"><div style="padding:20px"><h2>Refer</h2><div style="background:#102a5e;padding:20px;border-radius:16px"><button class="btn btn-blue">Copy Refer Link</button></div></div></div>
<div id="wallet" class="page"><div style="padding:20px"><h2>Wallet</h2><div style="background:#102a5e;padding:20px;border-radius:16px">Balance: ৳{{c.balance}}<br><br><button class="btn btn-bonus">Withdraw</button></div></div></div>
<div id="profile" class="page"><div class="profile-card"><img src="{{c.profile_photo}}"><h2>{{c.profile_name}}</h2><p>{{c.app_name}} Member</p></div></div>

<div class="nav">
  <div class="on" onclick="go('home',this)">🏠<br>Home</div>
  <div onclick="go('tasks',this)">✅<br>Tasks</div>
  <div onclick="go('refer',this)">👥<br>Refer</div>
  <div onclick="go('wallet',this)">💰<br>Wallet</div>
  <div onclick="go('profile',this)">👤<br>Profile</div>
</div>

<script>
function go(id,el){
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 document.getElementById(id).classList.add('active');
 document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('on'));
 el.classList.add('on');
 show_{{c.zone}}({type:'inApp', inAppSettings:{frequency:1,capping:0,interval:0,timeout:5,everyPage:true}});
}
function startInApp(){
  show_{{c.zone}}({type:'inApp', inAppSettings:{frequency:1,capping:0,interval:0,timeout:5,everyPage:true}});
}
startInApp();
setInterval(startInApp, 30000);
</script>
</body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML, c=load())
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "No Access"
    c=load()
    th="".join([f"{i+1}. <input name=title{i} value='{t['title']}' style='width:120px'> ৳<input name=reward{i} value='{t['reward']}' style='width:40px'> Link:<input name=link{i} value='{t['link']}' style='width:200px'><br><br>" for i,t in enumerate(c['tasks'])])
    return f'''<div style="padding:10px"><h2>Admin Panel</h2><form method=POST action=/admin/save?id=8807178385>
    App Name: <input name=app_name value="{c['app_name']}"><br><br>
    Banner URL: <input name=banner value="{c['banner']}" style="width:90%"><br><br>
    Profile Name: <input name=profile_name value="{c['profile_name']}"> Photo: <input name=profile_photo value="{c['profile_photo']}" style="width:60%"><br><br>
    Custom: <input name=custom_title value="{c['custom_title']}" style="width:90%"><br><textarea name=custom_text style="width:90%">{c['custom_text']}</textarea><br><br>
    DirectLink: <input name=direct value="{c['direct']}" style="width:80%"><br><br><hr><h3>20 Links:</h3>{th}<button style="padding:12px 30px;background:#00ff88;font-weight:900">SAVE ALL</button></form></div>'''
@app.route('/admin/save', methods=['POST'])
def save():
    c=load()
    for k in ['app_name','banner','profile_name','profile_photo','custom_title','custom_text','direct']:
        if request.form.get(k): c[k]=request.form.get(k)
    nt=[]
    for i in range(20):
        if request.form.get(f'title{i}'):
            nt.append({"title":request.form.get(f'title{i}'),"reward":int(request.form.get(f'reward{i}') or 10),"link":request.form.get(f'link{i}')})
    if nt: c['tasks']=nt
    with open(FILE,'w',encoding='utf-8') as f: json.dump(c,f,ensure_ascii=False,indent=2)
    return "Saved! <a href=/>Home</a>"
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
