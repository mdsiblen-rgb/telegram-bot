from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# ডাটাবেস - রিয়েল ইউজার এখানে জমা হবে
users_db = []
# তোমার নিজের ডাটা
MY_BALANCE = 715
MY_DIAMOND = 6
MY_ID = "user_1788812920707"

@app.route('/')
def home():
    total_users = len(users_db)
    # কেউ জয়েন না করলে 0 দেখাবে, ফেক 1284 দেখাবে না
    return render_template('index.html', 
        balance=MY_BALANCE,
        diamond=MY_DIAMOND,
        user_id=MY_ID,
        total_refer=total_users,
        users=users_db
    )

@app.route('/admin')
def admin():
    # ?pass=653598 দিয়ে ঢুকলে এডমিন দেখবে
    return render_template('admin.html', users=users_db, total_balance=MY_BALANCE)

@app.route('/api/join', methods=['POST'])
def join_user():
    data = request.json
    new_user = {
        "id": data.get("user_id", "user_"+str(len(users_db)+1)),
        "join_time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "referred_by": data.get("referred_by", "Direct"),
        "status": "সক্রিয়"
    }
    users_db.append(new_user)
    return jsonify({"success": True, "users": users_db})

@app.route('/api/watch_ad', methods=['POST'])
def watch_ad():
    global MY_BALANCE
    MY_BALANCE += 18
    return jsonify({"new_balance": MY_BALANCE})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
