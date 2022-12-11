from pydantic import BaseModel


class OrderCreate(BaseModel):
    incoming_number: str
    provaider: str


class Order(OrderCreate):
    id: int
    date: str


class ArrivalBase(BaseModel):
    order_id: int
    product: str


class ArrivalCreate(ArrivalBase):
    remainder: float
    price: float


class ArrivalAccepted(ArrivalBase):
    received: bool

