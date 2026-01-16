import logging

from aiogram_dialog import DialogManager


logger = logging.getLogger(__name__)

async def get_chat_info(dialog_manager: DialogManager, **kwargs):
    chat_id = dialog_manager.start_data.get("chat_id")
    chat_name = dialog_manager.start_data.get("chat_name")
    return {'chat_id': chat_id, 'chat_name': chat_name}

async def get_chat_messages(dialog_manager: DialogManager, **kwargs):
    # TODO: получение сообщений из чата и их парсинг по стикерам
    chat_name = dialog_manager.start_data.get("chat_name")
    messages = [
        ('🕒 <дата> <время> <название>', 1),
        ('✅ 12.01.2026 17:30 Название сообщения', 2),
        ('Название сообщения', 3)
    ]
    return {'chat_name': chat_name, 'list_messages': messages}