from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    name: str = Field(min_length=1) 
    age: int = Field(gt=0, lt=101) 
    phone: int = Field(gt=0, lt=9999999999) 


USERS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@app.post("/",)
def create_user(user: User, db: Session = Depends(get_db)):

    user_model = models.Users()
    user_model.name = user.name
    user_model.age = user.age
    user_model.phone = user.phone

    db.add(user_model)
    db.commit()

    return user


@app.put("/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    user_model.name = user.name
    user_model.age = user.age
    user_model.phone = user.phone

    db.add(user_model)
    db.commit()

    return user


@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    db.query(models.Users).filter(models.Users.id == user_id).delete()

    db.commit()
