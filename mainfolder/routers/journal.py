from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router =APIRouter(
    prefix='/journal',
    tags=["journal"],
)

@router.get('', status_code=status.HTTP_200_OK, response_model=List[schemas.Journal])
def all_journals(db: Session=Depends(get_db)):
    journals=db.query(models.Journal).all()
    return journals

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Journal)
def show_individual_journal(id, db:Session=Depends(get_db)):
    journal=db.query(models.Journal).filter(models.Journal.id == id).first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return journal

@router.get('/user/{id}', response_model=schemas.ShowUserJournal)
def show_user_journal(id, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return user

@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_journal(request: schemas.Journal, db: Session=Depends(get_db)):
    journal_entry=models.Journal(
        title=request.title,
        body=request.body,
        user_id=1#id
        )
    db.add(journal_entry)
    db.commit()
    db.refresh(journal_entry)
    return request

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_entry(id, request:schemas.Journal, db:Session=Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.update(request.dict())
    db.commit()
    return 'Journal has been updated as requested'

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_journal(id, db:Session=Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.delete(synchronize_session=False)    
    db.commit()
    return 'journal entry has been removed'