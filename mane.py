# FINAL A TO Z - profile color + 5 badge color + 5 slider
import os,json
from flask import Flask,request,jsonify,render_template_string
from datetime import datetime
app=Flask(__name__);DB='database.json'
def load_db():
 if not os.path.exists(DB):
  d={"users":{},"settings":{"slider_img1":"","slider_img2":"","slider_img3":"","slider_img4":"","slider_img5":"","slider_txt1":"Bonus Today","slider_txt2":"Safe","slider_txt3":"100TK Bonus","slider_txt4":"Guaranteed","slider_txt5":"কাজ করুন","profile_card_bg":"#14142a","profile_card_border":"#1e1e3a","avatar_border_color":"#6d4cff","profile_name_color":"#ffffff","profile_id_color":"#9ca3af","badge1_name":"Bronze","badge1_bg":"#6d4cff","badge1_text":"#ffffff","badge1_icon":"🏅","badge2_name":"Silver","badge2_bg":"#9ca3af","badge2_text":"#000000","badge2_icon":"🥈","badge3_name":"Gold","badge3_bg":"#f59e0b","badge3_text":"#000000","badge3_icon":"🥇","badge4_name":"Platinum","badge4_bg":"#06b6d4","badge4_text":"#ffffff","badge4_icon":"💎","badge5_name":"Diamond","badge5_bg":"#e2136e","badge5_text":"#ffffff","badge5_icon":"👑"}}
  open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2));return d
 return json.load(open(DB,'r',encoding='utf-8'))
def save_db(d):open(DB,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
def get_user(db,uid):
 uid=str(uid)
 if uid not in db["users"]:db["users"][uid]={"id":uid,"name":"User","balance":1120,"company":0,"popup":0,"badge":1,"img":""}
 return db["users"][uid]
@app.route('/')
def home():return render_template_string(HTML)
@app.route('/admin')
def adm():
 if request.args.get('id')!='8807178385':return "use?id=8807178385"
 return render_template_string(ADMIN)
@app.route('/api/get')
def g():db=load_db();u=get_user(db,request.args.get('id','0'));save_db(db);return jsonify({"user":u,"settings":db["settings"]})
@app.route('/api/reward')
def r():db=load_db();u=get_user(db,request.args.get('id'));u["company"]+=1;u["balance"]+=2;tot=u["company"];u["badge"]=5 if tot>=50 else 4 if tot>=40 else 3 if tot>=25 else 2 if tot>=10 else 1;save_db(db);return jsonify({"ok":1})
@app.route('/api/profile/save',methods=['POST'])
def ps():db=load_db();j=request.json;u=get_user(db,j.get('id'));u["name"]=j.get('name');u["img"]=j.get('img');save_db(db);return jsonify({"msg":"Save"})
@app.route('/api/admin/save',methods=['POST'])
def sv():db=load_db();j=request.json;db["settings"].update(j);save_db(db);return jsonify({"msg":"✅ Save Done"})
HTML="""<html><head><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>body{background:#08080f;color:#fff;max-width:430px;margin:0 auto}.card{margin:10px;border-radius:20px;padding:14px;background:#14142a;border:1px solid #1e1e3a}.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:800;color:#fff;margin-top:10px;background:#6d4cff}.slider{height:160px;border-radius:20px;overflow:hidden;position:relative}.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;transition:1s;background-size:cover}.slide.active{opacity:1}.avatar{width:110px;height:110px;border-radius:50%;margin:0 auto;background:#1e293b;display:flex;align-items:center;justify-content:center;overflow:hidden}</style></head><body>
<div class="card" style="padding:0;overflow:hidden"><div class="slider"><div class="slide active" id="s1"><span id="st1"></span></div><div class="slide" id="s2"><span id="st2"></span></div><div class="slide" id="s3"><span id="st3"></span></div><div class="slide" id="s4"><span id="st4"></span></div><div class="slide" id="s5"><span id="st5"></span></div></div></div>
<div class="card" id="pc" style="text-align:center"><div class="avatar" id="av"><img id="pAv" style="display:none;width:100%;height:100%;object-fit:cover"><span id="pAvT">👤</span></div><div id="pn" style="margin-top:8px;font-weight:800">User</div><div id="bd" style="display:inline-block;padding:6px 14px;border-radius:20px;margin-top:6px">🏅 Bronze</div><input id="pNameIn" style="width:100%;padding:10px;border-radius:10px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:10px"><button class="btn" onclick="saveP()">Save Profile</button><input type="file" id="fi" accept="image/*" style="display:none" onchange="hf(this)"></div>
<div class="card"><button class="btn" onclick="doR()">Ads দেখুন ৳2</button><button class="btn" style="background:#22c55e" onclick="location.href='/admin?id=8807178385'">Admin Panel</button></div>
<script>
let uid='8807178385',img='',s={};let c=0;
function init(){fetch('/api/get?id='+uid).then(r=>r.json()).then(d=>{s=d.settings;let u=d.user;
for(let i=1;i<=5;i++){let im=s['slider_img'+i];if(im)document.getElementById('s'+i).style.backgroundImage='url('+im+')';document.getElementById('st'+i).innerText=s['slider_txt'+i];}
document.getElementById('pc').style.background=s.profile_card_bg;document.getElementById('pc').style.borderColor=s.profile_card_border;document.getElementById('av').style.border='3px solid '+s.avatar_border_color;document.getElementById('pn').style.color=s.profile_name_color;
let b=u.badge||1;let el=document.getElementById('bd');el.innerText=s['badge'+b+'_icon']+' '+s['badge'+b+'_name'];el.style.background=s['badge'+b+'_bg'];el.style.color=s['badge'+b+'_text'];
document.getElementById('pn').innerText=u.name;document.getElementById('pNameIn').value=u.name;
if(u.img){document.getElementById('pAv').src=u.img;document.getElementById('pAv').style.display='block';document.getElementById('pAvT').style.display='none';img=u.img;}
});}
function doR(){fetch('/api/reward?id='+uid).then(()=>init());}
function saveP(){let n=document.getElementById('pNameIn').value;fetch('/api/profile/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,name:n,img:img})}).then(()=>{alert('Save');init();});}
function hf(i){let f=i.files[0];let r=new FileReader();r.onload=e=>{img=e.target.result;document.getElementById('pAv').src=img;document.getElementById('pAv').style.display='block';document.getElementById('pAvT').style.display='none';};r.readAsDataURL(f);}
setInterval(()=>{c=(c+1)%5;document.querySelectorAll('.slide').forEach((e,i)=>e.classList.toggle('active',i==c));},3000);
init();
</script></body></html>
"""
ADMIN="""<html><head><meta name="viewport" content="width=device-width,initial-scale=1.0"><style>body{background:#070710;color:#fff;max-width:700px;margin:0 auto;padding:10px;font-family:system-ui}.card{background:#15152a;border-radius:12px;padding:10px;margin:8px 0} input{width:100%;padding:8px;border-radius:8px;background:#0e0e20;border:1px solid #333;color:#fff;margin-top:4px} input[type=color]{height:40px} label{font-size:11px;color:#aaa}.row{display:grid;grid-template-columns:1fr 1fr;gap:6px}.btn{width:100%;padding:12px;background:#6d4cff;border:none;border-radius:10px;color:#fff;font-weight:800;margin-top:10px}</style></head><body>
<h3 style="text-align:center">Admin - Profile Rong + 5 Badge + 5 Image</h3>
<div class="card"><h4>5 Image Slider - 3sec</h4><label>Img1</label><input id="slider_img1"><label>Txt1</label><input id="slider_txt1"><label>Img2</label><input id="slider_img2"><label>Txt2</label><input id="slider_txt2"><label>Img3</label><input id="slider_img3"><label>Txt3</label><input id="slider_txt3"><label>Img4</label><input id="slider_img4"><label>Txt4</label><input id="slider_txt4"><label>Img5</label><input id="slider_img5"><label>Txt5</label><input id="slider_txt5"></div>
<div class="card"><h4>Profile Rong</h4><div class="row"><div><label>Card BG</label><input type="color" id="profile_card_bg"><input id="profile_card_bg"></div><div><label>Border</label><input type="color" id="profile_card_border"><input id="profile_card_border"></div></div><div class="row"><div><label>Avatar Border</label><input type="color" id="avatar_border_color"></div><div><label>Name Color</label><input type="color" id="profile_name_color"></div></div></div>
<div class="card"><h4>5 Badge Rong</h4>
<label>Badge1 Name</label><input id="badge1_name"><div class="row"><div><label>BG</label><input type="color" id="badge1_bg"></div><div><label>Text</label><input type="color" id="badge1_text"></div></div><label>Icon</label><input id="badge1_icon">
<label>Badge2 Name</label><input id="badge2_name"><div class="row"><div><label>BG</label><input type="color" id="badge2_bg"></div><div><label>Text</label><input type="color" id="badge2_text"></div></div><label>Icon</label><input id="badge2_icon">
<label>Badge3 Name</label><input id="badge3_name"><div class="row"><div><label>BG</label><input type="color" id="badge3_bg"></div><div><label>Text</label><input type="color" id="badge3_text"></div></div><label>Icon</label><input id="badge3_icon">
<label>Badge4 Name</label><input id="badge4_name"><div class="row"><div><label>BG</label><input type="color" id="badge4_bg"></div><div><label>Text</label><input type="color" id="badge4_text"></div></div><label>Icon</label><input id="badge4_icon">
<label>Badge5 Name</label><input id="badge5_name"><div class="row"><div><label>BG</label><input type="color" id="badge5_bg"></div><div><label>Text</label><input type="color" id="badge5_text"></div></div><label>Icon</label><input id="badge5_icon">
</div>
<button class="btn" onclick="saveAll()">SAVE ALL</button><div id="msg" style="text-align:center;color:#22c55e;margin-top:8px"></div>
<script>
function load(){fetch('/api/get?id=8807178385').then(r=>r.json()).then(d=>{for(let k in d.settings){document.querySelectorAll('#'+k).forEach(e=>{if(e)e.value=d.settings[k];});}});}
function saveAll(){let data={};document.querySelectorAll('input').forEach(e=>{if(e.id)data[e.id]=e.value;});fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>{document.getElementById('msg').innerText=d.msg;});}
load();
</script></body></html>
"""
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
