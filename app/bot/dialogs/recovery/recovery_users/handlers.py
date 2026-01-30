from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.bot.dialogs.states import RecoverySG


async def get_user_for_recovery(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    recovery_user_id = item_id  # TODO: поменять на название из БД
    recovery_username = 'Иванов Иван Иванович'  # TODO: поменять на название из БД
    dialog_manager.dialog_data['recovery_user_id'] = recovery_user_id
    dialog_manager.dialog_data['recovery_username'] = recovery_username
    await dialog_manager.switch_to(state=RecoverySG.confirm_recovery_user)


async def recovery_user(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    recovery_user_id = dialog_manager.dialog_data.get('recovery_user_id')
    # TODO: восстановление пользователя - перенос пользователя из таблицы удалённых
    await dialog_manager.switch_to(state=RecoverySG.recovery_user_done)