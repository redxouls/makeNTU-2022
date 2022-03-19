from email.policy import default
from glob import glob
import os, json, argparse, threading, time
from flask import Flask, request, jsonify
from Publisher import Publisher
from Subscriber import Subscriber

app = Flask(__name__)

class Light_controller:
    def __init__(self, num_lights=8) -> None:
        self.num_lights = num_lights
        self.fall_warning = False
        self.warning_timer = time.time()
        self.warning_period = 5
        self.lumos_timer = [time.time() for i in range(8)]
        self.lumos_period = 5
        self.lumos_range = 2
        self.payload = [{
                            'id':i,
                            'brightness':128,
                            'color':'w',
                            'flash': False
                        } for i in range(self.num_lights)]
        self.default_light = {
                            'brightness':128,
                            'color':'w',
                            'flash': False
                        }
    def lumos(self, index, brightness=255):
        for i in range( max(0, index - self.lumos_range), min(self.num_lights, index + self.lumos_range) ):
            self.payload[i]['brightness'] = brightness
            self.lumos_timer[i] = time.time()
    def fall(self, prob):
        if prob > 0.2:
            print("[Fall detected!]")
            self.fall_warning = True
            self.warning_timer = time.time()
            for i in range(self.num_lights):
                self.payload[i]['brightness'] = 255
                self.payload[i]['color'] = 'r'
                self.payload[i]['flash'] = True
    
    def update(self, publisher, lock):
        # print("updating")
        if self.fall_warning:
            if time.time() - self.warning_timer > self.warning_period:
                self.fall_warning = False
                print("Fall alarm stopped")
                for i in range(self.num_lights):
                    lock.acquire()
                    self.payload[i]['brightness'] = self.default_light['brightness']
                    self.payload[i]['color'] = self.default_light['color']
                    self.payload[i]['flash'] = self.default_light['flash']
                    lock.release()
        else:
            for i in range(self.num_lights):
                if time.time() - self.lumos_timer[i] > self.lumos_period:
                    lock.acquire()
                    self.payload[i]['brightness'] = self.default_light['brightness']
                    lock.release()
        publisher.publish('lights', self.payload)
        time.sleep(0.1)

light_controller = Light_controller(8)

@app.route("/api/allStreetlights", methods=['GET'])
def home():
    with open("config.json", 'r') as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/fall", methods=['POST'])
def fall():
    received_data = request.form
    # received_data = {
    #     "from": 2,
    #     "probability": 0.1
    # }
    prob = float(received_data.get('probability')) 
    light_controller.fall(prob)
    return jsonify(received_data)

@app.route("/api/obj_passed", methods=['POST'])
def obj_passed():
    received_data = request.form
    index = int(received_data.get('from'))
    print("[Lamp ", index, " triggered]")
    light_controller.lumos(index)

    return jsonify(received_data)

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
    print("Create publisher and subscriber")
    publisher = Publisher(args)
    subscriber = Subscriber(args)

    lock = threading.Lock()

    t_subscriber = threading.Thread(target = subscriber.main)
    t_subscriber.start()

    t_update = threading.Thread(target = light_controller.update, args=(lock,))
    t_update.start()

    t_subscriber.join()
    t_update.join()

    


