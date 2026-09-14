import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__)
DB='database.json'
def load_db():
 if not os.path.exists(DB):
  d={"users":{},"settings":{
   "slider_img1":"","slider_img2":"","slider_img3":"","slider_img4":"","slider_img5":"",
   "slider_txt1":"1 - Daily Bonus Available","slider_txt2":"2 - Company Sponsored Safe","slider_txt3":"3 - 50 Ads = 100TK Bonus","slider_txt4":"4 - 100% Payment Guaranteed","slider_txt5":"5 - প্রতিদিন কাজ করুন",
   "profile_card_bg":"#14142a","profile_card_border":"#6d4cff","avatar_border_color":"#6d4cff","profile_name_color":"#ffffff","profile_id_color":"#9ca3af","stats_card_bg":"#0e0e20","stats_border":"#1e1e3a",
   "badge1_name":"1 Bronze Member","badge1_bg":"#6d4cff","badge1_text":"#ffffff","badge1_icon":"🏅","badge2_name":"2 Silver Member","badge2_bg":"#9ca3af","badge2_text":"#000000","badge2_icon":"🥈","badge3_name":"3 Gold Member","badge3_bg":"#f59e0b","badge3_text":"#000000","badge3_icon":"🥇","badge4_name":"4 Platinum Member","badge4_bg":"#06b6d4","badge4_text":"#ffffff","badge4_icon":"💎","badge5_name":"5 Diamond Member","badge5_bg":"#e2136e","badge5_text":"#ffffff","badge5_icon":"👑"
  }}
  open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
  return d
 return json.load(open(DB,'r',encoding='utf-8'))
def save_db(d):open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
 uid=str(uid)
 if uid not in db["users"]:db["users"][uid]={"id":uid,"name":"User","balance":1120,"company":0,"badge":1,"img":""}
 return db["users"][uid]
@app.route('/')
def home():return render_template_string(HTML)
@app.route('/admin')
def admin():
 if request.args.get('id')!='8807178385':return "admin?id=8807178385"
 return render_template_string(ADMIN)
@app.route('/api/get')
def api_get():db=load_db();u=get_user(db,request.args.get('id','0'));save_db(db);return jsonify({"user":u,"settings":db["settings"]})
@app.route('/api/reward')
def reward():db=load_db();u=get_user(db,request.args.get('id'));u["company"]+=1;u["balance"]+=2;u["badge"]=5 if u["company"]>=50 else 4 if u["company"]>=40 else 3 if u["company"]>=25 else 2 if u["company"]>=10 else 1;save_db(db);return jsonify({"msg":"ok"})
@app.route('/api/profile/save',methods=['POST'])
def psave():db=load_db();j=request.json;u=get_user(db,j.get('id'));u["name"]=j.get('name');u["img"]=j.get('img');save_db(db);return jsonify({"msg":"Save"})
@app.route('/api/admin/save',methods=['POST'])
def asave():db=load_db();j=request.json;db["settings"].update(j);save_db(db);return jsonify({"msg":"✅ 1 থেকে 5 সব সেভ হয়েছে"})

HTML="""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><script src="//libtl.com/sdk.js" data-zone="11764581" data-sdk="show_11764581"></script><style>*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui}body{background:#08080f;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}.card{margin:10px 12px;border-radius:22px;padding:14px;background:#14142a;border:1px solid #1e1e3a}.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;color:#fff;margin-top:10px;cursor:pointer;background:#6d4cff}.slider{position:relative;width:100%;height:170px;border-radius:22px;overflow:hidden;background:#111}.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;opacity:0;transition:opacity 1s ease;background-size:cover;background-position:center;text-shadow:0 2px 10px #000}.slide.active{opacity:1}.dotWrap{display:flex;gap:6px;justify-content:center;margin-top:8px}.dot{width:8px;height:8px;background:#ffffff40;border-radius:50%}.dot.active{background:#fff;width:22px}.avatarWrap{width:120px;height:120px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#1e293b}.progressWrap{width:100%;height:8px;background:#0006;border-radius:10px;margin-top:12px;overflow:hidden}.progressBar{height:100%;width:0%;background:linear-gradient(90deg,#22c55e,#f59e0b);transition:1s}</style></head><body>
<div id="p-home" class="page active"><div class="card" style="padding:0;border:none;overflow:hidden"><div class="slider" id="sliderBox"><div class="slide active" id="s1"><span id="st1">1 - Daily Bonus</span></div><div class="slide" id="s2"><span id="st2">2 - Safe</span></div><div class="slide" id="s3"><span id="st3">3 - Bonus</span></div><div class="slide" id="s4"><span id="st4">4 - Guaranteed</span></div><div class="slide" id="s5"><span id="st5">5 - কাজ করুন</span></div></div><div class="dotWrap"><div class="dot active" id="d1"></div><div class="dot" id="d2"></div><div class="dot" id="d3"></div><div class="dot" id="d4"></div><div class="dot" id="d5"></div></div></div>
<div class="card" style="background:linear-gradient(135deg,#1d4ed8,#06b6d4,#10b981);text-align:center;border:none"><div style="font-size:50px;font-weight:900" id="bal">৳1120</div><div class="progressWrap"><div id="pb" class="progressBar"></div></div><div id="pcTxt" style="font-size:12px;margin-top:4px">0/50</div></div>
<div class="card"><button class="btn" onclick="doAds()">📺 COMPANY ADS (৳2) <span id="cc">0/50</span></button><button class="btn" style="background:#22c55e" onclick="goP('profile')">👤 Profile রং দেখুন</button></div></div>
<div id="p-profile" class="page" style="display:none"><div class="card" id="pCard" style="text-align:center"><div class="avatarWrap" id="avWrap" onclick="openG()"><img id="pAv" style="display:none;width:100%;height:100%;object-fit:cover"><span id="pAvT" style="font-size:60px">👤</span></div><div id="pName" style="font-weight:800;font-size:20px;margin-top:10px">User</div><div id="pId" style="font-size:12px">ID</div><div id="badge" style="display:inline-block;padding:7px 16px;border-radius:20px;font-weight:800;margin-top:8px">🏅 Bronze</div><input id="pNameIn" placeholder="নাম" style="width:100%;padding:12px;border-radius:12px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:12px;text-align:center"><button class="btn" onclick="openG()">📸 গ্যালারি</button><button class="btn" style="background:#22c55e" onclick="savePr()">💾 Save</button><input type="file" id="fileIn" accept="image/*" style="display:none" onchange="handleF(this)"></div><div class="card"><button class="btn" style="background:#1e293b" onclick="goP('home')">🏠 Home</button><button class="btn" style="background:#ef4444" onclick="location.href='/admin?id=8807178385'">⚙️ Admin Panel</button></div></div>
<script>
let uid='8807178385',tmp='',set={},cur=0;
function goP(p){document.getElementById('p-home').style.display=p=='home'?'block':'none';document.getElementById('p-profile').style.display=p=='profile'?'block':'none';}
function init(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{set=d.settings;let u=d.user;
for(let i=1;i<=5;i++){let im=set['slider_img'+i];if(im){document.getElementById('s'+i).style.backgroundImage='url('+im+')';document.getElementById('s'+i).style.backgroundColor='#000';}document.getElementById('st'+i).innerText=set['slider_txt'+i];}
document.getElementById('pCard').style.background=set.profile_card_bg;document.getElementById('pCard').style.borderColor=set.profile_card_border;document.getElementById('avWrap').style.border='3px solid '+set.avatar_border_color;document.getElementById('pName').style.color=set.profile_name_color;document.getElementById('pId').style.color=set.profile_id_color;
let b=u.badge||1;let el=document.getElementById('badge');el.innerText=set['badge'+b+'_icon']+' '+set['badge'+b+'_name'];el.style.background=set['badge'+b+'_bg'];el.style.color=set['badge'+b+'_text'];
document.getElementById('bal').innerText='৳'+u.balance;document.getElementById('cc').innerText=u.company+'/50';document.getElementById('pb').style.width=Math.min(u.company/50*100,100)+'%';document.getElementById('pcTxt').innerText=u.company+'/50 Complete';document.getElementById('pName').innerText=u.name;document.getElementById('pId').innerText='ID: '+u.id;document.getElementById('pNameIn').value=u.name;
if(u.img){document.getElementById('pAv').src=u.img;document.getElementById('pAv').style.display='block';document.getElementById('pAvT').style.display='none';tmp=u.img;}
});}
function doAds(){fetch('/api/reward?id='+uid).then(()=>{init();if(typeof show_11764581==='function')show_11764581();});}
function openG(){document.getElementById('fileIn').click();}
function handleF(i){let f=i.files[0];let r=new FileReader();r.onload=e=>{tmp=e.target.result;document.getElementById('pAv').src=tmp;document.getElementById('pAv').style.display='block';document.getElementById('pAvT').style.display='none';};r.readAsDataURL(f);}
function savePr(){let n=document.getElementById('pNameIn').value;fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:tmp})}).then(r=>r.json()).then(d=>{alert(d.msg);init();});}
setInterval(()=>{cur=(cur+1)%5;for(let i=1;i<=5;i++){document.getElementById('s'+i).classList.toggle('active',i-1==cur);document.getElementById('d'+i).classList.toggle('active',i-1==cur);}},3000);
init();
</script></body></html>
"""

ADMIN="""<html><head><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>body{background:#070710;color:#fff;max-width:750px;margin:0 auto;padding:12px;font-family:system-ui}.card{background:#15152a;border-radius:12px;padding:12px;margin:10px 0;border:1px solid #222}input{width:100%;padding:9px;border-radius:8px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:5px}input[type=color]{height:44px}label{font-size:11px;color:#aaa;margin-top:8px;display:block}.row{display:grid;grid-template-columns:1fr 1fr;gap:8px}.btn{width:100%;padding:14px;background:#6d4cff;border:none;border-radius:12px;color:#fff;font-weight:900;margin-top:14px}</style></head><body>
<h2 style="text-align:center">👑 FINAL Admin - 1 থেকে 5 পুরাটা</h2>
<div class="card" style="border:2px solid #f59e0b"><h3>1 থেকে 5 - উপরের বক্স - 3 সেকেন্ড পর পর</h3>
<label>1 - Image URL</label><input id="slider_img1" placeholder="https://...jpg"><label>1 - Text</label><input id="slider_txt1">
<label>2 - Image URL</label><input id="slider_img2"><label>2 - Text</label><input id="slider_txt2">
<label>3 - Image URL</label><input id="slider_img3"><label>3 - Text</label><input id="slider_txt3">
<label>4 - Image URL</label><input id="slider_img4"><label>4 - Text</label><input id="slider_txt4">
<label>5 - Image URL</label><input id="slider_img5"><label>5 - Text</label><input id="slider_txt5">
</div>
<div class="card" style="border:2px solid #6d4cff"><h3>🎨 প্রোফাইল রং - যে কোন রং</h3><div class="row"><div><label>Card BG</label><input type="color" id="profile_card_bg"><input id="profile_card_bg"></div><div><label>Border Color</label><input type="color" id="profile_card_border"><input id="profile_card_border"></div></div><div class="row"><div><label>Avatar Border</label><input type="color" id="avatar_border_color"></div><div><label>Name Color</label><input type="color" id="profile_name_color"></div></div><label>ID Color</label><input type="color" id="profile_id_color"></div>
<div class="card" style="border:2px solid #e2136e"><h3>🏅 1 থেকে 5 - বেজের রং সিস্টেম</h3>
<div style="background:#0003;padding:8px;border-radius:10px;margin-top:6px"><b>1 - Bronze</b><label>Name</label><input id="badge1_name"><div class="row"><div><label>BG</label><input type="color" id="badge1_bg"></div><div><label>Text</label><input type="color" id="badge1_text"></div></div><label>Icon</label><input id="badge1_icon"></div>
<div style="background:#0003;padding:8px;border-radius:10px;margin-top:6px"><b>2 - Silver</b><label>Name</label><input id="badge2_name"><div class="row"><div><label>BG</label><input type="color" id="badge2_bg"></div><div><label>Text</label><input type="color" id="badge2_text"></div></div><label>Icon</label><input id="badge2_icon"></div>
<div style="background:#0003;padding:8px;border-radius:10px;margin-top:6px"><b>3 - Gold</b><label>Name</label><input id="badge3_name"><div class="row"><div><label>BG</label><input type="color" id="badge3_bg"></div><div><label>Text</label><input type="color" id="badge3_text"></div></div><label>Icon</label><input id="badge3_icon"></div>
<div style="background:#0003;padding:8px;border-radius:10px;margin-top:6px"><b>4 - Platinum</b><label>Name</label><input id="badge4_name"><div class="row"><div><label>BG</label><input type="color" id="badge4_bg"></div><div><label>Text</label><input type="color" id="badge4_text"></div></div><label>Icon</label><input id="badge4_icon"></div>
<div style="background:#0003;padding:8px;border-radius:10px;margin-top:6px"><b>5 - Diamond</b><label>Name</label><input id="badge5_name"><div class="row"><div><label>BG</label><input type="color" id="badge5_bg"></div><div><label>Text</label><input type="color" id="badge5_text"></div></div><label>Icon</label><input id="badge5_icon"></div>
</div>
<button class="btn" onclick="saveAll()">💾 SAVE - 1 থেকে 5 সব সেভ</button><div id="msg" style="text-align:center;color:#22c55e;margin-top:10px"></div>
<script>
function load(){fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{for(let k in d.settings){document.querySelectorAll('#'+k).forEach(e=>{if(e)e.value=d.settings[k];});}});}
function saveAll(){let data={};document.querySelectorAll('input').forEach(e=>{if(e.id)data[e.id]=e.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{document.getElementById('msg').innerText=d.msg;alert('✅ 1 থেকে 5 সব সেভ');});}
load();
</script></body></html>
"""
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
