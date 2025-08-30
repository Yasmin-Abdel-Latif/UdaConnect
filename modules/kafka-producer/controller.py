from flask import Blueprint, request, jsonify
from producer import publish_to_kafka
from flask import Flask
app = Flask(__name__)
bp = Blueprint('kafka_producer', __name__)

@bp.route('/produce/location', methods=['POST'])
def produce_location():
    data = request.get_json()
    try:
        publish_to_kafka('locations', data)
        return jsonify({'status': 'Message published'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="0.0.0.0", port=5000)