from sqlalchemy.orm import Session
from db.models import Arrival, OrderToSupplier
from .schemas import OrderCreate, ArrivalCreate, ArrivalAccepted


async def create_order(db: Session, order: OrderCreate):
    db_order = OrderToSupplier(incoming_number=order.incoming_number,
                               supplier_name=order.supplier_name
                               )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


async def get_order(db: Session):
    return db.query(OrderToSupplier).all()


async def get_orders_for_supplier(db: Session, supplier: str):
    return db.query(OrderToSupplier).filter(OrderToSupplier.supplier == supplier).all()


async def delete_order(db: Session, order: str):
    db_delete = db.query(OrderToSupplier).filter(OrderToSupplier.incoming_number == order).one()
    db.delete(db_delete)
    db.commit()


async def create_arrival(db: Session, arrival: ArrivalCreate):
    db_arrival = Arrival(order_number=arrival.order_number,
                         product=arrival.product,
                         remainder=arrival.remainder,
                         price=arrival.price)
    db.add(db_arrival)
    db.commit()
    db.refresh(db_arrival)
    return db_arrival


async def get_arrival(db: Session):
    return db.query(Arrival).all()


async def get_arrival_for_order_number(db: Session, order: str):
    return db.query(Arrival).filter(Arrival.order_number == order).all()


async def get_arrival_for_product(db: Session, product: str):
    return db.query(Arrival).filter(Arrival.product == product).all()

