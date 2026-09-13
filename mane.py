from flask import Flask, request, render_template_string
import json, os
app = Flask(__name__)
FILE="config.json"
CFG={
 "balance":60, "zone":"11764581", "direct":"https://omg10.com/4/11760259",
 "banner":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
 "custom_title":"🔥 আজকের ধামাকা অফার",
 "custom_text":"আজ 50 টা Ads দেখলেই 100 TK বোনাস পাবেন!",
 "custom_btn":"Join Now"
}
def load():
    if os.path.exists(FILE):
        with open(FILE,'r',encoding='utf-8') as f: return json.load(f)
    return CFG

HTML="""
<!DOCTYPE html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='{{c.zone}}' data-sdk='show_{{c.zone}}'></script>
<style>
body{margin:0;background:#06122e;color:#fff;font-family:sans-serif;padding-bottom:85px}
.header{background:#0e2252;padding:14px 16px;display:flex;align-items:center;gap:10px}
.tick{background:#00ff88;color:#000;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900}
.balbox{background:#0a1940;padding:18px 18px 22px;border-radius:0 0 28px 28px}
.bal{color:#00ff88;font-size:54px;font-weight:900}
.notice{margin:12px;background:#102a5e;border:2px solid #00ff88;border-radius:16px;padding:13px;display:flex;justify-content:space-between;align-items:center}
.live{background:#00ff88;color:#000;padding:7px 16px;border-radius:22px;font-weight:900;display:flex;align-items:center;gap:7px;box-shadow:0 0 15px #00ff88}
.dot{width:10px;height:10px;background:#000;border-radius:50%;animation:blink 0.8s infinite}
@keyframes blink{0%{opacity:1} 50%{opacity:0.1} 100%{opacity:1}}
.banner{margin:12px;height:210px;border-radius:20px;background:url('{{c.banner}}') center/cover}
.custom{background:linear-gradient(90deg,#ff8c00,#ff5e00);margin:12px;padding:16px;border-radius:18px}
.btn{width:100%;padding:17px;border:none;border-radius:16px;font-weight:900;font-size:18px;margin-top:12px}
.btn-bonus{background:linear-gradient(90deg,#00ff88,#00cc6a);color:#000}
.btn-blue{background:linear-gradient(90deg,#00aaff,#0066ff);color:#fff}
.btn-red{background:linear-gradient(90deg,#ff3b3b,#cc0000);color:#fff}
.btn-white{background:#fff;color:#ff5e00}
.page{display:none}.page.active{display:block}
.nav{position:fixed;bottom:0;width:100%;background:#06122e;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #1a3a7a}
.nav div{opacity:0.5;text-align:center;font-size:12px}.nav div.on{opacity:1;color:#00ff88}
</style>
</head><body>
<div class="header"><span>👑</span><b>Protidiner Kaj BD</b><span class="tick">✓</span></div>

<div id="home" class="page active">
  <div class="balbox"><div class="bal">৳ {{c.balance}}</div><div>Ads: 0/100</div></div>
  <div class="notice"><div><b>Official Notice</b><br><small>Watch Ads Daily - Earn Upto ৳500</small></div><div class="live"><div class="dot"></div>LIVE</div></div>
  <div class="banner"></div>
  <div class="custom"><b>{{c.custom_title}}</b><br><small>{{c.custom_text}}</small><br>
  <button class="btn btn-white" onclick="show_{{c.zone}}('pop'); window.open('{{c.direct}}','_blank');">{{c.custom_btn}}</button></div>
  <div style="margin:12px;background:#102a5e;padding:18px;border-radius:18px"><b>🎬 স্পেশাল অফার</b>
  <button class="btn btn-bonus" onclick="show_{{c.zone}}().then(()=>{window.open('{{c.direct}}','_blank'); alert('৳2 Added')})">▶ ADS দেখুন - ৳2 বোনাস</button></div>
</div>

<div id="tasks" class="page">
  <div style="padding:16px"><h2>Tasks</h2></div>
  <div style="margin:12px;background:#102a5e;padding:16px;border-radius:14px;display:flex;justify-content:space-between"><span>⭐ YouTube Subscribe</span><b>৳25</b></div>
  <div style="margin:12px"><button class="btn btn-red" onclick="show_{{c.zone}}().then(()=>{window.open('{{c.direct}}','_blank')})">▶ Join & Get 25 Tk</button></div>
  <div style="margin:12px;background:#102a5e;padding:16px;border-radius:14px;display:flex;justify-content:space-between"><span>⭐ Telegram Join</span><b>৳10</b></div>
  <div style="margin:12px"><button class="btn btn-blue" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">✈ Join Now</button></div>
</div>

<div class="nav">
  <div class="on" onclick="go('home',this)">🏠<br>Home</div>
  <div onclick="go('tasks',this)">✅<br>Tasks</div>
  <div>👥<br>Refer</div><div>💰<br>Wallet</div><div>👤<br>Profile</div>
</div>
<script>
function go(id,el){
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 document.getElementById(id).classList.add('active');
 document.querySelectorAll('.nav div').forEach(d=>d.classList.remove('on'));
 el.classList.add('on');
}
show_{{c.zone}}({type:'inApp', inAppSettings:{frequency:2,capping:0.1,interval:30}});
</script>
</body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML, c=load())
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "No"
    c=load(); return f'''<form method=POST action=/admin/save?id=8807178385>
    Banner:<br><input name=banner value="{c['banner']}" style="width:95%"><br><br>
    Title:<br><input name=custom_title value="{c['custom_title']}" style="width:95%"><br><br>
    Text:<br><textarea name=custom_text style="width:95%">{c['custom_text']}</textarea><br><br>
    DirectLink:<br><input name=direct value="{c['direct']}" style="width:95%"><br><br>
    <button>Save</button></form>'''
@app.route('/admin/save', methods=['POST'])
def save():
    c=load()
    for k in c:
        if request.form.get(k): c[k]=request.form.get(k)
    with open(FILE,'w',encoding='utf-8') as f: json.dump(c,f,ensure_ascii=False,indent=2)
    return "Saved <a href=/>Home</a>"
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
