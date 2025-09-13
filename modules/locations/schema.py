from pydantic import BaseModel

class LocationCreate(BaseModel):
    person_id: int
    latitude: float
    longitude: float

class LocationRead(LocationCreate):
    id: int

    class Config:
        from_attributes = True
