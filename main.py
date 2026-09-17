import os, json, time
from flask import Flask, request, jsonify
app = Flask(__name__)
DB = "/data/database.json" if os.path.exists("/data") else "database.json"

def load_db():
    if not os.path.exists(DB):
        d = {"users": {}, "wds": [], "settings": {"app_name": "প্রতিদিনের কাজ বিডি", "ad_c": 0.5, "ad_p": 0.3, "clim": 30, "plim": 30, "min": 200, "ref": 20, "direct_link": "https://omg10.com/4/11760259", "spon_link": "https://google.com", "notice": "রাত ১০টার পর Withdraw বন্ধ"}, "tasks": []}
        open(DB, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
        return d
    try:
        return json.load(open(DB, "r", encoding="utf-8"))
    except:
        return {"users": {}, "wds": [], "settings": {"app_name": "প্রতিদিনের কাজ বিডি", "ad_c": 0.5, "ad_p": 0.3, "clim": 30, "plim": 30, "min": 200, "ref": 20, "direct_link": "https://omg10.com/4/11760259", "spon_link": "https://google.com", "notice": "Notice"}, "tasks": []}

def save_db(db):
    open(DB, "w", encoding="utf-8").write(json.dumps(db, ensure_ascii=False, indent=2))

def get_user(db, uid):
    uid = str(uid)
    now = int(time.time())
    if uid not in db["users"]:
        db["users"][uid] = {"id": uid, "name": "User 4250", "bal": 21.1, "total": 21.1, "diamonds": 2110, "c": 0, "p": 0, "last_reset": now}
    u = db["users"][uid]
    if now - u.get("last_reset", now) > 43200:
        u["c"] = 0
        u["p"] = 0
        u["last_reset"] = now
    return u

@app.after_request
def after(r):
    r.headers.add('Access-Control-Allow-Origin', '*')
    return r

@app.route('/api/init', methods=['POST'])
def api_init():
    db = load_db()
    uid = str((request.json or {}).get('id', '4250'))
    u = get_user(db, uid)
    save_db(db)
    return jsonify({"user": u, "s": db["settings"]})

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
            return jsonify({"ok": False, "msg": "Limit sesh"})
        u["c"] += 1
        u["bal"] = round(u["bal"] + float(s["ad_c"]), 2)
        u["diamonds"] += 25
    else:
        if u["p"] >= s["plim"]:
            return jsonify({"ok": False, "msg": "Limit sesh"})
        u["p"] += 1
        u["bal"] = round(u["bal"] + float(s["ad_p"]), 2)
        u["diamonds"] += 15
    save_db(db)
    return jsonify({"ok": True, "user": u})

@app.route('/api/wd', methods=['POST'])
def api_wd():
    db = load_db()
    j = request.json or {}
    uid = str(j.get('id', '4250'))
    u = get_user(db, uid)
    s = db["settings"]
    amt = int(float(j.get('amt', 0)))
    if amt < s["min"]:
        return jsonify({"ok": False, "msg": "Min ৳" + str(s["min"])})
    if u["bal"] < amt:
        return jsonify({"ok": False, "msg": "Balance kom"})
    u["bal"] = round(u["bal"] - amt, 2)
    db["wds"].append({"uid": uid, "amt": amt, "num": j.get('num',''), "method": j.get('method','bKash')})
    save_db(db)
    return jsonify({"ok": True, "msg": "Withdraw Success"})

@app.route('/admin', methods=['GET','POST'])
def admin():
    db = load_db()
    s = db["settings"]
    if request.method == 'POST':
        f = request.form
        if f.get('app_name'): s['app_name'] = f.get('app_name')
        if f.get('ad_c'): s['ad_c'] = float(f.get('ad_c'))
        if f.get('ad_p'): s['ad_p'] = float(f.get('ad_p'))
        if f.get('clim'): s['clim'] = int(f.get('clim'))
        if f.get('plim'): s['plim'] = int(f.get('plim'))
        if f.get('min'): s['min'] = int(f.get('min'))
        if f.get('direct_link'): s['direct_link'] = f.get('direct_link')
        if f.get('spon_link'): s['spon_link'] = f.get('spon_link')
        save_db(db)
    h = "<body style='background:#0B0E1C;color:#fff;padding:15px;max-width:500px;margin:auto;font-family:system-ui'><h2>Admin Panel</h2><form method='POST' style='background:#1A2040;padding:15px;border-radius:12px'><input name='app_name' value='APP_NAME' style='width:100%;padding:8px'><br><br>Company Ad <input name='ad_c' value='AD_C' type='number' step='0.1'> Limit <input name='clim' value='CLIM' type='number'><br><br>Popup Ad <input name='ad_p' value='AD_P' type='number' step='0.1'> Limit <input name='plim' value='PLIM' type='number'><br><br>Min WD <input name='min' value='MINW' type='number'><br><br>Direct Link <input name='direct_link' value='DLINK' style='width:100%'><br><br>Sponsor Link <input name='spon_link' value='SLINK' style='width:100%'><br><br><button style='width:100%;padding:12px;background:#8b5cf6;color:#fff;border:none;border-radius:8px'>SAVE</button></form></body>"
    h = h.replace("APP_NAME", s["app_name"]).replace("AD_C", str(s["ad_c"])).replace("AD_P", str(s["ad_p"])).replace("CLIM", str(s["clim"])).replace("PLIM", str(s["plim"])).replace("MINW", str(s["min"])).replace("DLINK", s["direct_link"]).replace("SLINK", s["spon_link"])
    return h

@app.route('/')
def home():
    db = load_db()
    s = db["settings"]
    html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0B0E1C;color:#fff;max-width:430px;margin:auto;padding-bottom:130px}
.top{display:flex;gap:8px;padding:12px}
.ib{width:56px;height:56px;background:#151A2D;border:2px solid #8b5cf6;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:30px}
.tt{flex:1;background:#151A2D;border:1px solid #f59e0b;border-radius:14px;padding:10px;font-weight:700;font-size:13px}
.card{background:#1A2040;border-radius:22px;padding:18px;margin:12px}
.bal{color:#22c55e;font-size:40px;font-weight:900}
.btn{width:100%;padding:15px;border:none;border-radius:14px;font-weight:800;background:#8b5cf6;color:#fff;font-size:15px}
.btn2{background:#f59e0b;color:#000}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#151A2D;display:flex;padding:14px 0 22px;border-radius:24px 24px 0 0;border-top:1px solid #2a2f4a}
.btm div{flex:1;text-align:center;color:#64748b;font-size:14px;font-weight:700}
.btm div.on{color:#8b5cf6}
.btm div span{font-size:28px;display:block;margin-bottom:4px}
.page{display:none}.page.active{display:block}
.method{flex:1;padding:14px;border-radius:12px;text-align:center;font-weight:800;border:2px solid #1e293b;background:#0B0E1C;cursor:pointer}
.method.on{border-color:#8b5cf6;background:#1A2040}
</style></head><body>

<div id="p1" class="page active">
<div class="top"><div class="ib">💎</div><div class="tt">APP_NAME<br>বিডি</div><div class="tt">Daily Work BD ✅<br><span style="color:#22c55e" id="balTop">৳21.1</span></div></div>
<div class="card"><div style="color:#a78bfa">💎 Diamond Member</div><div class="bal" id="bal1">৳21.1</div><div>💎 <span id="diam1">2110</span> | <span id="adCount">0</span> Ads - 12h Reset</div></div>
<div style="display:flex;gap:10px;margin:0 12px">
<div class="card" style="flex:1;margin:0"><b>Company<br><span style="color:#f59e0b">AD_C_TK</span></b><br><small><span id="cCount">0</span>/CLIM_L</small><br><button class="btn" onclick="doAd('c')">Start</button></div>
<div class="card" style="flex:1;margin:0"><b>Popup<br><span style="color:#f59e0b">AD_P_TK</span></b><br><small><span id="pCount">0</span>/PLIM_L</small><br><button class="btn btn2" onclick="doAd('p')">Watch</button></div>
</div>
<div class="card"><button class="btn" style="background:#22c55e" onclick="showPage(4)">Withdraw - Min MIN_TK</button></div>
</div>

<div id="p2" class="page"><div class="top"><div class="ib">🎯</div><div class="tt">Tasks</div></div><div class="card"><b>🎯 Tasks</b><br>Company Links - Admin থেকে Control</div></div>
<div id="p3" class="page"><div class="top"><div class="ib">👥</div><div class="tt">Refer</div></div><div class="card"><b>Refer & Earn</b><div id="refLink" style="background:#0B0E1C;padding:10px;border-radius:10px;margin-top:8px;font-size:11px;word-break:break-all"></div><button class="btn" style="margin-top:10px" onclick="copyRef()">Copy Link</button></div></div>
<div id="p4" class="page"><div class="top"><div class="ib">💸</div><div class="tt">Withdraw</div></div><div class="card"><b>Withdraw Min MIN_TK</b><div style="display:flex;gap:10px;margin-top:12px"><div id="mBkash" class="method on" onclick="setMethod('bKash')">bKash</div><div id="mNagad" class="method" onclick="setMethod('Nagad')">Nagad</div></div><input id="wdNum" placeholder="01XXXXXXXXX" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:10px"><input id="wdAmt" placeholder="Amount" type="number" style="width:100%;padding:12px;border-radius:12px;background:#0B0E1C;border:1px solid #2a2f4a;color:#fff;margin-top:10px"><button class="btn" style="background:#22c55e;margin-top:12px" onclick="doWd()">Withdraw Now</button><div style="margin-top:8px"><small>Selected: <b id="methodTxt">bKash</b></small></div></div></div>
<div id="p5" class="page"><div class="top"><div class="ib">👤</div><div class="tt">Profile</div></div><div class="card" style="text-align:center"><div style="font-size:50px">👤</div><h2>User 4250</h2><div>💎 <span id="diam2">2110</span></div></div></div>

<div class="btm">
<div class="on" id="b1" onclick="showPage(1)"><span>🏠</span>Home</div>
<div id="b2" onclick="showPage(2)"><span>🎯</span>Tasks</div>
<div id="b3" onclick="showPage(3)"><span>👥</span>Refer</div>
<div id="b4" onclick="showPage(4)"><span>💸</span>Withdraw</div>
<div id="b5" onclick="showPage(5)"><span>👤</span>Profile</div>
</div>

<script>
var tg = window.Telegram.WebApp; tg.expand();
var uid = "4250"; try{ uid = String(tg.initDataUnsafe.user.id); }catch(e){}
var directLink = "DIRECT_LINK"; var sponLink = "SPON_LINK";
var curMethod = "bKash";
document.getElementById('refLink').innerText = "https://t.me/YourBot?start=" + uid;
function showPage(n){
  var pages = document.querySelectorAll('.page'); for(var i=0;i<pages.length;i++){ pages[i].classList.remove('active'); }
  document.getElementById('p'+n).classList.add('active');
  var btns = document.querySelectorAll('.btm div'); for(var i=0;i<btns.length;i++){ btns[i].classList.remove('on'); }
  document.getElementById('b'+n).classList.add('on');
}
function setMethod(m){ curMethod = m; document.getElementById('mBkash').classList.remove('on'); document.getElementById('mNagad').classList.remove('on'); if(m=='bKash'){ document.getElementById('mBkash').classList.add('on'); } else { document.getElementById('mNagad').classList.add('on'); } document.getElementById('methodTxt').innerText = m; }
function copyRef(){ navigator.clipboard.writeText(document.getElementById('refLink').innerText); alert('Copied'); }
function doAd(t){
  var link = (t=='c')? directLink : sponLink;
  try{ tg.openLink(link); }catch(e){ window.open(link, '_blank'); }
  setTimeout(function(){ fetch('/api/ads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,type:t})}).then(function(r){ return r.json(); }).then(function(j){ if(j.ok==false){ alert(j.msg); } else { alert('টাকা যোগ হয়েছে - Permanent'); init(); } }); }, 3000);
}
function doWd(){
  var num = document.getElementById('wdNum').value; var amt = document.getElementById('wdAmt').value;
  fetch('/api/wd',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid,num:num,amt:amt,method:curMethod})}).then(function(r){ return r.json(); }).then(function(j){ alert(j.msg); });
}
function init(){
  fetch('/api/init',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:uid})}).then(function(r){ return r.json(); }).then(function(d){ var u=d.user; document.getElementById('balTop').innerText='৳'+u.bal; document.getElementById('bal1').innerText='৳'+u.bal; document.getElementById('diam1').innerText=u.diamonds; document.getElementById('diam2').innerText=u.diamonds; document.getElementById('cCount').innerText=u.c; document.getElementById('pCount').innerText=u.p; document.getElementById('adCount').innerText=u.c+u.p; });
}
init();
</script></body></html>
    """
    html = html.replace("APP_NAME", s["app_name"]).replace("AD_C_TK", "৳" + str(s["ad_c"])).replace("AD_P_TK", "৳" + str(s["ad_p"])).replace("CLIM_L", str(s["clim"])).replace("PLIM_L", str(s["plim"])).replace("MIN_TK", str(s["min"])).replace("DIRECT_LINK", s["direct_link"]).replace("SPON_LINK", s["spon_link"])
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
