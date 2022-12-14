from sqlalchemy.orm import Session
from users.function import pass_gen
from db import models
from users import schemas


async def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_hashed_password(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user.hashed_password


async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pass_gen(str(user.password))
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
