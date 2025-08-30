from sqlalchemy.orm import Session
import models, schema

def create_connection(db: Session, connection: schema.ConnectionCreate):
    db_connection = models.Connection(**connection.dict())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

def get_all_connections(db: Session):
    return db.query(models.Connection).all()