from io import BytesIO

from aiogram import types
from aiogram.types import InputMediaPhoto
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import get_db_catalogs, get_db_products, add_to_db_cart, delete_from_db_cart, reduce_product_in_db_cart, \
    get_user_carts, get_product_db_by_title
from kb import get_user_main_menu, get_user_catalogs, get_products_bts, get_user_cart_bts, get_simple_kb, \
    get_search_result_bts
import config
from utils.utils import Paginator, save_bytes_to_image


async def get_menu_main(
        level: int,
        menu_name: str):
    answer_ = InputMediaPhoto(
        media='https://kartinki.pics/uploads/posts/2022-12/1671752704_kartinkin-net-p-kartinki-elektroniki-instagram-5.jpg',
        caption=config.answer[menu_name],
        parse_mode=ParseMode.HTML)
    kbds = get_user_main_menu(level=level)
    return answer_, kbds


async def make_slugs_shorter(
        catalogs: list):
    for index, (k, v) in enumerate(catalogs):
        if v.count('-') >= 3:
            v = v.split('-')
            str_ = '-'.join([v[0], v[-1]])
            t = (k, str_)
            catalogs.pop(index)
            catalogs.insert(index, t)
    return catalogs


async def get_menu_catalogs(
        level: int,
        menu_name: str | None,
        session: AsyncSession,
        page: int):

    catalogs = await get_db_catalogs(session)
    paginator = Paginator(array=catalogs, page=page, per_page=5)
    pagination_btns = pages(paginator)
    answer_ = InputMediaPhoto(
        media='https://kartinki.pics/uploads/posts/2022-12/1671752661_kartinkin-net-p-kartinki-elektroniki-instagram-7.jpg',
        caption=f'''<b>Cписок каталогов:</b>
        Страница {paginator.page} из {paginator.pages}''',
        parse_mode=ParseMode.HTML
    )
    kbds = get_user_catalogs(
        level=level,
        catalogs=paginator.get_page(),
        pagination_btns=pagination_btns,
        page=page)
    return answer_, kbds


def pages(
        paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns['prev'] = 'prev'
    if paginator.has_next():
        btns['next'] = 'next'
    return btns


def get_description(
        description: str):
    if description:
        return description[:600] if len(description) > 500 else description
    return 'Описание отсутствует.'


async def get_products(
        level: int,
        menu_name: str | None,
        session: AsyncSession,
        catalog_id: int,
        page: int):
    products = await get_db_products(session, catalog_id)
    paginator = Paginator(array=products, page=page)
    product = paginator.get_page()[0]
    pagination_btns = pages(paginator)
    description = get_description(product.description)
    text = f'''
<b>Заголовок:</b> {product.title}
<b>Артикль:</b> {product.article}
<b>В наличие:</b> {'Есть' if product.exist else 'Нет'}
<b>Цена:</b> {product.price_list}
<b>Описание:</b> {description}
<b>Ссылка:</b> {product.url}
Товар {paginator.page} из {paginator.pages}
'''
    answer_ = InputMediaPhoto(
        media=product.image,
        caption=text,
        parse_mode=ParseMode.HTML
    )
    kbds = get_products_bts(
        level=level,
        catalog_id=catalog_id,
        page=page,
        product_id=product.id,
        pagination_btns=pagination_btns,
    )
    return answer_, kbds


async def get_cart(
        level: int,
        session: AsyncSession,
        menu_name: str,
        page: int,
        user_id: int,
        product_id: int | None = None):
    answer_, kbds = None, None
    try:
        if menu_name == 'delete':
            await delete_from_db_cart(session, user_id, product_id)
            if page > 1:
                page -= 1
        elif menu_name == 'decrement':
            is_cart = await reduce_product_in_db_cart(session, user_id, product_id)
            if page > 1 and not is_cart:
                page -= 1
        elif menu_name == 'increment':
            await add_to_db_cart(session, user_id, product_id)

        carts = await get_user_carts(session, user_id)
        if not carts:
            answer_ = InputMediaPhoto(
                media='https://cdn.icon-icons.com/icons2/1580/PNG/512/2849824-basket-buy-market-multimedia-shop-shopping-store_107977.png',
                caption='<b>Корзина пуста.</b>',
                parse_mode=ParseMode.HTML)
            kbds=get_user_cart_bts(
                level=level,
                page=None,
                pagination_btns=None,
                product_id=None)
        else:
            paginator = Paginator(carts, page=page)
            cart = paginator.get_page()[0]
            cart_price = round(cart.quantity * cart.product.price_list, 2)
            total_price = round(sum(cart.quantity * cart.product.price_list for cart in carts), 2)
            answer_ = InputMediaPhoto(
                media=cart.product.image,
                caption=f'''
                <b>{cart.product.title}</b>
    <b>Цена</b>: {cart.product.price_list}
    <b>Кол в корзине</b>: {cart.quantity} шт, сумма: {cart_price} тг
    Товар {paginator.page} из {paginator.pages} в корзине.
    <b>Общая стоимость</b>: {total_price}''',
                parse_mode=ParseMode.HTML
            )
            pagination_btns = pages(paginator)
            kbds = get_user_cart_bts(
                level=level,
                page=page,
                pagination_btns=pagination_btns,
                product_id=cart.product_id)
        return answer_, kbds
    except Exception as e:
        print(e)


async def search(
        level: int,
        session: AsyncSession,
        menu_name: str,
        page: int | None,
        message: str):
    products = await get_product_db_by_title(message, session)
    paginator = Paginator(array=products, page=page)
    product = paginator.get_page()[0]
    pagination_btns = pages(paginator)
    description = get_description(product.description)
    answer_ = InputMediaPhoto(
        media=product.image,
        caption=f'''
    <b>Заголовок:</b> {product.title}
    <b>Артикль:</b> {product.article}
    <b>В наличие:</b> {'Есть' if product.exist else 'Нет'}
    <b>Цена:</b> {product.price_list if product.price_list else ''}
    <b>Описание:</b> {description}
    <b>Ссылка:</b> {product.url}
    Товар {paginator.page} из {paginator.pages} найденного.''')
    kbds = get_search_result_bts(
        level=level,
        menu_name=menu_name,
        page=page,
        product_id=product.id,
        pagination_btns=pagination_btns,
    )
    return answer_, kbds


async def get_menu_content(
        level: int,
        menu_name: str,
        catalog_id: int | None = None,
        session: AsyncSession | None = None,
        page: int | None = None,
        user_id: int | None = None,
        product_id: int | None = None,
        message: str | None = None):
    if level == 0:
        return await get_menu_main(level, menu_name)
    elif level == 1:
        return await get_menu_catalogs(level, menu_name, session, page)
    elif level == 2:
        return await get_products(level, menu_name, session, catalog_id, page)
    elif level == 3:
        return await get_cart(level, session, menu_name, page, user_id, product_id)
    elif level == 4:
        return await search(level, session, menu_name, page, message)
