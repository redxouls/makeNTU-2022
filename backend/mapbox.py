import os, json, argparse, threading
from flask import Flask, request, jsonify
from Publisher import Publisher
from Subscriber import Subscriber

app = Flask(__name__)

fall = {}

@app.route("/api/allStreetlights", methods=['GET'])
def home():
    with open("config.json", 'r') as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/api/fall", methods=['POST'])
def fall():
    global fall
    # received_data = request.form
    received_data = {
        "from": 2,
        "probability": 0.1
    }

    print(received_data)
    publisher.publish('fall', received_data)
    
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
    publisher = Publisher(args)
    subscriber = Subscriber(args)

    t_subscriber = threading.Thread(target = subscriber.main)
    t_subscriber.start()

