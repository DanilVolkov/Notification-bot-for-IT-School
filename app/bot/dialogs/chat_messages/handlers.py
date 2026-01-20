import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.dialogs.states import ChatMessagesSG, MessageInfoSG

logger = logging.getLogger(__name__)


async def set_message_info(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    chat_id = dialog_manager.start_data.get("chat_id")

    logger.info(f"Получение сообщения {item_id} из чата {chat_id}")

    await dialog_manager.start(MessageInfoSG.start, data={"message_id": item_id, "chat_id": chat_id})


async def save_message_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await dialog_manager.switch_to(ChatMessagesSG.add_message_text)


async def save_message_text(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await dialog_manager.switch_to(ChatMessagesSG.add_message_datetime)


async def save_message_datetime(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    chat_id = dialog_manager.start_data.get("chat_id")
    # TODO: создание в БД нового сообщения одной отдельной функцией
    # TODO: получение id сообщения
    await dialog_manager.switch_to(ChatMessagesSG.start)
    await dialog_manager.start(MessageInfoSG.start, data={"message_id": 5, "chat_id": chat_id})


async def save_message_without_datetime(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    chat_id = dialog_manager.start_data.get("chat_id")
    # TODO: создание в БД нового сообщения одной отдельной функцией
    # TODO: получение id сообщения
    await dialog_manager.switch_to(ChatMessagesSG.start)
    await dialog_manager.start(MessageInfoSG.start, data={"message_id": 5, "chat_id": chat_id})


async def update_chat_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    # TODO: изменение имени чата

    await dialog_manager.switch_to(state=ChatMessagesSG.start)


async def find_message(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    # TODO: поиск сообщений в БД
    found_messages = [
        "✅ 12.01.2026 17:30 Название сообщения",
        "12.01.2026 17:35 Название сообщения",
    ]  # TODO: найденные чаты в БД
    # found_messages.clear()
    dialog_manager.dialog_data["found_messages"] = found_messages
    await dialog_manager.switch_to(ChatMessagesSG.found_messages)
