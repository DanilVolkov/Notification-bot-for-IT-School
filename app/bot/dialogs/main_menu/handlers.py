from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.bot.dialogs.states import AccountSG


async def start_account_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AccountSG.start, data={"user_id": callback.from_user.id})
