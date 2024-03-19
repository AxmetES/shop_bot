from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db.engine import AsyncSession


class DBSession(BaseMiddleware):
    def __init__(self, session_pool: AsyncSession) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)