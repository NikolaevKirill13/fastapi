from sqlalchemy.orm import Session
from db.models import Nomenclature, Category
from .schemas import NomenclatureCreate, CategoryCreate


async def get_category(db: Session):
    return db.query(Category).all()


async def create_category(db: Session, category: CategoryCreate):
    db_category = Category(title=category.title, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


async def get_nomenclature(db: Session):
    return db.query(Nomenclature).all()


async def get_nomenclature_by_product(db: Session, product: str):
    return db.query(Nomenclature).filter(Nomenclature.product == product).first()


async def create_nomenclature(db: Session, nomenclature: NomenclatureCreate):
    db_nomenclature = Nomenclature(product=nomenclature.product, description=nomenclature.description,
                                   remainder=nomenclature.remainder, category_title=nomenclature.category_title,
                                   price=nomenclature.price)
    db.add(db_nomenclature)
    db.commit()
    db.refresh(db_nomenclature)
    return db_nomenclature
