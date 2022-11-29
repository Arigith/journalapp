from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas

def get_all(db:Session):
    journals=db.query(models.Journal).all()
    return journals

def get_by_id(id:int, db:Session):
    journal=db.query(models.Journal).filter(models.Journal.id == id).first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return journal

def get_by_user(id:int, db:Session):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return user

def create(request: schemas.Journal, db:Session):
    journal_entry=models.Journal(
        title=request.title,
        body=request.body,
        user_id=1#id
        )
    db.add(journal_entry)
    db.commit()
    db.refresh(journal_entry)
    return request

def update(id:int, request:schemas.Journal, db:Session):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.update(request.dict())
    db.commit()
    return 'Journal has been updated as requested'

def delete(id:int, db:Session):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.delete(synchronize_session=False)    
    db.commit()
    return 'journal entry has been removed'