from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import answer
from utils.utils import MenuCallBack


def get_user_main_menu(level: int,
                       size: tuple[int] = (2,)):
    kb = InlineKeyboardBuilder()
    btns = {
        'Поиск': 'search',
        'Каталоги': 'catalogs',
        'О нас': 'about_us',
        'Корзина 🛒': 'cart'
    }

    for key, val in btns.items():
        if val == 'search':
            kb.add(InlineKeyboardButton(
                text=val,
                callback_data=MenuCallBack(level=4, menu_name=val).pack()
            ))
        elif val == 'catalogs':
            kb.add(InlineKeyboardButton(
                text=key,
                callback_data=MenuCallBack(level=level + 1, menu_name=val).pack()
            ))
        elif val == 'cart':
            kb.add(InlineKeyboardButton(
                text=key,
                callback_data=MenuCallBack(level=3, menu_name=val).pack()
            ))
        else:
            kb.add(InlineKeyboardButton(
                text=key,
                callback_data=MenuCallBack(level=level, menu_name=val).pack()
            ))
    return kb.adjust(*size).as_markup()


def get_user_catalogs(
        level: int,
        catalogs: list,
        pagination_btns: dict | None,
        page: int,
        size: tuple[int] = (2, 1)):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(
        text='Назад',
        callback_data=MenuCallBack(level=0, menu_name='main').pack()))
    kb.add(InlineKeyboardButton(
        text=answer['cart'],
        callback_data=MenuCallBack(level=3, menu_name='cart').pack()))
    for catalog in catalogs:
        kb.add(InlineKeyboardButton(
            text=catalog.catalog_rus,
            callback_data=MenuCallBack(
                level=level+1,
                menu_name=catalog.catalog_name,
                catalog_id=catalog.id).pack()))
    kb.adjust(*size)
    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == 'next':
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    # catalog='catalogs',
                    page=page + 1).pack()))
        elif menu_name == 'prev':
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    # catalog='catalogs',
                    page=page - 1).pack()))
    return kb.row(*row).as_markup()


def get_products_bts(level: int,
                     catalog_id: int,
                     page: int,
                     product_id: int,
                     pagination_btns: dict,
                     size: tuple[int] = (2, 1)):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text='Назад',
                                callback_data=MenuCallBack(
                                    level=level - 1,
                                    menu_name='catalogs').pack()))
    kb.add(InlineKeyboardButton(text=answer['cart'],
                                callback_data=MenuCallBack(
                                    level=3,
                                    menu_name='cart').pack()))
    kb.add(InlineKeyboardButton(text=answer['add_to_cart'],
                                callback_data=MenuCallBack(
                                    level=level,
                                    menu_name='add_to_cart',
                                    product_id=product_id).pack()))
    kb.adjust(*size)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == 'next':
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    catalog_id=catalog_id,
                    page=page + 1).pack()))
        elif menu_name == 'prev':
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    catalog_id=catalog_id,
                    page=page - 1).pack()))
    return kb.row(*row).as_markup()


def get_user_cart_bts(
        level: int,
        page: int | None,
        pagination_btns: dict | None,
        product_id: int | None,
        size: tuple[int] = (3,)) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if page:
        kb.add(
            InlineKeyboardButton(
                text='Удалить',
                callback_data=MenuCallBack(
                    level=level,
                    menu_name='delete',
                    product_id=product_id,
                    page=page).pack()))
        kb.add(
            InlineKeyboardButton(
                text='━ 1',
                callback_data=MenuCallBack(
                    level=level,
                    menu_name='decrement',
                    product_id=product_id,
                    page=page).pack()))
        kb.add(
            InlineKeyboardButton(
                text='✚ 1',
                callback_data=MenuCallBack(
                    level=level,
                    menu_name='increment',
                    product_id=product_id,
                    page=page).pack()))
        kb.adjust(*size)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == 'next':
                row.append(InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        page=page + 1).pack()))
            elif menu_name == 'prev':
                row.append(InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        page=page - 1).pack()))
        kb.row(*row)

        row_2 = [
            InlineKeyboardButton(
                text='На главную',
                callback_data=MenuCallBack(
                    level=0,
                    menu_name='main').pack()),
            InlineKeyboardButton(
                text='Заказать',
                callback_data=MenuCallBack(
                    level=0,
                    menu_name='order').pack()),
        ]
        return kb.row(*row_2).as_markup()
    else:
        kb.add(
            InlineKeyboardButton(
                text='На главную',
                callback_data=MenuCallBack(
                    level=0,
                    menu_name='main').pack()))
        return kb.adjust(*size).as_markup()


def get_simple_kb(size: tuple[int] = (2, 1)):
    keyboard = InlineKeyboardBuilder()
    InlineKeyboardButton(
        text='На главную',
        callback_data=MenuCallBack(
            level=0,
            menu_name='main').pack())
    return keyboard.adjust(*size).as_markup()


def get_search_result_bts(
        level: int,
        menu_name: str,
        page: int,
        product_id: int,
        pagination_btns: dict | None,
        size: tuple[int] = (3,)):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text='Назад',
                                callback_data=MenuCallBack(
                                    level=0,
                                    menu_name='main').pack()))
    kb.add(InlineKeyboardButton(text=answer['cart'],
                                callback_data=MenuCallBack(
                                    level=3,
                                    menu_name='cart').pack()))
    kb.add(InlineKeyboardButton(text=answer['add_to_cart'],
                                callback_data=MenuCallBack(
                                    level=level,
                                    menu_name='add_to_cart',
                                    product_id=product_id).pack()))
    kb.adjust(*size)

    row = []

    for text, menu_name in pagination_btns.items():
        if menu_name == 'next':
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    page=page + 1).pack()))
        elif menu_name == 'prev':
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    page=page - 1).pack()))
    return kb.row(*row).as_markup()
