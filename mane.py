from flask import Flask, request, jsonify, render_template_string
import json, os

app = Flask(__name__)
CONFIG_FILE = "config.json"

DEFAULT = {
 "app_name": "প্রতিদিনের কাজ BD",
 "logo": "",
 "balance": 60,
 "ads_count": "0/100",
 "notice_title": "Official Notice",
 "notice_text": "Watch Ads Daily - Earn Upto ৳500",
 # === তোমার কাস্টম বক্স - এডমিন থেকে চেঞ্জ হবে ===
 "custom_title": "🔥 আজকের ধামাকা অফার",
 "custom_text": "আজ 50 টা Ads দেখলেই 100 TK বোনাস পাবেন! অফার সীমিত",
 "custom_btn": "Join Now",
 "custom_link": "https://t.me/ProtidinerKajBD",
 "ad_zone": "11764581"
}

def load_cfg():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return DEFAULT

HTML = """
<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src='//libtl.com/sdk.js' data-zone='{{cfg.ad_zone}}' data-sdk='show_{{cfg.ad_zone}}'></script>
<script> show_{{cfg.ad_zone}}({type:'inApp', inAppSettings:{frequency:2,capping:0.1,interval:30,timeout:5,everyPage:false}}); </script>
<style>
body{background:#0a1931;color:white;font-family:sans-serif;margin:0;padding-bottom:80px}
.top{background:#1a2d5a;padding:20px;border-radius:0 0 25px 25px}
.bal{color:#00ff88;font-size:48px;font-weight:bold}
.box{margin:15px;background:#132a54;border:2px solid #00ff88;border-radius:15px;padding:15px}
.notice{display:flex;justify-content:space-between;align-items:center}
.live{background:#00ff88;color:black;padding:8px 20px;border-radius:20px;font-weight:bold}
.banner{margin:15px;border-radius:20px;overflow:hidden;height:180px;background:url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4') center/cover}
.custom{background:linear-gradient(135deg,#FF9500,#FF5E00);margin:15px;padding:15px;border-radius:15px;color:white}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:bold;font-size:16px;margin-top:10px}
.blue{background:#00aaff;color:white} .red{background:#ff2a2a;color:white}
.task{background:#132a54;margin:12px;padding:15px;border-radius:15px;display:flex;justify-content:space-between;align-items:center}
.nav{position:fixed;bottom:0;width:100%;background:#0a1931;display:flex;justify-content:space-around;padding:10px 0;border-top:1px solid #333}
.nav div{text-align:center;font-size:12px}
.active{color:#00ff88}
</style>
</head>
<body>

<div class="top">
<div class="bal">৳ {{cfg.balance}}</div>
<div>Ads: {{cfg.ads_count}}</div>
</div>

<div class="box">
<div class="notice">
<div><b>{{cfg.notice_title}}</b><br><small>{{cfg.notice_text}}</small></div>
<div class="live">● LIVE</div>
</div>
</div>

<div class="banner"></div>

<!-- === তোমার নতুন কাস্টম বক্স - এটাই ১ নম্বরে থাকবে === -->
<div class="custom">
<b>{{cfg.custom_title}}</b><br>
<small>{{cfg.custom_text}}</small><br>
<button class="btn" style="background:white;color:#FF5E00" onclick="window.open('{{cfg.custom_link}}','_blank'); show_{{cfg.ad_zone}}('pop').then(()=>{});">{{cfg.custom_btn}}</button>
</div>

<!-- ১ম পেজ - Home -->
<div id="home">
<div class="task" style="flex-direction:column;align-items:stretch">
<b>🎬 স্পেশাল অফার - বোনাস Ads</b>
<button class="btn blue" onclick="show_{{cfg.ad_zone}}().then(()=>{alert('৳2 পেয়েছো!');})">ADS দেখুন - ৳2 বোনাস</button>
</div>
</div>

<!-- ২য় পেজ - Tasks -->
<div id="tasks">
<div class="task"><div><b>⭐ YouTube Subscribe</b></div><div>৳25</div></div>
<div class="task" style="flex-direction:column"><button class="btn red">Join & Get 25 Tk</button></div>
<div class="task"><div><b>⭐ Telegram Join</b></div><div>৳10</div></div>
<div class="task" style="flex-direction:column"><button class="btn blue" onclick="window.open('https://t.me/ProtidinerKajBD','_blank')">Join Now</button></div>
</div>

<div class="nav">
<div class="active">🏠<br>Home</div>
<div style="color:#00ff88">✅<br>Tasks</div>
<div>👥<br>Refer</div>
<div>💰<br>Wallet</div>
<div>👤<br>Profile</div>
</div>

</body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, cfg=load_cfg())

@app.route('/admin')
def admin():
    if request.args.get('id') != '8807178385': return "No Access"
    cfg=load_cfg()
    return f'''
    <h2>Admin Panel - {cfg['app_name']}</h2>
    <form method=POST action=/admin/save?id=8807178385>
    App Name: <input name=app_name value="{cfg['app_name']}"><br><br>
    Custom Box Title: <input name=custom_title value="{cfg['custom_title']}" style="width:300px"><br><br>
    Custom Text: <textarea name=custom_text style="width:300px">{cfg['custom_text']}</textarea><br><br>
    Button Text: <input name=custom_btn value="{cfg['custom_btn']}"><br><br>
    Link: <input name=custom_link value="{cfg['custom_link']}" style="width:300px"><br><br>
    <button type=submit>Save</button>
    </form>
    '''

@app.route('/admin/save', methods=['POST'])
def save():
    cfg=load_cfg()
    cfg['app_name']=request.form.get('app_name')
    cfg['custom_title']=request.form.get('custom_title')
    cfg['custom_text']=request.form.get('custom_text')
    cfg['custom_btn']=request.form.get('custom_btn')
    cfg['custom_link']=request.form.get('custom_link')
    with open(CONFIG_FILE,'w',encoding='utf-8') as f: json.dump(cfg,f,ensure_ascii=False,indent=2)
    return "Saved! <a href=/>Go Home</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
