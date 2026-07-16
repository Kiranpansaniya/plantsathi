from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,Header
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db,Customer

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    print("Password:", repr(password))
    print("Type:", type(password))
    print("Length:", len(password))
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict)->str:
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(
        authorization : Optional[str]=Header(None),
        db : Session = Depends(get_db)
    )->Customer:
    credentials_exception=HTTPException(
    status_code=401,
    detail="Could not validate credential",
    )
    if authorization is None or not authorization.startswith("Bearer"):
        raise credentials_exception
    token=authorization.split(" ")[1]
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user=db.query(Customer).filter(Customer.id==int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user