@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return "OK"
