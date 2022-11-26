from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from utils.dependencies import get_db
from . import schemas
from db import crud


user_router = APIRouter(
    prefix="",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/users", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@user_router.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@user_router.get("/user/{username}", response_model=schemas.User)
async def read_user_username(username: str, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.get("/user/id/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
