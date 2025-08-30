from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class KafkaEvent(Base):
    __tablename__ = "kafka_events"

    id = Column(Integer, primary_key=True)
    payload = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
