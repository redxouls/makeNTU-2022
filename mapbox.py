import os, threading
from flask import Flask, render_template, request, jsonify, send_from_directory

from sensors.Subscriber import Subscriber

app = Flask(__name__, static_folder="build", template_folder="build")


subscriber = Subscriber()

t = threading.Thread(target=subscriber.main)
t.start()

app_data = {}

@app.route("/api/navigate", methods=['POST'])
def navigate():
    global app_data

    request_data = request.json
    if "start" in request_data:
        app_data["start"] = request_data["start"]
    if "end" in request_data:
        app_data["end"] = request_data["end"]
    print(app_data)
    return jsonify(request_data)


@app.route("/api/current/<mode>", methods=['GET'])
def current(mode):
    global subscriber

    if mode == "location":
        current_location = {
            "coordinates": subscriber.data["gps"],
        }
        return jsonify(current_location)
    elif mode == "bearing":
        bearing = {
            "bearing": subscriber.data["compass"]["bearing"],
        }

        return jsonify(bearing)
    # coord = get_coord()
    # coord = [121.54373533333333, 25.019046666666668]

    # current_location = {
    #     "coordinates": [coord[0]+ random.random()/(10e4), coord[1]+ random.random()/(10e4)]
    # }

@app.route("/api/data", methods=['GET'])
def data():
    global app_data
    return jsonify(app_data)

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
