from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category = Column(ForeignKey("categorys.title"))
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))
    remainder = Column(Numeric(precision=2, asdecimal=True))
    price = Column(Numeric(precision=2, asdecimal=True))


class Cart(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    customer = Column(ForeignKey("user.id"))


class CartProduct(Base):
    __tablename__ = "cart_products"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product = Column(ForeignKey("nomenclature.id"))
    cart = Column(ForeignKey("cart.id"))
    remainder = Column(Integer, default=0)
    price = Column(ForeignKey)  # ?
