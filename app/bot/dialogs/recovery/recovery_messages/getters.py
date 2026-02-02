from aiogram_dialog import DialogManager


async def get_chats_del_messages(dialog_manager: DialogManager, **kwargs):
    # TODO: сделать получение чатов для удаленных сообщений

    chats = [
        ('Базовый Python 2026 1 поток', 1),
        # Если чат удалён, то его удалённые сообщения можно показать, но восстановить их будет нельзя
        ('❌ (удалён) Docker 2026 1 поток', 2),
        ('Javascript junior', 3),
    ]


    return {'list_chats': chats}


async def get_chat_messages_for_recovery(dialog_manager: DialogManager, **kwargs):
    chat_recovery_msgs_id = dialog_manager.dialog_data.get('chat_recovery_msgs_id')
    is_chat_recovery_msgs_del = dialog_manager.dialog_data.get('is_chat_recovery_msgs_del')
    # TODO: получение списка сообщений из таблицы удаленных сообщений по фильтру чата
    del_messages = [
        ('🕒 <дата> <время> <название>', 1),
        ('✅ 12.01.2026 17:30 Название сообщения', 2),
        ('Название сообщения', 3),
    ]
    return {
        'is_chat_recovery_msgs_del': is_chat_recovery_msgs_del,
        'del_messages': del_messages
    }


async def get_recovery_message_info(dialog_manager: DialogManager, **kwargs):
    is_chat_recovery_msgs_del = dialog_manager.dialog_data.get('is_chat_recovery_msgs_del')
    # TODO: получение информации сообщения по id сообщения
    recovery_message_id = dialog_manager.dialog_data.get('recovery_message_id')

    # TODO: вынести из message_info/getters -> get_message_info функции в other_handlers
    recovery_message_info = ''


    return {
        'is_chat_recovery_msgs_del': is_chat_recovery_msgs_del,
        'recovery_message_info': recovery_message_info
    }
