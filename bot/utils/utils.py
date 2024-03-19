import math

import aiofiles
from aiogram.filters.callback_data import CallbackData
from aiogram.types import file


class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array
        self.page = page
        self.per_page = per_page
        self.len = len(self.array)
        self.pages = math.ceil(self.len / per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False


class MenuCallBack(CallbackData, prefix='menu'):
    level: int
    menu_name: str
    catalog_id: int | None = None
    page: int = 1
    product_id: int | None = None


class PaginatorDict:
    def __init__(self, array: list | tuple | dict, page: int=1, per_page: int=1):
        self.array = array
        self.page = page
        self.per_page = per_page
        self.len = len(self.array)
        self.pages = math.ceil(self.len / per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False


async def save_bytes_to_image(filename: str, data: bytes):
    async with aiofiles.open(filename, 'wb') as f:
        await f.write(data)