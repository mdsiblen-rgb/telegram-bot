"""
প্রতিদিনের কাজ BD - FINAL LONG VERSION (2500+ Line Logic in Single File)
আগের বড় ফাইলের সব ডিজাইন + নতুন ৭টা দাবি = A-Z Complete

1. ইউজার A-Z: জয়েন ডেট, টাইম, ব্যালেন্স, মোট আয়, কটা বিজ্ঞাপন, কটা রেফার, কে রেফার করলো
2. এডমিন A-Z: মোট ডলার, মোট টাকা জমা, মোট ইউজার, কোম্পানি এড
3. 2 নং পেজে রেফার বাটন + এডমিন থেকে লিংক চেঞ্জ
4. 3 নং পেজের খালি জায়গা এডমিন থেকে এডিট
5. 4 নং পেজে bKash/Nagad কার্ড ডিজাইন + পেমেন্ট টাইম এডমিন লিখবে
6. 5 নং পেজে টেলিগ্রাম প্রোফাইল অটো
7. উইথড্র A-Z: কে কখন উইথড্র করলো, তুমি কখন টাকা দিলে
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, session, redirect, g

app = Flask(__name__)
app.secret_key = 'protidiener_kaj_bd_FINAL_2026_secure_key_@123'
DATABASE = 'protiden_final_long.db'

# ==================== DATABASE ====================
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        name TEXT,
        username TEXT,
        photo_url TEXT,
        balance INTEGER DEFAULT 60,
        total_earned INTEGER DEFAULT 60,
        total_withdraw INTEGER DEFAULT 0,
        ads_watched INTEGER DEFAULT 0,
        ads_watched_today INTEGER DEFAULT 0,
        last_ad_date TEXT,
        referrals INTEGER DEFAULT 0,
        refer_code TEXT,
        referred_by TEXT,
        join_date TEXT,
        join_time TEXT,
        join_datetime TEXT,
        last_active TEXT,
        daily_claimed_date TEXT,
        is_banned INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS withdraws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        user_name TEXT,
        amount INTEGER,
        method TEXT,
        number TEXT,
        status TEXT DEFAULT 'pending',
        request_date TEXT,
        request_time TEXT,
        request_datetime TEXT,
        approve_date TEXT,
        approve_time TEXT,
        approve_datetime TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS ad_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        view_date TEXT,
        view_time TEXT,
        view_datetime TEXT,
        amount INTEGER DEFAULT 1
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS company_ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        image_url TEXT,
        link_url TEXT,
        is_active INTEGER DEFAULT 1
    )''')

    defaults = {
        'monetag_zone_id': '11764581',
        'ad_timer_seconds': '30',
        'ad_daily_limit': '100',
        'welcome_bonus_amount': '60',
        'daily_checkin_bonus': '10',
        'refer_bonus_amount': '50',
        'min_withdraw': '100',
        'telegram_channel_url': 'https://t.me/yourchannel',
        'telegram_channel_title': 'Telegram Channel Join',
        'youtube_channel_url': 'https://youtube.com/@yourchannel',
        'youtube_channel_title': 'YouTube Subscribe',
        'facebook_page_url': 'https://facebook.com/yourpage',
        'facebook_page_title': 'Facebook Page Like',
        'company_task_1_url': 'https://example.com/company1',
        'company_task_1_title': 'কোম্পানি টাস্ক ১ - ভিজিট করুন',
        'company_task_2_url': 'https://example.com/company2',
        'company_task_2_title': 'কোম্পানি টাস্ক ২ - ভিজিট করুন',
        'company_task_3_url': 'https://example.com/company3',
        'company_task_3_title': 'কোম্পানি টাস্ক ৩ - ভিজিট করুন',
        'refer_link_base_url': 'https://t.me/ProtidenKajBDBot?start=',
        'refer_button_text': '🔗 রেফার লিংক কপি করুন',
        'page1_top_own_ad_text': '🔥 স্পেশাল অফার! আমাদের প্রিমিয়াম মেম্বারশিপ নিন এবং 2x বেশি আয় করুন! বিস্তারিত জানতে সাপোর্টে মেসেজ দিন।',
        'page1_top_own_ad_link': 'https://t.me/yourchannel',
        'page1_top_own_ad_active': 'true',
        'page3_middle_custom_text': '🎧 সাপোর্ট সেন্টার\n\nআমাদের সাপোর্ট টিম ২৪ ঘন্টা আপনাদের সেবায় নিয়োজিত। যেকোনো সমস্যা, পেমেন্ট সংক্রান্ত বা টাস্ক বুঝতে অসুবিধা হলে নিচের অফিসিয়াল চ্যানেলে যোগাযোগ করুন। আমরা ২ ঘন্টার মধ্যে রিপ্লাই দেই।\n\n⚠️ নোট: ফেক স্ক্রিনশট দিলে একাউন্ট ব্যান হবে।',
        'page3_middle_custom_text_active': 'true',
        'page4_payment_time_text': '⏰ পেমেন্ট সময়: প্রতিদিন বিকাল ৫টা - রাত ১০টা (শুক্রবার বন্ধ)',
        'page4_bkash_personal_number': '01712-345678',
        'page4_nagad_personal_number': '01812-345678',
        'page4_bkash_active': 'true',
        'page4_nagad_active': 'true',
        'slider_image_1': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=200&fit=crop',
        'slider_image_2': 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=600&h=200&fit=crop',
        'slider_image_3': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=200&fit=crop',
        'admin_total_earning_bdt': '0',
        'admin_monetag_total_dollars': '0.00',
        'admin_monetag_today_dollars': '0.00',
        'company_ads_global_enabled': 'true',
        'app_name': 'প্রতিদিনের কাজ BD',
        'app_version': 'Final v5.0'
    }
    for k,v in defaults.items():
        c.execute('INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)', (k,v))
    conn.commit()
    conn.close()

init_db()

def get_setting(key):
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        row = conn.execute('SELECT value FROM settings WHERE key=?',(key,)).fetchone()
        conn.close()
        return row['value'] if row else ''
    except:
        return ''

def set_setting(key, value):
    conn = sqlite3.connect(DATABASE)
    conn.execute('INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)',(key,value))
    conn.commit()
    conn.close()

# ==================== MAIN FRONTEND (LONG DESIGN - 5 PAGES EXACT LIKE YOUR SCREENSHOT) ====================
MAIN_HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{{app_name}}</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="//libtl.com/sdk.js" data-zone="{{monetag_zone_id}}" data-sdk="show_{{monetag_zone_id}}"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;font-family:'Hind Siliguri',sans-serif}
body{background:#eef2ff;overflow-x:hidden;-webkit-tap-highlight-color: transparent;}
.header{background:linear-gradient(135deg,#2a3baf,#3040c8);color:white;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 15px rgba(48,64,200,.3);position:sticky;top:0;z-index:100}
.header-left{display:flex;align-items:center;gap:12px}
.header-left img{width:48px;height:48px;border-radius:50%;border:3px solid white;background:white;object-fit:cover}
.header-title{font-size:18px;font-weight:700;line-height:1.2}
.header-subtitle{font-size:11px;opacity:.8}
.balance-box{background:rgba(255,255,255,.2);backdrop-filter:blur(10px);padding:8px 14px;border-radius:30px;display:flex;align-items:center;gap:6px;border:1px solid rgba(255,255,255,.3)}
.balance-box i{font-size:18px;color:#ffeb3b}
.balance-amount{font-size:22px;font-weight:800}
.card{background:white;margin:14px 12px;border-radius:22px;padding:16px;box-shadow:0 6px 20px rgba(0,0,0,.08);border:1px solid #f0f0f0}
.card-header{font-size:17px;font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:8px;color:#1a1a1a}
.slider-container{position:relative;width:100%;height:150px;border-radius:16px;overflow:hidden;margin-bottom:14px;background:#f5f5f5}
.slider-container img{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;opacity:0;transition:opacity .8s}
.slider-container img.active{opacity:1}
.slider-dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px}
.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.5);transition:.3s}
.dot.active{background:white;width:22px;border-radius:10px}
.own-ad-box{background:linear-gradient(135deg,#FFF9C4 0%,#FFE082 100%);border:2px dashed #FFA000;border-radius:14px;padding:14px;margin:12px 0;text-align:center;position:relative}
.own-ad-box:before{content:'AD';position:absolute;top:-8px;left:12px;background:#FF6F00;color:white;font-size:10px;padding:2px 8px;border-radius:10px;font-weight:bold}
.btn{width:100%;padding:15px;border:none;border-radius:14px;color:white;font-size:16px;font-weight:700;margin:9px 0;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 4px 12px rgba(0,0,0,.15);transition:.2s;position:relative;overflow:hidden}
.btn:active{transform:scale(.97)}
.btn-blue{background:linear-gradient(135deg,#1a3ec1,#2d5bff)} .btn-red{background:linear-gradient(135deg,#d32f2f,#ff5252)} .btn-lightblue{background:linear-gradient(135deg,#0288d1,#29b6f6)} .btn-green{background:linear-gradient(135deg,#2e7d32,#66bb6a)} .btn-orange{background:linear-gradient(135deg,#ef6c00,#ffa726)}
.task-item{display:flex;align-items:center;justify-content:space-between;background:#f8f9ff;padding:14px;border-radius:14px;margin:8px 0;border:1px solid #e8eaff}
.task-left{display:flex;align-items:center;gap:12px}
.task-icon{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;font-size:20px}
.progress-bar{width:100%;height:8px;background:#e0e0e0;border-radius:10px;overflow:hidden;margin-top:8px}
.progress-fill{height:100%;background:linear-gradient(90deg,#3040c8,#5c6bc0);border-radius:10px;transition:.5s}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;background:white;display:flex;justify-content:space-around;padding:8px 0 12px;border-top:1px solid #e0e0e0;z-index:999;box-shadow:0 -4px 20px rgba(0,0,0,.08);border-radius:20px 20px 0 0}
.nav-item{text-align:center;font-size:11px;cursor:pointer;color:#9e9e9e;flex:1;padding:6px;transition:.3s}
.nav-item i{font-size:22px;display:block;margin-bottom:4px}
.nav-item.active{color:#3040c8;font-weight:700;transform:translateY(-2px)}
.nav-item.active i{color:#3040c8}
.page{display:none;padding-bottom:90px;animation:fadeIn .3s} .page.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.withdraw-card-main{background:linear-gradient(135deg,#e91e63 0%,#ff5722 100%);color:white;border-radius:22px;padding:22px;margin:12px 0;position:relative;overflow:hidden;box-shadow:0 8px 20px rgba(233,30,99,.3)}
.withdraw-card-main.nagad{background:linear-gradient(135deg,#ff6f00 0%,#ffca28 100%)}
.withdraw-card-main:before{content:'';position:absolute;top:-50%;right:-30%;width:200px;height:200px;background:rgba(255,255,255,.15);border-radius:50%}
.profile-avatar-container{position:relative;width:92px;height:92px;margin:0 auto 12px}
.profile-avatar{width:92px;height:92px;border-radius:50%;border:4px solid #3040c8;object-fit:cover;background:#f0f0f0}
.profile-verified{position:absolute;bottom:0;right:0;background:#4caf50;color:white;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:3px solid white;font-size:14px}
.info-row{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid #f0f0f0;font-size:14px}
.info-row:last-child{border:none}
.info-label{color:#666;display:flex;align-items:center;gap:6px}
.info-value{font-weight:700;color:#1a1a1a}
</style>
</head>
<body>
<div class="header">
  <div class="header-left">
    <img id="topUserPhoto" src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png">
    <div><div class="header-title">{{app_name}}</div><div class="header-subtitle">Final v5.0 • Online</div></div>
  </div>
  <div class="balance-box"><i class="fas fa-coins"></i><span class="balance-amount">৳<span id="headerBalance">60</span></span></div>
</div>

<!-- HOME PAGE - 1 -->
<div id="page-home" class="page active">
  <div class="card">
    <div class="card-header"><i class="fas fa-images" style="color:#3040c8"></i> স্পেশাল অফার</div>
    <div class="slider-container" id="mainSlider">
      <img id="slide1" class="active"><img id="slide2"><img id="slide3">
      <div class="slider-dots"><div class="dot active"></div><div class="dot"></div><div class="dot"></div></div>
    </div>
    <div class="own-ad-box" id="page1OwnAdBox" onclick="openOwnAdLink()"><span id="page1OwnAdText"></span></div>
    <button class="btn btn-blue" onclick="watchMonetagAd()"><i class="fas fa-play"></i> বিজ্ঞাপন দেখুন (৩০ সেকেন্ড)</button>
    <div style="display:flex;justify-content:space-between;font-size:13px;color:#666;margin:6px 2px"><span>আজ দেখেছেন: <b id="todayAds">0</b>/{{ad_daily_limit}}</span><span style="color:#4caf50">প্রতি এড ৳1</span></div>
    <div class="progress-bar"><div class="progress-fill" id="adProgress" style="width:0%"></div></div>
    <button class="btn btn-green" onclick="claimDailyBonus()"><i class="fas fa-gift"></i> ডেইলি চেক-ইন ৳{{daily_checkin_bonus}}</button>
  </div>

  <div class="card">
    <div class="card-header"><i class="fas fa-tasks" style="color:#ff5722"></i> কোম্পানির টাস্ক (এডমিন থেকে সব লিংক চেঞ্জ)</div>
    <div class="task-item"><div class="task-left"><div class="task-icon" style="background:#0088cc"><i class="fab fa-telegram"></i></div><div><div style="font-weight:700">Telegram Channel</div><div style="font-size:12px;color:#666">জয়েন করুন</div></div></div><button class="btn btn-blue" style="width:auto;padding:8px 18px;margin:0" onclick="doCompanyTask('telegram_channel_url')">Go</button></div>
    <div class="task-item"><div class="task-left"><div class="task-icon" style="background:#ff0000"><i class="fab fa-youtube"></i></div><div><div style="font-weight:700">YouTube</div><div style="font-size:12px;color:#666">সাবস্ক্রাইব</div></div></div><button class="btn btn-red" style="width:auto;padding:8px 18px;margin:0" onclick="doCompanyTask('youtube_channel_url')">Go</button></div>
    <div class="task-item"><div class="task-left"><div class="task-icon" style="background:#1877f2"><i class="fab fa-facebook"></i></div><div><div style="font-weight:700">Facebook</div><div style="font-size:12px;color:#666">লাইক দিন</div></div></div><button class="btn btn-lightblue" style="width:auto;padding:8px 18px;margin:0" onclick="doCompanyTask('facebook_page_url')">Go</button></div>
    <div class="task-item"><div class="task-left"><div class="task-icon" style="background:#ff6f00"><i class="fas fa-briefcase"></i></div><div><div style="font-weight:700" id="ct1Title"></div><div style="font-size:12px;color:#666">কোম্পানি এড</div></div></div><button class="btn btn-orange" style="width:auto;padding:8px 18px;margin:0" onclick="doCompanyTask('company_task_1_url')">Go</button></div>
    <div class="task-item"><div class="task-left"><div class="task-icon" style="background:#6a1b9a"><i class="fas fa-building"></i></div><div><div style="font-weight:700" id="ct2Title"></div></div></div><button class="btn btn-orange" style="width:auto;padding:8px 18px;margin:0" onclick="doCompanyTask('company_task_2_url')">Go</button></div>
    <div class="task-item"><div class="task-left"><div class="task-icon" style="background:#2e7d32"><i class="fas fa-industry"></i></div><div><div style="font-weight:700" id="ct3Title"></div></div></div><button class="btn btn-orange" style="width:auto;padding:8px 18px;margin:0" onclick="doCompanyTask('company_task_3_url')">Go</button></div>
  </div>
</div>

<!-- INCOME PAGE - 2 WITH REFER BUTTON LIKE OTHER BUTTONS -->
<div id="page-income" class="page">
  <div class="card" style="background:linear-gradient(135deg,#3040c8,#5c6bc0);color:white;text-align:center">
    <div style="font-size:14px;opacity:.9">আপনার মোট রেফার আয়</div>
    <div style="font-size:36px;font-weight:800;margin:8px 0">৳<span id="referEarn">0</span></div>
    <div style="background:rgba(255,255,255,.2);padding:10px;border-radius:12px;display:flex;justify-content:space-around"><div><div style="font-size:20px;font-weight:800" id="totalReferCount">0</div><div style="font-size:12px">মোট রেফার</div></div><div><div style="font-size:20px;font-weight:800">৳{{refer_bonus_amount}}</div><div style="font-size:12px">প্রতি রেফার</div></div></div>
  </div>
  <div class="card">
    <div class="card-header"><i class="fas fa-link" style="color:#3040c8"></i> রেফার করুন (বাটন ডিজাইন বাকিগুলোর মতো)</div>
    <button class="btn btn-blue" onclick="copyReferLink()"><i class="fas fa-copy"></i> <span id="referBtnText">{{refer_button_text}}</span></button>
    <div style="background:#f5f7ff;border:2px dashed #3040c8;padding:14px;border-radius:14px;word-break:break-all;font-size:13px;margin:12px 0" id="referLinkDisplay"></div>
    <button class="btn btn-green" onclick="shareReferLink()"><i class="fas fa-share-alt"></i> বন্ধুদের শেয়ার করুন</button>
    <div style="font-size:12px;color:#666;text-align:center;margin-top:8px">এই লিংক এডমিন প্যানেল থেকে যেকোনো সময় চেঞ্জ করা যাবে</div>
  </div>
</div>

<!-- SUPPORT PAGE - 3 WITH EDITABLE AREA -->
<div id="page-support" class="page">
  <div class="card">
    <div class="card-header" style="justify-content:center;font-size:20px"><i class="fas fa-headset"></i> সাপোর্ট সেন্টার</div>
    <button class="btn btn-blue" onclick="openSupportLink('telegram_channel_url')"><i class="fab fa-telegram"></i> Telegram Channel</button>
    <button class="btn btn-red" onclick="openSupportLink('youtube_channel_url')"><i class="fab fa-youtube"></i> YouTube Channel</button>
    <button class="btn btn-lightblue" onclick="openSupportLink('facebook_page_url')"><i class="fab fa-facebook"></i> Facebook Page</button>
    <div style="margin-top:20px;background:#f8f9ff;border-radius:16px;padding:18px;border-left:5px solid #3040c8">
      <div style="font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:8px"><i class="fas fa-edit" style="color:#3040c8"></i> এডমিন নোট (এডমিন থেকে এডিটেবল খালি জায়গা)</div>
      <div id="adminCustomSupportText" style="white-space:pre-wrap;line-height:1.7;color:#333;font-size:14px"></div>
    </div>
  </div>
</div>

<!-- WITHDRAW PAGE - 4 WITH BKASH/NAGAD CARD DESIGN -->
<div id="page-withdraw" class="page">
  <div class="card">
    <div class="card-header"><i class="fas fa-money-bill-wave" style="color:#e91e63"></i> উইথড্র করুন</div>
    <div style="background:#fff3e0;padding:12px;border-radius:12px;text-align:center;font-weight:700;color:#e65100;margin-bottom:14px" id="withdrawPaymentTime"></div>
    <div class="withdraw-card-main"><div style="display:flex;justify-content:space-between;align-items:center"><div><div style="font-size:13px;opacity:.9">bKash Personal</div><div style="font-size:20px;font-weight:800;margin-top:4px" id="bkashNumberDisplay"></div></div><i class="fas fa-wallet" style="font-size:40px;opacity:.3"></i></div><div style="margin-top:14px;font-size:12px;background:rgba(0,0,0,.15);padding:8px;border-radius:8px">✅ bKash এ পেমেন্ট করা হয়</div></div>
    <div class="withdraw-card-main nagad"><div style="display:flex;justify-content:space-between;align-items:center"><div><div style="font-size:13px;opacity:.9">Nagad Personal</div><div style="font-size:20px;font-weight:800;margin-top:4px" id="nagadNumberDisplay"></div></div><i class="fas fa-mobile-alt" style="font-size:40px;opacity:.3"></i></div><div style="margin-top:14px;font-size:12px;background:rgba(0,0,0,.15);padding:8px;border-radius:8px">✅ Nagad এ পেমেন্ট করা হয়</div></div>
    <div style="background:#f5f5f5;padding:16px;border-radius:16px;margin-top:10px">
      <label style="font-weight:700;font-size:13px">টাকার পরিমাণ (Min ৳{{min_withdraw}})</label>
      <input id="wdAmountInput" type="number" placeholder="যেমন: 200" style="width:100%;padding:14px;margin:8px 0 12px;border-radius:12px;border:2px solid #e0e0e0;font-size:16px">
      <label style="font-weight:700;font-size:13px">মেথড সিলেক্ট করুন</label>
      <select id="wdMethodSelect" style="width:100%;padding:14px;margin:8px 0 12px;border-radius:12px;border:2px solid #e0e0e0"><option value="bKash">bKash Personal</option><option value="Nagad">Nagad Personal</option></select>
      <label style="font-weight:700;font-size:13px">আপনার নাম্বার</label>
      <input id="wdNumberInput" type="text" placeholder="01XXXXXXXXX" style="width:100%;padding:14px;margin:8px 0 12px;border-radius:12px;border:2px solid #e0e0e0;font-size:16px">
      <button class="btn btn-blue" onclick="submitWithdrawRequest()"><i class="fas fa-paper-plane"></i> উইথড্র রিকোয়েস্ট পাঠান</button>
    </div>
  </div>
</div>

<!-- PROFILE PAGE - 5 WITH AUTO TELEGRAM PHOTO -->
<div id="page-profile" class="page">
  <div class="card" style="text-align:center">
    <div class="profile-avatar-container">
      <img id="mainProfilePhoto" class="profile-avatar" src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png">
      <div class="profile-verified"><i class="fas fa-check"></i></div>
    </div>
    <h2 id="profileDisplayName" style="font-size:22px;font-weight:800">Loading...</h2>
    <p id="profileDisplayUsername" style="color:#666;font-size:14px;margin-top:4px"></p>
    <div style="background:#e8f5e9;color:#2e7d32;padding:8px 16px;border-radius:20px;display:inline-flex;align-items:center;gap:6px;margin-top:10px;font-size:13px;font-weight:700"><i class="fas fa-circle" style="font-size:8px"></i> Active • Telegram Auto Login</div>
    
    <div style="text-align:left;margin-top:22px;background:#f8f9ff;border-radius:16px;padding:16px">
      <div class="info-row"><span class="info-label"><i class="fas fa-id-badge" style="color:#3040c8"></i> Telegram ID</span><span class="info-value" id="infoTgId">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-calendar-plus" style="color:#ff5722"></i> জয়েন ডেট</span><span class="info-value" id="infoJoinDate">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-clock" style="color:#ff9800"></i> জয়েন টাইম</span><span class="info-value" id="infoJoinTime">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-coins" style="color:#ffb300"></i> বর্তমান ব্যালেন্স</span><span class="info-value" style="color:#2e7d32" id="infoBalance">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-chart-line" style="color:#3040c8"></i> মোট আয়</span><span class="info-value" id="infoTotalEarn">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-eye" style="color:#9c27b0"></i> বিজ্ঞাপন দেখেছেন</span><span class="info-value" id="infoTotalAds">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-users" style="color:#0288d1"></i> রেফার করেছেন</span><span class="info-value" id="infoTotalRefer">-</span></div>
      <div class="info-row"><span class="info-label"><i class="fas fa-money-bill" style="color:#e91e63"></i> মোট উইথড্র</span><span class="info-value" id="infoTotalWd">-</span></div>
    </div>
    <div style="font-size:11px;color:#999;margin-top:14px">Telegram প্রোফাইল ফটো অটোমেটিক সেট করা হয়েছে</div>
  </div>
</div>

<div class="bottom-nav">
  <div class="nav-item active" onclick="switchPage('home',this)"><i class="fas fa-home"></i>হোম</div>
  <div class="nav-item" onclick="switchPage('income',this)"><i class="fas fa-sack-dollar"></i>আয়</div>
  <div class="nav-item" onclick="switchPage('support',this)"><i class="fas fa-headset"></i>সাপোর্ট</div>
  <div class="nav-item" onclick="switchPage('withdraw',this)"><i class="fas fa-wallet"></i>উইথড্র</div>
  <div class="nav-item" onclick="switchPage('profile',this)"><i class="fas fa-user-circle"></i>প্রোফাইল</div>
</div>

<script>
let tgApp = window.Telegram.WebApp; tgApp.expand(); tgApp.enableClosingConfirmation();
let currentUser = tgApp.initDataUnsafe.user || {id:'123456789', first_name:'Demo User', username:'demo_user', photo_url:'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'};

// Auto set Telegram photo - তোমার ৫ নং পেজের দাবি
if(currentUser.photo_url){
  document.getElementById('topUserPhoto').src = currentUser.photo_url;
  document.getElementById('mainProfilePhoto').src = currentUser.photo_url;
}
document.getElementById('profileDisplayName').innerText = currentUser.first_name + (currentUser.last_name ? ' ' + currentUser.last_name : '');
document.getElementById('profileDisplayUsername').innerText = '@' + (currentUser.username || 'username');
document.getElementById('infoTgId').innerText = currentUser.id;

let ownAdLinkGlobal = '';
function switchPage(pageName, el){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('page-'+pageName).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  if(el) el.classList.add('active');
  else document.querySelector(`[onclick="switchPage('${pageName}',this)"]`)?.classList.add('active');
}

// Slider Auto
let currentSlide = 0;
function autoSlider(){
  let slides = document.querySelectorAll('#mainSlider img');
  let dots = document.querySelectorAll('.dot');
  if(slides.length===0) return;
  slides.forEach(s=>s.classList.remove('active'));
  dots.forEach(d=>d.classList.remove('active'));
  currentSlide = (currentSlide+1)%slides.length;
  slides[currentSlide].classList.add('active');
  dots[currentSlide].classList.add('active');
}
setInterval(autoSlider, 3500);

function loadAllData(){
  fetch(`/api/user_full_info?tg_id=${currentUser.id}&name=${encodeURIComponent(currentUser.first_name)}&username=${currentUser.username||''}&photo=${encodeURIComponent(currentUser.photo_url||'')}&refer=${tgApp.initDataUnsafe.start_param||''}`)
  .then(r=>r.json()).then(data=>{
    document.getElementById('headerBalance').innerText = data.balance;
    document.getElementById('todayAds').innerText = data.ads_today;
    document.getElementById('adProgress').style.width = (data.ads_today/{{ad_daily_limit}}*100)+'%';
    document.getElementById('page1OwnAdText').innerText = data.page1_ad_text;
    ownAdLinkGlobal = data.page1_ad_link;
    document.getElementById('adminCustomSupportText').innerText = data.page3_text;
    document.getElementById('withdrawPaymentTime').innerText = data.pay_time;
    document.getElementById('bkashNumberDisplay').innerText = data.bkash_num;
    document.getElementById('nagadNumberDisplay').innerText = data.nagad_num;
    document.getElementById('referLinkDisplay').innerText = data.refer_link;
    document.getElementById('referBtnText').innerText = data.refer_btn_text;
    document.getElementById('totalReferCount').innerText = data.referrals;
    document.getElementById('infoJoinDate').innerText = data.join_date;
    document.getElementById('infoJoinTime').innerText = data.join_time;
    document.getElementById('infoBalance').innerText = '৳'+data.balance;
    document.getElementById('infoTotalEarn').innerText = '৳'+data.total_earned;
    document.getElementById('infoTotalAds').innerText = data.ads_watched+' টি';
    document.getElementById('infoTotalRefer').innerText = data.referrals+' জন';
    document.getElementById('infoTotalWd').innerText = '৳'+data.total_withdraw;
    document.getElementById('referEarn').innerText = data.referrals*{{refer_bonus_amount}};
    document.getElementById('slide1').src = data.slider1;
    document.getElementById('slide2').src = data.slider2;
    document.getElementById('slide3').src = data.slider3;
    document.getElementById('ct1Title').innerText = data.ct1_title;
    document.getElementById('ct2Title').innerText = data.ct2_title;
    document.getElementById('ct3Title').innerText = data.ct3_title;
  });
}
loadAllData();

function watchMonetagAd(){
  let btn = event.currentTarget; let original = btn.innerHTML; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ৩০ সেকেন্ড অপেক্ষা...'; btn.disabled=true;
  if(typeof show_{{monetag_zone_id}} === 'function'){ try{ show_{{monetag_zone_id}}(); }catch(e){} }
  let sec=30; let iv=setInterval(()=>{sec--; btn.innerHTML=`<i class="fas fa-clock"></i> ${sec}s অপেক্ষা করুন`; if(sec<=0){clearInterval(iv); fetch(`/api/watch_ad_final?tg_id=${currentUser.id}`).then(r=>r.json()).then(d=>{tgApp.HapticFeedback.notificationOccurred('success'); alert(d.msg); loadAllData(); btn.innerHTML=original; btn.disabled=false;});}},1000);
}
function claimDailyBonus(){ fetch(`/api/daily_final?tg_id=${currentUser.id}`).then(r=>r.json()).then(d=>{alert(d.msg); loadAllData();}); }
function doCompanyTask(key){ fetch(`/api/get_task_link?key=${key}`).then(r=>r.json()).then(d=>{window.open(d.url,'_
