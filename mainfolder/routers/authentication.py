from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas, database, models, jwt_token

router = APIRouter(
    prefix='/login',
    tags=['login']
)

@router.post('')
def login(request: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    if not schemas.Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong. Please check your details and try again')
    access_token_expires = jwt_token.timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}