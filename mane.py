import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={
        "app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅",
        "primary":"#8b5cf6","secondary":"#f59e0b",
        "bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস পেয়েছেন!",
        "ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,
        "company_ad_id":"11764581","popup_ad_id":"11798857",
        "direct_link":"https://omg10.com/4/11760259",
        "spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন!","spon_btn":"🚀 Explore Now","spon_link":"https://google.com",
        "ref_title":"👥 Refer & Earn","ref_desc":"প্রতি রেফারে ৳৮০","ref_rules":"• বন্ধু জয়েন করলে ৳৮০","ref_banner":"🎉 Refer Contest Top 10",
        "sup_title":"💎 Support","sup_desc":"২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com",
        "sup_notice":"⚠️ রাত ১০টার পর Withdraw বন্ধ","sup_faq1_q":"Withdraw কতক্ষণে?","sup_faq1_a":"৫-৩০ মিনিট","sup_faq2_q":"Refer টাকা?","sup_faq2_a":"Instant","sup_faq3_q":"Ads আসে না?","sup_faq3_a":"VPN বন্ধ করুন",
        "sup_rules":"1. এক ফোনে এক আইডি","pro_title":"👤 My Profile","pro_notice":"Diamond Member","pro_ver":"Version 3.1",
        "levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]
    }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[
            {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
            {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},
            {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}]}
        open(DB,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=2));return data
    db=json.load(open(DB,'r',encoding='utf-8'))
    for k,v in d.items():
        if k not in db["settings"]: db["settings"][k]=v
    return db

def save_db(db): open(DB,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,indent=2))
def get_level(total, levels):
    lvl=1
    for i,th in enumerate(levels):
        if total>=th: lvl=i+1
    return lvl

def get_user(db,uid,ref=None):
    uid=str(uid);is_new=False
    if uid not in db["users"]:
        is_new=True
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"ads":0,"diamonds":db["settings"]["bonus"]*db["settings"]["diamond_rate"],"task_timer":{},"ad_date":"","c_today":0,"p_today":0}
        if ref and ref in db["users"] and ref!=uid:
            db["users"][ref]["refl"].append(uid);db["users"][ref]["bal"]+=db["settings"]["ref"];db["users"][ref]["total"]+=db["settings"]["ref"]
    return db["users"][uid],is_new

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u,is_new=get_user(db,str(j.get('id')),j.get('ref'));save_db(db)
    wds=[x for x in db["wds"] if x["uid"]==u["id"]]
    lvl=get_level(u["total"], db["settings"]["levels"])
    nxt=db["settings"]["levels"][lvl] if lvl < len(db["settings"]["levels"]) else db["settings"]["levels"][-1]
    prog=int((u["total"]/nxt*100)) if nxt>0 else 0
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds,"level":lvl,"next":nxt,"prog":prog,"is_new":is_new})

@app.route('/api/ads', methods=['POST'])
def handle_ads():
    db=load_db();data=request.json;uid=str(data.get('id') or '');ad_type=str(data.get('type') or 'c')
    user,_=get_user(db,uid);s=db["settings"];today=time.strftime("%Y-%m-%d")
    if user.get("ad_date")!=today: user["ad_date"]=today;user["c_today"]=0;user["p_today"]=0
    if ad_type=='c':
        if user.get("c_today",0)>=s.get("clim",50): return jsonify({"msg":"Ajker Company limit sesh"})
        reward=float(s.get("ad",0.2));user["c_today"]+=1
    else:
        if user.get("p_today",0)>=s.get("plim",30): return jsonify({"msg":"Ajker Popup limit sesh"})
        reward=float(s.get("pop",0.3));user["p_today"]+=1
    user["bal"]+=reward;user["total"]+=reward;user["diamonds"]+=int(reward*100);save_db(db)
    return jsonify({"msg":f"{reward} Taka Added","bal":user["bal"]})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        act=request.form.get('act')
        if act=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif act=='del_task':
            db["tasks"]=[t for t in db["tasks"] if t["id"]!=int(request.form.get('id'))]
        elif act=='save_all':
            for k in list(db["settings"].keys()):
                if request.form.get(k) not in (None,''):
                    v=request.form.get(k)
                    if k in ["ad","pop","bonus","ref","diamond_rate","min"]:
                        try: db["settings"][k]=float(v)
                        except: db["settings"][k]=v
                    elif k in ["clim","plim","ad_time"]:
                        try: db["settings"][k]=int(float(v))
                        except: pass
                    else: db["settings"][k]=v
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='display:flex;justify-content:space-between;background:#0B0E1C;padding:8px;margin:4px;border-radius:8px'>{t['id']}. {t['icon']} {t['title']} ৳{t['reward']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return render_template_string(f"""
    <style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui;max-width:700px;margin:auto}}.card{{background:#151A2D;padding:16px;border-radius:14px;margin-bottom:14px;border:1px solid #1e293b}}input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}button{{padding:8px 14px;border-radius:8px;background:#8b5cf6;color:#fff;border:none}}</style>
    <div class='card'><h2>✅ Admin - ID Safe Mode ON</h2>Company: {s.get('company_ad_id')} | Popup: {s.get('popup_ad_id')}</div>
    <form method='post' class='card'><input type='hidden' name='act' value='save_all'>
    <h3>🎨 App + Money Control - সবকিছু কন্ট্রোল</h3>
    App Name: <input name='app_name' value="{s['app_name']}"> App Name2: <input name='app_name2' value="{s['app_name2']}">
    Bonus: <input name='bonus' value="{s['bonus']}"> Welcome Bonus: <input name='welcome_bonus' value="{s.get('welcome_bonus',20)}">
    Per Ad: <input name='ad' value="{s['ad']}"> Per Pop: <input name='pop' value="{s['pop']}">
    Daily Ad Limit: <input name='clim' value="{s['clim']}"> Daily Pop Limit: <input name='plim' value="{s['plim']}">
    Min Withdraw: <input name='min' value="{s['min']}"> Ref Bonus: <input name='ref' value="{s['ref']}">
    Ad Time: <input name='ad_time' value="{s['ad_time']}">
    <h3>📦 Ads Control</h3>
    Company AD ID: <input name='company_ad_id' value="{s['company_ad_id']}">
    Popup AD ID: <input name='popup_ad_id' value="{s['popup_ad_id']}">
    Direct Link (omg10): <input name='direct_link' value="{s['direct_link']}">
    <h3>🔥 Sponsor Box - বড় বক্স</h3>
    Title: <input name='spon_title' value="{s['spon_title']}">
    Desc: <textarea name='spon_desc'>{s['spon_desc']}</textarea>
    Btn: <input name='spon_btn' value="{s['spon_btn']}"> Link: <input name='spon_link' value="{s['spon_link']}">
    <h3>👥 Refer Box</h3>Title: <input name='ref_title' value="{s['ref_title']}"> Desc: <input name='ref_desc' value="{s['ref_desc']}">
    <h3>💎 Support Box</h3>Title: <input name='sup_title' value="{s['sup_title']}"> TG: <input name='sup_tg' value="{s['sup_tg']}"> WA: <input name='sup_wa' value="{s['sup_wa']}">
    <br><br><button type='submit'>💾 SAVE ALL - সব সেভ করুন</button>
    </form>
    <div class='card'><h3>Tasks</h3>{rows}
    <form method='post'><input type='hidden' name='act' value='add_task'>Icon: <input name='icon'> Title: <input name='title'> Reward: <input name='reward'> Link: <input name='link'><button>Add Task</button></form></div>
    <div class='card'><p>✅ ID Ban Fix: এখন সব লিংক Telegram.WebApp.openLink দিয়ে বাইরে খুলবে, তাই বাইরে থেকে দেখলেও ID ব্যান হবে না।</p></div>
    """)

@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
    <!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <script src='https://telegram.org/js/telegram-web-app.js'></script>
    <script src='//libtl.com/sdk.js' data-zone='{{s.company_ad_id}}' data-sdk='show_{{s.company_ad_id}}'></script>
    <style>body{font-family:system-ui;background:#f5f5f5;padding:12px}.card{background:#fff;padding:14px;border-radius:12px;margin-bottom:10px}button{width:100%;padding:12px;border-radius:8px;background:#8b5cf6;color:#fff;border:none;margin-top:6px}</style>
    </head><body>
    <div class='card'><h2>{{s.app_name2}}</h2><p id='bal'>Loading...</p>
    <button onclick='watchAd("c")'>Watch Company AD - {{s.ad}} Tk</button>
    <button onclick='watchAd("p")'>Watch Popup AD - {{s.pop}} Tk</button>
    <button onclick='openSponsor()'>{{s.spon_btn}}</button>
    </div>
    <div class='card'><h3>{{s.spon_title}}</h3><p>{{s.spon_desc}}</p></div>
    <script>
    const S = {{s|tojson}};
    function openSponsor(){ Telegram.WebApp.openLink(S.spon_link); }
    function openDirect(){ Telegram.WebApp.openLink(S.direct_link); }
    function watchAd(type){
      let zone = type=='c'? 'show_{{s.company_ad_id}}' : 'show_{{s.popup_ad_id}}';
      if(typeof window[zone]==='function'){
        window[zone]().then(()=>{
          fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id: Telegram.WebApp.initDataUnsafe.user.id, type: type})}).then(r=>r.json()).then(d=>{ document.getElementById('bal').innerText=d.bal; alert(d.msg); });
        });
      } else { alert('Ad not ready - No Ban Risk'); }
    }
    fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id: Telegram.WebApp.initDataUnsafe.user.id})}).then(r=>r.json()).then(d=>{ document.getElementById('bal').innerText=d.user.bal; });
    </script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
