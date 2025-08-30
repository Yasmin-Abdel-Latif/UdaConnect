from flask import Blueprint
from flask import Flask
app = Flask(__name__)
bp = Blueprint("kafka_consumer", __name__)

@bp.route("/healthz", methods=["GET"])
def health_check():
    return {"status": "kafka-consumer healthy"}, 200
if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="0.0.0.0", port=5000)