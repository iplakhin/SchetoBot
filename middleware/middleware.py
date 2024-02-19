from typing import Callable, Dict, Any, Awaitable, Union

from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject, Update

from db.db import get_user, create_user, check_permission


class RegistrationCheck(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update,
                       data: Dict[str, Any]):
        user = await get_user(event.message.from_user.id)
        if not user:
            await create_user(event.message.from_user.id)
        return handler(event, data)


class PermissionCheck(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update,
                       data: Dict[str, Any]):
        user = get_user(event.message.from_user.id)
        if user is None:
            create_user(event.message.from_user.id)
        if not check_permission(event.message.from_user.id):
            await event.message.answer("Доступ запрещен!")
            raise CancelHandler('Unauthorized access!')
        return await handler(event, data)
