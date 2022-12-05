from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from db.database import get_db
from auth.util import get_user_role, check_role

nomenclature_router = APIRouter(prefix="", dependencies=[Depends(get_db)], responses={404:{"description": "Not found"}})

#  попробовать дописать зависимость get_user_role к декоратору пути

@nomenclature_router.get("/category", response_model=list[schemas.Category])
async def read_categories(db: Session = Depends(get_db), role=Depends(get_user_role), roles=('manager', 'admin')):
    for i in roles:
        if role == i:  # мне не нравится это, н что-то пока не получается по нормальному=(
            return await crud.get_categories(db)  # хотя оно работает, но было бы здорово сделать декоратор
    raise HTTPException(status_code=403, detail="Forbidden")


    #return await crud.get_categories(db)


@nomenclature_router.get("/category/{title}", response_model=list[schemas.Nomenclature])
async def get_category_products(category: str, db: Session = Depends(get_db)):
    return await crud.get_nomenclature_by_category(db, category)


@nomenclature_router.post("/category", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return await crud.create_category(db=db, category=category)


@nomenclature_router.get('/nomenclature', response_model=list[schemas.Nomenclature])
async def read_nomenclatures(db: Session = Depends(get_db)):
    nomenclatures = await crud.get_nomenclature(db)
    return nomenclatures


@nomenclature_router.post("/nomenclature", response_model=schemas.Nomenclature)
async def create_nomenclature(nomenclature: schemas.NomenclatureCreate, db: Session = Depends(get_db)):
    # db_nomenclatures = await crud.get_nomenclature_by_product(db, product=nomenclature.product)
    # if db_nomenclatures:
    #    raise HTTPException(status_code=400, detail="ТАкое уже есть, надо добавлять кол-во")
    return await crud.create_nomenclature(db=db, nomenclature=nomenclature)


@nomenclature_router.post("/nomenclatures")
async def create_nomenclatures(nomenclatures: list[schemas.NomenclatureCreate], db: Session = Depends(get_db)):
    for i in nomenclatures:
        await crud.create_nomenclatures(db=db,
                                        product=i.product,
                                        description=i.description,
                                        remainder=i.remainder,
                                        category_title=i.category_title,
                                        price=i.price)

    return nomenclatures
