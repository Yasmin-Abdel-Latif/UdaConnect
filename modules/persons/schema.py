from pydantic import BaseModel

class PersonCreate(BaseModel):
    name: str
    company: str

class PersonRead(PersonCreate):
    id: int

    class Config:
        orm_mode = True
