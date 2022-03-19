import os, json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/allStreetlights", methods=['GET'])
def home():
    with open("config.json", 'r') as f:
        data = json.load(f)

    return jsonify(data)


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

