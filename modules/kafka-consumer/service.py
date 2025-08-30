from models import KafkaEvent
from database import SessionLocal

def save_kafka_event(payload):
    db = SessionLocal()
    event = KafkaEvent(payload=str(payload))
    db.add(event)
    db.commit()
    db.close()
