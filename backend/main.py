from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Plant
from schemas import PlantOut

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