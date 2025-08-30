import grpc
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, request, jsonify

from modules.connections import location_connection_pb2
from modules.connections import location_connection_pb2_grpc

app = Flask(__name__)

@app.route("/persons", methods=["GET", "POST"])
def proxy_persons():
    if request.method == "GET":
        resp = requests.get("http://persons:5000/persons")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "POST":
        resp = requests.post("http://persons:5000/persons", json=request.get_json())
        return jsonify(resp.json()), resp.status_code

@app.route("/locations", methods=["GET", "POST"])
def proxy_locations():
    if request.method == "GET":
        resp = requests.get("http://locations:5001/locations")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "POST":
        resp = requests.post("http://locations:5001/locations", json=request.get_json())
        return jsonify(resp.json()), resp.status_code

@app.route("/connections", methods=["GET", "POST"])
def proxy_connections():
    if request.method == "GET":
        resp = requests.get("http://connections:5003/connections")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "POST":
        resp = requests.post("http://connections:5003/connections", json=request.get_json())
        return jsonify(resp.json()), resp.status_code

@app.route("/locations/proximity", methods=["POST"])
def proximity_query():
    payload = request.get_json()
    channel = grpc.insecure_channel("connections:50051")
    stub = location_connection_pb2_grpc.LocationServiceStub(channel)
    grpc_request = location_connection_pb2.LocationRequest(
        person_id=payload["person_id"],
        distance=payload["meters"]
    )
    response = stub.CheckNearby(grpc_request)
    return jsonify([{
        "person_id": r.person_id,
        "latitude": r.latitude,
        "longitude": r.longitude,
        "distance": r.distance
    } for r in response.nearby_persons])
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)