import json
from decimal import Decimal

from sqlalchemy import (DateTime, ForeignKey, Numeric, String, Text, BigInteger, func, Boolean,
                        JSON, ARRAY, LargeBinary)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    catalog_name: Mapped[str] = mapped_column(String(50))
    catalog_rus: Mapped[str] = mapped_column(String(50))


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exist: Mapped[bool] = mapped_column(Boolean())
    title: Mapped[str] = mapped_column(String(150), unique=True)
    image: Mapped[str] = mapped_column(String(200))
    article: Mapped[str] = mapped_column(String(150))
    price_list: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    price_in_chain_stores: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    price_in_the_online_store: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    product_price_of_the_week: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    details: Mapped[json] = mapped_column(JSON, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(150), nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='SET NULL'), nullable=False)
    category: Mapped[Category] = relationship(backref='product')


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int]

    user: Mapped['User'] = relationship(backref='cart')
    product: Mapped['Product'] = relationship(backref='cart')