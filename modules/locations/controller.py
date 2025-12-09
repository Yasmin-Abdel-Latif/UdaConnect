from flask import Flask
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
import service, schema
from models import Base
from database import engine, get_db
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app)
Base.metadata.create_all(bind=engine)
bp = Blueprint("locations", __name__, url_prefix="/locations")

@bp.route("", methods=["POST"])
def create_location():
        """
        Create Location
        ---
        tags:
            - locations
        parameters:
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    properties:
                        person_id:
                            type: integer
                        latitude:
                            type: number
                        longitude:
                            type: number
        responses:
            201:
                description: Created location
                schema:
                    type: object
        """
        db: Session = next(get_db())
        location_data = schema.LocationCreate(**request.json)
        location = service.create_location(db, location_data)
        return jsonify(schema.LocationRead.from_orm(location).dict())

@bp.route("", methods=["GET"])
def list_locations():
        """
        List Locations
        ---
        tags:
            - locations
        responses:
            200:
                description: List of locations
                schema:
                    type: array
                    items:
                        type: object
        """
        db: Session = next(get_db())
        locations = service.get_all_locations(db)
        return jsonify([schema.LocationRead.from_orm(loc).dict() for loc in locations])
if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="0.0.0.0", port=5001)