from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.bot.dialogs.states import AccountSG


async def start_account_dialog(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    # TODO: передача id пользователя при старте диалога

    await dialog_manager.start(AccountSG.start, data={"user_id": item_id})
