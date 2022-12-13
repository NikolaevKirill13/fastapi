from sqlalchemy.orm import Session
from db.models import Arrival, OrderToSupplier
from .schemas import OrderCreate, ArrivalCreate, ArrivalAccepted


async def get_order(db: Session):
    return db.query(OrderToSupplier).all()


async def get_orders_for_supplier(db: Session, supplier: str):
    return db.query(OrderToSupplier).filter(OrderToSupplier.supplier == supplier).all()


async def get_arrival(db: Session):
    return db.query(Arrival).all()


async def get_arrival_for_order_number(db: Session, number: int):
    return db.query(Arrival).filter(Arrival.order_id == number).all()

