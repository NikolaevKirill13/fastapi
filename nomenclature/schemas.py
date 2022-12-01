from pydantic import BaseModel
from db.models import Category


class NomenclatureBase(BaseModel):
    product: str
    description: str


class NomenclatureCreate(NomenclatureBase):
    remainder: int
    category_name = Category
    price: int


class Nomenclature(BaseModel):
    id: int
    product: str
    description: str
    remainder: int
    category_name = Category
    price: int

    class Config:
        orm_mode = True
