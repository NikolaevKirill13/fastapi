from pydantic import BaseModel
from typing import List


class Supplier(BaseModel):
    name: str


class OrderCreate(BaseModel):
    incoming_number: str
    supplier_name: List[Supplier] = []


class Order(OrderCreate):
    date: str


class ArrivalBase(BaseModel):
    order_number: str
    product: str


class ArrivalCreate(ArrivalBase):
    remainder: float
    price: float


class Arrival(ArrivalCreate):
    id: int


class ArrivalAccepted(ArrivalBase):
    received: bool

