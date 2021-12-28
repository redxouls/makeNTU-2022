from flask import Flask, render_template, request, jsonify
from GPS import get_coord

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("navigation.html")

@app.route("/api/navigate", methods=['POST'])
def navigate():
    request_data = request.json
    return jsonify(request_data)


@app.route("/api/current", methods=['GET'])
def current():
    coord = get_coord()
    current_location = {
        "coordinates": coord
    }
    return jsonify(current_location)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
# app.run(host="127.0.0.1", port=3000)
