from email.policy import default
from glob import glob
import os, json, argparse, threading, time
from flask import Flask, request, jsonify
from Publisher import Publisher
from Subscriber import Subscriber

app = Flask(__name__)
fall_warning = False
warning_timer = time.time()
warning_period = 5
lumos_timer = [time.time() for i in range(8)]
lumos_period = 5
lumos_range = 2

payload = [{
        'id':i,
        'brightness':128,
        'color':'w',
        'flash': False
    } for i in range(8)]

default_light = {
        'brightness':128,
        'color':'w',
        'flash': False
    }

def lumos(index, brightness=255):
    global payload, lumos_range, lumos_timer
    for i in range( max(0, index - lumos_range), min(8, index + lumos_range) ):
        payload[i]['brightness'] = brightness
        lumos_timer = time.time()

def update(publisher, lock):
    global payload, lumos_timer, lumos_period, default_light, fall_warning, warning_period, warning_timer
    if fall_warning:
        if time.time() - warning_timer > warning_period:
            fall_warning = False
            for i in range(8):
                lock.acquire()
                payload[i]['brightness'] = default_light['brightness']
                payload[i]['color'] = default_light['color']
                payload[i]['flash'] = default_light['flash']
                lock.release()
    else:
        for i in range(8):
            if time.time() - lumos_timer[i] > lumos_period:
                lock.acquire()
                payload[i]['brightness'] = default_light['brightness']
                lock.release()
    publisher.publish('lights', payload)
    time.sleep(0.1)

@app.route("/api/allStreetlights", methods=['GET'])
def home():
    with open("config.json", 'r') as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/fall", methods=['POST'])
def fall():
    global fall_warning, payload, warning_timer
    received_data = request.form
    # received_data = {
    #     "from": 2,
    #     "probability": 0.1
    # }
    if received_data.get('probability') > 0.2:
        fall_warning = True
        warning_timer = time.time()
        for i in range(8):
            payload[i]['brightness'] = 255
            payload[i]['color'] = 'r'
            payload[i]['flash'] = True

    # return jsonify(received_data)

@app.route("/api/obj_passed", methods=['POST'])
def obj_passed():
    received_data = request.form
    lumos(received_data.get('from'))

    # return jsonify(received_data)

@app.route("/api/allSensors", methods=['GET'])
def sensor():
    return subscriber.data

# Serve React App
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(app.static_folder + '/' + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = parser.parse_args()
    publisher = Publisher(args)
    subscriber = Subscriber(args)

    lock = threading.Lock()

    t_subscriber = threading.Thread(target = subscriber.main)
    t_subscriber.start()

    t_update = threading.Thread(target = update, args=(lock,))
    t_update.start()

    t_subscriber.join()
    t_update.join()

    


