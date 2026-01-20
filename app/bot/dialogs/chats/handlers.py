import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.consts import labels_texts
from app.bot.dialogs.states import ChatMessagesSG, ChatsSG

logger = logging.getLogger(__name__)


async def save_chat_from_copy(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    logger.debug(f"Выбран чат, откуда копировать, с id={item_id}")  # TODO: поменять на название из БД
    dialog_manager.dialog_data["chat_from_id"] = item_id  # TODO: поменять на название
    await dialog_manager.switch_to(state=ChatsSG.copy_messages_in_chat)


async def copy_messages(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    logger.debug(f"Выбран чат, куда копировать, с id={item_id}")  # TODO: поменять на название

    if dialog_manager.dialog_data.get("chat_from_id") == item_id:
        await callback.answer(text=labels_texts.ALERT_COPY_CHAT, show_alert=True)
        return

    await callback.answer(text=labels_texts.COPY_MESSAGES)

    logger.debug(
        f"Копирование сообщений из чата с id = {dialog_manager.dialog_data.get('chat_from_id')} в чат с id {item_id}"
    )  # TODO: поменять на название
    dialog_manager.dialog_data["chat_in_id"] = item_id  # TODO: поменять на название
    # TODO: обмен данными с БД
    await dialog_manager.switch_to(state=ChatsSG.copy_messages_done)


async def confirm_del_chat(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    logger.debug(f"Выбран чат для удаления, с id={item_id}")
    dialog_manager.dialog_data["chat_del_id"] = item_id
    dialog_manager.dialog_data["chat_del_name"] = "Название чата"  # TODO: поменять на название из БД
    dialog_manager.dialog_data["chat_del_confirm"] = False
    await dialog_manager.switch_to(state=ChatsSG.del_chat_confirm)


async def del_chat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logger.info(
        f"Удаление чата: id={dialog_manager.dialog_data.get('chat_del_id')}, "
        f"name={dialog_manager.dialog_data['chat_del_name']}"
    )
    dialog_manager.dialog_data["chat_del_confirm"] = True
    await callback.answer(text=labels_texts.DEL_CHAT_PROCESS)
    # TODO: обмен данными с БД
    await dialog_manager.switch_to(state=ChatsSG.del_chat_done)


async def find_chat(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    logger.info(f"Поиск чатов по запросу: {message.text}")
    # TODO: поиск чатов в БД
    found_chats = ["Базовый Python 2026 1 поток", "Базовый Python 2026 2 поток"]  # TODO: найденные чаты в БД
    # found_chats.clear()
    dialog_manager.dialog_data["found_chats"] = found_chats
    await dialog_manager.switch_to(ChatsSG.found_chats)


async def start_chat_messages_dialog(
    callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str
):

    logger.info(f"Выбран чат {item_id}")  # TODO: поменять на название из БД
    chat_id = item_id  # TODO: здесь должен быть id чата из БД
    chat_name = "Базовый Python 2026 1 поток"  # TODO: здесь название чата (бот) из БД
    # TODO: добавить обработчик ошибок
    logger.debug("Переходим в диалог MessagesSG")
    await dialog_manager.switch_to(state=ChatsSG.start)
    await dialog_manager.start(ChatMessagesSG.start, data={"chat_id": chat_id, "chat_name": chat_name})
