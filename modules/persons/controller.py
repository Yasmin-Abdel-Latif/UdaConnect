from flask import Blueprint, request, jsonify
from database import get_db
from models import Person
from database import Base, engine
import service, schema
from flask import Flask
app = Flask(__name__)
Base.metadata.create_all(bind=engine)
bp = Blueprint('persons', __name__, url_prefix='/persons')

@bp.route('', methods=['GET'])
def list_persons():
    db = next(get_db())
    persons = service.get_all_persons(db)
    return jsonify([{"id": p.id, "name": p.name, "company": p.company} for p in persons])

@bp.route('', methods=['POST'])
def create_person():
    db = next(get_db())
    data = request.json
    person_in = schema.PersonCreate(**data)
    person = service.create_person(db, person_in)
    return jsonify({"id": person.id, "name": person.name, "company": person.company})
if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="0.0.0.0", port=5000)
