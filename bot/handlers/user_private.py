from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud import add_db_user, add_to_db_cart, check_if_exist
from handlers.menu_processing import get_menu_content
from kb import MenuCallBack

user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: types.Message,):
    media, reply_markup = await get_menu_content(level=0, menu_name='main')
    await message.answer_photo(
        media.media,
        caption=media.caption,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup)


async def add_to_cart(callback: types.CallbackQuery,
                      callback_data: MenuCallBack,
                      session: AsyncSession):
    user = callback.from_user
    await add_db_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None
    )
    if await check_if_exist(session, product_id=callback_data.product_id):
        await add_to_db_cart(
            session,
            user_id=user.id,
            product_id=callback_data.product_id)
        await callback.answer('Товар добавлен в корзину!')
    else:
        await callback.answer('Товара нет в наличие!')


@user_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery,
                    callback_data: MenuCallBack,
                    session: AsyncSession):
    try:
        if callback_data.menu_name == 'add_to_cart':
            await add_to_cart(callback, callback_data, session)
            return

        if callback_data.menu_name == 'search':
            await callback.answer('Отправьте название товара:')
            return

        answer, reply_markup = await get_menu_content(
            level=callback_data.level,
            menu_name=callback_data.menu_name,
            catalog_id=callback_data.catalog_id,
            session=session,
            page=callback_data.page,
            user_id=callback.from_user.id,
            product_id=callback_data.product_id)

        await callback.message.edit_media(media=answer, reply_markup=reply_markup)
        await callback.answer()
    except Exception as e:
        print(e)


@user_router.message(F.content_type.in_({'text'}))
async def search_by(message: types.Message,
                    session: AsyncSession):
    try:
        media, reply_markup = await get_menu_content(
            level=4,
            menu_name='search',
            catalog_id=None,
            session=session,
            page=1,
            message=message.text)
        await message.answer_photo(
            media.media,
            caption=media.caption,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)
    except Exception as e:
        print(e)
