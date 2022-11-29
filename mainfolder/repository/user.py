from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas

def create(request:schemas.User, db:Session):
    new_user=models.User(name=request.name, email=request.email ,password=schemas.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_id(id:int, db:Session):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    return user

def delete_user(id:int, db:Session):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    user.delete(synchronize_session=False)
    db.commit()
    return 'Deleted as requested'