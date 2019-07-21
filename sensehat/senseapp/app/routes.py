from flask import render_template
from flask import request
from flask import jsonify
from app import app
import random
import os
from datetime import datetime
from sense_hat import SenseHat

# Homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Homepage")

# API Environtment.
@app.route('/api/sense', methods = ['GET'])
def api_sense():
    sense = SenseHat()
    sense.clear()
    # Get CPU Temp.
    cpu_temp = os.popen('vcgencmd measure_temp').readline()
    temp = float(cpu_temp.replace("temp=","").replace("'C\n",""))
    t = sense.get_temperature()
    data = {
        'temperature': t - ((temp-t)/1.5),
        'humidity': sense.get_humidity(),
        'pressure': sense.get_pressure(),
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
