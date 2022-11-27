from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.test import authenticate_user, get_current_user, User
from utils.dependencies import get_db
import users.routers
from db import models
from db.database import engine
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(users.routers.user_router)


@app.get('/')
async def index_for_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        return {'detail': 'user active'}
    else:
        return {'detail user': 'user not active'}



