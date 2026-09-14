import os, json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
app = Flask(__name__)
DB='database.json'
def load_db():
    if not os.path.exists(DB):
        d={"users":{},"withdraws":[],"settings":{
            "app_name":"Protidiner Kaj BD","admin_name":"SHIBLI NOMAN","slider_img1":"","slider_img2":"","slider_img3":"","slider_img4":"","slider_img5":"",
            "slider_txt1":"Daily Bonus Available Today","slider_txt2":"Company Sponsored • 100% Safe","slider_txt3":"50 Ads দেখলে ৳100 বোনাস","slider_txt4":"100% Payment Guaranteed","slider_txt5":"প্রতিদিন কাজ করুন",
            "profile_card_bg":"#14142a","profile_card_border":"#1e1e3a","avatar_border_color":"#6d4cff","profile_name_color":"#ffffff","profile_id_color":"#9ca3af","stats_card_bg":"#0e0e20","stats_border":"#1e1e3a","verified_bg":"linear-gradient(135deg,#065f46,#047857)",
            "badge1_name":"Bronze Member","badge1_bg":"#6d4cff","badge1_text":"#ffffff","badge1_icon":"🏅",
            "badge2_name":"Silver Member","badge2_bg":"#9ca3af","badge2_text":"#000000","badge2_icon":"🥈",
            "badge3_name":"Gold Member","badge3_bg":"#f59e0b","badge3_text":"#000000","badge3_icon":"🥇",
            "badge4_name":"Platinum Member","badge4_bg":"#06b6d4","badge4_text":"#ffffff","badge4_icon":"💎",
            "badge5_name":"Diamond Member","badge5_bg":"#e2136e","badge5_text":"#ffffff","badge5_icon":"👑",
            "bkash_logo":"","nagad_logo":"","tele_sup_link":"https://t.me/","wa_sup_link":"https://wa.me/8801","tutorial_youtube_link":"https://youtube.com/","zone":"11764581"
        }}
        open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)); return d
    return json.load(open(DB,'r',encoding='utf-8'))
def save_db(d): open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid); today=str(datetime.now().date())
    if uid not in db["users"]: db["users"][uid]={"id":uid,"name":f"User {uid[-4:]}","balance":1120,"company":0,"popup":0,"total":0,"tasks":[],"img":"","join":today,"last":today,"badge":1}
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
    db=load_db(); u=get_user(db,request.args.get('id','0')); save_db(db); return jsonify({"user":u,"settings":db["settings"]})
@app.route('/api/reward')
def reward():
    db=load_db(); typ=request.args.get('type','company'); u=get_user(db,request.args.get('id'))
    if typ=='company': u["company"]+=1; u["balance"]+=2
    else: u["popup"]+=1; u["balance"]+=3
    u["total"]+=1; tot=u["company"]+u["popup"]+len(u["tasks"]); u["badge"]=5 if tot>=50 else 4 if tot>=40 else 3 if tot>=25 else 2 if tot>=10 else 1
    save_db(db); return jsonify({"msg":"৳ যোগ"})
@app.route('/api/task/done',methods=['POST'])
def taskdone():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); tid=int(j.get('tid'))
    if tid not in u["tasks"]: u["tasks"].append(tid); u["balance"]+=20; u["total"]+=1; save_db(db); return jsonify({"msg":"✅ 20 TK"})
    return jsonify({"msg":"করা হয়েছে"})
@app.route('/api/withdraw',methods=['POST'])
def wd():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); amt=int(j.get('amt',0))
    if amt<500: return jsonify({"msg":"মিনিমাম ৳500"})
    if u["balance"]<amt: return jsonify({"msg":"ব্যালেন্স কম"})
    u["balance"]-=amt; save_db(db); return jsonify({"msg":"✅ Withdraw"})
@app.route('/api/profile/save',methods=['POST'])
def psave():
    db=load_db(); j=request.json; u=get_user(db,j.get('id')); u["name"]=j.get('name',u["name"]); u["img"]=j.get('img',u["img"]); save_db(db); return jsonify({"msg":"✅ Save"})
@app.route('/api/admin/save',methods=['POST'])
def asave():
    db=load_db(); j=request.json;
    for k,v in j.items(): db["settings"][k]=v
    save_db(db); return jsonify({"msg":"✅ রং + 5 বেজ + 5 ছবি সব সেভ"})

HTML="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Protidiner Kaj BD</title><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#08080f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:100px}
.top{padding:12px 14px;display:flex;justify-content:space-between;align-items:center;background:#0c0c1a;position:sticky;top:0;z-index:99}
.card{margin:10px 12px;border-radius:22px;padding:14px;background:#14142a;border:1px solid #1e1e3a}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;margin-top:10px;cursor:pointer}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0f0f1e;display:flex;padding:8px 0 12px;border-radius:22px 22px 0 0;z-index:99}
.btm div{flex:1;text-align:center;color:#6b6b8a;font-size:11px;cursor:pointer}.btm div.on{color:#fff}.btm div span{font-size:24px;display:block}
input{width:100%;padding:12px;border-radius:12px;border:1px solid #2a2a4a;background:#0e0e20;color:#fff;margin-top:8px}
.page{display:none}.page.active{display:block}
.halkaDew{animation:dewGlow 4s ease-in-out infinite}@keyframes dewGlow{0%{box-shadow:0 0 0px transparent}50%{box-shadow:0 0 22px #ffffff0d}100%{box-shadow:0 0 0px transparent}}
.progressWrap{width:100%;height:8px;background:#00000060;border-radius:10px;margin-top:14px;overflow:hidden}.progressBar{height:100%;width:0%;background:linear-gradient(90deg,#22c55e,#f59e0b);transition:width 1.2s ease}
.payCard{display:flex;align-items:center;gap:12px;background:#0e0e20;border:2px solid #2a2a4a;border-radius:18px;padding:14px;margin:12px 0;cursor:pointer;position:relative}.payCard.active{border-color:#e2136e}.check{position:absolute;right:12px;width:24px;height:24px;background:#22c55e;border-radius:50%;display:none;align-items:center;justify-content:center}.payCard.active.check{display:flex}
.slider{position:relative;width:100%;height:160px;border-radius:22px;overflow:hidden}.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;opacity:0;transition:opacity 1s ease;background-size:cover;background-position:center}.slide.active{opacity:1}
.dotWrap{display:flex;gap:6px;justify-content:center;margin-top:8px}.dot{width:8px;height:8px;background:#ffffff40;border-radius:50%}.dot.active{background:#fff;width:20px}
.avatarWrap{width:120px;height:120px;border-radius:50%;margin:0 auto;position:relative;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden}
</style></head><body>
<div class="top"><div style="display:flex;gap:10px;align-items:center"><div style="font-size:32px">👑</div><div><div style="font-weight:800" id="appNameTop">Protidiner Kaj BD</div><div style="font-size:12px;color:#9ca3af">Admin: SHIBLI NOMAN</div></div></div><div onclick="goPage('profile')" style="width:46px;height:46px;border-radius:50%;border:2px solid #6d4cff;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden"><img id="topAv" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="topAvT">👤</span></div></div>

<div id="p-home" class="page active">
<div class="card halkaDew" style="padding:0;border:none;overflow:hidden"><div class="slider"><div class="slide active" id="s1" style="background:linear-gradient(90deg,#f59e0b,#ef4444)"><span id="st1">Daily Bonus</span></div><div class="slide" id="s2" style="background:linear-gradient(90deg,#06b6d4,#3b82f6)"><span id="st2">Company Safe</span></div><div class="slide" id="s3" style="background:linear-gradient(90deg,#10b981,#06b6d4)"><span id="st3">Bonus</span></div><div class="slide" id="s4" style="background:linear-gradient(90deg,#8b5cf6,#ec4899)"><span id="st4">Guaranteed</span></div><div class="slide" id="s5" style="background:linear-gradient(90deg,#f97316,#eab308)"><span id="st5">কাজ করুন</span></div></div><div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div></div>
<div class="card halkaDew" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4,#10b981);text-align:center;border:none"><div id="balTitle">ব্যালেন্স</div><div style="font-size:56px;font-weight:900" id="balMain">৳1120</div><div style="display:flex;gap:8px;justify-content:center"><span style="background:#0005;padding:6px 12px;border-radius:20px;font-size:12px" id="c1">0/30</span><span style="background:#0005;padding:6px 12px;border-radius:20px;font-size:12px" id="c2">0/20</span><span style="background:#0005;padding:6px 12px;border-radius:20px;font-size:12px" id="c3">Total 0</span></div><div class="progressWrap"><div id="progressBar" class="progressBar"></div></div></div>
<div class="card"><button class="btn" style="background:#7c3aed" onclick="doCompany()">📺 COMPANY ADS <span id="btnC">0/30</span></button><button class="btn" style="background:#16a34a" onclick="doPopup()">💰 POPUP ADS <span id="btnP">0/20</span></button><button class="btn" style="background:#1e293b" onclick="goPage('tasks')">📋 TASK BONUS</button></div>
</div>

<div id="p-tasks" class="page"><div class="card"><div id="taskList"></div></div></div>
<div id="p-wallet" class="page"><div class="card" style="background:#1e293b;text-align:center"><div id="wBal" style="font-size:52px;font-weight:900">৳1120</div><div class="progressWrap"><div id="wProgress" class="progressBar"></div></div></div><div class="card"><div id="bCard" class="payCard active" onclick="selectPay('bKash')"><div style="width:56px;height:56px;background:#e2136e;border-radius:16px;display:flex;align-items:center;justify-content:center">৳</div><div style="flex:1"><b>bKash</b></div><div class="check">✓</div></div><div id="nCard" class="payCard" onclick="selectPay('Nagad')"><div style="width:56px;height:56px;background:#f59e0b;border-radius:16px;display:flex;align-items:center;justify-content:center">৳</div><div style="flex:1"><b>Nagad</b></div><div class="check">✓</div></div><input id="accNum" placeholder="01XXX"><input id="wdAmt" type="number" placeholder="500"><button class="btn" style="background:linear-gradient(90deg,#e2136e,#f59e0b)" onclick="doWithdraw()">Withdraw করুন</button></div></div>
<div id="p-support" class="page"><div class="card"><button class="btn" style="background:#0ea5e9" onclick="openLink('tele')">Telegram</button><button class="btn" style="background:#22c55e" onclick="openLink('wa')">WhatsApp</button><button class="btn" style="background:#f59e0b" onclick="openLink('tut')">Tutorial Video</button></div></div>

<div id="p-profile" class="page">
<div class="card" id="profileCard" style="text-align:center"><div class="avatarWrap halkaDew" id="avatarWrap" onclick="openGal()"><img id="pAv" src="" style="display:none;width:100%;height:100%;object-fit:cover"><span id="pAvT" style="font-size:64px">👤</span></div><div style="margin-top:12px"><b id="pName">User</b><div id="pId" style="font-size:12px">ID:</div><div id="memberBadge" style="display:inline-block;padding:7px 16px;border-radius:20px;font-size:13px;font-weight:800;margin-top:8px">🏅 Bronze</div></div><input id="pNameIn" placeholder="নাম" style="text-align:center;margin-top:12px"><button class="btn" style="background:#6d4cff" onclick="openGal()">📸 গ্যালারি থেকে ছবি নিন</button><button class="btn" style="background:#22c55e" onclick="saveProf()">💾 Save Profile</button><input type="file" id="fileIn" accept="image/*" style="display:none" onchange="handleFile(this)"></div>
<div class="card" id="statsCard"><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px"><div class="sBox" style="background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:14px;text-align:center"><div>💰</div><div style="font-weight:900" id="sBal">৳1120</div></div><div class="sBox" style="background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:14px;text-align:center"><div>📺</div><div style="font-weight:900" id="sAds">0</div></div><div class="sBox" style="background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:14px;text-align:center"><div>📋</div><div style="font-weight:900" id="sTask">0</div></div></div><div style="margin-top:12px;background:#0e0e20;padding:10px;border-radius:12px;font-size:11px" id="myRef"></div><button class="btn" style="background:#1e293b" onclick="copyText('myRef')">📋 Copy</button><button class="btn" style="background:#ef4444" onclick="localStorage.clear();location.reload()">🚪 লগআউট</button></div>
<div class="card" id="verifiedCard" style="text-align:center"><div id="verifiedTitle">Verified User</div></div>
</div>

<div class="btm"><div id="n-home" class="on" onclick="goPage('home')"><span>🏠</span>Home</div><div id="n-tasks" onclick="goPage('tasks')"><span>📋</span>Task</div><div id="n-wallet" onclick="goPage('wallet')"><span>💰</span>Wallet</div><div id="n-support" onclick="goPage('support')"><span>💬</span>Support</div><div id="n-profile" onclick="goPage('profile')"><span>👤</span>Profile</div></div>

<script>
let uid=localStorage.getItem('locked_phone')||'8807178385'; let tempImg=''; let settings={}; let method='bKash'; let curSlide=0;
function init(){ fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{ settings=d.settings; let u=d.user; let total=u.company+u.popup; let pct=Math.min(Math.round((total/50)*100),100);
for(let i=1;i<=5;i++){ let img=settings['slider_img'+i]; if(img){ document.getElementById('s'+i).style.backgroundImage='url('+img+')'; document.getElementById('s'+i).style.backgroundSize='cover'; } document.getElementById('st'+i).innerText=settings['slider_txt'+i]; }
document.getElementById('profileCard').style.background=settings.profile_card_bg; document.getElementById('profileCard').style.borderColor=settings.profile_card_border; document.getElementById('avatarWrap').style.border='3px solid '+settings.avatar_border_color; document.getElementById('pName').style.color=settings.profile_name_color; document.getElementById('pId').style.color=settings.profile_id_color;
document.querySelectorAll('.sBox').forEach(el=>{ el.style.background=settings.stats_card_bg; el.style.borderColor=settings.stats_border; }); document.getElementById('verifiedCard').style.background=settings.verified_bg;
let bIdx=u.badge||1; let badgeEl=document.getElementById('memberBadge'); badgeEl.innerText=settings['badge'+bIdx+'_icon']+' '+settings['badge'+bIdx+'_name']; badgeEl.style.background=settings['badge'+bIdx+'_bg']; badgeEl.style.color=settings['badge'+bIdx+'_text'];
document.getElementById('balMain').innerText='৳'+u.balance; document.getElementById('wBal').innerText='৳'+u.balance; document.getElementById('sBal').innerText='৳'+u.balance; document.getElementById('c1').innerText='Company '+u.company+'/30'; document.getElementById('c2').innerText='Popup '+u.popup+'/20'; document.getElementById('c3').innerText='Total '+u.total; document.getElementById('btnC').innerText=u.company+'/30'; document.getElementById('btnP').innerText=u.popup+'/20'; document.getElementById('progressBar').style.width=pct+'%'; document.getElementById('wProgress').style.width=pct+'%';
document.getElementById('pName').innerText=u.name; document.getElementById('pId').innerText='ID: '+u.id; document.getElementById('sAds').innerText=total; document.getElementById('sTask').innerText=u.tasks.length; document.getElementById('myRef').innerText=location.origin+'/?ref='+u.id; document.getElementById('pNameIn').value=u.name;
if(u.img){ document.getElementById('pAv').src=u.img; document.getElementById('pAv').style.display='block'; document.getElementById('pAvT').style.display='none'; document.getElementById('topAv').src=u.img; document.getElementById('topAv').style.display='block'; document.getElementById('topAvT').style.display='none'; tempImg=u.img; }
let taskHtml=''; for(let i=1;i<=5;i++){ let done=u.tasks.includes(i); taskHtml+=`<div style="display:flex;justify-content:space-between;background:#0e0e20;border:1px solid #1e1e3a;border-radius:16px;padding:12px;margin:10px 0"><div><b>${['','Telegram','YouTube','Facebook','Refer','Check-in'][i]}</b></div><button class="btn" style="width:auto;background:${done?'#22c55e':'#6d4cff'};padding:10px 18px;margin:0" onclick="doTask(${i})">${done?'✓':'20৳'}</button></div>`; } document.getElementById('taskList').innerHTML=taskHtml;
});}
function goPage(p){ document.querySelectorAll('.page').forEach(e=>e.classList.remove('active')); document.getElementById('p-'+p).classList.add('active'); document.querySelectorAll('.btm div').forEach(e=>e.classList.remove('on')); document.getElementById('n-'+p).classList.add('on');}
function doCompany(){ fetch('/api/reward?id='+uid+'&type=company').then(r=>r.json()).then(d=>{ init(); if(typeof show_11764581==='function') show_11764581(); });}
function doPopup(){ fetch('/api/reward?id='+uid+'&type=popup').then(r=>r.json()).then(d=>{ init(); if(typeof show_11764581==='function') show_11764581(); });}
function doTask(i){ fetch('/api/task/done',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,tid:i})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); });}
function selectPay(m){ method=m; document.getElementById('bCard').classList.toggle('active',m=='bKash'); document.getElementById('nCard').classList.toggle('active',m=='Nagad'); }
function doWithdraw(){ let num=document.getElementById('accNum').value; let amt=document.getElementById('wdAmt').value; if(!num||!amt){alert('দিন');return;} fetch('/api/withdraw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:method})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); });}
function openLink(k){ if(settings[k]) window.open(settings[k],'_blank');}
function openGal(){ document.getElementById('fileIn').click(); }
function handleFile(inp){ let f=inp.files[0]; if(!f) return; let rd=new FileReader(); rd.onload=e=>{ tempImg=e.target.result; document.getElementById('pAv').src=tempImg; document.getElementById('pAv').style.display='block'; document.getElementById('pAvT').style.display='none'; document.getElementById('topAv').src=tempImg; document.getElementById('topAv').style.display='block'; document.getElementById('topAvT').style.display='none'; }; rd.readAsDataURL(f); }
function saveProf(){ let name=document.getElementById('pNameIn').value||'User'; fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:name,img:tempImg})}).then(r=>r.json()).then(d=>{ alert(d.msg); init(); });}
function copyText(id){ navigator.clipboard.writeText(document.getElementById(id).innerText); alert('Copy');}
setInterval(()=>{ curSlide=(curSlide+1)%5; document.querySelectorAll('.slide').forEach((el,i)=>el.classList.toggle('active',i==curSlide)); document.querySelectorAll('.dot').forEach((el,i)=>el.classList.toggle('active',i==curSlide)); },3000);
init();
</script></body></html>
"""

ADMIN="""<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Admin Color</title><style>body{background:#070710;color:#fff;max-width:850px;margin:0 auto;padding:14px;font-family:system-ui}.card{background:#15152a;border-radius:14px;padding:14px;margin:12px 0;border:1px solid #222}input{width:100%;padding:10px;border-radius:10px;border:1px solid #333;background:#0e0e20;color:#fff;margin-top:6px}input[type=color]{height:50px}label{font-size:11px;color:#9ca3af;margin-top:10px;display:block}.btn{width:100%;padding:14px;background:#6d4cff;border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:16px;cursor:pointer}.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}</style></head><body>
<h2 style="text-align:center">👑 Admin - প্রোফাইল রং + ৫ বেজ + ৫ ছবি</h2>

<div class="card" style="border:2px solid #f59e0b"><h3>🎠 5 ছবি - 3 সেকেন্ড পর পর</h3><label>Image1 URL</label><input id="slider_img1"><label>Text1</label><input id="slider_txt1"><label>Image2</label><input id="slider_img2"><label>Text2</label><input id="slider_txt2"><label>Image3</label><input id="slider_img3"><label>Text3</label><input id="slider_txt3"><label>Image4</label><input id="slider_img4"><label>Text4</label><input id="slider_txt4"><label>Image5</label><input id="slider_img5"><label>Text5</label><input id="slider_txt5"></div>

<div class="card" style="border:2px solid #6d4cff"><h3>🎨 প্রোফাইল রং - যে কোন রং</h3><div class="row"><div><label>Profile Card BG</label><input type="color" id="profile_card_bg"><input id="profile_card_bg"></div><div><label>Border</label><input type="color" id="profile_card_border"><input id="profile_card_border"></div></div><div class="row"><div><label>Avatar Border</label><input type="color" id="avatar_border_color"></div><div><label>Name Color</label><input type="color" id="profile_name_color"></div></div><div class="row"><div><label>ID Color</label><input type="color" id="profile_id_color"></div><div><label>Stats BG</label><input type="color" id="stats_card_bg"></div></div><div class="row"><div><label>Stats Border</label><input type="color" id="stats_border"></div><div><label>Verified BG</label><input id="verified_bg"></div></div></div>

<div class="card" style="border:2px solid #e2136e"><h3>🏅 ৫টা বেজের রং</h3>
<div style="background:#0003;padding:10px;border-radius:12px;margin-top:8px"><h4>Badge 1 Bronze (0-9)</h4><div class="row"><div><label>Name</label><input id="badge1_name"></div><div><label>Icon</label><input id="badge1_icon"></div></div><div class="row"><div><label>BG</label><input type="color" id="badge1_bg"></div><div><label>Text</label><input type="color" id="badge1_text"></div></div></div>
<div style="background:#0003;padding:10px;border-radius:12px;margin-top:8px"><h4>Badge 2 Silver (10+)</h4><div class="row"><div><label>Name</label><input id="badge2_name"></div><div><label>Icon</label><input id="badge2_icon"></div></div><div class="row"><div><label>BG</label><input type="color" id="badge2_bg"></div><div><label>Text</label><input type="color" id="badge2_text"></div></div></div>
<div style="background:#0003;padding:10px;border-radius:12px;margin-top:8px"><h4>Badge 3 Gold (25+)</h4><div class="row"><div><label>Name</label><input id="badge3_name"></div><div><label>Icon</label><input id="badge3_icon"></div></div><div class="row"><div><label>BG</label><input type="color" id="badge3_bg"></div><div><label>Text</label><input type="color" id="badge3_text"></div></div></div>
<div style="background:#0003;padding:10px;border-radius:12px;margin-top:8px"><h4>Badge 4 Platinum (40+)</h4><div class="row"><div><label>Name</label><input id="badge4_name"></div><div><label>Icon</label><input id="badge4_icon"></div></div><div class="row"><div><label>BG</label><input type="color" id="badge4_bg"></div><div><label>Text</label><input type="color" id="badge4_text"></div></div></div>
<div style="background:#0003;padding:10px;border-radius:12px;margin-top:8px"><h4>Badge 5 Diamond (50+)</h4><div class="row"><div><label>Name</label><input id="badge5_name"></div><div><label>Icon</label><input id="badge5_icon"></div></div><div class="row"><div><label>BG</label><input type="color" id="badge5_bg"></div><div><label>Text</label><input type="color" id="badge5_text"></div></div></div>
</div>

<button class="btn" onclick="saveAll()">💾 SAVE - রং + বেজ + ছবি</button><div id="msg" style="color:#22c55e;text-align:center;margin-top:12px"></div>
<script>
function load(){ fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{ for(let k in d.settings){ document.querySelectorAll('#'+k).forEach(el=>{ if(el) el.value=d.settings[k]; }); } });}
function saveAll(){ let data={}; document.querySelectorAll('input').forEach(e=>{ if(e.id) data[e.id]=e.value; }); fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{ document.getElementById('msg').innerText=d.msg; alert('✅ সব সেভ'); });}
load();
</script></body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
