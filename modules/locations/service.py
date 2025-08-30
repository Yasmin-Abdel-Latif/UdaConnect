from models import Location
from sqlalchemy.orm import Session

def create_location(db: Session, location_data):
    location = Location(**location_data.dict())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

def get_all_locations(db: Session):
    return db.query(Location).all()
