import os, json, hmac, hashlib, sqlite3, time, secrets, base64, re
from urllib.parse import parse_qsl
from functools import wraps
from decimal import Decimal, ROUND_DOWN

import requests
from flask import Flask, request, jsonify, render_template_string, session

APP_NAME = "Protidiner Kaj BD"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8807178385"))
DB_PATH = os.getenv("DATABASE_PATH", "app.db")

DEFAULT_SETTINGS = {
    "app_name": APP_NAME,
    "welcome_title": "👑 প্রতিদিনের কাজ বিডি",
    "welcome_text": "স্বাগতম! কাজ করুন, Diamond সংগ্রহ করুন এবং Reward নিন।",
    "currency": "৳",
    "min_withdraw": "200",
    "welcome_cash": "0",
    "welcome_diamonds": "100",
    "referral_bonus": "20",
    "referral_commission_percent": "15",
    "daily_bonus": "5",
    "maintenance": "0",
    "support_username": "@ProtidinerKajBD",
    "support_whatsapp": "",
    "support_email": "support@example.com",
    "channel_link": "https://t.me/ProtidinerKajBD",
    "group_link": "https://t.me/+hb8X-V4buToxYmJl",
    "bot_link": "https://t.me/ProtidinerKaj_BD_Bot",
    "ad_link": "",
    "ad_script_1": "",
    "ad_script_2": "",
    "company_ad_reward": "0.50",
    "popup_ad_reward": "0.30",
    "company_ad_diamonds": "5",
    "popup_ad_diamonds": "3",
    "ad_duration": "15",
    "daily_ad_limit": "80",
    "ad_cooldown": "0",
    "diamonds_per_taka": "100",
    "level_1_diamonds": "0",
    "level_2_diamonds": "5000",
    "level_3_diamonds": "15000",
    "level_4_diamonds": "30000",
    "level_5_diamonds": "60000",
    "level_6_diamonds": "100000",
    "level_bonus_2": "0",
    "level_bonus_3": "0",
    "level_bonus_4": "0",
    "level_bonus_5": "0",
    "level_bonus_6": "0",
    "vip_enabled": "1",
    "vip_text": "VIP হলে বেশি ইনকাম পাবেন। Admin থেকে অফার লিখুন",
    "vip_link": "",
    "notice_text": "রাত ১১টার পর Withdraw বন্ধ থাকতে পারে। Fake Account করলে ব্যান হতে পারে।",
    "rules_text": "একাধিক একাউন্ট খুলবেন না|ভুল তথ্য দিবেন না|Fake Refer করবেন না|Admin এর সিদ্ধান্তই চূড়ান্ত",
    "theme_bg": "#080c1b",
    "theme_card": "#1b2447",
    "theme_card_dark": "#080b19",
    "theme_primary": "#8b55ff",
    "theme_green": "#19d37b",
    "theme_text": "#f5f7ff",
    "theme_muted": "#aab3ce",
}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))


def db():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con


def now(): return int(time.time())


def money(v):
    try: return float(Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_DOWN))
    except Exception: return 0.0


def init_db():
    con = db(); cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY, username TEXT DEFAULT '', first_name TEXT DEFAULT '',
      last_name TEXT DEFAULT '', photo_url TEXT DEFAULT '', profile_photo TEXT DEFAULT '',
      display_name TEXT DEFAULT '', balance REAL DEFAULT 0, referral_code TEXT UNIQUE,
      referred_by INTEGER DEFAULT NULL, total_earned REAL DEFAULT 0, total_withdrawn REAL DEFAULT 0,
      diamonds INTEGER DEFAULT 0, level INTEGER DEFAULT 1, blocked INTEGER DEFAULT 0,
      welcome_claimed INTEGER DEFAULT 0, privacy_locked INTEGER DEFAULT 0, pin_hash TEXT DEFAULT '',
      hide_name INTEGER DEFAULT 0, hide_username INTEGER DEFAULT 0, hide_photo INTEGER DEFAULT 0,
      hide_stats INTEGER DEFAULT 0, created_at INTEGER NOT NULL, last_daily INTEGER DEFAULT 0,
      ads_watched INTEGER DEFAULT 0, refer_count INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS tasks(
      id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT DEFAULT '',
      url TEXT NOT NULL, reward REAL DEFAULT 0, diamonds INTEGER DEFAULT 0,
      task_type TEXT DEFAULT 'link', active INTEGER DEFAULT 1, daily_limit INTEGER DEFAULT 1, created_at INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS task_claims(user_id INTEGER NOT NULL, task_id INTEGER NOT NULL, claimed_at INTEGER NOT NULL,
      PRIMARY KEY(user_id,task_id));
    CREATE TABLE IF NOT EXISTS withdrawals(
      id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,method TEXT NOT NULL,account TEXT NOT NULL,
      amount REAL NOT NULL,status TEXT DEFAULT 'pending',note TEXT DEFAULT '',created_at INTEGER NOT NULL,processed_at INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS support(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,message TEXT NOT NULL,
      reply TEXT DEFAULT '',status TEXT DEFAULT 'open',created_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,kind TEXT NOT NULL,
      cash REAL DEFAULT 0,diamonds INTEGER DEFAULT 0,reason TEXT DEFAULT '',ref_id TEXT DEFAULT '',created_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS ad_configs(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,ad_type TEXT NOT NULL,url TEXT DEFAULT '',script TEXT DEFAULT '',
      duration INTEGER DEFAULT 15,reward REAL DEFAULT 0,diamonds INTEGER DEFAULT 0,daily_limit INTEGER DEFAULT 80,cooldown INTEGER DEFAULT 0,active INTEGER DEFAULT 1,created_at INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS ad_sessions(token TEXT PRIMARY KEY,user_id INTEGER NOT NULL,ad_id INTEGER NOT NULL,started_at INTEGER NOT NULL,
      completed_at INTEGER DEFAULT 0,status TEXT DEFAULT 'started');
    CREATE TABLE IF NOT EXISTS ad_views(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,ad_id INTEGER NOT NULL,token TEXT,watched_at INTEGER NOT NULL,
      reward REAL DEFAULT 0,diamonds INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS levels(level INTEGER PRIMARY KEY,min_diamonds INTEGER NOT NULL,bonus REAL DEFAULT 0,title TEXT DEFAULT '');
    """)
    for k,v in DEFAULT_SETTINGS.items(): cur.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)",(k,str(v)))
    defaults=[(1,0,0,'Diamond Member'),(2,5000,0,'Bronze'),(3,15000,0,'Silver'),(4,30000,0,'Gold'),(5,60000,0,'Platinum'),(6,100000,0,'VIP')]
    for lv,md,b,t in defaults: cur.execute("INSERT OR IGNORE INTO levels(level,min_diamonds,bonus,title) VALUES(?,?,?,?)",(lv,md,b,t))
    # Seed ad configs once.
    if cur.execute("SELECT COUNT(*) c FROM ad_configs").fetchone()["c"] == 0:
        cur.execute("INSERT INTO ad_configs(name,ad_type,duration,reward,diamonds,daily_limit,cooldown,created_at) VALUES(?,?,?,?,?,?,?,?)",
                    ('Company Ads','company',15,0.50,5,80,0,now()))
        cur.execute("INSERT INTO ad_configs(name,ad_type,duration,reward,diamonds,daily_limit,cooldown,created_at) VALUES(?,?,?,?,?,?,?,?)",
                    ('Popup Ads','popup',15,0.30,3,80,0,now()))
    con.commit(); con.close()

init_db()


def get_settings():
    con=db(); rows=con.execute("SELECT key,value FROM settings").fetchall(); con.close()
    d=DEFAULT_SETTINGS.copy(); d.update({r['key']:r['value'] for r in rows}); return d


def set_setting(k,v):
    con=db(); con.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(k,str(v))); con.commit(); con.close()


def verify_init_data(init_data):
    if not init_data or not BOT_TOKEN: return None
    try:
        pairs=dict(parse_qsl(init_data,keep_blank_values=True)); received=pairs.pop('hash',None)
        if not received: return None
        check='\n'.join(f'{k}={pairs[k]}' for k in sorted(pairs))
        secret=hmac.new(b'WebAppData',BOT_TOKEN.encode(),hashlib.sha256).digest()
        calc=hmac.new(secret,check.encode(),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc,received): return None
        auth=int(pairs.get('auth_date','0'))
        if auth and now()-auth>86400: return None
        user=json.loads(pairs.get('user','{}'))
        return user if user.get('id') else None
    except Exception: return None


def level_for(diamonds):
    con=db(); rows=con.execute("SELECT level,min_diamonds FROM levels ORDER BY min_diamonds ASC").fetchall(); con.close()
    lv=1
    for r in rows:
        if diamonds >= r['min_diamonds']: lv=r['level']
    return lv


def ensure_user(tg):
    uid=int(tg['id']); con=db(); row=con.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone()
    if not row:
        code='U'+str(uid); name=(tg.get('first_name','')+' '+tg.get('last_name','')).strip()
        con.execute("INSERT INTO users(id,username,first_name,last_name,photo_url,display_name,referral_code,created_at) VALUES(?,?,?,?,?,?,?,?)",
                     (uid,tg.get('username',''),tg.get('first_name',''),tg.get('last_name',''),tg.get('photo_url',''),name,code,now()))
        row=con.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone()
        # First join bonus exactly once.
        s=get_settings(); cash=money(s.get('welcome_cash')); diamonds=int(float(s.get('welcome_diamonds','0') or 0))
        con.execute('UPDATE users SET balance=?,total_earned=?,diamonds=?,welcome_claimed=1 WHERE id=?',(cash,cash,diamonds,uid))
        if cash or diamonds: con.execute("INSERT INTO transactions(user_id,kind,cash,diamonds,reason,created_at) VALUES(?,?,?,?,?,?)",(uid,'welcome',cash,diamonds,'First join welcome bonus',now()))
    else:
        con.execute("UPDATE users SET username=?,first_name=?,last_name=?,photo_url=? WHERE id=?",
                     (tg.get('username',''),tg.get('first_name',''),tg.get('last_name',''),tg.get('photo_url',''),uid))
    # referral from startapp/ref query can be applied elsewhere; level always recalculated.
    r=con.execute('SELECT diamonds FROM users WHERE id=?',(uid,)).fetchone(); con.execute('UPDATE users SET level=? WHERE id=?',(level_for(r['diamonds']),uid))
    con.commit(); con.close()


def current_user():
    uid=session.get('user_id')
    if not uid:return None
    con=db(); r=con.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone(); con.close(); return r


def api_login_required(fn):
    @wraps(fn)
    def wrap(*a,**kw):
        tg=verify_init_data(request.headers.get('X-Telegram-Init-Data',''))
        if not tg:return jsonify(ok=False,error='Telegram authentication required'),401
        ensure_user(tg); session['user_id']=int(tg['id']); u=current_user()
        if not u:return jsonify(ok=False,error='User not found'),401
        if u['blocked']:return jsonify(ok=False,error='আপনার অ্যাকাউন্ট ব্লক করা হয়েছে।'),403
        return fn(*a,**kw)
    return wrap


def admin_required(fn):
    @wraps(fn)
    def wrap(*a,**kw):
        if session.get('admin_id')==ADMIN_ID:return fn(*a,**kw)
        tg=verify_init_data(request.headers.get('X-Telegram-Init-Data',''))
        if tg and int(tg['id'])==ADMIN_ID: session['admin_id']=ADMIN_ID; return fn(*a,**kw)
        return jsonify(ok=False,error='Admin access denied'),403
    return wrap


def add_reward(con,uid,cash=0,diamonds=0,reason='',ref=''):
    cash=money(cash); diamonds=int(diamonds or 0)
    if not cash and not diamonds:return
    con.execute('UPDATE users SET balance=balance+?,total_earned=total_earned+?,diamonds=diamonds+? WHERE id=?',(cash,cash,diamonds,uid))
    r=con.execute('SELECT diamonds FROM users WHERE id=?',(uid,)).fetchone(); con.execute('UPDATE users SET level=? WHERE id=?',(level_for(r['diamonds']),uid))
    con.execute('INSERT INTO transactions(user_id,kind,cash,diamonds,reason,ref_id,created_at) VALUES(?,?,?,?,?,?,?)',(uid,'credit',cash,diamonds,reason,ref,now()))

@app.get('/')
def index(): return render_template_string(MINI_APP_HTML,settings=get_settings())

@app.post('/api/login')
def login():
    b=request.get_json(silent=True) or {}; tg=verify_init_data(b.get('initData',''))
    if not tg:return jsonify(ok=False,error='Invalid Telegram data'),401
    ensure_user(tg); session['user_id']=int(tg['id'])
    return jsonify(ok=True)

@app.get('/api/me')
@api_login_required
def me():
    u=current_user(); s=get_settings(); con=db()
    wd=con.execute('SELECT id,method,account,amount,status,note,created_at FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 50',(u['id'],)).fetchall()
    sp=con.execute('SELECT id,message,reply,status,created_at FROM support WHERE user_id=? ORDER BY id DESC LIMIT 20',(u['id'],)).fetchall()
    tx=con.execute('SELECT id,kind,cash,diamonds,reason,created_at FROM transactions WHERE user_id=? ORDER BY id DESC LIMIT 50',(u['id'],)).fetchall()
    con.close()
    diamonds=int(u['diamonds']); lv=int(u['level']); con2=db(); nxt=con2.execute('SELECT level,min_diamonds FROM levels WHERE level>? ORDER BY level LIMIT 1',(lv,)).fetchone(); cur=con2.execute('SELECT level,min_diamonds FROM levels WHERE level=?',(lv,)).fetchone(); con2.close()
    target=int(nxt['min_diamonds']) if nxt else int(cur['min_diamonds']) if cur else diamonds
    base=int(cur['min_diamonds']) if cur else 0
    progress=100 if not nxt else max(0,min(100,round((diamonds-base)*100/max(1,target-base))))
    return jsonify(ok=True,user=dict(u),settings=s,withdrawals=[dict(x) for x in wd],support=[dict(x) for x in sp],transactions=[dict(x) for x in tx],level_next=target,level_base=base,progress=progress)

@app.post('/api/profile')
@api_login_required
def profile():
    u=current_user(); b=request.form
    name=str(b.get('display_name','')).strip()[:60]
    privacy_locked=1 if b.get('privacy_locked')=='1' else 0
    hide_name=1 if b.get('hide_name')=='1' else 0; hide_username=1 if b.get('hide_username')=='1' else 0; hide_photo=1 if b.get('hide_photo')=='1' else 0; hide_stats=1 if b.get('hide_stats')=='1' else 0
    pin=str(b.get('pin','')).strip()
    con=db()
    if privacy_locked:
        if pin and not re.fullmatch(r'\d{4,8}',pin): con.close(); return jsonify(ok=False,error='PIN 4-8 সংখ্যার হতে হবে।'),400
        if pin: ph=hashlib.sha256(pin.encode()).hexdigest()
        else: ph=u['pin_hash']
    else: ph=''
    photo=u['profile_photo']
    f=request.files.get('photo')
    if f and f.filename:
        data=f.read()
        if len(data)>600*1024: con.close(); return jsonify(ok=False,error='ছবির সাইজ 600KB-এর বেশি হতে পারবে না।'),400
        if not (f.mimetype or '').startswith('image/'): con.close(); return jsonify(ok=False,error='শুধু ছবি আপলোড করুন।'),400
        photo='data:'+f.mimetype+';base64,'+base64.b64encode(data).decode()
    con.execute('UPDATE users SET display_name=?,profile_photo=?,privacy_locked=?,pin_hash=?,hide_name=?,hide_username=?,hide_photo=?,hide_stats=? WHERE id=?',
                (name or u['display_name'] or u['first_name'],photo,privacy_locked,ph,hide_name,hide_username,hide_photo,hide_stats,u['id']))
    con.commit(); con.close(); return jsonify(ok=True)

@app.post('/api/profile/unlock')
@api_login_required
def unlock():
    pin=str((request.get_json(silent=True) or {}).get('pin','')).strip(); u=current_user()
    if not u['privacy_locked']: return jsonify(ok=True)
    if not pin or hashlib.sha256(pin.encode()).hexdigest()!=u['pin_hash']: return jsonify(ok=False,error='ভুল PIN'),403
    return jsonify(ok=True)

@app.get('/api/tasks')
@api_login_required
def tasks():
    uid=current_user()['id']; con=db(); rows=con.execute('SELECT t.*,CASE WHEN c.user_id IS NULL THEN 0 ELSE 1 END claimed FROM tasks t LEFT JOIN task_claims c ON c.task_id=t.id AND c.user_id=? WHERE t.active=1 ORDER BY t.id DESC',(uid,)).fetchall(); con.close(); return jsonify(ok=True,tasks=[dict(x) for x in rows])

@app.post('/api/task/<int:tid>/claim')
@api_login_required
def claim_task(tid):
    uid=current_user()['id']; con=db(); t=con.execute('SELECT * FROM tasks WHERE id=? AND active=1',(tid,)).fetchone()
    if not t: con.close(); return jsonify(ok=False,error='Task not found'),404
    if con.execute('SELECT 1 FROM task_claims WHERE user_id=? AND task_id=?',(uid,tid)).fetchone(): con.close(); return jsonify(ok=False,error='এই কাজটি আগে সম্পন্ন করেছেন।')
    con.execute('INSERT INTO task_claims VALUES(?,?,?)',(uid,tid,now())); add_reward(con,uid,t['reward'],t['diamonds'],'Task reward',str(tid)); con.commit(); con.close(); return jsonify(ok=True,reward=t['reward'],diamonds=t['diamonds'])

@app.post('/api/daily')
@api_login_required
def daily():
    uid=current_user()['id']; s=get_settings(); con=db(); u=con.execute('SELECT last_daily FROM users WHERE id=?',(uid,)).fetchone()
    if u['last_daily'] and now()-u['last_daily']<86400: con.close(); return jsonify(ok=False,error='আজকের Daily Bonus নেওয়া হয়েছে।')
    r=money(s['daily_bonus']); con.execute('UPDATE users SET last_daily=? WHERE id=?',(now(),uid)); add_reward(con,uid,r,0,'Daily bonus'); con.commit(); con.close(); return jsonify(ok=True,reward=r)

@app.get('/api/referral')
@api_login_required
def referral():
    u=current_user(); return jsonify(ok=True,code=u['referral_code'],link=f"{request.host_url.rstrip('/')}/?ref={u['referral_code']}")

@app.post('/api/support')
@api_login_required
def support():
    m=str((request.get_json(silent=True) or {}).get('message','')).strip()
    if not m:return jsonify(ok=False,error='মেসেজ লিখুন।'),400
    con=db(); con.execute('INSERT INTO support(user_id,message,created_at) VALUES(?,?,?)',(current_user()['id'],m[:2000],now())); con.commit(); con.close(); return jsonify(ok=True,message='আপনার মেসেজ পাঠানো হয়েছে।')

@app.post('/api/withdraw')
@api_login_required
def withdraw():
    uid=current_user()['id']; b=request.get_json(silent=True) or {}; method=str(b.get('method','')).strip(); account=str(b.get('account','')).strip(); amount=money(b.get('amount',0)); s=get_settings()
    if method not in ('bKash','Nagad','Bank'):return jsonify(ok=False,error='সঠিক পেমেন্ট মেথড নির্বাচন করুন।'),400
    if len(account)<5:return jsonify(ok=False,error='পেমেন্ট অ্যাকাউন্ট দিন।'),400
    if amount<money(s['min_withdraw']):return jsonify(ok=False,error=f"Minimum withdrawal {s['currency']}{s['min_withdraw']}"),400
    con=db(); u=con.execute('SELECT balance FROM users WHERE id=?',(uid,)).fetchone()
    if u['balance']<amount:con.close();return jsonify(ok=False,error='আপনার পর্যাপ্ত ব্যালেন্স নেই।'),400
    con.execute('UPDATE users SET balance=balance-? WHERE id=?',(amount,uid)); con.execute('INSERT INTO withdrawals(user_id,method,account,amount,created_at) VALUES(?,?,?,?,?)',(uid,method,account,amount,now())); con.execute("INSERT INTO transactions(user_id,kind,cash,reason,created_at) VALUES(?,?,?,?,?)",(uid,'withdraw_hold',-amount,'Withdrawal request',now())); con.commit(); con.close(); return jsonify(ok=True,message='Withdrawal request submitted.')

# Ad system: server session + duration/cooldown/daily limit. Actual ad-network callback can be added later.
@app.get('/api/ads')
@api_login_required
def ads():
    uid=current_user()['id']; con=db(); rows=con.execute('SELECT * FROM ad_configs WHERE active=1 ORDER BY id').fetchall(); out=[]
    for r in rows:
        day=int(now()//86400); count=con.execute('SELECT COUNT(*) c FROM ad_views WHERE user_id=? AND ad_id=? AND watched_at>=?',(uid,r['id'],day*86400)).fetchone()['c']
        out.append({**dict(r),'watched_today':count,'remaining':max(0,r['daily_limit']-count)})
    con.close(); return jsonify(ok=True,ads=out)

@app.post('/api/ad/<int:ad_id>/start')
@api_login_required
def ad_start(ad_id):
    uid=current_user()['id']; con=db(); a=con.execute('SELECT * FROM ad_configs WHERE id=? AND active=1',(ad_id,)).fetchone()
    if not a:con.close();return jsonify(ok=False,error='Ad not found'),404
    day=int(now()//86400); count=con.execute('SELECT COUNT(*) c FROM ad_views WHERE user_id=? AND ad_id=? AND watched_at>=?',(uid,ad_id,day*86400)).fetchone()['c']
    if count>=a['daily_limit']:con.close();return jsonify(ok=False,error='আজকের Ad limit শেষ।'),400
    last=con.execute('SELECT watched_at FROM ad_views WHERE user_id=? AND ad_id=? ORDER BY id DESC LIMIT 1',(uid,ad_id)).fetchone()
    if last and now()-last['watched_at']<a['cooldown']:con.close();return jsonify(ok=False,error='কিছুক্ষণ পর আবার চেষ্টা করুন।'),400
    token=secrets.token_urlsafe(24); con.execute('INSERT INTO ad_sessions(token,user_id,ad_id,started_at) VALUES(?,?,?,?)',(token,uid,ad_id,now())); con.commit(); con.close()
    return jsonify(ok=True,token=token,duration=a['duration'],url=a['url'],script=a['script'],reward=a['reward'],diamonds=a['diamonds'])

@app.post('/api/ad/complete')
@api_login_required
def ad_complete():
    token=str((request.get_json(silent=True) or {}).get('token','')); uid=current_user()['id']; con=db(); s=con.execute('SELECT * FROM ad_sessions WHERE token=? AND user_id=? AND status="started"',(token,uid)).fetchone()
    if not s:con.close();return jsonify(ok=False,error='Invalid ad session'),400
    a=con.execute('SELECT * FROM ad_configs WHERE id=?',(s['ad_id'],)).fetchone(); elapsed=now()-s['started_at']
    if elapsed<max(1,int(a['duration'])):con.close();return jsonify(ok=False,error=f"আরও {int(a['duration'])-elapsed} সেকেন্ড অপেক্ষা করুন।"),400
    con.execute('UPDATE ad_sessions SET status="completed",completed_at=? WHERE token=?',(now(),token)); con.execute('INSERT INTO ad_views(user_id,ad_id,token,watched_at,reward,diamonds) VALUES(?,?,?,?,?,?)',(uid,a['id'],token,now(),a['reward'],a['diamonds'])); con.execute('UPDATE users SET ads_watched=ads_watched+1 WHERE id=?',(uid,)); add_reward(con,uid,a['reward'],a['diamonds'],'Ad reward',str(a['id'])); con.commit(); con.close(); return jsonify(ok=True,reward=a['reward'],diamonds=a['diamonds'])

# ---------- Admin ----------
@app.get('/admin')
def admin_page():return render_template_string(ADMIN_HTML,settings=get_settings())
@app.post('/admin/session')
def admin_session():
    tg=verify_init_data(request.headers.get('X-Telegram-Init-Data',''))
    if not tg or int(tg['id'])!=ADMIN_ID:return jsonify(ok=False,error='শুধু Admin Telegram account থেকে প্রবেশ করুন।'),403
    session['admin_id']=ADMIN_ID;return jsonify(ok=True)

@app.get('/api/admin/stats')
@admin_required
def admin_stats():
    con=db(); r={
      'users':con.execute('SELECT COUNT(*) c FROM users').fetchone()['c'],'active':con.execute('SELECT COUNT(*) c FROM users WHERE blocked=0').fetchone()['c'],
      'pending':con.execute("SELECT COUNT(*) c FROM withdrawals WHERE status='pending'").fetchone()['c'],'balance':con.execute('SELECT COALESCE(SUM(balance),0) x FROM users').fetchone()['x'],
      'earned':con.execute('SELECT COALESCE(SUM(total_earned),0) x FROM users').fetchone()['x'],'diamonds':con.execute('SELECT COALESCE(SUM(diamonds),0) x FROM users').fetchone()['x'],
      'ads':con.execute('SELECT COALESCE(SUM(ads_watched),0) x FROM users').fetchone()['x']};con.close();return jsonify(ok=True,**r)

@app.get('/api/admin/users')
@admin_required
def admin_users():
    q=request.args.get('q','').strip(); con=db(); sql='SELECT id,username,first_name,display_name,balance,total_earned,total_withdrawn,diamonds,level,blocked,created_at,ads_watched,refer_count FROM users'; args=[]
    if q:sql+=' WHERE CAST(id AS TEXT) LIKE ? OR username LIKE ? OR first_name LIKE ? OR display_name LIKE ?';args=[f'%{q}%']*4
    sql+=' ORDER BY id DESC LIMIT 200';rows=con.execute(sql,args).fetchall();con.close();return jsonify(ok=True,users=[dict(x) for x in rows])

@app.post('/api/admin/user/<int:uid>/adjust')
@admin_required
def admin_adjust(uid):
    b=request.get_json(silent=True) or {}; cash=money(b.get('cash',0)); dia=int(float(b.get('diamonds',0) or 0)); con=db(); add_reward(con,uid,cash,dia,'Admin adjustment');con.commit();con.close();return jsonify(ok=True)

@app.post('/api/admin/user/<int:uid>/block')
@admin_required
def admin_block(uid):
    b=request.get_json(silent=True) or {};con=db();con.execute('UPDATE users SET blocked=? WHERE id=?',(1 if b.get('blocked') else 0,uid));con.commit();con.close();return jsonify(ok=True)

@app.post('/api/admin/user/<int:uid>/reset-pin')
@admin_required
def reset_pin(uid):
    con=db();con.execute('UPDATE users SET pin_hash="",privacy_locked=0 WHERE id=?',(uid,));con.commit();con.close();return jsonify(ok=True)

@app.get('/api/admin/transactions')
@admin_required
def admin_transactions():
    con=db();rows=con.execute('SELECT t.*,u.username,u.first_name FROM transactions t LEFT JOIN users u ON u.id=t.user_id ORDER BY t.id DESC LIMIT 300').fetchall();con.close();return jsonify(ok=True,transactions=[dict(x) for x in rows])

@app.get('/api/admin/tasks')
@admin_required
def admin_tasks():
    con=db();rows=con.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall();con.close();return jsonify(ok=True,tasks=[dict(x) for x in rows])

@app.post('/api/admin/tasks')
@admin_required
def admin_create_task():
    b=request.get_json(silent=True) or {};title=str(b.get('title','')).strip();url=str(b.get('url','')).strip();reward=money(b.get('reward',0));dia=int(float(b.get('diamonds',0) or 0))
    if not title or not url:return jsonify(ok=False,error='Title ও URL দিন।'),400
    con=db();con.execute('INSERT INTO tasks(title,description,url,reward,diamonds,task_type,active,daily_limit,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(title,str(b.get('description','')),url,reward,dia,str(b.get('task_type','link')),1,int(b.get('daily_limit',1)),now()));con.commit();con.close();return jsonify(ok=True)

@app.post('/api/admin/task/<int:tid>')
@admin_required
def admin_update_task(tid):
    b=request.get_json(silent=True) or {};allowed=['title','description','url','reward','diamonds','task_type','active','daily_limit'];vals={k:b[k] for k in allowed if k in b};
    if 'reward' in vals:vals['reward']=money(vals['reward'])
    if 'diamonds' in vals:vals['diamonds']=int(float(vals['diamonds']))
    con=db();
    if vals:con.execute('UPDATE tasks SET '+','.join(k+'=?' for k in vals)+' WHERE id=?',(*vals.values(),tid))
    con.commit();con.close();return jsonify(ok=True)

@app.delete('/api/admin/task/<int:tid>')
@admin_required
def admin_delete_task(tid):
    con=db();con.execute('DELETE FROM tasks WHERE id=?',(tid,));con.execute('DELETE FROM task_claims WHERE task_id=?',(tid,));con.commit();con.close();return jsonify(ok=True)

@app.get('/api/admin/ads')
@admin_required
def admin_ads():
    con=db();rows=con.execute('SELECT * FROM ad_configs ORDER BY id').fetchall();con.close();return jsonify(ok=True,ads=[dict(x) for x in rows])

@app.post('/api/admin/ads')
@admin_required
def admin_ad_create():
    b=request.get_json(silent=True) or {};con=db();con.execute('INSERT INTO ad_configs(name,ad_type,url,script,duration,reward,diamonds,daily_limit,cooldown,active,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
      (str(b.get('name','Ad')),str(b.get('ad_type','company')),str(b.get('url','')),str(b.get('script','')),int(b.get('duration',15)),money(b.get('reward',0)),int(float(b.get('diamonds',0) or 0)),int(b.get('daily_limit',80)),int(b.get('cooldown',0)),1,now()));con.commit();con.close();return jsonify(ok=True)

@app.post('/api/admin/ad/<int:aid>')
@admin_required
def admin_ad_update(aid):
    b=request.get_json(silent=True) or {};allowed=['name','ad_type','url','script','duration','reward','diamonds','daily_limit','cooldown','active'];vals={k:b[k] for k in allowed if k in b};
    if 'reward' in vals:vals['reward']=money(vals['reward'])
    con=db();
    if vals:con.execute('UPDATE ad_configs SET '+','.join(k+'=?' for k in vals)+' WHERE id=?',(*vals.values(),aid))
    con.commit();con.close();return jsonify(ok=True)

@app.delete('/api/admin/ad/<int:aid>')
@admin_required
def admin_ad_delete(aid):
    con=db();con.execute('DELETE FROM ad_configs WHERE id=?',(aid,));con.commit();con.close();return jsonify(ok=True)

@app.get('/api/admin/withdrawals')
@admin_required
def admin_withdrawals():
    con=db();rows=con.execute('SELECT w.*,u.username,u.first_name FROM withdrawals w LEFT JOIN users u ON u.id=w.user_id ORDER BY w.id DESC LIMIT 300').fetchall();con.close();return jsonify(ok=True,withdrawals=[dict(x) for x in rows])

@app.post('/api/admin/withdrawal/<int:wid>')
@admin_required
def admin_withdrawal(wid):
    b=request.get_json(silent=True) or {};status=b.get('status');note=str(b.get('note',''));con=db();w=con.execute('SELECT * FROM withdrawals WHERE id=?',(wid,)).fetchone()
    if not w:con.close();return jsonify(ok=False,error='Withdrawal not found'),404
    old=w['status']
    if status not in ('pending','approved','rejected'):con.close();return jsonify(ok=False,error='Invalid status'),400
    if old!='rejected' and status=='rejected': con.execute('UPDATE users SET balance=balance+? WHERE id=?',(w['amount'],w['user_id']));con.execute('INSERT INTO transactions(user_id,kind,cash,reason,ref_id,created_at) VALUES(?,?,?,?,?,?)',(w['user_id'],'refund',w['amount'],'Rejected withdrawal',str(wid),now()))
    if old=='rejected' and status!='rejected': con.execute('UPDATE users SET balance=balance-? WHERE id=?',(w['amount'],w['user_id']))
    if old!='approved' and status=='approved':con.execute('UPDATE users SET total_withdrawn=total_withdrawn+? WHERE id=?',(w['amount'],w['user_id']))
    if old=='approved' and status!='approved':con.execute('UPDATE users SET total_withdrawn=total_withdrawn-? WHERE id=?',(w['amount'],w['user_id']))
    con.execute('UPDATE withdrawals SET status=?,note=?,processed_at=? WHERE id=?',(status,note,now(),wid));con.commit();con.close();return jsonify(ok=True)

@app.get('/api/admin/support')
@admin_required
def admin_support():
    con=db();rows=con.execute('SELECT s.*,u.username,u.first_name FROM support s LEFT JOIN users u ON u.id=s.user_id ORDER BY s.id DESC LIMIT 300').fetchall();con.close();return jsonify(ok=True,support=[dict(x) for x in rows])

@app.post('/api/admin/support/<int:sid>')
@admin_required
def admin_support_reply(sid):
    b=request.get_json(silent=True) or {};con=db();con.execute('UPDATE support SET reply=?,status=? WHERE id=?',(str(b.get('reply',''))[:3000],str(b.get('status','answered')),sid));con.commit();con.close();return jsonify(ok=True)

@app.get('/api/admin/settings')
@admin_required
def admin_settings():return jsonify(ok=True,settings=get_settings())
@app.post('/api/admin/settings')
@admin_required
def admin_save_settings():
    b=request.get_json(silent=True) or {}
    for k in DEFAULT_SETTINGS:
        if k in b:set_setting(k,b[k])
    return jsonify(ok=True,settings=get_settings())

@app.get('/api/admin/levels')
@admin_required
def admin_levels():
    con=db();rows=con.execute('SELECT * FROM levels ORDER BY level').fetchall();con.close();return jsonify(ok=True,levels=[dict(x) for x in rows])
@app.post('/api/admin/levels')
@admin_required
def admin_levels_save():
    arr=(request.get_json(silent=True) or {}).get('levels',[]);con=db()
    for x in arr:
        con.execute('INSERT INTO levels(level,min_diamonds,bonus,title) VALUES(?,?,?,?) ON CONFLICT(level) DO UPDATE SET min_diamonds=excluded.min_diamonds,bonus=excluded.bonus,title=excluded.title',(int(x['level']),int(x['min_diamonds']),money(x.get('bonus',0)),str(x.get('title',''))))
    con.commit();
    rows=con.execute('SELECT id,diamonds FROM users').fetchall()
    for r in rows:con.execute('UPDATE users SET level=? WHERE id=?',(level_for(r['diamonds']),r['id']))
    con.commit();con.close();return jsonify(ok=True)

ADMIN_HTML=r'''<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin Panel</title><style>
*{box-sizing:border-box}body{margin:0;background:#080c1b;color:#f5f7ff;font-family:Arial,sans-serif}.wrap{max-width:1200px;margin:auto;padding:18px 14px 60px}.top{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:15px}.brand{font-size:25px;font-weight:800}.sub{color:#aab3ce}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.box,.panel{background:#1b2447;border:1px solid #2f3c70;border-radius:20px;padding:16px;margin-bottom:14px;box-shadow:0 8px 25px #0005}.num{font-size:25px;font-weight:800;color:#19d37b;margin-top:7px}.tabs{display:flex;gap:8px;overflow:auto;margin-bottom:14px}.tabs button{border:1px solid #3a477a;background:#11162b;color:#ccd3e8;padding:10px 13px;border-radius:12px;white-space:nowrap}.tabs button.active{background:#8b55ff;color:white}.tab{display:none}.tab.active{display:block}.input,.select,.textarea{width:100%;background:#080b19;color:#fff;border:1px solid #364577;border-radius:11px;padding:11px;margin:6px 0 10px}.textarea{min-height:90px}.btn{border:0;border-radius:12px;padding:10px 14px;background:#8b55ff;color:#fff;font-weight:800}.danger{background:#d34a67}.ok{background:#159b61}.muted{background:#303a61}.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}.wide{grid-column:1/-1}.table{width:100%;border-collapse:collapse;font-size:13px}.table th,.table td{padding:9px;border-bottom:1px solid #303a61;text-align:left;vertical-align:top}.scroll{overflow:auto}.pill{padding:4px 8px;border-radius:9px;background:#303a61}.formgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}@media(max-width:700px){.grid{grid-template-columns:1fr 1fr}.row,.formgrid{grid-template-columns:1fr}.wide{grid-column:auto}}
</style></head><body><div class="wrap"><div class="top"><div><div class="brand">⚙️ Admin Control Center</div><div class="sub">Protidiner Kaj BD — সবকিছু এক জায়গা থেকে</div></div><button class="btn" onclick="verify()">🔐 Verify Admin</button></div>
<div class="grid"><div class="box">👥 Users<div id="users" class="num">0</div></div><div class="box">🟢 Active<div id="active" class="num">0</div></div><div class="box">💰 Balance<div id="balance" class="num">0</div></div><div class="box">💎 Diamonds<div id="diamonds" class="num">0</div></div></div>
<div class="tabs"><button class="active" onclick="tab('dash',this)">📊 Dashboard</button><button onclick="tab('usersTab',this)">👥 Users</button><button onclick="tab('ads',this)">📺 Ads</button><button onclick="tab('tasks',this)">🎯 Tasks</button><button onclick="tab('wd',this)">💳 Withdraw</button><button onclick="tab('support',this)">💬 Support</button><button onclick="tab('levels',this)">💎 Levels</button><button onclick="tab('settings',this)">⚙️ Settings</button><button onclick="tab('tx',this)">📜 Ledger</button></div>
<div id="dash" class="tab active panel"><h2>📊 Dashboard</h2><p class="sub">Welcome bonus, Diamond, Level, Ads, Tasks, Referral, Withdrawal, Profile privacy এবং Theme—সব Admin controlled.</p><button class="btn muted" onclick="refresh()">🔄 Refresh</button></div>
<div id="usersTab" class="tab panel"><h2>👥 User Management</h2><input id="uq" class="input" placeholder="ID / username / name search" oninput="loadUsers()"><div id="ul" class="scroll"></div></div>
<div id="ads" class="tab panel"><h2>📺 Ad Management</h2><div class="row"><input id="an" class="input" placeholder="Ad name"><input id="at" class="input" placeholder="Type: company/popup"></div><div class="row"><input id="au" class="input" placeholder="Direct/Pop URL"><input id="adur" class="input" type="number" placeholder="Duration seconds"></div><div class="row"><input id="ar" class="input" type="number" step="0.01" placeholder="Cash reward"><input id="adi" class="input" type="number" placeholder="Diamond reward"></div><div class="row"><input id="adl" class="input" type="number" placeholder="Daily limit"><input id="ac" class="input" type="number" placeholder="Cooldown seconds"></div><textarea id="asc" class="textarea" placeholder="Ad script / zone"></textarea><button class="btn ok" onclick="addAd()">➕ Add Ad</button><div id="adlist" class="scroll" style="margin-top:15px"></div></div>
<div id="tasks" class="tab panel"><h2>🎯 Task Management</h2><div class="row"><input id="tt" class="input" placeholder="Task title"><input id="tr" class="input" type="number" step="0.01" placeholder="Cash reward"></div><div class="row"><input id="tdi" class="input" type="number" placeholder="Diamond reward"><input id="tu" class="input" placeholder="Task URL"></div><textarea id="td" class="textarea" placeholder="Description"></textarea><button class="btn ok" onclick="addTask()">➕ Add Task</button><div id="tl" class="scroll" style="margin-top:15px"></div></div>
<div id="wd" class="tab panel"><h2>💳 Withdrawal Management</h2><div id="wl" class="scroll"></div></div>
<div id="support" class="tab panel"><h2>💬 Support Inbox</h2><div id="sl"></div></div>
<div id="levels" class="tab panel"><h2>💎 Diamond Levels</h2><p class="sub">কত Diamond হলে কোন Level হবে—এখান থেকেই নির্ধারণ করুন।</p><div id="lv"></div><button class="btn ok" onclick="saveLevels()">💾 Save Levels</button></div>
<div id="settings" class="tab panel"><h2>⚙️ All Settings</h2><div id="sf"></div><button class="btn ok" onclick="saveSettings()">💾 Save All Settings</button></div>
<div id="tx" class="tab panel"><h2>📜 Transaction Ledger</h2><div id="txl" class="scroll"></div></div></div>
<script>const tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand()} const initData=tg?tg.initData:'';async function api(u,o={}){o.headers=Object.assign({},o.headers||{}, {'X-Telegram-Init-Data':initData,'Content-Type':'application/json'});let r=await fetch(u,o),j=await r.json();if(!r.ok||j.ok===false)throw Error(j.error||'Error');return j}function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}async function verify(){try{await api('/admin/session',{method:'POST'});alert('Admin verified');refresh()}catch(e){alert(e.message)}}function tab(id,b){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('active'));b.classList.add('active');({usersTab:loadUsers,ads:loadAds,tasks:loadTasks,wd:loadWd,support:loadSupport,levels:loadLevels,settings:loadSettings,tx:loadTx})[id]?.()}async function refresh(){try{let j=await api('/api/admin/stats');users.textContent=j.users;active.textContent=j.active;balance.textContent=Number(j.balance).toFixed(2);diamonds.textContent=j.diamonds}catch(e){console.log(e.message)}}async function loadUsers(){try{let j=await api('/api/admin/users?q='+encodeURIComponent(uq.value));ul.innerHTML='<table class="table"><tr><th>User</th><th>Money</th><th>Diamond</th><th>Action</th></tr>'+j.users.map(x=>`<tr><td>${x.id}<br>${esc(x.display_name||x.first_name)}<br>@${esc(x.username||'')}</td><td>৳${x.balance}<br>Earned ৳${x.total_earned}</td><td>💎 ${x.diamonds}<br>Level ${x.level}</td><td><button class="btn" onclick="adj(${x.id})">Adjust</button> <button class="btn ${x.blocked?'ok':'danger'}" onclick="block(${x.id},${x.blocked?0:1})">${x.blocked?'Unblock':'Block'}</button> <button class="btn muted" onclick="pin(${x.id})">Reset PIN</button></td></tr>`).join('')+'</table>'}catch(e){alert(e.message)}}async function adj(id){let c=prompt('Cash +/- (e.g. 10 or -5)','0');if(c===null)return;let d=prompt('Diamond +/-','0');if(d===null)return;await api('/api/admin/user/'+id+'/adjust',{method:'POST',body:JSON.stringify({cash:c,diamonds:d})});loadUsers();refresh()}async function block(id,b){await api('/api/admin/user/'+id+'/block',{method:'POST',body:JSON.stringify({blocked:b})});loadUsers()}async function pin(id){await api('/api/admin/user/'+id+'/reset-pin',{method:'POST'});alert('PIN reset')}async function addAd(){await api('/api/admin/ads',{method:'POST',body:JSON.stringify({name:an.value,ad_type:at.value,url:au.value,duration:adur.value,reward:ar.value,diamonds:adi.value,daily_limit:adl.value,cooldown:ac.value,script:asc.value})});an.value=at.value=au.value=adur.value=ar.value=adi.value=adl.value=ac.value=asc.value='';loadAds()}async function loadAds(){let j=await api('/api/admin/ads');adlist.innerHTML='<table class="table"><tr><th>Ad</th><th>Reward</th><th>Limit</th><th>Action</th></tr>'+j.ads.map(x=>`<tr><td>${esc(x.name)}<br>${x.duration}s / ${x.ad_type}</td><td>৳${x.reward}<br>💎${x.diamonds}</td><td>${x.daily_limit}<br>CD ${x.cooldown}s</td><td><button class="btn ${x.active?'danger':'ok'}" onclick="toggleAd(${x.id},${x.active?0:1})">${x.active?'Disable':'Enable'}</button> <button class="btn danger" onclick="delAd(${x.id})">Delete</button></td></tr>`).join('')+'</table>'}async function toggleAd(id,a){await api('/api/admin/ad/'+id,{method:'POST',body:JSON.stringify({active:a})});loadAds()}async function delAd(id){if(confirm('Delete?')){await api('/api/admin/ad/'+id,{method:'DELETE'});loadAds()}}async function addTask(){await api('/api/admin/tasks',{method:'POST',body:JSON.stringify({title:tt.value,reward:tr.value,diamonds:tdi.value,url:tu.value,description:td.value})});tt.value=tr.value=tdi.value=tu.value=td.value='';loadTasks()}async function loadTasks(){let j=await api('/api/admin/tasks');tl.innerHTML='<table class="table"><tr><th>Task</th><th>Reward</th><th>Action</th></tr>'+j.tasks.map(x=>`<tr><td>${esc(x.title)}<br>${esc(x.url)}</td><td>৳${x.reward}<br>💎${x.diamonds}</td><td><button class="btn danger" onclick="delTask(${x.id})">Delete</button></td></tr>`).join('')+'</table>'}async function delTask(id){if(confirm('Delete?')){await api('/api/admin/task/'+id,{method:'DELETE'});loadTasks()}}async function loadWd(){let j=await api('/api/admin/withdrawals');wl.innerHTML='<table class="table"><tr><th>#</th><th>User</th><th>Method</th><th>Account</th><th>Amount</th><th>Status</th><th>Action</th></tr>'+j.withdrawals.map(x=>`<tr><td>${x.id}</td><td>${x.user_id}<br>@${esc(x.username||'')}</td><td>${x.method}</td><td>${esc(x.account)}</td><td>৳${x.amount}</td><td>${x.status}</td><td><button class="btn ok" onclick="wd(${x.id},'approved')">Approve</button> <button class="btn danger" onclick="wd(${x.id},'rejected')">Reject</button></td></tr>`).join('')+'</table>'}async function wd(id,s){let n=prompt('Note','');await api('/api/admin/withdrawal/'+id,{method:'POST',body:JSON.stringify({status:s,note:n||''})});loadWd();refresh()}async function loadSupport(){let j=await api('/api/admin/support');sl.innerHTML=j.support.map(x=>`<div class="box"><b>#${x.id} User ${x.user_id}</b><p>${esc(x.message)}</p><p>Reply: ${esc(x.reply||'—')}</p><textarea id="rp${x.id}" class="textarea" placeholder="Reply"></textarea><button class="btn ok" onclick="reply(${x.id})">Send Reply</button></div>`).join('')}async function reply(id){await api('/api/admin/support/'+id,{method:'POST',body:JSON.stringify({reply:document.getElementById('rp'+id).value,status:'answered'})});loadSupport()}async function loadLevels(){let j=await api('/api/admin/levels');lv.innerHTML=j.levels.map(x=>`<div class="row"><input class="input lvn" data-l="${x.level}" value="${esc(x.title)}" placeholder="Level title"><input class="input lvd" data-l="${x.level}" value="${x.min_diamonds}" type="number" placeholder="Minimum diamonds"></div>`).join('')}async function saveLevels(){let arr=[...document.querySelectorAll('.lvn')].map(x=>({level:x.dataset.l,min_diamonds:document.querySelector('.lvd[data-l="'+x.dataset.l+'"]').value,title:x.value}));await api('/api/admin/levels',{method:'POST',body:JSON.stringify({levels:arr})});alert('Levels saved')}async function loadSettings(){let j=await api('/api/admin/settings');sf.innerHTML=Object.entries(j.settings).map(([k,v])=>`<label>${esc(k)}<input class="input sk" data-key="${esc(k)}" value="${esc(v)}"></label>`).join('')}async function saveSettings(){let b={};document.querySelectorAll('.sk').forEach(x=>b[x.dataset.key]=x.value);await api('/api/admin/settings',{method:'POST',body:JSON.stringify(b)});alert('Saved')}async function loadTx(){let j=await api('/api/admin/transactions');txl.innerHTML='<table class="table"><tr><th>Time</th><th>User</th><th>Kind</th><th>Cash</th><th>Diamond</th><th>Reason</th></tr>'+j.transactions.map(x=>`<tr><td>${new Date(x.created_at*1000).toLocaleString()}</td><td>${x.user_id}</td><td>${esc(x.kind)}</td><td>${x.cash}</td><td>${x.diamonds}</td><td>${esc(x.reason)}</td></tr>`).join('')+'</table>'}refresh();</script></body></html>'''

MINI_APP_HTML=r'''<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><title>{{settings.app_name}}</title><script src="https://telegram.org/js/telegram-web-app.js"></script><style>
:root{--bg:{{settings.theme_bg}};--card:{{settings.theme_card}};--dark:{{settings.theme_card_dark}};--pri:{{settings.theme_primary}};--green:{{settings.theme_green}};--txt:{{settings.theme_text}};--muted:{{settings.theme_muted}}}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font-family:Arial,sans-serif}.app{max-width:620px;margin:auto;padding:14px 14px 95px}.top{display:grid;grid-template-columns:68px 1fr 145px;gap:8px;align-items:center}.top .icon,.top .title,.top .brand{border:1px solid var(--pri);border-radius:20px;height:62px;display:flex;align-items:center;justify-content:center;background:#10162e}.top .icon{font-size:34px;box-shadow:0 0 22px #8b55ff66}.top .title{font-size:20px;font-weight:800}.top .brand{border-color:#ffad28;font-size:16px;text-align:center;line-height:1.25}.brand b{color:var(--green);display:block}.card{background:var(--card);border:1px solid #2f3b70;border-radius:24px;padding:18px;margin-top:14px;box-shadow:0 10px 30px #0005}.profile{text-align:center}.avatar{width:120px;height:120px;border:3px solid var(--pri);border-radius:28px;margin:auto;overflow:hidden;background:#080b19;display:flex;align-items:center;justify-content:center;font-size:65px}.avatar img{width:100%;height:100%;object-fit:cover}.level{display:inline-block;background:#ffb019;color:#17120a;border-radius:20px;padding:5px 16px;font-weight:800;margin-top:10px}.name{font-size:29px;font-weight:800;margin-top:8px}.join{color:var(--muted);margin:3px 0 10px}.diam{font-size:19px}.progressBox{border:2px solid var(--pri);border-radius:20px;padding:14px;margin-top:14px;background:#171238}.progressTop{display:flex;justify-content:space-between;font-weight:800}.bar{height:18px;border-radius:20px;background:#303c70;overflow:hidden;margin:10px 0}.fill{height:100%;background:linear-gradient(90deg,#9d43ff,#cf4dff);border-radius:20px}.pct{text-align:center;font-size:22px;font-weight:800}.small{color:var(--muted);font-size:13px;text-align:center}.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px}.stat{background:#080b19;border-radius:20px;padding:16px;text-align:center}.stat b{display:block;font-size:27px;margin-bottom:6px}.green{color:var(--green)}.purple{color:#9c66ff}.orange{color:#ffad28}.pink{color:#e44e9e}.section{display:none}.section.active{display:block}.h2{font-size:23px;font-weight:800;margin-bottom:12px}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}.offer{border:2px solid #ff8c1a;background:#281d15}.btn{width:100%;border:0;border-radius:15px;background:var(--pri);color:#fff;padding:13px;font-weight:800;font-size:16px;margin-top:10px}.btn.greenbtn{background:#16985e}.btn.dark{background:#303a61}.input,.select,.textarea{width:100%;background:#080b19;color:#fff;border:1px solid #344272;border-radius:14px;padding:13px;margin-top:8px}.textarea{min-height:100px}.task{background:#080b19;border:1px solid #313d70;border-radius:18px;padding:15px;margin-top:10px}.reward{color:var(--green);font-weight:800}.nav{position:fixed;z-index:50;bottom:0;left:0;right:0;background:#11172b;border-top:1px solid #313b63;display:flex;justify-content:center}.nav button{flex:1;max-width:125px;border:0;background:transparent;color:#8892ad;padding:9px 4px 8px;font-size:12px}.nav button b{display:block;font-size:25px}.nav button.active{color:var(--pri)}.notice{background:#0f3543;border-radius:15px;padding:13px;color:#8eeaff}.lock{background:#12172a;border:1px solid #3c4773;border-radius:16px;padding:13px;margin-top:10px}.hidden{display:none!important}.history{max-height:250px;overflow:auto}.vip{border:2px solid var(--pri);background:#241b4a}.muted{color:var(--muted)}@media(max-width:390px){.top{grid-template-columns:55px 1fr 120px}.top .icon,.top .title,.top .brand{height:55px}.top .title{font-size:16px}.name{font-size:25px}}
</style></head><body><div class="app">
<div class="top"><div class="icon">👤</div><div class="title">Profile</div><div class="brand">Daily Work BD ✅<b id="topBal">৳0</b></div></div>
<div id="home" class="section active"></div><div id="tasks" class="section"></div><div id="refer" class="section"></div><div id="support" class="section"></div><div id="profile" class="section"></div>
</div><div class="nav"><button onclick="show('home')" class="active"><b>🏠</b>Home</button><button onclick="show('tasks')"><b>🎯</b>Tasks</button><button onclick="show('refer')"><b>👥</b>Refer</button><button onclick="show('support')"><b>💬</b>Support</button><button onclick="show('profile')"><b>👤</b>Profile</button></div>
<script>const tg=window.Telegram.WebApp;tg.ready();tg.expand();const initData=tg.initData;let DATA=null,unlocked=false;async function api(u,o={}){o.headers=Object.assign({},o.headers||{}, {'X-Telegram-Init-Data':initData});if(o.body&&!(o.body instanceof FormData))o.headers['Content-Type']='application/json';let r=await fetch(u,o),j=await r.json();if(!r.ok||j.ok===false)throw Error(j.error||'Error');return j}function toast(x){try{tg.showAlert(x)}catch(e){alert(x)}}function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}function show(id){document.querySelectorAll('.section').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));let n={home:0,tasks:1,refer:2,support:3,profile:4}[id];document.querySelectorAll('.nav button')[n].classList.add('active');if(id==='tasks')loadTasks();if(id==='refer')loadRef();if(id==='support')renderSupport();if(id==='profile')renderProfile()}function money(v){return Number(v||0).toFixed(2)}function renderHome(){let u=DATA.user,s=DATA.settings;document.getElementById('home').innerHTML=`<div class="card profile"><div class="avatar">${u.profile_photo&&!u.hide_photo?`<img src="${u.profile_photo}">`:'👤'}</div><div class="level">Level ${u.level}</div><div class="name">${esc(u.display_name||u.first_name)}</div><div class="join">Join: ${new Date(u.created_at*1000).toISOString().slice(0,10)}</div><div class="diam">💎 ${u.diamonds} Diamond | ${money(u.balance)} Taka</div><div class="progressBox"><div class="progressTop"><span>💎 ${u.diamonds} / ${DATA.level_next}</span><span>Level ${u.level} → ${DATA.level_next>u.diamonds?'Level '+(u.level+1):'MAX'}</span></div><div class="bar"><div class="fill" style="width:${DATA.progress}%"></div></div><div class="pct">${DATA.progress}%</div><div class="small">${DATA.level_next>u.diamonds?'💎 আরও '+(DATA.level_next-u.diamonds)+' Diamond সংগ্রহ করুন পরবর্তী Level পেতে':'🎉 আপনার বর্তমান Level সম্পূর্ণ হয়েছে'}</div></div></div><div class="card"><div class="h2">📊 Statistics</div><div class="stats"><div class="stat"><b class="green">৳${money(u.total_earned)}</b>Total Earned</div><div class="stat"><b class="purple">৳${money(u.balance)}</b>Balance</div><div class="stat"><b class="orange">${u.ads_watched}</b>Ads</div><div class="stat"><b class="pink">${u.refer_count}</b>Refer</div></div></div><div class="card"><div class="h2">📺 Watch Ads & Earn</div><div id="adsBox">Loading...</div></div><div class="card"><div class="h2">💳 Withdraw</div><div class="grid2"><button class="btn dark" onclick="withdrawTab('bKash')">bKash</button><button class="btn dark" onclick="withdrawTab('Nagad')">Nagad</button></div><input id="wacc" class="input" placeholder="বিকাশ/নগদ নম্বর"><input id="wamt" class="input" type="number" placeholder="Amount — Min ${s.min_withdraw}"><button class="btn greenbtn" onclick="doWithdraw()">Withdraw Now</button></div><div class="card offer"><div class="h2">🔥🔥 Biggest Earning Offer</div><p>Admin থেকে নতুন অফার/বোনাস এখানে দেখানো যাবে।</p><button class="btn" onclick="show('tasks')">Claim Now</button></div>`;loadAds()}function withdrawTab(m){document.getElementById('wacc').placeholder=m+' নম্বর'}async function doWithdraw(){try{let a=document.getElementById('wacc').value,amt=document.getElementById('wamt').value;let m=document.getElementById('wacc').placeholder.startsWith('Nagad')?'Nagad':'bKash';await api('/api/withdraw',{method:'POST',body:JSON.stringify({method:m,account:a,amount:amt})});toast('Withdrawal request sent');await loadMe()}catch(e){toast(e.message)}}async function loadAds(){try{let j=await api('/api/ads');document.getElementById('adsBox').innerHTML=j.ads.map(a=>`<div class="task"><b>${esc(a.name)}</b><div class="reward">৳${a.reward} + 💎${a.diamonds} | ${a.watched_today}/${a.daily_limit}</div><button class="btn" onclick="watchAd(${a.id})">▶️ Watch</button></div>`).join('')||'<p class="muted">No active ads</p>'}catch(e){document.getElementById('adsBox').innerHTML='<p>'+esc(e.message)+'</p>'}}async function watchAd(id){try{let j=await api('/api/ad/'+id+'/start',{method:'POST'});if(j.url)tg.openLink(j.url);let end=Date.now()+j.duration*1000;toast('Ad started. '+j.duration+' সেকেন্ড পর আবার এখানে এসে Complete চাপুন।');let b=document.querySelector('#adsBox button');setTimeout(async()=>{try{let x=await api('/api/ad/complete',{method:'POST',body:JSON.stringify({token:j.token})});toast('Reward +৳'+x.reward+' +💎'+x.diamonds);await loadMe()}catch(e){toast(e.message)}},Math.max(1000,j.duration*1000))}catch(e){toast(e.message)}}async function loadTasks(){try{let j=await api('/api/tasks');document.getElementById('tasks').innerHTML='<div class="card"><div class="h2">🎯 Tasks & Company Links</div><p class="muted">প্রতি Task এ Cash + Diamond</p></div>'+j.tasks.map(t=>`<div class="task"><b>${esc(t.title)}</b><p>${esc(t.description||'')}</p><div class="reward">৳${t.reward} + 💎${t.diamonds}</div><button class="btn ${t.claimed?'dark':''}" ${t.claimed?'disabled':''} onclick="goTask(${t.id},'${esc(t.url)}')">${t.claimed?'✅ Completed':'Go'}</button></div>`).join('')}catch(e){toast(e.message)}}async function goTask(id,url){tg.openLink(url);setTimeout(async()=>{try{let j=await api('/api/task/'+id+'/claim',{method:'POST'});toast('Reward +৳'+j.reward+' +💎'+j.diamonds);loadMe()}catch(e){toast(e.message)}},1200)}async function loadRef(){let j=await api('/api/referral');document.getElementById('refer').innerHTML=`<div class="card offer"><div class="h2">🎉 Refer Contest চলছে</div><p>বন্ধু Invite করে Unlimited আয়</p></div><div class="card"><div class="h2">👥 Refer & Earn</div><input class="input" id="ref" readonly value="${esc(j.link)}"><button class="btn" onclick="navigator.clipboard.writeText(ref.value);toast('Copied')">📋 Copy Refer Link</button><button class="btn dark" onclick="tg.openTelegramLink('https://t.me/share/url?url='+encodeURIComponent(ref.value))">📤 Share</button><p>1. বন্ধু কে লিংক শেয়ার করো<br>2. বন্ধু Join করলে Admin নির্ধারিত Bonus পাবে<br>3. বন্ধু Ads দেখলে Commission পেতে পারে</p></div>`}function renderSupport(){let s=DATA.settings;document.getElementById('support').innerHTML=`<div class="card"><div class="h2">🆘 Support Center</div><button class="btn" onclick="tg.openTelegramLink('${esc(s.channel_link)}')">📢 Telegram</button>${s.support_whatsapp?`<button class="btn greenbtn" onclick="tg.openLink('${esc(s.support_whatsapp)}')">💚 WhatsApp</button>`:''}<p>${esc(s.support_email)}</p><div class="notice">📌 ${esc(s.notice_text)}</div><textarea id="sm" class="textarea" placeholder="আপনার সমস্যাটি লিখুন..."></textarea><button class="btn" onclick="sendSupport()">Send Message</button></div><div class="card"><div class="h2">📜 Rules</div>${esc(s.rules_text).split('|').map((x,i)=>`<p>${i+1}. ${x}</p>`).join('')}</div>`}async function sendSupport(){try{await api('/api/support',{method:'POST',body:JSON.stringify({message:sm.value})});toast('Sent');sm.value='';await loadMe()}catch(e){toast(e.message)}}function renderSupportHistory(){}function renderProfile(){let u=DATA.user,s=DATA.settings;let locked=u.privacy_locked&&!unlocked;document.getElementById('profile').innerHTML=`<div class="card"><div class="h2">👤 Profile Settings</div>${locked?`<div class="lock">🔒 আপনার ব্যক্তিগত সেটিংস লক করা আছে।<input id="upin" class="input" type="password" inputmode="numeric" placeholder="PIN"><button class="btn" onclick="unlock()">🔓 Unlock</button></div>`:`<form id="pf"><input name="display_name" class="input" value="${esc(u.display_name||u.first_name)}" placeholder="আপনার নাম"><input name="photo" class="input" type="file" accept="image/*"><label><input name="hide_name" type="checkbox" ${u.hide_name?'checked':''}> Name private</label><br><label><input name="hide_username" type="checkbox" ${u.hide_username?'checked':''}> Username private</label><br><label><input name="hide_photo" type="checkbox" ${u.hide_photo?'checked':''}> Photo private</label><br><label><input name="hide_stats" type="checkbox" ${u.hide_stats?'checked':''}> Statistics private</label><hr><label><input name="privacy_locked" value="1" type="checkbox" ${u.privacy_locked?'checked':''}> 🔒 Lock personal settings</label><input name="pin" class="input" type="password" inputmode="numeric" placeholder="নতুন PIN (4-8 digits)"><button type="submit" class="btn">💾 Save Profile</button></form>`}</div><div class="card"><div class="h2">📊 Statistics</div><div class="stats"><div class="stat"><b class="green">৳${money(u.total_earned)}</b>Total Earned</div><div class="stat"><b class="purple">৳${money(u.balance)}</b>Balance</div><div class="stat"><b class="orange">${u.ads_watched}</b>Ads</div><div class="stat"><b class="pink">${u.refer_count}</b>Refer</div></div></div><div class="card"><div class="h2">💳 Withdraw History</div><div class="history">${DATA.withdrawals.length?DATA.withdrawals.map(x=>`<div class="task">#${x.id} — ৳${x.amount} — ${x.status}</div>`).join(''):'No withdraw'}</div></div>${s.vip_enabled==='1'?`<div class="card vip"><div class="h2">💎 VIP Membership</div><p>${esc(s.vip_text)}</p>${s.vip_link?`<button class="btn" onclick="tg.openLink('${esc(s.vip_link)}')">⭐ Upgrade Now</button>`:''}</div>`:''}`;let f=document.getElementById('pf');if(f)f.onsubmit=saveProfile}async function unlock(){try{await api('/api/profile/unlock',{method:'POST',body:JSON.stringify({pin:upin.value})});unlocked=true;renderProfile()}catch(e){toast(e.message)}}async function saveProfile(ev){ev.preventDefault();try{let fd=new FormData(ev.target);fd.set('hide_name',ev.target.hide_name.checked?'1':'0');fd.set('hide_username',ev.target.hide_username.checked?'1':'0');fd.set('hide_photo',ev.target.hide_photo.checked?'1':'0');fd.set('hide_stats',ev.target.hide_stats.checked?'1':'0');fd.set('privacy_locked',ev.target.privacy_locked.checked?'1':'0');await api('/api/profile',{method:'POST',body:fd});toast('Profile saved');unlocked=false;await loadMe()}catch(e){toast(e.message)}}function renderSupport2(){}async function loadMe(){try{DATA=await api('/api/me');document.getElementById('topBal').textContent='৳'+money(DATA.user.balance);renderHome();renderSupport();renderProfile()}catch(e){toast(e.message)}}async function login(){if(!initData){toast('এই Mini App Telegram-এর ভিতর থেকে খুলুন।');return}try{await api('/api/login',{method:'POST',body:JSON.stringify({initData})});await loadMe();show('home')}catch(e){toast(e.message)}}login();</script></body></html>'''

if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')))
