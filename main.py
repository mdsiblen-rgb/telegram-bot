from flask import Flask, render_template, request, jsonify
import json, os
app = Flask(__name__)
DB="db.json"
def load(): return json.load(open(DB,"r",encoding="utf-8")) if os.path.exists(DB) else {}
def save(d): json.dump(d,open(DB,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

@app.route("/")
def home():
    uid = request.args.get("start") or request.args.get("user_id") or "8807178385"
    db=load()
    if uid not in db:
        db[uid]={"balance":715,"ads":0,"today":0,"refs":0,"total":37}; save(db)
    u=db[uid]
    return render_template("index.html",uid=uid,b=u["balance"],ads=u["ads"],today=u["today"],refs=u["refs"],total=u["total"])

@app.route("/api/watch_ad",methods=["POST"])
def ad():
    uid=request.args.get("user_id") or request.args.get("start")
    db=load(); u=db[uid]
    if u["ads"]>=15: return jsonify(error="শেষ")
    u["balance"]+=15; u["ads"]+=1; u["today"]+=15; u["total"]+=1; save(db); return jsonify(ok=True)

@app.route("/api/withdraw",methods=["POST"])
def wd():
    d=request.json; db=load(); u=db[d["user_id"]]
    u["balance"]-=int(d["amount"]); save(db); return jsonify(ok=True)

@app.route("/reset_all")
def reset(): save({}); return "DONE"
if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
