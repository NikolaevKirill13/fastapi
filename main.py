from fastapi import FastAPI, Depends
import auth.routers
from sqlalchemy.orm import Session
import settings
import nomenclature.nomenclature_router
import users.users_routers
from db import models
from db.database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.routers.auth_router)
app.include_router(users.users_routers.user_router)
app.include_router(nomenclature.nomenclature_router.nomenclature_router)


@app.on_event("startup")
async def startup():
    #models.Base.metadata.create_all(bind=engine)
    print('админа нет')
"""надо получить админа из .env и сверить с дб, если дб нет - создать дб с моделями
    и добавить туда главного админа. если дб есть - проверить наличие админа, если нет - создать"""


@app.get('/')
async def index():
    return {'message': 'hello world'}
