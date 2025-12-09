from flask import Blueprint, request, jsonify, Flask
from database import get_db
from models import Person
from database import Base, engine
import service, schema
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
Base.metadata.create_all(bind=engine)
bp = Blueprint('persons', __name__, url_prefix='/persons')


@bp.route('', methods=['GET'])
def list_persons():
        """
        List Persons
        ---
        tags:
            - persons
        responses:
            200:
                description: A list of persons
                schema:
                    type: array
                    items:
                        type: object
        """
        db = next(get_db())
        persons = service.get_all_persons(db)
        return jsonify([{"id": p.id, "name": p.name, "company": p.company} for p in persons])


@bp.route('', methods=['POST'])
def create_person():
        """
        Create Person
        ---
        tags:
            - persons
        parameters:
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    properties:
                        name:
                            type: string
                        company:
                            type: string
        responses:
            201:
                description: Created person
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                        name:
                            type: string
                        company:
                            type: string
        """
        db = next(get_db())
        data = request.json
        person_in = schema.PersonCreate(**data)
        person = service.create_person(db, person_in)
        return jsonify({"id": person.id, "name": person.name, "company": person.company})


if __name__ == "__main__":
        app.register_blueprint(bp)
        app.run(host="0.0.0.0", port=5000)
