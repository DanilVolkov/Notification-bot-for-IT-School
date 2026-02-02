from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.dialogs.states import RecoverySG


async def set_chat_messages_for_recovery(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    chat_recovery_msgs_id = item_id  # TODO: поменять на id из БД
    chat_recovery_msgs_name = (
        'Python для начинающих'  # TODO: поменять на название из БД
    )
    dialog_manager.dialog_data['chat_recovery_msgs_id'] = chat_recovery_msgs_id
    dialog_manager.dialog_data['chat_recovery_msgs_name'] = (
        chat_recovery_msgs_name
    )
    # True, если чат удален, иначе False
    dialog_manager.dialog_data['is_chat_recovery_msgs_del'] = False
    await dialog_manager.switch_to(state=RecoverySG.list_del_messages_in_chat)


async def set_del_message_info(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    recovery_msgs_id = item_id  # TODO: поменять на id из БД
    dialog_manager.dialog_data['recovery_message_id'] = recovery_msgs_id
    await dialog_manager.switch_to(state=RecoverySG.confirm_recovery_messages)


async def recovery_message(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    pass
