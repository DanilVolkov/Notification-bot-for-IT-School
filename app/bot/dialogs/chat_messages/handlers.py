import logging
from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.consts import labels_texts
from app.bot.dialogs.states import MessagesSG

logger = logging.getLogger(__name__)


async def set_message_info(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    chat_id = dialog_manager.start_data.get("chat_id")

    dialog_manager.dialog_data["message_id"] = item_id
    message_name = "Название сообщения"  # TODO: получение названия сообщения из БД

    logger.info(f"Получение сообщения {item_id} из чата {chat_id}")

    await dialog_manager.switch_to(MessagesSG.message_info)


async def save_message_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data["message_name"] = text
    await dialog_manager.switch_to(MessagesSG.add_message_text)


async def save_message_text(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data["message_text"] = text
    await dialog_manager.switch_to(MessagesSG.add_message_datetime)


async def save_message_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data["message_datetime"] = text
    # TODO: создание в БД нового сообщения
    # TODO: получение id сообщения
    dialog_manager.dialog_data["message_id"] = 5
    await dialog_manager.switch_to(MessagesSG.message_info)


async def update_message_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):

    # TODO: изменение имени в БД

    await dialog_manager.switch_to(MessagesSG.message_info)


async def update_message_text(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):

    # TODO: изменение текста в БД

    await dialog_manager.switch_to(MessagesSG.message_info)


async def update_message_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):

    # TODO: изменение даты в БД

    await dialog_manager.switch_to(MessagesSG.message_info)


def datetime_check(text: Any) -> str:
    try:
        planned_datetime = datetime.strptime(text, "%d.%m.%Y %H:%M")
    except:
        raise ValueError("Неверный формат даты или времени")
    if planned_datetime <= datetime.now():
        raise ValueError("Время должно быть больше, чем настоящий момент")
    return text


async def error_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    logger.debug(f"Ошибка при добавлении даты и времени: {error}")
    if "Неверный формат даты или времени" in str(error):
        await message.answer(labels_texts.ERROR_TYPE_DATETIME)
    else:
        await message.answer(labels_texts.ERROR_DATETIME)


async def del_message(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer(text=labels_texts.DEL_MESSAGE_PROCESS)
    # TODO: удаление сообщения из БД
    await dialog_manager.switch_to(state=MessagesSG.del_message_done)


async def update_chat_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    # TODO: изменение имени чата

    await dialog_manager.switch_to(state=MessagesSG.start)


async def find_message(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    # TODO: поиск сообщений в БД
    found_messages = [
        "✅ 12.01.2026 17:30 Название сообщения",
        "12.01.2026 17:35 Название сообщения",
    ]  # TODO: найденные чаты в БД
    # found_messages.clear()
    dialog_manager.dialog_data["found_messages"] = found_messages
    await dialog_manager.switch_to(MessagesSG.found_messages)
