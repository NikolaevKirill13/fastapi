from fastapi import FastAPI
import auth.routers
import nomenclature.nomenclature_router
import users.users_routers
from db import models
from db.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.routers.auth_router)
app.include_router(users.users_routers.user_router)
app.include_router(nomenclature.nomenclature_router.nomenclature_router)


@app.get('/')
async def index():
    return {'message': 'hello world'}
