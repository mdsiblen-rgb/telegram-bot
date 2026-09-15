import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={ "app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস!","ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন!","spon_btn":"🚀 Explore Now - Click Here","spon_link":"https://google.com","ref_title":"👥 Refer & Earn","ref_desc":"প্রতি রেফারে ৳৮০","sup_title":"💎 Support","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"","sup_email":"","sup_notice":"⚠️ রাত ১০টার পর Withdraw বন্ধ","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]}
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[{"id":1,"title":"Join Telegram","reward":20,"link":"https://t.me/","icon":"📢"}]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    db=json.load(open(DB,'r',encoding='utf-8'))
    for k,v in d.items():
        if k not in db["settings"]: db["settings"][k]=v
    return db

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
def get_user(db,uid,ref=None):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c_today":0,"p_today":0,"ad_date":"","diamonds":2000}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["bal"]+=db["settings"]["ref"]
    return db["users"][uid],False

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')),j.get('ref'));save_db(db)
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"]})

@app.route('/api/ads', methods=['POST'])
def handle_ads():
    db=load_db();data=request.json;uid=str(data.get('id') or '');ad_type=str(data.get('type') or 'c')
    user,_=get_user(db,uid);s=db["settings"];today=time.strftime("%Y-%m-%d")
    if user.get("ad_date")!=today: user["ad_date"]=today;user["c_today"]=0;user["p_today"]=0
    if ad_type=='c':
        if user.get("c_today",0)>=int(s.get("clim",50)): return jsonify({"msg":"Ajker Company limit sesh"})
        reward=float(s.get("ad",0.2));user["c_today"]+=1
    else:
        if user.get("p_today",0)>=int(s.get("plim",30)): return jsonify({"msg":"Ajker Popup limit sesh"})
        reward=float(s.get("pop",0.3));user["p_today"]+=1
    user["bal"]+=reward;user["total"]+=reward;save_db(db)
    return jsonify({"msg":f"{reward} Taka Added","bal":user["bal"]})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        act=request.form.get('act')
        if act=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":"📢"})
        elif act=='del_task':
            db["tasks"]=[t for t in db["tasks"] if str(t["id"])!=str(request.form.get('id'))]
        elif act=='save_all':
            for k in db["settings"].keys():
                if request.form.get(k) not in (None,''):
                    db["settings"][k]=request.form.get(k)
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='display:flex;justify-content:space-between;padding:8px;background:#0B0E1C;margin:4px;border-radius:8px'>{t['title']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return render_template_string(f"""
    <style>body{{background:#0B0E1C;color:#fff;padding:16px;max-width:700px;margin:auto;font-family:system-ui}}.card{{background:#151A2D;padding:16px;border-radius:12px;margin-bottom:12px}}input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #333;margin-top:6px}}button{{background:#8b5cf6;color:#fff;padding:10px;border:none;border-radius:8px}}</style>
    <div class='card'><h3>✅ Admin Fixed - ID Safe</h3></div>
    <form method='post' class='card'><input type='hidden' name='act' value='save_all'>
    App Name: <input name='app_name' value="{s['app_name']}">
    Bonus: <input name='bonus' value="{s['bonus']}">
    Company Ad: <input name='ad' value="{s['ad']}">
    Popup Ad: <input name='pop' value="{s['pop']}">
    Company ID: <input name='company_ad_id' value="{s['company_ad_id']}">
    Popup ID: <input name='popup_ad_id' value="{s['popup_ad_id']}">
    Direct: <input name='direct_link' value="{s['direct_link']}">
    Sponsor Title: <input name='spon_title' value="{s['spon_title']}">
    Sponsor Desc: <textarea name='spon_desc'>{s['spon_desc']}</textarea>
    Sponsor Btn: <input name='spon_btn' value="{s['spon_btn']}">
    Sponsor Link: <input name='spon_link' value="{s['spon_link']}">
    <br><br><button type='submit'>SAVE ALL</button></form>
    <div class='card'>{rows}<form method='post'><input type='hidden' name='act' value='add_task'>Title<input name='title'>Reward<input name='reward'>Link<input name='link'><button>Add</button></form></div>
    """)

@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
    <!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <script src='https://telegram.org/js/telegram-web-app.js'></script>
    <script src='//libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
    <style>body{font-family:system-ui;background:#f5f5f5;padding:12px}.card{background:#fff;padding:14px;border-radius:12px;margin-bottom:10px;box-shadow:0 2px 8px #0001}button{width:100%;padding:12px;border-radius:10px;background:#8b5cf6;color:#fff;border:none;margin-top:8px;font-weight:600}</style>
    </head><body>
    <div class='card'><h2 style='margin:0'>{{ s["app_name2"] }}</h2><p>Balance: <b id='bal'>Loading...</b> Tk</p>
    <button onclick='watchAd("c")'>Watch Company AD - {{ s["ad"] }} Tk</button>
    <button onclick='watchAd("p")'>Watch Popup AD - {{ s["pop"] }} Tk</button>
    <button onclick='openSponsor()' style='background:#111'>{{ s["spon_btn"] }}</button>
    <button onclick='openDirect()' style='background:#f59e0b'>Direct Link</button>
    </div>
    <div class='card'><h3 style='margin:0'>{{ s["spon_title"] }}</h3><p>{{ s["spon_desc"] }}</p></div>
    <script>
    const S = {{ s|tojson }};
    function openSponsor(){ Telegram.WebApp.openLink(S.spon_link); }
    function openDirect(){ Telegram.WebApp.openLink(S.direct_link); }
    function watchAd(type){
      let zone = type=='c'? `show_${S.company_ad_id}` : `show_${S.popup_ad_id}`;
      if(typeof window[zone]==='function'){
        window[zone]().then(()=>{
          fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id: (Telegram.WebApp.initDataUnsafe.user||{id:'123'}).id, type: type})}).then(r=>r.json()).then(d=>{ if(d.bal) document.getElementById('bal').innerText=d.bal; alert(d.msg); });
        });
      } else { alert('Ad Loading... Try again'); }
    }
    fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id: (Telegram.WebApp.initDataUnsafe.user||{id:'123'}).id})}).then(r=>r.json()).then(d=>{ document.getElementById('bal').innerText=d.user.bal; });
    </script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
