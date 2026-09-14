import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'

def load_db():
 if not os.path.exists(DB):
  d={"users":{},"withdraws":[],"settings":{
   "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN",
   # 1-5 Slider
   "slider1_txt":"🎉 Daily Bonus Available Today","slider1_bg":"linear-gradient(90deg,#FF9A00,#FF3D00)","slider1_img":"",
   "slider2_txt":"📢 Company Sponsored • 100% Safe","slider2_bg":"linear-gradient(90deg,#FF9A00,#FF3D00)","slider2_img":"",
   "slider3_txt":"🎁 50 Ads দেখলে ৳100 বোনাস!","slider3_bg":"linear-gradient(90deg,#FF9A00,#FF3D00)","slider3_img":"",
   "slider4_txt":"💰 100% Payment Guaranteed","slider4_bg":"linear-gradient(90deg,#FF9A00,#FF3D00)","slider4_img":"",
   "slider5_txt":"🔥 প্রতিদিন কাজ করুন - Unlimited Income","slider5_bg":"linear-gradient(90deg,#FF9A00,#FF3D00)","slider5_img":"",
   # Home
   "balance_title":"💰 আপনার বর্তমান ব্যালেন্স","special_title":"🎉 আজকের স্পেশাল অফার","special_desc":"প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!",
   "balance_card_bg":"linear-gradient(135deg,#2a5bff,#00d1b2)",
   # Task Page Links
   "task_tele_link":"https://t.me/","task_yt_link":"https://youtube.com/","task_fb_link":"https://facebook.com/","tele_channel_link":"https://t.me/ProtidinerKajBD",
   # Wallet - Logo Change Admin থেকে
   "bkash_logo":"","nagad_logo":"","bkash_name":"bKash","nagad_name":"Nagad","min_withdraw":"500",
   # Support
   "tele_support_link":"https://t.me/","wa_number":"01XXXXXXXXXX","wa_link":"https://wa.me/8801","email_support":"support@protidinerkajbd.com","tutorial_link":"https://youtube.com/","tutorial_thumb":"",
   # Locking System
   "lock_vpn":"on","lock_multi_account":"on","lock_emulator":"on","ads_limit_company":"30","ads_limit_popup":"20",
   # Profile Colors
   "profile_card_bg":"#14142a","profile_card_border":"#1e1e3a","avatar_border":"#6d4cff","verified_bg":"linear-gradient(135deg,#065f46,#047857)",
   "badge1_name":"Bronze Member","badge1_bg":"#6d4cff","badge1_text":"#fff","badge1_icon":"🏅",
   "badge2_name":"Silver Member","badge2_bg":"#9ca3af","badge2_text":"#000","badge2_icon":"🥈",
   "badge3_name":"Gold Member","badge3_bg":"#f59e0b","badge3_text":"#000","badge3_icon":"🥇",
   "badge4_name":"Platinum Member","badge4_bg":"#06b6d4","badge4_text":"#fff","badge4_icon":"💎",
   "badge5_name":"Diamond Member","badge5_bg":"#e2136e","badge5_text":"#fff","badge5_icon":"👑",
   "zone_id":"11764581"
  }}
  open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2));return d
 return json.load(open(DB,'r',encoding='utf-8'))

def save_db(d):open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
 uid=str(uid);today=str(datetime.now().date())
 if uid not in db["users"]:
  db["users"][uid]={"id":uid,"name":"User 8385","balance":1120,"company":0,"popup":0,"total":0,"tasks":[],"img":"","join":"2026-09-13","last":today}
 u=db["users"][uid]
 if u.get("last")!=today:u["company"]=0;u["popup"]=0;u["last"]=today
 tot=u["company"]+u["popup"]+len(u["tasks"])
 u["badge"]=5 if tot>=50 else 4 if tot>=40 else 3 if tot>=25 else 2 if tot>=10 else 1
 u["total"]=tot
 return u

@app.route('/')
def home():return render_template_string(HTML)
@app.route('/admin')
def admin_page():
 if request.args.get('id')!='8807178385':return "Admin: /admin?id=8807178385"
 return render_template_string(ADMIN)
@app.route('/api/get')
def api_get():db=load_db();u=get_user(db,request.args.get('id','8807178385'));save_db(db);return jsonify({"user":u,"settings":db["settings"],"withdraws":db["withdraws"]})
@app.route('/api/reward')
def reward():db=load_db();u=get_user(db,request.args.get('id'));t=request.args.get('type','company');limit=int(db["settings"]["ads_limit_company"]) if t=='company' else int(db["settings"]["ads_limit_popup"]);cur=u["company"] if t=='company' else u["popup"];
 if cur>=limit:return jsonify({"msg":"Limit"})
 u["company"]+=1 if t=='company' else 0;u["popup"]+=1 if t!='company' else 0;u["balance"]+=2 if t=='company' else 3;save_db(db);return jsonify({"ok":1})
@app.route('/api/task/done',methods=['POST'])
def td():db=load_db();j=request.json;u=get_user(db,j.get('id'));tid=str(j.get('tid'));amt=int(j.get('amt',20));u["tasks"].append(tid) if tid not in u["tasks"] else None;u["balance"]+=amt;save_db(db);return jsonify({"msg":f"✅ ৳{amt} Bonus যোগ হয়েছে"})
@app.route('/api/withdraw',methods=['POST'])
def wd():db=load_db();j=request.json;u=get_user(db,j.get('id'));amt=int(j.get('amt',0));mini=int(db["settings"]["min_withdraw"])
 if u["balance"]<amt:return jsonify({"msg":"❌ ব্যালেন্স কম"})
 if amt<mini:return jsonify({"msg":f"❌ মিনিমাম ৳{mini}"})
 u["balance"]-=amt;db["withdraws"].append({"uid":str(u["id"]),"amt":amt,"num":j.get('num'),"method":j.get('method'),"status":"Pending","time":str(datetime.now())[:16]});save_db(db);return jsonify({"msg":f"✅ {j.get('method')} এ ৳{amt} Request গেছে"})
@app.route('/api/profile/save',methods=['POST'])
def ps():db=load_db();j=request.json;u=get_user(db,j.get('id'));u["name"]=j.get('name',u["name"]);u["img"]=j.get('img',u["img"]);save_db(db);return jsonify({"msg":"✅ Save Profile হয়েছে"})
@app.route('/api/admin/save',methods=['POST'])
def asave():db=load_db();j=request.json;db["settings"].update(j);save_db(db);return jsonify({"msg":"✅ সব SAVE হয়েছে - 1 থেকে 5 পর্যন্ত"})

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#000;color:#fff;max-width:430px;margin:0 auto;padding-bottom:110px}
.header{background:#0a0a18;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:99}
.bottomNav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;justify-content:space-around;padding:10px 0 14px;border-radius:24px 24px 0 0;z-index:99}
.navItem{text-align:center;color:#6b7280;font-size:11px;cursor:pointer}.navItem.active{color:#fff}.navItem span{font-size:24px;display:block}
.page{display:none}.page.active{display:block}
.dotWrap{display:flex;gap:6px;justify-content:center;margin-top:10px}.dot{width:8px;height:8px;background:#fff4;border-radius:50%}.dot.active{background:#fff;width:22px}
.slider{height:130px;border-radius:24px;display:flex;align-items:center;justify-content:center;font-weight:800;position:relative;overflow:hidden}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;transition:1s;background-size:cover;background-position:center}.slide.active{opacity:1}
.balanceCard{border-radius:24px;padding:20px;text-align:center;margin:12px}
.btn{width:100%;padding:16px;border:none;border-radius:16px;font-weight:800;color:#fff;margin:7px 0;cursor:pointer}
.btn-purple{background:#6d28d9}.btn-green{background:#16a34a}.btn-dark{background:#232336}
.taskContainer{background:#0f0f1f;border-radius:24px;padding:12px;margin:12px;border:1px solid #1e1e2e}
.taskRow{display:flex;align-items:center;justify-content:space-between;background:#17172a;border:1px solid #22223a;border-radius:16px;padding:12px 14px;margin:10px 0}
.referBox{background:linear-gradient(135deg,#6d28d9,#7c3aed);border-radius:20px;padding:16px;margin:12px}
.teleBox{background:linear-gradient(90deg,#0ea5e9,#0284c7);border-radius:20px;padding:16px;margin:12px;display:flex;justify-content:space-between;align-items:center}
.walletBalanceCard{background:linear-gradient(135deg,#1e293b,#2d3a4f);border-radius:24px;padding:24px;text-align:center;margin:12px;border:1px solid #1e293b}
.methodCard{display:flex;align-items:center;gap:12px;background:#1a1a30;border:2px solid #25253d;border-radius:16px;padding:14px;margin:10px 0;cursor:pointer}
.methodCard.active{border-color:#e2136e}.methodIcon{width:52px;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900}
.supportTopBox{background:linear-gradient(135deg,#6d28d9,#4f46e5);border-radius:24px;padding:20px;margin:12px;text-align:center}
.contactRow{display:flex;align-items:center;gap:12px;background:#1a1a30;border:1.5px solid #25253d;border-radius:16px;padding:14px;margin:10px 0}
.videoBox{background:#000;border:2px solid #ff8c00;border-radius:20px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer}
.profileTopCard{background:linear-gradient(180deg,#162040,#0f172a);border-radius:24px;padding:20px;margin:12px;border:1px solid #1e293b;text-align:center}
.avatarWrap{width:120px;height:120px;border-radius:50%;margin:0 auto;position:relative;border:3px solid #6d4cff;display:flex;align-items:center;justify-content:center;background:#0f172a;overflow:hidden}
.statsGrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px}
.statCard{background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;text-align:center}
</style></head><body>
<div class="header"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:900" id="appName">Protidiner Kaj BD ✓</div><div style="font-size:11px;color:#9ca3af" id="adminName">Admin: SHIBLI NOMAN</div></div></div><div style="width:42px;height:42px;border-radius:50%;background:#1e1e3a;border:2px solid #6d4cff;display:flex;align-items:center;justify-content:center;overflow:hidden" onclick="goP('profile')"><img id="topAv" style="display:none;width:100%;height:100%;object-fit:cover"><span id="topAvI">👤</span></div></div>

<!-- HOME -->
<div id="p-home" class="page active">
<div style="position:relative;margin:12px"><div id="s1" class="slide active"></div><div id="s2" class="slide"></div><div id="s3" class="slide"></div><div id="s4" class="slide"></div><div id="s5" class="slide"></div><div style="height:130px"></div><div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div></div>
<div class="balanceCard" id="balCard"><div style="font-size:13px" id="balTitle">💰 আপনার বর্তমান ব্যালেন্স</div><div style="font-size:56px;font-weight:900;margin:6px 0" id="bal">৳1120</div><div style="display:flex;gap:6px;justify-content:center"><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bC">Company 0/30</span><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bP">Popup 0/20</span><span style="background:#0004;padding:6px 10px;border-radius:20px;font-size:12px" id="bT">Total 0</span></div></div>
<div style="background:#15151f;border-radius:24px;padding:14px;margin:12px"><button class="btn btn-purple" onclick="doR('company')">📺 COMPANY ADS (৳2) - <span id="btnC">0/30</span></button><button class="btn btn-green" onclick="doR('popup')">💰 POPUP ADS (৳3) - <span id="btnP">0/20</span></button><button class="btn btn-dark" onclick="goP('tasks')">📋 TASK BONUS - 5 টা/দিন</button></div>
<div style="border:2px solid #f59e0b;border-radius:20px;padding:14px;margin:12px;background:#12121e"><div style="font-weight:800" id="spT">🎉 আজকের স্পেশাল অফার</div><div style="font-size:13px;color:#9ca3af;margin-top:4px" id="spD">প্রথম 100 জন 50 টা Ads দেখলে ৳100 বোনাস!</div></div>
</div>

<!-- TASK - 2nd Page -->
<div id="p-tasks" class="page"><div class="taskContainer"><div style="font-size:20px;font-weight:900">📋 Task Bonus - দিনে 5 টা</div><div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;background:#0ea5e922;border-radius:12px;display:flex;align-items:center;justify-content:center">✈️</div><div><b>Telegram Channel Join</b><div style="font-size:12px;color:#9ca3af">চ্যানেলে জয়েন • ৳25</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('tele',25)">৳25</button></div><div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;background:#f59e0b22;border-radius:12px;display:flex;align-items:center;justify-content:center">▶️</div><div><b>YouTube Subscribe</b><div style="font-size:12px;color:#9ca3af">সাবস্ক্রাইব • ৳30</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('yt',30)">৳30</button></div><div class="taskRow"><div style="display:flex;gap:12px;align-items:center"><div style="width:44px;height:44px;background:#22c55e22;border-radius:12px;display:flex;align-items:center;justify-content:center">👍</div><div><b>Facebook Page Like</b><div style="font-size:12px;color:#9ca3af">লাইক • ৳20</div></div></div><button style="background:#6d4cff;color:#fff;border:none;padding:10px 18px;border-radius:12px;font-weight:800" onclick="doTask('fb',20)">৳20</button></div></div><div class="referBox"><div style="font-size:18px;font-weight:900">🎁 Refer & Earn ৳50</div><div style="background:#2a1a6a;border-radius:12px;padding:10px;font-size:12px;margin-top:10px;word-break:break-all" id="refLinkTask">https://...</div><button style="background:#fff;color:#4c1d95;border:none;width:100%;padding:12px;border-radius:12px;font-weight:900;margin-top:10px" onclick="copyRef()">📋 লিংক কপি</button></div><div class="teleBox"><div><div style="font-size:18px;font-weight:900">📢 Telegram Channel</div><div style="font-size:12px">আপডেট ও প্রুফ</div></div><button style="background:#fff;color:#0ea5e9;border:none;padding:10px 18px;border-radius:20px;font-weight:800" onclick="window.open('https://t.me/','_blank')">Join ✈️</button></div></div>

<!-- WALLET - 3rd Page -->
<div id="p-wallet" class="page"><div class="walletBalanceCard"><div style="font-size:13px;color:#94a3b8">ব্যালেন্স</div><div style="font-size:56px;font-weight:900" id="wBal">৳1120</div><div style="font-size:13px;color:#94a3b8">Min <span id="minW">৳500</span></div></div><div style="background:#131326;border-radius:24px;padding:16px;margin:12px"><div style="font-size:18px;font-weight:900">💸 Withdraw Method</div><div id="bkCard" class="methodCard active" onclick="selPay('bKash')"><div class="methodIcon" style="background:#e2136e" id="bkIconWrap"><img id="bkLogo" style="width:32px;height:32px;object-fit:contain;display:none"><span id="bkTxt">৳</span></div><div><b id="bkName">bKash</b><div style="font-size:11px;color:#9ca3af">Personal</div></div><div style="margin-left:auto;color:#22c55e">✓</div></div><div id="ngCard" class="methodCard" onclick="selPay('Nagad')"><div class="methodIcon" style="background:#ff8c00" id="ngIconWrap"><img id="ngLogo" style="width:32px;height:32px;object-fit:contain;display:none"><span id="ngTxt">৳</span></div><div><b id="ngName">Nagad</b><div style="font-size:11px;color:#9ca3af">Fast</div></div></div><input id="accNum" style="width:100%;background:#0e0e20;border:1px solid #333;border-radius:12px;padding:14px;color:#fff;margin:8px 0" placeholder="01XXXXXXXXXX"><input id="wdAmt" type="number" style="width:100%;background:#0e0e20;border:1px solid #333;border-radius:12px;padding:14px;color:#fff" placeholder="500"><button style="width:100%;background:linear-gradient(90deg,#e2136e,#ff8c00);border:none;border-radius:14px;padding:16px;font-weight:900;color:#fff;margin-top:12px" onclick="doWd()">🚀 Withdraw করুন</button></div><div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:16px;margin:12px"><div style="font-weight:900">✅ Withdraw নিয়ম</div><div style="font-size:13px;margin-top:6px;line-height:1.8">- মিনিমাম <span id="minTxt">৳500</span><br>- Personal নাম্বার<br>- 24 ঘণ্টায় পেমেন্ট</div></div><div style="background:#131326;border-radius:20px;padding:16px;margin:12px"><div style="font-weight:900">📜 History</div><div id="wdHist" style="font-size:13px;color:#9ca3af;margin-top:8px">কোনো Withdraw নেই</div></div></div>

<!-- SUPPORT - 4th Page -->
<div id="p-support" class="page"><div class="supportTopBox"><div style="background:#0003;border-radius:50px;padding:10px 16px;font-size:13px;display:inline-block">💬 যেকোনো প্রয়োজনে এডমিনের সাথে যোগাযোগ করুন</div><div style="font-size:36px;margin:10px 0">💬</div><div style="font-size:22px;font-weight:900">আমরা আছি আপনার পাশে</div><div style="font-size:13px;opacity:.8;margin-top:6px">২৪ ঘণ্টা সাপোর্ট • 100% Trusted • SHIBLI NOMAN Team</div></div><div style="background:#131326;border-radius:20px;padding:14px;margin:12px"><div style="font-weight:900">🚀 দ্রুত যোগাযোগ করুন</div><div class="contactRow" style="border-color:#0ea5e9" onclick="window.open(document.getElementById('teleLink').value||'https://t.me/','_blank')"><div style="width:52px;height:52px;background:#0ea5e9;border-radius:14px;display:flex;align-items:center;justify-content:center">✈️</div><div><b>Telegram Support (Fast Reply)</b><div style="font-size:12px;color:#9ca3af">2 মিনিটে রিপ্লাই • 9AM-12AM</div></div><div style="margin-left:auto">➡️</div></div><div class="contactRow" onclick="window.open('https://wa.me/'+document.getElementById('waNum').value,'_blank')"><div style="width:52px;height:52px;background:#22c55e;border-radius:14px;display:flex;align-items:center;justify-content:center">💬</div><div><b>WhatsApp Support</b><div style="font-size:12px;color:#9ca3af" id="waNumTxt">01XXXXXXXXXX</div></div><div style="margin-left:auto">➡️</div></div><div class="contactRow" onclick="location.href='mailto:'+document.getElementById('emailSup').value"><div style="width:52px;height:52px;background:#f59e0b;border-radius:14px;display:flex;align-items:center;justify-content:center">📧</div><div><b>Email Support</b><div style="font-size:12px;color:#9ca3af" id="emailTxt">support@...</div></div><div style="margin-left:auto">➡️</div></div></div><div style="background:#131326;border-radius:20px;padding:16px;margin:12px"><div style="font-weight:900">🎥 কিভাবে কাজ করবেন?</div><div class="videoBox" onclick="window.open(document.getElementById('tutLink').value||'https://youtube.com/','_blank')"><div style="width:78px;height:78px;background:linear-gradient(135deg,#ff8c00,#f59e0b);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:36px">▶️</div><div style="background:#ff8c00;color:#fff;padding:8px 18px;border-radius:20px;font-weight:800;margin-top:14px">Tutorial - 2 মিনিটে শিখুন</div><div style="font-size:12px;color:#9ca3af;margin-top:6px">Click করলে ভিডিও চলবে</div></div><div style="font-size:13px;margin-top:10px;line-height:1.8">Step 1: Ads দেখুন<br>Step 2: Task complete করুন<br>Step 3: ৳500 হলেই Withdraw</div></div><div style="background:#131326;border-radius:20px;padding:16px;margin:12px"><div style="font-weight:900">❓ FAQ</div><div style="background:#1a1a30;border:1px solid #25253d;border-radius:12px;padding:12px;margin:8px 0"><b>Q: টাকা কখন পাবো?</b><div style="font-size:12px;color:#9ca3af">A: 24 ঘণ্টার মধ্যে bKash/Nagad এ।</div></div><div style="background:#1a1a30;border:1px solid #25253d;border-radius:12px;padding:12px;margin:8px 0"><b>Q: VPN চলবে?</b><div style="font-size:12px;color:#9ca3af">A: না, ব্যান হবে।</div></div><div style="background:#1a1a30;border:1px solid #25253d;border-radius:12px;padding:12px;margin:8px 0"><b>Q: 1 ফোনে কয়টা একাউন্ট?</b><div style="font-size:12px;color:#9ca3af">A: 1 টা।</div></div><div style="background:#1a1a30;border:1px solid #25253d;border-radius:12px;padding:12px;margin:8px 0"><b>Q: Refer বোনাস?</b><div style="font-size:12px;color:#9ca3af">A: 1 জন = ৳50 সাথে সাথে।</div></div></div><div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px;text-align:center"><div style="font-weight:900;font-size:18px">🛡️ 100% Trusted</div><div style="font-size:12px;margin-top:4px">50k+ ইউজার, 100% পেমেন্ট গ্যারান্টি। সমস্যা হলে Telegram এ মেসেজ দিন।</div></div></div>

<!-- PROFILE - 5th Page -->
<div id="p-profile" class="page"><div class="profileTopCard" id="pCard"><div class="avatarWrap" id="avWrap" onclick="openGallery()"><img id="avImg" style="display:none;width:100%;height:100%;object-fit:cover"><span id="avIcon" style="font-size:60px">👤</span><div style="position:absolute;bottom:0;right:5px;width:30px;height:30px;background:#1e293b;border:2px solid #6d4cff;border-radius:50%;display:flex;align-items:center;justify-content:center">📸</div></div><div style="font-size:20px;font-weight:800;margin-top:12px" id="pNameTop">User 8385</div><div style="font-size:12px;color:#9ca3af" id="pIdTop">ID: 8807178385</div><div style="background:#6d4cff;color:#fff;padding:6px 14px;border-radius:20px;font-size:13px;display:inline-block;margin-top:8px" id="badge">🏅 Bronze Member</div><input id="nameIn" style="width:100%;background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:14px;color:#fff;margin-top:14px;text-align:center" placeholder="আপনার নাম লিখুন"><button style="width:100%;background:#6d4cff;border:none;border-radius:14px;padding:14px;color:#fff;font-weight:800;margin-top:10px" onclick="openGallery()">📸 গ্যালারি থেকে ছবি নিন</button><button style="width:100%;background:#22c55e;border:none;border-radius:14px;padding:14px;color:#fff;font-weight:800;margin-top:10px" onclick="saveProfile()">💾 Save Profile</button><div style="font-size:11px;color:#64748b;margin-top:6px">ছবিতে বা বাটনে ক্লিক → গ্যালারি খুলবে → Save দিন</div><input type="file" id="fileIn" accept="image/*" style="display:none" onchange="handleFile(this)"></div><div style="background:#131326;border-radius:20px;padding:16px;margin:12px"><div style="font-weight:900">📊 পরিসংখ্যান</div><div class="statsGrid"><div class="statCard"><div style="font-size:20px">💰</div><div style="font-weight:900" id="sBal">৳1120</div><div style="font-size:11px;color:#9ca3af">ব্যালেন্স</div></div><div class="statCard"><div style="font-size:20px">📺</div><div style="font-weight:900" id="sAds">0</div><div style="font-size:11px;color:#9ca3af">Ads</div></div><div class="statCard"><div style="font-size:20px">📋</div><div style="font-weight:900" id="sTask">0</div><div style="font-size:11px;color:#9ca3af">Task</div></div><div class="statCard"><div style="font-size:20px">👥</div><div style="font-weight:900">0</div><div style="font-size:11px;color:#9ca3af">Total Work</div></div><div class="statCard"><div>📅</div><div style="font-weight:900;font-size:14px" id="sDate">2026-09-13</div><div style="font-size:11px;color:#9ca3af">Join Date</div></div><div class="statCard"><div style="background:#a855f7;padding:2px 6px;border-radius:4px;font-size:10px;display:inline-block">ID</div><div style="font-weight:900;font-size:11px;margin-top:4px" id="sId">8807178385</div><div style="font-size:11px;color:#9ca3af">User ID</div></div></div></div><div style="background:#131326;border-radius:20px;padding:16px;margin:12px"><div style="font-weight:900">⚙️ সেটিংস</div><div style="display:flex;gap:12px;align-items:center;background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;margin:10px 0" onclick="goP('wallet')"><div style="width:48px;height:48px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center">💸</div><div><b>Withdraw History</b><div style="font-size:12px;color:#9ca3af">আপনার পেমেন্ট দেখুন</div></div><div style="margin-left:auto">➡️</div></div><div style="display:flex;gap:12px;align-items:center;background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;margin:10px 0" onclick="copyRef()"><div style="width:48px;height:48px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center">🔗</div><div style="flex:1"><b>My Refer Link</b><div style="font-size:10px;color:#9ca3af;word-break:break-all" id="refLink">https://...</div></div><div>📋</div></div><div style="display:flex;gap:12px;align-items:center;background:#1a1a30;border:1px solid #25253d;border-radius:14px;padding:14px;margin:10px 0"><div style="width:48px;height:48px;background:#1e293b;border-radius:12px;display:flex;align-items:center;justify-content:center">⭐</div><div><b>App Rate করুন</b><div style="font-size:12px;color:#9ca3af">5 Star দিন</div></div><div style="margin-left:auto">➡️</div></div></div><div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:20px;padding:18px;margin:12px;text-align:center"><div style="font-weight:900">🛡️ Verified User</div><div style="font-size:12px;margin-top:4px">আপনার একাউন্ট 100% Safe • 24h Support</div></div></div>

<div class="bottomNav"><div class="navItem active" id="n-home" onclick="goP('home')"><span>🏠</span>Home</div><div class="navItem" id="n-tasks" onclick="goP('tasks')"><span>📋</span>Task</div><div class="navItem" id="n-wallet" onclick="goP('wallet')"><span>💰</span>Wallet</div><div class="navItem" id="n-support" onclick="goP('support')"><span>💬</span>Support</div><div class="navItem" id="n-profile" onclick="goP('profile')"><span>👤</span>Profile</div></div>

<!-- Hidden Admin Inputs for Links -->
<div style="display:none"><input id="teleLink"><input id="waNum"><input id="emailSup"><input id="tutLink"></div>

<script>
let uid='8807178385',method='bKash',tempImg='',cur=0,set={};
function goP(p){document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));document.getElementById('p-'+p).classList.add('active');document.querySelectorAll('.navItem').forEach(e=>e.classList.remove('active'));document.getElementById('n-'+p).classList.add('active');}
function init(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{set=d.settings;let u=d.user;
document.getElementById('appName').innerText=set.app_name+' ✓';document.getElementById('adminName').innerText='Admin: '+set.admin_name;
for(let i=1;i<=5;i++){let s=document.getElementById('s'+i);let bg=set['slider'+i+'_bg'];let txt=set['slider'+i+'_txt'];let img=set['slider'+i+'_img'];s.innerText=txt;if(bg)s.style.background=bg;if(img){s.style.backgroundImage='url('+img+')';s.style.backgroundSize='cover';}}
document.getElementById('balCard').style.background=set.balance_card_bg;document.getElementById('balTitle').innerText=set.balance_title;document.getElementById('spT').innerText=set.special_title;document.getElementById('spD').innerText=set.special_desc;
document.getElementById('bal').innerText='৳'+u.balance;document.getElementById('wBal').innerText='৳'+u.balance;document.getElementById('sBal').innerText='৳'+u.balance;document.getElementById('bC').innerText='Company '+u.company+'/'+set.ads_limit_company;document.getElementById('bP').innerText='Popup '+u.popup+'/'+set.ads_limit_popup;document.getElementById('bT').innerText='Total '+(u.company+u.popup);document.getElementById('btnC').innerText=u.company+'/'+set.ads_limit_company;document.getElementById('btnP').innerText=u.popup+'/'+set.ads_limit_popup;document.getElementById('sAds').innerText=u.company+u.popup;document.getElementById('sTask').innerText=u.tasks.length;document.getElementById('sDate').innerText=u.join;document.getElementById('sId').innerText=u.id;document.getElementById('pNameTop').innerText=u.name;document.getElementById('pIdTop').innerText='ID: '+u.id;document.getElementById('nameIn').value=u.name;let b=u.badge||1;document.getElementById('badge').innerText=set['badge'+b+'_icon']+' '+set['badge'+b+'_name'];document.getElementById('badge').style.background=set['badge'+b+'_bg'];document.getElementById('badge').style.color=set['badge'+b+'_text'];document.getElementById('pCard').style.background=set.profile_card_bg;document.getElementById('avWrap').style.borderColor=set.avatar_border;
if(u.img){document.getElementById('avImg').src=u.img;document.getElementById('avImg').style.display='block';document.getElementById('avIcon').style.display='none';document.getElementById('topAv').src=u.img;document.getElementById('topAv').style.display='block';document.getElementById('topAvI').style.display='none';tempImg=u.img;}
let link='https://telegram-bot-1-v77g.onrender.com/?ref='+u.id;document.getElementById('refLink').innerText=link;document.getElementById('refLinkTask').innerText=link;
document.getElementById('bkName').innerText=set.bkash_name;document.getElementById('ngName').innerText=set.nagad_name;if(set.bkash_logo){document.getElementById('bkLogo').src=set.bkash_logo;document.getElementById('bkLogo').style.display='block';document.getElementById('bkTxt').style.display='none';}if(set.nagad_logo){document.getElementById('ngLogo').src=set.nagad_logo;document.getElementById('ngLogo').style.display='block';document.getElementById('ngTxt').style.display='none';}
document.getElementById('minW').innerText='৳'+set.min_withdraw;document.getElementById('minTxt').innerText='৳'+set.min_withdraw;
document.getElementById('teleLink').value=set.tele_support_link;document.getElementById('waNum').value=set.wa_number;document.getElementById('emailSup').value=set.email_support;document.getElementById('tutLink').value=set.tutorial_link;document.getElementById('waNumTxt').innerText=set.wa_number;document.getElementById('emailTxt').innerText=set.email_support;
let hist=d.withdraws.filter(w=>w.uid==uid);let hEl=document.getElementById('wdHist');if(hist.length>0){hEl.innerHTML=hist.map(h=>`<div style="background:#0e0e20;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between"><span>${h.method} - ৳${h.amt}</span><span style="color:#f59e0b">${h.status}</span></div>`).join('');}
});}
function doR(t){fetch('/api/reward?id='+uid+'&type='+t).then(()=>{init();if(typeof show_11764581==='function')show_11764581();});}
function doTask(id,amt){fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:id,amt:amt})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function selPay(m){method=m;document.getElementById('bkCard').classList.toggle('active',m=='bKash');document.getElementById('ngCard').classList.toggle('active',m=='Nagad');}
function doWd(){let num=document.getElementById('accNum').value;let amt=document.getElementById('wdAmt').value;if(!num||!amt){alert('নাম্বার ও টাকা দিন');return;}fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:method})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function openGallery(){document.getElementById('fileIn').click();}
function handleFile(inp){let f=inp.files[0];let r=new FileReader();r.onload=e=>{tempImg=e.target.result;document.getElementById('avImg').src=tempImg;document.getElementById('avImg').style.display='block';document.getElementById('avIcon').style.display='none';document.getElementById('topAv').src=tempImg;document.getElementById('topAv').style.display='block';document.getElementById('topAvI').style.display='none';};r.readAsDataURL(f);}
function saveProfile(){let n=document.getElementById('nameIn').value;fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:tempImg})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
function copyRef(){let t=document.getElementById('refLink').innerText;navigator.clipboard.writeText(t);alert('✅ কপি হয়েছে');}
setInterval(()=>{cur=(cur+1)%5;for(let i=1;i<=5;i++){let s=document.getElementById('s'+i);let d=document.getElementById('d'+i);if(s)s.classList.toggle('active',i-1==cur);if(d)d.classList.toggle('active',i-1==cur);}},3000);
init();
</script></body></html>
"""

ADMIN="""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>body{background:#070710;color:#fff;max-width:900px;margin:0 auto;padding:12px;font-family:system-ui}.card{background:#15152a;border-radius:14px;padding:14px;margin:12px 0;border:1px solid #222}input{width:100%;padding:10px;border-radius:10px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:6px}input[type=color]{height:48px}label{font-size:11px;color:#aaa;margin-top:10px;display:block;font-weight:700}.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}.btn{width:100%;padding:16px;background:linear-gradient(90deg,#6d4cff,#e2136e);border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:16px;cursor:pointer}h3{color:#f59e0b}</style></head><body>
<h2 style="text-align:center">👑 FINAL ADMIN - 1 থেকে 5 + Logo + Locking</h2>

<div class="card" style="border:2px solid #f59e0b"><h3>🎠 1 - Slider 1 থেকে 5 (Text + BG + Image URL)</h3>
<label>1 Text</label><input id="slider1_txt"><label>1 BG Color/Gradient</label><input id="slider1_bg"><label>1 Image URL (যদি ছবি দিতে চান)</label><input id="slider1_img">
<label>2 Text</label><input id="slider2_txt"><label>2 BG</label><input id="slider2_bg"><label>2 Image URL</label><input id="slider2_img">
<label>3 Text</label><input id="slider3_txt"><label>3 BG</label><input id="slider3_bg"><label>3 Image URL</label><input id="slider3_img">
<label>4 Text</label><input id="slider4_txt"><label>4 BG</label><input id="slider4_bg"><label>4 Image URL</label><input id="slider4_img">
<label>5 Text</label><input id="slider5_txt"><label>5 BG</label><input id="slider5_bg"><label>5 Image URL</label><input id="slider5_img">
</div>

<div class="card" style="border:2px solid #06b6d4"><h3>💰 2 - Home Balance + Special</h3>
<label>Balance Title</label><input id="balance_title"><label>Balance Card BG</label><input id="balance_card_bg"><label>Special Title</label><input id="special_title"><label>Special Desc</label><input id="special_desc">
<div class="row"><div><label>Company Ads Limit</label><input id="ads_limit_company"></div><div><label>Popup Ads Limit</label><input id="ads_limit_popup"></div></div>
</div>

<div class="card" style="border:2px solid #e2136e"><h3>💸 3 - Wallet - bKash/Nagad Logo পরিবর্তন Admin থেকে</h3>
<div class="row"><div><label>bKash Name</label><input id="bkash_name"></div><div><label>Nagad Name</label><input id="nagad_name"></div></div>
<label>bKash Logo URL (PNG লিংক দিন - Admin থেকে চেঞ্জ হবে)</label><input id="bkash_logo" placeholder="https://.../bkash.png">
<label>Nagad Logo URL</label><input id="nagad_logo" placeholder="https://.../nagad.png">
<label>Min Withdraw</label><input id="min_withdraw">
</div>

<div class="card" style="border:2px solid #22c55e"><h3>💬 4 - Support - Telegram/WhatsApp/Email/Tutorial Link</h3>
<label>Telegram Support Link</label><input id="tele_support_link"><label>WhatsApp Number</label><input id="wa_number"><label>WhatsApp Link</label><input id="wa_link"><label>Email Support</label><input id="email_support"><label>Tutorial YouTube Link</label><input id="tutorial_link">
</div>

<div class="card" style="border:2px solid #a855f7"><h3>🔒 5 - Locking System + Profile Colors + Badge 1-5</h3>
<div class="row"><div><label>Lock VPN (on/off)</label><input id="lock_vpn"></div><div><label>Lock Multi Account</label><input id="lock_multi_account"></div></div><label>Lock Emulator</label><input id="lock_emulator">
<div class="row"><div><label>Profile Card BG</label><input type="color" id="profile_card_bg"><input id="profile_card_bg"></div><div><label>Avatar Border</label><input type="color" id="avatar_border"></div></div>
<label>Badge 1 Name</label><input id="badge1_name"><div class="row"><div><label>Badge1 BG</label><input type="color" id="badge1_bg"></div><div><label>Badge1 Text</label><input type="color" id="badge1_text"></div></div>
<label>Badge 2</label><input id="badge2_name"><div class="row"><div><label>BG</label><input type="color" id="badge2_bg"></div><div><label>Text</label><input type="color" id="badge2_text"></div></div>
<label>Badge 3</label><input id="badge3_name"><div class="row"><div><label>BG</label><input type="color" id="badge3_bg"></div><div><label>Text</label><input type="color" id="badge3_text"></div></div>
<label>Badge 4</label><input id="badge4_name"><div class="row"><div><label>BG</label><input type="color" id="badge4_bg"></div><div><label>Text</label><input type="color" id="badge4_text"></div></div>
<label>Badge 5</label><input id="badge5_name"><div class="row"><div><label>BG</label><input type="color" id="badge5_bg"></div><div><label>Text</label><input type="color" id="badge5_text"></div></div>
</div>

<button class="btn" onclick="saveAll()">💾 SAVE ALL - 1 থেকে 5 + Logo + Locking</button><div id="msg" style="text-align:center;color:#22c55e;margin-top:12px;font-weight:900"></div>
<script>
function load(){fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{for(let k in d.settings){let el=document.getElementById(k);if(el)el.value=d.settings[k];}});}
function saveAll(){let data={};document.querySelectorAll('input').forEach(e=>{if(e.id)data[e.id]=e.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{document.getElementById('msg').innerText=d.msg;alert('✅ FINAL SAVE - 1 থেকে 5 সব');});}
load();
</script></body></html>
"""
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
