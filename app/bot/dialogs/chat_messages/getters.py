import logging

from aiogram_dialog import DialogManager

logger = logging.getLogger(__name__)


async def get_chat_messages(dialog_manager: DialogManager, **kwargs):
    # TODO: получение сообщений из чата их статуса и их парсинг по стикерам
    # chat_id = dialog_manager.start_data.get("chat_id")
    chat_name = dialog_manager.start_data.get("chat_name")

    # TODO: получить статусы сообщений, названия, текста и времени из БД

    # TODO: добавить обработку для стикеров по статусу и формирование сообщения

    messages = [
        ("🕒 <дата> <время> <название>", 1),
        ("✅ 12.01.2026 17:30 Название сообщения", 2),
        ("Название сообщения", 3),
    ]
    return {"chat_name": chat_name, "list_messages": messages}


async def get_chat_name(dialog_manager: DialogManager, **kwargs):
    chat_name = dialog_manager.start_data.get("chat_name")
    return {"chat_name": chat_name}


async def get_chat_info(dialog_manager: DialogManager, **kwargs):
    chat_id = dialog_manager.start_data.get("chat_id")
    chat_name = dialog_manager.start_data.get("chat_name")
    return {"chat_id": chat_id, "chat_name": chat_name}


async def get_found_messages(dialog_manager: DialogManager, **kwargs):
    found_messages = dialog_manager.dialog_data.get("found_messages")
    found_messages = [(chat_name, index) for index, chat_name in enumerate(found_messages)]
    is_found_messages = True if found_messages else False
    return {
        "found_messages": found_messages,
        "is_found_messages": is_found_messages,
        "is_not_found_messages": not is_found_messages,
    }
