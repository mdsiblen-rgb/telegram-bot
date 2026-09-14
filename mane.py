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
            "task_title":"Task Bonus - দিনে 5 টা","task1_title":"Telegram Channel Join","task1_sub":"চ্যানেলে জয়েন করুন • ৳25","task1_reward":"25","task1_link":"https://t.me/","task2_title":"YouTube Subscribe","task2_sub":"সাবস্ক্রাইব + লাইক • ৳30","task2_reward":"30","task2_link":"https://youtube.com/","task3_title":"Facebook Page Like","task3_sub":"পেজে লাইক দিন • ৳20","task3_reward":"20","task3_link":"https://facebook.com/","task4_title":"Refer Friend","task4_sub":"১ জন রেফার = ৳50","task4_reward":"50","task5_title":"Daily Check-in","task5_sub":"প্রতিদিন একবার • ৳15","task5_reward":"15",
            "refer_title":"Refer & Earn ৳50","tele_box_title":"Telegram Channel","tele_box_sub":"আপডেট ও প্রুফ","tele_box_link":"https://t.me/",
            "wallet_bal_title":"ব্যালেন্স","wallet_min":"Min ৳500","wallet_method_title":"Withdraw Method","bkash_name":"bKash","bkash_sub":"Personal • Instant Payment","bkash_logo":"","nagad_name":"Nagad","nagad_sub":"Personal • Fast Withdraw","nagad_logo":"","withdraw_btn":"Withdraw করুন","rule_title":"Withdraw নিয়ম","rule1":"- মিনিমাম ৳500","rule2":"- Personal নাম্বার দিন","rule3":"- 24 ঘণ্টায় পেমেন্ট",
            "support_top_msg":"যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন","support_center_title":"আমরা আছি আপনার পাশে","support_center_sub":"২৪ ঘণ্টা সাপোর্ট • 100% Trusted • SHIBLI NOMAN Team","quick_contact_title":"দ্রুত যোগাযোগ করুন","tele_sup_title":"Telegram Support (Fast Reply)","tele_sup_sub":"2 মিনিটে রিপ্লাই • 9AM-12AM","tele_sup_link":"https://t.me/","wa_sup_title":"WhatsApp Support","wa_sup_number":"01XXXXXXXXXX","wa_sup_link":"https://wa.me/8801","email_sup_title":"Email Support","email_sup_address":"support@protidinerkajbd.com","email_sup_link":"mailto:support@","how_work_title":"কিভাবে কাজ করবেন?","tutorial_btn_text":"Tutorial - 2 মিনিটে শিখুন","tutorial_click_text":"Click করলে ভিডিও চলবে","tutorial_youtube_link":"https://youtube.com/","step1":"Step 1: Ads দেখুন","step2":"Step 2: Task complete করুন","step3":"Step 3: ৳500 হলেই Withdraw","faq_q1":"Q: টাকা কখন পাবো?","faq_a1":"A: 24 ঘণ্টার মধ্যে bKash/Nagad এ।",
            "profile_card_bg":"#14142a","profile_card_border":"#1e1e3a","avatar_border_color":"#6d4cff","profile_name_color":"#ffffff","profile_id_color":"#9ca3af","stats_card_bg":"#0e0e20","stats_border":"#1e1e3a","verified_bg":"linear-gradient(135deg,#065f46,#047857)",
            "badge1_name":"Bronze Member","badge1_bg":"#6d4cff","badge1_text":"#ffffff","badge1_icon":"🏅","badge2_name":"Silver Member","badge2_bg":"#9ca3af","badge2_text":"#000000","badge2_icon":"🥈","badge3_name":"Gold Member","badge3_bg":"#f59e0b","badge3_text":"#000000","badge3_icon":"🥇","badge4_name":"Platinum Member","badge4_bg":"#06b6d4","badge4_text":"#ffffff","badge4_icon":"💎","badge5_name":"Diamond Member","badge5_bg":"#e2136e","badge5_text":"#ffffff","badge5_icon":"👑",
            "zone":"11764581"
        }}
        open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
        return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","balance":1120,"company":0,"popup":0,"total":0,"tasks":[],"img":"","join":today,"last":today,"badge":1,"phone":uid}
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
    u["total"]+=1; tot=u["company"]+u["popup"]+len(u["tasks"]); u["badge"]=5 if tot>=50 else 4 if tot>=40 else 3 if tot>=25 else 2 if tot>=10 else 1
    save_db(db); return jsonify({"msg":f"✅ ৳{'2' if typ=='company' else '3'} যোগ"})
@app.route('/api/task/done',methods=['POST'])
def taskdone():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); tid=int(j.get('tid'))
    if tid in u["tasks"]: return jsonify({"msg":"এটা করা হয়েছে"})
    rw=int(db["settings"].get(f'task{tid}_reward','20')); u["tasks"].append(tid); u["balance"]+=rw; u["total"]+=1; tot=u["company"]+u["popup"]+len(u["tasks"]); u["badge"]=5 if tot>=50 else 4 if tot>=40 else 3 if tot>=25 else 2 if tot>=10 else 1
    save_db(db); return jsonify({"msg":f"✅ {rw} TK যোগ"})
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
    save_db(db); return jsonify({"msg":"✅ FINAL BIG SAVE - রং + বেজ + 5 ছবি সব সেভ"})

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#08080f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:100px}
.top{padding:12px 14px;display:flex;justify-content:space-between;align-items:center;background:#0c0c1a;position:sticky;top:0;z-index:99;border-bottom:1px solid #1a1a2e}
.card{margin:10px 12px;border-radius:22px;padding:14px;background:#14142a;border:1px solid #1e1e3a}
.btn{width:100%;padding:15px;border:none;border-radius:14px;font-weight:800;color:#fff;margin-top:10px;cursor:pointer;font-size:15px}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;z-index:99;border-top:1px solid #1e1e3a}
.btm div{flex:1;text-align:center;color:#6b6b8a;font-size:11px;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:24px;display:block}
input{width:100%;padding:14px;border-radius:14px;border:1px solid #2a2a4a;background:#0e0e20;color:#fff;margin-top:10px}
.page{display:none}.page.active{display:block}
.halkaDew{animation:dewGlow 4s ease-in-out infinite}
@keyframes dewGlow{0%{box-shadow:0 0 0px transparent}50%{box-shadow:0 0 22px #ffffff0d,0 0 35px #6d4cff1a}100%{box-shadow:0 0 0px transparent}}
.progressWrap{width:100%;height:8px;background:#00000060;border-radius:10px;margin-top:14px;overflow:hidden}
.progressBar{height:100%;width:0%;background:linear-gradient(90deg,#22c55e,#f59e0b);border-radius:10px;transition:width 1.2s ease}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #2a2a4a;border-radius:18px;padding:14px;margin:12px 0;cursor:pointer;position:relative}
.payCard.active{border-color:#e2136e;background:#1a1a35;box-shadow:0 0 15px #e2136e33}
.check{position:absolute;right:12px;width:24px;height:24px;background:#22c55e;border-radius:50%;display:none;align-items:center;justify-content:center}
.payCard.active.check{display:flex}
.slider{position:relative;width:100%;height:160px;border-radius:22px;overflow:hidden}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;opacity:0;transition:opacity 1s ease;background-size:cover;background-position:center}
.slide.active{opacity:1}
.dotWrap{display:flex;gap:6px;justify-content:center;margin-top:8px}
.dot{width:8px;height:8px;background:#ffffff40;border-radius:50%}
.dot.active{background:#fff;width:20px}
.avatarWrap{width:120px;height:120px;border-radius:50%;margin:0 auto;position:relative;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden}
.statGrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px}
.statBox{border-radius:16px;padding:14px;text-align:center}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:800;font-size:16px" id="appNameTop">Protidiner Kaj BD <span style="background:#22c55e;width:20px;height:20px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:12px">✓</span></div><div style="font-size:12px;color:#9ca3af" id="adminNameTop">Admin: SHIBLI NOMAN</div></div></div><div onclick="goPage('profile')" style="width:46px;height:46px;border-radius:50%;border:2px solid #6d4cff;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden;cursor:pointer"><img id="topAv" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="topAvT">👤</span></div></div>

<!-- HOME 1 - BIG FULL -->
<div id="p-home" class="page active">
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
<div class="card halkaDew" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4,#10b981);text-align:center;border:none;padding:22px"><div style="font-size:13px" id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:56px;font-weight:900;margin:8px 0" id="balMain">৳1120</div><div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap"><span style="background:#00000040;padding:6px 12px;border-radius:20px;font-size:12px" id="c1">Company 0/30</span><span style="background:#00000040;padding:6px 12px;border-radius:20px;font-size:12px" id="c2">Popup 0/20</span><span style="background:#00000040;padding:6px 12px;border-radius:20px;font-size:12px" id="c3">Total 0</span></div><div class="progressWrap"><div id="progressBar" class="progressBar"></div></div><div style="font-size:11px;margin-top:6px;opacity:.8" id="progTxt">0% Complete - Ads দেখলে বাড়বে</div></div>
<div class="card"><button class="btn" style="background:#7c3aed" onclick="doCompany()">📺 <span id="btnCTxt">COMPANY ADS (৳2) -</span> <span id="btnC">0/30</span></button><button class="btn" style="background:#16a34a" onclick="doPopup()">💰 <span id="btnPTxt">POPUP ADS (৳3) -</span> <span id="btnP">0/20</span></button><button class="btn" style="background:#1e293b" onclick="goPage('tasks')">📋 <span id="btnTTxt">TASK BONUS - 5 টা/দিন</span></button></div>
<div class="card halkaDew" style="border:1px solid #f59e0b"><div style="font-weight:800" id="offerT">🎉 আজকের স্পেশাল অফার</div><div style="font-size:13px;color:#9ca3af;margin-top:4px" id="offerD">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</div><button class="btn" style="background:linear-gradient(90deg,#f59e0b,#ef4444);margin-top:10px" onclick="alert('অফার - কাজ করে')">🎁 অফার নিন</button></div>
</div>

<!-- TASK 2 - BIG FULL -->
<div id="p-tasks" class="page">
<div class="card"><div style="font-weight:800;font-size:18px;margin-bottom:12px" id="taskTitle">📋 Task Bonus - দিনে 5 টা</div><div id="taskList"></div><div style="background:linear-gradient(135deg,#6d4cff,#4f46e5);border-radius:20px;padding:16px;margin-top:16px" class="halkaDew"><div style="font-weight:800;font-size:18px" id="referTitle">🎁 Refer & Earn ৳50</div><div style="background:#00000040;border-radius:12px;padding:10px;margin-top:10px;font-size:12px;word-break:break-all" id="refLink2">https://.../?ref=</div><button class="btn" style="background:#fff;color:#4f46e5" onclick="copyText('refLink2')">📋 লিংক কপি - কাজ করে</button></div><div style="background:linear-gradient(90deg,#0ea5e9,#0284c7);border-radius:20px;padding:16px;margin-top:14px;display:flex;justify-content:space-between;align-items:center" class="halkaDew"><div><div style="font-weight:800;font-size:17px" id="teleBoxTitle">📢 Telegram Channel</div><div style="font-size:11px;opacity:.9" id="teleBoxSub">আপডেট ও প্রুফ</div></div><button class="btn" style="width:auto;background:#fff;color:#0ea5e9;padding:10px 18px;border-radius:24px;margin:0" onclick="openLink('tele_box_link')">Join ✈️</button></div></div>
</div>

<!-- WALLET 3 - BIG FULL - সবুজ টিক দুইটাতেই -->
<div id="p-wallet" class="page">
<div class="card halkaDew" style="background:#1e293b;text-align:center;padding:24px"><div style="font-size:14px;color:#94a3b8" id="walletTitle">ব্যালেন্স</div><div style="font-size:52px;font-weight:900;margin:6px 0" id="wBal">৳1120</div><div style="font-size:13px;color:#94a3b8" id="walletMin">Min ৳500</div><div class="progressWrap"><div id="wProgress" class="progressBar"></div></div></div>
<div class="card"><div style="font-weight:800;font-size:18px;margin-bottom:12px" id="walletMethodTitle">💸 Withdraw Method</div><div id="bCard" class="payCard active" onclick="selectPay('bKash')"><div id="bLogo" style="width:56px;height:56px;background:#e2136e;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:24px">৳</div><div style="flex:1"><b id="bName">bKash</b><div style="font-size:12px;color:#94a3b8" id="bSub">Personal • Instant Payment</div></div><div class="check">✓</div></div><div id="nCard" class="payCard" onclick="selectPay('Nagad')"><div id="nLogo" style="width:56px;height:56px;background:#f59e0b;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:24px">৳</div><div style="flex:1"><b id="nName">Nagad</b><div style="font-size:12px;color:#94a3af" id="nSub">Personal • Fast Withdraw</div></div><div class="check">✓</div></div><input id="accNum" placeholder="01XXXXXXXXXXX"><input id="wdAmt" type="number" placeholder="500"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f59e0b)" onclick="doWithdraw()" id="wdBtn">🚀 Withdraw করুন - কাজ করে</button></div>
<div class="card" style="background:linear-gradient(135deg,#065f46,#047857);border:none"><div style="font-weight:800" id="ruleTitle">✅ Withdraw নিয়ম</div><div style="font-size:14px;margin-top:8px;line-height:24px"><span id="rule1">- মিনিমাম ৳500</span><br><span id="rule2">- Personal নাম্বার দিন</span><br><span id="rule3">- 24 ঘণ্টায় পেমেন্ট</span></div></div><div class="card"><div style="font-weight:800">📜 History</div><div id="wHist" style="font-size:13px;color:#94a3b8;margin-top:8px">কোনো Withdraw নেই</div></div>
</div>

<!-- SUPPORT 4 - BIG FULL -->
<div id="p-support" class="page">
<div class="card halkaDew" style="background:linear-gradient(135deg,#4f46e5,#6d4cff);text-align:center"><div style="background:#00000030;border-radius:20px;padding:12px;font-size:14px;font-weight:800" id="supTop">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:34px;margin-top:14px">💬</div><div style="font-size:22px;font-weight:900;margin-top:8px" id="supCenter">আমরা আছি আপনার পাশে</div><div style="font-size:12px;margin-top:6px;opacity:.9" id="supSub">২৪ ঘণ্টা সাপোর্ট • 100% Trusted • SHIBLI NOMAN Team</div></div>
<div class="card"><div style="font-weight:800;font-size:18px;margin-bottom:12px" id="quickT">🚀 দ্রুত যোগাযোগ করুন</div><div style="background:#0e0e20;border:2px solid #0ea5e9;padding:14px;border-radius:18px;display:flex;gap:12px;align-items:center;cursor:pointer" onclick="openLink('tele_sup_link')"><div style="width:52px;height:52px;background:#0ea5e9;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:28px">✈️</div><div style="flex:1"><b id="teleSupT">Telegram Support (Fast Reply)</b><div style="font-size:11px;color:#9ca3af" id="teleSupSub">2 মিনিটে রিপ্লাই • 9AM-12AM</div></div><div style="background:#334155;padding:6px 10px;border-radius:8px">➡️</div></div><div style="background:#0e0e20;padding:14px;border-radius:18px;display:flex;gap:12px;align-items:center;cursor:pointer;margin-top:10px" onclick="openLink('wa_sup_link')"><div style="width:52px;height:52px;background:#22c55e;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:28px">💬</div><div style="flex:1"><b id="waSupT">WhatsApp Support</b><div style="font-size:12px;color:#9ca3af" id="waSupNum">01XXXXXXXXXX</div></div><div style="background:#334155;padding:6px 10px;border-radius:8px">➡️</div></div><div style="background:#0e0e20;padding:14px;border-radius:18px;display:flex;gap:12px;align-items:center;cursor:pointer;margin-top:10px" onclick="openLink('email_sup_link')"><div style="width:52px;height:52px;background:#f59e0b;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:24px">📧</div><div style="flex:1"><b id="emailSupT">Email Support</b><div style="font-size:11px;color:#9ca3af" id="emailSupAddr">support@protidinerkajbd.com</div></div><div style="background:#334155;padding:6px 10px;border-radius:8px">➡️</div></div></div>
<div class="card"><div style="font-weight:800;font-size:18px" id="howWorkT">🎥 কিভাবে কাজ করবেন?</div><div style="background:#0a0a0a;border:2px solid #f59e0b;border-radius:18px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;margin-top:12px" onclick="openLink('tutorial_youtube_link')"><div style="width:80px;height:80px;background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:36px">▶️</div><div style="background:#f59e0b;color:#fff;padding:8px 16px;border-radius:20px;font-size:13px;font-weight:800;margin-top:14px" id="tutBtnT">Tutorial - 2 মিনিটে শিখুন</div><div style="font-size:11px;color:#9ca3af;margin-top:8px" id="tutClickT">▶️ Click করলে ভিডিও চলবে</div></div><div style="font-size:14px;margin-top:12px;line-height:26px;color:#cbd5e1"><span id="step1">Step 1: Ads দেখুন</span><br><span id="step2">Step 2: Task complete করুন</span><br><span id="step3">Step 3: ৳500 হলেই Withdraw</span></div></div>
</div>

<!-- PROFILE 5 - BIG FULL WITH COLOR CONTROL -->
<div id="p-profile" class="page">
<div class="card" id="profileCard" style="text-align:center;padding:20px"><div class="avatarWrap halkaDew" id="avatarWrap" onclick="openGal()"><img id="pAv" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="pAvT" style="font-size:64px">👤</span><div style="position:absolute;bottom:0;right:0;width:34px;height:34px;background:#6d4cff;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid #13132a">📸</div></div><div style="margin-top:14px"><b style="font-size:22px" id="pName">User 8385</b><div style="font-size:13px" id="pId">ID: 8807178385</div><div id="memberBadge" style="display:inline-block;padding:7px 16px;border-radius:20px;font-size:13px;font-weight:800;margin-top:8px">🏅 Bronze Member</div></div><input id="pNameIn" placeholder="আপনার নাম লিখুন" style="text-align:center;margin-top:16px"><button class="btn" style="background:linear-gradient(90deg,#6d4cff,#4f46e5);padding:16px" onclick="openGal()">📸 গ্যালারি থেকে ছবি নিন - কাজ করে</button><button class="btn" style="background:#22c55e;padding:16px" onclick="saveProf()">💾 Save Profile - কাজ করে</button><div style="font-size:11px;color:#6b7280;margin-top:8px">ছবিতে বা বাটনে ক্লিক → গ্যালারি খুলবে → Save দিন</div><input type="file" id="fileIn" accept="image/*" style="display:none" onchange="handleFile(this)"></div>
<div class="card" id="statsCard"><div style="font-weight:800;font-size:18px" id="statsTitle">📊 পরিসংখ্যান</div><div class="statGrid"><div class="statBox sBox"><div style="font-size:26px">💰</div><div style="font-size:18px;font-weight:900" id="sBal">৳1120</div><div style="font-size:11px;color:#9ca3af">ব্যালেন্স</div></div><div class="statBox sBox"><div style="font-size:24px">📺</div><div style="font-size:20px;font-weight:900" id="sAds">0</div><div style="font-size:11px;color:#9ca3af">Ads</div></div><div class="statBox sBox"><div style="font-size:24px">📋</div><div style="font-size:20px;font-weight:900" id="sTask">0</div><div style="font-size:11px;color:#9ca3af">Task</div></div><div class="statBox sBox"><div style="font-size:24px">👥</div><div style="font-size:20px;font-weight:900" id="sTotal">0</div><div style="font-size:11px;color:#9ca3af">Total Work</div></div><div class="statBox sBox"><div style="font-size:20px">📅</div><div style="font-size:16px;font-weight:900" id="sJoin">2026-09-13</div><div style="font-size:11px;color:#9ca3af">Join Date</div></div><div class="statBox sBox"><div style="font-size:12px;background:#a855f7;padding:2px 6px;border-radius:4px;display:inline-block">ID</div><div style="font-size:13px;font-weight:900;margin-top:4px" id="sUid">8807178385</div><div style="font-size:11px;color:#9ca3af">User ID</div></div></div></div>
<div class="card"><div style="font-weight:800;font-size:18px;margin-bottom:12px">⚙️ সেটিংস</div><div class="statBox sBox" style="display:flex;align-items:center;gap:12px;text-align:left;padding:14px;cursor:pointer" onclick="goPage('wallet')"><div style="width:48px;height:48px;background:#1a1a35;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px">💸</div><div style="flex:1"><b>Withdraw History</b><div style="font-size:11px;color:#9ca3af">আপনার পেমেন্ট দেখুন</div></div><div style="background:#334155;padding:6px 10px;border-radius:8px">➡️</div></div><div class="statBox sBox" style="display:flex;align-items:center;gap:12px;text-align:left;padding:14px;margin-top:10px"><div style="width:48px;height:48px;background:#1a1a35;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px">🔗</div><div style="flex:1"><b>My Refer Link</b><div style="font-size:10px;color:#9ca3af;word-break:break-all" id="myRef">https://.../?ref=</div></div><div style="background:#334155;padding:6px 10px;border-radius:8px;cursor:pointer" onclick="copyText('myRef')">📋</div></div></div>
<div class="card halkaDew" id="verifiedCard" style="text-align:center;padding:18px"><div style="font-size:18px;font-weight:900" id="verifiedTitle">🛡️ Verified User</div><div style="font-size:12px;margin-top:6px;opacity:.9" id="verifiedDesc">আপনার একাউন্ট 100% Safe • 24h Support</div></div>
<div class="card"><button class="btn" style="background:#ef4444" onclick="localStorage.clear();location.reload()">🚪 লগআউট - কাজ করে</button></div>
</div>

<div class="btm"><div id="n-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div><div id="n-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div><div id="n-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div><div id="n-support" onclick="goPage('support')"><span>💬</span>Support</div><div id="n-profile" onclick="goPage('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=localStorage.getItem('locked_phone')||'8807178385'; let tempImg=''; let settings={}; let method='bKash'; let curSlide=0;
function init(){ fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ settings=d.settings; let u=d.user; let total=u.company+u.popup; let pct=Math.min(Math.round((total/50)*100),100);
document.getElementById('appNameTop').innerHTML=settings.app_name+' <span style="background:#22c55e;width:20px;height:20px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:12px">'+settings.verified_txt+'</span>';
document.getElementById('adminNameTop').innerText='Admin: '+settings.admin_name;
for(let i=1;i<=5;i++){ let img=settings['slider_img'+i]; if(img){ document.getElementById('s'+i).style.backgroundImage='url('+img+')'; document.getElementById('s'+i).style.backgroundSize='cover'; } document.getElementById('st'+i).innerText=settings['slider_txt'+i]; }
document.getElementById('balTitle').innerText=settings.balance_title; document.getElementById('balMain').innerText='৳'+u.balance; document.getElementById('wBal').innerText='৳'+u.balance; document.getElementById('sBal').innerText='৳'+u.balance;
document.getElementById('c1').innerText='Company '+u.company+'/30'; document.getElementById('c2').innerText='Popup '+u.popup+'/20'; document.getElementById('c3').innerText='Total '+u.total; document.getElementById('btnCTxt').innerText=settings.company_btn; document.getElementById('btnPTxt').innerText=settings.popup_btn; document.getElementById('btnTTxt').innerText=settings.task_btn; document.getElementById('btnC').innerText=u.company+'/30'; document.getElementById('btnP').innerText=u.popup+'/20';
document.getElementById('progressBar').style.width=pct+'%'; document.getElementById('wProgress').style.width=pct+'%'; document.getElementById('progTxt').innerText=pct+'% Complete - '+total+' টা Ads';
document.getElementById('offerT').innerText=settings.offer_title; document.getElementById('offerD').innerText=settings.offer_desc;
document.getElementById('walletTitle').innerText=settings.wallet_bal_title; document.getElementById('walletMin').innerText=settings.wallet_min; document.getElementById('walletMethodTitle').innerText=settings.wallet_method_title; document.getElementById('bName').innerText=settings.bkash_name; document.getElementById('bSub').innerText=settings.bkash_sub; document.getElementById('nName').innerText=settings.nagad_name; document.getElementById('nSub').innerText=settings.nagad_sub; document.getElementById('wdBtn').innerText=settings.withdraw_btn; document.getElementById('ruleTitle').innerText=settings.rule_title; document.getElementById('rule1').innerText=settings.rule1; document.getElementById('rule2').innerText=settings.rule2; document.getElementById('rule3').innerText=settings.rule3;
if(settings.bkash_logo){ document.getElementById('bLogo').innerHTML='<img src='+settings.bkash_logo+' style=width:100%;height:100%;object-fit:cover;border-radius:16px>'; } if(settings.nagad_logo){ document.getElementById('nLogo').innerHTML='<img src='+settings.nagad_logo+' style=width:100%;height:100%;object-fit:cover;border-radius:16px>'; }
document.getElementById('supTop').innerText=settings.support_top_msg; document.getElementById('supCenter').innerText=settings.support_center_title; document.getElementById('supSub').innerText=settings.support_center_sub; document.getElementById('quickT').innerText=settings.quick_contact_title; document.getElementById('teleSupT').innerText=settings.tele_sup_title; document.getElementById('teleSupSub').innerText=settings.tele_sup_sub; document.getElementById('waSupT').innerText=settings.wa_sup_title; document.getElementById('waSupNum').innerText=settings.wa_sup_number; document.getElementById('emailSupT').innerText=settings.email_sup_title; document.getElementById('emailSupAddr').innerText=settings.email_sup_address; document.getElementById('howWorkT').innerText=settings.how_work_title; document.getElementById('tutBtnT').innerText=settings.tutorial_btn_text; document.getElementById('tutClickT').innerText=settings.tutorial_click_text; document.getElementById('step1').innerText=settings.step1; document.getElementById('step2').innerText=settings.step2; document.getElementById('step3').innerText=settings.step3;
// Profile Color
document.getElementById('profileCard').style.background=settings.profile_card_bg; document.getElementById('profileCard').style.borderColor=settings.profile_card_border; document.getElementById('avatarWrap').style.border='3px solid '+settings.avatar_border_color; document.getElementById('pName').style.color=settings.profile_name_color; document.getElementById('pId').style.color=settings.profile_id_color; document.querySelectorAll('.sBox').forEach(el=>{ el.style.background=settings.stats_card_bg; el.style.borderColor=settings.stats_border; }); document.getElementById('verifiedCard').style.background=settings.verified_bg;
let bIdx=u.badge||1; let badgeEl=document.getElementById('memberBadge'); badgeEl.innerText=settings['badge'+bIdx+'_icon']+' '+settings['badge'+bIdx+'_name']; badgeEl.style.background=settings['badge'+bIdx+'_bg']; badgeEl.style.color=settings['badge'+bIdx+'_text'];
document.getElementById('pName').innerText=u.name; document.getElementById('pId').innerText='ID: '+u.id; document.getElementById('sAds').innerText=total; document.getElementById('sTask').innerText=u.tasks.length; document.getElementById('sTotal').innerText=u.total; document.getElementById('sJoin').innerText=u.join; document.getElementById('sUid').innerText=u.id; document.getElementById('myRef').innerText=location.origin+'/?ref='+u.id; document.getElementById('refLink2').innerText=location.origin+'/?ref='+u.id; document.getElementById('pNameIn').value=u.name; document.getElementById('teleBoxTitle').innerText=settings.tele_box_title; document.getElementById('teleBoxSub').innerText=settings.tele_box_sub; document.getElementById('statsTitle').innerText=settings.stats_title; document.getElementById('verifiedTitle').innerText=settings.verified_title; document.getElementById('verifiedDesc').innerText=settings.verified_desc;
if(u.img){ document.getElementById('pAv').src=u.img; document.getElementById('pAv').style.display='block'; document.getElementById('pAvT').style.display='none'; document.getElementById('topAv').src=u.img; document.getElementById('topAv').style.display='block'; document.getElementById('topAvT').style.display='none'; tempImg=u.img; }
let taskHtml=''; for(let i=1;i<=5;i++){ let done=u.tasks.includes(i); taskHtml+=`<div style="display:flex;align-items:center;justify-content:space-between;background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:12px;margin:10px 0"><div style="display:flex;gap:12px;align-items:center"><div style="width:48px;height:48px;background:#6d4cff33;border-radius:12px;display:flex;align-items:center;justify-content:center">📋</div><div><b>${settings['task'+i+'_title']}</b><div style="font-size:11px;color:#9ca3af">${settings['task'+i+'_sub']}</div></div></div><button class="btn" style="width:auto;background:${done?'#22c55e':'#6d4cff'};padding:10px 18px;margin:0" onclick="doTask(${i})">${done?'✓':settings['task'+i+'_reward']+'৳'}</button></div>`; } document.getElementById('taskList').innerHTML=taskHtml; document.getElementById('taskTitle').innerText=settings.task_title; document.getElementById('referTitle').innerText=settings.refer_title;
let h=''; d.withdraws.slice(-5).reverse().forEach(w=>{ h+=`<div style="background:#0e0e20;padding:10px;border-radius:10px;margin-top:6px">💸 ${w.method} ৳${w.amt} - ${w.status} - ${w.time}</div>`; }); if(h) document.getElementById('wHist').innerHTML=h;
});}
function goPage(p){ document.querySelectorAll('.page').forEach(e=>e.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on')); document.getElementById('n-'+p).classList.add('on'); window.scrollTo(0,0);}
function doCompany(){ fetch('/api/reward?id='+uid+'&type=company').then(r=>r.json()).then(d=>{ alert(d.msg); init(); if(typeof show_11764581==='function') show_11764581(); });}
function doPopup(){ fetch('/api/reward?id='+uid+'&type=popup').then(r=>r.json()).then(d=>{ alert(d.msg); init(); if(typeof show_11764581==='function') show_11764581(); });}
function doTask(i){ let links={1:settings.task1_link,2:settings.task2_link,3:settings.task3_link,4:settings.tele_box_link}; if(links[i]) window.open(links[i],'_blank'); fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:i})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); });
