from pydantic import BaseModel


class NomenclatureBase(BaseModel):
    product: str
    description: str


class NomenclatureCreate(NomenclatureBase):
    remainder: int
    category_title: str
    price: int


class Nomenclature(BaseModel):
    id: int
    product: str
    description: str
    remainder: int
    category_title: str
    price: int

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    title: str
    description: str


class Category(CategoryCreate):
    id: int

    class Config:
        orm_mode = True
