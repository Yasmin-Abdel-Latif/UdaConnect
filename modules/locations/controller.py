from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
import service, schema
from models import Base
from database import engine, get_db
from flask import Flask
app = Flask(__name__)
Base.metadata.create_all(bind=engine)
bp = Blueprint("locations", __name__, url_prefix="/locations")

@bp.route("", methods=["POST"])
def create_location():
    db: Session = next(get_db())
    location_data = schema.LocationCreate(**request.json)
    location = service.create_location(db, location_data)
    return jsonify(schema.LocationRead.from_orm(location).dict())

@bp.route("", methods=["GET"])
def list_locations():
    db: Session = next(get_db())
    locations = service.get_all_locations(db)
    return jsonify([schema.LocationRead.from_orm(loc).dict() for loc in locations])
if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="0.0.0.0", port=5001)