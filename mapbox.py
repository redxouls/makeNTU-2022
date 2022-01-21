import os, threading
from flask import Flask, render_template, request, jsonify, send_from_directory

from sensors.Subscriber import Subscriber
from controller.Navigator import Navigator

from sensors.Publisher import Publisher

app = Flask(__name__, static_folder="build", template_folder="build")


publisher = Publisher()
t_publisher = threading.Thread(target=publisher.main)
t_publisher.start()

subscriber = Subscriber()
stm_serial = Publisher.get_stm_serial()
navigator =  Navigator(subscriber=subscriber, serial_port=stm_serial)

t_subscriber = threading.Thread(target=subscriber.main)
t_subscriber.start()

@app.route("/api/navigate", methods=['POST'])
def navigate_post():
    global navigator

    request_data = request.json
    if "start" in request_data:
        navigator.setOrigin(request_data["start"])
    if "end" in request_data:
        navigator.setDestination(request_data["end"])
    
    return jsonify(request_data)

@app.route("/api/navigate/<mode>", methods=['GET'])
def navigate_get(mode):
    global navigator
    
    if mode == "start":
        t = threading.Thread(target=navigator.navigate)
        t.start()
        
    elif mode == "stop":
        navigator.stop()
    
    return jsonify({"status": 200})

@app.route("/api/current/<mode>", methods=['GET'])
def current(mode):
    global subscriber

    data = {}
    if mode == "location":
        data = {
            "coordinates": subscriber.data.get("gps", [121.543764, 25.019388])
        }
    elif mode == "bearing":
        data = {
            "bearing": subscriber.data.get("compass").get("azimuth", 0),
        }
    return jsonify(data)

@app.route("/api/records/<mode>", methods=['GET'])
def record_get(mode):
    if mode == "0":
        # data = {"status": 200}
        # return send_from_directory('./camera/test.flv')
        return send_from_directory('./camera', 'test.html')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, threaded=True)
# app.run(host="127.0.0.1", port=3000)
