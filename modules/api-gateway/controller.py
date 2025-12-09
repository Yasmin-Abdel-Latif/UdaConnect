import grpc
import requests
from flask import Flask, request, jsonify
from flasgger import Swagger
import json
import logging

from modules.connections import location_connection_pb2
from modules.connections import location_connection_pb2_grpc
from openapi_aggregator import get_aggregated_spec

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/persons", methods=["GET", "POST"])
def proxy_persons():
    """
    Proxy Persons API
    ---
    tags:
      - api-gateway
    responses:
      200:
        description: Proxy to persons service
    """
    if request.method == "GET":
        resp = requests.get("http://persons:5000/persons")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "POST":
        resp = requests.post("http://persons:5000/persons", json=request.get_json())
        return jsonify(resp.json()), resp.status_code

@app.route("/locations", methods=["GET", "POST"])
def proxy_locations():
    """
    Proxy Locations API
    ---
    tags:
      - api-gateway
    responses:
      200:
        description: Proxy to locations service
    """
    if request.method == "GET":
        resp = requests.get("http://locations:5001/locations")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "POST":
        resp = requests.post("http://locations:5001/locations", json=request.get_json())
        return jsonify(resp.json()), resp.status_code

@app.route("/connections", methods=["GET", "POST"])
def proxy_connections():
    """
    Proxy Connections API
    ---
    tags:
      - api-gateway
    responses:
      200:
        description: Proxy to connections service
    """
    if request.method == "GET":
        resp = requests.get("http://connections:5003/connections")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "POST":
        resp = requests.post("http://connections:5003/connections", json=request.get_json())
        return jsonify(resp.json()), resp.status_code

@app.route("/locations/proximity", methods=["POST"])
def proximity_query():
    """
    Proximity Query (gRPC)
    ---
    tags:
      - api-gateway
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            person_id:
              type: integer
            meters:
              type: integer
    responses:
      200:
        description: List of nearby persons
        schema:
          type: array
          items:
            type: object
    """
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


@app.route("/openapi.json", methods=["GET"])
def get_openapi_spec():
    """
    Get aggregated OpenAPI specification
    ---
    tags:
      - gateway
    responses:
      200:
        description: Aggregated OpenAPI specification in JSON format
        content:
          application/json:
            schema:
              type: object
    """
    logger.info("Fetching aggregated OpenAPI spec")
    try:
        spec = get_aggregated_spec()
        logger.info(f"Successfully retrieved spec with {len(spec.get('paths', {}))} paths")
        return jsonify(spec)
    except Exception as e:
        logger.error(f"Error fetching spec: {e}", exc_info=True)
        return {"error": str(e)}, 500


@app.route("/swagger-ui", methods=["GET"])
def swagger_ui():
    """
    Swagger UI for aggregated API
    ---
    tags:
      - gateway
    responses:
      200:
        description: Interactive API documentation (Swagger UI)
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>UdaConnect API Gateway - Swagger UI</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.css">
        <style>
            html {
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }
            *, *:before, *:after {
                box-sizing: inherit;
            }
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/openapi.json",
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "StandaloneLayout"
                });
                window.ui = ui;
            };
        </script>
    </body>
    </html>
    """
    return html_content, 200, {"Content-Type": "text/html; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)