from email.policy import default
from glob import glob
import os, json, argparse, threading, time
from flask import Flask, request, jsonify
from Publisher import Publisher
from Subscriber import Subscriber
from LightController import LightController
app = Flask(__name__)


@app.route("/api/allStreetlights", methods=['GET'])
def allStreetlights():
    with open("config.json", 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route("/api/brightness", methods=['POST'])
def brightness():
    received_data = request.json
    index = received_data.get('to', 255)
    brightness  = received_data.get('brightness', 255)
    light_controller.change_brightness(index, brightness)
    
    return jsonify(request.json)


@app.route("/api/fall", methods=['POST'])
def fall():
    received_data = request.json
    prob = float(received_data.get('probability')) 
    index = received_data.get('from')
    light_controller.fall(index, prob)
    return jsonify(received_data)

@app.route("/api/obj_passed", methods=['POST'])
def obj_passed():
    received_data = request.json
    index = int(received_data.get('from'))
    print("[Lamp ", index, " triggered]")
    light_controller.lumos(index)

    return jsonify(received_data)

@app.route("/api/allSensors", methods=['GET'])
def allSensors():
    return jsonify(subscriber.data)

@app.route("/api/sensor/<index>", methods=['GET'])
def sensor(index):
    return jsonify(subscriber.data.get(int(index), []))


@app.route("/api/fall_alarm", methods=['GET'])
def fall_alarm():
    return jsonify(light_controller.getStatus())
# Serve React App
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve(path):
#     if path != "" and os.path.exists(app.static_folder + '/' + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return render_template('index.html')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    print("Create publisher and subscriber")
    
    publisher = Publisher(args)
    subscriber = Subscriber(args)
    light_controller = LightController(8)

    t_subscriber = threading.Thread(target = subscriber.main)
    t_subscriber.start()

    t_update = threading.Thread(target = light_controller.update, args=(publisher, subscriber))
    t_update.start()


    app.run(host="0.0.0.0", port=6000, debug=True)

    t_subscriber.join()
    t_update.join()

    # python3 main.py --index 0  --source_url "http://b78c-2001-b400-e434-2f7e-c1f3-f180-3909-71cb.ngrok.io/video/playlist.m3u8" --target_url "http://b78c-2001-b400-e434-2f7e-c1f3-f180-3909-71cb.ngrok.io/api/fall"


