from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.bot.consts import labels_texts
from app.bot.dialogs.states import RecoverySG


async def set_chat_for_recovery(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    recovery_chat_id = item_id  # TODO: поменять на название из БД
    recovery_chat_name = 'Python для начинающих'  # TODO: поменять на название из БД
    dialog_manager.dialog_data['recovery_chat_id'] = recovery_chat_id
    dialog_manager.dialog_data['recovery_chat_name'] = recovery_chat_name
    await dialog_manager.switch_to(state=RecoverySG.recovery_messages_for_chat)


async def set_recovery_msg_mode(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    recovery_mode = ''
    match button.widget_id:
        case 'btn_recovery_msg_with_dates':
            recovery_mode = labels_texts.RECOVERY_MSG_WITH_DATES
        case 'btn_recovery_msg_without_dates':
            recovery_mode = labels_texts.RECOVERY_MSG_WITHOUT_DATES
        case 'btn_recovery_only_chat':
            recovery_mode = labels_texts.RECOVERY_ONLY_CHAT
        case _:
            recovery_mode = ''

    dialog_manager.dialog_data['recovery_mode'] = recovery_mode

    await dialog_manager.switch_to(state=RecoverySG.confirm_recovery_chat)


async def recovery_chat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    recovery_chat_id = dialog_manager.dialog_data.get('recovery_chat_id')
    recovery_mode = dialog_manager.dialog_data.get('recovery_mode')
    # TODO: восстановление чата - перенос пользователя из таблицы удалённых
    # TODO: восстановление сообщений чата при выбранном режиме
    match recovery_mode:
        case labels_texts.RECOVERY_MSG_WITH_DATES:
            pass
        case labels_texts.RECOVERY_MSG_WITHOUT_DATES:
            pass
        case labels_texts.RECOVERY_ONLY_CHAT:
            pass

    await dialog_manager.switch_to(state=RecoverySG.recovery_chat_done)