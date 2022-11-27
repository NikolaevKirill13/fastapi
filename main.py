from fastapi import FastAPI, Depends
from auth.test import get_current_user, User
import users.routers
from db import models
from db.database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(users.routers.user_router)


@app.get('/')
async def index_for_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        return {'detail': 'user active'}
    else:
        return {'detail user': 'user not active'}



