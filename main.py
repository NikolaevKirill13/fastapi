from fastapi import FastAPI, Depends

import auth.routers
from auth.util import get_current_user, User
import users.routers
from db import models
from db.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.routers.auth_router)
app.include_router(users.routers.user_router)


@app.get('/')
async def index():
    return {'message': 'hello world'}
