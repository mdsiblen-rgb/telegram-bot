# FINAL - JOKO WIRAWAN PROFILE - EXACT SCREENSHOT - NO SYNTAX ERROR - 8807178385
import os, json
from flask import Flask, jsonify, request, render_template_string
app = Flask(__name__)
DB_FILE = 'database.json'
ADMIN = "8807178385"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users":{"8807178385":{"id":"8807178385","name":"JOKO WIRAWAN","bal":24850000,"avail":18200000,"pending":6650000}}}
    with open(DB_FILE,'r',encoding='utf-8') as f: return json.load(f)
def save_db(d):
    with open(DB_FILE,'w',encoding='utf-8') as f: json.dump(f,d,indent=2)

@app.route('/')
def home():
    return render_template_string(PAGE)

@app.route('/admin')
def admin():
    if request.args.get('id')!=ADMIN: return "Need?id=8807178385"
    return "Admin OK - 8807178385"

@app.route('/api/balance')
def bal():
    return jsonify({"total":"IDR 24,850,000","avail":"IDR 18,200,000","pending":"IDR 6,650,000","week":"+IDR 1,250,000"})

PAGE = '''
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#050b19;color:#fff;max-width:430px;margin:0 auto;padding-bottom:90px}
.top{padding:14px;display:flex;align-items:center;gap:12px}
.search{flex:1;background:#111a2e;border:1px solid #1e2d4f;border-radius:24px;padding:12px 16px;display:flex;align-items:center;gap:10px}
.search input{flex:1;background:0;border:0;color:#8aa0bf;outline:0;font-size:14px}
.pro{background:linear-gradient(135deg,#0f2a4a,#143a5e);margin:0 14px;border-radius:18px;padding:16px;display:flex;justify-content:space-between;align-items:center;border:1px solid #1e4a6e;position:relative;overflow:hidden}
.pro::after{content:'';position:absolute;bottom:0;left:0;right:0;height:30px;background:rgba(0,0,0,0.3)}
.profile{margin:20px 14px;display:flex;gap:14px;align-items:center}
.ring{width:76px;height:76px;border-radius:50%;padding:3px;background:linear-gradient(135deg,#22c55e,#3b82f6)}
.ring img{width:100%;height:100%;border-radius:50%;object-fit:cover;background:#fff}
.balance{background:linear-gradient(135deg,#0c2342,#0f2e52);margin:14px;border-radius:18px;padding:16px;border:1px solid #1e3a5f;position:relative}
.mini{display:flex;gap:10px;margin:14px}
.mini div{flex:1;background:#0f1c34;border-radius:14px;padding:14px;border:1px solid #1e3a5f}
.live{margin:14px;background:#0a1429;border:2px solid #22c55e;border-radius:16px;padding:14px;box-shadow:0 0 20px rgba(34,197,94,0.25)}
.map{margin:14px;border-radius:16px;overflow:hidden;border:1px solid #1e3a5f;background:#0a1a36}
.map img{width:100%;height:200px;object-fit:cover}
.activity{margin:14px}
.act{background:#0f1c34;border-radius:12px;padding:12px;margin-top:8px;display:flex;justify-content:space-between;align-items:center;border:1px solid #1e2d4f}
.btm{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#0a1222;display:flex;padding:10px 0;border-top:1px solid #1e293b;z-index:99}
.btm div{flex:1;text-align:center;color:#5a6b8a;font-size:11px}
.btm div.on{color:#22c55e}
.btm span{font-size:22px;display:block}
</style></head><body>
<div class="top"><span style="font-size:24px;color:#4ade80">☰</span><div class="search"><input id="topText" value="Search or edit profile header..."><span style="color:#4ade80">✏️</span></div></div>

<div class="pro" onclick="alert('PRO BONUS LIVE')">
<div><div style="font-weight:900;font-size:16px">PRO MEMBER BONUS <span style="color:#4ade80">LIVE NOW</span></div><div style="font-size:11px;opacity:0.7;margin-top:4px">Unlock 20% extra withdrawal limit • Ends in 12:34:50</div></div>
<div style="font-size:36px">🎁</div>
</div>

<div class="profile">
<div class="ring"><img src="https://i.pravatar.cc/150?img=68"></div>
<div style="flex:1"><div style="font-weight:900;font-size:17px;display:flex;align-items:center;gap:6px">ADMIN • JOKO WIRAWAN <span>👑</span><span style="background:#22c55e;border-radius:50%;width:18px;height:18px;display:inline-flex;align-items:center;justify-content:center;font-size:10px">✓</span></div>
<div style="font-size:12px;color:#8aa0bf;margin-top:4px;display:flex;gap:6px">📍 joko.wirawan 📍 Jakarta Pusat, DKI Jakarta</div>
<div style="margin-top:8px"><span style="background:rgba(34,197,94,0.15);color:#4ade80;padding:5px 12px;border-radius:20px;font-size:11px;border:1px solid #22c55e">Super Admin</span></div></div>
</div>

<div class="balance"><div style="font-size:11px;opacity:0.6;letter-spacing:1px">TOTAL BALANCE</div><div style="font-size:26px;font-weight:900;color:#4ade80;margin-top:4px;display:flex;justify-content:space-between"><span>IDR 24,850,000</span><span style="color:#60a5fa">👁️</span></div><div style="font-size:12px;color:#4ade80;margin-top:4px">↗ +IDR 1,250,000 this week</div></div>

<div class="mini">
<div style="border-color:#22c55e"><div style="font-size:11px;opacity:0.6">AVAILABLE</div><div style="font-weight:900;font-size:18px;margin-top:4px">IDR 18,200,000</div><div style="font-size:11px;color:#4ade80;margin-top:2px">Ready to withdraw</div></div>
<div><div style="font-size:11px;opacity:0.6">PENDING</div><div style="font-weight:900;font-size:18px;margin-top:4px">IDR 6,650,000</div><div style="font-size:11px;color:#60a5fa;margin-top:2px">Processing • 1-2h</div></div>
</div>

<div class="live"><div style="display:flex;align-items:center;gap:8px"><div style="width:10px;height:10px;background:#22c55e;border-radius:50%;box-shadow:0 0 8px #22c55e"></div><div style="font-weight:900;color:#4ade80">LIVE WITHDRAW <span style="font-size:11px;opacity:0.6;color:#fff;font-weight:400">Instant withdrawal</span></div></div>
<div style="font-weight:800;margin-top:6px">— up to IDR 10,000,000</div>
<div style="margin-top:10px;display:flex;gap:10px;align-items:center"><button style="background:#86efac;color:#000;padding:7px 16px;border-radius:20px;border:0;font-weight:800;font-size:13px">Withdraw Now →</button><span style="font-size:11px;opacity:0.7">Fee: 0% • Available 24/7</span></div></div>

<div style="margin:16px 14px 8px 14px;font-size:13px;color:#60a5fa;font-weight:700">Location Overview</div>
<div class="map"><img src="https://i.ibb.co.com/1fJ0L2k/jakarta-map.png" onerror="this.src='https://maps.googleapis.com/maps/api/staticmap?center=Jakarta&zoom=11&size=600x300&maptype=roadmap&key=demo'"><div style="padding:10px;background:linear-gradient(transparent,rgba(0,0,0,0.8));position:relative;margin-top:-40px;color:#fff;font-size:10px;display:flex;justify-content:space-between"><span>LAUT JAWA</span><span>5 km</span></div></div>

<div class="activity"><div style="font-size:13px;color:#60a5fa;font-weight:700;margin-bottom:8px">Recent Activity</div>
<div class="act"><div style="display:flex;gap:10px;align-items:center"><div style="width:30px;height:30px;background:#22c55e;border-radius:8px;display:flex;align-items:center;justify-content:center">↓</div><div><div style="font-size:13px;font-weight:700">Withdraw to BCA • Successful</div></div></div><div style="font-size:11px;opacity:0.7">-IDR 500,000 • Today 14:22</div></div>
<div class="act"><div style="display:flex;gap:10px;align-items:center"><div style="width:30px;height:30px;background:#3b82f6;border-radius:8px;display:flex;align-items:center;justify-content:center">+</div><div><div style="font-size:13px;font-weight:700">Deposit via QRIS • Successful</div></div></div><div style="font-size:11px;opacity:0.7">+IDR 2,500,000 • Today 09:15</div></div>
</div>

<div class="btm"><div><span>🏠</span>Home</div><div><span>💼</span>Wallet</div><div class="on" style="background:linear-gradient(180deg,#16a34a,#0a3a1a);border-radius:16px;padding:4px"><span>🍃</span>Profile</div><div><span>📋</span>History</div><div><span>⚙️</span>More</div></div>

<script>
let uid=new URLSearchParams(location.search).get('id')||'8807178385';
function load(){fetch('/api/balance?id='+uid).then(r=>r.json()).then(d=>{});}load();
</script></body></html>
'''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
