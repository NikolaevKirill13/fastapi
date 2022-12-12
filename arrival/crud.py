from sqlalchemy.orm import Session
from db.models import Arrival, OrderToSupplier
from .schemas import OrderCreate, ArrivalCreate, ArrivalAccepted


async def get_order(db: Session):
    return db.query(OrderToSupplier).all()


async def get_arrival(db: Session):
    return db.query(Arrival).all()
