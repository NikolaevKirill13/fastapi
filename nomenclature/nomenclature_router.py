from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from db.models import Category

from db.database import get_db


nomenclature_router = APIRouter(
    prefix="",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@nomenclature_router.get("/category", response_model=list[schemas.Category])
async def read_category(db: Session = Depends(get_db)):

    return await crud.get_category(db)


@nomenclature_router.post("/category", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):

    return await crud.create_category(db=db, category=category)


@nomenclature_router.get('/nomenclature', response_model=list[schemas.Nomenclature])
async def read_nomenclature(db: Session = Depends(get_db)):
    nomenclatures = await crud.get_nomenclature(db)
    return nomenclatures


@nomenclature_router.post("/nomenclature", response_model=schemas.Nomenclature)
async def create_nomenclature(nomenclature: schemas.NomenclatureCreate, db: Session = Depends(get_db)):
    # db_nomenclatures = await crud.get_nomenclature_by_product(db, product=nomenclature.product)
    # if db_nomenclatures:
    #    raise HTTPException(status_code=400, detail="ТАкое уже есть, надо добавлять кол-во")
    return await crud.create_nomenclature(db=db, nomenclature=nomenclature)


@nomenclature_router.get("/test", response_model=list[schemas.Category])
async def get_test(cretery: str, db: Session = Depends(get_db)):

    return await crud.get_test(db, modely=Category, cretery=cretery)
