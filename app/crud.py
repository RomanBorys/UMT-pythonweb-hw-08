from . import models
from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import schemas

# CREATE
def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# READ ALL + SEARCH
def get_contacts(db: Session, search: str = None):
    query = db.query(models.Contact)

    if search:
        query = query.filter(
            (models.Contact.first_name.contains(search)) |
            (models.Contact.last_name.contains(search)) |
            (models.Contact.email.contains(search))
        )

    return query.all()


# READ ONE
def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


# UPDATE
def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None

    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


# DELETE
def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None

    db.delete(db_contact)
    db.commit()
    return db_contact


# BIRTHDAYS (7 days)
def get_upcoming_birthdays(db: Session):
    today = date.today()
    in_7_days = today + timedelta(days=7)

    contacts = db.query(models.Contact).all()

    result = []
    for c in contacts:
        bday_this_year = c.birthday.replace(year=today.year)

        if today <= bday_this_year <= in_7_days:
            result.append(c)

    return result