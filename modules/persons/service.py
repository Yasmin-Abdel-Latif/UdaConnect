from sqlalchemy.orm import Session
import models, schema

def create_person(db: Session, person: schema.PersonCreate):
    db_person = models.Person(name=person.name, company=person.company)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_all_persons(db: Session):
    return db.query(models.Person).all()
