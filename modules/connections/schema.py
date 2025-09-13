from pydantic import BaseModel
from datetime import datetime

class ConnectionCreate(BaseModel):
    person_id: int
    location_id: int

class ConnectionRead(BaseModel):
    id: int
    person_id: int
    location_id: int
    creation_time: datetime

    class Config:
        from_attributes = True