from flask import Flask, render_template, url_for, redirect, jsonify, json, request, session
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html', status=session['status'])

@app.route('/status', methods=['POST'])
def status_post():
    postJson = request.get_json()
    status = "online"
    if postJson:
        status = postJson['status']
        session['status'] = status
    return jsonify(status)

if __name__ == '__main__':
    app.run(host='192.168.10.6')