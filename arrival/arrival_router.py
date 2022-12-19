from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from . import schemas, crud

arrival_router = APIRouter(prefix="", dependencies=[Depends(get_db)], responses={404: {"description": "Not found"}},)


@arrival_router.get("/orders", response_model=list[schemas.Order])
async def get_orders(db: Session = Depends(get_db)):
    return await crud.get_order(db)


@arrival_router.get("/order/{number}", response_model=list[schemas.Arrival])
async def get_arrival_by_number(order: str, db: Session = Depends(get_db)):
    return await crud.get_arrival_for_order_number(db, order)
