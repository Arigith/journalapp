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
    

@app.post('/journal/create', status_code=status.HTTP_201_CREATED, tags=["journal"])
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

@app.put('/journal/update/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["journal"])
def update_entry(id, request:schemas.Journal, db:Session=Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.update(request.dict())
    db.commit()
    return 'Journal has been updated as requested'

@app.delete('/journal/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["journal"])
def delete_journal(id, db:Session=Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == id)
    if not journal.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    journal.delete(synchronize_session=False)    
    db.commit()
    return 'journal entry has been removed'

@app.get('/journal', status_code=status.HTTP_200_OK, response_model=List[schemas.Journal], tags=["journal"])
def all_journals(db: Session=Depends(get_db)):
    journals=db.query(models.Journal).all()
    return journals

@app.get('/journal/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Journal, tags=["journal"])
def show_individual_journal(id, db:Session=Depends(get_db)):
    journal=db.query(models.Journal).filter(models.Journal.id == id).first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return journal

@app.post('/user/create', response_model=schemas.ShowUser, tags=["user"])
def create_user(request:schemas.User, db:Session=Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email ,password=schemas.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=["user"])
def show_user(id, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return user

@app.delete('/user/delete/{id}', tags=["user"])
def delete_user(id, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    user.delete(synchronize_session=False)
    db.commit()
    return 'Deleted as requested'