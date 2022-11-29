from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas
from repository import user

router=APIRouter(
    prefix='/user',
    tags=["user"],
)

@router.post('/create', response_model=schemas.ShowUser)
def create_user(request:schemas.User, db:Session=Depends(get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def show_user(id, db:Session=Depends(get_db)):
    return user.get_id(id, db)

@router.delete('/delete/{id}')
def delete_user(id, db:Session=Depends(get_db)):
    return user.delete_user(id, db)