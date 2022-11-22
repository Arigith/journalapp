from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.post('/journal', status_code=status.HTTP_201_CREATED)
def create_journal(request: schemas.Journal, db: Session=Depends(get_db)):
    journal_entry=models.Journal(
        title=request.title,
        body=request.body
        )
    db.add(journal_entry)
    db.commit()
    db.refresh(journal_entry)
    return request

@app.put('/journal/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_entry(id, request:schemas.Journal, db:Session=Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.update(request.dict())
    db.commit()
    return 'Journal has been updated as requested'

@app.delete('/journal/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_journal(id, db:Session=Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.delete(synchronize_session=False)    
    db.commit()
    return 'journal entry has been removed'

@app.get('/journal', status_code=status.HTTP_200_OK, response_model=List[schemas.Journal])
def all_journals(db: Session=Depends(get_db)):
    journals=db.query(models.Journal).all()
    return journals

@app.get('/journal/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Journal)
def show_individual_journal(id, db:Session=Depends(get_db)):
    journal=db.query(models.Journal).filter(models.Journal.id == id).first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return journal

@app.post('/user')
def create_user(request:schemas.User):
    return