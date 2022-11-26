from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import users.routers
from db import crud, models
from users import schemas, routers
from utils.dependencies import get_db
from db.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(users.routers.user_router)



