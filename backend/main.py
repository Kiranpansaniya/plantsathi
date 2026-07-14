from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from database import get_db, Plant,Customer
from schemas import PlantOut,TokenResponse,UserSignup,UserLogin,UserOut
from auth import hash_password,verify_password,create_access_token,get_current_user
from schemas import PlantOut,TokenResponse,UserSignup,UserLogin,UserOut
from database import get_db,Plant,Customer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/plants", response_model=List[PlantOut])
def get_plants(db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return plants

@app.post("/api/auth/signup",response_model=TokenResponse)
def signup(user_data:UserSignup,db:Session=Depends(get_db)):
    existing=db.query(Customer).filter(Customer.email==user_data.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")
    new_user=Customer(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

@app.post("/api/auth/login",response_model=TokenResponse)
def login(credentials:UserLogin,db:Session=Depends(get_db)):
    user=db.query(Customer).filter(Customer.email==credentials.email).first()

    if not user or not verify_password(credentials.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    token = create_access_token({"sub":str(user.id)})
    return {"access_token":token,"user":user}

@app.get("/api/auth/me",response_model=UserOut)
def get_me(current_user:Customer=Depends(get_current_user)):
    return current_user 