from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Table
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
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category_id = Column(ForeignKey("category.id"))
    category = relationship("Category")
    title = Column(String(64), unique=True, index=True)
    description = Column(String(128))
    remainder = Column(Numeric(precision=2, asdecimal=True))
    price = Column(Numeric(precision=2, asdecimal=True))
    cart_products = relationship("CartProduct")


cart_cartproduct = Table("cart_cartproduct", Base.metadata,
                         Column("cart_id", Integer(), ForeignKey("carts.id")),
                         Column("cart_product_id", Integer(), ForeignKey("cart_products.id"))
                         )

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


class CartProduct(Base):
    __tablename__ = "cart_products"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    product_id = Column(ForeignKey("nomenclature.id"))
    product = relationship("Nomenclature")
    remainder = Column(Integer, default=0)
    #price = Column(ForeignKey)  # ?
    cart_id = Column(ForeignKey("carts.id"))
    final_price = Column(Numeric(precision=2, asdecimal=True))
    cart = relationship("Cart", secondary=cart_cartproduct, backref="cart_products")

    def get_final_price(self):
        final_price = self.product_id.price * self.remainder
        return final_price
