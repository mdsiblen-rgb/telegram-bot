# ADMIN PANEL BEAUTIFUL - ALL FIELDS FILLED - COPY ONE BY ONE - 8807178385
import os, json
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN_ID = "8807178385"
TOKEN = "11764581"

def default_db():
    return {
        "users": {"8807178385":{"id":"8807178385","name":"User 8807178385","bal":60,"ads":0,"ref_c":0,"w_total":0}},
        "withdraws": [],
        "settings": {
            "app_title": f"প্রতিদিনের কাজ BD - {TOKEN} - {ADMIN_ID}",
            "notice_title": f"অফিসিয়াল নোটিস - {TOKEN}",
            "notice_desc": f"প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন - প্রতিদিন ৳500 পর্যন্ত ইনকাম - Token {TOKEN} - Admin {ADMIN_ID}",
            "mini_title": "স্পেশাল অফার - Mini Boy Ads",
            "mini_btn": f"ADS দেখুন - Token {TOKEN}",
            "zone_text": f"Zone: {TOKEN} - Token {TOKEN} - Admin {ADMIN_ID}",
            "wallet_title": f"Wallet - {ADMIN_ID}",
            "wallet_min": f"Min: ৳1000 - Token {TOKEN}",
            "bkash_text": f"bKash - {TOKEN}",
            "nagad_text": f"Nagad - {TOKEN}",
            "withdraw_btn": f"Withdraw - {TOKEN}",
            "live_title": "Live Withdraw - সবাই কত তুলছে - Auto",
            "live_desc": f"কেউ Withdraw করলেই এখানে Auto ভাসবে - Token {TOKEN} - Admin {ADMIN_ID}",
            "live_empty": f"এখনো কেউ Withdraw করেনি - Token {TOKEN}",
            "rules_title": f"Withdraw নিয়ম - Admin থেকে Change করতে পারবেন - {TOKEN}",
            "rules_text": f"১. Minimum ৳1000 হলে Withdraw দিতে পারবেন\n২. bKash / Nagad Number সঠিক ভাবে দিন\n৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন\n৪. ভুল Number দিলে টাকা পাবেন না, দায় আপনার\n৫. একাধিক Account করলে Ban হবেন",
            "warning": f"সতর্কতা: একাধিক Account করলে Ban হবেন। Fake Refer করলে Balance 0 করে দেওয়া হবে। ভুল Number এ টাকা গেলে Admin দায়ী নয়। - Admin {ADMIN_ID} - Token {TOKEN}",
            "mini_ad_btn2": f"Mini Boy Ad দেখুন - {TOKEN}",
            "refer_title": f"Refer & Earn ৳20 - {TOKEN}",
            "refer_desc": f"আপনার লিংক শেয়ার করুন - প্রতি রেফারে ৳20 পাবেন - বন্ধু 60 টাকা বোনাস পাবে - Admin {ADMIN_ID} - Token {TOKEN}",
            "profile_title": f"Profile - {ADMIN_ID} - {TOKEN}",
            "support_title": f"সাপোর্ট সেন্টার - {ADMIN_ID}",
            "support_desc": f"যেকোনো সমস্যায় যোগাযোগ করুন - Telegram: @ProtidinerKajBD - Admin ID {ADMIN_ID} - Token {TOKEN}",
            "slider": [
                {"img":"https://i.ibb.co.com/nsT0W7r6/gaming1.jpg","link":"https://t.me"},
                {"img":"https://i.ibb.co.com/0y0L0p0/rocket.png","link":"https://youtube.com"},
                {"img":"https://picsum.photos/600/300?random=10","link":"https://facebook.com"},
                {"img":"https://picsum.photos/600/300?random=11","link":"https://t.me"},
                {"img":"https://picsum.photos/600/300?random=12","link":"https://google.com"},
                {"img":"https://picsum.photos/600/300?random=13","link":"https://t.me"}
            ]
        },
        "tasks": [
            {"title":"YouTube Subscribe","reward":25,"link":"https://youtube.com","color":"#dc2626","btn":f"Join & Get 25 Tk - {TOKEN}"},
            {"title":"Telegram Join","reward":10,"link":"https://t.me","color":"#1e40af","btn":f"Join & Get 10 Tk - {TOKEN}"},
            {"title":"Facebook Follow","reward":15,"link":"https://facebook.com","color":"#0ea5e9","btn":f"Follow & Get 15 Tk - {TOKEN}"},
            {"title":"Website Visit","reward":20,"link":"https://google.com","color":"#7c3aed","btn":f"Visit & Get 20 Tk - {TOKEN}"}
        ]
    }

def load_db():
    if not os.path.exists(DB_FILE):
        d=default_db(); save_db(d); return d
    try:
        with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
    except:
        d=default_db(); save_db(d); return d

def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2,ensure_ascii=False)

@app.route('/')
def home():
    return render_template_string("<h2 style='color:#fff;background:#0a1229;padding:20px;text-align:center'>User App - Go to /admin?id=8807178385 for Admin - Token 11764581</h2>")

@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN_ID: return f"Need?id={ADMIN_ID}"
    return render_template_string(ADMIN_PAGE)

@app.route('/api/admin/db')
def adb(): return jsonify(load_db())

@app.route('/api/admin/save',methods=['POST'])
def asave():
    db=load_db(); j=request.json
    db["settings"].update(j.get("settings",{}))
    if "tasks" in j: db["tasks"]=j["tasks"]
    if "slider" in j: db["settings"]["slider"]=j["slider"]
    save_db(db)
    return jsonify({"msg":"Saved - Live"})

ADMIN_PAGE = '''
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a1020;color:#fff;font-family:sans-serif;padding:12px;max-width:500px;margin:0 auto}
h2{color:#22c55e;font-size:22px;text-align:center;margin:12px 0}
.card{background:#151f35;border:1px solid #1e2d4f;border-radius:16px;padding:14px;margin:12px 0}
.label{color:#38bdf8;font-size:12px;margin:14px 0 6px 0;display:flex;justify-content:space-between;align-items:center}
.input{background:#0a1229;border:1px solid #2a3a5f;border-radius:10px;padding:12px;width:100%;color:#fff;outline:none}
.input:focus{border-color:#22c55e;box-shadow:0 0 8px rgba(34,197,94,0.3)}
textarea.input{min-height:90px;resize:vertical}
.copy{font-size:11px;background:#1e293b;border:1px solid #334155;padding:4px 8px;border-radius:6px;cursor:pointer;color:#22c55e}
.section{font-weight:900;font-size:16px;margin-bottom:10px;display:flex;gap:8px;align-items:center}
.btn-save{width:100%;padding:16px;background:linear-gradient(90deg,#22c55e,#16a34a);border:0;border-radius:14px;font-weight:900;color:#fff;font-size:16px;cursor:pointer;position:fixed;bottom:10px;left:50%;transform:translateX(-50%);max-width:480px;z-index:99;box-shadow:0 -4px 20px rgba(0,0,0,0.5)}
.btn-add{background:#22c55e;width:100%;padding:12px;border:0;border-radius:10px;font-weight:800;color:#fff;margin-top:10px}
.slide-item{background:#0a1229;padding:10px;border-radius:12px;margin:8px 0;border:1px solid #1e2d4f}
</style></head><body>
<h2>ADMIN FULL CONTROL<br>8807178385 - Token 11764581</h2>
<p style="text-align:center;opacity:0.6;font-size:13px">এখানে যা লিখবে App এ Live হবে - সবুজ বাতি মিটমিট, Slider, সব লেখা</p>

<div class="card">
<div class="section">📝 সব লেখা Control - একটা একটা Copy করো</div>

<div class="label">App Title (উপরে) <span class="copy" onclick="copyVal('app_title')">Copy</span></div>
<input class="input" id="app_title" value="প্রতিদিনের কাজ BD - 11764581 - 8807178385">

<div class="label">Notice Title <span class="copy" onclick="copyVal('notice_title')">Copy</span></div>
<input class="input" id="notice_title" value="অফিসিয়াল নোটিস - 11764581">

<div class="label">Notice Desc <span class="copy" onclick="copyVal('notice_desc')">Copy</span></div>
<textarea class="input" id="notice_desc">প্রতিদিন Ads দেখুন এবং টাস্ক কমপ্লিট করুন - প্রতিদিন ৳500 পর্যন্ত ইনকাম - Token 11764581 - Admin 8807178385</textarea>

<div class="label">Mini Title - Special Offer <span class="copy" onclick="copyVal('mini_title')">Copy</span></div>
<input class="input" id="mini_title" value="স্পেশাল অফার - Mini Boy Ads">

<div class="label">Mini Button Text <span class="copy" onclick="copyVal('mini_btn')">Copy</span></div>
<input class="input" id="mini_btn" value="ADS দেখুন - Token 11764581">

<div class="label">Zone Text <span class="copy" onclick="copyVal('zone_text')">Copy</span></div>
<input class="input" id="zone_text" value="Zone: 11764581 - Token 11764581 - Admin 8807178385">

<div class="label">Wallet Title <span class="copy" onclick="copyVal('wallet_title')">Copy</span></div>
<input class="input" id="wallet_title" value="Wallet - 8807178385">

<div class="label">Wallet Min Text <span class="copy" onclick="copyVal('wallet_min')">Copy</span></div>
<input class="input" id="wallet_min" value="Min: ৳1000 - Token 11764581">

<div class="label">bKash Text <span class="copy" onclick="copyVal('bkash_text')">Copy</span></div>
<input class="input" id="bkash_text" value="bKash - 11764581">

<div class="label">Nagad Text <span class="copy" onclick="copyVal('nagad_text')">Copy</span></div>
<input class="input" id="nagad_text" value="Nagad - 11764581">

<div class="label">Withdraw Button <span class="copy" onclick="copyVal('withdraw_btn')">Copy</span></div>
<input class="input" id="withdraw_btn" value="Withdraw - 11764581">

<div class="label">Live Title <span class="copy" onclick="copyVal('live_title')">Copy</span></div>
<input class="input" id="live_title" value="Live Withdraw - সবাই কত তুলছে - Auto">

<div class="label">Live Desc <span class="copy" onclick="copyVal('live_desc')">Copy</span></div>
<input class="input" id="live_desc" value="কেউ Withdraw করলেই এখানে Auto ভাসবে - Token 11764581 - Admin 8807178385">

<div class="label">Live Empty Text <span class="copy" onclick="copyVal('live_empty')">Copy</span></div>
<input class="input" id="live_empty" value="এখনো কেউ Withdraw করেনি - Token 11764581">

<div class="label">Rules Title <span class="copy" onclick="copyVal('rules_title')">Copy</span></div>
<input class="input" id="rules_title" value="Withdraw নিয়ম - Admin থেকে Change করতে পারবেন - 11764581">

<div class="label">Rules Text (Withdraw নিয়ম) <span class="copy" onclick="copyVal('rules_text')">Copy</span></div>
<textarea class="input" id="rules_text" style="min-height:140px">১. Minimum ৳1000 হলে Withdraw দিতে পারবেন
২. bKash / Nagad Number সঠিক ভাবে দিন
৩. ২৪ ঘণ্টার মধ্যে পেমেন্ট পাবেন
৪. ভুল Number দিলে টাকা পাবেন না, দায় আপনার
৫. একাধিক Account করলে Ban হবেন

এই লেখাটি Admin Panel থেকে যেকোনো সময় Change করতে পারবেন - Token 11764581 - Admin ID 8807178385</textarea>

<div class="label">Warning Text <span class="copy" onclick="copyVal('warning')">Copy</span></div>
<textarea class="input" id="warning">সতর্কতা: একাধিক Account করলে Ban হবেন। Fake Refer করলে Balance 0 করে দেওয়া হবে। ভুল Number এ টাকা গেলে Admin দায়ী নয়। - Admin 8807178385 - Token 11764581</textarea>

<div class="label">Mini Ad Button 2 <span class="copy" onclick="copyVal('mini_ad_btn2')">Copy</span></div>
<input class="input" id="mini_ad_btn2" value="Mini Boy Ad দেখুন - 11764581">

<div class="label">Refer Title <span class="copy" onclick="copyVal('refer_title')">Copy</span></div>
<input class="input" id="refer_title" value="Refer & Earn ৳20 - 11764581">

<div class="label">Refer Desc <span class="copy" onclick="copyVal('refer_desc')">Copy</span></div>
<textarea class="input" id="refer_desc">আপনার লিংক শেয়ার করুন - প্রতি রেফারে ৳20 পাবেন - বন্ধু 60 টাকা বোনাস পাবে - Admin 8807178385 - Token 11764581
কিভাবে রেফার কাজ করে?
১. লিংক Copy করুন
২. বন্ধুকে পাঠান
৩. বন্ধু Join করলে টাকা পাবেন</textarea>

<div class="label">Profile Title <span class="copy" onclick="copyVal('profile_title')">Copy</span></div>
<input class="input" id="profile_title" value="Profile - 8807178385 - 11764581">

<div class="label">Support Title <span class="copy" onclick="copyVal('support_title')">Copy</span></div>
<input class="input" id="support_title" value="সাপোর্ট সেন্টার - 8807178385">

<div class="label">Support Desc <span class="copy" onclick="copyVal('support_desc')">Copy</span></div>
<textarea class="input" id="support_desc">যেকোনো সমস্যায় যোগাযোগ করুন - Telegram: @ProtidinerKajBD - Admin ID 8807178385 - Token 11764581
২৪ ঘণ্টা Support - দ্রুত Reply পাবেন</textarea>
</div>

<div class="card">
<div class="section">🖼️ উপরে Slider - 6 টা ছবি - 2 সেকেন্ড পর পর - Auto</div>
<div id="sliderBox"></div>
<button class="btn-add" onclick="addSlide()">+ Add Slider Image - 6 টা ছবি চলবে</button>
</div>

<div class="card">
<div class="section">📋 Tasks - সব লিংক + টাকা + বাটন Text Control</div>
<div id="tasksBox"></div>
<button class="btn-add" onclick="addTask()">+ Add Task - নতুন Task যোগ করো</button>
</div>

<div class="card">
<div class="section">💸 Live Withdraw List - কে কত তুলছে</div>
<div id="wList" style="font-size:12px"></div>
</div>

<div style="height:80px"></div>
<button class="btn-save" onclick="saveAll()">💾 SAVE ALL - LIVE করো</button>

<script>
let DB={};
function copyVal(id){
let el=document.getElementById(id);
el.select();
navigator.clipboard.writeText(el.value).then(()=>alert('Copied: '+id));
}
function load(){
fetch('/api/admin/db?id=8807178385').then(r=>r.json()).then(d=>{
DB=d;
for(let k in d.settings){
if(k=='slider')continue;
let el=document.getElementById(k);
if(el&&d.settings[k])el.value=d.settings[k];
}
let sHtml='';
d.settings.slider.forEach((s,i)=>{
sHtml+='<div class="slide-item"><b>Image '+(i+1)+' - 2s পর পর</b> <span class="copy" style="float:right" onclick="delSlide('+i+')">Delete</span><div class="label">Image URL</div><input class="input" id="slide_img_'+i+'" value="'+s.img+'"><div class="label">Link (Click করলে যাবে)</div><input class="input" id="slide_link_'+i+'" value="'+s.link+'"><img src="'+s.img+'" style="width:100%;height:80px;object-fit:cover;border-radius:8px;margin-top:6px"></div>';
});
document.getElementById('sliderBox').innerHTML=sHtml;

let tHtml='';
d.tasks.forEach((t,i)=>{
tHtml+='<div class="slide-item"><b>Task '+(i+1)+'</b> <span class="copy" style="float:right" onclick="delTask('+i+')">Delete</span><div class="label">Title</div><input class="input" id="t_title_'+i+'" value="'+t.title+'"><div class="label">Reward ৳</div><input class="input" id="t_reward_'+i+'" type="number" value="'+t.reward+'"><div class="label">Link</div><input class="input" id="t_link_'+i+'" value="'+t.link+'"><div class="label">Button Color (ex: #dc2626)</div><input class="input" id="t_color_'+i+'" value="'+t.color+'"><div class="label">Button Text</div><input class="input" id="t_btn_'+i+'" value="'+t.btn+'"></div>';
});
document.getElementById('tasksBox').innerHTML=tHtml;

let wHtml='';
if(d.withdraws.length==0)wHtml='এখনো কেউ Withdraw করেনি';
else d.withdraws.slice(-10).reverse().forEach(w=>{wHtml+='<div style="padding:6px;border-bottom:1px solid #1e2d4f">ID:'+w.uid+' - '+w.method+' '+w.number+' - ৳'+w.amount+'</div>';});
document.getElementById('wList').innerHTML=wHtml;
});
}
function addSlide(){DB.settings.slider.push({img:"https://picsum.photos/600/300?random="+Date.now(),link:"https://t.me"});saveTemp();load();}
function delSlide(i){DB.settings.slider.splice(i,1);saveTemp();}
function addTask(){DB.tasks.push({title:"New Task",reward:20,link:"https://t.me",color:"#2563eb",btn:"Join & Get 20 Tk - 11764581"});load();}
function delTask(i){DB.tasks.splice(i,1);saveTemp();}
function saveTemp(){
let slider=[];for(let i=0;i<DB.settings.slider.length;i++){let im=document.getElementById('slide_img_'+i);if(!im)continue;slider.push({img:im.value,link:document.getElementById('slide_link_'+i).value});}
let tasks=[];for(let i=0;i<DB.tasks.length;i++){let tt=document.getElementById('t_title_'+i);if(!tt)continue;tasks.push({title:tt.value,reward:parseInt(document.getElementById('t_reward_'+i).value)||20,link:document.getElementById('t_link_'+i).value,color:document.getElementById('t_color_'+i).value,btn:document.getElementById('t_btn_'+i).value});}
fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:DB.settings,tasks:tasks,slider:slider})});
}
function saveAll(){
let settings={};
["app_title","notice_title","notice_desc","mini_title","mini_btn","zone_text","wallet_title","wallet_min","bkash_text","nagad_text","withdraw_btn","live_title","live_desc","live_empty","rules_title","rules_text","warning","mini_ad_btn2","refer_title","refer_desc","profile_title","support_title","support_desc"].forEach(k=>{
let el=document.getElementById(k);if(el)settings[k]=el.value;
});
let slider=[];for(let i=0;i<DB.settings.slider.length;i++){let im=document.getElementById('slide_img_'+i);if(!im)continue;slider.push({img:im.value,link:document.getElementById('slide_link_'+i).value});}
let tasks=[];for(let i=0;i<DB.tasks.length;i++){let tt=document.getElementById('t_title_'+i);if(!tt)continue;tasks.push({title:tt.value,reward:parseInt(document.getElementById('t_reward_'+i).value)||20,link:document.getElementById('t_link_'+i).value,color:document.getElementById('t_color_'+i).value,btn:document.getElementById('t_btn_'+i).value});}
fetch('/api/admin/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({settings:settings,tasks:tasks,slider:slider})}).then(()=>{alert('✅ SAVE DONE - সব Live - সবুজ বাতি মিটমিট করছে');load();});
}
load();
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
