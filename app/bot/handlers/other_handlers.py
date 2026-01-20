import logging
from datetime import datetime
from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from app.bot.consts import labels_texts

logger = logging.getLogger(__name__)


async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer(labels_texts.NO_TEXT)


def datetime_check(text: Any) -> str:
    try:
        planned_datetime = datetime.strptime(text, "%d.%m.%Y %H:%M")
    except:  # noqa
        raise ValueError("Неверный формат даты или времени")  # noqa
    if planned_datetime <= datetime.now():
        raise ValueError("Время должно быть больше, чем настоящий момент")
    return text


async def error_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    logger.debug(f"Ошибка при добавлении даты и времени: {error}")
    if "Неверный формат даты или времени" in str(error):
        await message.answer(labels_texts.ERROR_TYPE_DATETIME)
    else:
        await message.answer(labels_texts.ERROR_DATETIME)
