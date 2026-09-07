from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime
app = Flask(__name__)
DB = "db.json"
def load_db():
    if not os.path.exists(DB): return {}
    with open(DB,"r",encoding="utf-8") as f: return json.load(f)
def save_db(d):
    with open(DB,"w",encoding="utf-8") as f: json.dump(d,f,indent=2,ensure_ascii=False)

@app.route("/")
def home():
    uid=request.args.get("user_id","108365"); db=load_db()
    if uid not in db:
        db[uid]={"balance":50,"diamond":0,"ads":0,"today":0,"yesterday":0,"refs":0,"withdraws":[]}
        save_db(db)
    u=db[uid]
    return render_template("index.html",user_id=uid,balance=u["balance"],ads_watched=u["ads"],today=u["today"],yesterday=u["yesterday"],refs=u["refs"])

@app.route("/reset_all")
def reset_all(): save_db({}); return "DONE"

@app.route("/api/watch_ad",methods=["POST"])
def watch_ad():
    uid=request.args.get("user_id"); db=load_db(); u=db[uid]
    if u["ads"]>=25: return jsonify({"error":"আজকের 25 টা শেষ"})
    u["balance"]+=5; u["ads"]+=1; u["today"]+=5; save_db(db); return jsonify({"ok":True})

@app.route("/api/withdraw",methods=["POST"])
def wd():
    d=request.json; db=load_db(); u=db[d["user_id"]]
    if u["balance"]<1000: return jsonify({"error":"Min 1000"})
    u["withdraws"].append({"number":d["number"],"amount":d["amount"],"method":d["method"],"time":datetime.now().strftime("%d/%m %H:%M")}); u["balance"]-=d["amount"]; save_db(db); return jsonify({"ok":True})

@app.route("/admin")
def admin():
    db=load_db(); w=[]
    for uid,u in db.items():
        for x in u.get("withdraws",[]): w.append({**x,"user":uid})
    return render_template("admin.html",withdraws=w[::-1])

if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
