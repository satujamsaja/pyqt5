from flask import render_template
from flask import request
from flask import jsonify
from app import app
import random
from datetime import datetime

# Homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Homepage")

# API Environtment.
@app.route('/api/sense', methods = ['GET'])
def api_sense():
    data = {
        'temperature': random.randint(20, 50),
        'humidity': random.randint(1, 100),
        'pressure': random.randint(10000, 11000),
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if data:
        return jsonify(data)
    else:
        return not_found()



# 404 handle.
@app.errorhandler(404)
def not_found(error=None):
    resp = jsonify({
        'status' : 404,
        'message': 'Page not found.'
    })
    resp.status_code = 404
    return resp
