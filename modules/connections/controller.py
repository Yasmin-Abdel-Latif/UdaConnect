from flask import Flask
from flask import Blueprint, request, jsonify
from database import get_db
from models import Connection
from database import Base, engine
import service, schema
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app)
Base.metadata.create_all(bind=engine)
connection_blueprint = Blueprint("connection", __name__)

@connection_blueprint.route("/connections", methods=["POST"])
def create_connection():
    db = next(get_db())
    data = request.json
    new_conn = schema.ConnectionCreate(**data)
    result = service.create_connection(db, new_conn)
    return jsonify({"id": result.id})

@connection_blueprint.route("/connections", methods=["GET"])
def get_connections():
    db = next(get_db())
    results = service.get_all_connections(db)
    return jsonify([{"id": c.id, "person_id": c.person_id, "location_id": c.location_id, "creation_time": c.creation_time.isoformat()} for c in results])
if __name__ == "__main__":
    app.register_blueprint(connection_blueprint)
    app.run(host="0.0.0.0", port=5003)