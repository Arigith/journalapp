from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import schemas, oauth2
from repository import journal

router =APIRouter(
    prefix='/journal',
    tags=["journal"],
)

@router.get('', status_code=status.HTTP_200_OK, response_model=List[schemas.Journal])
def all_journals(db: Session=Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return journal.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Journal)
def show_individual_journal(id, db:Session=Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return journal.get_by_id(id, db)

@router.get('/user/{id}', response_model=schemas.ShowUserJournal)
def show_user_journal(id, db:Session=Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return journal.get_by_user(id, db)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_journal(request: schemas.Journal, db: Session=Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return journal.create(request, db)

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_entry(id, request:schemas.Journal, db:Session=Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return journal.update(id, request, db)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_journal(id, db:Session=Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return journal.delete(id, db)