from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
import datetime
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


class AgentContragent(Base): #  дурацкое название, но лучше мне не придумать
    __tablename__ = 'agent_contragent'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    company_name = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(32), unique=True, nullable=False)
    contact_name = Column(String(32), nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class ClientScore(Base):
    __tablename__ = 'client_score'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    company_id = Column(ForeignKey("agent_contragent.id"))
    company = relationship('AgentContragent', foreign_keys='ClientScore.company_id', lazy='joined')
    remainder = Column(Float)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category_title = Column(ForeignKey("category.title"))
    category = relationship('Category', foreign_keys='Nomenclature.category_title', lazy='joined')
    product = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))
    remainder = Column(Numeric(precision=2, asdecimal=True))
    price = Column(Float, nullable=False)


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    client_id = Column(ForeignKey("agent_contragent.id"))
    client = relationship("AgentContragent", foreign_keys='Cart.client_id', lazy='joined')
    payment = Column(Boolean, default=False)

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

    product_id = Column(ForeignKey("nomenclature.id"), primary_key=True, index=True)
    products = relationship("Nomenclature", foreign_keys='CartProduct.product_id')
    remainder_product = Column(Integer, default=0)
    price_product = Column(Float, nullable=False)
    cart_id = Column(ForeignKey("carts.id"))
    final_price = Column(Float, nullable=False)

    def get_price(self):
        self.price_product = self.products_id.price
        return self.price_product

    def get_final_price(self):
        self.final_price = self.price_product * self.remainder
        return self.final_price


class OrderToSupplier(Base):
    __tablename__ = 'order_to_supplier'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    receipt_date = Column(DateTime)
    provaider = Column(String)
    product = Column(String(128), index=True, nullable=False)
    remainder = Column(Float, nullable=False)
    price = Column(Float, nullable=False)


class Arrival(Base):
    __tablename__ = 'arrival'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    receipt_date = Column(DateTime)
    reason_id = Column(ForeignKey('order_to_supplier.id'))
    reason = relationship("OrderToSupplier", foreign_keys="Arrival.reason_id")
    incoming_number = Column(String(64), index=True)
    product = Column(String(128), index=True, nullable=False)
    remainder = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
