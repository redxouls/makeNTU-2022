import os, random
from flask import Flask, render_template, request, jsonify, send_from_directory
# from GPS import get_coord

app = Flask(__name__, static_folder="build", template_folder="build")

app_data = {}

# @app.route("/")
# def home():
#     return render_template("navigation.html")

@app.route("/api/navigate", methods=['POST'])
def navigate():
    global app_data
    app_data = request.json
    request_data = request.json
    
    if "start" in request_data:
        app_data["start"] = request_data["start"]
    elif "end" in request_data:
        app_data["end"] = request_data["end"]
    
    return jsonify(request_data)


@app.route("/api/current", methods=['GET'])
def current():
    # coord = get_coord()
    coord = [121.54373533333333, 25.019046666666668]
    
    # current_location = {
    #     "coordinates": coord,
    # }

    current_location = {
        "coordinates": [coord[0]+ random.random()/(10e4), coord[1]+ random.random()/(10e4)]
    }

    return jsonify(current_location)

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
