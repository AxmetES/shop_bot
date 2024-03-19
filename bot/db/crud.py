import asyncio
import logging

from sqlalchemy import select, update, delete, distinct
from sqlalchemy import text
from sqlalchemy.orm import joinedload

from db.models import Product, User, Cart, Category
from db.engine import AsyncSession


async def get_db_catalogs(session: AsyncSession):
    try:
        sql_query = select(Category)
        result = await session.execute(sql_query)
        return result.scalars().all()
    except Exception as e:
        logging.exception(e)


async def get_db_products(session: AsyncSession,
                          catalog_id: int):
    try:
        query = select(Product).where(Product.category_id == catalog_id)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        logging.exception(e)
        print(e)


async def add_db_user(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None):
    try:
        query = select(User).where(User.user_id == 6416664703)
        result = await session.execute(query)
        if result.first() is None:
            session.add(
                User(user_id=user_id,
                     first_name=first_name,
                     last_name=last_name,
                     phone=phone)
            )
            await session.commit()
    except Exception as e:
        print(e)


async def add_to_db_cart(
        session: AsyncSession,
        user_id: int,
        product_id: int):
    query = select(Cart).where(
        Cart.user_id == user_id,
        Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
    else:
        session.add(
            Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=1))
        await session.commit()


async def delete_from_db_cart(
        session: AsyncSession,
        user_id: int,
        product_id: int):
    query = delete(Cart).where(
        Cart.user_id == user_id,
        Cart.product_id == product_id)
    await session.execute(query)
    await session.commit()


async def reduce_product_in_db_cart(
        session: AsyncSession,
        user_id: int,
        product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(
        joinedload(Cart.product))
    cart = await session.execute(query)
    cart = cart.scalar()
    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await delete_from_db_cart(session, user_id, product_id)
        return False


async def get_user_carts(
        session: AsyncSession,
        user_id: int):
    try:
        query = select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
        result = await session.execute(query)
        result = result.scalars().all()
        return result
    except Exception as e:
        print(e)


async def check_if_exist(session: AsyncSession,
                         product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    result = result.scalar()
    if not result or result.exist is False:
        return False
    return True


async def get_product_db_by_title(
        title: str,
        session: AsyncSession):
    try:
        query = select(Product).where(Product.title.ilike(f'%{title}%'))
        result = await session.execute(query)
        result = result.scalars().all()
        return result
    except Exception as e:
        print(e)
