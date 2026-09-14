import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'

def load_db():
    if not os.path.exists(DB):
        d={"users":{},"withdraws":[],"settings":{
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","verified_txt":"✓",
            "slider_img1":"","slider_img2":"","slider_img3":"","slider_img4":"","slider_img5":"",
            "slider_txt1":"🎉 Daily Bonus Available Today","slider_txt2":"📢 Company Sponsored • 100% Safe","slider_txt3":"🎁 50 Ads দেখলে ৳100 বোনাস","slider_txt4":"💰 100% Payment Guaranteed","slider_txt5":"🚀 প্রতিদিন কাজ করুন",
            "balance_title":"আপনার বর্তমান ব্যালেন্স","company_btn":"COMPANY ADS (৳2) -","popup_btn":"POPUP ADS (৳3) -","task_btn":"TASK BONUS - 5 টা/দিন","offer_title":"আজকের স্পেশাল অফার","offer_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!",
            "task1_title":"Telegram Channel Join","task1_sub":"চ্যানেলে জয়েন করুন • ৳25","task1_reward":"25","task1_link":"https://t.me/","task2_title":"YouTube Subscribe","task2_sub":"সাবস্ক্রাইব + লাইক • ৳30","task2_reward":"30","task2_link":"https://youtube.com/","task3_title":"Facebook Page Like","task3_sub":"পেজে লাইক দিন • ৳20","task3_reward":"20","task3_link":"https://facebook.com/","task4_title":"Refer Friend","task4_sub":"১ জন রেফার = ৳50","task4_reward":"50","task5_title":"Daily Check-in","task5_sub":"প্রতিদিন একবার • ৳15","task5_reward":"15",
            "refer_title":"Refer & Earn ৳50","tele_box_title":"Telegram Channel","tele_box_sub":"আপডেট ও প্রুফ","tele_box_link":"https://t.me/",
            "wallet_bal_title":"ব্যালেন্স","wallet_min":"Min ৳500","wallet_method_title":"Withdraw Method","bkash_name":"bKash","bkash_sub":"Personal • Instant Payment","bkash_logo":"","nagad_name":"Nagad","nagad_sub":"Personal • Fast Withdraw","nagad_logo":"","withdraw_btn":"Withdraw করুন","rule_title":"Withdraw নিয়ম","rule1":"- মিনিমাম ৳500","rule2":"- Personal নাম্বার দিন","rule3":"- 24 ঘণ্টায় পেমেন্ট",
            "support_top_msg":"যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন","support_center_title":"আমরা আছি আপনার পাশে","support_center_sub":"২৪ ঘণ্টা সাপোর্ট • 100% Trusted • SHIBLI NOMAN Team","quick_contact_title":"দ্রুত যোগাযোগ করুন","tele_sup_title":"Telegram Support (Fast Reply)","tele_sup_sub":"2 মিনিটে রিপ্লাই • 9AM-12AM","tele_sup_link":"https://t.me/","wa_sup_title":"WhatsApp Support","wa_sup_number":"01XXXXXXXXXX","wa_sup_link":"https://wa.me/8801","email_sup_title":"Email Support","email_sup_address":"support@protidinerkajbd.com","email_sup_link":"mailto:support@","how_work_title":"কিভাবে কাজ করবেন?","tutorial_btn_text":"Tutorial - 2 মিনিটে শিখুন","tutorial_click_text":"Click করলে ভিডিও চলবে","tutorial_youtube_link":"https://youtube.com/","step1":"Step 1: Ads দেখুন","step2":"Step 2: Task complete করুন","step3":"Step 3: ৳500 হলেই Withdraw",
            "profile_member_badge":"Bronze Member","stats_title":"পরিসংখ্যান","verified_title":"Verified User","verified_desc":"আপনার একাউন্ট 100% Safe • 24h Support",
            "zone":"11764581"
        }}
        open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
        return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","balance":1120,"company":0,"popup":0,"total":0,"tasks":[],"img":"","join":today,"last":today,"phone":uid}
    u=db["users"][uid]
    if u.get("last")!=today: u["company"]=0; u["popup"]=0; u["last"]=today
    return u

@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/admin')
def admin():
    if request.args.get('id')!='8807178385': return "Admin?id=8807178385"
    return render_template_string(ADMIN)
@app.route('/api/get')
def api_get():
    db=load_db(); u=get_user(db,request.args.get('id','0')); wds=[w for w in db["withdraws"] if w["uid"]==str(u["id"])]; save_db(db)
    return jsonify({"user":u,"settings":db["settings"],"withdraws":wds})
@app.route('/api/reward')
def reward():
    db=load_db(); typ=request.args.get('type','company'); u=get_user(db,request.args.get('id'))
    if typ=='company':
        if u["company"]>=30: return jsonify({"msg":"Company 30 শেষ"})
        u["company"]+=1; u["balance"]+=2
    else:
        if u["popup"]>=20: return jsonify({"msg":"Popup 20 শেষ"})
        u["popup"]+=1; u["balance"]+=3
    u["total"]+=1; save_db(db); return jsonify({"msg":"৳ যোগ","user":u})
@app.route('/api/task/done',methods=['POST'])
def taskdone():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); tid=int(j.get('tid'))
    if tid in u["tasks"]: return jsonify({"msg":"করা হয়েছে"})
    rw=int(db["settings"].get(f'task{tid}_reward','20')); u["tasks"].append(tid); u["balance"]+=rw; u["total"]+=1; save_db(db); return jsonify({"msg":f"✅ {rw} TK"})
@app.route('/api/withdraw',methods=['POST'])
def wd():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); amt=int(j.get('amt',0))
    if amt<500: return jsonify({"msg":"মিনিমাম ৳500"})
    if u["balance"]<amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt; db["withdraws"].append({"uid":str(u["id"]),"amt":amt,"num":j.get('num'),"method":j.get('method'),"status":"Pending","time":str(datetime.now())[:16]}); save_db(db); return jsonify({"msg":"✅ Withdraw Request"})
@app.route('/api/profile/save',methods=['POST'])
def psave():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); u["name"]=j.get('name',u["name"]); u["img"]=j.get('img',u["img"]); save_db(db); return jsonify({"msg":"✅ Profile Save"})
@app.route('/api/admin/save',methods=['POST'])
def asave():
    db=load_db(); j=request.json
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ FINAL SAVE - সব সেভ হয়েছে"})

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#08080f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:100px}
.top{padding:12px 14px;display:flex;justify-content:space-between;align-items:center;background:#0c0c1a;position:sticky;top:0;z-index:99;border-bottom:1px solid #1a1a2e}
.card{margin:10px 12px;border-radius:22px;padding:14px;background:#14142a;border:1px solid #1e1e3a}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;margin-top:10px;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;z-index:99;border-top:1px solid #1e1e3a}
.btm div{flex:1;text-align:center;color:#6b6b8a;font-size:11px;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:24px;display:block}
input{width:100%;padding:12px;border-radius:12px;border:1px solid #2a2a4a;background:#0e0e20;color:#fff;margin-top:8px}
.page{display:none}.page.active{display:block}
.halkaDew{animation:dewGlow 4s ease-in-out infinite}
@keyframes dewGlow{0%{box-shadow:0 0 0px transparent}50%{box-shadow:0 0 22px #ffffff0d,0 0 35px #6d4cff1a}100%{box-shadow:0 0 0px transparent}}
.progressWrap{width:100%;height:8px;background:#00000060;border-radius:10px;margin-top:14px;overflow:hidden}
.progressBar{height:100%;width:0%;background:linear-gradient(90deg,#22c55e,#f59e0b);border-radius:10px;transition:width 1.2s ease}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #2a2a4a;border-radius:18px;padding:14px;margin:12px 0;cursor:pointer;position:relative}
.payCard.active{border-color:#e2136e;background:#1a1a35;box-shadow:0 0 15px #e2136e33}
.check{position:absolute;right:12px;width:24px;height:24px;background:#22c55e;border-radius:50%;display:none;align-items:center;justify-content:center;font-size:14px;font-weight:900}
.payCard.active.check{display:flex}
.slider{position:relative;width:100%;height:160px;border-radius:22px;overflow:hidden;background:linear-gradient(90deg,#f59e0b,#ef4444)}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;opacity:0;transition:opacity 1s ease;background-size:cover;background-position:center}
.slide.active{opacity:1}
.dotWrap{display:flex;gap:6px;justify-content:center;margin-top:8px}
.dot{width:8px;height:8px;background:#ffffff40;border-radius:50%;transition:all.3s}
.dot.active{background:#fff;width:20px}
.avatarWrap{width:120px;height:120px;border-radius:50%;border:3px solid #6d4cff;margin:0 auto;position:relative;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden}
.statGrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px}
.statBox{background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:14px;text-align:center}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:800;font-size:16px" id="appNameTop">Protidiner Kaj BD <span style="background:#22c55e;width:20px;height:20px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:12px">✓</span></div><div style="font-size:12px;color:#9ca3af" id="adminNameTop">Admin: SHIBLI NOMAN</div></div></div><div onclick="goPage('profile')" style="width:46px;height:46px;border-radius:50%;border:2px solid #6d4cff;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden;cursor:pointer"><img id="topAv" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="topAvT">👤</span></div></div>

<div id="p-home" class="page active">
<!-- 5 ছবির স্লাইডার - উপরের বক্স - 3 সেকেন্ড পর পর - Admin থেকে চেঞ্জ -->
<div class="card halkaDew" style="padding:0;border:none;overflow:hidden">
<div class="slider" id="mainSlider">
<div class="slide active" id="s1" style="background:linear-gradient(90deg,#f59e0b,#ef4444)"><span id="st1">🎉 Daily Bonus Available Today</span></div>
<div class="slide" id="s2" style="background:linear-gradient(90deg,#06b6d4,#3b82f6)"><span id="st2">📢 Company Sponsored • 100% Safe</span></div>
<div class="slide" id="s3" style="background:linear-gradient(90deg,#10b981,#06b6d4)"><span id="st3">🎁 50 Ads দেখলে ৳100 বোনাস</span></div>
<div class="slide" id="s4" style="background:linear-gradient(90deg,#8b5cf6,#ec4899)"><span id="st4">💰 100% Payment Guaranteed</span></div>
<div class="slide" id="s5" style="background:linear-gradient(90deg,#f97316,#eab308)"><span id="st5">🚀 প্রতিদিন কাজ করুন</span></div>
</div>
<div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div>
</div>

<div class="card halkaDew" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4,#10b981);text-align:center;border:none"><div style="font-size:13px" id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:56px;font-weight:900;margin:8px 0" id="balMain">৳1120</div><div style="display:flex;gap:8px;justify-content:center"><span style="background:#0005;padding:6px 12px;border-radius:20px;font-size:12px" id="c1">Company 0/30</span><span style="background:#0005;padding:6px 12px;border-radius:20px;font-size:12px" id="c2">Popup 0/20</span><span style="background:#0005;padding:6px 12px;border-radius:20px;font-size:12px" id="c3">Total 0</span></div><div class="progressWrap"><div id="progressBar" class="progressBar"></div></div><div style="font-size:11px;margin-top:6px;opacity:.8" id="progTxt">0% Complete</div></div>

<div class="card"><button class="btn" style="background:#7c3aed" onclick="doCompany()">📺 <span id="btnCTxt">COMPANY ADS (৳2) -</span> <span id="btnC">0/30</span></button><button class="btn" style="background:#16a34a" onclick="doPopup()">💰 <span id="btnPTxt">POPUP ADS (৳3) -</span> <span id="btnP">0/20</span></button><button class="btn" style="background:#1e293b" onclick="goPage('tasks')">📋 <span id="btnTTxt">TASK BONUS - 5 টা/দিন</span></button></div>
<div class="card halkaDew" style="border:1px solid #f59e0b"><div style="font-weight:800" id="offerT">🎉 আজকের স্পেশাল অফার</div><div style="font-size:13px;color:#9ca3af" id="offerD">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</div><button class="btn" style="background:linear-gradient(90deg,#f59e0b,#ef4444)" onclick="alert('অফার - কাজ করে')">🎁 অফার নিন</button></div>
</div>

<div id="p-tasks" class="page"><div class="card"><div style="font-weight:800;font-size:18px;margin-bottom:10px" id="taskTitle">📋 Task Bonus - দিনে 5 টা</div><div id="taskList"></div><div style="background:linear-gradient(135deg,#6d4cff,#4f46e5);border-radius:20px;padding:16px;margin-top:16px" class="halkaDew"><div style="font-weight:800" id="referTitle">🎁 Refer & Earn ৳50</div><div style="background:#00000040;border-radius:12px;padding:10px;margin-top:10px;font-size:12px;word-break:break-all" id="refLink2"></div><button class="btn" style="background:#fff;color:#4f46e5" onclick="copyText('refLink2')">📋 লিংক কপি</button></div></div></div>

<div id="p-wallet" class="page"><div class="card halkaDew" style="background:#1e293b;text-align:center;padding:24px"><div style="color:#94a3b8" id="walletTitle">ব্যালেন্স</div><div style="font-size:52px;font-weight:900" id="wBal">৳1120</div><div style="color:#94a3b8" id="walletMin">Min ৳500</div><div class="progressWrap"><div id="wProgress" class="progressBar"></div></div></div><div class="card"><div style="font-weight:800;font-size:18px;margin-bottom:12px" id="walletMethodTitle">💸 Withdraw Method</div><div id="bCard" class="payCard active" onclick="selectPay('bKash')"><div id="bLogo" style="width:56px;height:56px;background:#e2136e;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:24px">৳</div><div style="flex:1"><b id="bName">bKash</b><div style="font-size:12px;color:#94a3b8" id="bSub">Personal • Instant Payment</div></div><div class="check">✓</div></div><div id="nCard" class="payCard" onclick="selectPay('Nagad')"><div id="nLogo" style="width:56px;height:56px;background:#f59e0b;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:24px">৳</div><div style="flex:1"><b id="nName">Nagad</b><div style="font-size:12px;color:#94a3af" id="nSub">Personal • Fast Withdraw</div></div><div class="check">✓</div></div><input id="accNum" placeholder="01XXXXXXXXXXX"><input id="wdAmt" type="number" placeholder="500"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f59e0b)" onclick="doWithdraw()" id="wdBtn">🚀 Withdraw করুন</button></div></div>

<div id="p-support" class="page"><div class="card halkaDew" style="background:linear-gradient(135deg,#4f46e5,#6d4cff);text-align:center"><div style="background:#0003;padding:10px;border-radius:12px;font-size:14px;font-weight:800" id="supTop">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:22px;font-weight:900;margin-top:10px" id="supCenter">আমরা আছি আপনার পাশে</div><div style="font-size:12px;margin-top:4px" id="supSub">২৪ ঘণ্টা সাপোর্ট • 100% Trusted • SHIBLI NOMAN Team</div></div><div class="card"><div style="font-weight:800;margin-bottom:10px" id="quickT">🚀 দ্রুত যোগাযোগ করুন</div><button class="btn" style="background:#0ea5e9" onclick="openLink('tele_sup')">✈️ <span id="teleSupT">Telegram Support</span></button><button class="btn" style="background:#22c55e" onclick="openLink('wa_sup')">💬 <span id="waSupT">WhatsApp Support</span></button><button class="btn" style="background:#f59e0b" onclick="openLink('email_sup')">📧 <span id="emailSupT">Email Support</span></button><button class="btn" style="background:#1a1a35" onclick="openLink('tutorial')">▶️ <span id="tutBtnT">Tutorial - 2 মিনিটে শিখুন</span></button></div></div>

<div id="p-profile" class="page"><div class="card" style="text-align:center"><div class="avatarWrap halkaDew" onclick="openGal()"><img id="pAv" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="pAvT" style="font-size:64px">👤</span></div><div style="margin-top:10px"><b id="pName">User</b><div style="font-size:12px;color:#9ca3af" id="pId">ID:</div><div style="background:#6d4cff;display:inline-block;padding:6px 14px;border-radius:20px;font-size:12px;margin-top:8px" id="memberBadge">🏅 Bronze Member</div></div><input id="pNameIn" placeholder="নাম" style="text-align:center"><button class="btn" style="background:#6d4cff" onclick="openGal()">📸 গ্যালারি থেকে ছবি নিন</button><button class="btn" style="background:#22c55e" onclick="saveProf()">💾 Save Profile</button><input type="file" id="fileIn" accept="image/*" style="display:none" onchange="handleFile(this)"></div><div class="card"><div style="font-weight:800" id="statsTitle">📊 পরিসংখ্যান</div><div class="statGrid"><div class="statBox"><div>💰</div><div style="font-weight:900" id="sBal">৳1120</div><div style="font-size:11px">ব্যালেন্স</div></div><div class="statBox"><div>📺</div><div style="font-weight:900" id="sAds">0</div><div style="font-size:11px">Ads</div></div><div class="statBox"><div>📋</div><div style="font-weight:900" id="sTask">0</div><div style="font-size:11px">Task</div></div></div><div style="margin-top:12px;background:#0e0e20;padding:10px;border-radius:12px;font-size:11px;word-break:break-all" id="myRef"></div><button class="btn" style="background:#1e293b" onclick="copyText('myRef')">📋 Refer Link Copy</button><button class="btn" style="background:#ef4444" onclick="localStorage.clear();location.reload()">🚪 লগআউট</button></div><div class="card halkaDew" style="background:linear-gradient(135deg,#065f46,#047857);text-align:center"><div style="font-weight:900" id="verifiedTitle">🛡️ Verified User</div><div style="font-size:12px" id="verifiedDesc">100% Safe</div></div></div>

<div class="btm"><div id="n-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div><div id="n-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div><div id="n-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div><div id="n-support" onclick="goPage('support')"><span>💬</span>Support</div><div id="n-profile" onclick="goPage('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=localStorage.getItem('locked_phone')||'8807178385'; let tempImg=''; let settings={}; let method='bKash'; let curSlide=0;
function init(){ fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ settings=d.settings; let u=d.user; let total=u.company+u.popup; let pct=Math.min(Math.round((total/50)*100),100);
document.getElementById('appNameTop').innerHTML=settings.app_name+' <span style="background:#22c55e;width:20px;height:20px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:12px">'+settings.verified_txt+'</span>';
document.getElementById('adminNameTop').innerText='Admin: '+settings.admin_name;
document.getElementById('st1').innerText=settings.slider_txt1; document.getElementById('st2').innerText=settings.slider_txt2; document.getElementById('st3').innerText=settings.slider_txt3; document.getElementById('st4').innerText=settings.slider_txt4; document.getElementById('st5').innerText=settings.slider_txt5;
// 5 ছবি থাকলে ব্যাকগ্রাউন্ডে বসবে
for(let i=1;i<=5;i++){ let img=settings['slider_img'+i]; if(img){ document.getElementById('s'+i).style.backgroundImage='url('+img+')'; document.getElementById('s'+i).style.backgroundSize='cover'; } }
document.getElementById('balTitle').innerText=settings.balance_title; document.getElementById('balMain').innerText='৳'+u.balance; document.getElementById('wBal').innerText='৳'+u.balance; document.getElementById('sBal').innerText='৳'+u.balance;
document.getElementById('c1').innerText='Company '+u.company+'/30'; document.getElementById('c2').innerText='Popup '+u.popup+'/20'; document.getElementById('c3').innerText='Total '+u.total;
document.getElementById('btnCTxt').innerText=settings.company_btn; document.getElementById('btnPTxt').innerText=settings.popup_btn; document.getElementById('btnTTxt').innerText=settings.task_btn;
document.getElementById('btnC').innerText=u.company+'/30'; document.getElementById('btnP').innerText=u.popup+'/20';
document.getElementById('progressBar').style.width=pct+'%'; document.getElementById('wProgress').style.width=pct+'%'; document.getElementById('progTxt').innerText=pct+'% Complete - '+total+' টা Ads';
document.getElementById('offerT').innerText=settings.offer_title; document.getElementById('offerD').innerText=settings.offer_desc;
document.getElementById('walletTitle').innerText=settings.wallet_bal_title; document.getElementById('walletMin').innerText=settings.wallet_min; document.getElementById('walletMethodTitle').innerText=settings.wallet_method_title;
document.getElementById('bName').innerText=settings.bkash_name; document.getElementById('bSub').innerText=settings.bkash_sub; document.getElementById('nName').innerText=settings.nagad_name; document.getElementById('nSub').innerText=settings.nagad_sub; document.getElementById('wdBtn').innerText=settings.withdraw_btn;
if(settings.bkash_logo){ document.getElementById('bLogo').innerHTML='<img src='+settings.bkash_logo+' style=width:100%;height:100%;object-fit:cover;border-radius:16px>'; } if(settings.nagad_logo){ document.getElementById('nLogo').innerHTML='<img src='+settings.nagad_logo+' style=width:100%;height:100%;object-fit:cover;border-radius:16px>'; }
document.getElementById('supTop').innerText=settings.support_top_msg; document.getElementById('supCenter').innerText=settings.support_center_title; document.getElementById('supSub').innerText=settings.support_center_sub; document.getElementById('quickT').innerText=settings.quick_contact_title; document.getElementById('teleSupT').innerText=settings.tele_sup_title; document.getElementById('waSupT').innerText=settings.wa_sup_title; document.getElementById('emailSupT').innerText=settings.email_sup_title; document.getElementById('tutBtnT').innerText=settings.tutorial_btn_text;
document.getElementById('pName').innerText=u.name; document.getElementById('pId').innerText='ID: '+u.id; document.getElementById('sAds').innerText=total; document.getElementById('sTask').innerText=u.tasks.length; document.getElementById('myRef').innerText=location.origin+'/?ref='+u.id; document.getElementById('refLink2').innerText=location.origin+'/?ref='+u.id; document.getElementById('pNameIn').value=u.name; document.getElementById('memberBadge').innerText=settings.profile_member_badge; document.getElementById('statsTitle').innerText=settings.stats_title; document.getElementById('verifiedTitle').innerText=settings.verified_title; document.getElementById('verifiedDesc').innerText=settings.verified_desc;
if(u.img){ document.getElementById('pAv').src=u.img; document.getElementById('pAv').style.display='block'; document.getElementById('pAvT').style.display='none'; document.getElementById('topAv').src=u.img; document.getElementById('topAv').style.display='block'; document.getElementById('topAvT').style.display='none'; tempImg=u.img; }
let taskHtml=''; for(let i=1;i<=5;i++){ let done=u.tasks.includes(i); taskHtml+=`<div style="display:flex;align-items:center;justify-content:space-between;background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:12px;margin:10px 0"><div><b>${settings['task'+i+'_title']}</b><div style="font-size:11px;color:#9ca3af">${settings['task'+i+'_sub']}</div></div><button class="btn" style="width:auto;background:${done?'#22c55e':'#6d4cff'};padding:10px 18px;margin:0" onclick="doTask(${i})">${done?'✓':settings['task'+i+'_reward']+'৳'}</button></div>`; } document.getElementById('taskList').innerHTML=taskHtml; document.getElementById('taskTitle').innerText=settings.task_title; document.getElementById('referTitle').innerText=settings.refer_title;
});}
function goPage(p){ document.querySelectorAll('.page').forEach(e=>e.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on')); document.getElementById('n-'+p).classList.add('on');}
function doCompany(){ fetch('/api/reward?id='+uid+'&type=company').then(r=>r.json()).then(d=>{ alert(d.msg); init(); if(typeof show_11764581==='function') show_11764581(); });}
function doPopup(){ fetch('/api/reward?id='+uid+'&type=popup').then(r=>r.json()).then(d=>{ alert(d.msg); init(); if(typeof show_11764581==='function') show_11764581(); });}
function doTask(i){ let links={1:settings.task1_link,2:settings.task2_link,3:settings.task3_link}; if(links[i]) window.open(links[i],'_blank'); fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:i})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); });}
function selectPay(m){ method=m; document.getElementById('bCard').classList.toggle('active',m=='bKash'); document.getElementById('nCard').classList.toggle('active',m=='Nagad'); }
function doWithdraw(){ let num=document.getElementById('accNum').value; let amt=document.getElementById('wdAmt').value; if(!num||!amt){alert('নাম্বার + টাকা দিন');return;} fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:method})}).then(r=>r.json()).then(d=>{ alert(d.msg+' - '+method+' ✓'); init(); });}
function openLink(k){ let map={tele_sup:settings.tele_sup_link,wa_sup:settings.wa_sup_link,email_sup:settings.email_sup_link,tutorial:settings.tutorial_youtube_link}; let l=map[k]; if(l) window.open(l,'_blank');}
function openGal(){ document.getElementById('fileIn').click(); }
function handleFile(inp){ let f=inp.files[0]; if(!f) return; let rd=new FileReader(); rd.onload=e=>{ tempImg=e.target.result; document.getElementById('pAv').src=tempImg; document.getElementById('pAv').style.display='block'; document.getElementById('pAvT').style.display='none'; document.getElementById('topAv').src=tempImg; document.getElementById('topAv').style.display='block'; document.getElementById('topAvT').style.display='none'; }; rd.readAsDataURL(f); }
function saveProf(){ let name=document.getElementById('pNameIn').value||'User'; fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:name,img:tempImg})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); });}
function copyText(id){ navigator.clipboard.writeText(document.getElementById(id).innerText); alert('✅ Copy');}
// 5 ছবি স্লাইডার - 3 সেকেন্ড পর পর
setInterval(()=>{ curSlide=(curSlide+1)%5; document.querySelectorAll('.slide').forEach((el,i)=>el.classList.toggle('active',i==curSlide)); document.querySelectorAll('.dot').forEach((el,i)=>el.classList.toggle('active',i==curSlide)); },3000);
init();
</script></body></html>
"""

ADMIN="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>FINAL Admin - A to Z</title><style>body{background:#070710;color:#fff;max-width:800px;margin:0 auto;padding:14px;font-family:system-ui}.card{background:#15152a;border-radius:14px;padding:14px;margin:12px 0;border:1px solid #222}input{width:100%;padding:10px;border-radius:10px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}label{font-size:12px;color:#9ca3af;margin-top:10px;display:block}.btn{width:100%;padding:14px;background:linear-gradient(90deg,#6d4cff,#4f46e5);border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:16px;cursor:pointer;font-size:16px}h3{color:#f59e0b;margin-bottom:8px}</style></head><body>
<h2 style="text-align:center">👑 FINAL Admin Panel - A to Z - 5 ছবি স্লাইডার</h2>
<div class="card" style="border:2px solid #f59e0b"><h3>🏠 উপরের বক্স - 5 ছবি - 3 সেকেন্ড পর পর বদলাবে - Admin থেকে চেঞ্জ</h3>
<label>Slider Image 1 URL (ছবি না দিলে লেখা দেখাবে)</label><input id="slider_img1" placeholder="https://...jpg">
<label>Slider Text 1</label><input id="slider_txt1">
<label>Slider Image 2 URL</label><input id="slider_img2" placeholder="https://...jpg">
<label>Slider Text 2</label><input id="slider_txt2">
<label>Slider Image 3 URL</label><input id="slider_img3">
<label>Slider Text 3</label><input id="slider_txt3">
<label>Slider Image 4 URL</label><input id="slider_img4">
<label>Slider Text 4</label><input id="slider_txt4">
<label>Slider Image 5 URL</label><input id="slider_img5">
<label>Slider Text 5</label><input id="slider_txt5">
</div>

<div class="card" style="border:2px solid #6d4cff"><h3>📝 নাম পরিবর্তন - সবকিছু</h3><label>App Name</label><input id="app_name"><label>Admin Name</label><input id="admin_name"><label>Balance Title</label><input id="balance_title"><label>Company Button Text</label><input id="company_btn"><label>Popup Button Text</label><input id="popup_btn"><label>Task Button Text</label><input id="task_btn"><label>Offer Title</label><input id="offer_title"><label>Offer Desc</label><input id="offer_desc"></div>

<div class="card" style="border:2px solid #22c55e"><h3>📋 Task - 5 টা - নাম + লিংক + টাকা</h3>
<label>Task1 Title</label><input id="task1_title"><label>Task1 Sub</label><input id="task1_sub"><label>Task1 Reward</label><input id="task1_reward"><label>Task1 Link</label><input id="task1_link">
<label>Task2 Title</label><input id="task2_title"><label>Task2 Sub</label><input id="task2_sub"><label>Task2 Reward</label><input id="task2_reward"><label>Task2 Link</label><input id="task2_link">
<label>Task3 Title</label><input id="task3_title"><label>Task3 Sub</label><input id="task3_sub"><label>Task3 Reward</label><input id="task3_reward"><label>Task3 Link</label><input id="task3_link">
<label>Task4 Title</label><input id="task4_title"><label>Task4 Sub</label><input id="task4_sub"><label>Task4 Reward</label><input id="task4_reward">
<label>Task5 Title</label><input id="task5_title"><label>Task5 Sub</label><input id="task5_sub"><label>Task5 Reward</label><input id="task5_reward">
</div>

<div class="card" style="border:2px solid #e2136e"><h3>💸 Wallet - bKash/Nagad Logo + নাম</h3><label>bKash Name</label><input id="bkash_name"><label>bKash Sub</label><input id="bkash_sub"><label>bKash Logo URL</label><input id="bkash_logo" placeholder="https://...png"><label>Nagad Name</label><input id="nagad_name"><label>Nagad Sub</label><input id="nagad_sub"><label>Nagad Logo URL</label><input id="nagad_logo" placeholder="https://...png"><label>Withdraw Button</label><input id="withdraw_btn"></div>

<div class="card" style="border:2px solid #0ea5e9"><h3>💬 Support - সব লিংক</h3><label>Support Top Msg</label><input id="support_top_msg"><label>Support Center Title</label><input id="support_center_title"><label>Support Center Sub</label><input id="support_center_sub"><label>Quick Contact Title</label><input id="quick_contact_title"><label>Telegram Title</label><input id="tele_sup_title"><label>Telegram Link</label><input id="tele_sup_link"><label>WhatsApp Title</label><input id="wa_sup_title"><label>WhatsApp Number</label><input id="wa_sup_number"><label>WhatsApp Link</label><input id="wa_sup_link"><label>Email Title</label><input id="email_sup_title"><label>Email Address</label><input id="email_sup_address"><label>Email Link</label><input id="email_sup_link"><label>How Work Title</label><input id="how_work_title"><label>Tutorial Button</label><input id="tutorial_btn_text"><label>Tutorial YouTube Link</label><input id="tutorial_youtube_link"></div>

<div class="card"><h3>⚙️ অন্যান্য</h3><label>Profile Member Badge</label><input id="profile_member_badge"><label>Stats Title</label><input id="stats_title"><label>Verified Title</label><input id="verified_title"><label>Verified Desc</label><input id="verified_desc"></div>

<button class="btn" onclick="saveAll()">💾 FINAL SAVE - সব সেভ করুন - A to Z</button><div id="msg" style="color:#22c55e;text-align:center;margin-top:12px;font-weight:800"></div>

<script>
function load(){ fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{ for(let k in d.settings){ let el=document.getElementById(k); if(el) el.value=d.settings[k]; } });}
function saveAll(){ let data={}; document.querySelectorAll('input').forEach(e=>{ if(e.id) data[e.id]=e.value; }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ document.getElementById('msg').innerText=d.msg; alert('✅ FINAL - সব সেভ হয়েছে - 5 ছবি 3 সেকেন্ড পর পর বদলাবে'); });}
load();
</script></body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
