import os,json,time
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={ "app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅","primary":"#8b5cf6","secondary":"#f59e0b","bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস পেয়েছেন! এখন ইনকাম শুরু করুন!","ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,"company_ad_id":"11764581","popup_ad_id":"11798857","direct_link":"https://omg10.com/4/11760259","spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন এবং বোনাস নিন। বড় বিজ্ঞাপন বক্সে আপনার অফার লিখুন!","spon_btn":"🚀 Explore Now - Click Here","spon_link":"https://google.com","ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• বন্ধুর প্রতি Ads থেকে ১৫% কমিশন\n• Min Withdraw ৳৩০০\n• Instant Payment","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০ বোনাস!","sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com","sup_notice":"⚠️ গুরুত্বপূর্ণ নোটিশ:\n• রাত ১০টার পর Withdraw বন্ধ\n• সকাল ৯টায় চালু\n• ভুয়া রেফার ব্যান\n• VPN ব্যবহার করবেন না","sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে bKash/Nagad এ পাবেন।","sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই ৳৮০ সাথে সাথে।","sup_faq3_q":"📢 Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN ব্যবহার করবেন না, ১০ সেকেন্ড দেখুন।","sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান\n3. VPN নিষেধ\n4. দিনে ৫০টা Company, ৩০টা Popup","pro_title":"👤 My Profile","pro_notice":"💎 Diamond Member - Level বাড়ান, বেশি ইনকাম করুন!","pro_ver":"Version 3.1 - Monetag 2 Ads Active","levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000] }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[ {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"}, {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"}, {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"} ]}
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
    return db["users"][uid], is_new

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
        if user.get("c_today",0)>=int(s.get("clim",50)): return jsonify({"msg":"Ajker Company limit sesh"})
        reward=float(s.get("ad",0.2));user["c_today"]+=1
    else:
        if user.get("p_today",0)>=int(s.get("plim",30)): return jsonify({"msg":"Ajker Popup limit sesh"})
        reward=float(s.get("pop",0.3));user["p_today"]+=1
    user["bal"]=float(user.get("bal",0))+reward;user["total"]=float(user.get("total",0))+reward;user["diamonds"]=int(user.get("diamonds",0))+int(reward*100);save_db(db)
    return jsonify({"msg": f"{reward} Taka Added","bal":user["bal"],"diamonds":user["diamonds"]})

@app.route('/admin',methods=['GET','POST'])
def admin():
    db=load_db()
    if request.method=='POST':
        act=request.form.get('act')
        if act=='add_task':
            nid=max([t["id"] for t in db["tasks"]],default=0)+1
            db["tasks"].append({"id":nid,"title":request.form.get('title'),"reward":int(request.form.get('reward',20)),"link":request.form.get('link'),"icon":request.form.get('icon','🔗')})
        elif act=='del_task':
            db["tasks"]=[t for t in db["tasks"] if str(t["id"])!=str(request.form.get('id'))]
        elif act=='save_all':
            for k in list(db["settings"].keys()):
                if request.form.get(k) not in (None,''):
                    v=request.form.get(k)
                    if k in ["ad","pop","bonus","ref","diamond_rate"]:
                        try: db["settings"][k]=float(v)
                        except: pass
                    elif k in ["clim","plim","min","ad_time"]:
                        try: db["settings"][k]=int(float(v))
                        except: pass
                    else: db["settings"][k]=v
        save_db(db)
    s=db["settings"]
    rows="".join([f"<div style='display:flex;justify-content:space-between;background:#0B0E1C;padding:8px;margin:4px;border-radius:8px'>{t['id']}. {t['icon']} {t['title']} ৳{t['reward']} <form method='post'><input type='hidden' name='act' value='del_task'><input type='hidden' name='id' value='{t['id']}'><button>Del</button></form></div>" for t in db["tasks"]])
    return render_template_string(f"""
    <style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui;max-width:700px;margin:auto}}.card{{background:#151A2D;padding:16px;border-radius:14px;margin-bottom:14px;border:1px solid #1e293b}}input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}button{{padding:8px 14px;border-radius:8px;background:#8b5cf6;color:#fff;border:none}}</style>
    <div class='card'><h3>✅ Admin - ID Safe Mode ON</h3><p>Company: {s.get('company_ad_id')} | Popup: {s.get('popup_ad_id')} | Direct: {s.get('direct_link')}</p></div>
    <form method='post' class='card'><input type='hidden' name='act' value='save_all'>
    <h3>🎨 Color + Money Control - সবকিছু কন্ট্রোল</h3>
    App Name: <input name='app_name' value="{s['app_name']}"> App Name2: <input name='app_name2' value="{s['app_name2']}">
    Per AD (Company): <input name='ad' value="{s['ad']}"> Per AD (Popup): <input name='pop' value="{s['pop']}">
    Bonus: <input name='bonus' value="{s['bonus']}"> Ref: <input name='ref' value="{s['ref']}"> Min WD: <input name='min' value="{s['min']}">
    Daily Company Limit: <input name='clim' value="{s['clim']}"> Daily Popup Limit: <input name='plim' value="{s['plim']}">
    <h3>📦 Ads ID Control</h3>
    Company AD ID: <input name='company_ad_id' value="{s['company_ad_id']}"> Popup AD ID: <input name='popup_ad_id' value="{s['popup_ad_id']}"> Direct Link: <input name='direct_link' value="{s['direct_link']}">
    <h3>🔥 Big Sponsored Box</h3>Title: <input name='spon_title' value="{s['spon_title']}"> Desc: <textarea name='spon_desc'>{s['spon_desc']}</textarea> Btn: <input name='spon_btn' value="{s['spon_btn']}"> Link: <input name='spon_link' value="{s['spon_link']}">
    <br><br><button type='submit'>💾 SAVE ALL</button></form>
    <div class='card'><h3>Tasks - এখন Delete কাজ করবে</h3>{rows}<form method='post'><input type='hidden' name='act' value='add_task'>Title <input name='title'> Reward <input name='reward'> Link <input name='link'> Icon <input name='icon' value='🔗'><button>Add</button></form></div>
    """)

@app.route('/')
def home():
    db=load_db();s=db["settings"]
    return render_template_string("""
    <!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <script src='https://telegram.org/js/telegram-web-app.js'></script>
    <script src='//libtl.com/sdk.js' data-zone='{{ s["company_ad_id"] }}' data-sdk='show_{{ s["company_ad_id"] }}'></script>
    <style>body{font-family:system-ui;background:#f0f2f5;margin:0;padding:12px}.card{background:#fff;padding:14px;border-radius:14px;margin-bottom:12px;box-shadow:0 2px 10px #0001}button{width:100%;padding:13px;border-radius:10px;background:#8b5cf6;color:#fff;border:none;margin-top:8px;font-weight:700}</style>
    </head><body>
    <div class='card'><h2 style='margin:0'>{{ s["app_name2"] }}</h2><p>Balance: <b id='bal'>Loading...</b> Tk | Diamond: <b id='dia'>0</b></p>
    <button onclick='watchAd("c")'>Watch Company AD - {{ s["ad"] }} Tk</button>
    <button onclick='watchAd("p")'>Watch Popup AD - {{ s["pop"] }} Tk</button>
    <button onclick='openSponsor()' style='background:#111'>{{ s["spon_btn"] }}</button>
    <button onclick='openDirect()' style='background:#f59e0b'>Direct Link</button>
    </div>
    <div class='card'><h3 style='margin:0 0 6px'>{{ s["spon_title"] }}</h3><p style='margin:0'>{{ s["spon_desc"] }}</p></div>
    <div class='card'><h3>{{ s["ref_title"] }}</h3><p>{{ s["ref_desc"] }}</p><p style='font-size:12px;white-space:pre-line'>{{ s["ref_banner"] }}</p></div>
    <div class='card'><h3>{{ s["sup_title"] }}</h3><p>{{ s["sup_desc"] }}</p><button onclick='Telegram.WebApp.openLink("{{ s['sup_tg'] }}")'>Telegram</button></div>
    <script>
    const S = {{ s|tojson }};
    function openSponsor(){ Telegram.WebApp.openLink(S.spon_link); }
    function openDirect(){ Telegram.WebApp.openLink(S.direct_link); }
    function watchAd(type){
      let zone = type=='c'? `show_${S.company_ad_id}` : `show_${S.popup_ad_id}`;
      if(typeof window[zone]==='function'){
        window[zone]().then(()=>{
          fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id: (Telegram.WebApp.initDataUnsafe.user||{id:'12345'}).id, type: type})}).then(r=>r.json()).then(d=>{ if(d.bal!==undefined){document.getElementById('bal').innerText=d.bal; document.getElementById('dia').innerText=d.diamonds||0;} alert(d.msg); });
        });
      } else { alert('Ad not ready - ID Safe Mode'); }
    }
    fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id: (Telegram.WebApp.initDataUnsafe.user||{id:'12345'}).id})}).then(r=>r.json()).then(d=>{ document.getElementById('bal').innerText=d.user.bal; document.getElementById('dia').innerText=d.user.diamonds; });
    </script></body></html>
    """, s=s)

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
