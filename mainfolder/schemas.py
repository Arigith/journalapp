from datetime import date
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext

pwd_ctxt=CryptContext(schemes=['bcrypt'],deprecated='auto')

class Hash():
    def bcrypt(password:str):
        return pwd_ctxt.hash(password)
    
    def verify(plain_password, hashed_password):
        return pwd_ctxt.verify(plain_password, hashed_password)

class JournalBase(BaseModel):
    title: str
    body: str

class Journal(JournalBase):
    title: str
    body: str
    date_created: date
    class Config():
        orm_mode=True
        
class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs:List[Journal] = []
    class Config():
        orm_mode=True

class show_blog(BaseModel):
    title:str
    body:str
    creator:ShowUser
    class Config():
        orm_mode=True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None