from sqlalchemy.orm import Session
from db.models import Nomenclature
from .schemas import NomenclatureCreate


async def get_nomenclature(db: Session):
    return db.query(Nomenclature).all()


async def get_nomenclature_by_product(db: Session, product: str):
    return db.query(Nomenclature).filter(Nomenclature.product == product).first()


async def create_nomenclature(db: Session, nomenclature: NomenclatureCreate):
    db_nomenclature = Nomenclature(product=nomenclature.product, description=nomenclature.description,
                                   remainder=nomenclature.remainder, category_name=nomenclature.category_name,
                                   price=nomenclature.price)
    db.add(db_nomenclature)
    db.commit()
    db.refresh(db_nomenclature)
    return db_nomenclature