import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'
def default_data(): return {"users":{},"withdraws":[],"settings":{"app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","zone":"3490663","bonus":1120,"ad_reward":2,"popup_reward":3,"company_limit":30,"popup_limit":20,"min_with":500,"tutorial_video":"https://youtube.com/","support_link":"https://t.me/"},"tasks":[{"id":1,"title":"Facebook Page Like","desc":"পেজে লাইক দিন","reward":20,"icon":"👍"},{"id":2,"title":"Refer Friend","desc":"১ জন = ৳50","reward":50,"icon":"👥"},{"id":3,"title":"Daily Check-in","desc":"প্রতিদিন একবার","reward":15,"icon":"✅"}]}
def load_db():
    if not os.path.exists(DB): d=default_data(); open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)); return d
    try: return json.load(open(DB,'r',encoding='utf-8'))
    except: d=default_data(); open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)); return d
def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":"User 8385","profile_img":"","balance":1120,"ads_today":0,"popup_today":0,"total":0,"tasks_done":[],"last":today,"join_date":"2026-09-13"}
    u=db["users"][uid]
    if u.get("last")!=today: u["ads_today"]=0; u["popup_today"]=0; u["last"]=today
    return u
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/api/get')
def api_get():
    db=load_db(); u=get_user(db,request.args.get('id','8807178385')); save_db(db); return jsonify({"user":u,"settings":db["settings"],"tasks":db["tasks"]})
@app.route('/api/reward')
def api_reward():
    db=load_db(); u=get_user(db,request.args.get('id')); t=request.args.get('type','company'); s=db["settings"]
    if t=='company':
        if u["ads_today"]>=s["company_limit"]: return jsonify({"msg":"Limit শেষ"})
        u["ads_today"]+=1; u["balance"]+=s["ad_reward"]
    else:
        if u["popup_today"]>=s["popup_limit"]: return jsonify({"msg":"Limit শেষ"})
        u["popup_today"]+=1; u["balance"]+=s["popup_reward"]
    u["total"]+=1; save_db(db); return jsonify({"msg":"Done"})
@app.route('/api/user/update',methods=['POST'])
def upd():
    db=load_db(); j=request.json; u=get_user(db,j.get('id'));
    if 'name' in j: u["name"]=j['name']
    if 'profile_img' in j and j['profile_img']: u["profile_img"]=j['profile_img']
    save_db(db); return jsonify({"msg":"Saved"})

HTML="""<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script src="//libtl.com/sdk.js" data-zone="3490663" data-sdk="show_3490663"></script><style>body{background:#08081a;color:#fff;max-width:430px;margin:0 auto;padding-bottom:80px;font-family:system-ui}.top{padding:12px;background:#0a0a1e;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #222}.card{margin:10px;background:#12122a;border-radius:16px;padding:14px}.bal{background:linear-gradient(135deg,#1e40ff,#00d2ff);border-radius:16px;padding:20px;text-align:center;margin:10px}.btn{width:100%;padding:12px;border:none;border-radius:12px;font-weight:800;color:#fff;margin:5px 0}.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0a0a1e;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #222}.btm div{text-align:center;font-size:11px;color:#666}.btm div.on{color:#fff}</style></head><body><div class="top"><b>👑 Protidiner Kaj BD ✓</b><span>👤</span></div><div class="bal"><div>আপনার বর্তমান ব্যালেন্স</div><h1>৳<span id="b">1120</span></h1><div>Company <span id="c">0/30</span> | Popup <span id="p">0/20</span></div></div><div class="card"><button class="btn" style="background:#5b2cff" onclick="ad('company')">📺 COMPANY ADS</button><button class="btn" style="background:#00c950" onclick="ad('popup')">💰 POPUP ADS</button></div><div class="card"><h3>📋 Tasks</h3><div id="t"></div></div><div class="btm"><div class="on">🏠 Home</div><div>📋 Task</div><div>💰 Wallet</div><div>💬 Support</div><div>👤 Profile</div></div><script>let uid='8807178385';function load(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{document.getElementById('b').innerText=d.user.balance;document.getElementById('c').innerText=d.user.ads_today+'/30';document.getElementById('p').innerText=d.user.popup_today+'/20';let h='';d.tasks.forEach(x=>{h+=`<div style="display:flex;justify-content:space-between;padding:10px;background:#1a1a35;margin:6px 0;border-radius:10px"><span>${x.icon} ${x.title}</span><b>৳${x.reward}</b></div>`});document.getElementById('t').innerHTML=h;});}function ad(type){if(typeof show_3490663==='function'){show_3490663(type==='popup'?{type:'popup'}:undefined).then(()=>{fetch('/api/reward?id='+uid+'&type='+type).then(()=>load());});}else alert('Loading...');}load();</script></body></html>"""
if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
