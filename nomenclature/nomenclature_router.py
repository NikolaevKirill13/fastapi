from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas

from db.database import get_db


nomenclature_router = APIRouter(
    prefix="",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@nomenclature_router.get('/nomenclature', response_model=list[schemas.Nomenclature])
async def read_nomenclature(db: Session = Depends(get_db)):
    nomenclatures = await crud.get_nomenclature(db)
    return nomenclatures


@nomenclature_router.post("/nomenclature", response_model=list[schemas.NomenclatureCreate])
async def create_nomenclature(nomenclature: schemas.NomenclatureCreate, db: Session = Depends(get_db)):
    #db_nomenclatures = await crud.get_nomenclature_by_product(db, product=nomenclature.product)
    #if db_nomenclatures:
    #    raise HTTPException(status_code=400, detail="ТАкое уже есть, надо добавлять кол-во")
    return await crud.create_nomenclature(db=db, nomenclature=nomenclature)
