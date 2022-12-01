from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from .database import Base


class User(Base):
    __tablename__ = "user"

    TYPES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'user')
    ]

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(ChoiceType(TYPES), default='user')


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)
    description = Column(String(128))



class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category_id = Column(ForeignKey("category.id"))
    category = relationship('Category', foreign_keys='Nomenclature.category_id', lazy='joined')
    product = Column(String(64), unique=True, index=True)
    description = Column(String(128))
    remainder = Column(Numeric(precision=2, asdecimal=True))
    price = Column(Float)


#cart_cartproduct = Table("cart_cartproduct", Base.metadata,
#                         Column("cart_id", Integer(), ForeignKey("carts.id")),
#                         Column("cart_product_id", Integer(), ForeignKey("cart_products.id"))
#                         )


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(ForeignKey("user.id"))
    user = relationship("User")

    def get_products(self):
        products = self.id.cart_products
        return products

    def get_final_price(self):
        rel_prod = self.get_products()
        final = 0
        for i in rel_prod:
            final += i.final_price
        return final


class CartProduct(Nomenclature):
    __tablename__ = "cart_product"

    #id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product_id = Column(ForeignKey("nomenclature.id"), primary_key=True, )
    products = relationship("Nomenclature", foreign_keys='CartProduct.product_id')
    remainder_product = Column(Integer, default=0)
    price_product = Column(Integer, default=0)
    cart_id = Column(ForeignKey("carts.id"))
    final_price = Column(Numeric(precision=2, asdecimal=True))

    def get_price(self):
        self.price_product = self.products_id.price
        return self.price_product

    def get_final_price(self):
        self.final_price = self.price_product * self.remainder
        return self.final_price
