from sqlalchemy import Column, Integer, Float, DateTime
from database import Base
from datetime import datetime

class Connection(Base):
    __tablename__ = "connections"
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, nullable=False)
    location_id = Column(Integer, nullable=False)
    creation_time = Column(DateTime, default=datetime.utcnow)