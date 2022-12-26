from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from datetime import datetime
from .database import Base


class Preference(Base):
    """Настройки компании"""
    __tablename__ = "preference"

    company_name = Column(String(64), primary_key=True, comment="Название компании")
    legal_address = Column(String, comment="Юридический адрес")
    actual_address = Column(String, comment="Фактический адрес")
    phone = Column(String, comment="Телефон")
    bank_name = Column(String, comment="Название банка компании")
    bank_account = Column(Integer, comment="номер банковского счета")
    corr_accounts = Column(Integer, comment="Корр.счет")
    bik = Column(Integer, comment="БИК банка")
    inn = Column(Integer, comment="ИНН компании")
    # заполнить

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


class User(Base):
    """Модель пользователей """
    __tablename__ = "user"

    # список возможных вариантов роли пользователя для примитивной версии ограничения прав доступа
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
    phone = Column(String(32), unique=True, nullable=False)
    contact_name = Column(String(32), nullable=True)
    discount = Column(Float(precision=2))
    is_active = Column(Boolean, default=True)
    role = Column(ChoiceType(USERS), default='user')
    address = relationship("Address", cascade="all, delete", passive_deletes=True)
    score = relationship("ClientScore", uselist=False)
    cart = relationship("Cart", uselist=False, cascade="all, delete", passive_deletes=True)
    fin_data = relationship("FinancialDataOfOrganizations", cascade="all, delete", passive_deletes=True)


class FinancialDataOfOrganizations(Base):
    __tablename__ = 'document_organizations'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(ForeignKey("user.username", ondelete="CASCADE"))
    user = relationship("User", foreign_keys="FinancialDataOfOrganizations.username", lazy='joined')
    company = Column(String(128), unique=True, index=True)
    bank_name = Column(String)
    bank_account = Column(Integer, comment="номер банковского счета")
    corr_accounts = Column(Integer)
    bik = Column(Integer)
    inn = Column(Integer, unique=True)

    # надо дозаполнить


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True, nullable=False)
    orders = relationship("OrderToSupplier")


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(ForeignKey("user.username", ondelete="CASCADE"))
    user = relationship("User", foreign_keys="Address.username", lazy='joined')
    address = Column(String)
    contact_phone = Column(String(24))


class UserScore(Base):
    __tablename__ = 'user_score'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(ForeignKey("user.username", ondelete="NULL"))
    user = relationship('User', foreign_keys='UserScore.username', lazy='joined')
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
    category_title = Column(ForeignKey("category.title", ondelete="NULL"))
    category = relationship('Category', foreign_keys='Nomenclature.category_title', lazy='joined')
    product = Column(String(64), unique=True, index=True, nullable=False)
    description = Column(String(128))
    remainder = Column(Numeric(precision=2, asdecimal=True))
    price = Column(Float, nullable=False)


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(ForeignKey("user.username", ondelete="CASCADE"))
    user = relationship("User", foreign_keys='Cart.username', lazy='joined')
    payment = Column(Boolean, default=False)
    products = relationship("CartProducts", cascade="all, delete", passive_deletes=True)

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

    product_id = Column(ForeignKey("nomenclature.product", ondelete="CASCADE"), primary_key=True, index=True)
    products = relationship("Nomenclature", foreign_keys='CartProduct.product_id')
    remainder_product = Column(Integer, default=0)
    price_product = Column(Float, nullable=False)
    cart_id = Column(ForeignKey("carts.id", ondelete="CASCADE"))
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
    supplier_name = Column(ForeignKey("supplier.name", ondelete="NULL"))
    supplier = relationship("Supplier", foreign_keys="OrderToSupplier.supplier_name", lazy='joined')
    order_date = Column(DateTime, default=datetime.now)
    arrivals = relationship("Arrival", cascade="all, delete", passive_deletes=True)


class Arrival(Base):
    __tablename__ = 'arrival'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    date = Column(DateTime(), default=datetime.now)
    order_number = Column(ForeignKey("order_to_supplier.incoming_number", ondelete="CASCADE"))
    order = relationship("OrderToSupplier", foreign_keys="Arrival.order_number", lazy='joined',
                         back_populates="arrivals")
    product = Column(String(128), index=True, nullable=False)
    remainder = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    received = Column(Boolean, default=False)
