from flask import Flask, request, render_template_string
import json, os
app = Flask(__name__)
FILE="config.json"
CFG={
 "balance":60,"zone":"11764581","direct":"https://omg10.com/4/11760259",
 "app_name":"Protidiner Kaj BD",
 "banner":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
 "profile_name":"Md Shamim","profile_photo":"https://i.pravatar.cc/150",
 "custom_title":"আজকের ধামাকা অফার","custom_text":"আজ 50 টা Ads দেখলেই 100 TK বোনাস!","custom_btn":"Join Now",
 "ad_box_title":"🎁 স্পেশাল বোনাস বক্স","ad_box_text":"এখানে তোমার বিজ্ঞাপন বসবে","ad_box_btn":"এখনই দেখুন","ad_box_link":"https://omg10.com/4/11760259","ad_box_banner":"https://images.unsplash.com/photo-1611224923853-80b023f02d71",
 "tasks":[{"title":f"Task {i+1}","reward":10,"link":"https://omg10.com/4/11760259"} for i in range(20)]
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
.header{background:#0e2252;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:10}
.h-left{display:flex;align-items:center;gap:10px}
.tick{background:#00ff88;color:#000;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900}
.header-pic{width:38px;height:38px;border-radius:50%;border:2px solid #00ff88;object-fit:cover}
.balbox{background:#0a1940;padding:18px 22px;border-radius:0 0 28px 28px}
.bal{color:#00ff88;font-size:52px;font-weight:900}
.notice{margin:12px;background:#102a5e;border:2px solid #00ff88;border-radius:16px;padding:13px;display:flex;justify-content:space-between;align-items:center}
.live{background:#00ff88;color:#000;padding:7px 16px;border-radius:22px;font-weight:900;display:flex;align-items:center;gap:7px;animation:liveBlink 1s infinite}
.dot{width:10px;height:10px;background:#005500;border-radius:50%;animation:dotBlink 0.8s infinite}
@keyframes liveBlink{0%{box-shadow:0 0 5px #00ff88} 50%{box-shadow:0 0 20px #00ff88} 100%{box-shadow:0 0 5px #00ff88}}
@keyframes dotBlink{0%{opacity:1} 50%{opacity:0} 100%{opacity:1}}
.banner{margin:12px;height:210px;border-radius:20px;background:url('{{c.banner}}') center/cover}
.custom{background:linear-gradient(90deg,#ff8c00,#ff5e00);margin:12px;padding:16px;border-radius:18px}
.adbox{margin:12px;background:#102a5e;border:2px dashed #ff8c00;border-radius:18px;overflow:hidden}
.adbox img{width:100%;height:160px;object-fit:cover}
.adbox-inner{padding:14px}
.btn{width:100%;padding:13px 16px;border:none;border-radius:12px;font-weight:700;font-size:16px;margin-top:10px}
.btn-bonus{background:linear-gradient(90deg,#00ff88,#00cc6a);color:#000}
.btn-red{background:linear-gradient(90deg,#ff3b3b,#cc0000);color:#fff}
.btn-white{background:#fff;color:#ff5e00}
.btn-orange{background:linear-gradient(90deg,#ff8c00,#ff5e00);color:#fff}
.taskbox{margin:10px 12px;background:#102a5e;padding:14px;border-radius:12px;display:flex;justify-content:space-between}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:0;width:100%;background:#06122e;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1a3a7a}
.nav div{opacity:0.5;text-align:center;font-size:12px}.nav div.on{opacity:1;color:#00ff88}
.profile-card{margin:16px;background:#102a5e;padding:20px;border-radius:20px;text-align:center}
.profile-card img{width:90px;height:90px;border-radius:50%;border:3px solid #00ff88}
</style>
</head><body>
<div class="header">
  <div class="h-left"><span>👑</span><b>{{c.app_name}}</b><span class="tick">✓</span></div>
  <img src="{{c.profile_photo}}" class="header-pic" onclick="go('profile',document.querySelectorAll('.nav div')[4])">
</div>

<div id="home" class="page active">
  <div class="balbox"><div class="bal">৳ {{c.balance}}</div><div>Ads: 0/100</div></div>
  <div class="notice"><div><b>Official Notice</b><br><small>Watch Ads Daily - Earn Upto ৳500</small></div><div class="live"><div class="dot"></div>LIVE</div></div>
  <div class="banner"></div>
  <div class="custom"><b>🔥 {{c.custom_title}}</b><br><small>{{c.custom_text}}</small><br>
  <button class="btn btn-white" onclick="show_{{c.zone}}('pop'); window.open('{{c.direct}}','_blank');">{{c.custom_btn}}</button></div>
  <div class="adbox"><img src="{{c.ad_box_banner}}"><div class="adbox-inner"><b>{{c.ad_box_title}}</b><br><small>{{c.ad_box_text}}</small><br><button class="btn btn-orange" onclick="show_{{c.zone}}().then(()=>window.open('{{c.ad_box_link}}','_blank'))">{{c.ad_box_btn}}</button></div></div>
</div>

<div id="tasks" class="page"><div style="padding:16px"><h2>Tasks</h2></div>
{% for t in c.tasks %}
<div class="taskbox"><span>⭐ {{t.title}}</span><b>৳{{t.reward}}</b></div>
<div style="margin:0 12px 12px 12px"><button class="btn btn-red" onclick="show_{{c.zone}}().then(()=>window.open('{{t.link}}','_blank'))">▶ Join & Get {{t.reward}} Tk</button></div>
{% endfor %}</div>

<div id="refer" class="page"><div style="padding:20px"><h2>Refer</h2></div></div>
<div id="wallet" class="page"><div style="padding:20px"><h2>Wallet ৳{{c.balance}}</h2></div></div>
<div id="profile" class="page"><div class="profile-card"><img src="{{c.profile_photo}}"><h2>{{c.profile_name}}</h2><p>{{c.app_name}}</p></div></div>

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
}
// কোনো অটো এড নেই - শুধু বাটনে ক্লিক করলে এড আসবে
</script>
</body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML, c=load())
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "No"
    c=load()
    th="".join([f"<div style='background:#fff;padding:10px;margin:5px;border-radius:8px'><b>{i+1}</b> Title:<input name=title{i} value='{t['title']}' style='width:95%'><br>Reward:<input name=reward{i} value='{t['reward']}'> Link:<input name=link{i} value='{t['link']}' style='width:95%'></div>" for i,t in enumerate(c['tasks'])])
    return f'''
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <div style="padding:10px;background:#f2f2f2;font-family:sans-serif">
    <h2>📱 Redmi Phone Admin</h2>
    <form method=POST action=/admin/save?id=8807178385>
    App Name:<br><input name=app_name value="{c['app_name']}" style="width:100%;padding:12px"><br><br>
    Balance:<br><input name=balance value="{c['balance']}" style="width:100%;padding:12px"><br><br>
    তোমার ছবি URL (কোনার পিক):<br><input name=profile_photo value="{c['profile_photo']}" style="width:100%;padding:12px"><br>
    <img src="{c['profile_photo']}" style="width:60px;height:60px;border-radius:50%;margin-top:5px"><br><br>
    নাম:<br><input name=profile_name value="{c['profile_name']}" style="width:100%;padding:12px"><br><br>
    Banner URL:<br><input name=banner value="{c['banner']}" style="width:100%;padding:12px"><br><br>
    Direct Link:<br><input name=direct value="{c['direct']}" style="width:100%;padding:12px"><br><br>
    <h3>অফার বক্স</h3>
    Title:<input name=custom_title value="{c['custom_title']}" style="width:100%;padding:12px"><br>
    Text:<textarea name=custom_text style="width:100%;padding:12px">{c['custom_text']}</textarea><br><br>
    <h3>তোমার বিজ্ঞাপনের বক্স</h3>
    Image:<input name=ad_box_banner value="{c['ad_box_banner']}" style="width:100%;padding:12px"><br>
    Title:<input name=ad_box_title value="{c['ad_box_title']}" style="width:100%;padding:12px"><br>
    Text:<textarea name=ad_box_text style="width:100%;padding:12px">{c['ad_box_text']}</textarea><br>
    Btn:<input name=ad_box_btn value="{c['ad_box_btn']}" style="width:100%;padding:12px"><br>
    Link:<input name=ad_box_link value="{c['ad_box_link']}" style="width:100%;padding:12px"><br><br>
    <h3>20 টা Task</h3>{th}
    <button style="width:100%;padding:18px;background:#00ff88;font-weight:900;font-size:20px;border:none;border-radius:12px;margin-top:20px">💾 SAVE - ফোন থেকে সেভ</button>
    </form></div>'''
@app.route('/admin/save', methods=['POST'])
def save():
    c=load()
    for k in ['app_name','banner','profile_name','profile_photo','custom_title','custom_text','custom_btn','direct','zone','ad_box_title','ad_box_text','ad_box_btn','ad_box_link','ad_box_banner']:
        if request.form.get(k): c[k]=request.form.get(k)
    if request.form.get('balance'): c['balance']=int(request.form.get('balance'))
    nt=[]
    for i in range(20):
        if request.form.get(f'title{i}'): nt.append({"title":request.form.get(f'title{i}'),"reward":int(request.form.get(f'reward{i}') or 10),"link":request.form.get(f'link{i}')})
    if nt: c['tasks']=nt
    with open(FILE,'w',encoding='utf-8') as f: json.dump(c,f,ensure_ascii=False,indent=2)
    return f"✅ Saved! <a href=/>Home</a> - <a href=/admin?id=8807178385>Admin Back</a><br><br>তোমার পিক এখন কোনায় দেখাবে: <img src={c['profile_photo']} style='width:80px;border-radius:50%'>"
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
