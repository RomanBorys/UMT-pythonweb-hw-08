from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud
from . import models
from . import schemas
from .database import engine
from .dependencies import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/contacts", response_model=schemas.ContactResponse)
def create(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@app.get("/contacts", response_model=list[schemas.ContactResponse])
def read_contacts(search: str = None, db: Session = Depends(get_db)):
    return crud.get_contacts(db, search)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def read_one(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(404, "Not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated = crud.update_contact(db, contact_id, contact)
    if not updated:
        raise HTTPException(404, "Not found")
    return updated


@app.delete("/contacts/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(404, "Not found")
    return {"message": "deleted"}


@app.get("/contacts/birthdays/upcoming", response_model=list[schemas.ContactResponse])
def birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)