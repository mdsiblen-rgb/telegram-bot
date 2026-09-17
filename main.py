import os
import sqlite3
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import threading

# --- CONFIGURATION ---
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # এখানে BotFather থেকে পাওয়া বটের টোকেন দিন
WEB_URL = "https://yourdomain.com"     # এখানে আপনার সার্ভার বা Ngrok এর HTTPS URL দিন

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # ইউজার টেবিল
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id TEXT PRIMARY KEY, username TEXT, diamonds REAL DEFAULT 0)''')
    # উইথড্র টেবিল
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdrawals 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, method TEXT, number TEXT, diamonds INTEGER, amount REAL, status TEXT DEFAULT 'Pending')''')
    # সেটিংস টেবিল
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('diamond_rate', '10')")   # ১০০০ ডায়মন্ড = ১০ টাকা
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('ad_reward_1', '50')")     # অ্যাড ১ = ৫০ ডায়মন্ড
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('ad_reward_2', '60')")     # অ্যাড ২ = ৬০ ডায়মন্ড
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('link_reward', '40')")     # ডিরেক্ট লিংক = ৪০ ডায়মন্ড
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('tg_reward', '50')")       # চ্যানেল টাস্ক = ৫০ ডায়মন্ড
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('tg_group_reward', '50')") # গ্রুপ টাস্ক = ৫০ ডায়মন্ড
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- TELEGRAM BOT SECTION ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = user.username or user.first_name
    
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

    keyboard = [[InlineKeyboardButton("📱 Open Mini App", web_app=WebAppInfo(url=WEB_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 হ্যালো {user.first_name}!\n💎 আমাদের 'প্রতিদিনের কাজ' মিনি অ্যাপে স্বাগতম। টাস্ক পূরণ করে ডায়মন্ড ও টাকা আয় করতে নিচের বাটনে ক্লিক করুন।",
        reply_markup=reply_markup
    )

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# --- FLASK WEB APP & ADMIN PANEL SECTION ---

@app.route('/')
def user_app():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Jobs BD - Mini App</title>
        <script src="https://tailwindcss.com"></script>
        <script src="https://telegram.org"></script>
        <link rel="stylesheet" href="https://cloudflare.com">
        
        <!-- Ad Scripts -->
        <script src='//://libtl.com' data-zone='11764581' data-sdk='show_11764581'></script>
        <script src='//://libtl.com' data-zone='11798857' data-sdk='show_11798857'></script>
        
        <style>
            .bg-glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); }
            .gradient-border { border: 1px solid rgba(255, 255, 255, 0.1); }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 font-sans min-h-screen pb-10 selection:bg-yellow-500 selection:text-slate-950">
        <div id="app_content" class="max-w-md mx-auto px-4 pt-6 hidden">
            
            <!-- Header Profile Info Card -->
            <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-5 shadow-2xl gradient-border mb-6 flex justify-between items-center">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-gradient-to-tr from-yellow-500 to-amber-400 rounded-full flex items-center justify-center text-slate-950 text-xl font-bold shadow-lg shadow-yellow-500/20">
                        <i class="fa-solid fa-user"></i>
                    </div>
                    <div>
                        <h2 class="text-lg font-bold tracking-wide">Hello, <span id="user_name_display" class="text-amber-400">Partner</span>!</h2>
                        <p class="text-xs text-slate-400">Daily Jobs Dashboard</p>
                    </div>
                </div>
                <div class="bg-slate-950/60 border border-amber-500/30 rounded-xl px-4 py-2 text-right">
                    <p class="text-[10px] text-slate-400 font-medium uppercase tracking-wider">Balance</p>
                    <p class="text-lg font-black text-amber-400">💎 <span id="balance">0</span></p>
                </div>
            </div>

            <!-- Task Container -->
            <div class="space-y-6">
                <!-- Video Ads Section -->
                <div>
                    <h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-circle-play text-red-500"></i> Video Ads Services
                    </h3>
                    <div class="grid grid-cols-2 gap-3">
                        <div class="bg-slate-900 rounded-xl p-4 gradient-border text-center shadow-lg">
                            <p class="font-bold text-sm text-slate-200">Ad Server 1</p>
                            <p class="text-[11px] text-green-400 font-semibold mt-1 mb-3">+💎<span id="r_ad1">50</span> Coins</p>
                            <button onclick="showAdAndReward(1)" class="w-full bg-gradient-to-r from-yellow-500 to-amber-500 text-slate-950 font-extrabold py-2 rounded-lg text-xs shadow-md shadow-yellow-500/10 active:scale-95 transition">Watch Ad</button>
                        </div>
                        <div class="bg-slate-900 rounded-xl p-4 gradient-border text-center shadow-lg">
                            <p class="font-bold text-sm text-slate-200">Ad Server 2</p>
                            <p class="text-[11px] text-green-400 font-semibold mt-1 mb-3">+💎<span id="r_ad2">60</span> Coins</p>
                            <button onclick="showAdAndReward(2)" class="w-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-extrabold py-2 rounded-lg text-xs shadow-md shadow-blue-500/10 active:scale-95 transition">Watch Ad</button>
                        </div>
                    </div>
                </div>

                <!-- Web Links Section -->
                <div>
                    <h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-link text-orange-500"></i> Premium Link Tasks
                    </h3>
                    <div class="bg-slate-900 rounded-xl p-4 gradient-border shadow-lg">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="font-bold text-sm text-slate-200">Premium High-CPM Link</p>
                                <p class="text-xs text-green-400 font-semibold mt-0.5">+💎<span id="r_link">40</span> Coins</p>
                            </div>
                            <button id="link_btn" onclick="startLinkTask()" class="bg-gradient-to-r from-orange-500 to-amber-600 text-white font-bold px-4 py-2 rounded-lg text-xs shadow-md shadow-orange-500/10 active:scale-95 transition">Visit Link</button>
                        </div>
                        <div id="timer_container" class="hidden mt-3 text-center text-xs text-slate-400 bg-slate-950/80 p-2.5 rounded-lg border border-orange-500/20">
                            <i class="fa-solid fa-hourglass-half animate-spin text-orange-400 mr-1"></i> Don't Close Page: <span id="countdown" class="text-orange-400 font-bold">20</span>s left...
                        </div>
                    </div>
                </div>

                <!-- Telegram Social Tasks Section -->
                <div>
                    <h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                        <i class="fa-brands fa-telegram text-sky-400"></i> Official Social Channels
                    </h3>
                    <div class="bg-slate-900 rounded-xl p-1 gradient-border shadow-lg divide-y divide-slate-800">
                        <!-- Channel Task -->
                        <div class="flex justify-between items-center p-3.5">
                            <div class="flex items-center gap-3">
                                <div class="w-8 h-8 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center"><i class="fa-solid fa-bullhorn text-sm"></i></div>
                                <div>
                                    <p class="font-bold text-xs text-slate-200">Join Official Channel</p>
                                    <p class="text-[10px] text-green-400 font-medium">+💎<span id="r_tg">50</span> Coins</p>
                                </div>
                            </div>
                            <button id="tg_btn" onclick="joinTelegram()" class="bg-sky-500 text-white font-bold px-4 py-1.5 rounded-lg text-xs active:scale-95 transition">Join</button>
                        </div>
                        <!-- Group Task -->
