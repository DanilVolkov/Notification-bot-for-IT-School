import logging
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class RoleMiddleware(BaseMiddleware):
    def __init__(self, admins: list[int]):
        self._admins = [int(el) for el in admins]

    async def __call__(
        self, handler: Callable[[TelegramObject, dict[str, Any]], Any], event: TelegramObject, data: dict[str, Any]
    ) -> Any:
        # logger.debug(event.model_dump_json(indent=4, exclude_none=True))
        user_id = int(data.get('event_from_user').id)

        role = await self.get_user_role(user_id)
        # TODO: добавить получение всей информации о пользователе
        # Добавляем в контекст
        data['user_role'] = role

        logger.debug(f'Добавили роль: {role}')

        return await handler(event, data)

    async def get_user_role(self, user_id: int) -> str:
        # TODO: сделать загрузку из БД
        if user_id in self._admins:
            return 'создатель'
        return 'неопознан'  # по умолчанию — неопознан
