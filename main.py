from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.test import authenticate_user
from utils.dependencies import get_db
import users.routers
from db import models
from db.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(users.routers.user_router)



