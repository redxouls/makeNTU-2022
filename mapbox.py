import requests
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("navigation.html")

@app.route("/api", methods=['POST'])
def api():
    print(request.json)
    return jsonify(request.json)
# app.run()

# app.run(host="0.0.0.0", port=3000)
app.run(host="127.0.0.1", port=3000)


# response = requests.get('https://api.mapbox.com/directions/v5/mapbox/cycling/121.542678%2C25.015552%3B121.535821%2C25.019733?alternatives=false&continue_straight=true&geometries=geojson&language=en&overview=simplified&steps=true&access_token=pk.eyJ1IjoicmVkeG91bHMiLCJhIjoiY2t4N2R1Nm1uMHl4aTJwcXViYno1Ym9sNCJ9.fByzZrach_1gQlboB02hCg')
# query_raw = response.json()
# routes = query_raw["routes"][0]["legs"][0]["steps"]
# html_route = []
# for i, route in enumerate(routes):
#     route_str = "%s: %s" % (route["maneuver"].get("modifier"), route["maneuver"].get("instruction"))
#     html_route.append(route_str)
# # return json.dumps(html_route)