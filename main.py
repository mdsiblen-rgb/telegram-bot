import os, json, time
from flask import Flask, request, jsonify
app = Flask(__name__)
DB="database.json"

def load_db():
    if not os.path.exists(DB):
        d={"users":{},"wds":[],"settings":{
            "app_name":"👑 প্রতিদিনের কাজ বিডি","bonus":20,"ad":0.5,"pop":0.3,"clim":80,"plim":80,"min":200,"ref":20,
            "direct_link":"https://omg10.com/4/11760259","spon_link":"https://google.com",
            "notice":"রাত ১০টার পর Withdraw বন্ধ থাকে\nসকাল ৯টার পর আবার চালু হয়\nFake Account করলে ব্যান"
        },"tasks":[
            {"t":"Visit Company Website - ৳20","s":"৳0.2","i":"🌐"},
            {"t":"Watch Video - ৳25","s":"৳0.25","i":"▶️"},
            {"t":"Join Telegram - ৳30","s":"৳0.3","i":"📢"}
        ]}
        open(DB,"w",encoding="utf-8").write(json.dumps(d,ensure_ascii=False,indent=2))
        return d
    try: return json.load(open(DB,"r",encoding="utf-8"))
    except: return {"users":{},"wds":[],"settings":{"app_name":"প্রতিদিনের কাজ বিডি"},"tasks":[]}

def save_db(db): open(DB,"w",encoding="utf-8").write(json.dumps(db,ensure_ascii=False,indent=2))
def get_user(db,uid):
    uid=str(uid)
    if uid not in db["users"]:
        db["users"][uid]={"id":uid,"name":"User 4250","bal":21.1,"total":21.1,"diamonds":2110,"c":2,"p":0,"refl":0,"join":"2026-09-15","img":""}
    return db["users"][uid]

@app.after_request
def after(r): r.headers.add('Access-Control-Allow-Origin','*'); return r

@app.route('/api/init',methods=['POST'])
def api_init():
    db=load_db(); uid=str((request.json or {}).get('id','4250')); u=get_user(db,uid); save_db(db)
    return jsonify({"user":u,"s":db["settings"],"tasks":db.get("tasks",[])})

@app.route('/')
def home():
    db=load_db(); s=db["settings"]
    tasks=""
    for x in db.get("tasks",[]):
        tasks+=f'<div class="list"><div><b>{x["i"]} {x["t"]}</b><br><small style="color:#22c55e">{x["s"]}</small></div><button class="go">Go</button></div>'

    html=f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}} body{{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:120px}}
.top{{display:flex;gap:8px;padding:12px}}.ib{{width:56px;height:56px;background:#151A2D;border:2px solid #8b5cf6;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:32px}}
.tt{{flex:1;background:#151A2D;border:1px solid #f59e0b;border-radius:14px;padding:10px;font-weight:700;font-size:13px}}
.card{{background:#1A2040;border:1px solid #1e293b;border-radius:22px;padding:18px;margin:12px}}.bal{{color:#22c55e;font-size:40px;font-weight:900}}
.list{{background:#1A2040;border-radius:18px;padding:14px;margin:10px 12px;display:flex;justify-content:space-between;align-items:center}}
.go{{background:#8b5cf6;border:none;color:#fff;padding:10px 18px;border-radius:12px;font-weight:700}}.btn{{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;background:#8b5cf6;color:#fff;cursor:pointer}}
.btm{{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:10px 0 18px;border-radius:22px 22px 0 0;border-top:1px solid #1e293b}}
.btm div{{flex:1;text-align:center;color:#64748b;font-size:12px;cursor:pointer}}.btm div.on{{color:#8b5cf6}}.page{{display:none}}.page.active{{display:block}}
.notice{{background:#1a1500;border:1px solid #f59e0b;border-radius:18px;padding:16px;margin:12px}}.faq{{background:#0B0E1C;border-radius:14px;padding:12px;margin:8px 0}}
.offer{{background:#2D1B4E;border:2px solid #8b5cf6;border-radius:22px;padding:18px;margin:12px}}
</style></head><body>

<div id="p1" class="page active">
<div class="top"><div class="ib">💎</div><div class="tt">👑 প্রতিদিনের কাজ<br>বিডি</div><div class="tt" style="border-color:#f59e0b">Daily Work BD ✅<br><span style="color:#22c55e">৳21.1</span></div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><span style="color:#a78bfa">💎 Diamond Member • Level 1</span><span>Balance<br><b style="color:#22c55e">৳21.1</b></span></div><div class="bal">৳21.1</div><div>💎 2110 Diamond | 2/80 Ads</div></div>
<div style="display:flex;gap:10px;margin:0 12px"><div class="card" style="flex:1;margin:0"><b>Company Ads<br><span style="color:#f59e0b">৳0.5</span></b><br><small>1/80</small><br><button class="btn" onclick="ad()">Start - ৳0.5</button></div><div class="card" style="flex:1;margin:0"><b>Popup Ads<br><span style="color:#f59e0b">৳0.3</span></b><br><small>1/80</small><br><button class="btn" style="background:#f59e0b;color:#000" onclick="ad()">Watch - ৳0.3</button></div></div>
<div class="card"><b>💸 Withdraw</b><div style="display:flex;gap:8px;margin-top:10px"><button class="btn" style="flex:1">bKash</button><button class="btn" style="flex:1;background:#0B0E1C;border:1px solid #2a2f4a">Nagad</button></div><input placeholder="01XXXXXXXXX" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><input placeholder="Min 200" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><button class="btn" style="margin-top:10px">Withdraw Now</button></div>
<div class="offer"><h2>🔥🔥 Biggest Earning Offer</h2><p>প্রতিদিন কাজ করে আয় করুন, বড় বোনাস নিন</p><button class="btn" style="background:#f59e0b;color:#000;margin-top:10px" onclick="window.open('{s['spon_link']}','_blank')">🚀 Claim Now</button></div>
</div>

<div id="p2" class="page">
<div class="top"><div class="ib">🎯</div><div class="tt">Tasks</div><div class="tt">Daily Work BD ✅</div></div>
<div class="card"><b>🎯 Tasks & Company Links</b><br><small>প্রতি Task এ ৳20-25 + Diamond</small></div>
{tasks}
<div class="offer"><h3>🔥 Special Offer</h3><small>এই বক্স Admin থেকে চেঞ্জ হবে</small><br><button class="btn" style="margin-top:10px">Claim Now</button></div>
</div>

<div id="p3" class="page">
<div class="top"><div class="ib">👥</div><div class="tt">Refer</div><div class="tt">Daily Work BD ✅</div></div>
<div style="background:#f59e0b;color:#000;padding:12px;border-radius:14px;margin:12px;font-weight:800;text-align:center">🎉🎉 Refer Contest চলছে! - ৳5000 পুরস্কার</div>
<div class="card"><b>👥 Refer & Earn</b><br><small>বন্ধুদের Invite করে Unlimited আয়</small><div style="display:flex;gap:10px;margin-top:10px"><div class="list" style="flex:1;flex-direction:column;margin:0"><b style="color:#8b5cf6;font-size:24px">0</b><small>Total Refer</small></div><div class="list" style="flex:1;flex-direction:column;margin:0"><b style="color:#22c55e;font-size:24px">৳20</b><small>Per Refer</small></div></div><div style="background:#0B0E1C;padding:10px;border-radius:10px;font-size:12px;margin-top:10px;word-break:break-all">https://telegram-bot-1-v77g.onrender.com/?ref=8807178385_4250</div><button class="btn" style="margin-top:10px">🔗 Copy Refer Link</button><div style="margin-top:10px;font-size:14px">1. বন্ধুকে লিংক শেয়ার করো<br>2. বন্ধু Join করলে ৳20 পাবে<br>3. বন্ধু Ads দেখলে 15% Commission পাবে</div></div>
<div class="card" style="background:linear-gradient(135deg,#0a2e0a,#123e12);border-color:#22c55e"><b>🔥 Refer Special Bonus</b><br><small>এখানে Admin থেকে যেকোনো লিংক/অফার লিখতে পারবে</small><br><button class="btn" style="background:#22c55e;margin-top:10px">Join Now</button></div>
</div>

<div id="p4" class="page">
<div class="top"><div class="ib">💬</div><div class="tt">Support</div><div class="tt">Daily Work BD ✅</div></div>
<div class="card"><b>💎 Support Center</b><br><small>যেকোনো সমস্যায় যোগাযোগ করুন - 24/7</small></div>
<div class="card"><b>📞 Contact Us</b><div style="display:flex;gap:10px;margin:10px 0"><button class="btn" style="flex:1;background:#8b5cf6">✈️ Telegram</button><button class="btn" style="flex:1;background:#f59e0b;color:#000">💬 WhatsApp</button></div><div style="background:#0B0E1C;padding:10px;border-radius:10px">📧 support@dailyworkbd.com</div></div>
<div class="notice"><b>📢 Notice Board</b><br><div style="margin-top:8px">⚠️ রাত ১০টার পর Withdraw বন্ধ থাকে<br>✅ সকাল ৯টার পর আবার চালু হয়<br>📢 Fake Account করলে ব্যান</div></div>
<div class="card"><b>❓ FAQ</b><div class="faq"><b>▶️ Withdraw কতক্ষণে পাবো?</b><br><small>২৪ ঘণ্টার ভিতরে পেমেন্ট করা হয়</small></div><div class="faq"><b>▶️ Refer টাকা কখন পাবো?</b><br><small>বন্ধু Join করলেই সাথে সাথে</small></div><div class="faq"><b>▶️ Ads দেখলে টাকা আসে না কেন?</b><br><small>VPN বন্ধ করে আবার চেষ্টা করুন</small></div></div>
<div class="card"><b>📜 Rules</b><br><div style="margin-top:8px;line-height:1.8">1. একাধিক একাউন্ট খুলবেন না<br>2. ভুল তথ্য দিবেন না<br>3. Fake Refer করবেন না<br>4. Admin এর সিদ্ধান্তই চূড়ান্ত</div></div>
<div class="card" style="background:#0a2e2e;border-color:#06b6d4"><b>📢 Important Update</b><br><small>এই জায়গাটা Admin থেকে কন্ট্রোল করতে পারবে</small><br><button class="btn" style="background:#06b6d4;color:#000;margin-top:10px">Contact Now</button></div>
</div>

<div id="p5" class="page">
<div class="top"><div class="ib">👤</div><div class="tt">Profile</div><div class="tt">Daily Work BD ✅ ৳21.1</div></div>
<div class="card" style="text-align:center"><div class="ib" style="width:90px;height:90px;margin:0 auto;font-size:48px">👤</div><br><span style="background:#f59e0b;color:#000;padding:4px 12px;border-radius:20px;font-weight:700;font-size:12px">Level 1</span><br><h2 style="margin-top:8px">User 4250</h2><small>Join: 2026-09-15</small><br><div style="margin-top:6px">💎 2110 Diamond | 21.1 Taka</div></div>
<div class="card"><b>📊 Statistics</b><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px"><div class="list" style="flex-direction:column;margin:0"><b style="color:#22c55e">৳21.1</b><small>Total Earned</small></div><div class="list" style="flex-direction:column;margin:0"><b style="color:#8b5cf6">৳21.1</b><small>Balance</small></div><div class="list" style="flex-direction:column;margin:0"><b style="color:#f59e0b">2</b><small>Ads</small></div><div class="list" style="flex-direction:column;margin:0"><b style="color:#ec4899">0</b><small>Refer</small></div></div></div>
<div class="card"><b>⚙️ Account - নাম/ছবি গ্যালারি থেকে</b><input value="8807178385_4250" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><input value="User 4250" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><div style="display:flex;gap:10px;margin-top:8px"><input type="file" style="flex:1"></div><button class="btn" style="margin-top:10px">💾 Save Profile</button></div>
<div class="card"><b>💸 Withdraw History</b><br><small>No withdraw</small></div>
<div class="offer"><b>💎 VIP Membership - বড় বক্স</b><br><small>VIP হলে বেশি ইনকাম পাবেন। Admin থেকে অফার লিখুন</small><br><button class="btn" style="margin-top:10px">⭐ Upgrade Now</button></div>
</div>

<div class="btm">
<div class="on" onclick="showP(1,this)"><span>🏠</span>Home</div>
<div onclick="showP(2,this)"><span>🎯</span>Tasks</div>
<div onclick="showP(3,this)"><span>👥</span>Refer</div>
<div onclick="showP(4,this)"><span>💬</span>Support</div>
<div onclick="showP(5,this)"><span>👤</span>Profile</div>
</div>
<script>
let tg=window.Telegram.WebApp;tg.expand();
function showP(n,el){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.getElementById('p'+n).classList.add('active');document.querySelectorAll('.btm div').forEach(d=>d.classList.remove('on'));el.classList.add('on');}
function ad(){{window.open('{s['direct_link']}','_blank');}}
</script></body></html>
    """
    return html

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
