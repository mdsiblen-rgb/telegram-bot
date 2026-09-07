from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1 style='text-align:center; margin-top:100px;'>💎 Protodin Kaj Live!</h1>
    <p style='text-align:center;'>Bot is Working</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
