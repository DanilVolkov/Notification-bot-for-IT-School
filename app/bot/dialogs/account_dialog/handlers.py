from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from app.bot.consts import labels_texts
from app.bot.dialogs.states import AccountSG


async def block_user(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    user_id = dialog_manager.start_data.get('user_id')
    # TODO: изменение статуса пользователя в БД
    # TODO: обновить мидлварь на блокировку пользователя
    await dialog_manager.switch_to(AccountSG.start)


async def activate_user(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    user_id = dialog_manager.start_data.get('user_id')
    # TODO: изменение статуса пользователя в БД


async def del_user(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    user_id = dialog_manager.start_data.get('user_id')
    # TODO: удаление пользователя и получение его ФИО
    user_fio = 'Иванов Иван Иваныч'
    dialog_manager.dialog_data["del_user_id"] = user_id
    dialog_manager.dialog_data["del_user_fio"] = user_fio
    await dialog_manager.switch_to(AccountSG.del_user_done)


async def save_user_fio(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    # TODO: изменение ФИО в БД
    await dialog_manager.switch_to(AccountSG.start)


async def error_info_user(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    await message.answer(labels_texts.INCORRECT_INFO_USER)


async def save_user_role(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    # TODO: изменение роли в БД
    await dialog_manager.switch_to(AccountSG.start)
