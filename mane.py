import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
    d={
        "app_name":"👑 প্রতিদিনের কাজ বিডি","app_name2":"Daily Work BD ✅",
"primary":"#8b5cf6","secondary":"#f59e0b",

        "bonus":20,"welcome_title":"🎉 স্বাগতম!","welcome_msg":"৳20 বোনাস পেয়েছেন! এখন ইনকাম শুরু করুন!",
        "ad":0.20,"pop":0.30,"clim":50,"plim":30,"min":500,"ref":80,"ad_time":10,"diamond_rate":100,
        "company_ad_id":"11764581","popup_ad_id":"11798857",
        "direct_link":"https://omg10.com/4/11760259",
        "spon_title":"🔥 আজকের সেরা অফার - BIG AD!","spon_desc":"প্রতিদিন ৫০০ টাকা পর্যন্ত ইনকাম করুন! এখনি ক্লিক করুন এবং বোনাস নিন। বড় বিজ্ঞাপন বক্সে আপনার অফার লিখুন!","spon_btn":"🚀 Explore Now - Click Here","spon_link":"https://google.com",
        "ref_title":"👥 Refer & Earn Unlimited","ref_desc":"প্রতি রেফারে ৳৮০ + ১৫% কমিশন!","ref_rules":"• বন্ধু জয়েন করলে ৳৮০\n• বন্ধুর প্রতি Ads থেকে ১৫% কমিশন\n• Min Withdraw ৳৩০০\n• Instant Payment","ref_banner":"🎉 Refer Contest - Top 10 পাবে ৳৫০০০ বোনাস!",
        "sup_title":"💎 Support Center","sup_desc":"যেকোনো সমস্যায় ২৪/৭ সাপোর্ট","sup_tg":"https://t.me/","sup_wa":"https://wa.me/","sup_fb":"https://facebook.com/","sup_email":"support@gmail.com",
        "sup_notice":"⚠️ গুরুত্বপূর্ণ নোটিশ:\n• রাত ১০টার পর Withdraw বন্ধ\n• সকাল ৯টায় চালু\n• ভুয়া রেফার ব্যান\n• VPN ব্যবহার করবেন না",
        "sup_faq1_q":"💸 Withdraw কতক্ষণে পাবো?","sup_faq1_a":"৫-৩০ মিনিটের মধ্যে bKash/Nagad এ পাবেন।","sup_faq2_q":"👥 Refer টাকা কখন পাবো?","sup_faq2_a":"বন্ধু জয়েন করলেই ৳৮০ সাথে সাথে।","sup_faq3_q":"📢 Ads দেখলে টাকা আসে না কেন?","sup_faq3_a":"VPN ব্যবহার করবেন না, ১০ সেকেন্ড দেখুন।",
        "sup_rules":"📜 নিয়ম:\n1. এক ফোনে এক আইডি\n2. ভুয়া রেফার ব্যান\n3. VPN নিষেধ\n4. দিনে ৫০টা Company, ৩০টা Popup",
        "pro_title":"👤 My Profile","pro_notice":"💎 Diamond Member - Level বাড়ান, বেশি ইনকাম করুন!","pro_ver":"Version 3.1 - Monetag 2 Ads Active",
        "levels":[0,500,2000,5000,10000,20000,35000,50000,80000,100000]
    }
    if not os.path.exists(DB):
        data={"users":{},"wds":[],"settings":d,"tasks":[
            {"id":1,"title":"Join Telegram Group","reward":20,"link":"https://t.me/","icon":"📢"},
            {"id":2,"title":"Company Website","reward":25,"link":"https://google.com","icon":"🏢"},
            {"id":3,"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","icon":"▶️"}
        ]}
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
    uid=str(uid)
    is_new=False
    if uid not in db["users"]:
        is_new=True
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","img":"","bal":db["settings"]["bonus"],"total":db["settings"]["bonus"],"c":0,"p":0,"done":[],"join":datetime.now().strftime("%Y-%m-%d"),"last":str(datetime.now().date()),"ref_by":ref,"refl":[],"ads":0,"diamonds":db["settings"]["bonus"]*db["settings"]["diamond_rate"]}
        if ref and ref in db["users"] and ref!=uid: db["users"][ref]["refl"].append(uid); db["users"][ref]["bal"]+=db["settings"]["ref"]; db["users"][ref]["total"]+=db["settings"]["ref"]
    return db["users"][uid], is_new

@app.route('/api/init',methods=['POST'])
def init_api():
    db=load_db();j=request.json;u,is_new=get_user(db,str(j.get('id')),j.get('ref'));save_db(db)
    wds=[x for x in db["wds"] if x["uid"]==u["id"]]
    lvl=get_level(u["total"], db["settings"]["levels"])
    nxt=db["settings"]["levels"][lvl] if lvl < len(db["settings"]["levels"]) else db["settings"]["levels"][-1]
    prog=int((u["total"]/nxt*100)) if nxt>0 else 0
    return jsonify({"user":u,"s":db["settings"],"tasks":db["tasks"],"wds":wds,"level":lvl,"next":nxt,"prog":prog,"is_new":is_new})
@app.route('/api/task',methods=['POST'])
def task():
    import time
    j=request.json
    db=load_db()
    uid=str(j.get('id'))
    u,_=get_user(db,uid)
    if not u:
        return jsonify({"msg":"User not found"}),404

    tid=str(j.get('tid') or '')
    ts=str(j.get('ts') or j.get('t') or tid)

    if "task_timer" not in u:
        u["task_timer"]={}
    # 1st call - timer start
    if ts not in u["task_timer"]:
        u["task_timer"][ts]=time.time()
        save_db(db)
        return jsonify({"msg":"Link e 30 sec thakun, tarpor abar Done chap din"})

    # 2nd call - check 30 sec
    left=30-(time.time()-u["task_timer"][ts])
    if left>0:
        return jsonify({"msg":f"Aro {int(left)} sec baki"})

    # --- GEAR SYSTEM FIXED ---
    if "done" not in u:
        u["done"]=[]
    if "diamonds" not in u:
        u["diamonds"]=0
    if "bal" not in u:
        u["bal"]=0
    if "total" not in u:
        u["total"]=0

    # Company = 20 Diamond, Popup = 30 Diamond
    if "company" in tid.lower() or tid=="1":
        reward=0.2
        d_reward=20
    else:
        reward=0.3
        d_reward=30

    u["bal"]+=reward
    u["total"]+=reward
    u["diamonds"]+=d_reward

    # Delete timer after done
    del u["task_timer"][ts]
    save_db(db)
    return jsonify({"msg":f"Done {reward} + Diamond {d_reward}","bal":u["bal"],"diamonds":u["diamonds"]})
@app.route('/api/ads', methods=['POST'])
def handle_ads():
    db = load_db()
    data = request.json
    uid = str(data.get('id') or data.get('uid') or '')
    ad_type = str(data.get('type') or 'c')

    user, idx = get_user(db, uid)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    s = db["settings"]
    today = time.strftime("%Y-%m-%d")
    
    if user.get("ad_date") != today:
        user["ad_date"] = today
        user["c_today"] = 0
        user["p_today"] = 0

    if ad_type == 'c':
        if user.get("c_today", 0) >= s.get("clim", 50):
            return jsonify({"msg": "Ajker Company limit sesh"})
        reward = float(s.get("ad", 0.2))
        user["c_today"] = user.get("c_today", 0) + 1
    else:
        if user.get("p_today", 0) >= s.get("plim", 30):
            return jsonify({"msg": "Ajker Popup limit sesh"})
        reward = float(s.get("pop", 0.3))
        user["p_today"] = user.get("p_today", 0) + 1

    user["bal"] = float(user.get("bal", 0)) + reward
    user["total"] = float(user.get("total", 0)) + reward
    user["diamonds"] = int(user.get("diamonds", 0)) + int(reward * 100)
    
    save_db(db)
    return jsonify({"msg": f"{reward} Taka Added", "bal": user["bal"], "diamonds": user["diamonds"]})
@app.route('/api/wd',methods=['POST'])
def wd():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')));s=db["settings"];amt=int(j.get('amt',0))
    if amt<s["min"]: return jsonify({"msg":f"Min {s['min']}"})
    if u["bal"]<amt: return jsonify({"msg":"Balance কম"})
    u["bal"]-=amt;db["wds"].append({"uid":u["id"],"name":u["name"],"amt":amt,"num":j.get('num'),"m":j.get('m'),"st":"Pending","time":datetime.now().strftime("%m-%d %H:%M")});save_db(db);return jsonify({"msg":"Withdraw সফল"})
@app.route('/api/update',methods=['POST'])
def up():
    db=load_db();j=request.json;u,_=get_user(db,str(j.get('id')))
    if 'name' in j: u["name"]=j['name'][:20]
    if 'img' in j and j['img']: u["img"]=j['img']
    save_db(db);return jsonify({"msg":"Saved"})

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
                    if k in ["ad","pop","bonus","ref","diamond_rate"]:
                        try: db["settings"][k]=float(v)
                        except: pass
                    elif k in ["clim","plim","min","ad_time","company_ad_id","popup_ad_id"]:
                        try: db["settings"][k]=int(float(v))
                        except: pass
                    else: db["settings"][k]=v
            if request.form.get('app_logo'): db["settings"]["app_logo"]=request.form.get('app_logo')
            save_db(db)
    s=db["settings"]
    rows="".join([f"<tr><td>{t['id']}</td><td>{t['icon']} {t['title']} ৳{t['reward']}</td><td><form method='post'><input type='hidden' name='act' value='del_task'>inputt type='hidden' name='id' value='{t['id']}'><button style='background:red;color:#fff;border:none;padding:4px 8px;border-radius:6px'>Del</button></form></td></tr>" for t in db["tasks"]])
    return render_template_string(f"""
    <html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#0B0E1C;color:#fff;padding:16px;font-family:system-ui;max-width:700px;margin:auto}}.card{{background:#151A2D;padding:16px;border-radius:14px;margin-bottom:14px;border:1px solid #1e293b}} input,textarea{{width:100%;padding:10px;border-radius:8px;background:#0B0E1C;color:#fff;border:1px solid #1e293b;margin-top:6px}}</style></head><body>
    <h2>✅ Admin - Monetag Active</h2>
    <div style='background:#22c55e20;border:1px solid #22c55e;padding:12px;border-radius:10px;margin-bottom:12px'><b style='color:#22c55e'>Company: {s.get('company_ad_id','')} | Popup: {s.get('popup_ad_id','')} | Direct: {s.get('importt_link','')}</b></div>
    <div class='card'><form method='post'><input type='hidden' name='act' value='save_all'>
    <b>📌 Top 2 Boxes - SHIBLI NOMAN</b><div style='display:flex;gap:8px'><input name='app_name' value='{s["app_name"]}'><input name='app_name2' value='{s["app_name2"]}'></div>
    <b>🎨 Color</b><div style='display:flex;gap:8px'><input name='primary' value='{s["primary"]}'><input name='secondary' value='{s["secondary"]}'></div>
    <b>💰 Money Control</b><div style='display:flex;gap:8px'><input name='ad' type='number' value='{s["ad"]}'><input name='clim' type='number' value='{s["clim"]}'><input name='pop' type='number' value='{s["pop"]}'><input name='plim' type='number' value='{s["plim"]}'></div>
    <input name='company_ad_id' value='{s["company_ad_id"]}' placeholder='11764581'><input name='popup_ad_id' value='{s["popup_ad_id"]}' placeholder='11760259'><input name='direct_link' value='{s["direct_link"]}'>
    <b>📦 Big Sponsored Box (নিচের বড় বক্স)</b><input name='spon_title' value='{s["spon_title"]}'><textarea name='spon_desc' rows='3'>{s["spon_desc"]}</textarea>
    <button style='background:{s["primary"]};color:#fff;width:100%;padding:12px;border:none;border-radius:10px;margin-top:10px;font-weight:800'>Save All</button></form></div>
    <div class='card'><h4>Tasks</h4><table style='width:100%'><tr><th>ID</th><th>Title</th><th>Del</th></tr>{rows}</table><form method='post'><input type='hidden' name='act' value='add_task'><input name='title' placeholder='Title' required><input name='link' placeholder='Link' required><input name='reward' type='number' value='20'><button style='background:{s["primary"]};color:#fff;width:100%;padding:8px;border:none;border-radius:8px;margin-top:6px'>Add</button></form></div>
    <a href='/' style='color:{s["primary"]}'>← App</a></body></html>
    """)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<script src='//libtl.com/sdk.js' data-zone='11764581' data-sdk='show_11764581'></script>
<style>
:root{--primary:#8b5cf6;--secondary:#f59e0b}
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:90px}
.glass{background:linear-gradient(135deg,#151A2D,#1A2040);border:1px solid rgba(139,92,246,.2);border-radius:20px;padding:16px;margin:12px}
.btn{width:100%;padding:12px;border:none;border-radius:12px;font-weight:800;color:#fff;background:var(--primary);margin-top:8px;cursor:pointer}
.btn2{background:var(--secondary)!important;color:#000!important}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:rgba(21,26,45,.98);backdrop-filter:blur(15px);display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#64748b;font-size:10px;font-weight:700;cursor:pointer}.btm div.on{color:var(--primary)}.btm div span{font-size:20px;display:block}
.page{display:none}.page.active{display:block}
.task-card{display:flex;justify-content:space-between;align-items:center;padding:14px;background:#0F1429;border:1px solid #1e293b;border-radius:14px;margin-top:10px}
input{width:100%;padding:12px;border-radius:12px;border:1px solid #1e293b;background:#0B0E1C;color:#fff;margin-top:8px;outline:none}
.meth{flex:1;padding:10px;border-radius:10px;border:1px solid #1e293b;text-align:center;cursor:pointer;background:#0B0E1C;font-weight:700}.meth.on{border-color:var(--primary);background:rgba(139,92,246,.2);color:var(--primary)}
.spon-big{background:linear-gradient(135deg,#1A1033 0%, #2D1B4E 50%, #1A1429 100%);border:1.5px solid var(--secondary);border-radius:24px;padding:22px;margin:12px;box-shadow:0 0 50px rgba(245,158,11,.25);min-height:170px}
.stat-box{flex:1;background:#0B0E1C;padding:12px;border-radius:12px;text-align:center;border:1px solid #1e293b}
.top-box{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid var(--primary);padding:6px 12px;border-radius:10px;font-size:13px;font-weight:800;display:inline-block}
.modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.8);display:none;align-items:center;justify-content:center;z-index:999;padding:20px}
.modal.on{display:flex}
</style></head><body>
<div id='welcomeModal' class='modal'><div class='glass' style='text-align:center;max-width:320px'><h2 id='wTitle'>🎉 স্বাগতম!</h2><p id='wMsg' style='margin:10px 0;font-size:13px;opacity:.8'></p><h1 style='color:#22c55e;margin:10px 0' id='wBonus'>৳100</h1><button class='btn' onclick='document.getElementById("welcomeModal").classList.remove("on")'>শুরু করুন 🚀</button></div></div>
<div id='adModal' class='modal'><div class='glass' style='text-align:center;max-width:320px'><h3>📢 Ads দেখুন</h3><p style='font-size:12px;opacity:.7;margin:8px 0' id='adInfo'>10 সেকেন্ড</p><h1 id='adTimer' style='font-size:40px;margin:10px'>10</h1><div style='width:100%;height:6px;background:#0B0E1C;border-radius:10px;overflow:hidden'><div id='adBar' style='height:100%;background:var(--primary);width:100%;transition:1s linear'></div></div><p style='font-size:11px;margin-top:8px;opacity:.6'>Reward: <b id='adReward' style='color:#22c55e'>৳3</b> | 💎 <span id='adDiamond'>300</span></p></div></div>
<div style='padding:10px 16px;display:flex;justify-content:space-between;align-items:center;background:#0F1429;position:sticky;top:0;z-index:99;border-bottom:1px solid #1e293b'>
<div style='display:flex;align-items:center;gap:8px'><div id='appLogo' style='width:38px;height:38px;border-radius:12px;background:#1e293b;display:flex;align-items:center;justify-content:center;border:1.5px solid var(--primary);overflow:hidden'>💎</div><div style='display:flex;gap:6px'><div class='top-box' id='appName'>SHIBLI👑</div><div class='top-box' style='border-color:var(--secondary)' id='appName2'>NOMAN✅</div></div></div><b id='bal' style='color:#22c55e'>৳0</b></div>
<div id='p-home' class='page active'>
<div class='glass'><div style='display:flex;justify-content:space-between'><div><small id='levelTxt' style='color:var(--primary)'>Level 1</small><br><b>Good Evening, <span id='uName'>User</span>!</b><br><small   <span style='font-size:10px;opacity:.6'>💎 <span id='diamond'>0</span> /span> Diamond | <span id='diamondRate'>100</span>=৳1</small></div><div style='text-align:right'><small>Total Balance</small><h2 id='bal2' style='color:#4ade80'>৳0</h2><small style='font-size:10px;color:var(--secondary)' id='adCount'>0/50 Ads</small></div></div></div>
<div style='display:flex;gap:10px;margin:0 12px'>
<div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><div style='display:flex;justify-content:space-between'><b style='font-size:13px'>Company Ads</b><small style='color:var(--secondary);font-size:10px' id='cAdInfo'>৳3</small></div><small style='font-size:10px;opacity:.6' id='cAdLimit'>0/50 today</small><button class='btn' style='padding:9px;font-size:12px;margin-top:8px' onclick='startAd("c")'>Start - ৳<span class='cReward'>3</span></button></div>
<div style='flex:1;background:#151A2D;border-radius:16px;padding:14px;border:1px solid #1e293b'><div style='display:flex;justify-content:space-between'><b style='font-size:13px'>Popup Ads</b><small style='color:var(--secondary);font-size:10px' id='pAdInfo'>৳5</small></div><small style='font-size:10px;opacity:.6' id='pAdLimit'>0/30 today</small><button class='btn btn2' style='padding:9px;font-size:12px;margin-top:8px' onclick='startAd("p")'>Watch - ৳<span class='pReward'>5</span></button></div>
</div>
<div class='glass'><h4>💸 Withdraw</h4>
<div style='display:flex;gap:8px;margin:8px 0'><div class='meth' id='m-bKash' onclick="selM('bKash')">bKash</div><div class='meth' id='m-Nagad' onclick="selM('Nagad')">Nagad</div></div>
<input id='wNum' placeholder='01XXXXXXXXX' style='margin-top:8px'>
<input id='wAmt' type='number' placeholder='Min 500 Taka' style='margin-top:8px'>
<button class='btn' onclick='doWD()' style='margin-top:10px'>Withdraw Now</button></div>
<div id='p-support' class='page'>
<div class='glass'><h3 id='supTitle'>💎 Support Center</h3><p id='supDesc' style='font-size:12px;opacity:.7;margin:6px 0'></p></div>
<div class='glass'><h4>📞 Contact Us</h4><div style='display:flex;gap:8px;margin-top:10px;flex-wrap:wrap'><button class='btn' style='flex:1;min-width:120px' onclick='window.open(document.getElementById("supTgLink").value,"_blank")'>✈️ Telegram</button><button class='btn btn2' style='flex:1;min-width:120px' onclick='window.open(document.getElementById("supWaLink").value,"_blank")'>💬 WhatsApp</button></div><div style='background:#0B0E1C;padding:10px;border-radius:10px;margin-top:8px;font-size:11px'><small>📧 Email: </small><b id='supEmailTxt'></b></div></div>
<div class='glass' style='border:1px solid var(--secondary);background:linear-gradient(135deg,#1A1400,#2A1F00)'><h4>📢 Notice Board</h4><p id='supNotice' style='font-size:13px;line-height:1.6;margin-top:8px;white-space:pre-wrap'></p></div>
<div class='glass'><h4>❓ FAQ</h4><details style='margin-top:8px;background:#0B0E1C;padding:10px;border-radius:10px'><summary style='font-size:13px;font-weight:700' id='faq1q'></summary><p style='font-size:12px;opacity:.7;margin-top:6px' id='faq1a'></p></details><details style='margin-top:8px;background:#0B0E1C;padding:10px;border-radius:10px'><summary style='font-size:13px;font-weight:700' id='faq2q'></summary><p style='font-size:12px;opacity:.7;margin-top:6px' id='faq2a'></p></details><details style='margin-top:8px;background:#0B0E1C;padding:10px;border-radius:10px'><summary style='font-size:13px;font-weight:700' id='faq3q'></summary><p style='font-size:12px;opacity:.7;margin-top:6px' id='faq3a'></p></details></div>
<div class='glass'><h4>📜 Rules</h4><pre id='supRules' style='white-space:pre-wrap;font-family:system-ui;font-size:12px;opacity:.8;line-height:1.6;margin-top:8px'></pre></div>
<input type='hidden' id='supTgLink'><input type='hidden' id='supWaLink'><input type='hidden' id='supFbLink'>
</div>
<div id='p-profile' class='page'>
<div class='glass' style='text-align:center'><div id='pImg' style='width:80px;height:80px;margin:0 auto;background:#1e293b;border-radius:22px;display:flex;align-items:center;justify-content:center;border:3px solid var(--primary);font-size:32px;overflow:hidden'>💎</div><div style='background:var(--secondary);display:inline-block;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:900;color:#000;margin-top:8px' id='pLevelBadge'>Level 1</div><h2 id='pName' style='margin-top:8px'>User</h2><small id='pJoin' style='opacity:.6'></small><br><small style='font-size:11px'>💎 <span id='pDiamond'>0</span> Diamond | <span id='pDiamondTaka'>0</span> Taka</small></div>
<div class='glass'><h4>📊 Statistics</h4><div style='display:flex;gap:8px;margin-top:10px'><div class='stat-box'><b style='font-size:18px;color:#22c55e' id='pTotal'>৳0</b><br><small>Total Earned</small></div><div class='stat-box'><b style='font-size:18px;color:var(--primary)' id='pBal'>৳0</b><br><small>Balance</small></div></div><div style='display:flex;gap:8px;margin-top:8px'><div class='stat-box'><b style='font-size:18px;color:var(--secondary)' id='pAds'>0</b><br><small>Ads</small></div><div class='stat-box'><b style='font-size:18px;color:#ec4899' id='pRef'>0</b><br><small>Refer</small></div></div></div>
<div class='glass'><h4>📈 Level Progress</h4><div style='display:flex;justify-content:space-between;font-size:12px;margin:8px 0'><span id='pLevelNow'>Level 1</span><span id='pLevelNext'>Next</span></div><div style='width:100%;height:10px;background:#0B0E1C;border-radius:20px;overflow:hidden'><div id='pProgBar' style='height:100%;background:var(--primary);width:0%;transition:1s'></div></div><small id='proNotice' style='opacity:.7;font-size:11px;margin-top:6px;display:block'></small></div>
<div class='glass'><h4>⚙️ Account</h4><div style='background:#0B0E1C;padding:12px;border-radius:12px;margin-top:8px'><small style='opacity:.6'>User ID</small><br><b id='pUid' style='font-size:12px'>u_123</b></div><input id='eName' placeholder='নতুন নাম'><input type='file' id='fImg' accept='image/*'><button class='btn' onclick='saveP()'>💾 Save Profile</button></div>
<div class='glass'><h4>💸 Withdraw History</h4><div id='pWhist' style='margin-top:8px'></div></div>
</div>
<div class='btm'>
<div onclick="show('home')" id='b-home' class='on'><span>🏠</span>Home</div>
<div onclick="show('tasks')" id='b-tasks'><span>🎯</span>Tasks</div>
<div onclick="show('refer')" id='b-refer'><span>👥</span>Refer</div>
<div onclick="show('support')" id='b-support'><span>💬</span>Support</div>
<div onclick="show('profile')" id='b-profile'><span>👤</span>Profile</div>
</div>
<script>
let uid=localStorage.getItem('uid'); if(!uid){uid='u_'+Date.now();localStorage.setItem('uid',uid)}
let ref=localStorage.getItem('ref')||new URLSearchParams(location.search).get('ref'); if(ref)localStorage.setItem('ref',ref)
let curM='bKash', sponLink='#', SET={}
function setM(m){curM=m;document.querySelectorAll('.meth').forEach(x=>x.classList.remove('on'));document.getElementById(m=='bKash'?'mBk':'mNa').classList.add('on')}
function startAd(type){
  let s=SET;
  let reward=type=='c'?s.ad:s.pop;
  document.getElementById('adReward').innerText='৳'+reward;
  document.getElementById('adDiamond').innerText=reward*s.diamond_rate;
  document.getElementById('adInfo').innerText=type=='c'?'Company Ads - '+s.ad_time+'s - Monetag ID: '+s.company_ad_id:'Popup Ads - '+s.ad_time+'s - ID: '+s.popup_ad_id;
  // REAL MONETAG CALL
  if(type=='c'){
    try{ if(typeof show_11764581 === 'function'){ show_11764581(); } }catch(e){}
  } else {
    window.open(s.direct_link,'_blank');
  }
  document.getElementById('adModal').classList.add('on');
  let t=s.ad_time; document.getElementById('adTimer').innerText=t; document.getElementById('adBar').style.width='100%';
  let iv=setInterval(()=>{
    t--; document.getElementById('adTimer').innerText=t; document.getElementById('adBar').style.width=(t/s.ad_time*100)+'%';
    if(t<=0){clearInterval(iv); document.getElementById('adModal').classList.remove('on');
      fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:type})}).then(r=>r.json()).then(d=>{alert(d.msg+' - Monetag Dollar আপনার একাউন্টে যোগ হবে');load()})
    }
  },1000);
}
function load(){fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,ref:ref})}).then(r=>r.json()).then(d=>{
SET=d.s;
document.documentElement.style.setProperty('--primary', d.s.primary);
document.documentElement.style.setProperty('--secondary', d.s.secondary);
document.getElementById('bal').innerText='৳'+d.user.bal;document.getElementById('bal2').innerText='৳'+d.user.bal;document.getElementById('uName').innerText=d.user.name;document.getElementById('pName').innerText=d.user.name;document.getElementById('pJoin').innerText='Join: '+d.user.join;document.getElementById('pUid').innerText=d.user.id;
document.getElementById('pTotal').innerText='৳'+d.user.total;document.getElementById('pBal').innerText='৳'+d.user.bal;document.getElementById('pAds').innerText=d.user.ads||0;document.getElementById('pRef').innerText=d.user.refl.length;
document.getElementById('diamond').innerText=d.user.diamonds||0;document.getElementById('diamondRate').innerText=d.s.diamond_rate;document.getElementById('pDiamond').innerText=d.user.diamonds||0;document.getElementById('pDiamondTaka').innerText=Math.floor((d.user.diamonds||0)/d.s.diamond_rate);
document.getElementById('pLevelBadge').innerText='Level '+d.level;document.getElementById('pLevelNow').innerText='Level '+d.level;document.getElementById('pLevelNext').innerText='Next: ৳'+d.next;document.getElementById('pProgBar').style.width=d.prog+'%';
document.getElementById('appName').innerText=d.s.app_name;document.getElementById('appName2').innerText=d.s.app_name2;
document.getElementById('sponTitle').innerText=d.s.spon_title;document.getElementById('sponDesc').innerText=d.s.spon_desc;document.getElementById('sponBtn').innerText=d.s.spon_btn; sponLink=d.s.spon_link;
document.getElementById('refTitle').innerText=d.s.ref_title;document.getElementById('refDesc').innerText=d.s.ref_desc;document.getElementById('refRules').innerText=d.s.ref_rules;document.getElementById('refBanner').innerText=d.s.ref_banner;
document.getElementById('supTitle').innerText=d.s.sup_title;document.getElementById('supDesc').innerText=d.s.sup_desc;document.getElementById('supNotice').innerText=d.s.sup_notice;document.getElementById('supRules').innerText=d.s.sup_rules;
document.getElementById('faq1q').innerText=d.s.sup_faq1_q;document.getElementById('faq1a').innerText=d.s.sup_faq1_a;document.getElementById('faq2q').innerText=d.s.sup_faq2_q;document.getElementById('faq2a').innerText=d.s.sup_faq2_a;document.getElementById('faq3q').innerText=d.s.sup_faq3_q;document.getElementById('faq3a').innerText=d.s.sup_faq3_a;
document.getElementById('supEmailTxt').innerText=d.s.sup_email;document.getElementById('supTgLink').value=d.s.sup_tg;document.getElementById('supWaLink').value=d.s.sup_wa;document.getElementById('supFbLink').value=d.s.sup_fb;
document.getElementById('proNotice').innerText=d.s.pro_notice;
document.getElementById('cAdInfo').innerText='৳'+d.s.ad;document.getElementById('pAdInfo').innerText='৳'+d.s.pop;document.querySelectorAll('.cReward').forEach(e=>e.innerText=d.s.ad);document.querySelectorAll('.pReward').forEach(e=>e.innerText=d.s.pop);
document.getElementById('cAdLimit').innerText=d.user.c+'/'+d.s.clim+' today';document.getElementById('pAdLimit').innerText=d.user.p+'/'+d.s.plim+' today';document.getElementById('adCount').innerText=(d.user.c+d.user.p)+'/'+(d.s.clim+d.s.plim)+' Ads';
if(d.s.app_logo){document.getElementById('appLogo').innerHTML='<img src="'+d.s.app_logo+'" style="width:100%;height:100%;object-fit:cover">'}
document.getElementById('levelTxt').innerText='Diamond Member • Level '+d.level;
document.getElementById('eName').value=d.user.name;
if(d.user.img){document.getElementById('pImg').innerHTML='<img src="'+d.user.img+'" style="width:100%;height:100%;object-fit:cover">'}
let tl='';d.tasks.forEach(t=>{let done=d.user.done.includes(t.id);tl+=`<div class='task-card'><div style='display:flex;gap:10px;align-items:center'><div style='font-size:20px'>${t.icon}</div><div><b style='font-size:13px'>${t.title}</b><br><small style='color:#22c55e'>৳${t.reward} + 💎${t.reward*d.s.diamond_rate}</small></div></div><button class='btn' style='width:auto;padding:7px 14px;margin:0' onclick='doT(${t.id},"${t.link}")' ${done?'disabled':''}>${done?'Done':'Go'}</button></div>`});document.getElementById('tList').innerHTML=tl;
document.getElementById('rLink').value=location.origin+'/?ref='+d.user.id;
document.getElementById('rCount').innerText=d.user.refl.length;document.getElementById('rEarn').innerText='৳'+(d.user.refl.length*d.s.ref);
let wh='';d.wds.forEach(w=>{wh+=`<div style='padding:6px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #1e293b'><span>${w.m} ৳${w.amt}</span><span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:8px'>${w.st}</span></div>`});document.getElementById('wH').innerHTML=wh||'<small style="opacity:.5">No history</small>';document.getElementById('pWhist').innerHTML=wh||'<small style="opacity:.5">No withdraw</small>';
document.getElementById('rList').innerHTML=d.user.refl.map(r=>`<div style='padding:8px;font-size:12px;border-bottom:1px solid #1e293b;display:flex;justify-content:space-between'><span>👤 ${r}</span><span style='color:#22c55e'>+৳${d.s.ref}</span></div>`).join('')||'<small style="opacity:.5">No refer yet</small>';
if(d.is_new){document.getElementById('wTitle').innerText=d.s.welcome_title;document.getElementById('wMsg').innerText=d.s.welcome_msg;document.getElementById('wBonus').innerText='৳'+d.s.bonus+' + 💎'+(d.s.bonus*d.s.diamond_rate);document.getElementById('welcomeModal').classList.add('on')}
})}
function doT(id,link){window.open(link,'_blank');fetch('/api/task',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function doWd(){let num=document.getElementById('wNum').value,amt=document.getElementById('wAmt').value;fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,m:curM,num:num,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}
function saveP(){let n=document.getElementById('eName').value;let f=document.getElementById('fImg').files[0];if(f){let rd=new FileReader();rd.onload=e=>{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:e.target.result})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})};rd.readAsDataURL(f)}else{fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n})}).then(r=>r.json()).then(d=>{alert(d.msg);load()})}}
function show(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.btm div').forEach(x=>x.classList.remove('on'));document.getElementById('b-'+p).classList.add('on')}
function copyR(){let i=document.getElementById('rLink');i.select();document.execCommand('copy');alert('Copied')}
document.getElementById('sponBtn').onclick=()=>{if(sponLink) window.open(sponLink,'_blank')}
load()
</script></body></html>
    """)

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
