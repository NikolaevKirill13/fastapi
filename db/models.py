from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "user"

    USERS = [
        ('admin', 'Администратор'),
        ('top_manager', 'Главный менеджер'),
        ('user', 'Пользователь'),
        ('sales_manager', 'Менеджер по продажам'),
        ('purchasing_manager', 'Менеджер по закупкам'),
        ('warehouse_manager', 'Менеджер склада'),
    ]

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(ChoiceType(USERS), default='user')


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    company_name = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(32), unique=True, nullable=False)
    contact_name = Column(String(32), nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    discount = Column(Float(precision=2))
    address = relationship("Address")
    score = relationship("ClientScore", uselist=False)
    cart = relationship("Cart", uselist=False)


class FinancialDataOfOrganizations(Base):
    __tablename__ = 'document_organizations'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    # надо дозаполнить


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True, nullable=False)
    orders = relationship("OrderToSupplier")


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    client_id = Column(ForeignKey("client.id"))
    client = relationship("Client", foreign_keys="Address.client_id", lazy='joined')
    address = Column(String)
    contact_phone = Column(String(24))


class ClientScore(Base):
    __tablename__ = 'client_score'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    client_id = Column(ForeignKey("client.id"))
    client = relationship('Client', foreign_keys='ClientScore.client_id', lazy='joined')
    remainder = Column(Float)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))
    products = relationship("Nomenclature")


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
    client_id = Column(ForeignKey("client.id"))
    client = relationship("Client", foreign_keys='Cart.client_id', lazy='joined')
    payment = Column(Boolean, default=False)
    products = relationship("CartProducts")

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

    product_id = Column(ForeignKey("nomenclature.product"), primary_key=True, index=True)
    products = relationship("Nomenclature", foreign_keys='CartProduct.product_id')
    remainder_product = Column(Integer, default=0)
    price_product = Column(Float, nullable=False)
    cart_id = Column(ForeignKey("carts.id"))
    cart = relationship("Cart", foreign_keys="CartProduct.cart_id")
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
    incoming_number = Column(String(64), index=True)
    supplier_name = Column(ForeignKey("supplier.name"))
    supplier = relationship("Supplier", foreign_keys="OrderToSupplier.supplier_name", lazy='joined')
    order_date = Column(DateTime, default=datetime.now)
    arrivals = relationship("Arrival")


class Arrival(Base):
    __tablename__ = 'arrival'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    date = Column(DateTime(), default=datetime.now)
    order_number = Column(ForeignKey("order_to_supplier.incoming_number"))
    order = relationship("OrderToSupplier", foreign_keys="Arrival.order_number", lazy='joined')
    product = Column(String(128), index=True, nullable=False)
    remainder = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    received = Column(Boolean, default=False)

