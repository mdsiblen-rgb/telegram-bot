import os, json, time
from flask import Flask, request, jsonify
app = Flask(__name__)
DB = "database.json"

def load_db():
    if not os.path.exists(DB):
        d = {
            "users": {},
            "wds": [],
            "settings": {
                "app_name": "প্রতিদিনের কাজ বিডি",
                "ad_c": 0.5, "ad_p": 0.3, "clim": 30, "plim": 30,
                "min": 200, "ref": 20, "bonus": 20,
                "direct_link": "https://omg10.com/4/11760259",
                "spon_link": "https://google.com",
                "notice": "রাত ১০টার পর Withdraw বন্ধ থাকে\nসকাল ৯টার পর আবার চালু হয়"
            },
            "tasks": [
                {"t": "Visit Company Website", "s": "৳20", "i": "🌐", "link": "https://google.com"},
                {"t": "Watch Video Task", "s": "৳25", "i": "▶️", "link": "https://google.com"}
            ]
        }
        open(DB, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
        return d
    try:
        return json.load(open(DB, "r", encoding="utf-8"))
    except:
        return {"users": {}, "wds": [], "settings": {"app_name": "প্রতিদিনের কাজ বিডি", "ad_c": 0.5, "ad_p": 0.3, "clim": 30, "plim": 30, "min": 200, "ref": 20, "bonus": 20, "direct_link": "https://omg10.com/4/11760259", "spon_link": "https://google.com", "notice": "Notice"}, "tasks": []}

def save_db(db):
    open(DB, "w", encoding="utf-8").write(json.dumps(db, ensure_ascii=False, indent=2))

def get_user(db, uid):
    uid = str(uid)
    now = int(time.time())
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid, "name": "User 4250", "bal": 21.1, "total": 21.1, "diamonds": 2110,
            "c": 0, "p": 0, "refl": 0, "join": "2026-09-15", "img": "",
            "last_reset": now, "method": "bKash"
        }
    u = db["users"][uid]
    # 12 ঘন্টা পর Ads Reset হবে, কিন্তু টাকা Permanent থাকবে
    if now - u.get("last_reset", now) > 43200: # 12 hours = 43200 sec
        u["c"] = 0
        u["p"] = 0
        u["last_reset"] = now
    return u

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin', '*')
    r.headers.add('Access-Control-Allow-Headers', '*')
    r.headers.add('Access-Control-Allow-Methods', '*')
    return r

@app.route('/api/init', methods=['POST'])
def api_init():
    db = load_db()
    uid = str((request.json or {}).get('id', '4250'))
    u = get_user(db, uid)
    save_db(db)
    return jsonify({"user": u, "s": db["settings"], "tasks": db.get("tasks", []), "wds": [x for x in db["wds"] if x["uid"]==uid][-5:]})

@app.route('/api/ads', methods=['POST'])
def api_ads():
    db = load_db()
    j = request.json or {}
    uid = str(j.get('id', '4250'))
    typ = j.get('type', 'c')
    u = get_user(db, uid)
    s = db["settings"]
    if typ == 'c':
        if u["c"] >= s["clim"]:
            return jsonify({"ok": False, "msg": "আজকের Company Ads শেষ, 12 ঘন্টা পর আবার"})
        u["c"] = u["c"] + 1
        u["bal"] = round(u["bal"] + float(s["ad_c"]), 2)
        u["total"] = round(u.get("total", 0) + float(s["ad_c"]), 2)
        u["diamonds"] = u["diamonds"] + 25
    else:
        if u["p"] >= s["plim"]:
            return jsonify({"ok": False, "msg": "আজকের Popup Ads শেষ, 12 ঘন্টা পর আবার"})
        u["p"] = u["p"] + 1
        u["bal"] = round(u["bal"] + float(s["ad_p"]), 2)
        u["total"] = round(u.get("total", 0) + float(s["ad_p"]), 2)
        u["diamonds"] = u["diamonds"] + 15
    save_db(db)
    return jsonify({"ok": True, "msg": "৳ + Diamond যোগ হয়েছে", "user": u})

@app.route('/api/wd', methods=['POST'])
def api_wd():
    db = load_db()
    j = request.json or {}
    uid = str(j.get('id', '4250'))
    u = get_user(db, uid)
    s = db["settings"]
    try:
        amt = int(float(j.get('amt', 0)))
    except:
        amt = 0
    num = j.get('num', '')
    method = j.get('method', 'bKash')
    if amt < s["min"]:
        return jsonify({"ok": False, "msg": "Minimum Withdraw ৳" + str(s["min"])})
    if u["bal"] < amt:
        return jsonify({"ok": False, "msg": "Balance কম আছে"})
    if len(num) < 8:
        return jsonify({"ok": False, "msg": "সঠিক Number দিন"})
    u["bal"] = round(u["bal"] - amt, 2) # টাকা কাটবে কিন্তু permanent database.json এ save হবে
    db["wds"].append({"uid": uid, "name": u["name"], "amt": amt, "num": num, "method": method, "time": time.strftime("%d-%m %H:%M"), "status": "Pending"})
    save_db(db)
    return jsonify({"ok": True, "msg": "Withdraw Request সফল! 24h এ পাবেন"})

@app.route('/api/profile', methods=['POST'])
def api_profile():
    db = load_db()
    j = request.json or {}
    uid = str(j.get('id', '4250'))
    u = get_user(db, uid)
    if j.get('name'):
        u["name"] = str(j.get('name'))[:20]
    if j.get('img'):
        u["img"] = j.get('img') # base64
    save_db(db)
    return jsonify({"ok": True, "msg": "Profile Saved", "user": u})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = load_db()
    if request.method == 'POST':
        f = request.form
        s = db["settings"]
        try:
            if f.get('app_name'): s['app_name'] = f.get('app_name')
            if f.get('ad_c'): s['ad_c'] = float(f.get('ad_c'))
            if f.get('ad_p'): s['ad_p'] = float(f.get('ad_p'))
            if f.get('clim'): s['clim'] = int(f.get('clim'))
            if f.get('plim'): s['plim'] = int(f.get('plim'))
            if f.get('min'): s['min'] = int(f.get('min'))
            if f.get('ref'): s['ref'] = int(f.get('ref'))
            if f.get('direct_link'): s['direct_link'] = f.get('direct_link')
            if f.get('spon_link'): s['spon_link'] = f.get('spon_link')
            if f.get('notice'): s['notice'] = f.get('notice')
            save_db(db)
        except:
            pass
    s = db["settings"]
    admin_html = """
    <body style="background:#0B0E1C;color:#fff;padding:15px;font-family:system-ui;max-width:600px;margin:auto">
    <h2>👑 Admin Panel - APP_NAME</h2>
    <div style="background:#1A2040;padding:15px;border-radius:12px;margin-top:10px">
    <form method="POST">
    App Name: <input name="app_name" value="APP_NAME" style="width:100%;padding:8px;margin:4px 0"><br>
    Company Ad ৳: <input name="ad_c" value="AD_C" type="number" step="0.01"> Limit: <input name="clim" value="CLIM" type="number"><br>
    Popup Ad ৳: <input name="ad_p" value="AD_P" type="number" step="0.01"> Limit: <input name="plim" value="PLIM" type="number"><br>
    Min Withdraw: <input name="min" value="MINW" type="number"> Refer ৳: <input name="ref" value="REFB" type="number"><br>
    Monetag Direct Link: <input name="direct_link" value="DLINK" style="width:100%;padding:8px;margin:4px 0"><br>
    Sponsor Link: <input name="spon_link" value="SLINK" style="width:100%;padding:8px;margin:4px 0"><br>
    Notice: <textarea name="notice" style="width:100%;height:70px">NOTICE_TXT</textarea><br><br>
    <button style="width:100%;padding:12px;background:#8b5cf6;color:#fff;border:none;border-radius:8px;font-weight:800">SAVE ALL - সব কন্ট্রোল Admin থেকে</button>
    </form></div>
    <p style="margin-top:10px">Total Users: UC | Withdraws: WC</p>
    <div>WD_LIST</div>
    </body>
    """
    wd_list = ""
    for w in db["wds"][-20:]:
        wd_list = wd_list + "<div style='background:#151A2D;padding:8px;margin:4px 0;border-radius:8px'>" + w.get("name","") + " - " + str(w.get("amt","")) + "Tk - " + w.get("num","") + " (" + w.get("method","") + ") - " + w.get("status","") + "</div>"

    admin_html = admin_html.replace("APP_NAME", s["app_name"])
    admin_html = admin_html.replace("AD_C", str(s["ad_c"]))
    admin_html = admin_html.replace("AD_P", str(s["ad_p"]))
    admin_html = admin_html.replace("CLIM", str(s["clim"]))
    admin_html = admin_html.replace("PLIM", str(s["plim"]))
    admin_html = admin_html.replace("MINW", str(s["min"]))
    admin_html = admin_html.replace("REFB", str(s["ref"]))
    admin_html = admin_html.replace("DLINK", s["direct_link"])
    admin_html = admin_html.replace("SLINK", s["spon_link"])
    admin_html = admin_html.replace("NOTICE_TXT", s["notice"])
    admin_html = admin_html.replace("UC", str(len(db["users"])))
    admin_html = admin_html.replace("WC", str(len(db["wds"])))
    admin_html = admin_html.replace("WD_LIST", wd_list)
    return admin_html

@app.route('/')
def home():
    db = load_db()
    s = db["settings"]

    tasks_html = ""
    for x in db.get("tasks", []):
        tasks_html = tasks_html + '<div class="list"><div><b>' + x["i"] + ' ' + x["t"] + '</b><br><small style="color:#22c55e">' + x["s"] + '</small></div><button class="go" onclick="window.open(\'' + x.get("link","https://google.com") + '\',\'_blank\')">Go</button></div>'

    html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:130px}
.top{display:flex;gap:8px;padding:12px}
.ib{width:56px;height:56px;background:#151A2D;border:2px solid #8b5cf6;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:32px}
.tt{flex:1;background:#151A2D;border:1px solid #f59e0b;border-radius:14px;padding:10px;font-weight:700;font-size:13px}
.card{background:#1A2040;border:1px solid #1e293b;border-radius:22px;padding:18px;margin:12px}
.bal{color:#22c55e;font-size:40px;font-weight:900}
.list{background:#1A2040;border-radius:18px;padding:14px;margin:10px 12px;display:flex;justify-content:space-between;align-items:center}
.go{background:#8b5cf6;border:none;color:#fff;padding:10px 18px;border-radius:12px;font-weight:700}
.btn{width:100%;padding:14px;border:none;border-radius:14px;font-weight:800;background:#8b5cf6;color:#fff;cursor:pointer}
.btn2{background:#f59e0b;color:#000}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:14px 0 22px;border-radius:24px 24px 0 0;border-top:1px solid #2a2f4a}
.btm div{flex:1;text-align:center;color:#64748b;font-size:13px;font-weight:700;cursor:pointer;padding:4px 0}
.btm div.on{color:#8b5cf6}
.btm div span{font-size:26px;display:block;margin-bottom:3px}
.page{display:none}
.page.active{display:block}
.offer{background:#2D1B4E;border:2px solid #8b5cf6;border-radius:22px;padding:18px;margin:12px}
.notice{background:#1a1500;border:1px solid #f59e0b;border-radius:18px;padding:16px;margin:12px}
.method{flex:1;padding:12px;border-radius:12px;text-align:center;cursor:pointer;font-weight:800;border:2px solid #1e293b;background:#0B0E1C}
.method.on{border-color:#8b5cf6;background:#1A2040;color:#fff}
</style></head><body>

<div id="p1" class="page active">
<div class="top"><div class="ib">💎</div><div class="tt">APP_NAME_TITLE<br>বিডি</div><div class="tt" style="border-color:#f59e0b">Daily Work BD ✅<br><span style="color:#22c55e" id="balTop">৳21.1</span></div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><span style="color:#a78bfa">💎 Diamond Member • Level 1</span><span>Balance<br><b style="color:#22c55e" id="bal1">৳21.1</b></span></div><div class="bal" id="bal2">৳21.1</div><div>💎 <span id="diam1">2110</span> Diamond | <span id="adCount">0</span>/TOTAL_ADS Ads | <small>12h পর Reset</small></div></div>
<div style="display:flex;gap:10px;margin:0 12px">
<div class="card" style="flex:1;margin:0"><b>Company Ads<br><span style="color:#f59e0b">AD_C_TK</span></b><br><small><span id="cCount">0</span>/CLIM_L</small><br><button class="btn" onclick="doAd('c')">Start - AD_C_TK</button></div>
<div class="card" style="flex:1;margin:0"><b>Popup Ads<br><span style="color:#f59e0b">AD_P_TK</span></b><br><small><span id="pCount">0</span>/PLIM_L</small><br><button class="btn btn2" onclick="doAd('p')">Watch - AD_P_TK</button></div>
</div>
<div class="card"><b>💸 Withdraw (Min MIN_TK)</b><button class="btn" style="background:#22c55e;margin-top:10px" onclick="showPage(4)">Withdraw Now</button></div>
<div class="offer"><h2>🔥🔥 Biggest Earning Offer</h2><p>প্রতিদিন কাজ করে আয় করুন, বড় বোনাস নিন</p><button class="btn btn2" style="margin-top:10px" onclick="openSpon()">🚀 Claim Now</button></div>
</div>

<div id="p2" class="page"><div class="top"><div class="ib">🎯</div><div class="tt">Tasks</div><div class="tt">Daily Work BD ✅</div></div><div class="card"><b>🎯 Tasks & Company Links</b></div>TASKS_PLACE</div>

<div id="p3" class="page"><div class="top"><div class="ib">👥</div><div class="tt">Refer</div><div class="tt">Daily Work BD ✅</div></div><div style="background:#f59e0b;color:#000;padding:12px;border-radius:14px;margin:12px;font-weight:800;text-align:center">🎉🎉 Refer Contest চলছে! - ৳5000 পুরস্কার</div><div class="card"><b>👥 Refer & Earn ৳REF_TK</b><div style="background:#0B0E1C;padding:10px;border-radius:10px;font-size:11px;margin-top:8px;word-break:break-all" id="refLink"></div><button class="btn" style="margin-top:10px" onclick="copyRef()">🔗 Copy Refer Link</button><div style="margin-top:8px"><small>Total Refer: <span id="refCount">0</span></small></div></div></div>

<div id="p4" class="page">
<div class="top"><div class="ib">💬</div><div class="tt">Support</div><div class="tt">Daily Work BD ✅</div></div>
<div class="card"><b>💸 Withdraw - Min MIN_TK</b>
<div style="display:flex;gap:10px;margin-top:12px">
<div id="mBkash" class="method on" onclick="setMethod('bKash')">bKash</div>
<div id="mNagad" class="method" onclick="setMethod('Nagad')">Nagad</div>
</div>
<input id="wdNum" placeholder="bKash/Nagad Number - 01XXXXXXXXX" style="width:100%;padding:13px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:10px">
<input id="wdAmt" placeholder="Amount - Min MIN_TK" type="number" style="width:100%;padding:13px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:10px">
<button class="btn" style="background:#22c55e;margin-top:12px" onclick="doWithdraw()">Withdraw Now</button>
<div style="margin-top:12px;font-size:12px;color:#94a3b8">Method: <b id="methodTxt" style="color:#fff">bKash</b> selected</div>
</div>
<div class="card"><b>💸 Withdraw History</b><div id="wdHistory"><small>No withdraw yet</small></div></div>
<div class="notice"><b>📢 Notice Board</b><br><div style="margin-top:8px">NOTICE_BOARD</div></div>
</div>

<div id="p5" class="page">
<div class="top"><div class="ib">👤</div><div class="tt">Profile</div><div class="tt">Daily Work BD ✅ <span id="balTop2">৳21.1</span></div></div>
<div class="card" style="text-align:center"><div class="ib" id="profileImgBox" style="width:90px;height:90px;margin:0 auto;font-size:48px">👤</div><br><h2 id="profileName" style="margin-top:8px">User 4250</h2><div>💎 <span id="diam2">2110</span> Diamond | ৳<span id="totalEarn">21.1</span> Total</div></div>
<div class="card"><b>⚙️ Account - নাম/ছবি গ্যালারি থেকে চেঞ্জ</b><input id="newName" placeholder="নতুন নাম লিখো" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:8px"><input type="file" id="newImg" accept="image/*" style="margin-top:10px"><button class="btn" style="margin-top:10px" onclick="saveProfile()">💾 Save Profile</button></div>
</div>

<div class="btm">
<div class="on" id="b1" onclick="showPage(1)"><span>🏠</span>Home</div>
<div id="b2" onclick="showPage(2)"><span>🎯</span>Tasks</div>
<div id="b3" onclick="showPage(3)"><span>👥</span>Refer</div>
<div id="b4" onclick="showPage(4)"><span>💸</span>Withdraw</div>
<div id="b5" onclick="showPage(5)"><span>👤</span>Profile</div>
</div>

<script>
var tg = window.Telegram.WebApp;
tg.expand();
var uid = "4250";
try { uid = String(tg.initDataUnsafe.user.id); } catch(e){}
var directLink = "DIRECT_LINK";
var sponLink = "SPON_LINK";
var currentMethod = "bKash";
document.getElementById('refLink').innerText = "https://t.me/YourBot?start=" + uid;

function showPage(n){
  var pages = document.querySelectorAll('.page');
  for(var i=0;i<pages.length;i++){ pages[i].classList.remove('active'); }
  document.getElementById('p'+n).classList.add('active');
  var btns = document.querySelectorAll('.btm div');
  for(var i=0;i<btns.length;i++){ btns[i].classList.remove('on'); }
  document.getElementById('b'+n).classList.add('on');
}

function setMethod(m){
  currentMethod = m;
  document.getElementById('mBkash').classList.remove('on');
  document.getElementById('mNagad').classList.remove('on');
  if(m=='bKash'){ document.getElementById('mBkash').classList.add('on'); }
  else{ document.getElementById('mNagad').classList.add('on'); }
  document.getElementById('methodTxt').innerText = m;
}

function openSpon(){ window.open(sponLink, '_blank'); }
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Refer Link Copied'); }

function doAd(t){
  window.open(directLink, '_blank');
  setTimeout(function(){
    fetch('/api/ads', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id:uid, type:t})})
   .then(function(r){ return r.json(); })
   .then(function(j){
      if(j.ok==false){ alert(j.msg); }
      else{ alert('টাকা যোগ হয়েছে - Permanent Save'); init(); }
    });
  }, 2500);
}

function doWithdraw(){
  var num = document.getElementById('wdNum').value;
  var amt = document.getElementById('wdAmt').value;
  if(num.length < 10){ alert('সঠিক bKash/Nagad Number দিন'); return; }
  if(amt==''){ alert('Amount দিন'); return; }
  fetch('/api/wd', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id:uid, num:num, amt:amt, method:currentMethod})})
 .then(function(r){ return r.json(); })
 .then(function(j){ alert(j.msg); if(j.ok){ init(); } });
}

function saveProfile(){
  var name = document.getElementById('newName').value;
  var fileInput = document.getElementById('newImg');
  var imgData = "";
  if(fileInput.files && fileInput.files[0]){
    var reader = new FileReader();
    reader.onload = function(e){
      imgData = e.target.result;
      sendProfile(name, imgData);
    };
    reader.readAsDataURL(fileInput.files[0]);
  } else {
    sendProfile(name, "");
  }
}

function sendProfile(name, img){
  fetch('/api/profile', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id:uid, name:name, img:img})})
 .then(function(r){ return r.json(); })
 .then(function(j){ alert(j.msg); init(); });
}

function init(){
  fetch('/api/init', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id:uid})})
 .then(function(r){ return r.json(); })
 .then(function(d){
    var u = d.user;
    document.getElementById('balTop').innerText = '৳' + u.bal;
    document.getElementById('balTop2').innerText = '৳' + u.bal;
    document.getElementById('bal1').innerText = '৳' + u.bal;
    document.getElementById('bal2').innerText = '৳' + u.bal;
    document.getElementById('diam1').innerText = u.diamonds;
    document.getElementById('diam2').innerText = u.diamonds;
    document.getElementById('totalEarn').innerText = u.total;
    document.getElementById('cCount').innerText = u.c;
    document.getElementById('pCount').innerText = u.p;
    document.getElementById('adCount').innerText = u.c + u.p;
    document.getElementById('profileName').innerText = u.name;
    document.getElementById('refCount').innerText = u.refl;
    if(u.img && u.img!=''){
      document.getElementById('profileImgBox').innerHTML = '<img src="' + u.img + '" style="width:100%;height:100%;object-fit:cover;border-radius:16px">';
    }
    var hist = d.wds || [];
    if(hist.length>0){
      var hHtml = "";
      for(var i=0;i<hist.length;i++){
        hHtml = hHtml + '<div style="background:#0B0E1C;padding:8px;border-radius:8px;margin-top:6px;font-size:12px">' + hist[i].amt + 'Tk - ' + hist[i].num + ' (' + hist[i].method + ') - ' + hist[i].status + '</div>';
      }
      document.getElementById('wdHistory').innerHTML = hHtml;
    }
  });
}
setMethod('bKash');
init();
</script></body></html>
    """
    html = html.replace("APP_NAME_TITLE", s["app_name"])
    html = html.replace("AD_C_TK", "৳" + str(s["ad_c"]))
    html = html.replace("AD_P_TK", "৳" + str(s["ad_p"]))
    html = html.replace("CLIM_L", str(s["clim"]))
    html = html.replace("PLIM_L", str(s["plim"]))
    html = html.replace("TOTAL_ADS", str(s["clim"] + s["plim"]))
    html = html.replace("MIN_TK", str(s["min"]))
    html = html.replace("REF_TK", str(s["ref"]))
    html = html.replace("DIRECT_LINK", s["direct_link"])
    html = html.replace("SPON_LINK", s["spon_link"])
    html = html.replace("NOTICE_BOARD", s["notice"].replace("\n", "<br>"))
    html = html.replace("TASKS_PLACE", tasks_html)
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
