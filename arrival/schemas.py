from pydantic import BaseModel


class OrderCreate(BaseModel):
    incoming_number: str
    provaider: str


class Order(OrderCreate):
    date: str


class ArrivalBase(BaseModel):
    order_number: str
    product: str


class ArrivalCreate(ArrivalBase):
    remainder: float
    price: float


class ArrivalAccepted(ArrivalBase):
    received: bool

